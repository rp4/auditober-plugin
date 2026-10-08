#!/usr/bin/env python3
"""Deterministic seed builder for coach-starter-pack.

Merges the canonical schema base + an optional controlsmap export + optional
own-data (CSV/JSON) into ONE coworkcanvas bulk-import envelope: unified controls
become `control` items, standards become the control's `framework` value, risks
become `risk` items. Dedups controls and gap-patches uncovered unified controls."""
import argparse
import csv
import json
import sys
from pathlib import Path

CANONICAL_FRAMEWORKS = {
    "nist-800-53", "nist-csf-2", "cobit-2019", "iso-27001", "iso-42001", "iso-31000",
    "soc2", "soc1", "sox", "coso-ic", "coso-erm", "iia-2024", "gdpr", "dora",
    "nydfs-500", "eu-ai-act", "nis2", "pci-dss", "hipaa", "ccpa",
}
FRAMEWORK_ALIASES = {
    "iia-pos-2026-erm": "iia-2024",
    "iia-pos-2026-three-lines": "iia-2024",
}
CANONICAL_DOMAINS = {
    "governance_policy_oversight", "risk_assessment_management", "asset_management_inventory",
    "access_control_identity", "cryptography_key_management", "human_resources_personnel_security",
    "physical_environmental_security", "secure_configuration_change_management",
    "vulnerability_patch_management", "logging_monitoring_detection", "incident_management_response",
    "business_continuity_disaster_recovery", "third_party_supply_chain_risk", "data_protection_privacy",
    "secure_development_sdlc", "network_communications_security", "awareness_training",
    "compliance_audit_assurance", "ai_governance", "financial_reporting_controls",
}
# controlsmap UC exports carry the domain's DISPLAY LABEL, not the slug; the
# labels equal core.json's own `domains` option labels (both regenerated from
# the same compliance graph — pinned by test_domain_aliases_match_core_json_labels).
# Several labels contain commas, so a domain value is one atom, never comma-split.
DOMAIN_ALIASES = {
    "Governance, Policy & Oversight": "governance_policy_oversight",
    "Risk Assessment & Management": "risk_assessment_management",
    "Asset Management & Inventory": "asset_management_inventory",
    "Access Control & Identity Management": "access_control_identity",
    "Cryptography & Key Management": "cryptography_key_management",
    "Human Resources / Personnel Security": "human_resources_personnel_security",
    "Physical & Environmental Security": "physical_environmental_security",
    "Secure Configuration & Change Management": "secure_configuration_change_management",
    "Vulnerability & Patch Management": "vulnerability_patch_management",
    "Logging, Monitoring & Detection": "logging_monitoring_detection",
    "Incident Management & Response": "incident_management_response",
    "Business Continuity & Disaster Recovery": "business_continuity_disaster_recovery",
    "Third-Party / Supply-Chain Risk": "third_party_supply_chain_risk",
    "Data Protection & Privacy": "data_protection_privacy",
    "Secure Development (SDLC) & Application Security": "secure_development_sdlc",
    "Network & Communications Security": "network_communications_security",
    "Awareness & Training": "awareness_training",
    "Compliance, Audit & Assurance": "compliance_audit_assurance",
    "AI Governance": "ai_governance",
    "Financial Reporting Controls (SOX)": "financial_reporting_controls",
}
# Canonical `risk` enums (core.json risk type; pinned by test_risk_enums_match_core_json).
# Gated because an off-enum SELECT/MULTISELECT value fails the whole row at
# import — and the live controlsmap vocabulary does not fully fit: risk
# category "financial" has no canonical bucket, and the export's taxonomies
# (iso-27005-threat, nist-800-30-*, coso-erm-risk, ...) are taxonomy SOURCES,
# disjoint from the canonical risk-theme values below.
RISK_CATEGORIES = {
    "cyber_security", "operational", "financial_reporting", "compliance_regulatory",
    "third_party", "privacy", "ai_governance", "strategic", "reputational", "esg",
    "people_hr", "business_continuity",
}
RISK_TAXONOMIES = {
    "cyber_security", "data_privacy", "financial_reporting", "operational_resilience",
    "third_party_risk", "ai_governance", "esg_sustainability", "people_hr",
    "regulatory_compliance", "strategic_risk", "reputational_risk", "business_continuity",
}


