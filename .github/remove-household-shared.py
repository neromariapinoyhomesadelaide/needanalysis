from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()
# Remove Household / Shared Information card.
s=re.sub(r'\s*<div class="card" id="householdSharedSection">.*?(?=<div class="card"><h2>Disclaimer</h2>)','\n',s,count=1,flags=re.S|re.I)
# Remove Household progress step.
s=re.sub(r'\s*<button[^>]*class="progress-step[^>]*data-key="household"[^>]*>.*?</button>','',s,count=1,flags=re.S|re.I)
# Renumber remaining progress steps.
def renumber(m):
    renumber.n+=1
    return re.sub(r'data-step="[^"]*"',f'data-step="{renumber.n}"',m.group(0),count=1)
renumber.n=0
s=re.sub(r'<button[^>]*class="progress-step[^>]*>',renumber,s)
# Six-column progress navigation and initial label.
s=re.sub(r'(\.progress-nav\{max-width:1100px;margin:0 auto;display:grid;grid-template-columns:repeat\()\d+(,1fr\);)',r'\g<1>6\2',s,count=1)
s=re.sub(r'Step 1 of \d+ — Personal Details','Step 1 of 6 — Personal Details',s,count=1)
# Remove household from progress labels/targets.
s=s.replace(",household:'Household / Shared Information'",'')
s=re.sub(r'\s*const household=document\.getElementById\([\'\"]householdSharedSection[\'\"]\);','',s)
s=s.replace(',household,review}',',review}')
# Remove household badge helper script if present.
s=re.sub(r'\s*<script>\s*\(function\(\)\{\s*function updateHouseholdProgressBadge\(\).*?</script>','',s,count=1,flags=re.S)
# Remove obsolete household sharing CSS.
s=re.sub(r'\s*\.household-sharing-wrap\{[^}]*\}\s*\.household-sharing-wrap label\{[^}]*\}\s*\.household-sharing-select\{[^}]*\}','',s,flags=re.S)
p.write_text(s)
