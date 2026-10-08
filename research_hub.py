AREAS=[
 {'id':'bilevel','title':'Bilevel Optimization','type':'Core theory','description':'Algorithms for nested learning, lower-level responses, and coupled constraints.','papers':['efficient-penalty','pbgd-free','smoothness','blocc'],'equation':'bilevel-map'},
 {'id':'moo','title':'Multi-Objective Optimization','type':'Core theory','description':'The geometry of competing objectives and how to represent their trade-offs.','papers':['surf'],'equation':'moo-map'},
 {'id':'applications','title':'Applications','type':'Learning & decision-making','description':'Self-supervised speech learning and behavioral audits of LLM agents.','papers':['retailagent','birq']}
]
def publication_preview(p):
 s=p['slug'];blue='#354ac6';green='#007c70';gray='#9aa7bd';inside='';caption='Conceptual illustration'
 if s=='surf':
  # Geometry is exact; spacing shown here is a preview of the interactive toy.
  pts=' '.join(f'{30+220*z*z:.2f},{130-100*(1-z)**4:.2f}' for z in [i/100 for i in range(101)])
  inside=f'<path d="M30 20 V130 H255" fill="none" stroke="{gray}"/><polyline points="{pts}" fill="none" stroke="{blue}" stroke-width="2.5"/>'
  for z in [.02,.08,.19,.35,.56,.79,1]:inside+=f'<circle cx="{30+220*z*z:.2f}" cy="{130-100*(1-z)**4:.2f}" r="4" fill="{green}"/>'
  inside+='<text x="140" y="159" text-anchor="middle">Pareto-front geometry</text>';caption='Illustrative geometry'
 elif s=='pbgd-free':
  inside=f'<path d="M30 20 V135 H255" fill="none" stroke="{gray}"/>'
  for f,col in [(lambda d:d,blue),(lambda d:d**1.5+.003,green)]:
   pts=' '.join(f'{30+220*d:.2f},{135-105*f(d):.2f}' for d in [i/100 for i in range(101)])
   inside+=f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2.5"/>'
  inside+='<text x="142" y="160" text-anchor="middle">Upper-level flatness</text>';caption='Illustrative bound envelope'
 elif s=='smoothness':
  inside=f'<path d="M30 20 V135 H255" fill="none" stroke="{gray}"/>'
  for a,col in [(5.5,blue),(.5,green)]:
   pts=' '.join(f'{30+220*i/100:.2f},{135-100*a*(-1+2*i/100)**2/5.5:.2f}' for i in range(101))
   inside+=f'<polyline points="{pts}" fill="none" stroke="{col}" stroke-width="2.5"/>'
  inside+='<text x="140" y="160" text-anchor="middle">Joint vs. reduced</text>';caption='Exact quadratic toy'
 elif s=='efficient-penalty':
  inside=f'<rect x="22" y="30" width="110" height="82" rx="4" fill="white" stroke="{gray}"/><rect x="148" y="30" width="110" height="82" rx="4" fill="white" stroke="{green}"/><text x="77" y="58" text-anchor="middle">Joint</text><text x="77" y="90" text-anchor="middle" class="math-word">O(γ)</text><text x="203" y="58" text-anchor="middle">Reduced</text><text x="203" y="90" text-anchor="middle" class="math-word">O(1)</text><text x="140" y="151" text-anchor="middle">Curvature &amp; updates</text>';caption='Conditional smoothness analysis'
 elif s=='blocc':
  pts=' '.join(f'{30+73*y:.2f},{135-25*(y-2)**2:.2f}' for y in [i*3/100 for i in range(101)])
  inside=f'<rect x="30" y="20" width="73" height="115" fill="#dff1ed"/><path d="M30 20 V135 H255" stroke="{gray}" fill="none"/><path d="M103 20 V135" stroke="{green}" stroke-dasharray="4 4"/><polyline points="{pts}" fill="none" stroke="{blue}" stroke-width="2.5"/><circle cx="103" cy="110" r="5" fill="{green}"/><text x="140" y="160" text-anchor="middle">A moving feasible set</text>';caption='Exact constrained toy'
 else:
  rows=[('BEST-RQ',19.6,'19.6%',blue),('BiRQ',12.6,'12.6%',green)] if s=='birq' else [('Intact',45.7,'−45.7',blue),('Global',3.5,'−3.5',gray),('Same-day',8.7,'−8.7',green)]
  maxval=22 if s=='birq' else 50
  for i,(name,val,number,color) in enumerate(rows):
   y=38+i*36;inside+=f'<text x="15" y="{y+15}">{name}</text><rect x="99" y="{y}" width="{116*val/maxval:.2f}" height="20" fill="{color}"/><text x="222" y="{y+15}">{number}</text>'
  inside+='<text x="140" y="160" text-anchor="middle">'+('test-other WER' if s=='birq' else 'Timing alpha / bps')+'</text>'
  caption='Table 2 · LibriSpeech' if s=='birq' else 'Table 1 · Text condition'
 svg=f'<svg viewBox="0 0 280 180" role="img" aria-label="{e(caption)} for {e(p["short"])}">{inside}</svg>'
 return '<a class="pub-preview" href="papers/'+s+'/" aria-label="'+e(p['short'])+' project page">'+svg+'<span>'+e(caption)+'</span></a>'