def _map_values(values, canonical, aliases=None):
    """Map a list of raw values onto a canonical enum via an optional alias
    table. Returns (mapped, unmapped) with order preserved and duplicates
    removed; empty entries are skipped. Unmapped values are surfaced for the
    caller — never emitted off-enum, never silently dropped."""
    if isinstance(values, str):
        raise TypeError(
            f"expected a list of values, got a bare str {values!r} — a string "
            "would be iterated character-by-character; wrap it in a list or use _split()")
    aliases = aliases or {}
    mapped, unmapped = [], []
    for raw in values or []:
        v = (raw or "").strip()
        if not v:
            continue
        cv = aliases.get(v, v)
        if cv in canonical:
            if cv not in mapped:
                mapped.append(cv)
        elif v not in unmapped:
            unmapped.append(v)
    return mapped, unmapped


def crosswalk_frameworks(values):
    """Map controlsmap framework ids onto the canonical framework enum.
    Returns (mapped, unmapped) with order preserved and duplicates removed."""
    return _map_values(values, CANONICAL_FRAMEWORKS, FRAMEWORK_ALIASES)


def _split(value):
    """Split a delimited string (comma or semicolon) into a clean list."""
    if isinstance(value, list):
        return [str(x).strip() for x in value if str(x).strip()]
    if not value:
        return []
    parts = str(value).replace(";", ",").split(",")
    return [p.strip() for p in parts if p.strip()]


def _as_list(value):
    """Wrap a scalar as a one-element list WITHOUT splitting it — for values
    that are one atom even when they contain commas (domain display labels)."""
    if isinstance(value, list):
        return value
    return [value] if value else []


def uc_to_control(uc_item):
    """controlsmap unified_control item -> canonical control item.

    The UC's comma-joined `frameworks` string feeds the crosswalk via _split;
    `unified_id` becomes control_id; `statement` becomes full_description (and,
    truncated, description); `domain` — a display label in real exports, e.g.
    "Access Control & Identity Management" — maps onto the canonical `domains`
    slug enum via DOMAIN_ALIASES. Status is the canonical control defaultStatus
    (ACTIVE); visibility is rewritten to "public" (the export's "team" is not a
    canvas item visibility — the importer would normalize it to private).
    Unmapped frameworks/domains are attached under fields['_unmapped_framework']
    / fields['_unmapped_domain'] for the caller to surface."""
    f = uc_item.get("fields", {})
    mapped, unmapped = crosswalk_frameworks(_split(f.get("frameworks")))
    domains, unmapped_domains = _map_values(
        _as_list(f.get("domain")), CANONICAL_DOMAINS, DOMAIN_ALIASES)
    fields = {
        "control_id": f.get("unified_id"),
        "framework": mapped,
        "domains": domains,
        "control_type": f.get("control_type") or None,
        "control_category": f.get("control_category") or None,
        "full_description": f.get("statement"),
        "description": (f.get("statement") or "")[:280] or None,
    }
    if unmapped:
        fields["_unmapped_framework"] = unmapped
    if unmapped_domains:
        fields["_unmapped_domain"] = unmapped_domains
    return {"title": uc_item.get("title"), "status": "ACTIVE", "visibility": "public",
            "fields": {k: v for k, v in fields.items() if v not in (None, [], "")}}


