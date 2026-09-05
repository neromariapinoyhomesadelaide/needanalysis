from pathlib import Path
import re

p = Path('index.html')
s = p.read_text()

# 1) Move the existing + Add Applicant 2 button to directly after Supporting Documents.
if 'id="applicant2AddAfterDocuments"' not in s:
    m = re.search(r'<button\b[^>]*id="addApplicant2Btn"[^>]*>.*?</button>', s, flags=re.S)
    if not m:
        raise SystemExit('Add Applicant 2 button not found')
    button = m.group(0)
    s = s[:m.start()] + s[m.end():]

    marker = '<div class="card"><h2>Disclaimer</h2>'
    if marker not in s:
        raise SystemExit('Disclaimer marker not found')
    moved = (
        '<div id="applicant2AddAfterDocuments" class="applicant2-add-wrap">'
        + button +
        '</div>\n'
    )
    s = s.replace(marker, moved + marker, 1)

# 2) Add styling for the moved Applicant 2 control and applicant badge.
if '.applicant2-add-wrap{' not in s:
    css = '''
.applicant2-add-wrap{max-width:1100px;margin:-4px auto 20px;padding:0;display:flex;justify-content:flex-end}
.applicant2-add-wrap button{min-width:190px}
.progress-applicant-row{max-width:1100px;margin:0 auto 6px;display:flex;align-items:center;justify-content:space-between;gap:10px}
.progress-applicant{display:inline-flex;align-items:center;gap:6px;padding:5px 10px;border-radius:999px;background:#e8eef8;color:var(--navy);font-size:12px;font-weight:800;white-space:nowrap}
.progress-applicant::before{content:'';width:8px;height:8px;border-radius:50%;background:var(--blue)}
@media(max-width:700px){.applicant2-add-wrap{padding:0 16px}.applicant2-add-wrap button{width:100%}.progress-applicant-row{margin-bottom:4px}.progress-applicant{font-size:11px;padding:4px 8px}}
'''
    s = s.replace('</style>', css + '\n</style>', 1)

# 3) Add Applicant 1 / Applicant 2 indicator to the sticky progress bar.
if 'id="progressApplicant"' not in s:
    nav_marker = '<div class="progress-current" id="progressCurrent">'
    if nav_marker not in s:
        raise SystemExit('Progress current marker not found')
    row = '<div class="progress-applicant-row"><div class="progress-applicant" id="progressApplicant">Applicant 1</div></div>\n  '
    s = s.replace(nav_marker, row + nav_marker, 1)

# 4) Add lightweight scroll logic that updates which applicant is active.
if 'function updateProgressApplicant()' not in s:
    js = '''
<script>
(function(){
  function updateProgressApplicant(){
    const badge = document.getElementById('progressApplicant');
    if (!badge) return;
    const nav = document.getElementById('formProgressNav');
    const cutoff = (nav?.offsetHeight || 0) + 48;
    const candidates = Array.from(document.querySelectorAll('h2,h3,.asset>strong'))
      .filter(el => el.offsetParent !== null)
      .filter(el => /Applicant\s+[12]/i.test(el.textContent || ''));

    let applicant = 'Applicant 1';
    candidates.forEach(el => {
      if (el.getBoundingClientRect().top <= cutoff) {
        const match = (el.textContent || '').match(/Applicant\s+[12]/i);
        if (match) applicant = match[0].replace(/applicant/i, 'Applicant');
      }
    });

    // When Applicant 2 is not active/visible, default to Applicant 1.
    const a2Card = document.getElementById('applicant2Card');
    if (applicant === 'Applicant 2' && a2Card && a2Card.style.display === 'none') applicant = 'Applicant 1';
    badge.textContent = applicant;
  }

  window.addEventListener('scroll', updateProgressApplicant, {passive:true});
  window.addEventListener('resize', updateProgressApplicant);
  document.getElementById('addApplicant2Btn')?.addEventListener('click', () => setTimeout(updateProgressApplicant, 0));
  updateProgressApplicant();
})();
</script>
'''
    if '</body>' not in s:
        raise SystemExit('Body marker not found')
    s = s.replace('</body>', js + '\n</body>', 1)

p.write_text(s)
