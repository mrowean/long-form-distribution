---
name: distribute
description: Turn a published long-form piece (newsletter issue, essay, blog post) into platform-native social posts built from the author's own sentences, then track which ones went live on a local dashboard. Use when the user gives a published URL and wants to distribute it, or asks to open their posting list or distribution dashboard.
argument-hint: <published-issue-url> | dashboard
---

# Distribute

One published piece → a set of posts for LinkedIn, X, Substack Notes (and Threads or Bluesky if asked) → a checklist on a local dashboard where the user ticks each post off and pastes its live link.

Everything stays on the user's machine. The dashboard is a small Python server (standard library only) bound to 127.0.0.1. Issue files and the posting log live in `~/distribution-tracker/` unless `LFD_HOME` says otherwise.

Arguments: `$ARGUMENTS`

- If the argument is `dashboard` (or the user only wants to see their list), skip to **Step 6**.
- If there is no URL, ask for the published link. Don't work from a draft that isn't live: the posts link back to it.

## Step 1 — Read the piece

Fetch the URL with WebFetch and ask for the full article text: the title, the publish date, the cover image URL if there is one, and every section heading with the body under it, verbatim. Ask it to leave out navigation, subscribe boxes, footers and comments.

If the fetch comes back truncated or paywalled, say so and ask the user to paste the text. Never fill in a gap from memory or a guess about what the piece says.

Save the text verbatim to `~/distribution-tracker/sources/<slug>.txt` (or `$LFD_HOME/sources/`), with the slug made as in **Step 5**. Step 4 checks every post against this file.

## Step 2 — Split it into sections

Use the piece's own headings. If it has none, split where the topic changes, and name each section with a short phrase taken from its own text.

Classify each section as:

- **feature**: 250+ words with an argument, a story or a number that stands alone. Worth 2–3 posts.
- **brief**: shorter, a link or an aside. Worth one post at most, often none.

## Step 3 — Show the table and wait

Show a table with these columns:

| # | Section | Type | Words | Strongest line (verbatim) | Suggested posts |
|---|---------|------|-------|---------------------------|-----------------|

Then ask which sections to distribute and on which platforms. The default is every feature, on LinkedIn, X and Substack Notes. **Wait for the user's answer.** They know which sections they're proud of, and that matters more than word count.

## Step 4 — Write the posts

Build every post out of the author's sentences. That is the whole method: the piece already contains the posts, and your job is to find them and cut them to length. These rules aren't optional:

1. **Start from the author's sentences.** The key line in each post comes from the piece, verbatim or trimmed. Around it, write what the format needs: a lead-in, a line that sets up the point for someone who hasn't read the piece, a reworded sentence that fits the length. Keep that copy plain and in the author's register, and keep it to framing. The claims stay the author's.
2. **Never fabricate.** No numbers, quotes, names, events or results that aren't in the piece. If a post needs a fact the piece doesn't have, leave it out.
3. **A different opening move per platform** for the same section. For example, the number on LinkedIn, the claim on X and the scene on Notes. Two posts that open the same way get scrolled past as duplicates by anyone who follows the author on both.
4. **Platform shape:**
   - **LinkedIn post**: under ~1,300 characters. The first two lines carry it, because that's all that shows before "see more". Short paragraphs. Put the link at the end, or tell the user to put it in the first comment.
   - **X post**: under 280 characters. **X thread**: 3–6 posts numbered `1/`, `2/`, each able to stand alone. The link goes in the last post.
     Tell the user: X can show a new post from an account under 50,000 followers near the top of some feeds, but only in its first two hours (X ranking change, September 30, 2026), and its ranking code weights a reply ten times a like. Post when they can answer replies for those two hours.
   - **Substack Note**: 1–4 sentences, conversational. No link needed when it's posted from the same publication.
   - **Threads / Bluesky**: like X, with a 500 / 300 character limit.
