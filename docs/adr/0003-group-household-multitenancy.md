# ADR-0003: Two-level tenancy (group → household) enforced in repositories

- **Status:** Accepted (documents existing practice — context reconstructed from the code; correct it if you know the original history)
- **Date:** 2026-10-02

## Context
A single Mealie server hosts multiple independent groups (families, friend circles). Within a group, several households want to share vocabulary (foods, units, tags) and read each other's recipes, while keeping their own meal plans and shopping lists.

## Decision
- Every user has exactly one `group_id` and one `household_id`.
- `AllRepositories(session, group_id=..., household_id=...)` is constructed per request from the current user (`BaseUserController.repos`).
- `GroupRepositoryGeneric` / `HouseholdRepositoryGeneric` (`repos/repository_generic.py`) require those IDs (`NOT_SET` raises) and `_filter_builder` adds them to every query.
- Group-wide reads deliberately pass `household_id=None` (e.g. `group_recipes` in `routes/recipe/_base.py`).
- Only `BaseAdminController` uses fully unscoped repositories.

## Consequences
- Cross-tenant leaks are prevented by default rather than by each handler remembering to filter.
- Wrong IDs surface as 404s — a common gotcha when writing services/tests.
- Every new scoped resource needs a `tests/multitenant_tests/case_*.py` and cross-boundary tests using `h2_user` (other household) / `g2_user` (other group).

## Alternatives considered
- Database-per-tenant — rejected: heavy for a self-hosted app on SQLite.
- Single-level (group only) — the original model; households were added so families in one group could keep separate plans/lists.