def cm_risk_to_risk(cm_item):
    """controlsmap risk item -> canonical risk item.

    The export's risk_id has no canonical home and is deliberately dropped.
    `category` and `taxonomies` are gated against the canonical risk enums (an
    off-enum SELECT/MULTISELECT value fails the whole row at import) with
    non-canonical values surfaced under fields['_unmapped_category'] /
    fields['_unmapped_taxonomy']. The severity scales (likelihood, impact,
    inherent_rating, treatment) pass through — the live controlsmap vocabulary
    is a subset of the canonical enums for all four. Status is the canonical
    risk defaultStatus (OPEN)."""
    f = cm_item.get("fields", {})
    cats, unmapped_cat = _map_values(_as_list(f.get("category")), RISK_CATEGORIES)
    taxes, unmapped_tax = _map_values(_split(f.get("taxonomies")), RISK_TAXONOMIES)
    fields = {
        "category": cats[0] if cats else None,
        "taxonomies": taxes,
        "likelihood": f.get("likelihood") or None,
        "impact": f.get("impact") or None,
        "inherent_rating": f.get("inherent_rating") or None,
        "treatment": f.get("treatment") or None,
    }
    # `category` is a single-valued SELECT, so only cats[0] can be emitted —
    # surface any extra canonical entries alongside the off-enum ones rather
    # than silently discarding them.
    if unmapped_cat or cats[1:]:
        fields["_unmapped_category"] = unmapped_cat + cats[1:]
    if unmapped_tax:
        fields["_unmapped_taxonomy"] = unmapped_tax
    return {"title": cm_item.get("title"), "status": "OPEN", "visibility": "public",
            "fields": {k: v for k, v in fields.items() if v not in (None, [], "")}}


# --- own data: a user's OWN controls/risks from CSV or JSON ------------------
#
# Scalar SELECT enums per type. Pinned to core.json (the authority on which
# fields exist and what values they accept) by TestOwnDataEnumsMatchCoreJson,
# which also asserts EVERY SELECT/MULTISELECT field of each type is gated —
# an off-enum value in any of them hard-fails the whole row at import.
# key_control is a SELECT whose option VALUES are the strings "true"/"false"
# (not a BOOLEAN field) — quirky but canonical.
_CONTROL_ENUMS = {
    "control_type": {"preventive", "detective", "corrective"},
    "control_category": {"administrative", "technical", "physical"},
    "control_class": {"entity_level", "business_process", "itgc", "itac",
                      "soc1_service_delivery"},
    "itgc_domain": {"access_to_programs_data", "program_changes", "computer_operations",
                    "program_development", "end_user_computing"},
    "automation": {"automated", "manual", "hybrid"},
    "key_control": {"true", "false"},
    "frequency": {"continuous", "daily", "weekly", "monthly", "quarterly",
                  "semi_annual", "annual", "ad_hoc"},
    "design_conclusion": {"not_assessed", "effective", "deficient"},
    "interim_result": {"not_tested", "in_progress", "effective", "exception"},
    "ye_result": {"not_tested", "in_progress", "effective", "exception"},
    "rollforward_strategy": {"full_retest", "roll_forward", "interim_sufficient",
                             "not_required"},
}
_RISK_ENUMS = {
    "category": RISK_CATEGORIES,
    "likelihood": {"low", "medium", "high", "very_high"},
    "impact": {"low", "medium", "high", "critical"},
    "inherent_likelihood": {"low", "medium", "high", "very_high"},
    "inherent_impact": {"low", "medium", "high", "critical"},
    "inherent_rating": {"low", "medium", "high", "critical"},
    "residual_rating": {"low", "medium", "high", "critical"},
    "treatment": {"mitigate", "accept", "transfer", "avoid"},
}
# MULTISELECT fields per type: (canonical enum, alias table).
_CONTROL_MULTI_ENUMS = {
    "framework": (CANONICAL_FRAMEWORKS, FRAMEWORK_ALIASES),
    "domains": (CANONICAL_DOMAINS, DOMAIN_ALIASES),
}
_RISK_MULTI_ENUMS = {
    "taxonomies": (RISK_TAXONOMIES, None),
    "domains": (CANONICAL_DOMAINS, DOMAIN_ALIASES),
}
# Every fieldKey that exists on the type in core.json (drift-pinned). A key
# outside this set still passes through, but is flagged in _issues — the
# canvas importer DROPS unknown keys silently, so an unflagged typo
# ("contorl_type") would vanish at import without trace.
_CONTROL_FIELDS = {
    "control_id", "description", "full_description", "framework", "family",
    "domains", "control_type", "control_category", "control_class", "itgc_domain",
    "automation", "key_control", "sox_applicable", "frequency", "locations",
    "control_owner",
    # SOX-testing cycle fields (canonical seed 2026-08): the results/conclusion
    # SELECTs are enum-gated above; workpaper is a DOCUMENT field (populated via
    # upload_document, never seeded) and last_tested_fy is free TEXT.
    "design_conclusion", "interim_result", "ye_result", "rollforward_strategy",
    "last_tested_fy", "workpaper",
}
_RISK_FIELDS = {
    "description", "full_description", "category", "subcategory", "taxonomies",
    "domains", "likelihood", "impact", "inherent_likelihood", "inherent_impact",
    "inherent_rating", "residual_rating", "treatment", "risk_owner",
}
_DEFAULT_STATUS = {"control": "ACTIVE", "risk": "OPEN"}  # core.json defaultStatus


