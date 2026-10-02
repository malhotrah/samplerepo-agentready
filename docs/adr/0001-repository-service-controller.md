# ADR-0001: Repository → Service → Controller layering

- **Status:** Accepted (documents existing practice — context reconstructed from the code; correct it if you know the original history)
- **Date:** 2026-10-02

## Context
Mealie's API covers many domains (recipes, households, meal plans, shopping lists, admin). Mixing HTTP handling, business rules and SQLAlchemy queries in route functions made logic hard to reuse (e.g. from scheduler tasks or migrations) and hard to test.

## Decision
Three layers, each with a base class:
- **Controllers** — `mealie/routes/**`, class-based views registered with `@controller(router)` (`routes/_base/controller.py`), inheriting from `routes/_base/base_controllers.py`. HTTP concerns only: auth, request/response models, error mapping. Plain CRUD may go through the `HttpRepo` mixin (`routes/_base/mixins.py`).
- **Services** — `mealie/services/**`, inheriting `BaseService`. Business logic; reusable outside HTTP.
- **Repositories** — `mealie/repos/**`, obtained from `AllRepositories` (`repos/repository_factory.py`). The only layer that builds queries.

## Consequences
- Business logic can be called from scheduler tasks, importers and tests without an HTTP request.
- Tenant scoping is enforced in one place (repositories) — see ADR-0003.
- New endpoints follow a predictable shape; `/add-endpoint` scaffolds it.
- Slightly more files per feature.

## Alternatives considered
- Fat route functions with inline queries — rejected: duplicated scoping logic, poor reuse.
