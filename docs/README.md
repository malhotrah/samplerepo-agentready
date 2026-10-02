# Engineering Docs

Internal docs for people (and agents) working **on** Mealie's code. Don't confuse them with `docs/docs/`, the public MkDocs site published at [docs.mealie.io](https://docs.mealie.io) (`task docs`). Files at this level sit outside the MkDocs `docs_dir`, so they are never published.

## Reading order for new engineers

1. Run `task onboard` (or `/onboard` in Claude Code)
2. [onboarding.md](onboarding.md): setup and your first change
3. [architecture.md](architecture.md): system, layers, request trace, multi-tenancy, codegen
4. [glossary.md](glossary.md): domain vocabulary
5. [testing.md](testing.md): test layout, fixtures, commands
6. [review-checklist.md](review-checklist.md): what reviewers look for
7. [adr/](adr/): why the main patterns exist

## Keeping these docs alive

- Change a convention or a layer boundary? Update `architecture.md` and the matching `AGENTS.md` in the same PR.
- Made a non-obvious design decision? Copy [adr/0000-template.md](adr/0000-template.md) to the next number.
- Reference real paths in backticks. Stale paths are the first sign a doc has rotted.
