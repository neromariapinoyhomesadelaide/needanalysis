from pathlib import Path
import re

p=Path('index.html')
s=p.read_text()

# Remove the duplicate Household Expenses subsection from Household / Shared Information.
s=re.sub(
    r'\s*<h3>Household Expenses\s*<span class="note">\(monthly\)</span></h3>\s*<div class="grid3">.*?</div>\s*(?=<h3>Property Goals</h3>)',
    '\n', s, count=1, flags=re.S|re.I
)

# Add compact sharing controls to every existing expense amount field in the form.
# We deliberately exclude the removed household_* expense fields and applicant debt repayments.
expense_words=re.compile(r'(expense|expenses|grocer|utilit|transport|insurance|rent|board|childcare|school|living|medical|health|education|entertainment|subscription)',re.I)
exclude_words=re.compile(r'(income|asset|liabil|loan|credit|mortgage|repayment|balance|limit|deposit|saving|property|value|supporting|document|household_)',re.I)

# A sharing selector is added beside each likely expense input/select based on its label/name.
def enhance_block(m):
    block=m.group(0)
    if 'expense-sharing-select' in block:
        return block
    labelm=re.search(r'<label[^>]*>(.*?)</label>',block,re.S|re.I)
    inputm=re.search(r'<(?:input|select)\b[^>]*\bname="([^"]+)"[^>]*>',block,re.S|re.I)
    if not labelm or not inputm:
        return block
    label=re.sub('<[^>]+>',' ',labelm.group(1))
    name=inputm.group(1)
    hay=label+' '+name
    if not expense_words.search(hay) or exclude_words.search(hay):
        return block
    # avoid adding to applicant-independent metadata fields
    share_name=name+'_sharing'
    selector=(
        '<div class="expense-sharing-wrap"><label>Is this expense shared?</label>'
        f'<select class="expense-sharing-select" name="{share_name}">'
        '<option value="">Select</option><option value="Yes - Shared">Yes — Shared</option>'
        '<option value="No - Applicant 1">No — Applicant 1 only</option>'
        '<option value="No - Applicant 2">No — Applicant 2 only</option>'
        '</select></div>'
    )
    return block[:-6]+selector+'</div>' if block.endswith('</div>') else block+selector

# Operate on simple field divs only.
s=re.sub(r'<div>(?:(?!<div>).)*?<label[^>]*>.*?</label>(?:(?!<div>).)*?<(?:input|select)\b[^>]*\bname="[^"]+"[^>]*>.*?</div>',enhance_block,s,flags=re.S|re.I)

# Styling.
if '.expense-sharing-wrap{' not in s:
    css='''\n.expense-sharing-wrap{margin-top:8px;padding-top:8px;border-top:1px dashed var(--border)}\n.expense-sharing-wrap label{font-size:11px;color:var(--muted);margin-bottom:4px}\n.expense-sharing-select{font-size:12px;padding:8px 9px;background:#f8fafc}\n'''
    s=s.replace('</style>',css+'</style>',1)

p.write_text(s)
