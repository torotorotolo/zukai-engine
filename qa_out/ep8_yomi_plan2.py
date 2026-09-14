# -*- coding: utf-8 -*-
r"""ep8_yomi_plan2.py — A/B の2周目。1周目で**効かなかった／悪化した**ものに別の書き方を当てる。

  python qa_out/ep8_yomi_plan2.py            … 検算して qa_out/ep8_yomi_plan2.json を書く
  python qa_out/ep8_yomi_plan2.py --show     … 表だけ

🔴 1周目で分かったこと（reference-elevenlabs-tts の「かな書き＝正解とは限らない」の実例）:
   離陸→りりく が『リリック』／積み荷→つみに が『隅の』／計算→けいさん が『Kさん』／
   黙とう→もくとう が『供養』／NASA→ナサ が『母』。**かな化は悪化する側にも倒れる。**
   そこで2周目は「かなにせず、**アクセント句を半角空白で切るだけ**」を主に試す。

⚠️ 検算は1周目と同じ（キーが台本に当たる／当たる行数が想定どおり／読点を足していない）。
⚠️ 1周目で辞書に入れた語は `el_text()` を通った時点でもう置換されている。
   ここのキーは**置換の影響を受けない部分**を選んである（例＝c210-1 は「〜」ではなく「920キロ」）。
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")

PLAN = [
    # ── かな化で悪化した → 空白で句を切るだけにする ──────────────────
    ("c212-2", "離陸から追い", "りりく から追い", 1, "かな『りりく』は『リリック』になった。空白を足す"),
    ("c403-1", "積み荷の実験", "積み荷 の実験", 1, "かな『つみに』は『隅の』になった。⚠️『積荷』はかなもカナも罪人（4本目）"),
    ("c511-1", "計算のほうは", "けいさん のほうは", 1, "かな続きだと『Kさん』。空白で切る"),
    ("c411-2", "黙とうをささげて", "もくとう をささげて", 1, "かな『もくとう』は『供養』になった"),
    ("c617-2", "NASAは確かめ", "NASA は確かめ", 1, "カナ『ナサ』は『母』になった。英字のまま空白で切る"),
    ("c807-2", "広さを当たった", "広さを 当たった", 1, "かな『あたった』は効かなかった。漢字のまま空白で切る"),
    ("c520-3", "15通りの経路", "ジュウゴ とおりの経路", 1, "『十も通り』のまま。カナと空白を両方"),
    ("c615-1", "チタンの小片", "チタンの しょうへん", 1, "『チタンの小刀』＝1周目は塞ぐ材料しか直していない"),
    ("c902-3", "8枚目の下半分", "8枚目の したはんぶん", 1, "『八枚目の一半分』＝1周目は破ったのはしか直していない"),
    # ── 数（1周目で効かなかった／悪化した）──────────────────────
    ("c710-2", "約4,400度", "約 ヨンセンヨンヒャク度", 1, "『四四〇〇度』＝1桁ずつ読んだ疑い。空白＋カナ"),
    ("c811-2", "83,900点", "ハチマンサンゼンキュウヒャクてん", 1, "🔴 かな混じりは『八幡さん、1900点』に悪化。全部カナで"),
    ("c316-1", "1,052キロ", "センゴジュウニキロ", 1, "🔴 見積りを直したら『一点五十二』に化けた＝数も固定する"),
    ("c210-1", "920キロ", "キュウヒャクニジュウキロ", 1, "🔴『六七〇から九二〇』＝1桁ずつ読んだ疑い。⚠️『〜』は辞書で から になっている"),
    ("c210-1", "約670", "約 ロッピャクナナジュウ", 1, "同上（前半）"),
    # ── 同じ文字列でも行で結果が逆だった（7本目のラングレー型）→ 行ごとに分ける ──
    ("pr02-2", "号は、9時00分18秒", "号は、クジ ゼロフン ジュウハチビョウ", 1,
     "1周目は『9時00分18秒』を両行に当てて pr02-2 は良化・c725-1 は悪化。**pr02-2 だけ**に絞る"),
]


def main():
    import el_script as ES
    lines = {l.lid: l.text for l in ES.lines()}
    allt = [l.text for l in ES.lines()]
    bad, out = [], []
    for lid, key, val, want, why in PLAN:
        t = lines.get(lid)
        if t is None:
            bad.append(f"{lid}: 台本に無い行ID")
            continue
        if key not in t:
            bad.append(f"{lid}: key「{key}」がその行に当たらない → {t}")
            continue
        hits = sum(1 for x in allt if key in x)
        if hits != want:
            bad.append(f"{lid}: key「{key}」の当たる行数 {hits}（想定 {want}）")
        if "、" in val and val.count("、") != key.count("、"):
            bad.append(f"{lid}: val に読点を足している: {val}")
        # 🔴 1周目の辞書を通したあとに key が残っているか（残っていないと A/B が空振りする）
        sent = ES.el_text(t)
        if key not in sent:
            bad.append(f"{lid}: key「{key}」は EL_YOMI 適用後の送信文に無い（辞書とぶつかっている）\n"
                       f"      送信文: {sent}")
        mark = "  " if hits == want else "🔴"
        print(f"{mark}{lid:<9}{hits:>3}/{want:>3}  「{key}」→「{val}」")
        out.append({"id": lid, "key": key, "val": val, "why": why})
    print(f"\n候補 {len(out)}件")
    if bad:
        print(f"\n🔴 直すところ {len(bad)}件:")
        for b in bad:
            print("   " + b)
        return 1
    if "--show" not in sys.argv:
        p = ROOT / "qa_out" / "ep8_yomi_plan2.json"
        p.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"→ {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
