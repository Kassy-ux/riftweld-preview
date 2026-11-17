import sys, pathlib, re, json
import markdown

src, title, standfirst, out = sys.argv[1:5]
md = pathlib.Path(src).read_text()
html = markdown.markdown(md, extensions=["extra", "sane_lists"])
# split off the trailing Sources heading into a styled block
m = re.search(r"(?is)<h2[^>]*>\s*Sources\s*</h2>(.*)$", html)
sources = ""
if m:
    sources = m.group(1)
    html = html[:m.start()]
page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · Riftweld preview</title><link rel="stylesheet" href="../assets/style.css"></head>
<body><div class="wrap">
<p class="eyebrow">Riftweld · preview</p>
<h1>{title}</h1>
<p class="standfirst">{standfirst}</p>
<div class="meta"><span>Headless writer session</span><span>For review</span></div>
{html}
<div class="src"><strong>Sources</strong>{sources}</div>
<footer>Preview build. Not the Riftweld production site.</footer>
</div></body></html>"""
pathlib.Path(out).write_text(page)
print(out)
