"""
Onboarding helper for new contributors: `task onboard`.

Checks the local toolchain and setup state, then prints a map of the repo and
where to read next. Stdlib only and read-only — safe to run at any time.
"""

import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# Windows consoles may not default to UTF-8; never crash on a check mark.
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

USE_COLOR = sys.stdout.isatty()
OK = "\033[32m✓\033[0m" if USE_COLOR else "✓"
BAD = "\033[31m✗\033[0m" if USE_COLOR else "✗"
WARN = "\033[33m!\033[0m" if USE_COLOR else "!"

# (command, version args, why it matters, install hint)
TOOLS: list[tuple[str, list[str], str, str]] = [
    ("task", ["--version"], "runs all dev commands", "https://taskfile.dev/installation/"),
    ("uv", ["--version"], "Python 3.14 + venv", "https://docs.astral.sh/uv/getting-started/installation/"),
    ("node", ["--version"], "frontend runtime", "https://nodejs.org/"),
    ("pnpm", ["--version"], "frontend packages", "corepack enable pnpm"),
    ("docker", ["--version"], "dev services + e2e (optional)", "https://docs.docker.com/get-docker/"),
    ("git", ["--version"], "version control", "https://git-scm.com/downloads"),
]

SETUP_STATE: list[tuple[str, str, str]] = [
    (".venv", "Python virtualenv", "task setup:py"),
    ("frontend/node_modules", "frontend dependencies", "task setup:ui"),
]

REPO_MAP: list[tuple[str, str]] = [
    ("mealie/routes/", "Controllers (HTTP layer), mounted under /api"),
    ("mealie/services/", "Business logic, scheduler, event bus"),
    ("mealie/repos/", "Data access — group/household-scoped repositories"),
    ("mealie/db/models/", "SQLAlchemy models"),
    ("mealie/alembic/", "DB migrations"),
    ("mealie/schema/", "Pydantic schemas (source of truth for TS types)"),
    ("mealie/core/", "Settings, security, dependencies"),
    ("frontend/app/", "Nuxt 4 app: pages, components, composables, lib/api"),
    ("tests/", "unit, integration, multitenant, e2e"),
    ("dev/code-generation/", "`task dev:generate` generators"),
    ("docs/", "Engineering docs (docs/docs/ = public site)"),
    (".claude/", "Agent commands, subagents, hooks, permissions"),
]

READING: list[tuple[str, str]] = [
    ("docs/onboarding.md", "setup + first change"),
    ("docs/architecture.md", "layers, request trace, multi-tenancy"),
    ("docs/glossary.md", "domain vocabulary"),
    ("docs/testing.md", "how to test"),
    ("AGENTS.md", "rules for humans and agents (+ mealie/, frontend/)"),
]

COMMANDS: list[tuple[str, str]] = [
    ("task setup", "install all dependencies"),
    ("task py", "backend on :9000 (API docs at /docs)"),
    ("task ui", "frontend on :3000"),
    ("task dev:services", "Postgres + Mailpit containers"),
    ("task dev:generate", "regenerate types after schema changes"),
    ("task py:test -- -k name", "run selected backend tests"),
    ("task ui:test", "frontend tests"),
    ("task py:check / ui:check", "full checks before a PR"),
]


def heading(text: str) -> None:
    print(f"\n== {text} " + "=" * max(0, 60 - len(text)))


def tool_version(cmd: str, args: list[str]) -> str | None:
    exe = shutil.which(cmd)
    if not exe:
        return None
    try:
        out = subprocess.run([exe, *args], capture_output=True, text=True, timeout=10)
    except (OSError, subprocess.TimeoutExpired):
        return "found (version unknown)"
    lines = (out.stdout or out.stderr).strip().splitlines()
    return lines[0] if lines else "found"


def check_tools() -> int:
    heading("Toolchain")
    missing = 0
    for cmd, args, why, hint in TOOLS:
        version = tool_version(cmd, args)
        if version:
            print(f"  {OK} {cmd:<7} {version}")
        else:
            optional = "optional" in why
            missing += 0 if optional else 1
            print(f"  {WARN if optional else BAD} {cmd:<7} missing — {why}. Install: {hint}")
    return missing


def check_setup() -> int:
    heading("Setup state")
    todo = 0
    for rel, what, fix in SETUP_STATE:
        if (ROOT / rel).exists():
            print(f"  {OK} {what} ({rel})")
        else:
            todo += 1
            print(f"  {BAD} {what} not installed — run `{fix}`")
    env_files = [name for name in (".env", ".dev.env") if (ROOT / name).exists()]
    if env_files:
        print(f"  {OK} env overrides: {', '.join(env_files)}")
    else:
        print(f"  {WARN} no .env — fine; Taskfile.yml provides dev defaults")
    return todo


def print_table(rows: list[tuple[str, str]]) -> None:
    width = max(len(left) for left, _ in rows)
    for left, right in rows:
        print(f"  {left:<{width}}  {right}")


def main() -> None:
    print("Mealie onboarding — FastAPI (Python 3.14) + Nuxt 4, SQLite/PostgreSQL")
    missing = check_tools()
    todo = check_setup()

    heading("Repo map")
    print_table(REPO_MAP)

    heading("Read next, in order")
    print_table(READING)

    heading("Everyday commands (task --list for all)")
    print_table(COMMANDS)

    heading("Next steps")
    if missing:
        print(f"  1. Install the {missing} missing tool(s) above, or open the repo in the Dev Container.")
    elif todo:
        print("  1. Run `task setup`.")
    else:
        print("  1. You're set up. Start `task py` and `task ui` in two terminals.")
    print("  2. Read docs/architecture.md (focus on the worked request trace).")
    print("  3. Using Claude Code? Run `/onboard` for a guided tour, `/trace <feature>` to follow any feature.")
    print()


if __name__ == "__main__":
    main()
