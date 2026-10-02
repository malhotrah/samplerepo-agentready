# Testing

## Commands

| Command | What |
|---------|------|
| `task py:test` | All backend tests, run in parallel (`pytest -n auto --dist loadfile`) |
| `task py:test -- -k recipe_crud` | Filter by name |
| `task py:test -- tests/unit_tests/test_security.py` | A single file |
| `task py:test -- tests/path/test_x.py::test_name -x` | A single test, stopping at the first failure |
| `task py:coverage` | Coverage HTML report |
| `task ui:test` | Frontend Vitest |
| `task e2e` | Playwright end-to-end tests against a Docker build (slow; mostly run in CI) |
| `task py:check` / `task ui:check` | Full lint, type-check and test run before a PR |

By default tests run on SQLite. To run them against Postgres, start `task dev:services` and set `DB_ENGINE=postgres` with the `POSTGRES_*` vars (see `py:postgres` in `Taskfile.yml`). Each xdist worker gets its own database (`tests/conftest.py`).

## Layout

| Folder | Scope | Notes |
|--------|-------|-------|
| `tests/unit_tests/` | Pure logic: parsers, services, repos, schemas, core | No HTTP. `repository_tests/` uses real sessions |
| `tests/integration_tests/` | API-level tests through FastAPI `TestClient` | Grouped by actor/domain: `user_recipe_tests/`, `user_household_tests/`, `admin_tests/`, `public_explorer_tests/`, … |
| `tests/multitenant_tests/` | Proves group/household isolation | One `case_*.py` per resource implementing `ABCMultiTenantTestCase` (`case_abc.py`), registered in `test_multitenant_cases.py` |
| `tests/e2e/` | Playwright (TypeScript) | Login and OIDC flows. Has its own `package.json` |
| `frontend/**/__tests__/`, `*.test.ts` | Vitest | Composables and utilities |

## Fixtures (`tests/fixtures/`, auto-loaded by `tests/conftest.py`)

| Fixture | From | Use |
|---------|------|-----|
| `api_client` | `conftest.py` | `TestClient(app)` with the DB overridden |
| `session`, `unfiltered_database` | `fixture_database.py` | Raw session; `AllRepositories` with no group or household scoping |
| `unique_user`, `unique_user_fn_scoped`, `unique_admin` | `fixture_users.py` | A fresh user (with token) in its own group and household |
| `h2_user` | `fixture_users.py` | A second user in the **same group, different household** |
| `g2_user` | `fixture_users.py` | A user in a **different group** |
| `admin_token`, `user_token`, `user_tuple` | `fixture_users.py` | Auth helpers |
| `multitenants` | `fixture_multitenant.py` | Two isolated tenants for the cross-tenant tests |
| recipe and shopping-list fixtures | `fixture_recipe.py`, `fixture_shopping_lists.py` | Seeded domain data |

Helpers live in `tests/utils/`:
- `api_routes/` (generated route helpers; regenerate them with `task dev:generate`)
- `factories.py` (random data)
- `assertion_helpers.py`
- `fixture_schemas.py` (`TestUser`)

## Conventions

- Use **the generated route helpers** in `tests/utils/api_routes` instead of hard-coding URLs.
- Use `unique_user` and random factories, so that tests are independent under `--dist loadfile`.
- Any new group- or household-scoped resource needs a multitenant case, plus an `h2_user`/`g2_user` test asserting a 404 or 403 across the boundary.
- Fix failing tests at the root cause. Don't weaken assertions. The `test-runner` subagent follows this rule.
- Schema changed? Run `task dev:generate` first. Stale generated helpers cause false failures.
