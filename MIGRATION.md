# Moving frankschmitt.org from DreamHost to GitHub Pages

Current state, as of this writing:

- `frankschmitt.org` A record → `69.163.177.182` (DreamHost shared hosting)
- Nameservers → `ns1/ns2/ns3.dreamhost.com`
- Registrar → DreamHost
- **MX → `ASPMX.L.GOOGLE.COM` — your mail. Do not touch this.**

The plan keeps the domain and DNS at DreamHost and only repoints the web
records. Nothing in this document affects email.

## 1. Back up the old site first

Before changing anything, pull down what DreamHost is serving. It's one page,
but it's the only copy:

```bash
curl -sSL https://frankschmitt.org/ -o ~/Desktop/frankschmitt-org-2015-backup.html
```

If you have other files in the DreamHost web root that aren't linked from the
homepage, grab those over SFTP too.

## 2. Create the GitHub repo and push

```bash
gh repo create frankus/frankschmitt.org --public --source . --remote origin --push
```

No `gh` installed? Create `frankus/frankschmitt.org` in the web UI, then:

```bash
git remote add origin git@github.com:frankus/frankschmitt.org.git
git push -u origin main
```

## 3. Turn on Pages

Repo → **Settings** → **Pages** → **Build and deployment** → Source:
**GitHub Actions**.

Push to `main` and the workflow builds and deploys. Confirm the site is live at
`https://frankus.github.io/frankschmitt.org/` before touching DNS. (It will
look unstyled at that URL because `base_url` is set to the real domain — that's
expected and resolves itself once the custom domain is attached.)

## 4. Add the custom domain in GitHub

Settings → Pages → **Custom domain** → `frankschmitt.org` → Save.

The repo already contains `static/CNAME`, which Zola copies to the site root,
so this should stick across deploys.

## 5. Stop DreamHost from serving the domain

In the DreamHost panel: **Websites** → **Manage Websites** → `frankschmitt.org`
→ remove the hosting / change it to **DNS only**.

This is the step that matters. As long as the domain is "fully hosted" there,
DreamHost owns the A record and will overwrite or fight your changes. Removing
hosting keeps the domain registration and DNS zone intact — **it does not touch
your MX records or your Google mail.**

## 6. Point DNS at GitHub

In the DreamHost DNS editor for `frankschmitt.org`, add:

| Type | Host | Value |
| --- | --- | --- |
| A | (blank / `@`) | `185.199.108.153` |
| A | (blank / `@`) | `185.199.109.153` |
| A | (blank / `@`) | `185.199.110.153` |
| A | (blank / `@`) | `185.199.111.153` |
| AAAA | (blank / `@`) | `2606:50c0:8000::153` |
| AAAA | (blank / `@`) | `2606:50c0:8001::153` |
| AAAA | (blank / `@`) | `2606:50c0:8002::153` |
| AAAA | (blank / `@`) | `2606:50c0:8003::153` |
| CNAME | `www` | `frankus.github.io.` |

Remove the old A record pointing at `69.163.177.182`. **Leave every MX record
exactly as it is.**

Verify:

```bash
dig +short frankschmitt.org A
dig +short frankschmitt.org MX   # must still be ASPMX.L.GOOGLE.COM
```

## 7. Enforce HTTPS

Once DNS has propagated, GitHub provisions a Let's Encrypt certificate —
usually minutes, occasionally up to an hour. Then Settings → Pages →
**Enforce HTTPS**.

This also fixes something the old setup never did: `http://frankschmitt.org`
currently returns 200 over plain HTTP instead of redirecting.

## 8. Only then, cancel DreamHost hosting

Keep the **domain registration** with DreamHost — that's what holds the DNS
zone your mail depends on. Cancel only the **web hosting plan**.

Give it a week of the new site being live first.

## Old URLs

Posts recovered from the 2007–2010 site keep their original paths via
`aliases` in their front matter, so `frankschmitt.org/2007/04/judging` still
resolves after the move.

These old pages were never recovered and will 404 — recreate them if you want
them: `/bio`, `/contact`, `/projects`, `/support`, `/credits`, `/resume`.
Links to them inside imported posts point at the Internet Archive instead of
dead-ending.
