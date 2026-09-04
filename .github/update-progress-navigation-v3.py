from pathlib import Path

p = Path('index.html')
s = p.read_text()

if 'id="formProgressNav"' in s:
    raise SystemExit('Progress navigation already installed')

css = '''
.progress-shell{position:sticky;top:0;z-index:50;background:rgba(245,247,250,.97);backdrop-filter:blur(8px);border-bottom:1px solid var(--border);padding:10px 16px}
.progress-nav{max-width:1100px;margin:0 auto;display:grid;grid-template-columns:repeat(5,1fr);gap:8px;position:relative}
.progress-step{appearance:none;border:0;background:transparent;padding:8px 6px;color:var(--muted);font-size:12px;font-weight:700;cursor:pointer;text-align:center;line-height:1.2;position:relative}
.progress-step::before{content:attr(data-step);display:flex;align-items:center;justify-content:center;width:28px;height:28px;border-radius:50%;border:2px solid #cbd5e1;background:#fff;margin:0 auto 6px;color:var(--muted);transition:.2s}
.progress-step.active{color:var(--navy)}
.progress-step.active::before,.progress-step.complete::before{border-color:var(--blue);background:var(--blue);color:#fff}
.progress-step:hover::before{border-color:var(--blue)}
.progress-bar-track{max-width:1100px;height:4px;background:#dbe3ec;border-radius:999px;margin:0 auto 7px;overflow:hidden}
.progress-bar-fill{height:100%;width:0;background:var(--blue);transition:width .25s ease}
.progress-current{display:none;max-width:1100px;margin:0 auto 6px;font-size:12px;font-weight:700;color:var(--navy)}
@media(max-width:700px){.progress-shell{padding:8px 10px}.progress-current{display:block}.progress-nav{display:flex;overflow-x:auto;gap:2px;scrollbar-width:none}.progress-nav::-webkit-scrollbar{display:none}.progress-step{min-width:118px;font-size:11px;padding:5px 3px}.progress-step::before{width:24px;height:24px;margin-bottom:4px}}
'''
s = s.replace('</style>', css + '\n</style>', 1)

nav = '''
<div class="progress-shell" id="formProgressNav">
  <div class="progress-current" id="progressCurrent">Step 1 of 5 — Personal Details</div>
  <div class="progress-bar-track"><div class="progress-bar-fill" id="progressBarFill"></div></div>
  <nav class="progress-nav" aria-label="Form progress">
    <button type="button" class="progress-step active" data-step="1" data-key="personal">Personal Details</button>
    <button type="button" class="progress-step" data-step="2" data-key="employment">Employment Details</button>
    <button type="button" class="progress-step" data-step="3" data-key="income">Income &amp; Expenses</button>
    <button type="button" class="progress-step" data-step="4" data-key="assets">Assets &amp; Liabilities</button>
    <button type="button" class="progress-step" data-step="5" data-key="documents">Supporting Documents</button>
  </nav>
</div>
'''
if '</header>' not in s:
    raise SystemExit('Header marker not found')
s = s.replace('</header>', '</header>\n' + nav, 1)

js = '''
<script>
(function(){
  const labels={personal:'Personal Details',employment:'Employment Details',income:'Income & Expenses',assets:'Assets & Liabilities',documents:'Supporting Documents'};
  function headingMatch(text){return Array.from(document.querySelectorAll('h2,h3')).find(h=>h.textContent.trim().toLowerCase().includes(text.toLowerCase()));}
  function progressTargets(){
    const personal=headingMatch('Personal Details — Applicant 1')||headingMatch('Personal Details')||document.querySelector('[name="a1_first_name"]')?.closest('.card');
    const employment=headingMatch('Employment Details — Applicant 1')||headingMatch('Employment Details');
    const income=headingMatch('Gross Income — Applicant 1')||headingMatch('Gross Income')||document.querySelector('[name="a1_base_income"]')?.closest('.card');
    const assets=headingMatch('Property Assets')||headingMatch('Assets')||document.querySelector('[name="property_1_address"]')?.closest('.card');
    const documents=Array.from(document.querySelectorAll('h2')).find(h=>h.textContent.trim()==='Supporting Documents')?.closest('.card');
    return {personal,employment,income,assets,documents};
  }
  const steps=Array.from(document.querySelectorAll('#formProgressNav .progress-step'));
  const fill=document.getElementById('progressBarFill');
  const current=document.getElementById('progressCurrent');
  function setActive(index){
    const safe=Math.max(0,Math.min(index,steps.length-1));
    steps.forEach((btn,i)=>{btn.classList.toggle('active',i===safe);btn.classList.toggle('complete',i<safe);if(i===safe)btn.setAttribute('aria-current','step');else btn.removeAttribute('aria-current');});
    if(fill)fill.style.width=((safe+1)/steps.length*100)+'%';
    if(current)current.textContent=`Step ${safe+1} of ${steps.length} — ${labels[steps[safe].dataset.key]}`;
    steps[safe]?.scrollIntoView({block:'nearest',inline:'center'});
  }
  steps.forEach((btn,index)=>btn.addEventListener('click',()=>{
    const target=progressTargets()[btn.dataset.key]; if(!target)return;
    const offset=document.getElementById('formProgressNav')?.offsetHeight||0;
    const y=target.getBoundingClientRect().top+window.scrollY-offset-14;
    window.scrollTo({top:y,behavior:'smooth'}); setActive(index);
  }));
  let ticking=false;
  function updateFromScroll(){
    if(ticking)return; ticking=true;
    requestAnimationFrame(()=>{
      const targets=progressTargets(); const offset=(document.getElementById('formProgressNav')?.offsetHeight||0)+40; let active=0;
      steps.forEach((btn,index)=>{const el=targets[btn.dataset.key]; if(el&&el.getBoundingClientRect().top<=offset)active=index;});
      setActive(active); ticking=false;
    });
  }
  window.addEventListener('scroll',updateFromScroll,{passive:true});
  window.addEventListener('resize',updateFromScroll);
  setActive(0); updateFromScroll();
})();
</script>
'''
if '</body>' not in s: raise SystemExit('Body marker not found')
s=s.replace('</body>',js+'\n</body>',1)
p.write_text(s)
