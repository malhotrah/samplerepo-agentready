---
description: Guided, read-only tour of the Mealie codebase for a new engineer
argument-hint: "[backend|frontend|db|tests] (optional focus area)"
allowed-tools: Read, Grep, Glob, Bash(task --list:*), Bash(task onboard:*), Bash(git log:*)
---

You are onboarding a new engineer to Mealie. Focus area: "$ARGUMENTS" (if empty, give the full-stack tour).

This is **read-only**: don't edit files, install anything or start servers.

1. **Ground yourself.** Read `docs/architecture.md` and `docs/glossary.md`. If the focus is `backend`/`db`, also read `mealie/AGENTS.md`. For `frontend`, read `frontend/AGENTS.md`. For `tests`, read `docs/testing.md`.
2. **Environment snapshot.** Run `task onboard` and summarise anything marked ✗ in one line each, with the fix. Don't paste the whole output.
3. **The 60-second picture.** In at most 8 bullets: what Mealie is, the dev and prod topology, the main layers, and the group → household tenancy model.
4. **Live trace.** Pick one real request that fits the focus area:
   - full stack or backend: `GET /api/recipes/{slug}`
   - frontend: the recipe page `frontend/app/pages/g/[groupSlug]/r/[slug]/index.vue`
   - db: the recipe model and repository
   - tests: one test in `tests/integration_tests/user_recipe_tests/`

   Open the actual files and walk the hops in order, giving the `path:line` and one sentence per hop. Verify each hop in the code instead of reciting the doc. If the doc is wrong, say so.
5. **Rules that bite newcomers.** Briefly cover:
   - generated files plus `task dev:generate`
   - `uv run` only
   - only `en-US` locales
   - repo scoping and 404s
   - Alembic migrations for model changes
6. **Where to look next.** A short table: "to do X → open Y", taken from `docs/architecture.md` §8 and filtered to the focus area.
7. **Starter tasks.** Suggest 2–3 small, concrete first tasks in the focus area. Base them on what you saw, such as a missing test or a small endpoint. Give the files to touch and the `task` command that verifies each one.
8. Finish by offering a follow-up: `/trace <feature>` for any feature, or `/onboard <other-area>`.

Keep the whole response skimmable: headings, short bullets, clickable `path:line` references, and no long code dumps.
