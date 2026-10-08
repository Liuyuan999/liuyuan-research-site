document.querySelectorAll("[data-copy]").forEach(b=>b.addEventListener("click",async()=>{const t=document.getElementById(b.dataset.copy).textContent;const s=b.nextElementSibling;try{await navigator.clipboard.writeText(t);s.textContent="Citation copied."}catch{ s.textContent="Select the citation below to copy it."}}));
const NS='http://www.w3.org/2000/svg';
const node=(name,attrs={},text='')=>{const n=document.createElementNS(NS,name);for(const[k,v]of Object.entries(attrs))n.setAttribute(k,v);n.textContent=text;return n;};
function draw(d,lines=[],dots=[],bars=[],xLabel='',yLabel=''){
 const g=d.querySelector('[data-plot]');g.replaceChildren();
 g.append(node('path',{d:'M65 25 V250 H590',fill:'none',stroke:'#9aabc7'}));
 for(let i=0;i<5;i++)g.append(node('path',{d:`M65 ${45+i*48} H590`,stroke:'#e2e7f0',fill:'none'}));
 for(const l of lines)g.append(node('polyline',{points:l.points.map(p=>p.join(',')).join(' '),fill:'none',stroke:l.color||'#354ac6','stroke-width':l.width||3,'stroke-dasharray':l.dash||''}));
 for(const b of bars){g.append(node('rect',{x:b.x,y:b.y,width:b.width,height:b.height,fill:b.color,rx:3}));if(b.label)g.append(node('text',{x:b.x+b.width/2,y:b.y-8,fill:'#111d34','font-size':14,'text-anchor':'middle'},b.label));}
 for(const p of dots)g.append(node('circle',{cx:p.x,cy:p.y,r:p.r||5,fill:p.color||'#354ac6',stroke:'#fff','stroke-width':1.5}));
 g.append(node('text',{x:330,y:283,fill:'#546176','font-size':15,'text-anchor':'middle'},xLabel));
 g.append(node('text',{x:35,y:145,fill:'#546176','font-size':15,transform:'rotate(-90 35 145)','text-anchor':'middle'},yLabel));
}
const cv=a=>{const m=a.reduce((s,x)=>s+x,0)/a.length;return Math.sqrt(a.reduce((s,x)=>s+(x-m)**2,0)/a.length)/m;};
for(const d of document.querySelectorAll('[data-demo]')){
 const type=d.dataset.demo,range=d.querySelector('input[type=range]');
 if(type==='surf'){
  // Solve w*z^2 +(1-w)*(1-z)^4 over [0,1] using its monotone derivative.
  const solve=w=>{if(w===0)return 1;if(w===1)return 0;let lo=0,hi=1;for(let j=0;j<55;j++){const z=(lo+hi)/2;const derivative=2*w*z-4*(1-w)*(1-z)**3;if(derivative>0)hi=z;else lo=z;}return(lo+hi)/2;};
  const M=4000,zs=Array.from({length:M+1},(_,i)=>i/M),cs=[0];
  for(let i=1;i<=M;i++){const z=zs[i],prev=zs[i-1];cs.push(cs[i-1]+Math.hypot(z*z-prev*prev,(1-z)**4-(1-prev)**4));}
  const total=cs[M],at=z=>{const idx=Math.min(M-1,Math.floor(z*M)),f=z*M-idx;return cs[idx]+f*(cs[idx+1]-cs[idx]);};
  const inverse=q=>{const target=q*total;let lo=0,hi=M;while(hi-lo>1){const mid=Math.floor((lo+hi)/2);if(cs[mid]<target)lo=mid;else hi=mid;}return (lo+(target-cs[lo])/(cs[hi]-cs[lo]))/M;};
  const xy=z=>[65+510*z*z,245-210*(1-z)**4];
  const update=()=>{const n=+range.value;d.querySelector('[data-count]').textContent=n;
   const uniform=Array.from({length:n},(_,i)=>solve(1-i/(n-1))),arc=Array.from({length:n},(_,i)=>inverse(i/(n-1)));
   const gaps=uniform.slice(1).map((z,i)=>at(z)-at(uniform[i]));
   draw(d,[{points:zs.filter((_,i)=>i%20===0).map(xy),color:'#adb7ca'}],uniform.map(z=>{const[x,y]=xy(z);return{x,y,color:'#354ac6',r:6}}).concat(arc.map(z=>{const[x,y]=xy(z);return{x,y,color:'#008274',r:4}})),[],'f₁(z) = z²','f₂(z)');
   d.querySelector('[data-metric]').textContent=`Arc-gap CV: ${cv(gaps).toFixed(2)} for equal weights; approximately 0 for equal arc length.`;};range.addEventListener('input',update);update();
 }
 if(type==='constraint'){
  const update=()=>{const x=+range.value;d.querySelector('[data-count]').textContent=x.toFixed(2);const yy=y=>245-210*(y-2*x)**2/36;
   draw(d,[{points:Array.from({length:121},(_,i)=>[65+510*i/120,yy(6*i/120)]),color:'#a2aeca'},{points:[[65+85*x,25],[65+85*x,250]],color:'#008274',dash:'6 5'}],[{x:65+85*x,y:yy(x),color:'#008274',r:7},{x:65+170*x,y:yy(2*x),color:'#354ac6',r:6}],[],'y (0 to 6)','Loss (0 to 36)');
   d.querySelector('[data-plot]').prepend(node('rect',{x:65,y:25,width:85*x,height:225,fill:'#e1f2ee'}));d.querySelector('[data-metric]').textContent=`x = ${x.toFixed(2)} · feasible y* = ${x.toFixed(2)} · unconstrained 2x = ${(2*x).toFixed(2)}${x>0?' · active-bound multiplier λ* = '+(2*x).toFixed(2):''}`;};range.addEventListener('input',update);update();
 }
 if(type==='timing'){
  const rs=[-20,15,-10,25,-15,5];let ps=[1,0,1,0,1,0];
  const update=()=>{const mean=ps.reduce((s,x)=>s+x,0)/6,score=rs.reduce((s,r,i)=>s+(ps[i]-mean)*r,0);
   d.querySelectorAll('[data-action]').forEach((b,i)=>{b.setAttribute('aria-pressed',String(!!ps[i]));b.textContent=`Interval ${i+1}: ${ps[i]?'Long':'Flat'}`;});
   draw(d,[{points:[[65,145],[590,145]],color:'#9aabc7',width:1}],[],rs.map((r,i)=>({x:94+i*80,y:r>=0?145-r*3:145,width:40,height:Math.abs(r)*3,color:ps[i]?'#354ac6':'#aab5c8',label:`${r>0?'+':''}${r}`})),'Interval 1 to 6','Return (bps)');
   d.querySelector('[data-metric]').textContent=`Exposure ${(100*mean).toFixed(0)}% · centered timing ${score.toFixed(1)} bps`;};
  d.querySelectorAll('[data-action]').forEach((b,i)=>b.addEventListener('click',()=>{ps[i]=1-ps[i];update();}));d.querySelector('[data-invert]').addEventListener('click',()=>{ps=ps.map(x=>1-x);update();});d.querySelector('[data-reset]').addEventListener('click',()=>{ps=[1,0,1,0,1,0];update();});update();
 }
 if(type==='curvature'){
  const update=()=>{const gamma=+range.value;d.querySelector('[data-count]').textContent=gamma;
   const points=f=>Array.from({length:101},(_,i)=>{const x=-1+2*i/100;return[65+510*i/100,245-215*f(x)/(gamma+.5)];});
   draw(d,[{points:points(x=>x*x/2+gamma*x*x),color:'#354ac6'},{points:points(x=>x*x/2),color:'#008274'}],[],[],'x (−1 to 1)',`Value (0 to ${(gamma+.5).toFixed(1)})`);
   d.querySelector('[data-metric]').textContent=`Fixed-slice curvature: ${1+2*gamma} · reduced curvature: 1`;};range.addEventListener('input',update);update();
 }
 if(type==='speech'){
  const update=source=>{const enhanced=source==='enhanced';d.querySelectorAll('[data-source]').forEach(b=>{b.setAttribute('aria-pressed',String(b.dataset.source===source));b.classList.toggle('primary',b.dataset.source===source);});d.querySelectorAll('[data-node]').forEach(n=>n.classList.toggle('active',['input','quant',enhanced?'repr':'anchor'].includes(n.dataset.node)));d.querySelector('[data-explanation]').textContent=enhanced?'Enhanced targets use intermediate model representations, followed by random-projection quantization. The learner’s evolving features help construct the labels used for learning.':'Anchor targets use raw-input quantization. This input-based branch complements the enhanced targets produced from the evolving model.';};
  d.querySelectorAll('[data-source]').forEach(b=>b.addEventListener('click',()=>update(b.dataset.source)));update('anchor');
 }
 if(type==='flatness'){
  const update=()=>{const v=+range.value;d.querySelector('[data-count]').textContent=v.toFixed(2);d.querySelector('[data-linear]').textContent=v.toFixed(4);d.querySelector('[data-flat]').textContent=(v**1.5+.003).toFixed(4);
   const pts=f=>Array.from({length:101},(_,i)=>[65+510*i/100,245-210*f(i/100)/1.05]);
   draw(d,[{points:pts(x=>x),color:'#354ac6'},{points:pts(x=>x**1.5+.003),color:'#008274'}],[{x:65+510*v,y:245-210*v/1.05,color:'#354ac6'},{x:65+510*v,y:245-210*(v**1.5+.003)/1.05,color:'#008274'}],[],'Distance d (0 to 1)','Bound (0 to 1.05)');
   d.querySelector('[data-metric]').textContent=`Distance term d^1.5 = ${(v**1.5).toFixed(4)} · residual δ = 0.0030`;};range.addEventListener('input',update);update();
 }
 if(type==='regime'){
  const update=mode=>{const coupled=mode==='coupled';d.querySelectorAll('[data-regime]').forEach(b=>{b.setAttribute('aria-pressed',String(b.dataset.regime===mode));b.classList.toggle('primary',b.dataset.regime===mode);});d.querySelectorAll('[data-regime-formula]').forEach(form=>form.hidden=form.dataset.regimeFormula!==mode);d.querySelector('[data-regime-title]').textContent=coupled?'Coupled constraints / inner solve retained':'Uncoupled constraints / fully single-loop';d.querySelector('[data-regime-description]').textContent=coupled?'The feasible set moves with x. Constraint multipliers enter the value-function derivative, and the coupled PBGD-Free extension retains an inner loop. Its work belongs in the total complexity.':'The feasible set is fixed as x changes. Under flatness and the stated assumptions, the analyzed PBGD-Free update removes the value-function loop and is fully single-loop.';};
  d.querySelectorAll('[data-regime]').forEach(b=>b.addEventListener('click',()=>update(b.dataset.regime)));update('fixed');
 }
 if(type==='schedule'){
  let mode='single',step=0;
  const update=()=>{const k=mode==='single'?1:4,lower=Math.floor(step/(k+1))*k+Math.min(step%(k+1),k),upper=Math.floor(step/(k+1));d.querySelector('[data-lower]').textContent=lower+' updates';d.querySelector('[data-upper]').textContent=upper+' updates';d.querySelector('[data-stage=lower]').classList.toggle('active',step>0&&step%(k+1)!==0);d.querySelector('[data-stage=upper]').classList.toggle('active',step>0&&step%(k+1)===0);d.querySelector('[data-explanation]').textContent=`Illustrated schedule: ${k} lower-level update${k===1?'':'s'} per upper-level update. ${step===0?'Press Next update to inspect the sequence.':'Completed '+step+' gradient updates in total.'}`;d.querySelectorAll('[data-mode]').forEach(b=>{b.setAttribute('aria-pressed',String(b.dataset.mode===mode));b.classList.toggle('primary',b.dataset.mode===mode);});};
  d.querySelectorAll('[data-mode]').forEach(b=>b.addEventListener('click',()=>{mode=b.dataset.mode;step=0;update();}));d.querySelector('[data-next]').addEventListener('click',()=>{step++;update();});update();
 }
}

