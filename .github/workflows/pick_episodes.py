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


def asked_for(wanted):
    """Read the workflow_dispatch input: 'all', one code, or a whole selection.

    The studio dispatches a batch as one space-separated list so a picker of thirty
    episodes waits for a single runner instead of queueing thirty of them.
    Order follows episodes/, not the order they were typed, so a batch renders
    predictably. Codes with no episode file are reported rather than failing the run."""
    have = known()
    if wanted in {'', 'all'}:
        return have
    asked = {c.upper() for c in re.split(r'[\s,]+', wanted) if c}
    for code in sorted(asked - set(have)):
        print(f'{code} is not an episode in episodes/, so it is skipped.', file=sys.stderr)
    return [c for c in have if c in asked]


if os.environ.get('EVENT') == 'workflow_dispatch':
    codes = asked_for((os.environ.get('WANTED') or 'all').strip())
else:
    codes = changed(os.environ.get('BEFORE', ''), os.environ.get('AFTER', 'HEAD'))

ready = [c for c in codes if has_bug(c)]
for code in codes:
    if code not in ready:
        print(f'{code} has no bug PNG yet, so it is not rendered. Add assets/{code}.png.', file=sys.stderr)
print('codes=' + ' '.join(ready))
