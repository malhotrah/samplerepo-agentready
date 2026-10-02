# PR Review Checklist

The source of truth for reviewing Mealie PRs. Humans use it, and so does the `code-reviewer` subagent (`.claude/agents/code-reviewer.md`). Skip the sections that don't apply to the diff.

## Architecture & Patterns
- [ ] Does the code follow the repository-service-controller pattern? ([adr/0001](adr/0001-repository-service-controller.md))
- [ ] Are controllers delegating business logic to services?
- [ ] Are services coordinating repositories rather than accessing the database directly?
- [ ] Is dependency injection used properly (`Depends(get_repositories)`, `Depends(get_current_user)`, `self.repos` in controllers)?

## Data Scoping
- [ ] Are repositories correctly scoped to group/household context? ([adr/0003](adr/0003-group-household-multitenancy.md))
- [ ] Do route handlers validate group/household ownership before operations?
- [ ] Are multi-tenant boundaries enforced, so users can't access other groups' data?
- [ ] Are unscoped repos (`group_id=None`) used only in admin controllers or with explicit justification?
- [ ] Does a new scoped resource have a case in `tests/multitenant_tests/`?

## Type Safety
- [ ] Are type hints present on all functions and methods?
- [ ] Are Pydantic schemas using the correct suffixes (`*In`, `*Out`, `*Create`, `*Update`)?
- [ ] For frontend code, does TypeScript pass strict type checking, with no new `any`?

## Generated Files ([adr/0002](adr/0002-generated-frontend-types.md))
- [ ] `frontend/app/lib/api/types/` files were not manually edited
- [ ] `mealie/schema/*/__init__.py` exports match the actual schema files
- [ ] If schemas changed, the generated files were updated with `task dev:generate`

## Code Quality
- [ ] Is the code readable and well organized?
- [ ] Are complex operations documented with clear comments?
- [ ] Do component names follow the naming conventions (Domain/Base/App/The prefixes)?
- [ ] Are composables used for shared frontend logic instead of duplication?

## Translations
- [ ] Only the `en-US` locale files were modified for new translation strings
- [ ] No other (Crowdin-managed) locale files were touched

## Database Changes
- [ ] Are Alembic migrations included for schema changes?
- [ ] Were the migrations tested against both SQLite and PostgreSQL?

## Docs
- [ ] If the change alters architecture, a layer boundary or a convention, are `docs/architecture.md`, the relevant `AGENTS.md`, or a new ADR updated?

## Review Etiquette
- Be constructive and specific in feedback
- Suggest code examples when proposing changes
- Focus on architecture and logic. CI and hooks handle formatting and linting
- Use "Approve" when the PR is ready to merge, "Request Changes" for blocking issues, and "Comment" for non-blocking suggestions
