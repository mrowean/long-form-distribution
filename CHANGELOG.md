# Changelog

## 0.2.4 — 2026-10-28

- **Tested in other agents.** The README has a compatibility table. Codex CLI 0.153.4 and Grok Build 1.0.46 each ran the sample issue from start to finish. Cursor and Gemini CLI are marked untested; the table says why for Gemini CLI.
- **Sandboxed agents get the right message.** `serve.py` used to report every failed port as "already in use". When an agent's sandbox blocks local servers, it now says so, exits with code 4 and prints the command to run in your own terminal. Step 6 of the skill tells the agent to pass that command to you and not to work around the sandbox.
- **The saved link is the one you gave.** In the Grok Build test, the saved issue had a different URL from the one given. Step 5 now says to use the published URL exactly as given.
- **Closing an issue on the dashboard works.** Clicking the open issue's card again hid the post list in the page's state but left it on screen, and its rows stopped responding. The list now disappears as it should.
- **README.** A demo GIF at the top, a one-line install for each agent, and a one-line command that clones the repo and starts the dashboard on the sample issues.

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
