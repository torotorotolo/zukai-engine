# -*- coding: utf-8 -*-
"""⑤b が「このカットに当てる絵が本当に在るか」を、台帳3冊から**語で引く**。

■ なぜ `nasa_probe list` ではなくこれか
  `list` は②が組んだ**欄（slot）**の単位でしか出せない。⑤bが知りたいのは
  「c604 のリチウムハイドロキシドの缶は在るか」のような**カット単位の問い**で、
  欄は10しか無い。欄を増やすより、**説明文を直接引いて1行ずつ読む**ほうが速くて正確。

■ ⚠️ これは絞る道具であって選ぶ道具ではない
  出た行は必ず人が読む。「語が説明文に出てくる」だけの取り違えは残る
  （②の `debris_field` `reentry` `test` `orbit` の4欄が実際にそうだった）。
  → [[feedback-inventory-is-not-usable-material]]

■ 権利
  `center` と `creator` を必ず出す。NASA でも契約企業・ESA/JAXA 提供の例外がある。

    python qa_out/ep8_pick.py "lithium hydroxide"
    python qa_out/ep8_pick.py "atlantis" --year 2003 --minw 1280
    python qa_out/ep8_pick.py "mission evaluation room|mer " --chars 200
"""
from __future__ import annotations

import argparse
import io
import json
import re
import sys
from pathlib import Path

def _utf8_stdout():
    """⚠️ **import されたときに包まない。**包むと、呼び出し側が自分で包んだ
    `TextIOWrapper` が回収された拍子に下の buffer ごと閉じ、
    `ValueError: I/O operation on closed file` で落ちる（2026-09-14 に実際に踏んだ）。"""
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


HERE = Path(__file__).resolve().parents[1]
LEDGERS = [
    ('nasalib', 'analytics/materials/ep8_nasalib.json', 'ep8'),
    ('ia', 'analytics/materials/ep8_nasa.json', 'ep8ia'),
    ('ia2', 'analytics/materials/ep8_ia2.json', 'ep8ia2'),
]


def load():
    """3冊を読んで `nasa_id` で潰す。⚠️ 潰さないと同じ物を二度数える（②で実際に起きた）。"""
    seen, out = {}, []
    for tag, path, key in LEDGERS:
        d = json.loads((HERE / path).read_text(encoding='utf-8'))[key]
        for it in d['items']:
            nid = it['nasa_id']
            if nid in seen:
                continue
            seen[nid] = tag
            out.append(dict(it, _db=tag))
    return out


def caption(it):
    """題名が資産IDそのものの件が7割あるので、そのときだけ説明文を見る（②と同じ扱い）。"""
    t = (it.get('title') or '').strip()
    d = (it.get('desc_head') or '').strip()
    if re.fullmatch(r'[A-Za-z]{2,4}[-0-9a-zA-Z_.]{4,}', t) or not t:
        return f'{t} — {d}' if d else t
    return f'{t} ｜{d}' if d else t


def main():
    _utf8_stdout()
    ap = argparse.ArgumentParser()
    ap.add_argument('pattern', help='正規表現（説明文と題名の両方に当てる・大小無視）')
    ap.add_argument('--year', type=int, default=0)
    ap.add_argument('--minw', type=int, default=0)
    ap.add_argument('--chars', type=int, default=130)
    ap.add_argument('--limit', type=int, default=40)
    ap.add_argument('--vid', action='store_true', help='動く映像（HSF-mov-*）だけ')
    a = ap.parse_args()

    rx = re.compile(a.pattern, re.I)
    items = load()
    hits = []
    for it in items:
        cap = caption(it)
        if not rx.search(cap):
            continue
        if a.year and it.get('year') != a.year:
            continue
        if a.minw and (it.get('w') or 0) < a.minw:
            continue
        is_vid = it['nasa_id'].startswith('HSF-mov')
        if a.vid != is_vid and a.vid:
            continue
        hits.append((it, cap))

    print(f'当たり {len(hits)} 件 / 台帳 {len(items)} 件'
          f'（year={a.year or "指定なし"} minw={a.minw or "指定なし"}）\n')
    for it, cap in hits[:a.limit]:
        w, h = it.get('w'), it.get('h')
        dim = f'{w}x{h}' if w else '未測'
        who = it.get('creator') or it.get('center') or ''
        print(f"[{it['_db']:<7}] {it['nasa_id']:<24} {it.get('date_created','')[:10]:<10} "
              f"{dim:<10} {who[:26]}")
        print(f"          {cap[:a.chars]}")
    if len(hits) > a.limit:
        print(f'\n… ほか {len(hits) - a.limit} 件（--limit を上げる）')


if __name__ == '__main__':
    main()
