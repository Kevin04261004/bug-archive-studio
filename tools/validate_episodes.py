#!/usr/bin/env python3
"""에피소드 JSON을 렌더러 한계와 작성 기준(EPISODE_STYLE.md)에 맞춰 검사한다.

렌더러가 거부하는 것(폭, 단일 변경, 메시지 길이)은 error,
작성 기준에서 벗어난 것(줄 수, 실험실 코드 냄새)은 warn 으로 보고한다.
"""
import argparse, difflib, json, re, sys
from pathlib import Path
from PIL import ImageFont

ROOT = Path(__file__).resolve().parent.parent
MONO = str(ROOT / 'fonts/DejaVuSansMono.ttf')
CODE_WIDTH = 704          # render.py: fit(line, 40, 704, True, 26)
MIN_CODE_SIZE = 26        # 이 아래로 떨어지면 render.py 가 종료한다
GOOD_CODE_SIZE = 29       # 29px 밑으로 떨어지면 폰에서 눈에 띄게 작아진다
MIN_LINES, MAX_LINES = 10, 20
HOST_TOP = 1450          # 진행자 스프라이트가 시작하는 자리. 진단 줄이 여기를 넘으면 겹친다

_cache = {}
def mono(size):
    if size not in _cache:
        _cache[size] = ImageFont.truetype(MONO, size)
    return _cache[size]

def code_size(lines):
    """render.py 와 같은 방식으로 이 코드가 렌더될 글자 크기를 구한다."""
    best = 40
    for line in lines:
        for size in range(40, MIN_CODE_SIZE - 1, -1):
            if mono(size).getlength(line) <= CODE_WIDTH:
                best = min(best, size)
                break
        else:
            return 0      # 26px 에서도 안 들어감
    return best

def layout(lines):
    """render.py 와 같은 식으로 코드 카드 아래 진단 줄(bar_y)이 어디에 놓이는지 계산한다."""
    count = len(lines)
    visible = min(count, 28)
    cs = min(min(code_size([l]) or 0 for l in lines), int(980 / visible) - 5)
    if cs < MIN_CODE_SIZE:
        return cs, None
    step = min(58, cs + 9)
    card_bottom = max(690, 350 + (visible - 1) * step + 54)
    return cs, card_bottom + 106


def message_fits(message, maxsize, width):
    """render.py 의 wrapped_message 와 같은 판정: 두 줄 안에 22px 이상으로 접히는가."""
    for size in range(maxsize, 22, -1):
        lines, line = [], ""
        for word in message.split():
            candidate = (line + " " + word).strip()
            if mono(size).getlength(candidate) <= width:
                line = candidate
            else:
                if line:
                    lines.append(line)
                line = word
        if line:
            lines.append(line)
        if len(lines) <= 2 and all(mono(size).getlength(z) <= width for z in lines):
            return True
    return False

LAB_PATTERNS = [
    (re.compile(r'\bclass\s+[A-Z]\b'),            '한 글자 클래스 이름'),
    (re.compile(r'\b(?:void|int|bool|string|float)\s+[A-Z]\s*\('), '한 글자 메서드 이름'),
    (re.compile(r'\b(?:int|float|string|bool|var|double)\s+[a-z]\s*[=;,)]'), '한 글자 변수 이름'),
    (re.compile(r'\b(?:foo|bar|baz|qux)\b'),      'foo/bar 자리표시자'),
    (re.compile(r'\bMyClass\b|\bMyMethod\b'),     'MyClass/MyMethod 자리표시자'),
]

def changed_rows(before, after):
    return [i for i in range(max(len(before), len(after)))
            if (before[i] if i < len(before) else None) != (after[i] if i < len(after) else None)]

