---
description: Scaffold a new API endpoint following Mealie's controller-service-repo pattern
argument-hint: <resource-name> (e.g. "shopping-list-label")
---

Add a new endpoint for resource: $ARGUMENTS

Follow the existing repository-service-controller pattern exactly as described in AGENTS.md:

1. Find the closest existing resource of similar shape under `mealie/routes/`, `mealie/services/`, `mealie/repos/`, `mealie/schema/` and use it as the template — don't invent new patterns.
2. Add Pydantic schemas in `mealie/schema/` with correct `*In`/`*Out`/`*Create`/`*Update` suffixes.
3. Add/extend the repository in `mealie/repos/`, scoped to group/household context.
4. Add the service in `mealie/services/` coordinating the repo.
5. Add the controller in `mealie/routes/`, inheriting `BaseUserController` or `BaseAdminController`, using `Depends(get_repositories)` and `Depends(get_current_user)`.
6. Run `task dev:generate` to regenerate TypeScript types and schema exports.
7. Add a test under `tests/` following the pattern in `tests/conftest.py`.
8. Run `task py:test` to confirm it passes.

Stop and ask before touching anything under `frontend/` unless the resource clearly needs a UI — scaffolding the backend endpoint is the default scope.
