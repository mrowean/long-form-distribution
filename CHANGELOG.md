# Changelog

## 0.2.3 — 2026-10-26

- **Provider-neutral wording.** OpenAI's plugin directory asks skills not to name one vendor's tools. `SKILL.md` now says `<skill-dir>` instead of `${CLAUDE_SKILL_DIR}` and drops `$ARGUMENTS`, "WebFetch in Claude Code" and "Claude in Chrome". The dashboard's hints say to ask your agent instead of quoting a Claude Code slash command. Nothing changes in what the skill does.
- Codex manifest: `shortDescription` is now "Social posts from your essays", inside the directory's 30-character limit.

## 0.2.2 — 2026-10-26

- **The dashboard's code is now its own file.** `index.html` carried its page logic and the sample issues inline, and the Claude plugin directory's scanner flagged it as a file the plugin could run. The logic now lives in `dashboard/app.js` and the sample data in `dashboard/sample-data.js`; `index.html` is markup and styles only. `serve.py` serves the two new files. Nothing changes in how the dashboard looks or works.

## 0.2.1 — 2026-10-09

- **No more `curl` in the skill.** Step 6 used `curl` against 127.0.0.1 to see whether the dashboard was already running. Security scanners read that as sending data to a remote endpoint. The skill now just starts the server, and `serve.py` exits with a clear message (code 3) when the port is already in use.
- Codex manifest: long description, icon and screenshot.
- Added Dependabot for the pinned GitHub Actions, and a `.codexignore`.

## 0.2.0 — 2026-10-09

- **Caveats travel with the claim.** `check_posts.py` warns `CAVEAT?` when a post drops a qualifier, a parenthetical or a following "But…" sentence from its source. Each saved post carries a `source` field, and the dashboard shows it beside the post.
- **Codex support.** Added a `.codex-plugin/plugin.json` manifest. The skill now works in agents that don't set `$ARGUMENTS` or `${CLAUDE_SKILL_DIR}` or have a tool named WebFetch. Tested in Codex CLI 0.160.0.
- **Paywalled posts.** Step 1 spots a cut-short fetch and offers four routes to the full text: your signed-in browser (if your agent has a browser tool, and only with your go-ahead), pasting from your editor, a file path, or your platform's export. It never tries to get around a paywall.
- **Text input.** You can give the text itself, pasted or as a file, together with the published URL.
- Added `PRIVACY.md`, `TERMS.md` and a CI workflow that runs the HOL plugin scanner and the quote check on the sample issues.

## 0.1.0

- First release: the `distribute` skill, the quote check and the local posting-list dashboard.
