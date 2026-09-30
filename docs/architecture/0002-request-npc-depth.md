# 0002 -- request_npc_depth, the first call type

## What

`contract/request_npc_depth.schema.json`: a party member asks the Court for depth -- what a character thinks, wants or
plans -- and gets back either that depth or a refusal.

- **Request:** `contract_version`, `npc_id`, `context_summary` (at most 500 characters), and an optional `distress`
  hint. Nothing else is accepted.
- **Reply:** exactly one of two shapes. A depth reply (`refused` false, `text`), or a refusal (`refused` true, a
  `reason` from `distress`, `rate_limit`, `unreachable`, and `fallback` = `plain_python`). A refusal can never also carry
  text.

## Why

- **Depth is the Court's to give; mechanics are the player's.** Everything else about a character runs in local Python.
  Only a party member's deeper intelligence crosses to the Court.
- **A refusal is a normal answer, not an error.** When the Court says no, the reply says why and tells the mechanics
  exactly what to do instead: fall back to plain Python. The game keeps running.
- **The distress field is a hint, never a verdict.** Code on the player's machine can be edited, so a client can always
  claim "no distress". The Court decides distress from what it sees; the field only lets an honest client say what it
  noticed.

## Turned down

- **A mirror of the schemas under `definitions` for older validators.** Rejected by the schema's author: a second copy
  that must be kept in step by hand drifts; there is one copy, under `$defs`.
- **A client-authoritative distress flag.** See above: it would put a protection in the hands of the person it protects
  against.
- **Naming the model that serves depth, or a business model, in the contract.** Either would make the contract wrong
  the day it changes.

## What it rests on

- FACT: the file is a valid JSON Schema (draft 2020-12), checked by `jsonschema` 4.25.1.
- FACT: the fifteen checks below pass; before the file existed they all failed, and a correct reference schema passed
  them, so they can do both.
- GUESS: 500 characters is enough context for a good depth answer. To be measured once real calls exist.

## How it is tested

`tests/test_request_npc_depth_schema.py` -- run from the repository root with
`.venv/bin/python -m unittest discover -s tests` (install `requirements-dev.txt` into a local `.venv` first). It checks
the draft and version, both named parts, a valid request, a missing or unknown field, that any distress field is optional
and says it is advisory, both reply shapes, and five kinds of invalid refusal.
