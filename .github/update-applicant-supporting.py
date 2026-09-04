from pathlib import Path
import re

p = Path("index.html")
s = p.read_text()

s, n1 = re.subn(
    r"if \(status\) status\.textContent = `\$\{SA_SUBURB_NAMES\.length\} South Australia suburbs/localities loaded\.`;",
    "if (status) { status.textContent = ''; status.style.display = 'none'; }",
    s,
    count=1
)
if n1 != 1:
    raise SystemExit("Suburb status line not found")

new_html = """<div class="card"><h2>Supporting Documents</h2><div class="content">
<p class="note" style="font-size:13px;margin-top:0">Upload each document under the correct applicant and category. You may add more than one file where required.</p>

<div class="asset" style="margin-bottom:16px">
<strong>Applicant 1</strong>
<div class="file-upload-box"><label for="a1PayslipsDocuments"><strong>1. Payslips</strong></label><input id="a1PayslipsDocuments" class="supporting-document-input" data-category="Applicant 1 — Payslips" type="file" multiple accept=".pdf,.jpg,.jpeg,.png,.doc,.docx" /><div class="file-list" data-file-list="Applicant 1 — Payslips"></div></div>
<div class="file-upload-box"><label for="a1IdentificationDocuments"><strong>2. Identification Cards</strong> <span class="note">(Driver's Licence, Passport)</span></label><input id="a1IdentificationDocuments" class="supporting-document-input" data-category="Applicant 1 — Identification Cards" type="file" multiple accept=".pdf,.jpg,.jpeg,.png,.doc,.docx" /><div class="file-list" data-file-list="Applicant 1 — Identification Cards"></div></div>
<div class="file-upload-box"><label for="a1IncomeStatementDocuments"><strong>3. Income Statements (ATO)</strong></label><input id="a1IncomeStatementDocuments" class="supporting-document-input" data-category="Applicant 1 — Income Statements (ATO)" type="file" multiple accept=".pdf,.jpg,.jpeg,.png,.doc,.docx" /><div class="file-list" data-file-list="Applicant 1 — Income Statements (ATO)"></div></div>
<div class="file-upload-box"><label for="a1BankStatementDocuments"><strong>4. Bank Statements</strong> <span class="note">(120-day Transaction Reports)</span></label><input id="a1BankStatementDocuments" class="supporting-document-input" data-category="Applicant 1 — Bank Statements (120-day Transaction Reports)" type="file" multiple accept=".pdf,.jpg,.jpeg,.png,.doc,.docx" /><div class="file-list" data-file-list="Applicant 1 — Bank Statements (120-day Transaction Reports)"></div></div>
</div>

<div class="asset a2-only" id="applicant2SupportingDocuments" style="margin-bottom:16px">
<strong>Applicant 2</strong>
<div class="file-upload-box"><label for="a2PayslipsDocuments"><strong>1. Payslips</strong></label><input id="a2PayslipsDocuments" class="supporting-document-input" data-category="Applicant 2 — Payslips" type="file" multiple accept=".pdf,.jpg,.jpeg,.png,.doc,.docx" /><div class="file-list" data-file-list="Applicant 2 — Payslips"></div></div>
<div class="file-upload-box"><label for="a2IdentificationDocuments"><strong>2. Identification Cards</strong> <span class="note">(Driver's Licence, Passport)</span></label><input id="a2IdentificationDocuments" class="supporting-document-input" data-category="Applicant 2 — Identification Cards" type="file" multiple accept=".pdf,.jpg,.jpeg,.png,.doc,.docx" /><div class="file-list" data-file-list="Applicant 2 — Identification Cards"></div></div>
<div class="file-upload-box"><label for="a2IncomeStatementDocuments"><strong>3. Income Statements (ATO)</strong></label><input id="a2IncomeStatementDocuments" class="supporting-document-input" data-category="Applicant 2 — Income Statements (ATO)" type="file" multiple accept=".pdf,.jpg,.jpeg,.png,.doc,.docx" /><div class="file-list" data-file-list="Applicant 2 — Income Statements (ATO)"></div></div>
<div class="file-upload-box"><label for="a2BankStatementDocuments"><strong>4. Bank Statements</strong> <span class="note">(120-day Transaction Reports)</span></label><input id="a2BankStatementDocuments" class="supporting-document-input" data-category="Applicant 2 — Bank Statements (120-day Transaction Reports)" type="file" multiple accept=".pdf,.jpg,.jpeg,.png,.doc,.docx" /><div class="file-list" data-file-list="Applicant 2 — Bank Statements (120-day Transaction Reports)"></div></div>
</div>

<p class="note">PDF, JPG, PNG, DOC or DOCX. Maximum 10 MB per file, up to 10 files in total.</p><div class="upload-status" id="uploadStatus"></div>
</div></div>"""

s, n2 = re.subn(
    r'<div class="card"><h2>Supporting Documents</h2>.*?</div></div>\n<div class="card"><h2>Disclaimer</h2>',
    new_html + '\n<div class="card"><h2>Disclaimer</h2>',
    s,
    count=1,
    flags=re.S
)
if n2 != 1:
    raise SystemExit("Supporting Documents block not found")

old = "  if (adding) card.scrollIntoView({behavior:'smooth', block:'start'});\n}"
new = "  if (!adding) {\n    selectedSupportingFiles = selectedSupportingFiles.filter(x => !String(x.category || '').startsWith('Applicant 2 — '));\n    renderSupportingFiles();\n  }\n  if (adding) card.scrollIntoView({behavior:'smooth', block:'start'});\n}"
if old not in s:
    raise SystemExit("toggleApplicant2 target not found")
s = s.replace(old, new, 1)

p.write_text(s)
