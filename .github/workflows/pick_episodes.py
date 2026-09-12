"""Print the episode codes this run should render, as a GITHUB_OUTPUT line."""
import os, re, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EPISODES = ROOT / 'episodes'
EMPTY = '0' * 40


def known():
    """Episodes render.py accepts: one CS0000.json per error code."""
    return sorted(p.stem for p in EPISODES.glob('*.json') if re.fullmatch(r'CS\d{4}', p.stem))


def changed(before, after):
    if not before or before == EMPTY:
        return known()
    files = subprocess.run(['git', 'diff', '--name-only', before, after],
                           cwd=ROOT, capture_output=True, text=True, check=True).stdout.split()
    if 'render.py' in files:
        return known()
    codes, have = set(), set(known())
    for name in files:
        path = Path(name)
        if path.parent.name in {'episodes', 'assets'} and path.stem in have:
            codes.add(path.stem)
    return sorted(codes)


if os.environ.get('EVENT') == 'workflow_dispatch':
    wanted = (os.environ.get('WANTED') or 'all').strip()
    codes = known() if wanted in {'', 'all'} else [c for c in known() if c == wanted]
else:
    codes = changed(os.environ.get('BEFORE', ''), os.environ.get('AFTER', 'HEAD'))

print('codes=' + ' '.join(codes))
