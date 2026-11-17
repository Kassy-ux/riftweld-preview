import html

INK="#18181b"; MUTED="#52525b"; LINE="#e4e4e7"; ACCENT="#b45309"

def esc(s): return html.escape(str(s), quote=False)

def wrap(label, width=18):
    words=str(label).split(); lines=[]; cur=""
    for w in words:
        if len(cur)+len(w)+1 > width and cur:
            lines.append(cur); cur=w
        else:
            cur=(cur+" "+w).strip()
    if cur: lines.append(cur)
    return lines[:2]

def text_lines(x, y, label, cls="t", width=18, lh=15):
    lines=wrap(label,width); out=[]
    start=y-(len(lines)-1)*lh/2
    for i,l in enumerate(lines):
        out.append(f'<text x="{x}" y="{start+i*lh:.1f}" class="{cls}" text-anchor="middle">{esc(l)}</text>')
    return "\n".join(out)

def frame(h, label):
    return (f'<svg viewBox="0 0 760 {h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{esc(label)}">'
            '<defs><marker id="ar" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            f'<path d="M0 0L10 5L0 10z" fill="{ACCENT}"/></marker></defs>'
            f'<style>.b{{fill:#fff;stroke:{LINE};}} .t{{font:500 13px ui-sans-serif,system-ui;fill:{INK}}} '
            f'.s{{font:400 11px ui-sans-serif,system-ui;fill:{MUTED}}} .a{{stroke:{ACCENT};stroke-width:1.5;fill:none}} '
            f'.d{{fill:{ACCENT}}} .l{{stroke:{LINE};stroke-width:1}}</style>'
            f'<rect x="0" y="0" width="760" height="{h}" fill="#fbfbf8"/>')

def chain_h(labels, caption=""):
    n=len(labels); m=20; gap=18; w=(760-2*m-(n-1)*gap)/n; h=66; y=70
    out=[frame(200, caption or "diagram")]
    for i,lab in enumerate(labels):
        x=m+i*(w+gap)
        out.append(f'<rect class="b" x="{x:.1f}" y="{y}" width="{w:.1f}" height="{h}" rx="6"/>')
        out.append(text_lines(x+w/2, y+h/2, lab, width=16))
        if i < n-1:
            ax=x+w+4; ay=y+h/2; bx=x+w+gap-4
            out.append(f'<line class="a" x1="{ax:.1f}" y1="{ay}" x2="{bx:.1f}" y2="{ay}" marker-end="url(#ar)"/>')
    out.append("</svg>")
    return "".join(out)

def chain_v(labels, caption=""):
    n=len(labels); w=520; x=120; h=48; gap=26; top=20
    out=[frame(top+n*(h+gap)+10, caption or "diagram")]
    for i,lab in enumerate(labels):
        y=top+i*(h+gap)
        out.append(f'<rect class="b" x="{x}" y="{y}" width="{w}" height="{h}" rx="6"/>')
        out.append(f'<text x="{x+w/2}" y="{y+h/2+5}" class="t" text-anchor="middle">{esc(lab)}</text>')
        if i < n-1:
            out.append(f'<line class="a" x1="{x+w/2}" y1="{y+h}" x2="{x+w/2}" y2="{y+h+gap-4}" marker-end="url(#ar)"/>')
    out.append("</svg>")
    return "".join(out)

def timeline(events, caption=""):
    n=len(events); out=[frame(210, caption or "timeline")]
    y=110; x0=50; x1=710; step=(x1-x0)/(n-1)
    out.append(f'<line class="l" x1="{x0}" y1="{y}" x2="{x1}" y2="{y}"/>')
    for i,(date,label) in enumerate(events):
        x=x0+i*step
        out.append(f'<circle cx="{x:.1f}" cy="{y}" r="5" class="d"/>')
        out.append(f'<text x="{x:.1f}" y="{y-22}" class="s" text-anchor="middle">{esc(date)}</text>')
        out.append(text_lines(x, y+40 if i%2==0 else y+72, label, width=15))
    out.append("</svg>")
    return "".join(out)