5. **Cut the AI tells** before showing anything:
   - "Here's the thing", "Let that sink in", "In today's fast-paced world"
   - "It's not X, it's Y" used as a reflex
   - "game-changer", "unlock", "delve", "navigate", "landscape", "elevate"
   - tricolons that exist for rhythm alone
   - rhetorical questions as hooks
   - emoji bullets
   - hashtag strings
   - a closing line that sums up a post that already said it
   
   If the author's own text uses one of these, keep it: it's their voice.
6. **Match the author's register.** If the piece is dry, the posts are dry. Don't add enthusiasm or exclamation marks the piece doesn't have.

If the user has a voice file (see **Voice**), read it before writing and follow it over the defaults above.

**Check the posts before showing them.** Write them to a scratch file, separated by lines of `---` (or as the `items` of an issue file), and run:

```bash
python3 "${CLAUDE_SKILL_DIR}/scripts/check_posts.py" --source ~/distribution-tracker/sources/<slug>.txt --posts <file>
```

It marks each line that isn't quoted from the piece as `adapted` (with the source sentence it came from) or `new` (lead-in or framing). Those are expected. It fails on two things: `NEW FACT`, a number, quoted phrase or name that isn't in the piece, and `TOO LONG`, a post over its platform's limit. Fix every failure and run it again. When you show the posts, list the adapted and new lines so the user can check that each one frames the point rather than changing it.

Show the posts grouped by section, and let the user edit or cut any of them before saving.

## Step 5 — Save the issue

Write one JSON file to `~/distribution-tracker/issues/<slug>.json` (or `$LFD_HOME/issues/`). Make the slug lowercase from the title: letters, digits and hyphens only, 60 characters max. Use the same shape as `${CLAUDE_SKILL_DIR}/sample/issues/sample-shortcuts-06.json`:

```json
{
  "slug": "my-newsletter-12-the-title",
  "title": "My Newsletter #12: The Title",
  "url": "https://…the published URL…",
  "published": "YYYY-MM-DD",
  "series": "My Newsletter",
  "cover": "https://…cover image URL, covers/<file>.jpg, or empty…",
  "sections": [{"id": "s1", "title": "…"}],
  "items": [
    {"id": "s1-li", "section": "s1", "platform": "linkedin", "format": "post",
     "label": "Hook over the full section", "copy": "…the post text…"}
  ]
}
```

- `platform` is one of `linkedin`, `x`, `substack`, `threads`, `bluesky`.
- `format` is `post`, `thread` or `note`.
- `label` is a few words the user will recognise in the checklist.
- Every item `id` must be unique within the file.
- Leave out `"sample"`.

If a file for this slug already exists, the issue has been distributed before. Ask before you overwrite it. Ticks and links are stored by item `id` in `log.jsonl`, so keep the existing ids for any post that stays.

## Step 6 — Open the dashboard

Check whether it's already running:

```bash
curl -s -o /dev/null -w '%{http_code}' http://127.0.0.1:8799/api/state
```

If that doesn't print `200`, start it in the background:

```bash
python3 "${CLAUDE_SKILL_DIR}/dashboard/serve.py"
```

Then tell the user to open **http://127.0.0.1:8799**. The new issue is at the top. On the dashboard:

- **Click a post** to see its text, then use **Copy text** to grab it.
- **Tick it** once it's posted.
- **Add link** saves the live URL. The server checks that a LinkedIn link is really from linkedin.com, and so on.
- **Skip** marks a post you've decided not to use.
- **Coverage** shows which sections have never gone out. Those are posts that are already written.
- **Export CSV** downloads every logged link.

If port 8799 is taken, start the server with `--port <another>` and give the user that address.

## Voice (optional, once)

If the user wants posts that sound more like their social writing than their long-form, ask them to paste 5–10 of their own posts that did well. Save the posts verbatim to `~/distribution-tracker/voice.md`, with a short list of patterns you noticed in them. Notice things like how posts open, line length, whether they use questions, and how they close. Read that file at the start of Step 4 from then on. Never write the voice file from guesses or from posts the user didn't give you.
