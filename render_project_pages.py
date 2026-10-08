G=json.loads((ROOT/'content/project-guides.json').read_text())
def guide_source(g,anchor):
 return g['source']+('#page='+anchor if g['source'].endswith('.pdf') else '#'+anchor)
def figure_reading(g):
 return '<div class="figure-reading" aria-label="How to read the figure">'+''.join('<div><span class="reading-index">'+str(i)+'</span><div><h3>'+e(title)+'</h3><p>'+e(body)+'</p></div></div>' for i,(title,body) in enumerate(g['figure_read'],1))+'</div>'
def evidence_panels(p,g):
 buttons=''.join(f'<button type="button" id="evidence-tab-{i}" role="tab" aria-selected="{str(i==0).lower()}" aria-controls="evidence-panel-{i}" tabindex="{0 if i==0 else -1}" data-evidence-tab="{i}">{e(x["label"])}</button>' for i,x in enumerate(g['panels']))
 panels=''
 for i,x in enumerate(g['panels']):
  rows=''
  for row in x['rows']:
   featured=row[0] in ['SURF','BiRQ','PBGD-Free','BLOCC','ALT-PBGD']
   rows+='<tr'+(' class="featured-result"' if featured else '')+'><th scope="row">'+e(row[0])+'</th>'+''.join('<td>'+e(cell)+'</td>' for cell in row[1:])+'</tr>'
  table='<div class="table-scroll" role="region" tabindex="0" aria-label="'+e(x['title'])+' results"><table class="research-table"><caption>'+e(x['caption'])+'</caption><thead><tr>'+''.join('<th scope="col">'+e(col)+'</th>' for col in x['columns'])+'</tr></thead><tbody>'+rows+'</tbody></table></div><p class="table-hint" hidden>Scroll horizontally to see all columns.</p>'
  panels+=f'<div id="evidence-panel-{i}" class="evidence-panel" data-evidence-panel="{i}"><h3>{e(x["title"])}</h3>{table}<div class="result-reading"><span>What to notice</span><p>{e(x["reading"])}</p></div><details class="protocol"><summary>Experiment setup and comparison details</summary><p>{e(x["protocol"])}</p></details><a class="source-anchor" href="{e(guide_source(g,x["source"]))}">Read the original {"analysis" if p["slug"]=="smoothness" or x["label"]=="Algorithm map" else "result"} <span aria-hidden="true">↗</span></a></div>'
 return '<div class="evidence-lab" data-evidence-lab><div class="evidence-tabs" role="tablist" aria-label="Select a reported comparison" hidden>'+buttons+'</div>'+panels+'</div>'
def research_cards(g):
 return '<div class="research-cards">'+''.join('<div class="research-card"><span class="eyebrow">'+e(label)+'</span><h3>'+e(title)+'</h3><p>'+e(body)+'</p><a href="'+e(guide_source(g,source))+'">Read the statement <span aria-hidden="true">↗</span></a></div>' for label,title,body,source in g['cards'])+'</div>'