def home():
 by={p['slug']:p for p in PAPERS};map_nodes='';groups=''
 for area in AREAS:
  count=len(area['papers']);signature=extra_math(area['equation']) if area.get('equation') else '<div class="application-links"><a href="papers/birq/">BiRQ · Speech</a><a href="papers/retailagent/">RetailAgent · LLM agents</a></div>'
  map_nodes+=f'<article class="research-node {area["id"]}"><div class="map-meta"><span>{e(area["type"])}</span><span>{count} paper{"s" if count!=1 else ""}</span></div><h2><a href="#{area["id"]}">{e(area["title"])}</a></h2><p>{e(area["description"])}</p>{signature}</article>'
  rows=''
  for slug in area['papers']:
   p=by[slug];authors=', '.join('<strong>'+e(n)+'</strong>' if n=='Liuyuan Jiang' else e(n) for n in p['authors'])
   links=f'<a href="{p["paper"]}">Paper</a>'
   if p.get('code'):links+=f'<a href="{p["code"]}">Code</a>'
   links+=f'<a href="papers/{slug}/">Project page</a><a href="videos/{slug}/">Video storyboard</a>'
   venue=e(p['venue']) if p['venue']!='Preprint' else 'arXiv preprint'
   note='<p class="pub-note">'+e(p['venue_note'])+'</p>' if p.get('venue_note') else ''
   rows+=f'<article class="publication-row">{publication_preview(p)}<div class="pub-record"><h3><a href="papers/{slug}/">{e(p["title"])}</a></h3><p class="pub-authors">{authors}</p><p class="pub-venue">{venue}{" · "+str(p["year"]) if str(p["year"]) not in p["venue"] else ""}</p>{note}<p class="pub-summary">{e(p["description"])}</p><div class="pub-links">{links}</div></div></article>'
  groups+=f'<section id="{area["id"]}" class="publication-group"><div class="group-heading"><h2>{e(area["title"])}</h2><span>{count} paper{"s" if count!=1 else ""}</span></div>{rows}</section>'
 return head('Liuyuan Jiang | Research','Bilevel optimization, multi-objective optimization, and applications in speech learning and LLM agents.')+f'<main id="main" class="wrap"><header class="research-intro"><div><div class="eyebrow">Liuyuan Jiang · University of Rochester</div><h1>Research,<br><em>explained.</em></h1></div><div><p>I study optimization theory and algorithms for learning with nested decisions and competing objectives, alongside applications in speech models and LLM agents.</p><a href="https://liuyuan999.github.io/">Academic homepage</a></div></header><section class="research-overview" aria-label="Research topic map"><div class="research-map">{map_nodes}</div></section><section id="papers" class="publication-collection"><div class="section-top"><h2>Publications &amp; projects</h2><span>7 public papers · 2024–2026</span></div>{groups}</section><section id="about" class="about"><div><div class="eyebrow">Behind the work</div><h2>Liuyuan Jiang</h2></div><div><p>I am a PhD student in Electrical and Computer Engineering at the University of Rochester, advised by Prof. Lisha Chen. Previously, I was a PhD student at Rensselaer Polytechnic Institute, advised by Prof. Tianyi Chen.</p><p>Each project page combines an accessible explanation with the method, results, and technical scope. Video narration and storyboards have their own pages.</p><div class="intro-links"><a href="mailto:ljiang24@ur.rochester.edu">Email</a><a href="https://liuyuan999.github.io/">Academic profile</a></div></div></section></main>'+footer()
