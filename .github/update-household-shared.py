from pathlib import Path
import re

p=Path('index.html')
s=p.read_text()

# Remove the old Additional Information card from the actual form.
s=re.sub(
    r'<div class="card"><h2>Additional Information</h2>.*?</div></div>\s*',
    '',
    s,
    count=1,
    flags=re.S|re.I
)
# Fallback for the older single-question card without an h2 match.
s=re.sub(
    r'<div class="card">(?:(?!<div class="card">).)*?<label>Anything else you would like us to know\?</label>.*?<textarea[^>]*name="additional_info"[^>]*>.*?</textarea>.*?</div></div>\s*',
    '',
    s,
    count=1,
    flags=re.S|re.I
)

# Add the shared household section once, immediately before Disclaimer.
if 'id="householdSharedSection"' not in s:
    household='''<div class="card" id="householdSharedSection"><h2>Household / Shared Information</h2><div class="content">
<p class="note" style="font-size:13px;margin-top:0">Complete these details once for the household. Use this section for information shared by Applicant 1 and Applicant 2.</p>

<h3>Dependants</h3>
<div class="grid3">
<div><label>Number of Dependants</label><input name="household_dependants_count" type="number" min="0" placeholder="0" /></div>
<div><label>Dependants' Ages</label><input name="household_dependants_ages" placeholder="e.g. 4, 8" /></div>
<div><label>Childcare / School Costs (monthly)</label><input name="household_childcare_school_costs" type="number" min="0" step="0.01" placeholder="$" /></div>
</div>

<h3>Household Expenses <span class="note">(monthly)</span></h3>
<div class="grid3">
<div><label>Rent / Board</label><input name="household_rent_board" type="number" min="0" step="0.01" placeholder="$" /></div>
<div><label>Groceries</label><input name="household_groceries" type="number" min="0" step="0.01" placeholder="$" /></div>
<div><label>Utilities</label><input name="household_utilities" type="number" min="0" step="0.01" placeholder="$" /></div>
<div><label>Transport</label><input name="household_transport" type="number" min="0" step="0.01" placeholder="$" /></div>
<div><label>Insurance</label><input name="household_insurance" type="number" min="0" step="0.01" placeholder="$" /></div>
<div><label>Other Regular Household Expenses</label><input name="household_other_expenses" type="number" min="0" step="0.01" placeholder="$" /></div>
</div>

<h3>Property Goals</h3>
<div class="grid3">
<div><label>Purpose</label><select name="household_property_purpose"><option value="">Select</option><option>First Home</option><option>Owner Occupied</option><option>Investment</option><option>Refinance</option></select></div>
<div><label>Preferred Suburbs / Areas</label><input name="household_preferred_suburbs" placeholder="e.g. Adelaide southern suburbs" /></div>
<div><label>Property Type</label><select name="household_property_type"><option value="">Select</option><option>House & Land</option><option>Established House</option><option>Townhouse</option><option>Apartment / Unit</option><option>Land Only</option><option>Other</option></select></div>
<div><label>Bedrooms</label><input name="household_bedrooms" type="number" min="0" /></div>
<div><label>Bathrooms</label><input name="household_bathrooms" type="number" min="0" /></div>
<div><label>Garage Spaces</label><input name="household_garage" type="number" min="0" /></div>
<div><label>Minimum Land Size (sqm)</label><input name="household_land_size" type="number" min="0" /></div>
<div><label>Target Budget</label><input name="household_target_budget" type="number" min="0" step="1000" placeholder="$" /></div>
<div><label>Preferred Timeframe</label><select name="household_timeframe"><option value="">Select</option><option>ASAP</option><option>0–3 months</option><option>3–6 months</option><option>6–12 months</option><option>12+ months</option></select></div>
</div>

<h3>Joint Assets</h3>
<div class="grid3">
<div><label>Joint Savings / Cash</label><input name="household_joint_savings" type="number" min="0" step="0.01" placeholder="$" /></div>
<div><label>Joint Property / Investment Value</label><input name="household_joint_property_value" type="number" min="0" step="0.01" placeholder="$" /></div>
<div><label>Other Joint Assets</label><input name="household_joint_other_assets" type="number" min="0" step="0.01" placeholder="$" /></div>
</div>

<h3>Joint Liabilities</h3>
<div class="grid3">
<div><label>Joint Home Loan Balance</label><input name="household_joint_home_loan_balance" type="number" min="0" step="0.01" placeholder="$" /></div>
<div><label>Joint Home Loan Repayment (monthly)</label><input name="household_joint_home_loan_repayment" type="number" min="0" step="0.01" placeholder="$" /></div>
<div><label>Joint Personal Loan Balance</label><input name="household_joint_personal_loan_balance" type="number" min="0" step="0.01" placeholder="$" /></div>
<div><label>Joint Personal Loan Repayment (monthly)</label><input name="household_joint_personal_loan_repayment" type="number" min="0" step="0.01" placeholder="$" /></div>
<div><label>Joint Credit Card Limit</label><input name="household_joint_credit_limit" type="number" min="0" step="0.01" placeholder="$" /></div>
<div><label>Joint Credit Card Balance</label><input name="household_joint_credit_balance" type="number" min="0" step="0.01" placeholder="$" /></div>
<div><label>BNPL / Other Joint Debt Balance</label><input name="household_joint_other_debt" type="number" min="0" step="0.01" placeholder="$" /></div>
</div>

<h3>Deposit / Funds Available</h3>
<div class="grid3">
<div><label>Savings Available for Deposit</label><input name="household_deposit_savings" type="number" min="0" step="0.01" placeholder="$" /></div>
<div><label>Gifted Funds</label><input name="household_gifted_funds" type="number" min="0" step="0.01" placeholder="$" /></div>
<div><label>First Home Super Saver (FHSS)</label><input name="household_fhss" type="number" min="0" step="0.01" placeholder="$" /></div>
<div><label>Expected Grants / Incentives</label><input name="household_grants" type="number" min="0" step="0.01" placeholder="$" /></div>
<div><label>Other Available Funds</label><input name="household_other_funds" type="number" min="0" step="0.01" placeholder="$" /></div>
</div>
</div></div>
'''
    marker='<div class="card"><h2>Disclaimer</h2>'
    if marker not in s: raise SystemExit('Disclaimer marker not found')
    s=s.replace(marker,household+'\n'+marker,1)

