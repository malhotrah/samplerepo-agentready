#!/usr/bin/env node
// PostToolUse hook: auto-formats a .py file with ruff right after Claude edits it,
// so formatting is never something Claude needs to think about or spend a turn on.
const { execFileSync } = require("child_process");

let input = "";
process.stdin.on("data", (chunk) => (input += chunk));
process.stdin.on("end", () => {
  let payload;
  try {
    payload = JSON.parse(input);
  } catch {
    process.exit(0);
  }

  const path = payload?.tool_input?.file_path || "";
  if (!path.endsWith(".py")) process.exit(0);

  try {
    execFileSync("uv", ["run", "ruff", "format", path], { stdio: "ignore" });
  } catch {
    // best-effort: don't block the agent if ruff/uv isn't set up
  }
  process.exit(0);
});
