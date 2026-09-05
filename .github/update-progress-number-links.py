from pathlib import Path

p=Path('index.html')
s=p.read_text()

# The progress steps are already buttons with click navigation. Make the numbered
# circle itself explicitly interactive and keyboard accessible by rendering it as
# a child span rather than a CSS pseudo-element.
if '.progress-step-number{' not in s:
    s=s.replace(
        ".progress-step::before{content:attr(data-step);display:flex;align-items:center;justify-content:center;width:28px;height:28px;border-radius:50%;border:2px solid #cbd5e1;background:#fff;margin:0 auto 6px;color:var(--muted);transition:.2s}",
        ".progress-step::before{display:none}.progress-step-number{display:flex;align-items:center;justify-content:center;width:28px;height:28px;border-radius:50%;border:2px solid #cbd5e1;background:#fff;margin:0 auto 6px;color:var(--muted);transition:.2s;cursor:pointer}.progress-step.active .progress-step-number,.progress-step.complete .progress-step-number{border-color:var(--blue);background:var(--blue);color:#fff}.progress-step:hover .progress-step-number,.progress-step-number:focus-visible{border-color:var(--blue);outline:none}",
        1
    )
    s=s.replace(
        ".progress-step.active::before,.progress-step.complete::before{border-color:var(--blue);background:var(--blue);color:#fff}\n.progress-step:hover::before{border-color:var(--blue)}",
        "",
        1
    )
    s=s.replace(
        ".progress-step::before{width:24px;height:24px;margin-bottom:4px}",
        ".progress-step-number{width:24px;height:24px;margin-bottom:4px}",
        1
    )

# Add visible numbered link spans inside every progress button. Clicking the
# number bubbles to the existing progress-step click handler and smooth-scrolls
# to exactly the same section as clicking the step label.
import re
def add_number(m):
    tag=m.group(1)
    body=m.group(2)
    if 'progress-step-number' in body:
        return m.group(0)
    step=re.search(r'data-step="([^"]+)"',tag)
    if not step:
        return m.group(0)
    num=step.group(1)
    return f'{tag}<span class="progress-step-number" role="link" tabindex="0" aria-label="Go to step {num}">{num}</span>{body}</button>'

s=re.sub(r'(<button[^>]*class="progress-step[^>]*>)(.*?)</button>',add_number,s,flags=re.S)

# Keyboard activation when the number itself is focused.
if 'progress-step-number-keyboard' not in s:
    js='''\n<script id="progress-step-number-keyboard">\n(function(){\n  document.querySelectorAll('.progress-step-number').forEach(function(number){\n    number.addEventListener('keydown',function(e){\n      if(e.key==='Enter'||e.key===' '){\n        e.preventDefault();\n        number.closest('.progress-step')?.click();\n      }\n    });\n  });\n})();\n</script>\n'''
    s=s.replace('</body>',js+'</body>',1)

p.write_text(s)
