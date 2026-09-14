# -*- coding: utf-8 -*-
"""8本目（コロンビア号）⑤b の作業表。**台本第2版と narration.json を突き合わせて出す。**

■ なぜ要るか
  216カットを台本の本文で読み直すと 1,500行を毎回抱えることになる。
  ⑤b が要るのは「カットID／画の欄／出典／行数／秒」の5つだけなので、それだけを出す。

■ ⚠️ `qa_out/ep8_firstuse.py` は使わない（台本**第1版**を見ていて、見出しの正規表現に
  `🔧` が無いので第2版の22カットを取り逃がす）。ここは `check_script.parse` と同じ
  正規表現を使い、**出典**の欄だけ足して読む。

■ 検算（fail closed）
  台本のカットID列と `audio/narration.json` の `durations` のキー列が
  **順番も込みで一致**しなければ止まる。片方だけ直したまま⑤bを進める事故を防ぐ。

    python qa_out/ep8_plan.py            # 章ごとの表
    python qa_out/ep8_plan.py --photo    # 「実写」の欄だけ
    python qa_out/ep8_plan.py --fig      # 図の欄だけ（型ごとに数える）
"""
from __future__ import annotations

import io
import json
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

HERE = Path(__file__).resolve().parents[1]
SCRIPT_MD = Path(
    r"C:\Users\konar\Documents\Obsidian Vault\Projects"
    r"\事故検証-コロンビア号-台本第2版-20260914.md")

# `check_script.CUT_RE` と同じ頭。3つめの欄（出典）まで取る
CUT_RE = re.compile(
    r'^\*\*([a-z]{1,2}\d{2,3}(?:-\d)?)\*\*\s*(?:🔧\s*)?／\s*([^／]*)／\s*(.*)$')
SUB_RE = re.compile(r'^>\s?(.*)$')
CH_RE = re.compile(r'^### (.+?)（(\d+)カット）')


def parse():
    cuts, cur, on, ch = [], None, False, '—'
    for raw in SCRIPT_MD.read_text(encoding='utf-8').split('\n'):
        line = raw.rstrip()
        if line.startswith('## 4. 台本'):
            on = True
            continue
        if on and re.match(r'^## \d', line):
            break
        if not on:
            continue
        m = CH_RE.match(line)
        if m:
            ch = m.group(1)
            continue
        m = CUT_RE.match(line)
        if m:
            cur = dict(cid=m.group(1), ch=ch, pic=m.group(2).strip(),
                       src=m.group(3).strip(), lines=[])
            cuts.append(cur)
            continue
        m = SUB_RE.match(line)
        if m and cur is not None and m.group(1).strip():
            cur['lines'].append(m.group(1).strip())
    return cuts


def load_audio():
    d = json.loads((HERE / 'audio' / 'narration.json').read_text(encoding='utf-8'))
    return d['durations'], d['subtitles']


def main():
    cuts = parse()
    dur, sub = load_audio()
    ids = [c['cid'] for c in cuts]
    # 🔴 fail closed：台本と音が1対1でなければ、⑤b は1文字も書いてはいけない
    if ids != list(dur):
        only_md = [i for i in ids if i not in dur]
        only_au = [i for i in dur if i not in ids]
        print(f'🔴 台本 {len(ids)}カット と narration.json {len(dur)}カット が食い違う')
        print(f'   台本だけ: {only_md}')
        print(f'   音だけ  : {only_au}')
        if not only_md and not only_au:
            print('   （並び順が違う）')
        sys.exit(2)

    want_photo = '--photo' in sys.argv
    want_fig = '--fig' in sys.argv
    figs, ch_tot, ch_ph = {}, {}, {}
    cur_ch = None
    for c in cuts:
        pic = c['pic']
        is_ph = pic.startswith('実写')
        ch_tot[c['ch']] = ch_tot.get(c['ch'], 0) + 1
        ch_ph[c['ch']] = ch_ph.get(c['ch'], 0) + (1 if is_ph else 0)
        if not is_ph:
            # 画の欄は3通り：「型名＋説明」／「図＋説明（型は⑤bで決める）」／「quote（決め所）」
            if pic.startswith('図'):
                kind = '図（型は⑤bで決める）'
            else:
                kind = re.split(r'[\s（(]', pic, 1)[0]
            figs[kind] = figs.get(kind, 0) + 1
        if want_photo and not is_ph:
            continue
        if want_fig and is_ph:
            continue
        if c['ch'] != cur_ch:
            cur_ch = c['ch']
            print(f'\n══ {cur_ch} ══')
        n = len(sub[c['cid']])
        sec = sum(x['d'] for x in sub[c['cid']])
        print(f"{c['cid']:<7} {n}行 {sec:5.1f}s  {pic}   ｜{c['src']}")

    print('\n──────── 章ごとの実写の割合 ────────')
    for ch in ch_tot:
        r = ch_ph[ch] / ch_tot[ch] * 100
        flag = '  ⚠️' if not (45 <= r <= 50) else ''
        print(f'{ch:<34} {ch_ph[ch]:>3}/{ch_tot[ch]:<3} {r:5.1f}%{flag}')
    tot, ph = sum(ch_tot.values()), sum(ch_ph.values())
    print(f'{"計":<34} {ph:>3}/{tot:<3} {ph / tot * 100:5.1f}%')
    print('\n──────── 図の型ごとの数 ────────')
    for k, v in sorted(figs.items(), key=lambda x: -x[1]):
        print(f'{v:>3}  {k}')


if __name__ == '__main__':
    main()
