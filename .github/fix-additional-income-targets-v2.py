from pathlib import Path
p=Path('index.html')
s=p.read_text()
old="""function incomeCards(){
    const headings=[...document.querySelectorAll('.card h2,.card h3')];
    let cards=headings.filter(h=>/^income\\s*&\\s*expenses$/i.test((h.textContent||'').trim())).map(h=>h.closest('.card')).filter(Boolean);
    if(!cards.length){
      cards=headings.filter(h=>/^income$/i.test((h.textContent||'').trim())).map(h=>h.closest('.card')).filter(Boolean);
    }
    return [...new Set(cards)];
  }"""
new="""function incomeCards(){
    const targets=[];
    const grossHeading=[...document.querySelectorAll('.card h2')].find(h=>/^gross\\s+income$/i.test((h.textContent||'').trim()));
    if(grossHeading && grossHeading.closest('.card')) targets.push(grossHeading.closest('.card'));
    const applicant2=document.querySelector('.applicant2-financial-details');
    if(applicant2) targets.push(applicant2);
    return targets;
  }"""
if old not in s:
    raise SystemExit('Original incomeCards block not found')
s=s.replace(old,new,1)
old2="if(card.classList.contains('a2-only') || card.closest('.a2-only')) return 2;"
new2="if(card.classList.contains('a2-only') || card.closest('.a2-only') || card.classList.contains('applicant2-financial-details') || card.closest('.applicant2-financial-details')) return 2;"
if old2 in s:
    s=s.replace(old2,new2,1)
p.write_text(s)
