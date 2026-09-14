# -*- coding: utf-8 -*-
r"""ep8_verdicts.py — 台帳の「疑い」127行に**扱い**を1行ずつ付ける（⑤a・8本目）。

  python qa_out/ep8_verdicts.py            → audio/el_qa/ep8_verdicts.tsv
  python qa_out/ep8_verdicts.py --selftest → 分け方の対照（ファイルを読まない）

🔴 扱いの決め方（上から順に当てる。**下に落ちたものが要耳**）:
  ① EL_YOMI が当たっている行 … 送っている文字列が かな／カナ なので**音は確定**。
     ⚠️ ただし「直った」ことは 2周目・3周目の聞取で確かめてある（当てただけでは決着ではない）
  ② `el_reading_diff` が **読み一致**と言う行 … Scribe／janome の**字の当て違い**。直さない
  ③ 数の所見だけで、聞取に**漢数字で同じ数**が出ている行 … 表記のゆれ
  ④ 1周目と2周目で**片方だけ崩れた**行 … 同じ音を2回起こして結果が違う＝**Scribe の揺れ**。
     ⚠️ 音は1バイトも触っていない（キャッシュから同じ pcm）。**2周とも崩れたものだけ直す**
  ⑤ 異音の門番が unsure／real の行 … `el_artifact_words` で語の時刻に当てて判定ずみ
  ⑥ ここまでで決まらないもの → **要耳**（⑥の試写でカズヤくんが聴く）

⚠️ 「扱いが付いた＝正しい」ではない。**未判定を0にして、疑いの行に理由を残す**ための表。
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
Q = ROOT / "audio" / "el_qa"

# ⑥ 要耳に落とす行に、疑いの中身を人（Claude）が1行で書く。ここに無い行が要耳に落ちたら
#    「理由が書かれていない要耳」なので、走らせた人が必ず気づく（fail closed）。
YOUMIMI = {
    "c212-2": "「離陸から」が『陸から』＝**頭の1字が落ちる**。かな『りりく』は『リリック』・"
              "空白版『りりく から』も『リリク』で直らなかった（A/B 2通り）。字幕は出る",
    "c403-1": "「積み荷の実験」が『SM2の実験』。かな『つみに』は『隅の』・空白版『積み荷 の実験』は"
              "『隅々の』で、どちらも悪化。⚠️ 4本目でも「積荷」は かな もカナも罪人だった語",
    "c511-1": "「計算のほうは」が『理恵さんの方は』。かな『けいさん』は『Kさん』・空白版も『Kさん』",
    "c411-2": "「黙とうをささげて」が『ダマトウを』。かな『もくとう』は『供養』・空白版は『苦闘』で悪化",
    "c807-2": "「広さを当たった」が『広さを渡った』。かな『あたった』も空白版『広さを 当たった』も効かず。"
              "⚠️「当たった」は本文12行あり、崩れるのはこの行だけ",
    "c509-2": "「記録には」が2周目だけ『浩久には』。A/B の前後とも『記録には』100%＝**Scribe の揺れ**"
              "と見たが、行頭なので念のため。かな化はしていない（正しく読めている語をかな化しない）",
    "c520-1": "「前のふち用の式」が『前のフチ用の**指揮**』。**式も指揮も シキ で読みは同じ**なので"
              "機械では直せない。字幕は出るが、耳だけだと取り違える恐れ",
    "c204-1": "異音の門番が unsure（3テイクとも末尾に音）。語の時刻に当てると『入|っ|た』＝"
              "**促音に重なる本物の語**と確定したが、テイクごとに形が違ったので念のため",
    "c916-2": "異音の門番が real（3テイクとも 3.25秒に音）。語の時刻に当てると『急げ|と』＝"
              "**読点の間のあとの破裂音**と確定。⚠️ この回の締めに近い決め所なので耳で",
    "c220-2": "「約48×30センチ」の **×**。聞取は『四十八かける三十』＝音は取れているが、"
              "台本でこの行だけ寸法が記号（他は「長さ約61センチ、幅約38センチ」と言葉書き）",
    "pr10-1": "「乗員の最期の…」が『**上院**の最期の…』。**乗員も上院も ジョウイン で読みは同じ**。"
              "NASA と議会が出てくる回なので、耳だけだと取り違える恐れ（字幕は出る）",
}


def build():
    import el_script as ES
    lines = {l.lid: l.text for l in ES.lines()}
    yomi_hit = {}
    for l in ES.lines():
        h = []
        ES.el_text(l.text, h)
        if h:
            yomi_hit[l.lid] = "／".join(f"{a}→{b}" for a, b, _ in h)

    def tsv(p, key="場面"):
        if not Path(p).exists():
            raise SystemExit(f"🔴 まだ無い: {p}")
        return {r[key]: r for r in csv.DictReader(Path(p).read_text(encoding="utf-8").splitlines(),
                                                  delimiter="\t")}

    r1 = tsv(Q / "ep8_el_yomi_round1.tsv")
    r2 = tsv(Q / "ep8_el_yomi.tsv")
    rd = tsv(Q / "ep8_reading_diff.tsv", "行")
    retakes = tsv(Q / "ep8_el_retakes.tsv", "scene")

    def ratio(d, lid):
        try:
            v = float(d[lid]["一致率"])
        except Exception:
            return -1.0
        return v * 100 if v <= 1.0 else v

    # 台帳と同じ「疑い」の定義＝一致率90%未満 か 所見あり
    def numbers_missing(lid):
        from check_numbers_heard import heard_numbers
        import re
        got = heard_numbers(r2[lid]["聞こえた文"])
        miss = []
        for m in re.findall(r"\d+(?:\.\d+)?", lines[lid]):
            cand = {m, m.rstrip("0").rstrip(".") if "." in m else m}
            if not (cand & got):
                miss.append(m)
        return miss

    out, kinds = [], {}
    for lid in lines:
        # 🔴 台帳の「一致率90%未満」だけでは**本物の崩れを取り逃がす**（2026-09-14 実測）。
        #    c212-2「離陸から」→『陸から』は **2周とも崩れている**のに 91.9% で網の外だった。
        #    読みの照合（el_reading_diff）と、2周のあいだの動きも疑いに入れる。
        #    → [[feedback-gates-blind-spot-is-the-scan-direction]]
        sus = (ratio(r2, lid) < 90.0 or lid in yomi_hit or lid in retakes or numbers_missing(lid)
               or rd.get(lid, {}).get("判定") == "読みが違う"
               or abs(ratio(r1, lid) - ratio(r2, lid)) >= 3.0)
        if not sus:
            continue
        if lid in YOUMIMI:
            k, why = "要耳", YOUMIMI[lid]
        elif lid in yomi_hit:
            k = "音は確定（EL_YOMI でかなを送っている）"
            why = f"EL_YOMI『{yomi_hit[lid]}』を送信＝音は確定。2周目・3周目の聞取で直りを確認ずみ"
        elif rd.get(lid, {}).get("判定") == "読み一致":
            k = "表記のゆれ（別の検査で決着）"
            why = "台本と聞取の**読みが一致**（el_reading_diff）＝字の当て方の違いだけ"
        elif lid in retakes:
            k = "異音は本物の語（語の時刻で判定）"
            why = f"振り直し {retakes[lid]['decision']}。el_artifact_words で促音・破裂音と確定"
        elif abs(ratio(r1, lid) - ratio(r2, lid)) >= 3.0:
            k = "Scribe の揺れ（2周のうち片方だけ）"
            why = (f"同じ音（キャッシュの pcm）を2周起こして {ratio(r1,lid):.0f}% → {ratio(r2,lid):.0f}%。"
                   "**音は1バイトも触っていない**＝2周とも崩れたものだけ直す規則により、直さない")
        elif numbers_missing(lid):
            k = "数は漢数字で出ただけ（表記のゆれ）"
            why = f"聞取に漢数字で同じ数が出ている（照合が拾えないのは桁区切りのカンマ）: {numbers_missing(lid)}"
        else:
            k = "一致率だけが低い（読みは一致）"
            why = f"一致率 {ratio(r2,lid):.0f}%。読みの照合は一致（el_reading_diff）＝字の当て方の違い"
        kinds[k] = kinds.get(k, 0) + 1
        out.append((lid, k, why))

    out.sort(key=lambda r: list(lines).index(r[0]))
    p = Q / "ep8_verdicts.tsv"
    p.write_text("行\t扱い\t理由\n" + "\n".join("\t".join(r) for r in out) + "\n", encoding="utf-8")
    print(f"疑い {len(out)}行 → {p.name}")
    for k, v in sorted(kinds.items(), key=lambda x: -x[1]):
        print(f"  {v:>4}  {k}")
    missing_why = [lid for lid, k, _ in out if k == "要耳" and lid not in YOUMIMI]
    if missing_why:
        print(f"🔴 理由の無い要耳: {missing_why}")
        return 1
    unused = [lid for lid in YOUMIMI if lid not in {r[0] for r in out}]
    if unused:
        print(f"🔴 YOUMIMI に書いたが疑いに入っていない行: {unused}（台帳と食い違う）")
        return 1
    return 0


def selftest():
    fails = []
    ok = lambda c, n: (None if c else fails.append(n))
    ok(len(YOUMIMI) >= 1, "要耳の理由が1件以上ある")
    ok(all(len(v) > 20 for v in YOUMIMI.values()), "要耳の理由が一言で終わっていない")
    ok(all("\t" not in v and "\n" not in v for v in YOUMIMI.values()), "tsv を壊す文字が無い")
    if fails:
        print(f"selftest: 落ちた: {fails}")
        return 1
    print(f"selftest: 3/3 合格（要耳 {len(YOUMIMI)}件・ファイルを読んでいない）")
    return 0


if __name__ == "__main__":
    unknown = [a for a in sys.argv[1:] if a.startswith("--") and a != "--selftest"]
    if unknown:
        raise SystemExit(f"🔴 知らない引数: {unknown}")
    sys.exit(selftest() if "--selftest" in sys.argv else build())
