# ADR-0002: Pydantic schemas are the single source of truth; TS types are generated

- **Status:** Accepted (documents existing practice — context reconstructed from the code; correct it if you know the original history)
- **Date:** 2026-10-02

## Context
The Nuxt frontend consumes ~all backend payloads. Hand-maintained TypeScript interfaces drifted from the Pydantic models, causing runtime bugs that type-checking couldn't catch.

## Decision
`task dev:generate` (`dev/code-generation/main.py`) generates from the live backend:
- `frontend/app/lib/api/types/*.ts` from Pydantic schemas (`gen_ts_types.py`)
- `mealie/schema/*/__init__.py` re-exports (`gen_py_schema_exports.py`)
- `tests/utils/api_routes/__init__.py` route helpers and test data paths

Generated files are never edited by hand. `.claude/hooks/block-generated-edits.js` enforces this for agents; reviewers enforce it for humans (`docs/review-checklist.md`).

## Consequences
- Any schema change must be followed by `task dev:generate` in the same PR.
- Schema naming (`*In`/`*Out`/`*Create`/`*Update`) directly shapes the frontend API.
- Stale generated files are a common cause of "mysterious" test failures — regenerate first.

## Alternatives considered
- OpenAPI client generators (full client) — rejected in favour of hand-written `BaseCRUDAPI` clients + generated types only, keeping client ergonomics under our control.
