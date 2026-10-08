#!/usr/bin/env python3
"""Preview a local Studio import without overwriting existing tenant types."""
from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from pathlib import Path

RETIRED = {"audit", "grc", "reg", "sox", "generic"}
FIELD_TYPES = {"TEXT", "TEXTAREA", "RICHTEXT", "NUMBER", "DATE", "DATETIME", "SELECT",
               "MULTISELECT", "BOOLEAN", "USER", "USERS", "DOCUMENT", "JSON"}
BUCKETS = {"itemTypes", "items", "itemRelationships", "workflows", "workflowsAttached", "dashboards", "customLists"}


def load_pack(directory: Path, kind: str = "core", from_path: Path | None = None) -> dict:
    if from_path is not None:
        return json.loads(Path(from_path).read_text(encoding="utf-8-sig"))
    if kind in RETIRED:
        raise ValueError(f"{kind} overlay is retired; use core or a current library template")
    if kind != "core":
        raise ValueError("unknown pack; use core or explicit --from")
    return json.loads((Path(directory) / "core.json").read_text(encoding="utf-8-sig"))


def options(field: dict) -> list[str]:
    raw = field.get("options")
    if raw is None:
        raw = []
    if not isinstance(raw, list):
        raise ValueError(f"{field.get('fieldKey')}: options must be an array")
    values = [value if isinstance(value, str) else value.get("value") if isinstance(value, dict) else None for value in raw]
    if any(not isinstance(value, str) for value in values):
        raise ValueError(f"{field.get('fieldKey')}: malformed options")
    return values


def fields_for(row: dict) -> dict:
    if "fields" in row:
        raise ValueError(f"{row.get('slug')}: use fieldDefinitions or FieldDefinition")
    fields = row.get("FieldDefinition", row.get("fieldDefinitions", []))
    if not isinstance(fields, list):
        raise ValueError("fieldDefinitions must be an array")
    result = {}
    for field in fields:
        if not isinstance(field, dict):
            raise ValueError("fieldDefinitions rows must be objects")
        key, kind = field.get("fieldKey"), field.get("fieldType")
        if not isinstance(key, str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9_]*", key) or key in result:
            raise ValueError(f"invalid or duplicate fieldKey: {key}")
        if kind not in FIELD_TYPES:
            raise ValueError(f"{key}: unsupported field type {kind}")
        if not field.get("label"):
            raise ValueError(f"{key}: label is required")
        allowed = options(field)
        if kind in {"SELECT", "MULTISELECT"} and not allowed:
            raise ValueError(f"{key}: options are required")
        if field.get("isSearchable") and kind not in {"TEXT", "TEXTAREA", "RICHTEXT"}:
            raise ValueError(f"{key}: cannot be searchable")
        if kind == "DOCUMENT" and any(field.get(k) not in (None, False, [], {}) for k in
            ("required", "isFilterable", "isSearchable", "options", "defaultValue", "validation", "customListCategory", "relatedItemTypeSlug")):
            raise ValueError(f"{key}: DOCUMENT accepts only a bare field definition")
        result[key] = {"type": kind, "required": bool(field.get("required")), "options": allowed}
    return result


def validate_item(item: dict, slug: str, schema: dict) -> None:
    if not isinstance(item, dict) or not isinstance(item.get("title"), str) or not item["title"].strip():
        raise ValueError(f"{slug}: item title is required")
    fields = item.get("fields", {})
    if not isinstance(fields, dict):
        raise ValueError(f"{slug}: item fields must be an object")
    definitions = schema["fields"]
    for key, value in fields.items():
        if key not in definitions:
            raise ValueError(f"{slug}.{key}: unknown field")
        definition = definitions[key]
        kind = definition["type"]
        if kind == "DOCUMENT":
            raise ValueError(f"{slug}.{key}: upload documents after import")
        if kind == "SELECT" and value not in definition["options"]:
            raise ValueError(f"{slug}.{key}: unsupported option")
        if kind == "MULTISELECT" and (not isinstance(value, list) or any(v not in definition["options"] for v in value)):
            raise ValueError(f"{slug}.{key}: unsupported options")
        if kind == "BOOLEAN" and not isinstance(value, bool):
            raise ValueError(f"{slug}.{key}: expected boolean")
        if kind == "NUMBER" and (not isinstance(value, (int, float)) or isinstance(value, bool)):
            raise ValueError(f"{slug}.{key}: expected number")
    for key, definition in definitions.items():
        if key not in {"status", "title"} and definition["required"] and fields.get(key) in (None, "", []):
            raise ValueError(f"{slug}.{key}: required value missing")
    statuses = schema.get("lifecycle", {}).get("statuses")
    if item.get("status") is not None and statuses is not None and item["status"] not in statuses:
        raise ValueError(f"{slug}: status is absent from the current lifecycle")


