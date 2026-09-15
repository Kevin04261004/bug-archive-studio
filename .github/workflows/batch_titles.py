"""Write the title sheet that ships inside a batch archive.

YouTube Studio fills each title from the file name on upload, but everything else —
description, tags, playlist — is typed once in its bulk editor. This sheet is what you
paste from: one row per video, in the order they were rendered, opening in a spreadsheet.
"""
import csv, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TITLE = 'C# QUIZ - ERROR {}'.format


def rows(codes):
    for code in codes:
        cfg = json.loads((ROOT / 'episodes' / f'{code}.json').read_text(encoding='utf-8-sig'))
        title = TITLE(code)
        yield [f'{title}.mp4', title, code, cfg.get('filename', 'Player.cs'), cfg['message']]


def main(listing, out):
    codes = Path(listing).read_text(encoding='utf-8').split()
    with open(out, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, delimiter='\t', lineterminator='\n')
        w.writerow(['file', 'title', 'error', 'source', 'compiler message'])
        w.writerows(rows(codes))
    print(f'{len(codes)} titles -> {out}')


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
