from pathlib import Path
import re
p=Path('index.html')
s=p.read_text()
# Remove the visible progress indicator shell.
s=re.sub(r'\s*<div[^>]*class="progress-shell"[^>]*>.*?</div>\s*</div>', '\n', s, count=1, flags=re.S|re.I)
# Remove progress-related CSS rules and mobile variants while leaving unrelated form styles intact.
s=re.sub(r'\n\.progress-shell\{.*?(?=\n\.applicant2-add-wrap\{)', '\n', s, count=1, flags=re.S)
s=re.sub(r'\n\.progress-applicant-row\{.*?@media\(max-width:700px\)\{\.applicant2-add-wrap\{padding:0 16px\}\.applicant2-add-wrap button\{width:100%\}\.progress-applicant-row\{.*?\}\}\n', '\n.applicant2-add-wrap{max-width:1100px;margin:-4px auto 20px;padding:0;display:flex;justify-content:flex-end}\n.applicant2-add-wrap button{min-width:190px}\n@media(max-width:700px){.applicant2-add-wrap{padding:0 16px}.applicant2-add-wrap button{width:100%}}\n', s, count=1, flags=re.S)
# Disable/remove progress JavaScript blocks that reference progress controls.
s=re.sub(r'\s*<script>\s*\(function\(\)\{(?:(?!</script>).)*progress(?:Shell|Step|Targets|Current|Applicant|Bar)(?:(?!</script>).)*</script>', '', s, flags=re.S|re.I)
p.write_text(s)
