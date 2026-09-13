# -*- coding: utf-8 -*-
"""章ごと・カットごとの字数を出す（どこが薄いかを機械で見る）。check_script の parse を借りる。"""
import sys, io
sys.path.insert(0, r"C:/Users/konar/Desktop/zukai-engine/tools")
sys.stdout.reconfigure(encoding='utf-8')
import check_script as cs
T = open(sys.argv[1], encoding='utf-8').read()
cuts = cs.parse(T)
ch = {}
for cid, _, ls in cuts:
    k = cid[:2]
    n = sum(len(cs.clean(l)) for l in ls)
    ch.setdefault(k, []).append((cid, n, len(ls)))
tot = 0
for k, v in ch.items():
    s = sum(x[1] for x in v)
    tot += s
    print('%-3s カット%3d  字%5d  平均%5.1f  行%3d' % (k, len(v), s, s/len(v), sum(x[2] for x in v)))
print('計 %d字' % tot)
if '--cuts' in sys.argv:
    for k, v in ch.items():
        thin = [x for x in v if x[1] < 48]
        print('%s 薄いカット(48字未満) %d件: %s' % (k, len(thin), ' '.join('%s=%d' % (a, b) for a, b, _ in thin)))
