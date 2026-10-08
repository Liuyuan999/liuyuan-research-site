from pathlib import Path
import json,html,math
ROOT=Path(__file__).resolve().parent
D=ROOT/'dist'
PAPERS=json.loads((ROOT/'content/papers.json').read_text())
e=html.escape
ORIGIN=json.loads((ROOT/'content/site.json').read_text()).get('origin','') if (ROOT/'content/site.json').exists() else ''
def chart(dark=False):
    pts=' '.join(f'{55+300*t},{225-170*(1-t)**2}' for t in [i/80 for i in range(81)])
    col='#bfcbff' if dark else '#354ac6'
    return f'<svg viewBox="0 0 420 280" role="img" aria-label="Illustrative Pareto front with uneven and even point spacing"><path d="M45 30 V235 H385" fill="none" stroke="#9aabc7"/><polyline points="{pts}" fill="none" stroke="{col}" stroke-width="3"/>'+''.join(f'<circle cx="{55+300*t}" cy="{225-170*(1-t)**2}" r="5" fill="{col}"/>' for t in [0,.03,.09,.18,.32,.51,.75,1])+ '<text x="170" y="267" fill="#8392ad" font-size="14">Objective 1</text><text x="12" y="150" fill="#8392ad" font-size="14" transform="rotate(-90 12 150)">Objective 2</text></svg>'
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
    cards=''
    for p in PAPERS:
        cards+=f'<article class="paper-card"><div class="meta"><span class="venue">{e(p["venue"])}</span><span>{p["year"]}</span><span>{e(p["topic"])}</span></div><h3><a href="papers/{p["slug"]}/">{e(p["title"])}</a></h3><p>{e(p["description"])}</p><div class="card-actions"><a href="papers/{p["slug"]}/">Project page</a><a href="papers/{p["slug"]}/#video">Video script</a></div></article>'
    return head('Liuyuan Jiang | Research, explained','Research in bilevel optimization, multi-objective learning, speech representations, and LLM agents.')+f'<main id="main" class="wrap"><section class="hero"><div><div class="eyebrow">Optimization · Machine learning</div><h1>Research,<br><em>explained.</em></h1><p>I’m Liuyuan Jiang, a PhD student at the University of Rochester. I study the geometry and algorithms behind learning with multiple objectives and nested decisions.</p><div class="intro-links"><a href="#papers">Explore the papers</a><a href="https://liuyuan999.github.io/">Academic homepage</a></div></div><div class="hero-art"><div class="eyebrow">A recurring question</div>{chart()}<p class="art-caption">How do our optimization choices shape the solutions we find? Illustrative geometry.</p></div></section><section id="papers"><div class="section-top"><h2>Inside the research</h2><span>7 public papers · 2024–2026</span></div><article class="featured"><div><div class="eyebrow">Featured · SURF · NeurIPS 2026</div><h3>Even preferences.<br>Uneven trade-offs.</h3><p>Choosing weights uniformly can crowd solutions into one part of the Pareto front. SURF uses the front’s geometry to spread them out.</p><a href="papers/surf/">Explore SURF</a></div><div>{chart(True)}<p class="note" style="color:#c4ccdc">Conceptual illustration. Explore the interactive example on the project page.</p></div></article><div class="paper-grid">{cards}</div></section><section id="about" class="about"><div><div class="eyebrow">Behind the work</div><h2>Liuyuan Jiang</h2></div><div><p>I am a PhD student in Electrical and Computer Engineering at the University of Rochester, advised by Prof. Lisha Chen. Previously, I was a PhD student at Rensselaer Polytechnic Institute, advised by Prof. Tianyi Chen.</p><p>My work connects optimization theory with applications in language models, speech learning, and decision-making. These pages explain the questions, methods, and evidence behind each paper.</p><div class="intro-links"><a href="mailto:ljiang24@ur.rochester.edu">Email</a><a href="https://liuyuan999.github.io/">Academic profile</a></div></div></section></main>'+footer()
save('index.html',home())
if (ROOT/'content/articles.json').exists():
    exec((ROOT/'render_articles.py').read_text())
print('Generated research hub and available articles.')
