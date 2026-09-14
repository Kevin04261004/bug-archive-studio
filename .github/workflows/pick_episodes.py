"""Print the episode codes this run should render, as a GITHUB_OUTPUT line."""
import json, os, re, subprocess, sys
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


def has_bug(code):
    """An episode waiting for its bug PNG is skipped, not failed: the PNG lands in a later commit.

    A truncated or otherwise unreadable PNG counts as missing too. Rendering it would fail the
    whole run, which costs Actions minutes and blocks the episode list refresh for everyone else."""
    try:
        cfg = json.loads((EPISODES / f'{code}.json').read_text(encoding='utf-8-sig'))
    except Exception:
        return False
    bug = cfg.get('bug') if isinstance(cfg.get('bug'), str) else f'../assets/{code}.png'
    path = (EPISODES / bug).resolve()
    if not path.is_file():
        return False
    try:
        from PIL import Image
        Image.open(path).convert('RGBA').load()
    except Exception as e:
        print(f'{code}: {path.name} cannot be read ({e}). Regenerate it.', file=sys.stderr)
        return False
    return True


if os.environ.get('EVENT') == 'workflow_dispatch':
    wanted = (os.environ.get('WANTED') or 'all').strip()
    codes = known() if wanted in {'', 'all'} else [c for c in known() if c == wanted]
else:
    codes = changed(os.environ.get('BEFORE', ''), os.environ.get('AFTER', 'HEAD'))

ready = [c for c in codes if has_bug(c)]
for code in codes:
    if code not in ready:
        print(f'{code} has no bug PNG yet, so it is not rendered. Add assets/{code}.png.', file=sys.stderr)
print('codes=' + ' '.join(ready))
