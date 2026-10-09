# Changelog

## 0.2.0 — 2026-10-09

- **Caveats travel with the claim.** `check_posts.py` warns `CAVEAT?` when a post drops a qualifier, a parenthetical or a following "But…" sentence from its source. Each saved post carries a `source` field, and the dashboard shows it beside the post.
- **Codex support.** Added a `.codex-plugin/plugin.json` manifest. The skill now works in agents that don't set `$ARGUMENTS` or `${CLAUDE_SKILL_DIR}` or have a tool named WebFetch. Tested in Codex CLI 0.160.0.
- **Paywalled posts.** Step 1 spots a cut-short fetch and offers four routes to the full text: your signed-in browser (if your agent has a browser tool, and only with your go-ahead), pasting from your editor, a file path, or your platform's export. It never tries to get around a paywall.
- **Text input.** You can give the text itself, pasted or as a file, together with the published URL.
- Added `PRIVACY.md`, `TERMS.md` and a CI workflow that runs the HOL plugin scanner and the quote check on the sample issues.

## 0.1.0

- First release: the `distribute` skill, the quote check and the local posting-list dashboard.
