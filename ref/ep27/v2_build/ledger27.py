# -*- coding: utf-8 -*-
"""27本目④'：所見の台帳（1行1粗）を、係の記録と ④' の本人の所見と差し替え表から組む（手で写さない）。

  python -P ref/ep27/v2_build/ledger27.py   → v2_build/ledger27.md

入力＝git の外 src/agents/wf27b/wf27b_findings.json（係6本＝G1〜G6）・v2_build/own27.json（④' の本人＝P）・
      v2_build/patches27.json（各差し替えの from＝もとの所見の番号）・下の NOT_ADOPTED（直さなかった所見と理由）・PARTIAL（一部だけ採った）
扱い＝直した（差し替えの id）／一部（理由）／直さない（理由）。OK 以外の所見で扱いが決まっていないものが1件でもあれば止める（exit 1）。
台本の字・原文の片（20字以内）だけを載せる。名前は載せない（namecheck27.py が当てる）。
"""
import collections
import json
import os
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
SEV = {'🔴': 0, '⚠️': 1, '・': 2}

NOT_ADOPTED = {
    'R1-036': '公開日は ② の在庫の記録（materials.md §2-2＝YT-C 2025-12-11）＝c106 の副題と同じ値。映像方針で動画の頁を開いて確かめる',
    'G6-024': '§6 に「110番＝ひゃくとおばん」がある（⑤a の読み辞書で固定）',
    'G6-026': 'カズヤくんの1通目「台本は『10月末の時点では』の形のまま」＝公開日で変わる＝⑥ の前に県警の頁で確かめる',
    'G6-029': '原文を読んだ G5 が元刑事の「撮ったものはSNSに上げず」を当てた（NEWSポストセブン 2026-10-25 の2ページ目）＝帰属は正しい（G6 はウェブを開かない係）',
    'G6-042': '§6 に「X（旧ツイッター）＝エックス」がある',
    'G1-007': '画像は開かない＝映像方針で手配ポスターの絵を原寸で見て「犯人」の字が無いか決める（④ の未達3）',
    'G2-018': 'G1 が TOS 2023-05-25 に「黒いTシャツ」を当てた＝画の札は残す',
    'G3-008': '任意の案。「受け付けた」で受理の言い換えになっている',
    'G5-021': 'G6-026 と同じ（カズヤくんの1通目）＝⑥ の前に確かめる',
    'G5-032': '確かめられたのは2回（2025-09 捜査1課の次席＝coki.jp／2026-06-29 県警 X の固定の投稿＝② で原文を読んだ・sources.md §1）＝「くり返し」は残す',
    'G5-033': "県警 X の固定の投稿は ② で原文を読んだ（sources.md §1・10-29）。④' は X を開かない＝⑤b-1 で投稿の画を取るとき字を確かめる",
}
PARTIAL = {
    'G6-004': '引きの行は OAB の原文のまま残し「それでも、」だけ足した（F103）。替え案「それでも警察は、海を調べた」は目撃の多さと海の捜索を因果のように並べる＝推測を足す＝承認① で見てもらう',
    'G6-032': '「1万3978件」は §6 にある。4378件・動画10本を足した（S6e）',
}


def load():
    d = json.load(open(os.path.join(EP, 'src', 'agents', 'wf27b', 'wf27b_findings.json'), encoding='utf-8'))
    rows = []
    for g in ('G1', 'G2', 'G3', 'G4', 'G5', 'G6'):
        for k, x in enumerate((d.get(g) or {}).get('findings', []), 1):
            x = dict(x)
            x.setdefault('id', '%s-%03d' % (g, k))
            rows.append(x)
    for x in json.load(open(os.path.join(HERE, 'own27.json'), encoding='utf-8')):
        rows.append(dict(x))
    rv = os.path.join(EP, 'src', 'agents', 'wf27b', 'rv27_findings.json')     # 当て直し（4'-18）＝R1・R2
    if os.path.exists(rv):
        r = json.load(open(rv, encoding='utf-8'))
        for g in ('R1', 'R2'):
            for k, x in enumerate((r.get(g) or {}).get('findings', []), 1):
                x = dict(x)
                x.setdefault('id', '%s-%03d' % (g, k))
                x.setdefault('aspect', 'B')
                rows.append(x)
    return rows


