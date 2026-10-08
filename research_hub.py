CURATION=json.loads((ROOT/'content/hub-curation.json').read_text())
FIGURES=json.loads((ROOT/'content/paper-figures.json').read_text())
AREAS=[
 {'id':'bilevel','title':'Bilevel Optimization','type':'Nested decisions','description':'How can we learn efficiently when one optimization problem sits inside another?','papers':['efficient-penalty','pbgd-free','smoothness','blocc']},
 {'id':'moo','title':'Multi-Objective Optimization','type':'Competing objectives','description':'How can we represent the full range of trade-offs between competing objectives?','papers':['surf']},
 {'id':'applications','title':'Applications','type':'Learning & behavior','description':'Better speech-learning targets, and a closer look at how LLM agents make decisions.','papers':['retailagent','birq']}
]
AREA_BY_SLUG={slug:area for area in AREAS for slug in area['papers']}
def chronological_papers():
 return sorted(PAPERS,key=lambda p:(p['year'],CURATION['release_months'][p['slug']]),reverse=True)
def atlas_diagram(area):
 # Functional scientific diagrams, not decorative illustrations.
 common='<defs><marker id="tip-'+area+'" markerWidth="7" markerHeight="7" refX="6" refY="3.5" orient="auto"><path d="M0 0 L7 3.5 L0 7" fill="currentColor"/></marker></defs>'
 if area=='bilevel':
  inside='<rect x="22" y="18" width="107" height="42" rx="5"/><rect x="196" y="18" width="107" height="42" rx="5"/><text x="76" y="44" text-anchor="middle">Leader x</text><text x="250" y="44" text-anchor="middle">Follower y*</text><path d="M136 39 H188" marker-end="url(#tip-bilevel)"/><path d="M250 69 V85 H76 V69" marker-end="url(#tip-bilevel)"/><text x="163" y="107" text-anchor="middle" class="diagram-note">Learn through the lower-level response</text>'
 elif area=='moo':
  pts=' '.join(f'{48+222*z*z:.2f},{82-66*(1-z)**4:.2f}' for z in [i/100 for i in range(101)])
  inside='<path class="diagram-axis" d="M41 12 V89 H288"/><polyline points="'+pts+'"/>'
  # Equal arc length on an explicit toy front.
  zs=[i/1000 for i in range(1001)];arc=[0.]
  for i,z in enumerate(zs[1:],1):arc.append(arc[-1]+math.hypot(z*z-zs[i-1]**2,(1-z)**4-(1-zs[i-1])**4))
  import bisect
  for j in range(7):
   k=min(1000,bisect.bisect_left(arc,j*arc[-1]/6));z=zs[k]
   inside+=f'<circle cx="{48+222*z*z:.2f}" cy="{82-66*(1-z)**4:.2f}" r="4"/>'
  inside+='<text x="163" y="110" text-anchor="middle" class="diagram-note">Cover the trade-off curve</text>'
 else:
  inside='<rect x="12" y="24" width="83" height="43" rx="5"/><rect x="119" y="24" width="85" height="43" rx="5"/><rect x="228" y="24" width="86" height="43" rx="5"/><text x="54" y="50" text-anchor="middle">Data</text><text x="162" y="50" text-anchor="middle">Model</text><text x="271" y="50" text-anchor="middle">Evaluate</text><path d="M99 46 H113" marker-end="url(#tip-applications)"/><path d="M208 46 H222" marker-end="url(#tip-applications)"/><text x="163" y="107" text-anchor="middle" class="diagram-note">Speech representations & agent behavior</text>'
 return '<svg class="atlas-diagram" viewBox="0 0 326 120" aria-hidden="true">'+common+inside+'</svg>'
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
def home():
 by={p['slug']:p for p in PAPERS};ordered=chronological_papers();rank={p['slug']:i for i,p in enumerate(ordered,1)};map_nodes=''
 for i,area in enumerate(AREAS,1):
  count=len(area['papers']);paper_links=''
  for slug in sorted(area['papers'],key=lambda s:rank[s]):
   p=by[slug]
   paper_links+='<a class="topic-paper" href="#paper-'+slug+'" aria-label="Jump to '+e(p['title'])+'"><span>'+e(CURATION['paper_labels'][slug])+'</span><small>'+str(p['year'])+'</small></a>'
  map_nodes+=f'<article id="{area["id"]}" class="research-node {area["id"]}"><div class="atlas-header"><div class="map-meta"><span>{i:02} / {e(area["type"])}</span><span>{count} paper{"s" if count!=1 else ""}</span></div>{atlas_diagram(area["id"])}</div><div class="atlas-body"><h2>{e(area["title"])}</h2><p>{e(area["description"])}</p><nav class="topic-papers" aria-label="{e(area["title"])} papers">{paper_links}</nav></div></article>'
 rows=''.join(publication_row(p,i) for i,p in enumerate(ordered,1))
 return head('Liuyuan Jiang | Research','Bilevel optimization, multi-objective optimization, and applications in speech learning and LLM agents.')+f'<main id="main" class="wrap"><header class="research-intro"><div><div class="eyebrow">Liuyuan Jiang · University of Rochester</div><h1>Research,<br><em>explained.</em></h1></div><div><p>I study optimization theory and algorithms for learning with nested decisions and competing objectives, alongside applications in speech models and LLM agents.</p><a href="https://liuyuan999.github.io/">Academic homepage</a></div></header><section class="research-overview" aria-label="Research topic map"><div class="atlas-intro"><span>Three connected research directions</span><span>Select a paper to jump to its publication</span></div><div class="research-map">{map_nodes}</div></section><section id="papers" class="publication-collection"><div class="section-top"><h2>Publications &amp; projects</h2><span>Newest first · publication year</span></div><div class="publication-list">{rows}</div></section><section id="about" class="about"><div><div class="eyebrow">Behind the work</div><h2>Liuyuan Jiang</h2></div><div><p>I am a PhD student in Electrical and Computer Engineering at the University of Rochester, advised by Prof. Lisha Chen. Previously, I was a PhD student at Rensselaer Polytechnic Institute, advised by Prof. Tianyi Chen.</p><p>Each project page combines an accessible explanation with the method, results, and technical scope. Video narration and storyboards have their own pages.</p><div class="intro-links"><a href="mailto:ljiang24@ur.rochester.edu">Email</a><a href="https://liuyuan999.github.io/">Academic profile</a></div></div></section></main>'+footer()
