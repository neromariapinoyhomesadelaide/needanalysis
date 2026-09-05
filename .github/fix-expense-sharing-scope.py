from pathlib import Path
import re

p=Path('index.html')
s=p.read_text()

# Remove every sharing selector previously injected outside the intended Expenses section.
s=re.sub(r'<div class="expense-sharing-wrap">.*?</div>','',s,flags=re.S|re.I)
s=re.sub(r'<div class="household-sharing-wrap">.*?</div>','',s,flags=re.S|re.I)

# Remove the now-unused Household sharing styles.
s=re.sub(r'\n?\.household-sharing-wrap\{.*?\}\n\.household-sharing-wrap label\{.*?\}\n\.household-sharing-select\{.*?\}\n?','\n',s,flags=re.S)

# Find cards whose main heading is specifically an Expenses section.
card_pattern=re.compile(r'<div class="card"[^>]*>.*?</div></div>',re.S|re.I)

def enhance_expenses_card(m):
    card=m.group(0)
    heading=re.search(r'<h2[^>]*>(.*?)</h2>',card,re.S|re.I)
    if not heading:
        return card
    heading_text=re.sub(r'<[^>]+>',' ',heading.group(1)).strip().lower()
    if 'expense' not in heading_text:
        return card

    # Add sharing selector to each simple field in this Expenses card only.
    def add_selector(fm):
        block=fm.group(0)
        if 'expense-sharing-select' in block:
            return block
        name_m=re.search(r'<(?:input|select)\b[^>]*\bname="([^"]+)"[^>]*>',block,re.S|re.I)
        if not name_m:
            return block
        name=name_m.group(1)
        selector=(
            '<div class="expense-sharing-wrap"><label>Is this expense shared?</label>'
            f'<select class="expense-sharing-select" name="{name}_sharing">'
            '<option value="">Select</option>'
            '<option value="Yes - Shared">Yes — Shared</option>'
            '<option value="No - Applicant 1">No — Applicant 1 only</option>'
            '<option value="No - Applicant 2">No — Applicant 2 only</option>'
            '</select></div>'
        )
        return block[:-6]+selector+'</div>' if block.endswith('</div>') else block+selector

    return re.sub(
        r'<div>(?:(?!<div>).)*?<label[^>]*>.*?</label>(?:(?!<div>).)*?<(?:input|select)\b[^>]*\bname="[^"]+"[^>]*>.*?</div>',
        add_selector,
        card,
        flags=re.S|re.I
    )

s=card_pattern.sub(enhance_expenses_card,s)

# Ensure styling exists for the selectors that remain in Expenses only.
if '.expense-sharing-wrap{' not in s:
    css='''\n.expense-sharing-wrap{margin-top:8px;padding-top:8px;border-top:1px dashed var(--border)}\n.expense-sharing-wrap label{font-size:11px;color:var(--muted);margin-bottom:4px}\n.expense-sharing-select{font-size:12px;padding:8px 9px;background:#f8fafc}\n'''
    s=s.replace('</style>',css+'</style>',1)

p.write_text(s)
