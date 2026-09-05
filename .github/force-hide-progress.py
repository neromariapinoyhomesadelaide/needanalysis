from pathlib import Path
p=Path('index.html')
s=p.read_text()
marker='/* FORCE_HIDE_PROGRESS_NAV */'
if marker not in s:
    css='''\n<style>\n/* FORCE_HIDE_PROGRESS_NAV */\n.progress-shell,.progress-current,.progress-nav,.progress-bar-track,.progress-applicant-row,.progress-applicant{display:none!important}\/n</style>\n'''.replace('\\/n','\n')
    s=s.replace('</head>', css+'</head>', 1)
    js='''\n<script>\ndocument.addEventListener('DOMContentLoaded',function(){\n  document.querySelectorAll('.progress-shell,.progress-current,.progress-nav,.progress-bar-track,.progress-applicant-row,.progress-applicant').forEach(function(el){el.remove();});\n  Array.from(document.querySelectorAll('body *')).forEach(function(el){\n    var t=(el.textContent||'').trim();\n    if(t==='Step 1 of 6 — Personal Details'){ el.remove(); }\n  });\n});\n</script>\n'''
    s=s.replace('</body>', js+'</body>', 1)
p.write_text(s)
