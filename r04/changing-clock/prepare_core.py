"""Record the copied own-research numerical helper before any new results."""
from pathlib import Path
import hashlib,json
here=Path(__file__).resolve().parent
source=here.parents[1]/'r03-analysis/hopper-clock/check_clock_contract.py'
text=source.read_text(encoding='utf-8').split('def main():')[0]
old='assert 0<v.numerator<10**12 and 0<v.denominator<10**12'
new='assert 0<v.numerator<10**50 and 0<v.denominator<10**50'
assert text.count(old)==1
dest=here/'audit_core.py';assert not dest.exists()
dest.write_text(text.replace(old,new),encoding='utf-8')
(here/'CORE_PROVENANCE.json').write_text(json.dumps(dict(
 source='r03-analysis/hopper-clock/check_clock_contract.py',
 source_sha256=hashlib.sha256(source.read_bytes()).hexdigest(),
 new_core_sha256=hashlib.sha256(dest.read_bytes()).hexdigest(),
 changes=['Exclude original main function; retain outward log/BF/Floyd/audit functions unchanged.',
          'Expand the asserted positive rational numerator/denominator size domain from12 to50 digits; independent exact-series validation remains mandatory.'],
 scientific_scope='No original R03 source, outputs or numerical values are modified.'),indent=2)+'\n',encoding='utf-8')