def _unmapped_key(field_key):
    """The `_unmapped_*` channel name for a field (Task-3 singular spellings)."""
    return {"domains": "_unmapped_domain", "taxonomies": "_unmapped_taxonomy"}.get(
        field_key, "_unmapped_" + field_key)


def _canon_token(value):
    """Case/separator-normalize a scalar enum candidate: 'Very High' ->
    'very_high', True -> 'true'. Safe because every canonical scalar option is
    lowercase snake_case (hyphens appear only in framework ids, which are
    multi-valued and crosswalked, never scalar-gated)."""
    return str(value).strip().lower().replace("-", "_").replace(" ", "_")


def _split_domains(value):
    """Split a domains cell. Semicolon is the authoritative delimiter — domain
    display labels contain commas ("Governance, Policy & Oversight"), so a
    comma-only cell is comma-split ONLY when it isn't itself one known
    label/slug."""
    if isinstance(value, list):
        return [str(x).strip() for x in value if str(x).strip()]
    if not value:
        return []
    s = str(value).strip()
    if ";" in s:
        return [p.strip() for p in s.split(";") if p.strip()]
    if s in DOMAIN_ALIASES or s in CANONICAL_DOMAINS:
        return [s]
    return [p.strip() for p in s.split(",") if p.strip()]


def _row_to_item(row, kind):
    """One csv.DictReader row -> item shape (title/status/visibility/fields).
    Header names are stripped+lowercased; empty cells are omitted; extra cells
    beyond the header (DictReader's restkey=None) are surfaced, never dropped."""
    fields, issues = {}, []
    title = ""
    for k, v in row.items():
        if k is None:  # row had more cells than the header has columns
            extras = [str(x).strip() for x in (v or []) if str(x).strip()]
            if extras:
                fields["_unmapped_extra_cells"] = extras
                issues.append(
                    f"row has {len(extras)} more cell(s) than header columns: {extras}")
            continue
        key = k.strip().lower()
        if isinstance(v, str):
            v = v.strip()
        if v in (None, ""):
            continue
        if key == "title":
            title = v
        else:
            fields[key] = v
    item = {"title": title, "status": _DEFAULT_STATUS[kind], "visibility": "public",
            "fields": fields}
    if issues:
        item["_issues"] = issues
    return item


def _normalize(item, scalar_enums, multi_enums, known_fields):
    """Gate an item's fields against the canonical enums. Off-enum values are
    WITHHELD from the emitted field (an invalid SELECT/MULTISELECT value fails
    the whole row at import) and surfaced under fields['_unmapped_<field>']
    plus a human-readable item['_issues'] entry. Unknown field keys are kept
    but flagged (the importer drops unknown keys silently). Empty values are
    stripped. Idempotent on already-canonical items."""
    issues = list(item.get("_issues") or [])
    fields = dict(item.get("fields") or {})
    for key, (canonical, aliases) in multi_enums.items():
        if key not in fields:
            continue
        raw = fields.pop(key)
        values = _split_domains(raw) if key == "domains" else _split(raw)
        mapped, unmapped = _map_values(values, canonical, aliases)
        if mapped:
            fields[key] = mapped
        if unmapped:
            fields.setdefault(_unmapped_key(key), []).extend(unmapped)
            issues.append(f"{key}: {unmapped} not in the canonical options; withheld")
    for key, allowed in scalar_enums.items():
        if key not in fields:
            continue
        raw = fields.pop(key)
        if raw in (None, ""):
            continue
        token = _canon_token(raw)
        if token in allowed:
            fields[key] = token
        else:
            fields.setdefault(_unmapped_key(key), []).append(str(raw).strip())
            issues.append(f"{key}={raw!r} not in {sorted(allowed)}; withheld")
    for key in fields:
        if not key.startswith("_") and key not in known_fields:
            issues.append(f"unknown field {key!r} (not on the canonical type; "
                          "the importer would silently drop it)")
    if not (item.get("title") or "").strip():
        issues.append("missing title")
    out = dict(item)
    out["fields"] = {k: v for k, v in fields.items() if v not in (None, "", [])}
    if issues:
        out["_issues"] = issues
    else:
        out.pop("_issues", None)
    return out


