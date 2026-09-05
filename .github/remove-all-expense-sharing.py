from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()
# Remove every expense-sharing UI block and its select field.
s=re.sub(r'\s*<div class="expense-sharing-wrap">.*?</div>','',s,flags=re.S|re.I)
# Remove any stray sharing selects/labels if markup was altered.
s=re.sub(r'\s*<label[^>]*>\s*Is this expense shared\?\s*</label>\s*','',s,flags=re.I)
s=re.sub(r'\s*<select[^>]*class="[^"]*expense-sharing-select[^"]*"[^>]*>.*?</select>','',s,flags=re.S|re.I)
# Remove styling for the deleted controls.
s=re.sub(r'\s*\.expense-sharing-wrap\{[^}]*\}\s*\.expense-sharing-wrap label\{[^}]*\}\s*\.expense-sharing-select\{[^}]*\}','',s,flags=re.S)
p.write_text(s)
