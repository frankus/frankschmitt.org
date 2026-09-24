import json, os, re, time, urllib.request, urllib.parse
S = "/private/tmp/claude-501/-Users-frank-Claude/0d3b9bcb-01cb-4274-9df5-c082b3749b6c/scratchpad"
OUT = os.path.join(S, "rescued"); os.makedirs(OUT, exist_ok=True)

TARGETS = {
 "blank-uilabels-in-iphone-os-2x": "/2009/03/blank-uilabels-in-iphone-os-2x",
 "ecvt-bicycle": "/2007/04/ecvt-bicycle",
 "gmail-sub-account": "/2008/01/gmail-sub-account",
 "comboboxen": "/2007/06/comboboxen",
 "ibrick": "/2007/09/ibrick",
 "ten-reasons-why-the-us-needs-a-carbon-tax": "/2007/04/ten-reasons-why-the-us-needs-a-carbon-tax",
}
UA = {"User-Agent": "frankschmitt.org-archive-import/1.0", "Accept-Encoding": "identity"}

def get(u, t=50):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=t).read().decode("utf-8","replace")

for slug, path in TARGETS.items():
    dest = os.path.join(OUT, slug + ".html")
    if os.path.exists(dest):
        print(f"{slug}: cached"); continue
    try:
        rows = json.loads(get("http://web.archive.org/cdx/search/cdx?url=" +
              urllib.parse.quote("frankschmitt.org"+path) + "&output=json&fl=timestamp,length,statuscode&limit=40"))
    except Exception as e:
        print(f"{slug}: cdx fail {e}"); continue
    rows = rows[1:] if rows and rows[0][0]=="timestamp" else rows
    ok = sorted([r for r in rows if r[2]=="200"], key=lambda r: int(r[1] or 0), reverse=True)
    got = False
    for ts, ln, _ in ok[:6]:
        try:
            h = get(f"http://web.archive.org/web/{ts}id_/http://frankschmitt.org{path}")
        except Exception as e:
            print(f"  {slug} {ts}: fetch fail {e}"); continue
        complete = "END POST-ENTRY" in h or re.search(r'</html>\s*$', h)
        has_more = "#more-" in h
        print(f"  {slug} {ts}: {len(h)}b complete={bool(complete)} more_tag={has_more}")
        if complete and not has_more:
            open(dest,"w",encoding="utf-8").write(h); got = True
            print(f"  -> RESCUED {slug}"); break
        time.sleep(0.8)
    if not got:
        print(f"{slug}: NO COMPLETE CAPTURE")