def normalize_control(raw):
    """User-supplied control item -> canonical-safe control item (see _normalize)."""
    return _normalize(raw, _CONTROL_ENUMS, _CONTROL_MULTI_ENUMS, _CONTROL_FIELDS)


def normalize_risk(raw):
    """User-supplied risk item -> canonical-safe risk item (see _normalize)."""
    return _normalize(raw, _RISK_ENUMS, _RISK_MULTI_ENUMS, _RISK_FIELDS)


def own_rows_to_items(path, kind):
    """Parse a user's own controls/risks (.csv or .json) into canonical items.

    kind: "control" | "risk". CSV: one row per item, `title` column required;
    multi-value columns (framework/domains/taxonomies) are ;- or ,-delimited
    (semicolons are the safe delimiter for domain display labels, which contain
    commas). JSON: a list — or {"items": [...]} — of flat rows shaped like the
    CSV, or of already-item-shaped {"title", "fields": {...}} objects. Every
    item is normalized on the way out (normalize_control / normalize_risk), so
    no emitted row carries an off-enum SELECT/MULTISELECT value that would
    hard-fail at import; problems are surfaced under fields['_unmapped_*'] and
    item['_issues']."""
    if kind not in _DEFAULT_STATUS:
        raise ValueError(f"kind must be one of {sorted(_DEFAULT_STATUS)}, got {kind!r}")
    p = Path(path)
    suffix = p.suffix.lower()
    if suffix == ".json":
        data = json.loads(p.read_text(encoding="utf-8-sig"))
        if isinstance(data, list):
            rows = data
        elif isinstance(data, dict) and isinstance(data.get("items"), list):
            rows = data["items"]
        else:
            raise ValueError(f"{path}: expected a JSON list of rows or an object "
                             "with an 'items' list")
        items = []
        for i, r in enumerate(rows):
            if not isinstance(r, dict):
                raise ValueError(f"{path}: row {i} is not an object: {r!r}")
            if isinstance(r.get("fields"), dict):  # already item-shaped
                item = dict(r)
                item.setdefault("status", _DEFAULT_STATUS[kind])
                item.setdefault("visibility", "public")
            else:                                  # flat row -> wrap like a CSV row
                fields, title = {}, ""
                for k, v in r.items():
                    key = str(k).strip().lower()
                    if v in (None, ""):
                        continue
                    if key == "title":
                        title = str(v).strip()
                    else:
                        fields[key] = v
                item = {"title": title, "status": _DEFAULT_STATUS[kind],
                        "visibility": "public", "fields": fields}
            items.append(item)
    elif suffix == ".csv":
        with p.open(newline="", encoding="utf-8-sig") as fh:
            items = [_row_to_item(r, kind) for r in csv.DictReader(fh)]
    else:
        raise ValueError(f"{path}: unsupported extension {suffix!r} "
                         "(expected .csv or .json)")
    norm = normalize_control if kind == "control" else normalize_risk
    return [norm(i) for i in items]


# --- dedup + coverage/gap-patch against the unified-control baseline ---------
#
# The unified-control set is the coverage baseline (the complete "comply-once"
# objectives). The user's existing controls are the starting point: where one
# already satisfies a UC, that UC must NOT be added again (dedup_controls +
# covered_and_gaps); every UC not covered becomes a proposed new control (the
# gap patch), surfaced for human approval — never patched silently. Coverage
# is judged hybrid: deterministically when a control_id resolves through the
# export's `satisfies` relationships (uc_coverage_map), otherwise via an
# agent-supplied overrides map carrying the semantic judgment.


def _deep_copy(obj):
    """Deep-copy a JSON-shaped item (every builder item is JSON-shaped)."""
    return json.loads(json.dumps(obj))


