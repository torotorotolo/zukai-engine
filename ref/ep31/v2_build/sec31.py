# -*- coding: utf-8 -*-
"""31本目④'：第2版の数（m31.py・quotes31.py の出力）から、§2（原文の片の表）と §3（章ごとの表・範囲の割合）を組み直す差し替え表を作る（30本目 sec_nums30.py の考えを写した）。

  python -P ref/ep31/v2_build/sec31.py   → v2_build/patches_sec_num.json（cut "§"・old＝第1版の行・new＝第2版の数の行）

順番＝組む（build31_v2.py）→ この道具 → merge31.py → もう一度組む。§2・§3 の字は §4 の数に効かない＝2周目も同じ数になる（final31.py で md5 を見る）。
章名は第1版の §3 の表のまま（承認①で変われば親が直す）。手で数を写さない。
"""
import json
import os
import re
import subprocess
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
REPO = os.path.dirname(os.path.dirname(EP))
V1 = os.path.join(EP, 'daihon_v1.md')
V2 = os.path.join(EP, 'daihon_v2.md')
ENV = dict(os.environ, PYTHONIOENCODING='utf-8', PYTHONUTF8='1')
ROW = re.compile(r'^\s+(c[0-9a-c])\s+(\d+)分(\d+)秒\s+(\d+)（\s*\d+）\s+(\d+)\s+(\d+)（\s*(\d+)・\s*[+-]?\d+）\s+([\d.]+)\s+(\d+)（\s*\d+）\s*(\d+)%\s+(\d+)\s+(\d+)\s+(\d+)（\s*\d+）')


def run(args):
    r = subprocess.run([sys.executable, '-P'] + args, cwd=REPO, env=ENV, capture_output=True, text=True, encoding='utf-8', errors='replace')
    return r.stdout + r.stderr


def comma(n):
    return '{:,}'.format(n)


