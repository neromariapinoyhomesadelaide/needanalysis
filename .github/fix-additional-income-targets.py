from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()
pattern=r'''function incomeCards\(\)\{.*?return \[\.\.\.new Set\(cards\)\];\n  \}'''
replacement='''function incomeCards(){
    const targets=[];
    const grossHeading=[...document.querySelectorAll('.card h2')].find(h=>/^gross\\s+income$/i.test((h.textContent||'').trim()));
    if(grossHeading && grossHeading.closest('.card')) targets.push(grossHeading.closest('.card'));
    const applicant2=document.querySelector('.applicant2-financial-details');
    if(applicant2) targets.push(applicant2);
    return targets;
  }'''
s2,n=re.subn(pattern,replacement,s,count=1,flags=re.S)
if n!=1:
    raise SystemExit('Could not locate additional income target function')
s=s2
# Ensure Applicant 2 container is recognised correctly.
s=s.replace("if(card.classList.contains('a2-only') || card.closest('.a2-only')) return 2;","if(card.classList.contains('a2-only') || card.closest('.a2-only') || card.classList.contains('applicant2-financial-details') || card.closest('.applicant2-financial-details')) return 2;")
p.write_text(s)