def check(path):
    errors, warns = [], []
    try:
        cfg = json.loads(path.read_text(encoding='utf-8-sig'))
    except Exception as exc:
        return [f'JSON 파싱 실패: {exc}'], []

    for key in ('error_code', 'message', 'before', 'after'):
        if key not in cfg:
            errors.append(f'필드 누락: {key}')
    if errors:
        return errors, warns

    before = [s.replace('\t', '    ') for s in cfg['before']]
    after = [s.replace('\t', '    ') for s in cfg['after']]

    if len(before) != len(after):
        errors.append(f'before {len(before)}줄 / after {len(after)}줄 — 줄 수가 다르면 diff 가 번진다')

    rows = changed_rows(before, after)
    if not rows:
        errors.append('before 와 after 가 같다')
    elif len(rows) > 1:
        errors.append(f'{len(rows)}줄이 바뀐다 (줄 {[r + 1 for r in rows]}) — 수정은 한 곳만')

    if rows:
        focus = cfg.get('focus_line')
        if focus is None:
            warns.append(f'focus_line 없음 (바뀐 줄은 {rows[0] + 1})')
        elif focus != rows[0] + 1:
            errors.append(f'focus_line={focus} 인데 실제로 바뀐 줄은 {rows[0] + 1}')

    size = code_size(before + after)
    if size == 0:
        worst = max(before + after, key=lambda s: mono(MIN_CODE_SIZE).getlength(s))
        errors.append(f'26px 에서도 화면 폭을 넘는 줄: {worst.strip()!r} ({len(worst)}자)')
    elif size < GOOD_CODE_SIZE:
        worst = max(before + after, key=lambda s: mono(size).getlength(s))
        warns.append(f'코드가 {size}px 로 줄어든다 — 가장 긴 줄 {len(worst)}자: {worst.strip()!r}')

    if not message_fits(cfg['message'], 29, 960 - 155 - 56):
        errors.append(f'오류 메시지가 진단 줄 두 줄에 안 들어간다 ({len(cfg["message"])}자)')
    elif not message_fits(cfg['message'], 32, 650):
        errors.append(f'오류 메시지가 도감 카드 두 줄에 안 들어간다 ({len(cfg["message"])}자)')

    cs_layout, bar_y = layout(before)
    if bar_y is None:
        pass                      # 폭 문제는 위에서 이미 보고했다
    elif bar_y > HOST_TOP:
        errors.append(f'{len(before)}줄이면 진단 줄이 y={int(bar_y)} 로 내려가 진행자를 덮는다 (한계 {HOST_TOP})')
    if len(before) > 28:
        errors.append(f'{len(before)}줄 — 28줄까지만 화면에 보인다 (visible=min(count,28))')

    n = len(before)
    if n < MIN_LINES:
        warns.append(f'{n}줄 — 맥락이 부족하다 (기준 {MIN_LINES}–{MAX_LINES}줄)')
    elif n > MAX_LINES:
        warns.append(f'{n}줄 — 훑다가 넘긴다 (기준 {MIN_LINES}–{MAX_LINES}줄)')

    body = re.sub(r'for \([^)]*\)', 'for (...)', '\n'.join(before))
    for pattern, label in LAB_PATTERNS:
        hit = pattern.search(body)
        if hit:
            warns.append(f'실험실 코드 냄새 — {label}: {hit.group()!r}')

    bug = (path.parent / cfg.get('bug', '../assets/CS1002.png')).resolve()
    if not bug.is_file():
        warns.append(f'버그 PNG 없음: {bug.name}')

    return errors, warns

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('paths', nargs='*', help='검사할 JSON (생략하면 episodes/ 전체)')
    ap.add_argument('--strict', action='store_true', help='경고도 실패로 취급')
    ap.add_argument('--quiet', action='store_true', help='요약만 출력')
    args = ap.parse_args()

    paths = [Path(p) for p in args.paths] or sorted(
        p for p in (ROOT / 'episodes').glob('*.json') if p.name != 'index.json')

    bad = warned = 0
    for path in paths:
        errors, warns = check(path)
        if errors:
            bad += 1
        if warns:
            warned += 1
        if (errors or warns) and not args.quiet:
            print(f'{path.name}')
            for e in errors:
                print(f'  ERROR {e}')
            for w in warns:
                print(f'  warn  {w}')

    print(f'\n{len(paths)}개 검사 — 오류 {bad}개, 경고 {warned}개')
    return 1 if bad or (args.strict and warned) else 0

if __name__ == '__main__':
    sys.exit(main())
