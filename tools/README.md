# Archive import tools

Scripts used to rebuild the 2007–2010 posts from the Internet Archive. Kept
so the import is reproducible, and as a starting point for importing
fcows.blogspot.com into fc-o.ws.

| Script | What it does |
| --- | --- |
| `fetch_months.py` | Downloads the archived monthly index pages. Picks the largest 200-status capture per month, which is what makes this work — the 2008 crawl truncated pages at ~6KB, the 2011 crawl stored them whole. |
| `rescue.py` | For posts the monthly pages only show an excerpt of (WordPress `<!--more-->`), tries to find a complete single-post capture. |
| `import_wp.py` | Parses both, converts to markdown, writes `content/blog/*.md` with front matter, aliases for old URLs, and downloads images. |
| `h2md.py` | Small HTML→Markdown converter for 2007-era WordPress bodies. No dependencies. |

They hardcode paths under a scratch directory (`S = ...`) — point that at a
working directory before rerunning.

## Importing the blogspot archive

`../archive-sources/fcows-blogspot-export.json` already holds all 95 posts
from fcows.blogspot.com with full content — no scraping needed. Each entry
has `title.$t`, `published.$t`, `content.$t` (HTML), and `link[].href` for
the original permalink. Feed `h2md.convert()` the content and write front
matter the same way `import_wp.py` does.
