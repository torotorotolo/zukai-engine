# -*- coding: utf-8 -*-
"""17本目④'：タイトル案を機械で数え、公開ずみの題（全数）と型を照合する（ルール 4'-8・§B4）。読むだけ。
    python ref/ep17/v2_build/titles17.py
公開ずみ＝ref/ep14/v2_build/titles.json（12本・videoId→題）＋config/meta_ep13.json の title（13本目）。
案＝同じフォルダの titles17.json（{"A": "…", …}）。
見ること：字数（len・67〜94・上限100）／末尾「の真相【事故検証】」／「264人が亡くなった中華航空140便墜落事故」を含む／
      文の数（。で割る）／【映像あり】を付けない（この回は無し）／死の語・煽り語／公開ずみの題と同じ語句（8字以上の共通部分）。
"""
import json, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
S = Path(__file__).resolve().parent
ROOT = S.parents[2]
pub = dict(json.load(open(ROOT / "ref/ep14/v2_build/titles.json", encoding="utf-8")))
pub["ep13"] = json.load(open(ROOT / "config/meta_ep13.json", encoding="utf-8"))["title"]
cand = json.load(open(S / "titles17.json", encoding="utf-8"))
NAME = "264人が亡くなった中華航空140便墜落事故の真相【事故検証】"
BAD = ["死亡", "即死", "絶命", "地獄", "瞬間", "【映像あり】"]
TEMPLATE = re.compile(r"(\d[\d,]*人|乗員\d+名|\d+名)(が亡くなった|を失った|喪失|が被曝した)|の真相【事故検証】|【映像あり】|【事故検証】")

L = [len(t) for t in pub.values()]
print(f"公開ずみ {len(pub)}本：字数 最短{min(L)}・最長{max(L)}・中央値{sorted(L)[len(L)//2]}")
for k, t in pub.items():
    s = [x for x in t.split("。") if x]
    print(f"  {len(t):3d}字 文{len(s)} 末尾={'真相【事故検証】' if t.endswith('の真相【事故検証】') else t[-14:]} | {t[:34]}…")
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
    ok = 67 <= len(t) <= 94 and t.endswith(NAME) and not bad
    print(f"案{k} {len(t)}字 {'✓' if ok else '✗'}  文{len(s)}（{' / '.join(str(len(x)) for x in s)}）  "
          f"事故名と人数={'✓' if NAME in t else '✗'}  使わない語={bad or 'なし'}  公開ずみと8字以上の共通={over or 'なし'}")
    print(f"   {t}")
    if not ok:
        rc = 1
sys.exit(rc)