def _dedup_key(control):
    """Case-insensitive control_id, falling back to the title for id-less
    rows. The 'title:' prefix keeps id keys and title keys from
    cross-colliding (a row WITH an id never merges into a title-keyed row)."""
    f = control.get("fields") or {}
    cid = str(f.get("control_id") or "").strip().lower()
    return cid or ("title:" + str(control.get("title") or "").strip().lower())


def dedup_controls(controls):
    """Collapse controls sharing a control_id (case-insensitive; title
    fallback for id-less rows) into the first occurrence, first-seen order
    preserved, inputs never mutated (outputs are deep copies).

    Nothing is silently lost when rows collapse:
      - list-valued fields (framework, domains, _unmapped_*, ...) UNION,
        order-preserved;
      - a field missing on the kept row is adopted from the duplicate;
      - a conflicting scalar keeps the FIRST value and surfaces the losing
        value in item['_issues'] (control_id casing differences are not
        conflicts — the key already treats them as equal);
      - merged-away titles are recorded under item['_merged'] (and accepted
        as override keys by covered_and_gaps).

    KNOWN LIMIT (surfaced, not silent): two genuinely different framework
    controls can share a bare id — in the live compliance graph ISO-27001
    and ISO-42001 both number 13 Annex-A ids (A.5.2, ...). Those collapse
    too, with frameworks unioned and both titles/_issues visible, for the
    human to split back apart if they are truly distinct controls."""
    by_key, order = {}, []
    for c in controls or []:
        k = _dedup_key(c)
        if k not in by_key:
            by_key[k] = _deep_copy(c)
            order.append(k)
            continue
        kept = by_key[k]
        fields = kept.setdefault("fields", {})
        issues = list(kept.get("_issues") or [])
        merged = list(kept.get("_merged") or [])
        dup_title = str(c.get("title") or "").strip()
        for t in [dup_title] + list(c.get("_merged") or []):
            if t and t not in merged:
                merged.append(t)
        for key, dv in (c.get("fields") or {}).items():
            if key not in fields:
                fields[key] = _deep_copy(dv)
            elif isinstance(fields[key], list) and isinstance(dv, list):
                unioned = list(fields[key])
                for v in dv:
                    if v not in unioned:
                        unioned.append(v)
                fields[key] = unioned
            elif fields[key] != dv:
                if (key == "control_id"
                        and str(fields[key]).strip().lower()
                        == str(dv).strip().lower()):
                    continue
                issues.append(
                    f"dedup: {key}={dv!r} from duplicate {dup_title or k!r} "
                    f"conflicts with kept {fields[key]!r}; kept the first")
        for extra in c.get("_issues") or []:
            if extra not in issues:
                issues.append(extra)
        if merged:
            kept["_merged"] = merged
        if issues:
            kept["_issues"] = issues
    return [by_key[k] for k in order]


def uc_coverage_map(export):
    """framework control_id -> unified-control title, from the export's
    `satisfies` relationships (control -> unified_control) joined to the
    granular `control` items by item title. Faithful to the controls-map
    buildEnvelope() shapes: relationships carry sourceItemTitle /
    targetItemTitle (+ItemType each) and `kind`; control items carry
    fields.control_id and fields.framework.

    Keys are lowercase, two forms per satisfying control: bare ('cc6.1')
    and framework-qualified ('soc2:cc6.1'). A value is the uc_title string
    when the key resolves to exactly ONE unified control. When different
    frameworks reuse a bare id for DIFFERENT unified controls (live case:
    ISO-27001 vs ISO-42001 share 13 Annex-A ids) the bare value is the
    SORTED list of candidate titles — surfaced for override judgment,
    never a silent last-writer-wins pick; the framework-qualified keys
    stay exact. Non-`satisfies` kinds (belongs_to, informs, mitigates) and
    relationships whose source title matches no control item contribute
    nothing. Real exports have globally unique control titles (verified
    against the live graph), which is what makes the title join sound."""
    data = (export or {}).get("data") or {}
    items = data.get("items") or {}
    by_title = {}
    for c in items.get("control") or []:
        title = c.get("title")
        f = c.get("fields") or {}
        cid = str(f.get("control_id") or "").strip().lower()
        fw = str(f.get("framework") or "").strip().lower()
        if title and cid:
            by_title[title] = (cid, fw)
    hits = {}
    for rel in data.get("itemRelationships") or []:
        if (rel.get("kind") != "satisfies"
                or rel.get("targetItemType") != "unified_control"):
            continue
        uc_title = rel.get("targetItemTitle")
        cid, fw = by_title.get(rel.get("sourceItemTitle"), ("", ""))
        if not cid or not uc_title:
            continue
        for key in ([cid, f"{fw}:{cid}"] if fw else [cid]):
            hits.setdefault(key, {})[uc_title] = None   # ordered de-dup
    return {key: (next(iter(ucs)) if len(ucs) == 1 else sorted(ucs))
            for key, ucs in hits.items()}


