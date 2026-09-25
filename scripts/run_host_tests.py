"""Run a regression script in an isolated Cinema 4D process."""
import argparse
import os
from pathlib import Path
import subprocess
import json

p=argparse.ArgumentParser()
p.add_argument('--host',default=r'C:\Program Files\Maxon Cinema 4D 2026\c4dpy.exe')
p.add_argument('--modules',required=True,help='Directory containing the test plugin')
p.add_argument('--test',default='host_smoke.py',choices=['host_smoke.py','inspect_scene.py'])
p.add_argument('--report',default='scene-inventory-with-plugin.json')
a=p.parse_args()
root=Path(__file__).resolve().parents[1]
env=dict(os.environ)
env['g_additionalModulePath']=str(Path(a.modules).resolve())
env['MS_OCEAN_REPORT']=a.report
result=subprocess.run([a.host,str(root/'tests'/a.test)],env=env)
if result.returncode:
    raise SystemExit(result.returncode)
report_path=root/'tests/results'/('host-smoke.json' if a.test=='host_smoke.py' else a.report)
report=json.loads(report_path.read_text(encoding='utf-8'))
raise SystemExit(0 if report.get('stage')=='complete' and not report.get('error') else 1)
