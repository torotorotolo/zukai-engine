# -*- coding: utf-8 -*-
"""33本目④'：照合の係（G1〜G5）と通し読みの係（G6）に渡す写しを、git の外（src/agents/wf33b/）へ書き出す（第1版は読むだけ・32本目 split32.py を写した）。
  python -P ref/ep33/v2_build/split33.py
出すもの（ref/ep33/src/agents/wf33b/）：
  cuts_v1.txt   §4 の全カット（当て残しの数え用）
  in_Gn.txt     その組のカットの全行（章の見出しつき。`**cNNN** ／ 画の欄 ／ 出典の欄`、続く `> ` が語り、`> Q: ` が聞き役）
  fixed_Gn.txt  ④ の直しの表（src/tools/patch_v1a.txt・patch_v1b.txt＝係4本の点検のあとの直し 130件）のうち、その組のカットのもの
                ＝「− 直す前（OLD）」「＋ 第1版（NEW）」。ルール 4'-5＝ここから当たる
  narr_all.txt  通し読み用＝章の見出し・カット番号・目安の時刻（句読点なし÷365 の積み上げ）・語りと聞き役の行だけ
  pic_all.txt   通し読み用＝カット番号と画の欄だけ（二重表示・画面の字を見る）
  times_v1.txt  時刻の網＝語りと画の欄の時刻（午前1時9分・1時14分・〈1:09〉・01.30 ほか）をカットごとに全部
  nums_v1.txt   数の多いカット（語りの数が4つ以上）
  sec_v1.txt    §4 の外の節（§0〜§3・§5〜§10）＝G5 と親が読む
  unmapped.txt  どのカットにも当てられなかった直し（あれば親が見る）
組＝G1 c1〜c3（冒頭・第1章・第2章）／G2 c4・c5（第3章・第4章）／G3 c6（第5章）／G4 c7・c8・c9（第6章〜第8章）／G5 ca・cb・cc（第9章〜第11章）＋§
出力は数だけ（名前は出さない）。終了コード 0＝書けた／1＝カットの数が 241 でない・形が読めない。
"""
import os
import pathlib
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
V1 = os.path.join(EP, 'daihon_v1.md')
TOOLS = os.path.join(EP, 'src', 'tools')
OUT = os.path.join(EP, 'src', 'agents', 'wf33b')
PUNCT = set('、。？！「」（）・')
CPM = 365.0
NCUT = 241
CUT = re.compile(r'^\*\*(c[0-9a-c]\d{2})\*\*')
GROUPS = {'G1': ['c1', 'c2', 'c3'], 'G2': ['c4', 'c5'], 'G3': ['c6'], 'G4': ['c7', 'c8', 'c9'],
          'G5': ['ca', 'cb', 'cc']}
PATCHES = [('patch_v1a.txt', '係の点検のあとの直し'), ('patch_v1b.txt', '係の点検のあとの直し')]
TIME = re.compile(r'(?:午前|午後|朝|夜)?\d{1,2}時(?:\d{1,2}分)?(?:\d{1,2}秒)?|\d{1,2}[:：]\d{2}(?::\d{2})?|0\d\.\d{2}')
NUM = re.compile(r'[0-9][0-9,.]*|[一二三四五六七八九十百千万億]+(?=[人つ件階戸回年月日時分秒倍]|か所|か月)')


def nopunct(s):
    return ''.join(ch for ch in s if ch not in PUNCT and not ch.isspace())


def parse_v1(text):
    lines = text.split('\n')
    s4 = next(i for i, l in enumerate(lines) if l.startswith('## 4. 台本'))
    e4 = next(i for i, l in enumerate(lines) if i > s4 and l.startswith('## 5.'))
    cuts, order, chap = {}, [], None
    cur = None
    for i in range(s4 + 1, e4):
        l = lines[i]
        if l.startswith('### '):
            chap = l[4:].strip()
            cur = None
            continue
        if l.startswith('## ') or l.strip() == '---':
            cur = None
            continue
        m = CUT.match(l)
        if m:
            cur = m.group(1)
            cuts[cur] = {'chap': chap, 'lines': [l]}
            order.append(cur)
            continue
        if cur is not None:
            cuts[cur]['lines'].append(l)
    for c in order:
        while cuts[c]['lines'] and not cuts[c]['lines'][-1].strip():
            cuts[c]['lines'].pop()
    outside = '\n'.join(lines[:s4] + ['', '（§4 台本は略）', ''] + lines[e4:])
    return cuts, order, outside