def project_page(p,a,t):
 s=p['slug'];g=G[s]
 labels=[('takeaway','At a glance'),('idea','The idea'),('interactive','Try it'),('evidence','Evidence'),('technical','Technical details'),('citation','Citation')]
 toc='<aside class="toc" aria-label="Page contents"><div class="eyebrow">On this page</div>'+''.join(f'<a href="#{i}"><span>{j+1:02}</span>{label}</a>' for j,(i,label) in enumerate(labels))+'</aside>'
 actions=f'<a class="button primary" href="{e(p["paper"])}">Read the paper <span aria-hidden="true">↗</span></a>'
 if p.get('code'):actions+=f'<a class="button" href="{e(p["code"])}">Code <span aria-hidden="true">↗</span></a>'
 actions+=f'<a class="button" href="../../videos/{s}/">Video &amp; storyboard</a><a class="text-action" href="#citation">Cite</a>'
 venue=p['venue'] if p['venue']!='Preprint' else 'Preprint · '+str(p['year'])
 hero=f'<header class="project-hero refined-hero"><a class="route-back" href="../../index.html#papers"><span aria-hidden="true">←</span> Publications &amp; projects</a><div class="paper-identity"><p class="meta"><span class="venue">{e(venue)}</span><span>{e(p["topic"])}</span></p><h1>{e(p["title"])}</h1><p class="authors">{authorshtml(p)}</p><div class="actions">{actions}</div></div></header>'
 findings='<div class="finding-links">'+''.join('<a href="#'+anchor+'"><span>'+e(label)+'</span><strong>'+e(value)+'</strong><p>'+e(text)+'</p><span class="finding-arrow" aria-hidden="true">↘</span></a>' for label,value,text,anchor in g['findings'])+'</div>'
 takeaway='<section id="takeaway" class="project-takeaway"><div class="eyebrow">'+e(p['short'])+' / The takeaway</div><h2>'+e(t['headline'])+'</h2><p class="lede">'+e(a['takeaway'])+'</p>'+findings+'</section>'
 story=''.join('<div class="story-block"><h3>'+e(title)+'</h3><p>'+e(body)+'</p></div>' for title,body in g['story'])
 method='<ol class="method-path">'+''.join(f'<li class="method-step"><div class="step-number">{i:02}</div><h3>{e(title)}</h3><p>{e(body)}</p></li>' for i,(title,body) in enumerate(t['steps'],1))+'</ol>'
 fig='' if s=='smoothness' else original_paper_figure(p,g['figure'])+figure_reading(g)
 idea=f'<section id="idea">{kicker(1,"The idea")}<h2>{e(g["scene"])}</h2>{story}{fig}<h3 class="method-heading">How the method works</h3>{method}<div class="reading-note"><strong>{e(t["why_title"])}</strong><p>{e(t["why"])}</p></div></section>'
 companion=original_paper_figure(p,0) if s=='surf' else ''
 interactive=f'<section id="interactive">{kicker(2,"Explore")}<h2>Make the idea tangible.</h2>{companion}{demo(p)}<div class="application-note"><span class="eyebrow">In practice</span><h3>{e(g["application"][0])}</h3><p>{e(g["application"][1])}</p></div></section>'
 evidence_figure=original_paper_figure(p,0)+figure_reading(g) if s=='smoothness' else ''
 evidence=f'<section id="evidence">{kicker(3,"Evidence")}<h2>{e(t["result_title"])}</h2><p class="evidence-intro">Choose a comparison to inspect the reported values, then open its setup for the evaluation details.</p>{evidence_figure}{evidence_panels(p,g)}<div class="scope-box"><h3>{e(g["result_note_title"])}</h3><p>{e(a["boundary"])}</p></div></section>'
 extra={'surf':('surf-refine','Damped empirical CDF refinement'),'retailagent':('retail-decompose','Equation 2 · Return decomposition'),'birq':('birq-update','Algorithm 1 · Weighted-gradient update'),'smoothness':('smoothness-cancel','The cancellation analyzed by directional derivatives'),'blocc':('blocc-value-gradient','Lemma 2 · Value gradient with boundary movement'),'pbgd-free':('pbgd-floor','Theorem 3 · Penalty-stationarity bound')}.get(s)
 core=paper_math(s)+'<p class="formula-reading">'+e(a['formula_note'])+'</p>'
 if extra:core+=extra_math(extra[0],extra[1])
 notation='<dl class="notation">'+''.join('<dt>'+e(symbol)+'</dt><dd>'+e(desc)+'</dd>' for symbol,desc in t['notation'])+'</dl>'
 deeper='<details class="technical-detail"><summary>Notation and the reasoning behind the formulation</summary>'+notation+''.join('<div class="story-block"><h3>'+e(title)+'</h3><p>'+e(body)+'</p></div>' for title,body in t['reasoning'])+'</details>'
 if t.get('update_equations'):deeper+='<details class="technical-detail"><summary>Inspect the single-loop update</summary><div class="equation-set update-set">'+extra_math('update-lower','Equation 8 · Lower tracking update')+extra_math('update-upper','Equation 8 · Outer update')+'</div><p>'+e(t['update_caption'])+'</p></details>'
 deeper+='<details class="technical-detail"><summary>Assumptions behind the analysis</summary><p>'+e(a['formal'])+'</p><a href="'+e(p['paper'])+'">'+e(t['anchor'])+' in the paper</a></details>'
 faq='<div class="reader-questions"><h3>Questions worth asking</h3>'+''.join('<details><summary>'+e(question)+'</summary><p>'+e(answer)+'</p></details>' for question,answer in g['faq'])+'</div>'
 technical=f'<section id="technical">{kicker(4,"A closer look")}<h2>From the intuition to the formulation.</h2>{core}{research_cards(g)}{deeper}{faq}<div class="connection"><h3>Continue the research thread</h3><p>{e(t["connection"])}</p>{relatedhtml(p,a)}</div></section>'
 venue_note='<p class="note">'+e(p['venue_note'])+'</p>' if p.get('venue_note') else ''
 citation=f'<section id="citation">{kicker(5,"Reference")}<h2>Cite this work</h2><button class="button" type="button" data-copy="bibtex">Copy BibTeX</button><p class="status" role="status"></p><pre id="bibtex">{e(bib(p))}</pre>{venue_note}<h3>Research sources</h3>{sourcehtml(p)}</section>'
 return head(p['short']+' | Liuyuan Jiang',t['deck'],2,'papers/'+s+'/')+'<main id="main" class="wrap refined-project">'+hero+'<div class="project-layout">'+toc+'<article class="article">'+takeaway+idea+interactive+evidence+technical+citation+'</article></div></main>'+footer(2)
