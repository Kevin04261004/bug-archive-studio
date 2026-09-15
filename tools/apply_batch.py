#!/usr/bin/env python3
"""리라이트 배치를 episodes/*.json 에 적용한다.

배치 파일은 {error_code: {filename, message, before, after, focus_line}} 형태다.
기존 에피소드의 bug 경로와 music 설정은 그대로 유지한다.
"""
import json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EPISODES = ROOT / 'episodes'

def main(batch_path):
    batch = json.loads(Path(batch_path).read_text(encoding='utf-8'))
    for code, new in batch.items():
        path = EPISODES / f'{code}.json'
        old = json.loads(path.read_text(encoding='utf-8-sig')) if path.is_file() else {}
        episode = {
            'error_code': code,
            'message': new['message'],
            'filename': new['filename'],
            'before': new['before'],
            'after': new['after'],
            'focus_line': new['focus_line'],
            'music': old.get('music', 'random'),
            'bug': old.get('bug', f'../assets/{code}.png'),
        }
        path.write_text(json.dumps(episode, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
        print(f'{code}  {len(new["before"])}줄')
    print(f'\n{len(batch)}편 적용')

if __name__ == '__main__':
    main(sys.argv[1])
