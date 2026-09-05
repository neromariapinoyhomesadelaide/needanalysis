from pathlib import Path
import re

p=Path('index.html')
s=p.read_text()

start=s.find('<div class="card" id="householdSharedSection">')
if start==-1: raise SystemExit('Household Shared section not found')
end=s.find('<div class="card"><h2>Disclaimer</h2>',start)
if end==-1: raise SystemExit('Disclaimer marker not found')
section=s[start:end]

# Make headings/labels neutral because each item can now be shared or individual.
section=section.replace('<h3>Joint Assets</h3>','<h3>Assets</h3>')
section=section.replace('<h3>Joint Liabilities</h3>','<h3>Liabilities</h3>')
section=section.replace('Joint Savings / Cash','Savings / Cash')
section=section.replace('Joint Property / Investment Value','Property / Investment Value')
section=section.replace('Other Joint Assets','Other Assets')
section=section.replace('Joint Home Loan Balance','Home Loan Balance')
section=section.replace('Joint Home Loan Repayment (monthly)','Home Loan Repayment (monthly)')
section=section.replace('Joint Personal Loan Balance','Personal Loan Balance')
section=section.replace('Joint Personal Loan Repayment (monthly)','Personal Loan Repayment (monthly)')
section=section.replace('Joint Credit Card Limit','Credit Card Limit')
section=section.replace('Joint Credit Card Balance','Credit Card Balance')
section=section.replace('BNPL / Other Joint Debt Balance','BNPL / Other Debt Balance')

# Add a Shared / Applicant 1 / Applicant 2 selector to each remaining Household field.
def add_selector(m):
    block=m.group(0)
    if 'household-sharing-select' in block or 'expense-sharing-select' in block:
        return block
    name_m=re.search(r'<(?:input|select)\b[^>]*\bname="([^"]+)"[^>]*>',block,re.I|re.S)
    if not name_m: return block
    name=name_m.group(1)
    if not name.startswith('household_'): return block
    selector=(
        '<div class="household-sharing-wrap"><label>Is this shared?</label>'
        f'<select class="household-sharing-select" name="{name}_sharing">'
        '<option value="">Select</option>'
        '<option value="Shared">Yes — Shared</option>'
        '<option value="Applicant 1 only">No — Applicant 1 only</option>'
        '<option value="Applicant 2 only">No — Applicant 2 only</option>'
        '</select></div>'
    )
    if block.endswith('</div>'):
        return block[:-6]+selector+'</div>'
    return block+selector

section=re.sub(r'<div>(?:(?!<div>).)*?<label[^>]*>.*?</label>(?:(?!<div>).)*?<(?:input|select)\b[^>]*\bname="household_[^"]+"[^>]*>.*?</div>',add_selector,section,flags=re.S|re.I)

s=s[:start]+section+s[end:]

if '.household-sharing-wrap{' not in s:
    css='''\n.household-sharing-wrap{margin-top:8px;padding-top:8px;border-top:1px dashed var(--border)}\n.household-sharing-wrap label{font-size:11px;color:var(--muted);margin-bottom:4px}\n.household-sharing-select{font-size:12px;padding:8px 9px;background:#f8fafc}\n'''
    s=s.replace('</style>',css+'</style>',1)

p.write_text(s)
