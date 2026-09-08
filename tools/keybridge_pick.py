# -*- coding: utf-8 -*-
"""⑤b-4：カットに当てるショットを決め、`footage.USE` の欄を**機械で書き出す**。

■ なぜ道具にするか
  `start` / `until` / `rate` を手で書くと必ずどこかで写し違える
  （記憶：`rate` は「機械で計算した。手で書いていない」）。
  ここに書くのは **(カットID, クリップ, ショット番号)** の3つだけ。
  秒と `rate` は台帳と尺から計算する。

■ 🔴 端の余白（2026-09-08 ⑤b-4 に実測して決めた）
  ②の境目は `tools/shots.py` が**1秒に1コマ**の標本から出していて、
  `boundaries()` は境目を「**後ろ側の秒**」に置く。
  ＝ ショット `[a, b)` について
     ・`t=a` は**もう新しいショット**（安全）
     ・`t=b` は**もう次のショット**（危険）。本当の切れ目は (b-1, b] のどこか
  → **`until = b - 1.0`**。ここを `b` のままにすると、カットの尻に
    次のショットの絵が最大1秒混じる。`footage.outside_shot()` は同じ台帳を読むので
    **この穴に構造上鳴らない**（[[feedback-gates-blind-spot-is-the-scan-direction]]）。

■ 🔴 台帳に無いスレートを避ける
  1秒の地図（`out/jiko/kb1s/map.json`）で、当てる区間の**全部の秒**が
  「札でない・大きい顔でない」ことを確かめる。台帳のショットの中に
  2秒だけのスレートが埋まっている実例がある（`240401-G-TL908-2303` の 67〜68秒）。

■ 使い方
    python tools/keybridge_pick.py            # 表を検算して USE の本文を書き出す
    python tools/keybridge_pick.py --check    # 検算だけ（書き出さない）
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

import keybridge_shotscan as K                              # noqa: E402

HEAD, TAIL = 0.0, 1.0          # 端の余白（秒）。頭は台帳の作りから 0 でよい

# ── 決めた割り当て（カットID, クリップ, ショット番号, ひとこと）──────────
#   ⚠️ ここに無いカットは**まだ決まっていない**。代用で埋めていない。
AER = "NTSB_B_Roll_Aerial_Imagery_of_Francis_Sc"
INV = "NTSB_B_Roll_Investigators_Aboard_the_Car"
HAZ = "NTSB_B_Roll_Hazardous_Material_Investiga"
PICK = [
    # ── 冒頭 ───────────────────────────────────────────────
    ("pr01", AER, 6, "崩落した中央径間の空撮（2024-03-26）"),
    ("pr02", "240326-G-KH296-2189", 2, "未明・応急艇の操舵席と落ちた橋"),
    ("pr03", AER, 12, "水面に沈んだトラスと橋脚"),
    ("pr05", INV, 29, "NTSB 調査員がトラスを撮る（後ろ姿）"),
    ("pr08", "240330-A-PA223-1001", 5, "ダリの船首に載った橋桁（寄り）"),
    # ── 第2〜5章 ─────────────────────────────────────────
    ("c215", INV, 17, "ダリの船体と凪いだ水面"),
    # 船尾に船名と船籍港（DALI / SINGAPORE）が読める唯一のショット
    ("c301", "240331-A-PA223-1003", 0, "ダリの船尾（船名と船籍港が写る）"),
    ("c318", AER, 28, "橋へ向かう主航路（空撮・広い）"),
    # 操舵室は3ショットしか無く、どれも6〜12秒。**動きの小さいショットを遅回しで使う**
    #   （m=4／m=6。静止に近い絵なので 0.55〜0.60 倍でも遅さが見えない）
    ("c306", HAZ, 41, "ダリの操舵室（窓の外に落ちた橋）"),
    ("c405", HAZ, 44, "航海データ記録装置を吸い出す手元"),
    ("c411", HAZ, 53, "操舵室の操作卓（手元と計器）"),
    ("c409", HAZ, 48, "ダリの船橋（操舵室の中）"),
    ("c424", AER, 27, "橋と主航路（船の長さを見せる広い空撮）"),
    ("c508", AER, 14, "崩落直後の橋（空撮・寄り）"),
    ("c512", AER, 8, "崩落した径間と橋脚（空撮）"),
    ("c517", AER, 26, "崩落した径間（空撮・引き）"),
    ("c519", AER, 16, "水面に散った残骸"),
    # ── 第6〜10章と締め ──────────────────────────────────
    ("c601", AER, 10, "折れた17番橋脚まわり（空撮）"),
    ("c607", AER, 25, "船首の上に載った橋桁"),
    ("c616", "240401-G-TL908-2303", 24, "崩落現場の全景（引きの空撮）"),
    ("c617", "240407-G-DV874-3002", 10, "潰れたコンテナと橋桁（真上から）"),
    ("c619", "240326-G-KH296-2189", 6, "夜明けの現場（応急艇から）"),
    ("c701", AER, 29, "航路に残るダリ（横から）"),
    ("c806", "240401-G-TL908-2303", 20, "現場の空撮（引き）"),
    ("c818", "240401-G-TL908-2303", 12, "橋脚と現場の空撮"),
    ("c819", "240401-G-TL908-2303", 13, "現場の空撮（クレーン台船）"),
    ("c823", AER, 30, "崩落現場（撤去が始まる前）"),
    ("c901", "240401-G-TL908-2303", 22, "塞がった航路（引きの空撮）"),
    ("c903", "240327-A-SE916-1046", 1, "各機関の調査員が船上で支度をする"),
    ("c904", "240404-G-KY623-1002", 5, "潜水士の支度（潜る）"),
    ("c905", "240330-G-LB555-1001", 9, "トラスを溶断する作業員"),
    ("c907", "240407-A-PA223-1003", 6, "コンテナを載せた台船"),
    ("c908", "240401-G-LB555-1002", 1, "仮設航路を通る台船"),
    ("c909", "240407-A-PA223-1005", 2, "トラスを運ぶクレーン台船"),
    ("ca01", AER, 31, "崩落した中央径間（空撮）"),
    ("ep01", AER, 35, "残った桁と崩落部（空撮）"),
    ("ep05", AER, 36, "崩落現場（引きの空撮）"),
]


def cutsecs():
    import scene_jiko as S
    return dict(S.CUTS)


def plan(check_only=False):
    secs = cutsecs()
    m = json.loads((K.SCAN / "map.json").read_text(encoding="utf-8"))
    rows, bad = [], []
    for cid, clip, i, note in PICK:
        sh = K.SHOTS[clip]["shots"][i]
        a, b = sh["start"] + HEAD, sh["until"] - TAIL
        need = secs[cid]
        rate = min(1.0, int((b - a) / need * 100) / 100)
        if rate < 0.55:
            bad.append(f"{cid}: rate {rate} ＝ 遅すぎる（{b - a:.0f}秒 / 尺 {need:.1f}秒）")
        end = a + need * rate
        # 🔴 当てる区間の**全部の秒**を1秒の地図で確かめる（札・大きい顔）
        by = {r["s"]: r for r in m[clip]}
        for s in range(int(a), int(end) + 1):
            r = by.get(s)
            if r is None:
                bad.append(f"{cid}: {clip} {s}秒の地図が無い＝測れていない")
            elif K.is_card(r):
                bad.append(f"{cid}: {clip} {s}秒が札（lum {r['lum']} 文字「{r['text'][:40]}」）")
            elif r["big"] >= 0.25:
                bad.append(f"{cid}: {clip} {s}秒に大きい顔（{r['big']}）")
        rows.append((cid, clip, a, b, rate, need, end, note))
    print(f"■ {len(rows)} 欄／尺の合計 {sum(r[5] for r in rows):.1f}秒")
    for cid, clip, a, b, rate, need, end, note in rows:
        print(f"  {cid}  {clip[:26]:26s} {a:6.1f}→{b:6.1f}"
              f"  尺{need:5.2f} rate {rate:.2f} 尻{end:6.1f}  {note}")
    if bad:
        print(f"\n🔴 {len(bad)} 件")
        for x in bad:
            print("   " + x)
    else:
        print("\n✓ 当てた区間の全部の秒が「札でない・大きい顔でない」")
    if check_only:
        return rows
    out = []
    for cid, clip, a, b, rate, need, end, note in rows:
        r = f", rate={rate:.2f}" if rate < 1.0 else ""
        out.append(f'    # {note}\n'
                   f'    "{cid}": dict(clip="{clip}", start={a:.1f}, '
                   f'until={b:.1f}{r}),')
    dest = K.SCAN / "USE_block.txt"
    dest.write_text("\n".join(out), encoding="utf-8")
    print(f"\n■ USE の本文 → {dest}")
    if "--apply" in sys.argv:
        apply_block("\n".join(out))
    return rows


HEAD_MARK = "    # <<<KB_USE"
TAIL_MARK = "    # KB_USE>>>"


def apply_block(block):
    """🔴 `tools/footage.py` の印の間だけを書き換える。**手で写さない。**

    ⚠️ 印が1つでも見つからなければ**何も書かずに止める**（黙って場所を推測しない）。
    """
    p = Path(__file__).parent / "footage.py"
    s = p.read_text(encoding="utf-8")
    i, j = s.find(HEAD_MARK), s.find(TAIL_MARK)
    if i < 0 or j < 0 or j < i:
        raise SystemExit(f"🔴 印が見つからない（{HEAD_MARK} / {TAIL_MARK}）。何も書かなかった")
    head_end = s.index("\n", i) + 1
    s2 = s[:head_end] + block + "\n" + s[j:]
    p.write_text(s2, encoding="utf-8")
    # 書いたあとに読み直して数を確かめる（書けたつもりで終わらせない）
    import importlib
    import footage
    importlib.reload(footage)
    print(f"■ footage.USE を書き換えた → {len(footage.USE)} 欄")


if __name__ == "__main__":
    plan("--check" in sys.argv)
