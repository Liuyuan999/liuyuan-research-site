CURATION=json.loads((ROOT/'content/hub-curation.json').read_text())
FIGURES=json.loads((ROOT/'content/paper-figures.json').read_text())
AREAS=[
 {'id':'moo','title':'Multi-objective Learning','type':'Competing objectives','question':'How do we cover the space of trade-offs?','description':'A preference weight is a dial, but turning it evenly can leave gaps in the solutions. Geometry tells us how to explore the Pareto front.','papers':['surf']},
 {'id':'bilevel','title':'Bilevel Optimization','type':'Nested decisions','question':'What changes when learning has an inner problem?','description':'An outer decision changes an inner solution. My work studies the curvature, update rules, and constraints that make this learning process efficient.','papers':['efficient-penalty','pbgd-free','smoothness','blocc']},
 {'id':'applications','title':'Applications','type':'Learning & behavior','question':'What do these ideas reveal in real models?','description':'Build better learning targets for speech, and examine the structure behind an LLM agent’s sequential decisions.','papers':['retailagent','birq']}
]
AREA_BY_SLUG={slug:area for area in AREAS for slug in area['papers']}
def chronological_papers():
 priorities=CURATION.get('display_priority',[])
 return sorted(PAPERS,key=lambda p:(p['slug'] in priorities,p['year'],CURATION['release_months'][p['slug']]),reverse=True)
def opening_visual(area):
 if area=='moo':
  # Same exact illustrative objectives as the project demo: z² and (1-z)^4.
  def solve(w):
   if w==0:return 1.
   if w==1:return 0.
   lo,hi=0.,1.
   for _ in range(50):
    z=(lo+hi)/2
    if 2*w*z-4*(1-w)*(1-z)**3>0:hi=z
    else:lo=z
   return (lo+hi)/2
  xy=lambda z:(90+280*z*z,305-280*(1-z)**4)
  points=' '.join(f'{x:.2f},{y:.2f}' for x,y in [xy(i/200) for i in range(201)])
  dots=''.join(f'<circle data-front-point="{i}" cx="{xy(solve(1-i/8))[0]:.2f}" cy="{xy(solve(1-i/8))[1]:.2f}" r="5.5"/>' for i in range(9))
  svg=f'<svg class="opening-plot" viewBox="0 0 460 360" role="img" aria-label="Illustrative Pareto front for z squared and one minus z to the fourth power"><path class="plot-grid" d="M90 25 H370 M90 95 H370 M90 165 H370 M90 235 H370"/><path class="plot-axis" d="M90 17 V305 H388"/><polyline class="front-curve" points="{points}"/>{dots}<text x="230" y="339" text-anchor="middle">Objective 1</text><text x="43" y="165" text-anchor="middle" transform="rotate(-90 43 165)">Objective 2</text></svg>'
  return '<div class="opening-lab" data-opening="pareto"><div class="lab-eyebrow">Explore the idea</div><h3>Same front. Different coverage.</h3><div class="lab-controls" aria-label="Pareto-front sampling"><button type="button" data-spacing="weights" aria-pressed="true">Equal weights</button><button type="button" data-spacing="arc" aria-pressed="false">Equal distances</button></div>'+svg+'<p class="lab-result" data-spacing-result aria-live="polite">Even weight increments produce uneven gaps.</p><p class="lab-note">An exact toy example of the spacing problem behind SURF. Both objectives are minimized.</p></div>'
 if area=='bilevel':
  return '<div class="opening-lab" data-opening="bilevel"><div class="lab-eyebrow">Explore the idea</div><h3>A moving constraint changes the response.</h3><div class="lab-range"><label for="opening-leader">Leader’s decision x</label><input id="opening-leader" type="range" min="0" max="3" step="0.1" value="1"><output for="opening-leader" data-leader-value>1.0</output></div><svg class="opening-plot" viewBox="0 0 460 290" role="img" aria-label="Exact constrained quadratic example showing the follower response and a moving feasibility boundary"><g data-response-plot></g></svg><div class="lab-legend"><span>Unconstrained response</span><span>Feasible response</span></div><p class="lab-result" data-response-result aria-live="polite"></p><p class="lab-note">Exact toy: minimize (y − 2x)² subject to 0 ≤ y ≤ x. This illustrates a coupled constraint.</p></div>'
 return '<div class="opening-lab" data-opening="applications"><div class="lab-eyebrow">Inside the applications</div><div class="lab-controls" aria-label="Application preview"><button type="button" data-application="speech" aria-pressed="true">Speech targets</button><button type="button" data-application="agents" aria-pressed="false">Agent decisions</button></div><div class="application-view" data-application-view="speech"><h3>Learn from the model’s own features.</h3><img class="speech-original" src="assets/paper-figures/birq-figure1.png" width="1938" height="2057" alt="Original BiRQ Figure 1: enhanced targets from intermediate features and anchoring targets from raw input." loading="lazy"><p class="lab-result">Enhanced labels evolve with the encoder; input-based anchors stabilize training.</p><p class="lab-note">Original BiRQ Figure 1. <a href="https://arxiv.org/html/2509.15430v1#S1.F1">Paper source</a></p></div><div class="application-view" data-application-view="agents" hidden><h3>Observe. Decide. Carry state forward.</h3><img class="agents-original" src="assets/paper-figures/retailagent-figure2.png" width="1452" height="708" alt="Original RetailAgent Figure 2 showing observations, self-authored memory, and a frozen LLM’s long-or-flat decisions." loading="lazy"><p class="lab-result">The agent commits to long or flat before the next return is revealed.</p><p class="lab-note">Original RetailAgent Figure 2. <a href="https://arxiv.org/pdf/2608.28399v1#page=3">Paper source</a></p></div></div>'
