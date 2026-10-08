from pathlib import Path
import json,html,math
ROOT=Path(__file__).resolve().parent
D=ROOT/'dist'
PAPERS=json.loads((ROOT/'content/papers.json').read_text())
e=html.escape
ORIGIN=json.loads((ROOT/'content/site.json').read_text()).get('origin','') if (ROOT/'content/site.json').exists() else ''
def chart(dark=False):
    n=1800;zs=[i/n for i in range(n+1)];arc=[0.]
    for i,z in enumerate(zs[1:],1):
        v=zs[i-1];arc.append(arc[-1]+math.hypot(z*z-v*v,(1-z)**4-(1-v)**4))
    def solve(w):
        if w==0:return 1.
        if w==1:return 0.
        lo,hi=0.,1.
        for _ in range(50):
            z=(lo+hi)/2
            if 2*w*z-4*(1-w)*(1-z)**3>0:hi=z
            else:lo=z
        return (lo+hi)/2
    def inv(q):
        import bisect
        j=min(n,max(1,bisect.bisect_left(arc,q*arc[-1])))
        return (j-1+(q*arc[-1]-arc[j-1])/(arc[j]-arc[j-1]))/n
    xy=lambda z:(45+350*z*z,235-190*(1-z)**4)
    pts=' '.join(f'{x:.2f},{y:.2f}' for x,y in map(xy,zs[::12]))
    dots=''
    for z in [solve(i/7) for i in range(8)]:
        x,y=xy(z);dots+=f'<circle cx="{x:.2f}" cy="{y:.2f}" r="6" fill="#354ac6" stroke="white" stroke-width="1.3"/>'
    for z in [inv(i/7) for i in range(8)]:
        x,y=xy(z);dots+=f'<circle cx="{x:.2f}" cy="{y:.2f}" r="4" fill="#007c70" stroke="white" stroke-width="1"/>'
    return f'<svg viewBox="0 0 430 310" role="img" aria-label="Exact toy Pareto front comparing equally spaced weights in blue and equally spaced arc lengths in green"><path d="M45 30 V235 H400" fill="none" stroke="#9aabc7"/><polyline points="{pts}" fill="none" stroke="#aab5c8" stroke-width="2"/>{dots}<text x="215" y="265" fill="#526077" font-size="15" text-anchor="middle">Objective 1 = z²</text><text x="30" y="130" fill="#526077" font-size="15" text-anchor="middle" transform="rotate(-90 30 130)">Objective 2 = (1 − z)⁴</text><circle cx="65" cy="294" r="5" fill="#354ac6"/><text x="77" y="299" font-size="15" fill="#526077">Equal weights</text><circle cx="255" cy="294" r="5" fill="#007c70"/><text x="267" y="299" font-size="15" fill="#526077">Equal distance</text></svg>'
def head(title,desc,depth=0,path=''):
    b='../'*depth
    canonical=f'<link rel="canonical" href="{ORIGIN}/{path}"><meta property="og:url" content="{ORIGIN}/{path}">' if ORIGIN else ''
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{e(title)}</title><meta name="description" content="{e(desc)}"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:type" content="website">{canonical}<link rel="stylesheet" href="{b}assets/style.css"><link rel="icon" type="image/svg+xml" href="data:image/svg+xml,%3Csvg xmlns=%27http://www.w3.org/2000/svg%27 viewBox=%270 0 32 32%27%3E%3Crect width=%2732%27 height=%2732%27 rx=%2716%27 fill=%27%23111d34%27/%3E%3Ctext x=%275%27 y=%2721%27 fill=%27white%27 font-size=%2714%27 font-family=%27Arial%27%3ELJ%3C/text%3E%3C/svg%3E"></head><body><a class="skip" href="#main">Skip to content</a><header class="site-header"><div class="wrap header-inner"><a class="brand" href="{b}index.html"><span class="monogram">LJ</span>Liuyuan Jiang <span class="note">/ Research</span></a><nav aria-label="Main navigation"><a href="{b}index.html#papers">Papers</a><a href="{b}index.html#about">About</a><a href="https://liuyuan999.github.io/">Homepage</a><a href="mailto:ljiang24@ur.rochester.edu">Contact</a></nav></div></header>'
def footer(depth=0):
    b='../'*depth
    return f'<footer class="footer"><div class="wrap"><span>Liuyuan Jiang · University of Rochester</span><span><a href="{b}index.html#papers">Research collection</a> · Updated October 8, 2026</span></div></footer><script src="{b}assets/site.js" defer></script></body></html>'
