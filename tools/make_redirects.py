"""Generate static redirect stubs for retired post URLs.

GitHub Pages can't serve a 301, so each stub is a meta-refresh page pointing
at the Internet Archive, with a visible link for anything that ignores it.
Written into static/, which Zola copies verbatim — so these never become Zola
pages and never appear in the feed, the archive list or the sitemap.
"""
import html, os

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Retired posts worth keeping reachable, chosen by Internet Archive recrawl
# count as a proxy for inbound links. All five are how-tos; the rest of the
# retired set was crawled once each.
REDIRECTS = [
    ("/2008/01/gmail-sub-account", 'Creating a “Sub Account” with GMail and Mail.app'),
    ("/2007/12/howto-disable-the-annoying-new-emacs-splash-screen", "HOWTO Disable that annoying Emacs Splashscreen"),
    ("/2008/01/easier-sub-account", 'Easier “Sub-Account” for GMail'),
    ("/2010/06/text-renderingoptimizelegibility", "text-rendering:optimizeLegibility;"),
    ("/2010/06/123together-com-setup-with-mac-os-x-mail-app", "123Together.com Setup with Mac OS X Mail.app"),
]

PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="robots" content="noindex">
<meta http-equiv="refresh" content="0; url={archive}">
<link rel="canonical" href="{archive}">
<title>{title} — moved</title>
<style>
  body {{ margin: 0; padding: 4rem 1.25rem; background: #fdfdfc; color: #1c1f23;
         font: 400 1.0625rem/1.6 -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, sans-serif; }}
  main {{ max-width: 34rem; margin: 0 auto; }}
  h1 {{ font-size: 1.25rem; font-weight: 600; margin: 0 0 1rem; }}
  a {{ color: #2a5d8f; }}
  p {{ margin: 0 0 1rem; }}
  .small {{ font-size: 0.875rem; color: #5b636d; }}
  @media (prefers-color-scheme: dark) {{
    body {{ background: #16181b; color: #e8e8e6; }}
    a {{ color: #7fb2e0; }}
    .small {{ color: #a3aab3; }}
  }}
</style>
</head>
<body>
<main>
  <h1>{title}</h1>
  <p>This post isn’t published here any more. The Internet Archive has a copy:</p>
  <p><a href="{archive}">{archive}</a></p>
  <p class="small">You should be redirected automatically.
     <a href="/">Back to frankschmitt.org</a>.</p>
</main>
</body>
</html>
"""

written = 0
for path, title in REDIRECTS:
    archive = "https://web.archive.org/web/2010/http://frankschmitt.org" + path
    out = os.path.join(SITE, "static", path.lstrip("/"), "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as f:
        f.write(PAGE.format(archive=html.escape(archive, quote=True), title=html.escape(title)))
    written += 1
    print("wrote static" + path + "/index.html")
print(f"\n{written} redirect stubs")