def main():
    rows = load()
    patches = json.load(open(os.path.join(HERE, 'patches27.json'), encoding='utf-8'))
    byf = collections.defaultdict(list)
    for p in patches:
        for f in p.get('from', []):
            byf[f].append(p['id'])
    ok = [x for x in rows if x.get('verdict') == 'OK']
    bad = [x for x in rows if x.get('verdict') != 'OK']
    bad.sort(key=lambda x: (SEV.get(x.get('severity'), 9), x.get('cut', ''), x['id']))
    out = ['# 27本目 ④\' 所見の台帳（ledger27.py が組む・手で直さない）', '',
           '- 入力＝係6本（G1〜G5＝章ごとの原文照合・G6＝通し読み）の記録 `src/agents/wf27b/wf27b_findings.json`（git の外）＋④\' の本人の所見 `own27.json`（P）＋差し替え表 `patches27.json`',
           '- 扱い＝**直した**（差し替えの id＝`patches27.json`）／**一部**／**直さない**（理由）。原文の片は20字以内。OK の所見は数だけ（記録は git の外）', '']
    cnt = collections.Counter()
    sev = collections.Counter()
    lines = []
    undecided = []
    for x in bad:
        fid = x['id']
        if fid in PARTIAL:
            how = '一部（%s）' % PARTIAL[fid]
            cnt['一部'] += 1
        elif fid in byf:
            how = '直した（%s）' % '・'.join(byf[fid])
            cnt['直した'] += 1
        elif fid in NOT_ADOPTED:
            how = '直さない（%s）' % NOT_ADOPTED[fid]
            cnt['直さない'] += 1
        else:
            how = '🔴 扱いが決まっていない'
            undecided.append(fid)
        sev[x.get('severity')] += 1
        frag = ('`%s`' % x['fragment']) if x.get('fragment') else ''
        lines.append('| %s | %s | %s | %s／%s | %s | %s %s | %s |' % (
            fid, x.get('severity'), x.get('cut'), x.get('aspect'), x.get('kind'),
            (x.get('text') or '').replace('|', '／')[:60], x.get('source', '')[:40], frag, how.replace('|', '／')))
    out.append('## 数')
    out.append('- 所見 %d件＝OK %d・OK 以外 %d（🔴 %d・⚠️ %d・・ %d）' % (len(rows), len(ok), len(bad), sev['🔴'], sev['⚠️'], sev['・']))
    out.append('- 扱い＝直した %d・一部 %d・直さない %d・決まっていない %d' % (cnt['直した'], cnt['一部'], cnt['直さない'], len(undecided)))
    per = collections.Counter(x['id'].split('-')[0] for x in rows)
    per_bad = collections.Counter(x['id'].split('-')[0] for x in bad)
    out.append('- 係ごと（所見／OK 以外）＝' + '・'.join('%s %d／%d' % (g, per[g], per_bad[g]) for g in ('G1', 'G2', 'G3', 'G4', 'G5', 'G6', 'P', 'R1', 'R2'))
               + '（R＝当て直し＝第2版の直しを別の目で原文に）')
    out.append('- 差し替え %d件（カット %d・§ と章の外 %d）' % (len(patches), sum(1 for p in patches if p['cut'].startswith('c')),
                                                   sum(1 for p in patches if not p['cut'].startswith('c'))))
    out += ['', '## OK 以外の所見（🔴→⚠️→・）', '',
            '| id | 重さ | カット | 面／型 | 台本の句 | 原文（出典・片） | 扱い |', '|---|---|---|---|---|---|---|'] + lines
    open(os.path.join(HERE, 'ledger27.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
    print('\n'.join(out[5:9]))
    print('→', os.path.join(HERE, 'ledger27.md'))
    if undecided:
        print('🔴 扱いが決まっていない:', ' '.join(undecided))
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
