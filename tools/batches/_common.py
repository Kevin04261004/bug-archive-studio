# -*- coding: utf-8 -*-
"""리라이트 배치가 함께 쓰는 헬퍼."""
import json, sys
from pathlib import Path


def lines(block):
    """코드 블록을 줄 배열로 만든다.

    앞뒤로 개행을 하나씩만 지운다. 삼중 따옴표 다음 줄바꿈과 닫기 전 줄바꿈만
    걷어내므로, 첫 줄이나 마지막 줄을 비워 둔 경우(중괄호나 지시문을 지운 자리)
    그 빈 줄이 살아남아 before 와 after 의 줄 수가 맞는다.
    """
    if block.startswith('\n'):
        block = block[1:]
    if block.endswith('\n'):
        block = block[:-1]
    return block.split('\n')


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
