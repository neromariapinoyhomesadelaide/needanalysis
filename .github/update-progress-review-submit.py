from pathlib import Path
import re

p=Path('index.html')
s=p.read_text()

# Remove Additional Information from the progress navigation only.
s,n=re.subn(r'\s*<button[^>]*class="progress-step[^>]*data-step="[^"]*"[^>]*data-key="[^"]*"[^>]*>Additional Information</button>','',s,count=1,flags=re.I)
if n==0:
    # tolerate implementations where attributes are ordered differently
    s=re.sub(r'\s*<button[^>]*class="progress-step[^>]*>\s*Additional Information\s*</button>','',s,count=1,flags=re.I)

# Add Review and Submit as the final progress step if absent.
if not re.search(r'class="progress-step[^>]*>\s*Review\s*&(?:amp;)?\s*Submit\s*</button>',s,re.I):
    nav_end='  </nav>\n</div>'
    btn='    <button type="button" class="progress-step" data-step="6" data-key="review">Review &amp; Submit</button>\n'
    if nav_end not in s: raise SystemExit('Progress nav end not found')
    s=s.replace(nav_end,btn+nav_end,1)

# Renumber all progress buttons and make the grid responsive to the new total.
def renumber(m, counter=[0]):
    counter[0]+=1
    tag=m.group(0)
    if 'data-step=' in tag:
        tag=re.sub(r'data-step="[^"]*"',f'data-step="{counter[0]}"',tag,1)
    else:
        tag=tag.replace('<button','<button data-step="%d"'%counter[0],1)
    return tag
s=re.sub(r'<button[^>]*class="progress-step[^>]*>',renumber,s)
s=re.sub(r'\.progress-nav\{max-width:1100px;margin:0 auto;display:grid;grid-template-columns:repeat\(\d+,1fr\);', '.progress-nav{max-width:1100px;margin:0 auto;display:grid;grid-template-columns:repeat(6,1fr);',s,count=1)

# Extend the existing progress script with Review & Submit target/label.
s=s.replace("documents:'Supporting Documents'};","documents:'Supporting Documents',review:'Review & Submit'};",1)
s=s.replace('return {personal,employment,income,assets,documents};',"const review=document.getElementById('reviewOverlay')||document.getElementById('reviewModal')||document.querySelector('[id*=\"review\" i]')||Array.from(document.querySelectorAll('button')).find(b=>/review|submit/i.test(b.textContent||''))?.closest('.card')||Array.from(document.querySelectorAll('h2,h3')).find(h=>/review|submit/i.test(h.textContent||''))?.closest('.card');\n    return {personal,employment,income,assets,documents,review};",1)

# Ensure the mobile current label starts with the correct total.
s=re.sub(r'Step 1 of \d+ — Personal Details','Step 1 of 6 — Personal Details',s,count=1)

p.write_text(s)