def main():
    roles = os.path.join(os.environ.get('TEMP', HERE), 'ep31_sec_roles.tsv')
    run([os.path.join(EP, 'v1_build', 'roles31.py'), V2, roles])
    m = run([os.path.join(EP, 'v1_build', 'm31.py'), V2, '--roles', roles])
    q = run([os.path.join(EP, 'v1_build', 'quotes31.py'), V2, '--out', os.path.join(os.environ.get('TEMP', HERE), 'ep31_sec_q.tsv')])
    rows = {mm.group(1): mm for mm in (ROW.match(ln) for ln in m.split('\n')) if mm}
    if len(rows) != 12:
        print('🔴 m31 の章の行が12でない:', sorted(rows))
        return 1
    ed = re.search(r'^\s+ed01\s+(\d+)分(\d+)秒', m, re.M)
    tot = re.search(r'カット (\d+) / 行 (\d+) / 句読点なし (\d+)字＋ed01 (\d+)＝(\d+)字', m)
    ph = re.search(r'写真・映像・紙面（実写）(\d+)（', m)
    im = re.search(r'フリー素材（イメージ）(\d+)', m)
    du = re.search(r'② 句読点なし÷365 (\d+)分(\d+)秒', m)
    lq = re.search(r"'q': (\d+)", m)
    if not (ed and tot and ph and im and du and lq):
        print('🔴 m31 の出力が読めない')
        return 1
    v1 = open(V1, encoding='utf-8').read().split('\n')
    s3 = next(i for i, ln in enumerate(v1) if ln.startswith('## 3. '))
    s1 = next(i for i, ln in enumerate(v1) if ln.startswith('## 1. '))
    names = {}
    old_rows = []
    for ln in v1[s3:s1]:
        mm = re.match(r'^\| (c[0-9a-c]) \| ([^|]+) \|', ln)
        if mm:
            names[mm.group(1)] = mm.group(2).strip()
            old_rows.append(ln)
        elif ln.startswith('| ed01 ') or ln.startswith('| **計** '):
            old_rows.append(ln)
    order = ['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'ca', 'cb', 'cc']
    new_rows = []
    for c in order:
        r = rows[c]
        new_rows.append('| %s | %s | %d:%02d | %s | %s（%s） | %s | %s | %s | %s |' % (
            c, names[c], int(r.group(2)), int(r.group(3)), r.group(4), comma(int(r.group(6))), comma(int(r.group(7))),
            r.group(8), r.group(9), r.group(11), r.group(13)))
    new_rows.append('| ed01 | 共通エンディング | %d:%02d | — | %s | %.2f | — | — | — |' % (int(ed.group(1)), int(ed.group(2)), tot.group(4), int(tot.group(4)) / 365.0))
    mins = {c: float(rows[c].group(8)) for c in order}
    total_min = int(tot.group(5)) / 365.0
    new_rows.append('| **計** | | **%d:%02d** | **%s** | **%s** | **%.2f** | **%s** | **%s** | **%s** |' % (
        int(du.group(1)), int(du.group(2)), tot.group(1), comma(int(tot.group(5))), total_min, ph.group(1), im.group(1), lq.group(1)))
    patches = [{'id': 'S-N03', 'cut': '§', 'old': '\n'.join(old_rows), 'new': '\n'.join(new_rows),
                'why': "④' の第2版の数（m31.py）で §3 の表を組み直した（手で写さない）", 'from': []}]
    old_rng = next(ln for ln in v1[s3:s1] if ln.startswith('- 範囲の割合'))
    ed_min = int(tot.group(4)) / 365.0
    groups = [('c1〜c2', ['c1', 'c2'], 0), ('c3〜c4', ['c3', 'c4'], 0), ('c5〜c7', ['c5', 'c6', 'c7'], 0),
              ('c8〜ca', ['c8', 'c9', 'ca'], 0), ('cb〜cc（ed01 こみ）', ['cb', 'cc'], ed_min)]
    parts = []
    for lab, cs, extra in groups:
        x = sum(mins[c] for c in cs) + extra
        parts.append('%s＝**%.1f分＝%.1f%%**' % (lab, x, x / total_min * 100))
    new_rng = old_rng.split('：')[0] + '：' + '／'.join(parts) + '（④\' の第2版）'
    patches.append({'id': 'S-N04', 'cut': '§', 'old': old_rng, 'new': new_rng, 'why': "④' の第2版の数で範囲の割合を組み直した", 'from': []})
    qa = re.search(r'片 (\d+): OK=(\d+)(?: 会=(\d+))?(?: 町=(\d+))?', q)
    qn = re.search(r'片の無いカット (\d+): (.*)', q)
    if not qa or not qn:
        print('🔴 quotes31 の出力が読めない')
        return 1
    n_all, n_ok = int(qa.group(1)), int(qa.group(2))
    n_kai, n_cho = int(qa.group(3) or 0), int(qa.group(4) or 0)
    n_bad = n_all - n_ok - n_kai - n_cho
    s2 = next(i for i, ln in enumerate(v1) if ln.startswith('## 2. '))
    sec2 = v1[s2:s3]
    o_ok = next(ln for ln in sec2 if ln.startswith('| OK（書いた資料にある）'))
    o_mc = next(ln for ln in sec2 if ln.startswith('| 町（雫石町の頁）'))
    o_bad = next(ln for ln in sec2 if ln.startswith('| 無し・短い・記号なし'))
    o_none = next(ln for ln in sec2 if ln.startswith('- 片の無いカット'))
    cuts = qn.group(2).split()
    patches += [
        {'id': 'S-N01', 'cut': '§', 'old': '\n'.join([o_ok, o_mc, o_bad]),
         'new': '\n'.join(['| OK（書いた資料にある） | **%d** |' % n_ok,
                           "| 町（雫石町の頁）・会（全日空の頁）＝手元に写しが無い＝機械で当てない（④' の親が 2026-11-07 に頁を読んで字を確かめた） | %d |" % (n_kai + n_cho),
                           '| 無し・短い・記号なし | **%d** |' % n_bad]),
         'why': "④' の第2版の quotes31.py の数で §2 の表を組み直した", 'from': []},
        {'id': 'S-N02', 'cut': '§', 'old': o_none,
         'new': '- 片の無いカット %d＝まとめ・橋・断り・問いのカットと、画の表示だけのカット（%s）' % (int(qn.group(1)), '・'.join(cuts)),
         'why': "④' の第2版の quotes31.py の一覧で組み直した（第1版の一覧は c208 が抜けて42個だった＝P-001）", 'from': ['P-001']},
    ]
    if n_bad:
        print('🔴 外れの片 %d' % n_bad)
    json.dump(patches, open(os.path.join(HERE, 'patches_sec_num.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('§2 片 %d＝OK %d・町と会 %d・外れ %d／片の無いカット %d　§3 計 %s カット・%s字・%d分%02d秒・写真 %s・イメージ %s・聞き役 %s → patches_sec_num.json（%d本）' % (
        n_all, n_ok, n_kai + n_cho, n_bad, int(qn.group(1)), tot.group(1), comma(int(tot.group(5))), int(du.group(1)), int(du.group(2)),
        ph.group(1), im.group(1), lq.group(1), len(patches)))
    return 1 if n_bad else 0


if __name__ == '__main__':
    sys.exit(main())