def save(path,s):
    target=D/path;target.parent.mkdir(parents=True,exist_ok=True);target.write_text(s)
def home():
    A=json.loads((ROOT/'content/articles.json').read_text())
    hooks={'surf':'Even preferences. Uneven trade-offs.','retailagent':'When an agent chooses the wrong moment.','birq':'Let a speech model improve its own targets.','efficient-penalty':'Rethink the cost of a bilevel update.','pbgd-free':'When can we let go of the inner solve?','smoothness':'The curvature bound was hiding a cancellation.','blocc':'The leader changes the follower’s choices.'}
    cards=''
    for i,p in enumerate(PAPERS,1):
        cards+=f'<article class="paper-card"><span class="paper-number">{i:02}</span><div><div class="meta"><span class="venue">{e(p["venue"])}</span><span>{p["year"]}</span></div><p class="paper-label">{e(p["short"])} · {e(p["topic"])}</p><h3><a href="papers/{p["slug"]}/">{e(hooks[p["slug"]])}</a></h3><p>{e(p["description"])}</p><div class="card-actions"><a href="papers/{p["slug"]}/">Project page</a><a href="videos/{p["slug"]}/">Video storyboard</a></div></div></article>'
    return head('Liuyuan Jiang | Research, explained','Research in bilevel optimization, multi-objective learning, speech representations, and LLM agents.')+f'<main id="main" class="wrap"><section class="hero"><div><div class="eyebrow">Liuyuan Jiang · University of Rochester</div><h1>Research,<br><em>explained.</em></h1><p>I study the geometry and algorithms behind learning with multiple objectives and nested decisions. Here are the questions, ideas, and evidence behind my papers.</p><div class="intro-links"><a class="button primary" href="#papers">Explore the research</a><a class="button" href="https://liuyuan999.github.io/">Academic homepage</a></div></div><div class="hero-art"><div class="eyebrow">Featured research / SURF</div><h2>Even preferences.<br>Uneven trade-offs.</h2>{chart()}<p class="art-caption">Equal changes in a weight can move different distances along a Pareto front. Exact toy scalarization of z² and (1 − z)⁴, with both objectives minimized.</p><a href="papers/surf/">Explore the geometry</a></div></section><section id="papers"><div class="section-top"><h2>Inside the research</h2><span>7 public papers · 2024–2026</span></div><div class="paper-grid">{cards}</div></section><section id="about" class="about"><div><div class="eyebrow">Behind the work</div><h2>Liuyuan Jiang</h2></div><div><p>I am a PhD student in Electrical and Computer Engineering at the University of Rochester, advised by Prof. Lisha Chen. Previously, I was a PhD student at Rensselaer Polytechnic Institute, advised by Prof. Tianyi Chen.</p><p>My work connects optimization theory with applications in language models, speech learning, and decision-making. Each project page combines an accessible explanation with the method, results, and technical scope. Video narration and storyboards have their own pages.</p><div class="intro-links"><a href="mailto:ljiang24@ur.rochester.edu">Email</a><a href="https://liuyuan999.github.io/">Academic profile</a></div></div></section></main>'+footer()
save('index.html',home())
if (ROOT/'content/articles.json').exists():
    exec((ROOT/'render_articles.py').read_text())
print('Generated research hub and available articles.')
