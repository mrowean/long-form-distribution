#!/usr/bin/env python3
"""Check that every post is built from the source piece's own sentences.

Usage:
  python3 check_posts.py --source piece.txt --posts issue.json
  python3 check_posts.py --source piece.txt --posts posts.txt

--source is the piece's full text. --posts is an issue file (the shape in
sample/issues/) or plain text with posts separated by lines of `---`.

Each line of each post is sorted into one of three kinds:

  quoted   every sentence is in the source, ignoring case, punctuation and
           spacing (trimmed sentences count; mark a cut in the middle with
           ... or …)
  adapted  reworded from a source sentence; the closest one is shown
  new      lead-in or framing written for the post

Adapted and new lines are expected: posts need lead-ins and wording that fits
the format. What they must not do is add facts. Any number, quoted phrase or
capitalised name in an adapted or new line that isn't in the source is
flagged NEW FACT. Lines with a URL or [link] are skipped.

Also checks length limits: X 280 per post (and per thread post), Bluesky 300,
Threads 500, LinkedIn 1,300.

Exit code 1 on any NEW FACT or TOO LONG, otherwise 0. Standard library only.
"""
import argparse
import difflib
import json
import re
import sys

LIMITS = {"x": 280, "bluesky": 300, "threads": 500, "linkedin": 1300}
MIN_CHARS = 12  # shorter fragments ("So.", "1/") are too short to check


def norm(s):
    s = s.lower().replace("’", "'").replace("‘", "'")
    s = re.sub(r"['“”\"]", "", s)
    return re.sub(r"[^a-z0-9%$]+", " ", s).strip()


def load_posts(path):
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    if path.endswith(".json"):
        data = json.loads(raw)
        items = data["items"] if isinstance(data, dict) else data
        return [(i.get("id", str(n + 1)), i.get("platform", ""), i.get("format", ""), i["copy"])
                for n, i in enumerate(items)]
    parts = [p.strip() for p in re.split(r"^\s*---\s*$", raw, flags=re.M) if p.strip()]
    return [(str(n + 1), "", "", p) for n, p in enumerate(parts)]


def is_link_line(line):
    return bool(re.search(r"https?://|\[link\]", line, re.I))


def thread_parts(copy):
    """Split an X/Threads/Bluesky thread on its 1/ 2/ 3/ markers."""
    parts = re.split(r"(?m)^\s*(?=\d+/\s)", copy)
    return [p.strip() for p in parts if p.strip()]


def is_quoted(line, source):
    """True if every sentence in the line is in the source."""
    for sent in re.split(r"(?<=[.!?;:])\s+", line):
        for frag in re.split(r"\.\.\.|\u2026", sent):
            n = norm(frag)
            if len(n) >= MIN_CHARS and n not in source:
                return False
    return True


def closest(line, sentences):
    n = norm(line)
    best, score = "", 0.0
    for s in sentences:
        r = difflib.SequenceMatcher(None, n, norm(s), autojunk=False).ratio()
        if r > score:
            best, score = s, r
    return best, score


def new_facts(line, source):
    """Numbers, quoted phrases and capitalised names not in the source."""
    found = []
    # A number passes if it appears in the source next to the same word on
    # either side ("about 15", "15 reached"), so "12 hours" isn't cleared by
    # "September 12".
    for m in re.finditer(r"\$?\d[\d,.]*%?", line):
        num = m.group().rstrip(".,")
        before = re.findall(r"[\w'\u2019]+", line[:m.start()])[-1:]
        after = re.findall(r"[\w'\u2019%]+", line[m.end():])[:1]
        pairs = [norm(" ".join(before + [num])), norm(" ".join([num] + after))]
        if not any(re.search(r"(^| )" + re.escape(p) + r"( |$)", source) for p in pairs if p):
            found.append(" ".join(before + [num] + after))
    for q in re.findall(r"[\"\u201c]([^\"\u201d]{4,})[\"\u201d]", line):
        if norm(q) not in source:
            found.append(f'"{q}"')
    words = re.findall(r"(?<![.!?:]\s)(?<!^)\b([A-Z][\w'\u2019-]+)", line.strip())
    for w in words:
        if not re.search(r"(^| )" + re.escape(norm(w)) + r"( |$)", source):
            found.append(w)
    return found


def check_post(copy, source, sentences):
    notes, failed = [], False
    for line in (l.strip() for l in copy.splitlines()):
        body = re.sub(r"^\s*\d+/\s*", "", line)  # thread numbering
        if not body or is_link_line(body) or is_quoted(body, source):
            continue
        near, score = closest(body, sentences)
        if score >= 0.6:
            notes.append(("adapted", f"{body}\n              from: {near}"))
        else:
            notes.append(("new", body))
        facts = new_facts(body, source)
        if facts:
            notes.append(("NEW FACT", ", ".join(facts)))
            failed = True
    return failed, notes


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--source", required=True, help="the piece's full text")
    ap.add_argument("--posts", required=True, help="issue .json, or text split by ---")
    a = ap.parse_args()

    with open(a.source, encoding="utf-8") as f:
        text = f.read()
    source = norm(text)
    sentences = [x for x in re.split(r"(?<=[.!?])\s+|\n+", text) if len(norm(x)) >= MIN_CHARS]
    posts = load_posts(a.posts)

    failures = 0
    for pid, platform, fmt, copy in posts:
        failed, notes = check_post(copy, source, sentences)
        limit = LIMITS.get(platform)
        if limit:
            chunks = thread_parts(copy) if fmt == "thread" else [copy]
            for c in chunks:
                if len(c) > limit:
                    notes.append(("TOO LONG", f"{len(c)} > {limit}: {c[:60]}…"))
                    failed = True
        failures += failed
        status = "FAIL" if failed else "ok  "
        print(f"{status} {pid}")
        for kind, text in notes:
            print(f"     {kind}: {text}")

    print(f"\n{len(posts) - failures} of {len(posts)} posts pass.")
    print("Adapted and new lines are fine to keep. Read each one: it should frame or fit the")
    print("author's point, not make a new claim.")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
