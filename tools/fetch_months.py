import json, os, sys, time, urllib.request, urllib.parse

S = "/private/tmp/claude-501/-Users-frank-Claude/0d3b9bcb-01cb-4274-9df5-c082b3749b6c/scratchpad"
CACHE = os.path.join(S, "months")
os.makedirs(CACHE, exist_ok=True)

def get(url, timeout=60):
    req = urllib.request.Request(url, headers={
        "User-Agent": "frankschmitt.org-archive-import/1.0 (personal site migration)",
        "Accept-Encoding": "identity",
    })
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", "replace")

months = [l.strip() for l in open(os.path.join(S, "months.txt")) if l.strip()]
report = []

for m in months:
    slug = m.replace("/", "-")
    out = os.path.join(CACHE, slug + ".html")
    if os.path.exists(out) and os.path.getsize(out) > 2000:
        report.append((m, "cached", os.path.getsize(out)))
        continue
    # pick the fattest 200 capture for this month
    cdx = ("http://web.archive.org/cdx/search/cdx?url=" + urllib.parse.quote(m) +
           "&output=json&fl=timestamp,length,statuscode&limit=40")
    try:
        rows = json.loads(get(cdx) or "[]")
    except Exception as e:
        report.append((m, f"cdx-fail {e}", 0)); continue
    rows = rows[1:] if rows and rows[0][0] == "timestamp" else rows
    ok = [r for r in rows if r[2] == "200"]
    if not ok:
        report.append((m, "no-200", 0)); continue
    ok.sort(key=lambda r: int(r[1] or 0), reverse=True)
    ts = ok[0][0]
    try:
        html = get(f"http://web.archive.org/web/{ts}id_/http://{m}")
    except Exception as e:
        report.append((m, f"fetch-fail {e}", 0)); continue
    open(out, "w", encoding="utf-8").write(html)
    report.append((m, f"ts={ts}", len(html)))
    time.sleep(1.2)

for m, status, size in report:
    print(f"{m:34s} {status:24s} {size:>7} bytes")
