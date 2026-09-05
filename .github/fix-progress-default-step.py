from pathlib import Path

p=Path('index.html')
s=p.read_text()

old="steps.forEach((btn,index)=>{const el=targets[btn.dataset.key]; if(el&&el.getBoundingClientRect().top<=offset)active=index;});"
new="steps.forEach((btn,index)=>{const el=targets[btn.dataset.key]; if(el && el.offsetParent !== null && el.getBoundingClientRect().top<=offset) active=index;});"

if old in s:
    s=s.replace(old,new,1)
elif new not in s:
    raise SystemExit('Progress scroll logic not found')

# Make sure a fresh form always starts visually on Step 1 when the page is at the top.
old2="setActive(0); updateFromScroll();"
new2="setActive(0); if(window.scrollY > 20) updateFromScroll();"
if old2 in s:
    s=s.replace(old2,new2,1)

p.write_text(s)
