"""Rebuild the 2007-2010 frankschmitt.org posts from Internet Archive captures."""
import html as H, os, re, sys, time, urllib.request
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import h2md

S = os.path.dirname(os.path.abspath(__file__))
SITE = "/Users/frank/Claude/frankschmitt.org"
OUT = os.path.join(SITE, "content/blog")
IMGDIR = os.path.join(SITE, "static/archive")
os.makedirs(OUT, exist_ok=True)

POST_RE = re.compile(r'<div id="post-(\d+)"[^>]*class="post"[^>]*>(.*?)<!--\s*END POST\s*-->', re.S | re.I)
TITLE_RE = re.compile(r'<h2 class="post-title">\s*<a href="([^"]+)"[^>]*rel="bookmark"\s*>(.*?)</a>', re.S | re.I)
# Single-post pages render the title without an anchor.
TITLE_PLAIN_RE = re.compile(r'<h2 class="post-title">\s*(?!<a\b)(.*?)</h2>', re.S | re.I)
CANON_RE = re.compile(r'<link[^>]+rel="canonical"[^>]+href="([^"]+)"', re.I)
DATE_RE = re.compile(r'<h3 class="post-date">\s*([0-9]{4}-[0-9]{2}-[0-9]{2}[ T][0-9:]+)\s*</h3>', re.I)
ENTRY_RE = re.compile(r'<div class="post-entry">(.*?)</div>\s*<!--\s*END POST-ENTRY\s*-->', re.S | re.I)
CAT_RE = re.compile(r'/category/([a-z0-9-]+)"[^>]*>([^<]+)</a>', re.I)

SOURCE_DIRS = [os.path.join(S, "months"), os.path.join(S, "rescued")]
sources = []
for d in SOURCE_DIRS:
    if os.path.isdir(d):
        sources += [os.path.join(d, f) for f in sorted(os.listdir(d)) if f.endswith(".html")]

posts = {}
for fp in sources:
    fn = os.path.basename(fp)
    doc = open(fp, encoding="utf-8", errors="replace").read()
    canon = CANON_RE.search(doc)
    for pid, blob in POST_RE.findall(doc):
        tm, dm, em = TITLE_RE.search(blob), DATE_RE.search(blob), ENTRY_RE.search(blob)
        if not em:
            continue
        if tm:
            permalink, title_html = tm.group(1), tm.group(2)
        else:
            tp = TITLE_PLAIN_RE.search(blob)
            if not tp:
                continue
            title_html = tp.group(1)
            permalink = canon.group(1) if canon else ""
            if not permalink and fn.endswith(".html"):
                permalink = "http://frankschmitt.org/" + fn[:-5]
        slug = permalink.rstrip("/").rsplit("/", 1)[-1]
        entry = em.group(1)
        meta_start = blob.find('class="post-metadata"')
        cats = [c.strip().lower() for _, c in CAT_RE.findall(blob[meta_start:] if meta_start > 0 else "")]
        cats = [c for c in cats if c != "uncategorized"]
        rec = {
            "slug": slug,
            "permalink": permalink,
            "title": H.unescape(re.sub(r"<[^>]+>", "", title_html)).strip(),
            "date": dm.group(1).replace(" ", "T") if dm else None,
            "entry": entry,
            "tags": sorted(set(cats)),
            "src": fn,
        }
        prev = posts.get(slug)
        if prev is None:
            posts[slug] = rec
        else:
            # Keep the fullest body, but don't lose metadata the other copy had.
            if len(entry) > len(prev["entry"]):
                prev["entry"], prev["src"] = entry, fn
            prev["date"] = prev["date"] or rec["date"]
            prev["tags"] = prev["tags"] or rec["tags"]
            if "frankschmitt.org/" in rec["permalink"] and re.search(r"/\d{4}/\d{2}/", rec["permalink"]):
                prev["permalink"] = rec["permalink"]

print(f"parsed {len(posts)} distinct posts from {len(sources)} archived pages")

