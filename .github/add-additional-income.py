from pathlib import Path

p = Path('index.html')
s = p.read_text()

marker = '<!-- ADDITIONAL_INCOME_FEATURE -->'
if marker not in s:
    feature = r'''
<!-- ADDITIONAL_INCOME_FEATURE -->
<style>
.additional-income-actions{margin-top:16px;display:flex;justify-content:flex-end}
.additional-income-actions .add-income-btn{background:#e9eef5;color:var(--navy);padding:10px 14px}
.additional-income-entry{margin-top:14px;border:1px solid var(--border);border-radius:9px;padding:14px;background:#fafbfc}
.additional-income-entry-header{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:12px}
.additional-income-entry-header strong{color:var(--navy);font-size:14px}
.additional-income-remove{padding:7px 10px;background:#f4e8e8;color:#8a1c1c;font-size:12px}
.additional-income-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:14px}
@media(max-width:720px){.additional-income-grid{grid-template-columns:1fr}.additional-income-actions .add-income-btn{width:100%}}
</style>
<script>
(function(){
  function incomeCards(){
    const headings=[...document.querySelectorAll('.card h2,.card h3')];
    let cards=headings.filter(h=>/^income\s*&\s*expenses$/i.test((h.textContent||'').trim())).map(h=>h.closest('.card')).filter(Boolean);
    if(!cards.length){
      cards=headings.filter(h=>/^income$/i.test((h.textContent||'').trim())).map(h=>h.closest('.card')).filter(Boolean);
    }
    return [...new Set(cards)];
  }
  function applicantNumber(card,index){
    if(card.classList.contains('a2-only') || card.closest('.a2-only')) return 2;
    const text=(card.textContent||'').slice(0,500);
    if(/Applicant\s*2/i.test(text)) return 2;
    return index+1;
  }
  function addEntry(card, applicant){
    const host=card.querySelector('.additional-income-list');
    const count=host.children.length+1;
    const key='applicant'+applicant+'_additional_income_'+Date.now()+'_'+count;
    const entry=document.createElement('div');
    entry.className='additional-income-entry';
    entry.innerHTML=`
      <div class="additional-income-entry-header">
        <strong>Additional Income ${count}</strong>
        <button type="button" class="additional-income-remove">Remove</button>
      </div>
      <div class="additional-income-grid">
        <div><label>Income Type / Source</label><input type="text" name="${key}_source" placeholder="e.g. Overtime, Allowance, Rental income, Centrelink"></div>
        <div><label>Gross Amount ($)</label><input type="number" min="0" step="0.01" name="${key}_amount" placeholder="0.00"></div>
        <div><label>Frequency</label><select name="${key}_frequency"><option value="">Select</option><option>Weekly</option><option>Fortnightly</option><option>Monthly</option><option>Quarterly</option><option>Annually</option></select></div>
        <div><label>Notes / Description</label><input type="text" name="${key}_notes" placeholder="Optional"></div>
      </div>`;
    entry.querySelector('.additional-income-remove').addEventListener('click',()=>entry.remove());
    host.appendChild(entry);
  }
  function init(){
    incomeCards().forEach((card,index)=>{
      if(card.querySelector('.additional-income-actions')) return;
      const content=card.querySelector('.content')||card;
      const list=document.createElement('div');
      list.className='additional-income-list';
      const actions=document.createElement('div');
      actions.className='additional-income-actions';
      const btn=document.createElement('button');
      btn.type='button';
      btn.className='add-income-btn';
      btn.textContent='+ Add Another Income';
      const applicant=applicantNumber(card,index);
      btn.addEventListener('click',()=>addEntry(card,applicant));
      actions.appendChild(btn);
      content.appendChild(list);
      content.appendChild(actions);
    });
  }
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',init); else init();
})();
</script>
'''
    s = s.replace('</body>', feature + '\n</body>', 1)
    p.write_text(s)
