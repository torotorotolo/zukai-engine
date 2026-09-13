# -*- coding: utf-8 -*-
"""台本の自己点検：①語尾の連続 ②同じ言い回しの重複 ③専門語の初出位置 を機械で見る。
⚠️ これは形しか見ない。意味のずれは通し読みでしか出ない（[[feedback-script-must-pass-a-cold-read]]）。"""
import sys, re, collections
sys.path.insert(0, r"C:/Users/konar/Desktop/zukai-engine/tools")
sys.stdout.reconfigure(encoding='utf-8')
import check_script as cs
T = open(sys.argv[1], encoding='utf-8').read()
cuts = cs.parse(T)
flat = [(cid, cs.clean(l)) for cid, _, ls in cuts for l in ls]

print('── ① 語尾（末尾4字）が3行以上続く')
prev, run = None, []
for cid, l in flat:
    tail = l.rstrip('。').rstrip('、')[-4:]
    if tail == prev:
        run.append(cid)
    else:
        if len(run) >= 3:
            print('   %s ×%d: %s' % (prev, len(run), ' '.join(run)))
        prev, run = tail, [cid]
if len(run) >= 3:
    print('   %s ×%d: %s' % (prev, len(run), ' '.join(run)))

print('── ② 同じ8字以上の並びが2か所以上（★の二重表示は門番が見るので、それ以外）')
seen = collections.defaultdict(list)
for cid, l in flat:
    s = l.replace('、', '').replace('。', '')
    for n in (10,):
        for i in range(len(s) - n + 1):
            seen[s[i:i+n]].append(cid)
for k, v in sorted(seen.items()):
    u = sorted(set(v))
    if len(u) >= 2:
        print('   「%s」 %s' % (k, ' '.join(u)))

print('── ③ 専門語の初出カット（説明がその前か同じカットに在るか、目で見る）')
TERMS = ['トランスポンダ', '応答符号', '一次レーダー', '二次レーダー', '跳ね返り',
         '航空路管制センター', 'コマンドセンター', '防空司令部', '連邦航空局',
         '国防総省', '北棟', '南棟', '緊急発進', '大統領警護隊', '運航管理']
for t in TERMS:
    hit = [cid for cid, l in flat if t in l]
    print('   %-12s 初出 %s（全%d回）' % (t, hit[0] if hit else '—', len(hit)))