def covered_and_gaps(user_controls, uc_controls, coverage_map, overrides=None):
    """Judge the user's controls against the unified-control baseline.

    Returns (covered, gaps):
      covered: {uc_title: [evidence strings]} — how each unified control
        was judged already-satisfied: a user control's control_id resolving
        through coverage_map (framework-qualified 'fw:cid' first, bare id
        when unambiguous), or an agent override
        {user_control_title: [uc_title, ...]} carrying semantic judgment
        made outside this script. Evidence names the user control and the
        path, so the exclusion of a UC from the gap patch is reviewable.
      gaps: deep copies of the uc_controls NOT covered, input order — the
        proposed gap patch, surfaced for human approval (this function
        never patches anything itself). A gap whose only deterministic
        signal was an AMBIGUOUS bare id carries _ambiguous_user_controls
        naming the user controls involved, so the ambiguity is visible
        instead of silently resolved either way.

    Every entry of uc_controls lands in exactly one of covered/gaps.
    Overrides are validated loudly: a key naming no user control (current
    or merged-away title) or a value naming no unified control raises
    ValueError — a typo must never silently mark coverage (nor silently do
    nothing); an override value that is not a list raises TypeError (a
    bare string would be iterated character-by-character)."""
    coverage_map = coverage_map or {}
    covered = {}
    ambiguous = {}

    def mark(uc_title, why):
        evidence = covered.setdefault(uc_title, [])
        if why not in evidence:
            evidence.append(why)

    for c in user_controls or []:
        f = c.get("fields") or {}
        cid = str(f.get("control_id") or "").strip().lower()
        if not cid:
            continue
        title = str(c.get("title") or "") or cid
        resolved = False
        for fw in _split(f.get("framework")):
            hit = coverage_map.get(f"{fw.strip().lower()}:{cid}")
            if isinstance(hit, str):
                mark(hit, f"control_id {cid!r} ({fw}) on user control {title!r}")
                resolved = True
        bare = coverage_map.get(cid)
        if isinstance(bare, str):
            mark(bare, f"control_id {cid!r} on user control {title!r}")
        elif isinstance(bare, list) and not resolved:
            for candidate in bare:
                names = ambiguous.setdefault(candidate, [])
                if title not in names:
                    names.append(title)

    known_ucs = {uc.get("title") for uc in uc_controls or []}
    user_titles = set()
    for c in user_controls or []:
        if c.get("title"):
            user_titles.add(c["title"])
        user_titles.update(c.get("_merged") or [])
    for user_title, uc_titles in (overrides or {}).items():
        if user_title not in user_titles:
            raise ValueError(
                f"override for unknown user control {user_title!r} — override "
                "keys must be user-control titles (or merged-away titles)")
        if isinstance(uc_titles, str) or not isinstance(uc_titles, (list, tuple)):
            raise TypeError(
                f"override for {user_title!r} must be a list of "
                f"unified-control titles, got {uc_titles!r}")
        for t in uc_titles:
            if t not in known_ucs:
                raise ValueError(
                    f"override for {user_title!r} names unknown unified "
                    f"control {t!r}")
            mark(t, f"override on user control {user_title!r}")

    gaps = []
    for uc in uc_controls or []:
        title = uc.get("title")
        if title in covered:
            continue
        gap = _deep_copy(uc)
        if title in ambiguous:
            gap["_ambiguous_user_controls"] = list(ambiguous[title])
        gaps.append(gap)
    return covered, gaps
