import json, pathlib, re, sys
import markdown

draft_path, slug = sys.argv[1], sys.argv[2]
d = json.load(open(draft_path))
body = d["body"].replace(" \u2014 ", ", ").replace(" \u2013 ", ", ")
body = body.replace(
    "WHAT DOES A CAMERA SERVICE NEED TO KNOW ABOUT DEFENDER?",
    "WHY DOES A CAMERA SERVICE TOUCH DEFENDER?",
)
html = markdown.markdown(body, extensions=["extra", "sane_lists"])
m = re.search(r"(?is)<h2[^>]*>\s*Sources\s*</h2>(.*)$", html)
sources = ""
if m:
    sources = m.group(1)
    html = html[:m.start()]

index_path = pathlib.Path("index.html")
index = index_path.read_text()
entry = (
    f'<a href="articles/{slug}.html"><b>{d["title"]}</b>'
    f'<span>{d["standfirst"]}</span></a>'
)
if slug not in index:
    index = index.replace('<div class="list" id="list"></div>',
                          f'<div class="list" id="list">{entry}</div>')
    index_path.write_text(index)

page = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{d['title']} · Riftweld preview</title><link rel="stylesheet" href="../assets/style.css"></head>
<body><div class="wrap">
<p class="eyebrow">Riftweld · headless writer test</p>
<h1>{d['title']}</h1>
<p class="standfirst">{d['standfirst']}</p>
<div class="meta"><span>Style: {d.get('author_name','')}</span><span>Status: review</span><span>Report 466</span></div>
{html}
<div class="src"><strong>Sources</strong>{sources}</div>
<footer>Preview build from the headless writer session. Not the Riftweld production site.</footer>
</div></body></html>"""
out = pathlib.Path("articles") / f"{slug}.html"
out.write_text(page)
print(out)
