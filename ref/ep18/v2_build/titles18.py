# -*- coding: utf-8 -*-
"""18本目④'：タイトル案を機械で数え、公開ずみの題（全数）と型を照合する（ルール 4'-8・§B4）。読むだけ。
17本目 ref/ep17/v2_build/titles17.py を写して18本目に合わせた。
    python ref/ep18/v2_build/titles18.py
公開ずみ＝ref/ep14/v2_build/titles.json（12本・videoId→題＝旧版 o9jfxyYeOBk を含む）＋config/meta_ep13.json・meta_ep14.json の title（計14本）。
案＝同じフォルダの titles18.json（{"A": "…", …}）。
見ること：字数（len・67〜100）／末尾「…129人が亡くなったスレッシャー号沈没事故の真相【事故検証】【ゆっくり解説】」（§B4-8）／
      文の数（。で割る）／【映像あり】を付けない（この回は無し＝確定）／死の語・煽り語／公開ずみの題と同じ語句（8字以上の共通部分）。
"""
import json, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
S = Path(__file__).resolve().parent
ROOT = S.parents[2]
pub = dict(json.load(open(ROOT / "ref/ep14/v2_build/titles.json", encoding="utf-8")))
# 10-01（④' 2本目）：15本目（2026-10-01 17:00 予約＝hsDtzoHIvE0）を足した＝網の漏れの点検の指摘（計15本）
for e in ("ep13", "ep14", "ep15"):
    pub[e] = json.load(open(ROOT / f"config/meta_{e}.json", encoding="utf-8"))["title"]
cand = json.load(open(S / "titles18.json", encoding="utf-8"))
NAME = "129人が亡くなったスレッシャー号沈没事故の真相【事故検証】【ゆっくり解説】"
# 🔴 10-01 カズヤくん決定（④'の承認）＝「出来る限り旧版に近いタイトル」→ 末尾も旧版の形（§B4-1 の型から外れる・この回だけの例外）
NAME_R = "スレッシャー号129名喪失事故の真相【事故検証】【ゆっくり解説】"
NAMES = (NAME, NAME_R)
BAD = ["死亡", "即死", "絶命", "地獄", "瞬間", "圧壊", "隠蔽", "衝撃", "【映像あり】", "〜"]
TEMPLATE = re.compile(r"(\d[\d,]*人|乗員\d+名|\d+名)(が亡くなった|を失った|喪失|が被曝した|が犠牲になった)|の真相【事故検証】|【映像あり】|【事故検証】|【ゆっくり解説】")

L = [len(t) for t in pub.values()]
print(f"公開ずみ {len(pub)}本：字数 最短{min(L)}・最長{max(L)}・中央値{sorted(L)[len(L)//2]}")
for k, t in pub.items():
    s = [x for x in t.split("。") if x]
    print(f"  {len(t):3d}字 文{len(s)} 末尾={t[-22:]} | {t[:30]}…")
print()


def common(a, b, n=8):
    a2 = TEMPLATE.sub("", a); b2 = TEMPLATE.sub("", b)
    out = set()
    for i in range(len(a2) - n + 1):
        if a2[i:i + n] in b2:
            out.add(a2[i:i + n])
    return out


rc = 0
for k, t in cand.items():
    s = [x for x in t.split("。") if x]
    bad = [w for w in BAD if w in t]
    over = {pk: sorted(common(t, pt)) for pk, pt in pub.items() if common(t, pt)}
    ok = 67 <= len(t) <= 100 and any(t.endswith(n) for n in NAMES) and not bad
    print(f"案{k} {len(t)}字 {'✓' if ok else '✗'}  文{len(s)}（{' / '.join(str(len(x)) for x in s)}）  "
          f"事故名と人数={'✓' if any(n in t for n in NAMES) else '✗'}  使わない語={bad or 'なし'}  公開ずみと8字以上の共通={over or 'なし'}")
    print(f"   {t}")
    if not ok and not k.startswith("旧版"):   # 旧版の題は比べるための参考＝止めない
        rc = 1
sys.exit(rc)