const contents=document.querySelector('.toc');
if(contents&&'IntersectionObserver' in window){
 const links=[...contents.querySelectorAll('a[href^="#"]')];
 const observer=new IntersectionObserver(entries=>{for(const entry of entries){if(entry.isIntersecting){links.forEach(link=>{if(link.getAttribute('href')==='#'+entry.target.id)link.setAttribute('aria-current','location');else link.removeAttribute('aria-current');});}}},{rootMargin:'-5% 0px -70% 0px'});
 links.forEach(link=>{const section=document.querySelector(link.getAttribute('href'));if(section)observer.observe(section);});
}

// The home-page research explorer keeps paper links as native fragment links.
for (const explorer of document.querySelectorAll('[data-direction-explorer]')) {
 const tabs=[...explorer.querySelectorAll('[data-direction]')];
 const select=id=>{
  for (const tab of tabs) {
   const active=tab.dataset.direction===id;
   tab.setAttribute('aria-selected',String(active));tab.tabIndex=active?0:-1;
   document.getElementById(tab.getAttribute('aria-controls')).hidden=!active;
  }
 };
 for (const [i,tab] of tabs.entries()) {
  tab.addEventListener('click',()=>select(tab.dataset.direction));
  tab.addEventListener('keydown',event=>{
   let index;
   if(event.key==='ArrowRight')index=(i+1)%tabs.length;
   if(event.key==='ArrowLeft')index=(i+tabs.length-1)%tabs.length;
   if(event.key==='Home')index=0;
   if(event.key==='End')index=tabs.length-1;
   if(index!==undefined){event.preventDefault();select(tabs[index].dataset.direction);tabs[index].focus();}
  });
 }
 const followDirectionHash=()=>{const id=location.hash.slice(1);if(tabs.some(tab=>tab.dataset.direction===id))select(id);};
 followDirectionHash();window.addEventListener('hashchange',followDirectionHash);
}
for (const lab of document.querySelectorAll('[data-opening]')) {
 if(lab.dataset.opening==='pareto') {
  const solve=w=>{if(w===0)return 1;if(w===1)return 0;let lo=0,hi=1;for(let i=0;i<55;i++){const z=(lo+hi)/2;if(2*w*z-4*(1-w)*(1-z)**3>0)hi=z;else lo=z;}return(lo+hi)/2;};
  const M=4000,arc=[0];
  for(let i=1;i<=M;i++){const z=i/M,p=(i-1)/M;arc.push(arc[i-1]+Math.hypot(z*z-p*p,(1-z)**4-(1-p)**4));}
  const at=z=>{const i=Math.min(M-1,Math.floor(z*M));return arc[i]+(z*M-i)*(arc[i+1]-arc[i]);};
  const inverse=q=>{const target=q*arc[M];let lo=0,hi=M;while(hi-lo>1){const mid=Math.floor((lo+hi)/2);if(arc[mid]<target)lo=mid;else hi=mid;}return(lo+(target-arc[lo])/(arc[hi]-arc[lo]))/M;};
  const points=[...lab.querySelectorAll('[data-front-point]')];
  const update=mode=>{
   lab.dataset.spacingMode=mode;
   for(const b of lab.querySelectorAll('[data-spacing]'))b.setAttribute('aria-pressed',String(b.dataset.spacing===mode));
   const zs=points.map((point,i)=>{const z=mode==='arc'?inverse(i/(points.length-1)):solve(1-i/(points.length-1));point.setAttribute('cx',90+280*z*z);point.setAttribute('cy',305-280*(1-z)**4);return z;});
   const gaps=zs.slice(1).map((z,i)=>at(z)-at(zs[i]));
   const ratio=Math.max(...gaps)/Math.min(...gaps);
   lab.querySelector('[data-spacing-result]').textContent=mode==='arc'?'The points spread into even arc-length gaps.':`The largest arc gap is ${ratio.toFixed(1)}× the smallest.`;
  };
  for(const b of lab.querySelectorAll('[data-spacing]'))b.addEventListener('click',()=>update(b.dataset.spacing));
  update('weights');
 }
 if(lab.dataset.opening==='bilevel') {
  const range=lab.querySelector('input'),g=lab.querySelector('[data-response-plot]');
  const update=()=>{
   const x=+range.value,xx=y=>55+350*y/6,yy=y=>225-175*(y-2*x)**2/36;
   g.replaceChildren();
   g.append(node('rect',{x:55,y:25,width:xx(x)-55,height:200,fill:'#e6f3f0'}));
   g.append(node('path',{d:'M55 25 V225 H422',fill:'none',stroke:'#9aabc7'}));
   g.append(node('polyline',{points:Array.from({length:121},(_,i)=>`${xx(i/20)},${yy(i/20)}`).join(' '),fill:'none',stroke:'#a6b2c9','stroke-width':2.5}));
   g.append(node('path',{d:`M${xx(x)} 25 V225`,stroke:'#007c70','stroke-width':2,'stroke-dasharray':'5 5'}));
   g.append(node('circle',{cx:xx(2*x),cy:yy(2*x),r:6,fill:'#354ac6',stroke:'white','stroke-width':2}));
   g.append(node('circle',{cx:xx(x),cy:yy(x),r:6,fill:'#007c70',stroke:'white','stroke-width':2}));
   g.append(node('text',{x:235,y:263,'text-anchor':'middle'},'Follower decision y (0 to 6)'));
   g.append(node('text',{x:20,y:135,'text-anchor':'middle',transform:'rotate(-90 20 135)'},'Inner loss'));
   lab.querySelector('[data-leader-value]').textContent=x.toFixed(1);
   lab.querySelector('[data-response-result]').textContent=`Without the constraint: y* = ${(2*x).toFixed(1)}. With it: y* = ${x.toFixed(1)}.`;
  };range.addEventListener('input',update);update();
 }
 if(lab.dataset.opening==='applications') {
  const select=id=>{
   for(const b of lab.querySelectorAll('[data-application]'))b.setAttribute('aria-pressed',String(b.dataset.application===id));
   for(const view of lab.querySelectorAll('[data-application-view]'))view.hidden=view.dataset.applicationView!==id;
  };
  for(const b of lab.querySelectorAll('[data-application]'))b.addEventListener('click',()=>select(b.dataset.application));
  select('speech');
 }
}
