import html, json, pathlib, re, sys
import markdown
from diagrams import DIAGRAMS
import pathlib as _pl

draft_path, slug = sys.argv[1], sys.argv[2]
d = json.load(open(draft_path))
authors = json.load(open("authors.json"))
meta = authors.get(d.get("author_id"), {})
title = d["title"].replace(" \u2014 ", ", ").replace(" \u2013 ", ", ")
standfirst = d.get("standfirst", "").replace(" \u2014 ", ", ").replace(" \u2013 ", ", ")
body = d["body"]
if body.startswith("# "):
    cut = body.find("\n## ")
    if cut > 0:
        body = body[cut + 1:]
body = body.replace(" \u2014 ", ", ").replace(" \u2013 ", ", ")
rendered = markdown.markdown(body, extensions=["extra", "sane_lists"])
m = re.search(r"(?is)<h2[^>]*>\s*Sources\s*</h2>(.*)$", rendered)
sources = ""
if m:
    sources = m.group(1)
    rendered = rendered[:m.start()]

photos = json.load(open("photos.json"))
photo = photos.get(slug)
photo_block = ""
if photo:
    credit = html.escape(photo.get("artist") or "Unknown")
    lic = html.escape(photo.get("license") or "")
    lic_url = html.escape(photo.get("license_url") or "")
    lic_html = f'<a href="{lic_url}">{lic}</a>' if lic_url else lic
    photo_block = (
        '<figure class="photo">'
        f'<img src="../{photo["file"]}" alt="{html.escape(photo.get("alt",""))}" loading="lazy">'
        f'<figcaption>{html.escape(photo.get("caption",""))} '
        f'<a href="{html.escape(photo.get("source",""))}">Photo: {credit}</a> / Wikimedia Commons ({lic_html}).</figcaption>'
        '</figure>'
    )

diagram_top = diagram_bottom = ""
diag = DIAGRAMS.get(slug)
if diag:
    block = f'<figure class="diagram">{diag["svg"]}<figcaption>{html.escape(diag["caption"])}</figcaption></figure>'
    if diag.get("position") == "top":
        diagram_top = block
    else:
        diagram_bottom = block

original = ""
if meta:
    original = (
        '<div class="original">'
        f'<p><strong>Reference article by {html.escape(meta["name"])}</strong></p>'
        f'<p><a href="{html.escape(meta["original_url"])}">{html.escape(meta["original_title"])}</a></p>'
        f'<p class="muted">The article above is written in an original voice informed by this author\'s style. It is not by {html.escape(meta["name"])}.</p>'
        '</div>'
    )

rendered_with_photo = rendered
if photo_block:
    if "</h2>" in rendered_with_photo:
        rendered_with_photo = rendered_with_photo.replace("</h2>", "</h2>\n" + photo_block, 1)
    else:
        rendered_with_photo = photo_block + rendered_with_photo

page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} · Riftweld preview</title><link rel="stylesheet" href="../assets/style.css"></head>
<body><div class="wrap">
<p class="eyebrow">Riftweld · headless writer test</p>
<h1>{html.escape(title)}</h1>
<p class="standfirst">{html.escape(standfirst)}</p>
<div class="meta"><span>Style: {html.escape(d.get('author_name',''))}</span><span>Status: review</span></div>
{diagram_top}
{rendered_with_photo}
<div class="src"><strong>Sources</strong>{sources}</div>
{diagram_bottom}
{original}
<footer>Preview build from the headless writer session. Not the Riftweld production site.</footer>
</div></body></html>"""

out = pathlib.Path("articles") / f"{slug}.html"
out.write_text(page)

manifest_path = pathlib.Path("articles.json")
manifest = json.load(open(manifest_path)) if manifest_path.exists() else []
entry = {
    "slug": slug, "title": title, "standfirst": standfirst,
    "author_id": d.get("author_id"), "author_name": d.get("author_name"),
    "original_title": meta.get("original_title"), "original_url": meta.get("original_url"),
}
manifest = [e for e in manifest if e["slug"] != slug] + [entry]
manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")

items = []
for e in manifest:
    ref = ""
    if e.get("original_url"):
        ref = f' · Reference: <a href="{html.escape(e["original_url"])}">{html.escape(e.get("original_title") or "")}</a>'
    items.append(
        '<div class="item">'
        f'<a class="item-title" href="articles/{e["slug"]}.html"><b>{html.escape(e["title"])}</b></a>'
        f'<p class="item-lede">{html.escape(e["standfirst"])}</p>'
        f'<p class="item-meta">Style: {html.escape(e.get("author_name") or "")}{ref}</p>'
        '</div>'
    )

index = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Riftweld article previews</title><link rel="stylesheet" href="assets/style.css"></head>
<body><div class="wrap">
<p class="eyebrow">Riftweld · headless writer test</p>
<h1>Article previews</h1>
<p class="standfirst">Each piece is written in one author's voice. The reference link goes to an original article by that author.</p>
<div class="list">
{''.join(items)}
</div>
<footer>Test host. Not the Riftweld production site. The pieces are original writing informed by the listed author, not by them.</footer>
</div></body></html>"""
pathlib.Path("index.html").write_text(index)
print(out)