def original_paper_figure(p,index=0):
 fs=FIGURES.get(p['slug'],[])
 if index>=len(fs):return ''
 f=fs[index];src='../../assets/paper-figures/'+f['file']
 portrait=' portrait' if f.get('portrait') else ''
 return '<figure class="paper-figure'+portrait+'"><div class="figure-heading"><span>From the paper</span><a href="'+e(src)+'" target="_blank" rel="noopener">View full size</a></div><a class="figure-image" href="'+e(src)+'" target="_blank" rel="noopener" aria-label="View full-size '+e(f['label'])+'"><img src="'+e(src)+'" width="'+str(f['width'])+'" height="'+str(f['height'])+'" loading="lazy" decoding="async" alt="'+e(f['alt'])+'"></a><figcaption><strong>'+e(f['label'])+'</strong><p>'+e(f['caption'])+'</p><a href="'+e(f['source'])+'">Original paper source</a></figcaption></figure>'
def publication_preview(p):
 s=p['slug'];original=next((f for f in FIGURES.get(s,[]) if f.get('preview')),None)
 if original:
  portrait=' portrait' if original.get('portrait') else ''
  return '<a class="pub-preview original-preview'+portrait+'" href="papers/'+s+'/#idea" aria-label="'+e(p['short'])+' project page"><div class="preview-image"><img src="assets/paper-figures/'+original['file']+'" width="'+str(original['width'])+'" height="'+str(original['height'])+'" alt="'+e(original['alt'])+'" loading="lazy" decoding="async"></div><span>Original paper · '+e(original['label'].split(' · ')[0])+'</span></a>'
 blue='#354ac6';green='#007c70';gray='#9aa7bd'
 if s=='retailagent':
  # Reported signed estimates and date-bootstrap 95% intervals, Table 1.
  rows=[('Intact',-45.7,-49.4,-41.8,blue),('Global shuffle',-3.5,-5.4,-1.7,gray),('Same-day',-8.7,-10.4,-7.1,green)]
  axis=lambda val:332+3.6*val
  inside='<text x="24" y="30" class="plot-title">Timing alpha</text><text x="24" y="51" class="plot-note">bps per stock-day · 95% CI</text><path d="M332 69 V177" stroke="'+gray+'"/>'
  for i,(label,value,lo,hi,color) in enumerate(rows):
   y=87+36*i;x=axis(value)
   inside+=f'<text x="24" y="{y+5}">{label}</text><rect x="{x:.2f}" y="{y-10}" width="{332-x:.2f}" height="20" rx="2" fill="{color}" opacity=".22"/><path d="M{axis(lo):.2f} {y} H{axis(hi):.2f} M{axis(lo):.2f} {y-5} V{y+5} M{axis(hi):.2f} {y-5} V{y+5}" stroke="{color}" stroke-width="2"/><circle cx="{x:.2f}" cy="{y}" r="4" fill="{color}"/><text x="354" y="{y+5}" text-anchor="end">{value:g}</text>'
  inside+='<text x="152" y="199">−50</text><text x="323" y="199">0</text>'
  # Keep values in a separate right column, so the zero reference remains visible.
  inside=inside.replace('x="354"','x="396"')
  caption='Reported results · Table 1';label='RetailAgent Table 1: intact schedule has −45.7 bps timing alpha, global shuffle −3.5, and same-day shuffle −8.7, with reported 95 percent confidence intervals.'
 else:
  inside='<text x="24" y="30" class="plot-title">Which objective is curved?</text><text x="24" y="51" class="plot-note">Exact quadratic example · γ = 5</text><path d="M48 75 V172 H372" fill="none" stroke="'+gray+'"/>'
  for a,col in [(5.5,blue),(.5,green)]:
   pts=' '.join(f'{48+324*i/100:.2f},{172-88*a*(-1+2*i/100)**2/5.5:.2f}' for i in range(101))
   inside+=f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="3"/>'
  inside+='<circle cx="45" cy="203" r="4" fill="'+blue+'"/><text x="56" y="208">Fixed y = 0</text><circle cx="232" cy="203" r="4" fill="'+green+'"/><text x="243" y="208">Minimize over y</text>'
  caption='Explanatory toy · joint vs. reduced';label='Exact quadratic toy: fixing y creates penalty-dependent curvature, while minimizing over y leaves x squared over two. This is an explanation, not paper experiment data.'
 svg='<svg viewBox="0 0 420 230" role="img" aria-label="'+e(label)+'">'+inside+'</svg>'
 return '<a class="pub-preview" href="papers/'+s+'/" aria-label="'+e(p['short'])+' project page">'+svg+'<span>'+e(caption)+'</span></a>'
