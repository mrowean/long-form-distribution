# Privacy

long-form-distribution collects nothing. It has no accounts, no analytics and no telemetry, and the author never receives any of your data.

## What stays on your machine

- Issue files, source text, the posting log, cover images and the optional voice file are written to `~/distribution-tracker/` (or wherever `LFD_HOME` points).
- The dashboard server listens only on 127.0.0.1 and only answers requests made from its own page.
- You can read, edit or delete any of these files at any time.

## What leaves your machine

- **The article URL you give it.** Your agent fetches it, or opens it in your browser if you allow that, to read the piece.
- **Your agent's model provider.** The piece's text and the drafted posts pass through the AI agent you run the plugin in (for example Claude Code or Codex). That provider handles them under its own privacy policy. The plugin adds no other service.

Nothing is posted to any social platform for you. You copy each post and publish it yourself.

## Contact

Questions: open an issue at https://github.com/mrowean/long-form-distribution/issues. Security reports: see [SECURITY.md](SECURITY.md).
