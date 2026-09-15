# -*- coding: utf-8 -*-
"""리라이트 배치가 함께 쓰는 헬퍼."""
import json, sys
from pathlib import Path


def lines(block):
    """코드 블록을 줄 배열로 만든다.

    앞의 빈 줄은 걷어내고, 끝은 개행 하나만 지운다. 블록이 빈 줄로 끝나면
    (중괄호를 지운 자리처럼) 그 빈 줄을 살려 before 와 after 의 줄 수를 맞춘다.
    """
    block = block.lstrip('\n')
    if block.endswith('\n\n'):
        return block[:-1].rstrip('\n').split('\n') + ['']
    return block.rstrip('\n').split('\n')


def make(episodes):
    """ep(...) 호출을 모아 배치 dict 를 만드는 수집기를 돌려준다."""
    def ep(code, filename, message, before, after, focus):
        episodes[code] = dict(filename=filename, message=message, focus_line=focus,
                              before=lines(before), after=lines(after))
    return ep


def write(episodes, default_out):
    out = Path(sys.argv[1] if len(sys.argv) > 1 else default_out)
    out.write_text(json.dumps(episodes, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    print(f'{len(episodes)}편 -> {out}')
