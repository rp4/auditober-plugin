---
title: Responding to Forms
description: "Answer a form assigned to you: the inbox, reading the ask, accepting a drafted answer, and submitting."
sidebar:
  order: 4
---

Inbox
Open
Answer
Submit

Scroll

Answering a form is usually the whole of your involvement in a workflow: you
are asked a set of questions, you answer them, and your response is recorded on
the [step](https://docs.assureswarm.com/concepts/workflows/) that asked. [Forms](https://docs.assureswarm.com/concepts/forms/) covers
how they are built and assigned; this page is the procedure for answering one.

## Your forms inbox

Every form addressed to you collects in your forms inbox, opened from your
avatar menu at the top right. Assignments group into **Pending** and
**Submitted**, so what is still owed is obvious at a glance. Select
**Open** on a pending card to answer it.

External collaborators get their own **My Forms** entry and land there when
they sign in.

## Open it and read the ask

A form opens on its own page with the step's name, the instructions written
for it, and the questions below. Read the instructions before you answer:
they carry the context the step owner wanted you to have, and you see only
the step context you are permitted to see, not the surrounding workflow.

Once a response exists, a green **Submitted** badge records when it went in
and who sent it.

## Answer, or accept a drafted answer

Answer each question, and note the red asterisk marking the required ones.
If an agent has proposed answers, a banner sits above the form and the
fields arrive pre-filled: read every value, edit anything that is wrong,
then press **Submit** to make them your answers. Dismiss the banner instead
to clear the suggestion without submitting.

Pre-filled values are a proposal until you submit. Nothing is recorded on
the step while the banner is sitting there.

## Submit, and correct it if you need to

Submitting records your answers on the step along with the time, and a
confirmation replaces the form's header: **Response saved successfully**.

An assigned respondent submits once. To correct a submitted response,
ask the sender to reissue the assignment. A person with edit access to the
parent item can update the form while the step remains open; that is a
separate permission from respondent access. Ask the workflow owner about
unclear questions before submitting.

## Where your answers go

Your answers are stored on the step that asked them, alongside its
instructions, result, and documents. That is where the step's approvers read
them, and where an agent reads them through
[get\_step\_context](https://docs.assureswarm.com/mcp/get_step_context/). Nothing about answering a form
approves the step: see [Working a step](https://docs.assureswarm.com/using-coworkcanvas/working-a-step/)
for how a step actually completes.

Form questions can include file uploads. Anything you upload through a form
becomes a step [document](https://docs.assureswarm.com/concepts/documents/) tied to your response, so it
sits with the rest of the step's evidence.

## Responding as an external collaborator

:::note\[You see only your form]
External collaborators are scoped to their own form and the step context it
needs: not the rest of the workflow, not other people's decisions, not
unrelated records. If a question does not make sense out of context, check with
whoever sent it to you rather than guessing.
:::

## If the request was a mistake

A form assignment can be **revoked** by the person who created it, so tell the
sender if a form has reached you in error rather than submitting an empty
response. You can hold only one active assignment per step, so nobody is asked
to fill out the same form twice at once.

And when an agent drafts your answers

## For agents

Your pending form assignments show up in
[get\_current\_context](https://docs.assureswarm.com/mcp/get_current_context/), and a step's form, with
its exact field keys, comes back from
[get\_step\_context](https://docs.assureswarm.com/mcp/get_step_context/). An agent proposes answers with
the `submit_form` action on
[suggest\_change](https://docs.assureswarm.com/mcp/suggest_change/), which creates a pending
[suggestion](https://docs.assureswarm.com/using-coworkcanvas/reviewing-suggestions/) and pre-fills the
form for you. A person still submits it.