def prepare(pack: dict, existing: dict | None = None) -> tuple[dict, dict]:
    existing = {} if existing is None else existing
    if not isinstance(existing, dict):
        raise ValueError("discovered types must be an object keyed by slug")
    # Reject NaN/Infinity at every nesting level, including metadata and JSON fields.
    json.dumps(pack, allow_nan=False)
    json.dumps(existing, allow_nan=False)
    for slug, schema in existing.items():
        if not isinstance(schema, dict) or not isinstance(schema.get("fields"), dict):
            raise ValueError(f"{slug}: malformed discovered schema")
        for key, field in schema["fields"].items():
            if not isinstance(field, dict) or field.get("type") not in FIELD_TYPES:
                raise ValueError(f"{slug}.{key}: malformed discovered field")
            options(field)
        if not isinstance(schema.get("lifecycle", {}), dict):
            raise ValueError(f"{slug}: malformed discovered lifecycle")
    if not isinstance(pack, dict) or pack.get("format") != "coworkcanvas" or not isinstance(pack.get("data"), dict):
        raise ValueError("expected a coworkcanvas envelope with a data object")
    data = pack["data"]
    unknown = set(data) - BUCKETS
    if unknown:
        raise ValueError(f"unsupported data buckets: {sorted(unknown)}")
    types, items = data.get("itemTypes", []), data.get("items", {})
    if not isinstance(types, list) or not isinstance(items, dict):
        raise ValueError("itemTypes must be an array; items must be an object keyed by slug")
    schemas = copy.deepcopy(existing)
    seen = set()
    for row in types:
        if not isinstance(row, dict):
            raise ValueError("itemTypes rows must be objects")
        slug = row.get("slug")
        if not isinstance(slug, str) or not re.fullmatch(r"[a-z][a-z0-9_]*", slug) or slug in seen:
            raise ValueError(f"invalid or duplicate type slug: {slug}")
        if not row.get("name") or not row.get("namePlural"):
            raise ValueError(f"{slug}: name and namePlural are required")
        seen.add(slug)
        fields = fields_for(row)
        if slug not in schemas:
            status = fields.pop("status", None)
            schemas[slug] = {"fields": fields, "lifecycle": {
                "defaultStatus": row.get("defaultStatus"),
                "statuses": status["options"] if status else None}}
    for slug, rows in items.items():
        if not isinstance(rows, list):
            raise ValueError(f"{slug}: items must be an array")
        if slug not in schemas:
            if rows:
                raise ValueError(f"{slug}: type not declared or discovered")
            continue
        for item in rows:
            validate_item(item, slug, schemas[slug])
    for bucket in BUCKETS - {"itemTypes", "items"}:
        if bucket in data and not isinstance(data[bucket], list):
            raise ValueError(f"{bucket} must be an array")
        if any(not isinstance(row, dict) for row in data.get(bucket, [])):
            raise ValueError(f"{bucket} rows must be objects")
    for row in data.get("customLists", []):
        if not all(isinstance(row.get(key), str) and row[key] for key in ("category", "value", "label")):
            raise ValueError("customLists must be flat category/value/label rows")
    # Non-schema payloads retain their exact content; admin preview validates their
    # graph, relationship references, permissions and duplicate handling.
    output = copy.deepcopy(pack)
    output["data"]["itemTypes"] = [row for row in output["data"].get("itemTypes", []) if row["slug"] not in existing]
    preserved = sorted(seen & set(existing))
    preview = {
        "types_to_create": len(output["data"]["itemTypes"]),
        "fields_on_new_types": sum(len(fields_for(row)) for row in output["data"]["itemTypes"]),
        "preserved_types": preserved,
        "schema_changes": [],
        "items": sum(len(rows) for rows in items.values()),
        "templates": len(data.get("workflows", [])),
        "relationships": len(data.get("itemRelationships", [])),
        "custom_list_values": len(data.get("customLists", [])),
        "validation": "local structure and field values checked; admin import preview still required",
        "notes": ["Existing type definitions are omitted, including missing fields; no customized type is overwritten.",
                  "Item duplicate handling and graph/reference checks remain for the admin preview; this helper makes no idempotency claim."],
    }
    return output, preview


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--packs", type=Path, default=Path(__file__).resolve().parents[3] / "starter-packs")
    parser.add_argument("--kind", default="core")
    parser.add_argument("--from", dest="from_path", type=Path)
    parser.add_argument("--schema", type=Path, help="current session projection with tenant_key, session_id and types")
    parser.add_argument("--tenant-key")
    parser.add_argument("--session-id")
    parser.add_argument("--empty-tenant", action="store_true", help="use only after complete discovery verifies no types")
    parser.add_argument("--out", type=Path, help="omit for preview only")
    args = parser.parse_args(argv)
    try:
        if args.out:
            protected = [args.packs / "core.json", Path(__file__).resolve().parents[3] / "starter-packs/core.json", args.from_path, args.schema]
            for source in filter(None, protected):
                if args.out.resolve() == source.resolve() or (args.out.exists() and source.exists() and args.out.samefile(source)):
                    raise ValueError(f"output would overwrite input or bundled core: {source}")
        if bool(args.schema) == bool(args.empty_tenant):
            raise ValueError("supply current --schema or verified --empty-tenant")
        existing = {}
        if args.schema:
            snapshot = json.loads(args.schema.read_text(encoding="utf-8-sig"))
            if not isinstance(snapshot, dict):
                raise ValueError("schema snapshot must be an object")
            if not args.tenant_key or not args.session_id or snapshot.get("tenant_key") != args.tenant_key or snapshot.get("session_id") != args.session_id:
                raise ValueError("schema tenant/session binding mismatch")
            existing = snapshot["types"]
        output, preview = prepare(load_pack(args.packs, args.kind, args.from_path), existing)
        if args.out:
            args.out.parent.mkdir(parents=True, exist_ok=True)
            args.out.write_text(json.dumps(output, indent=2, allow_nan=False) + "\n", encoding="utf-8")
            prepare(json.loads(args.out.read_text(encoding="utf-8")), existing)
            preview["artifact"] = str(args.out)
        print(json.dumps(preview, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
