---
description: Trace a feature or endpoint through every layer (frontend → controller → service → repo → model → tests)
argument-hint: <endpoint path or feature name> (e.g. "POST /api/households/shopping/lists" or "meal plan rules")
allowed-tools: Read, Grep, Glob
---

Trace "$ARGUMENTS" through the Mealie stack. This is read-only.

Use `docs/architecture.md` §2 ("Worked trace") as the model for the output. Find each hop by searching the code, not by guessing:

1. **Route.** Find the router prefix (`UserAPIRouter`/`AdminAPIRouter` in `mealie/routes/**`) and the decorated method. Note the controller base class and what it means for auth and scoping (`mealie/routes/_base/base_controllers.py`).
2. **Schemas.** List the request and response Pydantic models in `mealie/schema/**`.
3. **Service.** Find the service class and method it delegates to (`mealie/services/**`), and any events published (`publish_event`).
4. **Repository.** Find the `AllRepositories` property (`mealie/repos/repository_factory.py`), its class, and whether it's `Group`- or `Household`-scoped.
5. **Model.** Find the SQLAlchemy model and table (`mealie/db/models/**`).
6. **Frontend.** Find the API client method (`frontend/app/lib/api/**`), the composable, and the page or component that calls it.
7. **Tests.** Find the integration and unit tests, and any multitenant case covering it (`tests/**`). If coverage is missing, say so.

Output:
- a compact table: `Layer | File:line | Symbol | Note`
- a 3–5 line narrative of the request flow
- a "Gotchas" section with anything surprising, such as unscoped repos, logic in the controller, missing tests or generated code involved

If the feature doesn't exist or is ambiguous, list the closest matches and stop.