# ---- images -------------------------------------------------------------
img_urls = set()
for p in posts.values():
    for m in re.finditer(r'<img[^>]+src="([^"]+)"', p["entry"], re.I):
        u = m.group(1)
        if "frankschmitt.org" in u or u.startswith("/"):
            img_urls.add(u)

img_map = {}
if img_urls:
    os.makedirs(IMGDIR, exist_ok=True)
for u in sorted(img_urls):
    full = u if u.startswith("http") else "http://frankschmitt.org" + u
    name = re.sub(r"[^A-Za-z0-9._-]", "_", full.rsplit("/", 1)[-1].split("?")[0]) or "image"
    dest = os.path.join(IMGDIR, name)
    if not os.path.exists(dest):
        try:
            req = urllib.request.Request(
                "http://web.archive.org/web/2010id_/" + full,
                headers={"User-Agent": "frankschmitt.org-archive-import/1.0"})
            with urllib.request.urlopen(req, timeout=45) as r:
                data = r.read()
            if len(data) < 64:
                raise ValueError("suspiciously small")
            open(dest, "wb").write(data)
            print(f"  image ok   {name} ({len(data)} bytes)")
            time.sleep(0.8)
        except Exception as e:
            print(f"  image FAIL {full} -> {e}")
            continue
    img_map[u] = "/archive/" + name

# ---- link rewriting -----------------------------------------------------
by_permalink = {p["permalink"].rstrip("/"): p["slug"] for p in posts.values()}

def link_map(u):
    if not u:
        return u
    if u in img_map:
        return img_map[u]
    frag = ""
    if "#" in u:
        u, frag = u.split("#", 1)
        frag = "#" + frag
    key = u.rstrip("/")
    if key in by_permalink:
        return "/blog/%s/%s" % (by_permalink[key], frag)
    m = re.match(r'https?://(?:www\.)?frankschmitt\.org(/.*)?$', key)
    if m:
        path = m.group(1) or "/"
        tail = path.rstrip("/").rsplit("/", 1)[-1]
        if tail in posts:
            return "/blog/%s/%s" % (tail, frag)
        # Old page that no longer exists: point at the archive rather than a 404.
        return "https://web.archive.org/web/2010/http://frankschmitt.org" + path
    return u + frag

def toml_str(s):
    return '"%s"' % s.replace("\\", "\\\\").replace('"', '\\"')

written, skipped = 0, []
for slug, p in sorted(posts.items(), key=lambda kv: kv[1]["date"] or ""):
    partial = bool(re.search(r"#more-\d+", p["entry"]))
    body = h2md.convert(p["entry"], link_map)
    if partial:
        # Drop the dangling "(more…)" link — the rest was never archived.
        body = re.sub(r"\n*\[\(?more[^\]]*\]\([^)]*\)\s*$", "", body).rstrip()
    if not body.strip():
        skipped.append((slug, "empty body"))
        continue
    if not p["date"]:
        skipped.append((slug, "no date"))
        continue
    date = p["date"]
    if len(date) == 19:
        date += "Z"
    old_path = re.sub(r'^https?://(?:www\.)?frankschmitt\.org', "", p["permalink"]).rstrip("/")
    fm = ["+++", "title = " + toml_str(p["title"]), "date = " + date,
          "aliases = [%s]" % toml_str(old_path + "/")]
    if p["tags"]:
        fm += ["", "[taxonomies]", "tags = [%s]" % ", ".join(toml_str(t) for t in p["tags"])]
    fm += ["", "[extra]",
           'archived_from = "frankschmitt.org, %s"' % date[:4]]
    if partial:
        fm += ["partial = true"]
    fm += [
           "+++", "", ""]
    open(os.path.join(OUT, slug + ".md"), "w", encoding="utf-8").write("\n".join(fm) + body + "\n")
    written += 1

print(f"\nwrote {written} posts to content/blog/")
for s, why in skipped:
    print(f"  skipped {s}: {why}")
