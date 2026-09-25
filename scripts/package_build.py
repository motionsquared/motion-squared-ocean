"""Package a private development build together with its corresponding source."""
from pathlib import Path
import hashlib
import json
import zipfile

root=Path(__file__).resolve().parents[1]
binary=root/'build/ClangCL/bin/Release/plugins/motion-squared-ocean/motion-squared-ocean.xdl64'
if not binary.is_file():
    raise SystemExit('Build the plugin first')
report=root/'tests/results/host-smoke.json'
validation=json.loads(report.read_text(encoding='utf-8'))
if validation.get('stage')!='complete' or not all(t['passed'] for t in validation['tests']):
    raise SystemExit('Host regression tests must pass before packaging')
out=root/'dist'
out.mkdir(exist_ok=True)
target=out/'Motion-Squared-Ocean-2026-Windows-DEVELOPMENT.zip'
prefix='motion-squared-ocean/'
with zipfile.ZipFile(target,'w',zipfile.ZIP_DEFLATED) as z:
    z.write(binary,prefix+binary.name)
    for f in (root/'res').rglob('*'):
        if f.is_file():z.write(f,prefix+f.relative_to(root).as_posix())
    for name in ('README.md','INSTALL.md','CHANGELOG.md','COMPATIBILITY.md','CONTRIBUTING.md','THIRD-PARTY-NOTICES.md','VALIDATION.md'):
        z.write(root/name,prefix+name)
    z.write(root/'LICENSE.txt',prefix+'LICENSE.txt')
    for folder in ('source','project','scripts','tests'):
        for f in (root/folder).rglob('*'):
            if f.is_file() and not any(part in ('fixtures','results','__pycache__') for part in f.parts):
                z.write(f,prefix+'corresponding-source/'+f.relative_to(root).as_posix())
    for name in ('README.md','LICENSE.txt','THIRD-PARTY-NOTICES.md','.gitignore','.gitattributes'):
        z.write(root/name,prefix+'corresponding-source/'+name)
    report=root/'tests/results/host-smoke.json'
    if report.exists():z.write(report,prefix+'validation/host-smoke.json')
print(target)
print('SHA256:',hashlib.sha256(target.read_bytes()).hexdigest())