def matrix(rows, headers, caption=""):
    out=[frame(70+len(rows)*62, caption or "matrix")]
    cw=350; x1=20; x2=390
    out.append(f'<rect class="b" x="{x1}" y="20" width="{cw}" height="44" rx="6"/>')
    out.append(f'<rect class="b" x="{x2}" y="20" width="{cw}" height="44" rx="6"/>')
    out.append(f'<text x="{x1+cw/2}" y="47" class="t" text-anchor="middle">{esc(headers[0])}</text>')
    out.append(f'<text x="{x2+cw/2}" y="47" class="t" text-anchor="middle">{esc(headers[1])}</text>')
    for i,(a,b) in enumerate(rows):
        y=76+i*62
        out.append(f'<rect class="b" x="{x1}" y="{y}" width="{cw}" height="52" rx="6"/>')
        out.append(f'<rect class="b" x="{x2}" y="{y}" width="{cw}" height="52" rx="6"/>')
        out.append(text_lines(x1+cw/2, y+26, a, width=34))
        out.append(text_lines(x2+cw/2, y+26, b, width=34))
    out.append("</svg>")
    return "".join(out)

def stack(labels, caption=""):
    n=len(labels); out=[frame(20+n*72, caption or "stack")]
    w=480; x=140; h=50; gap=22
    for i,lab in enumerate(labels):
        y=20+i*(h+gap)
        out.append(f'<rect class="b" x="{x}" y="{y}" width="{w}" height="{h}" rx="6"/>')
        out.append(f'<text x="{x+w/2}" y="{y+h/2+5}" class="t" text-anchor="middle">{esc(lab)}</text>')
        if i < n-1:
            out.append(f'<line class="a" x1="{x+w/2}" y1="{y+h}" x2="{x+w/2}" y2="{y+h+gap-4}" marker-end="url(#ar)"/>')
    out.append("</svg>")
    return "".join(out)

DIAGRAMS = {
 "who-was-mining-crypto-on-13-organizations-camera-servers-and-which-flaw-let-them-in": {
   "position":"top","caption":"Execution chain observed by Huntress. The initial access vector is not publicly confirmed.",
   "svg":chain_v(["GeoStartupAgentService.exe (SYSTEM)","PowerShell download cradle","Scripts a / b / c","kvckiller.sys (BYOVD)","IFEO hijacks (Defender)","update.exe loader (DHT/PKARR)","XMRig miner"])},
 "a-mining-ceo-blamed-ai-the-blockchain-kept-its-own-notes": {
   "position":"top","caption":"The public record around the Luxor redirect. Times UTC unless noted.",
   "svg":timeline([("7 Nov 02:40","cctv-update.top registered"),("8-10 Nov","13 organisations hit"),("15 Nov 03:08","CoreX public alert"),("15 Nov 17:25","Luxor statement"),("15 Nov 22:54","second payout")])},
 "selling-ai-and-blaming-ai-were-never-the-same-decision": {
   "position":"bottom","caption":"The trust ledger: what the response did, and what it cost.",
   "svg":matrix([("Patched in two hours","The fix was fast; the story is still open"),("Paid clients in full","Money answers the loss, not the question"),("Called it AI-enabled","A claim with no mechanism")],("What Luxor did","What it cost in trust"))},
 "someone-moved-the-pool-settings-what-the-luxor-commander-hijack-teaches-us": {
   "position":"top","caption":"The defender checklist from the article.",
   "svg":chain_h(["Patch Commander","Restrict access","Check pool settings","Rotate API keys"])},
 "a-dashboard-is-a-load-bearing-wall": {
   "position":"top","caption":"The convenience and the risk are the same feature.",
   "svg":stack(["One dashboard","Hundreds of rigs","One credential","One redirect","Systemic leverage"])},
 "bulk-discount-how-a-fleet-manager-s-pool-setting-redirected-bitcoin-hashrate": {
   "position":"top","caption":"What is documented, in order, and where the record stops.",
   "svg":chain_h(["Commander","Change Pool Settings","OCEAN pool","0.162 BTC paid","No post-mortem"])},
}
