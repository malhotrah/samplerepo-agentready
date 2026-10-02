# Mealie Development Guide for AI Agents

## Project Overview

Mealie is a self-hosted recipe manager, meal planner, and shopping list application with a FastAPI backend (Python 3.14) and Nuxt 4 frontend (Vue 3 + TypeScript). It uses SQLAlchemy ORM with support for SQLite and PostgreSQL databases.

**Development vs Production:**
- **Development:** Frontend (port 3000) and backend (port 9000) run as separate processes
- **Production:** Frontend is statically generated and served via FastAPI's SPA module (`mealie/routes/spa/`) in a single container

**Area-specific rules load from nested files** — read them before working in that subtree:
- `mealie/AGENTS.md` — backend architecture (controller → service → repo), Python practices
- `frontend/AGENTS.md` — component naming, API clients, composables, translations

## Docs Map

Engineering docs live at the top level of `docs/` (not published; `docs/docs/` is the public MkDocs site):

| Need | Read |
|------|------|
| How the system fits together, request lifecycle | `docs/architecture.md` |
| Day-1 setup and first change | `docs/onboarding.md` |
| Test layout, fixtures, running a single test | `docs/testing.md` |
| Domain vocabulary (group, household, organizer…) | `docs/glossary.md` |
| PR review checklist | `docs/review-checklist.md` |
| Why things are the way they are | `docs/adr/` |

Commands for orientation: `task onboard` (environment check + repo map), `/onboard [area]` (guided tour), `/trace <feature>` (follow a feature through every layer).

## Essential Commands (via Task/Taskfile.yml)

**Development workflow:**
```bash
task setup              # Install all dependencies (Python + Node)
task dev:services       # Start Postgres & Mailpit containers
task py                 # Start FastAPI backend (port 9000)
task ui                 # Start Nuxt frontend (port 3000)
task docs               # Start Zensical documentation server
task onboard            # Check prerequisites and print a map of the repo
```

**Code generation (REQUIRED after schema changes):**
```bash
task dev:generate       # Generate TypeScript types, schema exports, test helpers
```

**Testing & Quality:**
```bash
task py:test            # Run pytest (supports args: task py:test -- -k test_name)
task py:check           # Format + lint + type-check + test (full validation)
task py:format          # Ruff format
task py:lint            # Ruff check
task py:mypy            # Type checking
task ui:test            # Vitest frontend tests
task ui:check           # Frontend lint + test
```

**Database:**
```bash
task py:migrate -- "description"  # Generate Alembic migration
task py:postgres        # Run backend with PostgreSQL config
```

**Docker:**
```bash
task docker:prod        # Build and run production Docker compose
```

## Cross-Cutting Concerns

1. **Code generation is source of truth:** After Pydantic schema changes, run `task dev:generate` to update:
   - TypeScript types (`frontend/app/lib/api/types/`)
   - Schema exports (`mealie/schema/*/__init__.py`)
   - Test data paths and routes

2. **Multi-tenancy:** All data scoped to **groups** and **households**:
   - Groups contain multiple households
   - Households contain recipes, meal plans, shopping lists
   - Repositories automatically filter by group/household context (see `docs/architecture.md#multi-tenancy`)

3. **Pre-commit hooks:** Install via `task setup:py`, enforces Ruff formatting/linting

4. **Testing before PRs:** Run `task py:check` and `task ui:check` before submitting PRs

## Pull Request Basics

1. **Draft PRs are optional:** Create a draft PR early if you want feedback while working, or open directly as ready when complete
2. **Verify code generation:** If you modified Pydantic schemas, ensure `task dev:generate` was run
3. **Follow Conventional Commits:** Title your PR according to the conventional commits format (see PR template)
4. **Add release notes:** Include user-facing changes in the PR description
5. **Review against** `docs/review-checklist.md` (the `code-reviewer` subagent enforces it)

## Common Gotchas

- **Don't manually edit generated files:** `frontend/app/lib/api/types/`, schema `__init__.py` files
- **Repository context:** Repos are group/household-scoped - passing wrong IDs causes 404s
- **Session handling:** Don't create sessions manually, use dependency injection or `session_context()`
- **Schema changes require codegen:** After changing Pydantic models, run `task dev:generate`
- **Translation files:** Only modify `en-US` locale files - all other locales are managed by Crowdin
- **Dev containers:** This project uses VS Code dev containers - leverage the pre-configured environment
- **Task commands:** Use `task` commands instead of direct tool invocation for consistency
- **Python:** Always `uv run …`, never bare `python`/`pip`

## Key Files to Reference

- `Taskfile.yml` - All development commands and workflows
- `mealie/routes/_base/base_controllers.py` - Controller base classes and patterns
- `mealie/repos/repository_factory.py` - Repository factory and available repos
- `frontend/app/lib/api/base/base-clients.ts` - API client base classes
- `tests/conftest.py` - Test fixtures and setup
- `dev/code-generation/main.py` - Code generation entry point

## Additional Resources

- [Documentation](https://docs.mealie.io/)
- [Contributors Guide](https://nightly.mealie.io/contributors/developers-guide/code-contributions/)
- [Discord](https://discord.gg/QuStdQGSGK)