def publication_row(p,number):
 slug=p['slug'];area=AREA_BY_SLUG[slug]
 authors=', '.join('<strong>'+e(n)+'</strong>' if n=='Liuyuan Jiang' else e(n) for n in p['authors'])
 links=f'<a href="{p["paper"]}">Paper</a>'
 if p.get('code'):links+=f'<a href="{p["code"]}">Code</a>'
 links+=f'<a href="papers/{slug}/">Project page</a><a href="videos/{slug}/">Video storyboard</a>'
 venue=e(p['venue']) if p['venue']!='Preprint' else 'arXiv preprint'
 note='<p class="pub-note">'+e(p['venue_note'])+'</p>' if p.get('venue_note') else ''
 return f'<article id="paper-{slug}" class="publication-row {area["id"]}" aria-labelledby="title-{slug}">{publication_preview(p)}<div class="pub-record"><div class="pub-overline"><span>{number:02} / {p["year"]}</span><span class="topic-label">{e(area["title"])}</span></div><h3 id="title-{slug}"><a href="papers/{slug}/">{e(p["title"])}</a></h3><p class="pub-authors">{authors}</p><p class="pub-venue">{venue}{" · "+str(p["year"]) if str(p["year"]) not in p["venue"] else ""}</p>{note}<p class="pub-summary">{e(p["description"])}</p><div class="pub-links">{links}</div></div></article>'
def direction_paper(p):
 c=CURATION['direction_papers'][p['slug']]
 venue=p['venue'] if p['venue']!='Preprint' else 'Preprint · '+str(p['year'])
 return '<a class="direction-paper" href="#paper-'+p['slug']+'"><span class="direction-paper-title">'+e(c['headline'])+'</span><span class="direction-paper-idea">'+e(c['idea'])+'</span><span class="direction-paper-meta">'+e(venue)+'<span>View publication below</span></span></a>'
def home():
 by={p['slug']:p for p in PAPERS};ordered=chronological_papers();rank={p['slug']:i for i,p in enumerate(ordered,1)};tabs='';panels=''
 for i,area in enumerate(AREAS):
  count=len(area['papers']);active=i==0
  tabs+=f'<button type="button" id="direction-tab-{area["id"]}" role="tab" aria-controls="{area["id"]}" aria-selected="{str(active).lower()}" tabindex="{0 if active else -1}" data-direction="{area["id"]}"><span>{e(area["title"])}</span><small>{e(area["type"])}</small></button>'
  paper_links=''.join(direction_paper(by[slug]) for slug in sorted(area['papers'],key=lambda s:rank[s]))
  panels+=f'<section id="{area["id"]}" class="direction-panel {area["id"]}" role="tabpanel" aria-labelledby="direction-tab-{area["id"]}" tabindex="0" {"" if active else "hidden"}><div class="direction-story"><div class="eyebrow">{e(area["type"])}</div><h2>{e(area["question"])}</h2><p class="direction-intro">{e(area["description"])}</p></div>{opening_visual(area["id"])}<div class="direction-papers">{paper_links}</div></section>'
 rows=''.join(publication_row(p,i) for i,p in enumerate(ordered,1))
 return head('Liuyuan Jiang | Learning and Decisions','Optimization for multi-objective learning, nested decisions, speech representations, and LLM agents.')+f'<main id="main" class="wrap"><header class="research-intro"><div><div class="eyebrow">Liuyuan Jiang · University of Rochester</div><h1>The geometry of<br><em>learning and decisions.</em></h1></div><div><p>I study how optimization shapes learning: navigating competing objectives, solving nested problems, and understanding model behavior.</p><a href="https://liuyuan999.github.io/">Academic homepage</a></div></header><section class="research-overview" aria-label="Research directions" data-direction-explorer><div class="atlas-intro"><h2>Research directions</h2><span>Explore a direction, then follow the papers.</span></div><div class="direction-tabs" role="tablist" aria-label="Research directions">{tabs}</div>{panels}<noscript><style>.direction-panel[hidden]{{display:grid!important}}.direction-tabs{{display:none}}</style></noscript></section><section id="papers" class="publication-collection"><div class="section-top"><h2>Publications &amp; projects</h2><span>Latest work first</span></div><div class="publication-list">{rows}</div></section><section id="about" class="about"><div><div class="eyebrow">Behind the work</div><h2>Liuyuan Jiang</h2></div><div><p>I am a PhD student in Electrical and Computer Engineering at the University of Rochester, advised by Prof. Lisha Chen. Previously, I was a PhD student at Rensselaer Polytechnic Institute, advised by Prof. Tianyi Chen.</p><p>Each project page combines an accessible explanation with the method, results, and technical scope. Video narration and storyboards have their own pages.</p><div class="intro-links"><a href="mailto:ljiang24@ur.rochester.edu">Email</a><a href="https://liuyuan999.github.io/">Academic profile</a></div></div></section></main>'+footer()
