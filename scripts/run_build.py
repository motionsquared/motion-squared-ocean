"""Launch PowerShell with a normalized Windows environment (Path/PATH aliases)."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import ctypes

shell = shutil.which('pwsh') or shutil.which('powershell')
if not shell:
    raise SystemExit('PowerShell is required')
env = dict(os.environ)
env['MSBUILDDISABLENODEREUSE'] = '1'
if os.name == 'nt':
    # Keep child compiler crashes in the build log instead of opening Windows dialogs.
    ctypes.windll.kernel32.SetErrorMode(0x0001 | 0x0002 | 0x8000)
raise SystemExit(subprocess.call(
    [shell, '-NoProfile', '-File', str(Path(__file__).with_name('Build-Windows.ps1')),
     *sys.argv[1:]], env=env))