# Add Household / Shared Information to progress navigation before Review & Submit.
if 'data-key="household"' not in s:
    review_btn=re.search(r'<button[^>]*class="progress-step[^>]*data-key="review"[^>]*>.*?</button>',s,re.S|re.I)
    if not review_btn: raise SystemExit('Review progress button not found')
    household_btn='<button type="button" class="progress-step" data-step="6" data-key="household">Household / Shared</button>\n    '
    s=s[:review_btn.start()]+household_btn+s[review_btn.start():]

# Renumber all progress steps and set a seven-column desktop grid.
def renumber(m):
    renumber.count+=1
    return re.sub(r'data-step="[^"]*"',f'data-step="{renumber.count}"',m.group(0),count=1)
renumber.count=0
s=re.sub(r'<button[^>]*class="progress-step[^>]*>',renumber,s)
s=re.sub(r'(\.progress-nav\{max-width:1100px;margin:0 auto;display:grid;grid-template-columns:repeat\()\d+(,1fr\);)',r'\g<1>7\2',s,count=1)
s=re.sub(r'Step 1 of \d+ — Personal Details','Step 1 of 7 — Personal Details',s,count=1)

# Extend the existing progress map with the Household target and label.
if "household:'Household / Shared Information'" not in s:
    s=s.replace("documents:'Supporting Documents',review:'Review & Submit'","documents:'Supporting Documents',household:'Household / Shared Information',review:'Review & Submit'",1)

if 'const household=document.getElementById(\'householdSharedSection\')' not in s:
    s=s.replace(
        "const review=document.getElementById('reviewOverlay')",
        "const household=document.getElementById('householdSharedSection');\n    const review=document.getElementById('reviewOverlay')",
        1
    )
s=s.replace('return {personal,employment,income,assets,documents,review};','return {personal,employment,income,assets,documents,household,review};',1)

# Update applicant badge so shared/review sections no longer appear as Applicant 1/2.
if 'householdSharedSection' in s and 'progressApplicant' in s and 'Shared Household' not in s:
    extra='''\n<script>\n(function(){\n  function updateHouseholdProgressBadge(){\n    const badge=document.getElementById('progressApplicant');\n    const nav=document.getElementById('formProgressNav');\n    const household=document.getElementById('householdSharedSection');\n    if(!badge||!household)return;\n    const cutoff=(nav?.offsetHeight||0)+48;\n    const top=household.getBoundingClientRect().top;\n    const bottom=household.getBoundingClientRect().bottom;\n    if(top<=cutoff&&bottom>cutoff) badge.textContent='Shared Household';\n  }\n  window.addEventListener('scroll',updateHouseholdProgressBadge,{passive:true});\n  window.addEventListener('resize',updateHouseholdProgressBadge);\n  updateHouseholdProgressBadge();\n})();\n</script>\n'''
    s=s.replace('</body>',extra+'</body>',1)

p.write_text(s)
