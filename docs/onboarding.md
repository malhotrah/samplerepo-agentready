# Onboarding: your first day on Mealie

Goal: by the end of today you'll have the app running locally, understand how a request flows through it, and have one small change working with tests passing.

## 0. Get oriented (5 min)

Run this from the repo root:

```bash
task onboard
```

It checks your toolchain and setup state, prints a map of the repo, and lists the docs to read next. If you use Claude Code, run `/onboard` for an interactive guided tour, or `/onboard backend|frontend|db|tests` to focus on one area.

## 1. Prerequisites

| Tool | Why | Check |
|------|-----|-------|
| [Task](https://taskfile.dev) | Runs every dev command (`Taskfile.yml`) | `task --version` |
| [uv](https://docs.astral.sh/uv/) | Manages Python 3.14 and the venv. Never use bare `pip`/`python` | `uv --version` |
| Node + [pnpm](https://pnpm.io) | Frontend | `node -v`, `pnpm -v` |
| Docker | Postgres and Mailpit for `task dev:services`, plus e2e tests | `docker --version` |
| git | | `git --version` |

**Shortcut:** open the repo in the VS Code **Dev Container** (`.devcontainer/`). It comes with everything preinstalled.

## 2. Install and run

```bash
task setup          # Python deps (uv) + frontend deps (pnpm) + pre-commit hooks
task dev:services   # optional: Postgres + Mailpit containers
task py             # backend  -> http://localhost:9000  (API docs at /docs)
task ui             # frontend -> http://localhost:3000  (second terminal)
```

The default dev login and other details are in `docs/docs/contributors/developers-guide/starting-dev-server.md`. To run against Postgres instead of SQLite, use `task py:postgres`.

## 3. Read (about 45 min, in this order)

1. [architecture.md](architecture.md). Pay most attention to §2 "Worked trace" and §3 "Multi-tenancy".
2. [glossary.md](glossary.md). Mealie's domain words (group, household, organizer, …).
3. Root `AGENTS.md` plus `mealie/AGENTS.md` / `frontend/AGENTS.md`. These are the rules that both humans and agents follow.
4. [testing.md](testing.md).
5. Skim [adr/](adr/) to see why the main patterns exist.

## 4. Make a first change

Pick something small. For example, add a read-only field to an existing response, or add a trivial endpoint.

1. Find the closest existing example. `/trace <feature>` in Claude Code maps a feature across every layer.
2. To add an endpoint, follow the controller → service → repo pattern. `/add-endpoint <resource>` scaffolds it.
3. If you touched a Pydantic schema, run `task dev:generate`.
4. If you touched a DB model, run `task py:migrate -- "describe change"`. See `docs/docs/contributors/developers-guide/database-changes.md`.
5. Add or extend a test (see [testing.md](testing.md)) and run `task py:test -- -k <name>`.
6. Before pushing, run `task py:check` and `task ui:check`.
7. Open a PR with a Conventional Commits title (see `.github/pull_request_template.md`). Self-review against [review-checklist.md](review-checklist.md). In Claude Code, the `code-reviewer` subagent does this for you.

## 5. Agent tooling in this repo

| Thing | Where | What it does |
|-------|-------|--------------|
| `AGENTS.md` (root and nested) | `/`, `mealie/`, `frontend/` | Rules loaded automatically (Claude through the `CLAUDE.md` → `@AGENTS.md` imports) |
| `/onboard`, `/trace`, `/add-endpoint` | `.claude/commands/` | Guided tour, feature tracing, endpoint scaffolding |
| `code-reviewer`, `test-runner` | `.claude/agents/` | Pre-PR review and test-fix loop |
| Hooks | `.claude/hooks/` | Block edits to generated files; auto-format Python |
| Permissions | `.claude/settings.json` | Pre-approves the safe `task` commands; denies `git push` |
| MCP servers | `.mcp.json` | Playwright (browser), GitHub (needs `GITHUB_PERSONAL_ACCESS_TOKEN`) |

## 6. Getting help

- Existing contributor docs: `docs/docs/contributors/developers-guide/`
- [Discord](https://discord.gg/QuStdQGSGK)
- `MAINTAINERS.md`
