#!/usr/bin/env node
// PreToolUse hook: refuses edits to files AGENTS.md marks as generated/do-not-edit.
const PROTECTED = [
  /frontend[\\/]app[\\/]lib[\\/]api[\\/]types[\\/]/,
  /mealie[\\/]schema[\\/].*__init__\.py$/,
  /tests[\\/]utils[\\/]api_routes[\\/]__init__\.py$/,
];

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
  const hit = PROTECTED.some((re) => re.test(path));

  if (hit) {
    process.stderr.write(
      `${path} is generated (see AGENTS.md "Common Gotchas"). ` +
        `Edit the Pydantic schema / source instead and run "task dev:generate".`
    );
    process.exit(2); // exit code 2 = block the tool call, message is fed back to Claude
  }

  process.exit(0);
});
