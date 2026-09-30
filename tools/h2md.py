"""Minimal HTML -> Markdown for 2007-era WordPress post bodies."""
import re
from html.parser import HTMLParser

BLOCK_IN_P = {"pre", "blockquote", "ul", "ol", "table", "hr",
                "h1", "h2", "h3", "h4", "h5", "h6"}
VOID = {"br", "hr", "img", "input", "meta", "link"}
INLINE = {"a", "em", "i", "strong", "b", "code", "span", "sub", "sup", "abbr", "u", "s", "strike", "del", "cite", "small", "tt"}


class Node:
    __slots__ = ("tag", "attrs", "kids")
    def __init__(self, tag, attrs=None):
        self.tag, self.attrs, self.kids = tag, dict(attrs or {}), []


class Tree(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.root = Node("#root")
        self.stack = [self.root]

    def handle_starttag(self, tag, attrs):
        n = Node(tag, attrs)
        self.stack[-1].kids.append(n)
        if tag not in VOID:
            self.stack.append(n)

    def handle_startendtag(self, tag, attrs):
        self.stack[-1].kids.append(Node(tag, attrs))

    def handle_endtag(self, tag):
        for i in range(len(self.stack) - 1, 0, -1):
            if self.stack[i].tag == tag:
                del self.stack[i:]
                return

    def handle_data(self, data):
        self.stack[-1].kids.append(data)


def esc(t):
    # Escape only what would otherwise become markdown syntax.
    t = re.sub(r"([\\`*_\[\]])", r"\\\1", t)
    return re.sub(r"^(\s*)([#>\-+]|\d+\.)(\s)", r"\1\\\2\3", t)


def inline(node, link_map):
    out = []
    for k in node.kids:
        if isinstance(k, str):
            out.append(esc(re.sub(r"\s+", " ", k)))
            continue
        t, txt = k.tag, inline(k, link_map)
        if t == "a":
            href = k.attrs.get("href", "")
            title = k.attrs.get("title", "")
            # Some originals shipped an empty href with the real URL in title=.
            if href.rstrip(":/") == "http" or not href.strip():
                if re.match(r"^https?://\S+$", title.strip()):
                    href = title.strip()
            href = link_map(href)
            if not txt.strip():
                continue
            out.append(f"[{txt}]({href})" if href else txt)
        elif t in ("em", "i", "cite"):
            out.append(f"*{txt}*" if txt.strip() else txt)
        elif t in ("strong", "b"):
            out.append(f"**{txt}**" if txt.strip() else txt)
        elif t in ("code", "tt"):
            raw = plain(k)
            out.append(f"`{raw}`" if raw.strip() else raw)
        elif t in ("del", "s", "strike"):
            out.append(f"~~{txt}~~")
        elif t == "br":
            out.append("  \n")
        elif t == "img":
            src = link_map(k.attrs.get("src", ""))
            alt = k.attrs.get("alt", "").strip()
            out.append(f"![{alt}]({src})" if src else "")
        else:
            out.append(txt)
    return "".join(out)


def plain(node):
    if isinstance(node, str):
        return node
    return "".join(plain(k) for k in node.kids)


def block(node, link_map, depth=0):
    """Render children of `node` as markdown blocks."""
    chunks, buf = [], []

    def flush():
        if buf:
            s = "".join(buf).strip()
            if s:
                chunks.append(s)
            buf.clear()

    for k in node.kids:
        if isinstance(k, str):
            if k.strip():
                buf.append(esc(re.sub(r"\s+", " ", k)))
            continue
        t = k.tag
        if t in INLINE or t in ("br", "img"):
            wrapper = Node("#w")
            wrapper.kids = [k]
            buf.append(inline(wrapper, link_map))
            continue
        flush()
        if t == "p":
            # Some sources nest block elements inside <p> (WordPress wrapped
            # <pre><code> that way). Flattening those to inline code loses the
            # code block, so recurse when a paragraph holds block children.
            if any(not isinstance(c, str) and c.tag in BLOCK_IN_P for c in k.kids):
                inner = block(k, link_map, depth + 1)
                if inner.strip():
                    chunks.append(inner)
            else:
                s = inline(k, link_map).strip()
                if s:
                    chunks.append(s)
        elif t == "blockquote":
            inner = block(k, link_map, depth + 1)
            chunks.append("\n".join("> " + l if l else ">" for l in inner.split("\n")))
        elif t in ("ul", "ol"):
            items = []
            n = 1
            for li in k.kids:
                if isinstance(li, str) or li.tag != "li":
                    continue
                inner = block(li, link_map, depth + 1)
                marker = f"{n}. " if t == "ol" else "- "
                n += 1
                pad = " " * len(marker)
                lines = inner.split("\n")
                items.append(marker + ("\n".join([lines[0]] + [pad + l if l else "" for l in lines[1:]]) if lines else ""))
            chunks.append("\n".join(items))
        elif t == "pre":
            code = plain(k).strip("\n")
            chunks.append("```\n" + code + "\n```")
        elif t in ("h1", "h2", "h3", "h4", "h5", "h6"):
            lvl = min(int(t[1]) + 1, 6)
            chunks.append("#" * lvl + " " + inline(k, link_map).strip())
        elif t == "hr":
            chunks.append("---")
        elif t in ("div", "center", "section", "article", "figure"):
            inner = block(k, link_map, depth + 1)
            if inner.strip():
                chunks.append(inner)
        elif t == "figcaption":
            chunks.append("*" + inline(k, link_map).strip() + "*")
        elif t == "table":
            chunks.append(re.sub(r"\n{3,}", "\n\n", raw_html(k)))
        elif t in ("script", "style", "iframe", "object", "embed"):
            continue
        else:
            inner = block(k, link_map, depth + 1)
            if inner.strip():
                chunks.append(inner)
    flush()
    return "\n\n".join(c for c in chunks if c.strip())


def raw_html(node):
    if isinstance(node, str):
        return node
    a = "".join(f' {k}="{v}"' for k, v in node.attrs.items())
    if node.tag in VOID:
        return f"<{node.tag}{a} />"
    return f"<{node.tag}{a}>" + "".join(raw_html(k) for k in node.kids) + f"</{node.tag}>"


def convert(html, link_map=lambda u: u):
    p = Tree()
    p.feed(html)
    p.close()
    md = block(p.root, link_map)
    md = re.sub(r"[ \t]+\n", "\n", md)
    md = re.sub(r"\n{3,}", "\n\n", md)
    return md.strip()