def parse_patches(path):
    t = open(path, encoding='utf-8').read().replace('\r\n', '\n')
    return [(m.group(1), m.group(2)) for m in re.finditer(r'@@@ OLD\n(.*?)\n@@@ NEW\n(.*?)\n@@@ END', t, re.S)]


def speech(lines):
    return [l[2:] if l.startswith('> ') else l[1:] for l in lines[1:] if l.startswith('>')]


def pic(head):
    parts = head.split('／')
    return parts[1].strip() if len(parts) >= 3 else ''


def main():
    text = open(V1, encoding='utf-8').read().replace('\r\n', '\n')
    cuts, order, outside = parse_v1(text)
    if len(order) != NCUT:
        print('🔴 カットの数が', len(order))
        return 1
    pathlib.Path(OUT).mkdir(parents=True, exist_ok=True)  # 名前の網の空鳴りを避ける書き方
    blocks = {c: '\n'.join(cuts[c]['lines']) for c in order}
    mapped = {c: [] for c in order}
    unmapped, total = [], 0
    for fn, label in PATCHES:
        p = os.path.join(TOOLS, fn)
        if not os.path.exists(p):
            print('🔴 直しの表が無い:', fn)
            return 1
        for k, (old, new) in enumerate(parse_patches(p), 1):
            total += 1
            hit = [c for c in order if new in blocks[c]]
            how = 'NEW がそのまま'
            if not hit:
                cand = sorted((l for l in new.split('\n') if len(l.strip()) >= 8), key=len, reverse=True)
                for l in cand:
                    hit = [c for c in order if l in blocks[c]]
                    if hit:
                        how = 'NEW の一部（あとの直しで変わった）'
                        break
            if not hit:
                cand = sorted((l for l in old.split('\n') if len(l.strip()) >= 8), key=len, reverse=True)
                for l in cand:
                    hit = [c for c in order if l in blocks[c]]
                    if hit:
                        how = 'OLD の一部が残っている'
                        break
            if hit:
                for c in hit[:3]:
                    mapped[c].append((fn, k, label, how, old, new))
            else:
                unmapped.append((fn, k, label, old, new))
    with open(os.path.join(OUT, 'cuts_v1.txt'), 'w', encoding='utf-8', newline='\n') as f:
        for c in order:
            f.write(blocks[c] + '\n\n')
    nfix = {}
    for g, prefixes in GROUPS.items():
        mine = [c for c in order if c[:2] in prefixes]
        with open(os.path.join(OUT, 'in_%s.txt' % g), 'w', encoding='utf-8', newline='\n') as f:
            f.write('# %s 受け持ち %d カット（%s〜%s）・台本 第1版 ref/ep33/daihon_v1.md の §4 の写し（読むだけ）\n\n' % (g, len(mine), mine[0], mine[-1]))
            chap = None
            for c in mine:
                if cuts[c]['chap'] != chap:
                    chap = cuts[c]['chap']
                    f.write('### %s\n\n' % chap)
                f.write(blocks[c] + '\n\n')
        n = 0
        with open(os.path.join(OUT, 'fixed_%s.txt' % g), 'w', encoding='utf-8', newline='\n') as f:
            f.write('# %s：④ の直しの表のうち受け持ちのカットのもの（− 直す前＝OLD／＋ 第1版＝NEW）。どれも ④ の係4本の点検のあとの直し\n' % g)
            f.write('# 当て方＝NEW が第1版のそのカットに入っているか。🔴 語を消して主張が残っていないか・縮めた文が原文の語を落としていないか・足した文が原文と合うか\n\n')
            for c in mine:
                for fn, k, label, how, old, new in mapped[c]:
                    n += 1
                    f.write('## %s ← %s #%d（%s・当て方＝%s）\n− 直す前:\n%s\n＋ 第1版:\n%s\n\n' % (c, fn, k, label, how, old, new))
        nfix[g] = n
    secs = 0.0
    tl, nl = [], []
    with open(os.path.join(OUT, 'narr_all.txt'), 'w', encoding='utf-8', newline='\n') as f, \
            open(os.path.join(OUT, 'pic_all.txt'), 'w', encoding='utf-8', newline='\n') as fp:
        f.write('# 33本目 台本 第1版の語りと聞き役だけ（耳で聞く順・画と出典の欄なし）。時刻＝句読点なしの字を1分365字で積み上げたカットの頭\n')
        f.write('# 行の頭の「れいむ:」＝聞き役（台本の印は `> Q: `）・ほか＝語り（まりさ）。最後に共通エンディング（ed01・46字）が続く\n\n')
        fp.write('# 33本目 台本 第1版の画の欄だけ（カット番号・目安の時刻・画の欄）\n\n')
        chap = None
        for c in order:
            if cuts[c]['chap'] != chap:
                chap = cuts[c]['chap']
                f.write('\n### %s\n\n' % chap)
                fp.write('\n### %s\n\n' % chap)
            sp = speech(cuts[c]['lines'])
            mm, ss = divmod(int(secs), 60)
            f.write('**%s** ［%d:%02d］\n' % (c, mm, ss))
            for l in sp:
                f.write(('れいむ: %s\n' % l[3:]) if l.startswith('Q: ') else ('%s\n' % l))
            f.write('\n')
            fp.write('**%s** ［%d:%02d］ %s\n' % (c, mm, ss, pic(cuts[c]['lines'][0])))
            for l in sp:
                for t in TIME.findall(l):
                    tl.append((c, '語り' if not l.startswith('Q: ') else '聞き役', t, l))
            for t in TIME.findall(pic(cuts[c]['lines'][0])):
                tl.append((c, '画', t, ''))
            spoken = ' '.join(l[3:] if l.startswith('Q: ') else l for l in sp)
            nums = NUM.findall(spoken)
            if len(nums) >= 4:
                nl.append((c, len(nums), ' '.join(nums), spoken))
            secs += sum(len(nopunct(l[3:] if l.startswith('Q: ') else l)) for l in sp) / CPM * 60
    with open(os.path.join(OUT, 'times_v1.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('# 時刻の網：語り・聞き役・画の欄（副題）に出る時刻の全部（カット順）。語りの行は同じ行の時刻をまとめて1回だけ載せる\n')
        f.write('# 当てる所＝P1ES ¶2.11 の表（要約）と P1V4 28章（結論）と、その時刻を詳しく書いた段落（P1V2・P1V3・P1V4 の本文）。要約の表と本文がずれる所がある（④：c516＝着いたのは2時31分・指揮の引き継ぎは2時44分）\n\n')
        seen = set()
        for c, who, t, l in tl:
            key = (c, who, l) if l else (c, who, t)
            if key in seen:
                continue
            seen.add(key)
            ts = [x for (cc, ww, x, ll) in tl if cc == c and ww == who and ll == l] if l else [t]
            f.write('%s\t%s\t%s\t%s\n' % (c, who, '・'.join(ts), l))
    with open(os.path.join(OUT, 'nums_v1.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('# 数の多いカット（語りと聞き役の数の語が4つ以上）＝§0-1 の5。耳で聞いて追えるか\n\n')
        for c, n, ns, sp in sorted(nl, key=lambda x: -x[1]):
            f.write('%s\t%d\t%s\t%s\n' % (c, n, ns, sp))
    with open(os.path.join(OUT, 'sec_v1.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(outside)
    with open(os.path.join(OUT, 'unmapped.txt'), 'w', encoding='utf-8', newline='\n') as f:
        for fn, k, label, old, new in unmapped:
            f.write('## %s #%d（%s）\n− 直す前:\n%s\n＋ 第1版:\n%s\n\n' % (fn, k, label, old, new))
    print('カット %d・直しの表 %d件（当てられなかった %d）' % (len(order), total, len(unmapped)))
    for g in GROUPS:
        mine = [c for c in order if c[:2] in GROUPS[g]]
        print('%s %dカット・直し %d件' % (g, len(mine), nfix[g]))
    ntl = len(open(os.path.join(OUT, 'times_v1.txt'), encoding='utf-8').read().splitlines()) - 3
    mm, ss = divmod(int(secs), 60)
    print('時刻の網 %d行・数の多いカット %d・語りの終わりの目安 %d分%02d秒（ed01 を除く）' % (ntl, len(nl), mm, ss))
    return 0


if __name__ == '__main__':
    sys.exit(main())
