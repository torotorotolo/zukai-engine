# -*- coding: utf-8 -*-
"""24本目 ⑥：Modal と同じ条件（GITHUB_ACTIONS なし＝仮の字を使わない）で、写真の全カットの出典の行を組み立てる
（17本目 credits_sim17.py・credwidth17.py の型を1本にまとめた）。名前は出さない（字数・幅・有無だけ）。
⑥（10-24）の結果＝作者の印の写真 29/29・例外0・タグ0・画面の外0（いちばん長い c511 840px）・陽性対照 タグ29／表なし29／長い名乗り5で鳴る。
次の回は EP24_CREDIT・_ep24_author・_EP24_PRIVATE をその回の名に替えて写す（scratchpad は会話ごとに消える＝リポに残した）。
  ・印が残っていないか・仮の字が無いか・タグや & が無いか・例外が無いか
  ・作者の名前の入った行の幅（全画面＝左の MG から右へ・額装＝右の RIGHT から左へ）が画面の内側か
  ・photo／ground 以外の鍵（tail・dual など）で印の写真を使うカットも数える
使い方: cd <repo> && python <this> [--pos]
  --pos＝陽性対照（作者欄にタグを残す直す前のふるまい／表が無いとき）＝鳴れば exit 0"""
import os
import sys

os.environ.pop("GITHUB_ACTIONS", None)
sys.path.insert(0, "tools")
import scene_jiko as S  # noqa: E402
import fontmetrics as fm  # noqa: E402
import jiko_style as J  # noqa: E402

marked = {k for k, v in S.EP24_CREDIT.items() if "{作者}" in v}


def walk(o, path=""):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from walk(v, f"{path}.{k}")
    elif isinstance(o, (list, tuple)):
        for i, v in enumerate(o):
            yield from walk(v, f"{path}[{i}]")
    elif isinstance(o, str):
        yield path, o


def run(quiet=False):
    bad, auth, other, n, widths = [], [], [], 0, []
    for cid in S.ORDER:
        sp = S.SPEC.get(cid) or {}
        for p, s in walk(sp):
            if s in marked and p not in (".photo", ".ground.photo"):
                other.append((cid, p, s.split("/")[-1]))
        if not sp.get("photo"):
            continue
        n += 1
        try:
            cr = S.credit_of(cid, sp)
        except Exception as e:  # noqa: BLE001
            bad.append((cid, type(e).__name__, str(e)[:120]))
            continue
        if any(ch in cr for ch in "<>&"):
            bad.append((cid, "html", f"出典の行にタグか & が残る（{len(cr)}字）"))
        uses = [x for x in (sp.get("photo"), (sp.get("ground") or {}).get("photo")) if x in marked]
        if uses:
            ok = ("{作者}" not in cr) and (S.EP23_AUTHOR_STANDIN not in cr)
            w = fm.width(cr, 24, "Noto")
            if sp.get("panel"):
                edge, over = J.RIGHT - w, -(J.RIGHT - w)            # 左端が 0 より左なら外
            else:
                edge, over = J.MG + w, (J.MG + w + 14) - 1920        # 暗い地の右端（＋14）が 1920 を超えたら外
            widths.append((over, cid, "額装" if sp.get("panel") else "全画面", round(w), round(edge)))
            auth.append((cid, ok, uses))
        elif "{作者}" in cr or S.EP23_AUTHOR_STANDIN in cr:
            bad.append((cid, "stray", "印か仮の字が残る"))
    outside = [x for x in widths if x[0] > 0]
    if not quiet:
        print(f"SPEC のカット {len(S.ORDER)}・写真のカット {n}・作者の印のある写真 {len(marked)} 点・それを使うカット {len(auth)}・例外と残り {len(bad)}")
        print(f"物差しの検算: 「あ」×10 24px = {round(fm.width('あ' * 10, 24, 'Noto'))}・MG={J.MG}・RIGHT={J.RIGHT}")
        for over, cid, kind, w, edge in sorted(widths, reverse=True):
            print(f"  {cid}\t{kind}\t幅 {w}px\t{'左端' if kind == '額装' else '右端'} x={edge}\t画面の端まで {-over}px")
        used = sorted({u for _, _, us in auth for u in us})
        print(f"使われた印の写真 {len(used)}/{len(marked)}・使われていない {sorted(m.split('/')[-1] for m in marked - set(used))}")
        print(f"photo／ground 以外の鍵で印の写真を使うカット {len(other)}")
        for o in other:
            print("  ⚠️", o)
        for b in bad:
            print("  NG", b)
        print(f"画面の外 {len(outside)}・印か仮の字が残る {sum(1 for _, ok, _ in auth if not ok)}")
    return bad, auth, outside


if "--pos" in sys.argv:
    real = S._ep24_author
    S._ep24_author = lambda name: '<a href="x">' + real(name) + "</a>"     # 直す前のふるまい（タグを残す）
    b1, _, _ = run(quiet=True)
    S._ep24_author = real
    keep = S._EP24_PRIVATE
    S._EP24_PRIVATE = S.HERE / "ref" / "ep24" / "src" / "__none__.tsv"     # 表が無い（保管庫に置き忘れ）
    b2, _, _ = run(quiet=True)
    S._EP24_PRIVATE = keep
    S._ep24_author = lambda name: "W" * 60                                  # 長すぎる名乗り＝画面の外
    _, _, o3 = run(quiet=True)
    S._ep24_author = real
    print(f"陽性対照: タグ {len(b1)} 件鳴る・表なし {len(b2)} 件鳴る・長い名乗り {len(o3)} 件が画面の外")
    sys.exit(0 if (b1 and b2 and o3) else 1)

bad, auth, outside = run()
sys.exit(1 if (bad or outside or not all(ok for _, ok, _ in auth)) else 0)
