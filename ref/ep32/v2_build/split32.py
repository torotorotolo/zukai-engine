# -*- coding: utf-8 -*-
"""32本目④'：照合の係（G1〜G6）と通し読みの係（G7）に渡す写しを、git の外（src/agents/wf32b/）へ書き出す（第1版は読むだけ・31本目 split31.py の考えを写した）。

  python -P ref/ep32/v2_build/split32.py

出すもの（ref/ep32/src/agents/wf32b/）：
  cuts_v1.txt   §4 の全カット（当て残しの数え用）
  in_Gn.txt     その組のカットの全行（章の見出しつき。`**cNNN** ／ 画の欄 ／ 出典の欄`、続く `> ` が語り、`> Q: ` が聞き役）
  fixed_Gn.txt  ④ の直しの表（src/tools/patch_v1a〜d.txt）のうち、その組のカットのもの＝「− 直す前（OLD）」「＋ 第1版（NEW）」
                （v1c・v1d＝係4本の点検のあとの直し 157件／v1a・v1b＝書きながらの直し）。ルール 4'-5＝ここから当たる
  narr_all.txt  通し読み用＝章の見出し・カット番号・目安の時刻（句読点なし÷365 の積み上げ）・語りと聞き役の行だけ（画と出典の欄なし）
  sec_v1.txt    §4 の外の節（§1 題・芯・問い・人・割れる時刻と数・そのほか／§5〜§9）＝G6 と親が読む
  unmapped.txt  どのカットにも当てられなかった直し（あれば親が見る）
組＝G1 c1〜c3（冒頭・第1章・第2章）／G2 c4・c5（第3章・第4章）／G3 c6（第5章）／G4 c7・c8（第6章・第7章）／G5 c9・ca（第8章・第9章）／G6 cb・cc（第10章・第11章）＋§
出力は数だけ（名前は出さない）。終了コード 0＝書けた／1＝カットの数が 237 でない・形が読めない。
"""
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')
HERE = os.path.dirname(os.path.abspath(__file__))
EP = os.path.dirname(HERE)
V1 = os.path.join(EP, 'daihon_v1.md')
TOOLS = os.path.join(EP, 'src', 'tools')
OUT = os.path.join(EP, 'src', 'agents', 'wf32b')
PUNCT = set('、。？！「」（）・')
CPM = 365.0
CUT = re.compile(r'^\*\*(c[0-9a-c]\d{2})\*\*')
GROUPS = {'G1': ['c1', 'c2', 'c3'], 'G2': ['c4', 'c5'], 'G3': ['c6'], 'G4': ['c7', 'c8'],
          'G5': ['c9', 'ca'], 'G6': ['cb', 'cc']}
PATCHES = [('patch_v1a.txt', '書きながらの直し'), ('patch_v1b.txt', '書きながらの直し'),
           ('patch_v1c.txt', '係の点検のあとの直し'), ('patch_v1d.txt', '係の点検のあとの直し')]


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
    out = []
    for m in re.finditer(r'@@@ OLD\n(.*?)\n@@@ NEW\n(.*?)\n@@@ END', t, re.S):
        out.append((m.group(1), m.group(2)))
    return out


def speech(lines):
    return [l[2:] if l.startswith('> ') else l[1:] for l in lines[1:] if l.startswith('>')]


def main():
    text = open(V1, encoding='utf-8').read().replace('\r\n', '\n')
    cuts, order, outside = parse_v1(text)
    if len(order) != 237:
        print('🔴 カットの数が', len(order))
        return 1
    os.makedirs(OUT, exist_ok=True)
    blocks = {c: '\n'.join(cuts[c]['lines']) for c in order}
    # 直しの表をカットに当てる（NEW がそのまま入っているカット → 無ければ NEW のいちばん長い行が入っているカット）
    mapped = {c: [] for c in order}
    unmapped = []
    total = 0
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
            if len(hit) >= 1:
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
            f.write('# %s 受け持ち %d カット（%s〜%s）・台本 第1版 ref/ep32/daihon_v1.md の §4 の写し（読むだけ）\n\n' % (g, len(mine), mine[0], mine[-1]))
            chap = None
            for c in mine:
                if cuts[c]['chap'] != chap:
                    chap = cuts[c]['chap']
                    f.write('### %s\n\n' % chap)
                f.write(blocks[c] + '\n\n')
        n = 0
        with open(os.path.join(OUT, 'fixed_%s.txt' % g), 'w', encoding='utf-8', newline='\n') as f:
            f.write('# %s：④ の直しの表のうち受け持ちのカットのもの（− 直す前＝OLD／＋ 第1版＝NEW）。v1c・v1d＝係4本の点検のあとの直し・v1a・v1b＝書きながらの直し\n' % g)
            f.write('# 当て方＝NEW が第1版のそのカットに入っているか（変わっていれば「あとの直しで変わった」）。🔴 語を消して主張が残っていないか・縮めた文が原文の語を落としていないか\n\n')
            for c in mine:
                for fn, k, label, how, old, new in mapped[c]:
                    n += 1
                    f.write('## %s ← %s #%d（%s・当て方＝%s）\n− 直す前:\n%s\n＋ 第1版:\n%s\n\n' % (c, fn, k, label, how, old, new))
        nfix[g] = n
    secs = 0.0
    with open(os.path.join(OUT, 'narr_all.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write('# 32本目 台本 第1版の語りと聞き役だけ（耳で聞く順・画と出典の欄なし）。時刻＝句読点なしの字を1分365字で積み上げたカットの頭\n')
        f.write('# 行の頭の「れいむ:」＝聞き役（台本の印は `> Q: `）・ほか＝語り（まりさ）。最後に共通エンディング（ed01・46字）が続く\n\n')
        chap = None
        for c in order:
            if cuts[c]['chap'] != chap:
                chap = cuts[c]['chap']
                f.write('\n### %s\n\n' % chap)
            sp = speech(cuts[c]['lines'])
            mm, ss = divmod(int(secs), 60)
            f.write('**%s** ［%d:%02d］\n' % (c, mm, ss))
            for l in sp:
                if l.startswith('Q: '):
                    f.write('れいむ: %s\n' % l[3:])
                else:
                    f.write('%s\n' % l)
            f.write('\n')
            secs += sum(len(nopunct(l[3:] if l.startswith('Q: ') else l)) for l in sp) / CPM * 60
    with open(os.path.join(OUT, 'sec_v1.txt'), 'w', encoding='utf-8', newline='\n') as f:
        f.write(outside)
    with open(os.path.join(OUT, 'unmapped.txt'), 'w', encoding='utf-8', newline='\n') as f:
        for fn, k, label, old, new in unmapped:
            f.write('## %s #%d（%s）\n− 直す前:\n%s\n＋ 第1版:\n%s\n\n' % (fn, k, label, old, new))
    print('カット %d・直しの表 %d件（当てられなかった %d）' % (len(order), total, len(unmapped)))
    for g in GROUPS:
        mine = [c for c in order if c[:2] in GROUPS[g]]
        print('%s %dカット・直し %d件' % (g, len(mine), nfix[g]))
    print('語りの終わりの目安 %d分%02d秒（ed01 を除く）' % divmod(int(secs), 60))
    return 0


if __name__ == '__main__':
    sys.exit(main())
