# frankschmitt.org

Personal site, built with [Zola](https://www.getzola.org/) and deployed to
GitHub Pages by the workflow in `.github/workflows/deploy.yml`.

## Working on it

Zola is a single binary — no runtime, no dependency tree.

```sh
zola serve      # http://127.0.0.1:1111, live reload
zola build      # output to public/
zola check      # validate links
```

If `zola` isn't on your PATH, it's at `~/.local/bin/zola`. Add this to
`~/.zshrc`:

```sh
export PATH="$HOME/.local/bin:$PATH"
```

To upgrade Zola later, download a new release from
https://github.com/getzola/zola/releases and replace the binary — then bump
`ZOLA_VERSION` in the deploy workflow so CI matches.

## Writing a post

Create `content/blog/some-slug.md`:

```toml
+++
title = "Post title"
date = 2026-09-23
description = "Optional one-line summary, shown in the archive list."

[taxonomies]
tags = ["swift"]
+++

Body in markdown.
```

Push to `main`; the workflow builds and deploys.

## Layout

| Path | What it is |
| --- | --- |
| `config.toml` | Site config, nav links, syntax highlighting |
| `content/` | Markdown: home, about, résumé, and `blog/` posts |
| `templates/` | Tera templates |
| `sass/style.scss` | The whole stylesheet, compiled to `/style.css` |
| `static/` | Verbatim assets, including `CNAME` for the custom domain |
| `archive-sources/` | Raw exports of the old blogs — see below |

## archive-sources/

Preserved originals, not used by the build:

- `fcows-blogspot-export.json` / `.atom.xml` — all 95 posts from
  fcows.blogspot.com (2005–2007), full content, pulled from the live Blogger
  feed. Earmarked for fc-o.ws.
- `wayback-*.txt` — Internet Archive capture indexes for both old sites.

Posts recovered from the 2007–2010 WordPress site carry
`extra.archived_from` in their front matter and keep their original URLs via
`aliases`.
