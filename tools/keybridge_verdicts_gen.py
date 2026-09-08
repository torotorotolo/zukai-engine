# -*- coding: utf-8 -*-
r"""keybridge_verdicts_gen.py — ⑤a 台帳の「扱い」欄（verdicts_manual.tsv）を、根拠つきで組む。

  python tools/keybridge_verdicts_gen.py          … audio/el_qa/keybridge_verdicts_manual.tsv を書く

🔴 なぜ手で書かずに道具にするか:
   扱いは「この行はこう決めた」という**判断の記録**なので、あとから
   「なぜそう決めたか」を1行ずつ引けないと意味がない（[[feedback-one-finding-one-defect]]）。
   語ごとの根拠をここに1回だけ書き、当たる行には機械で配る。手で並べると必ず取り違える。

⚠️ ここに書いてよいのは「**実測で決着した**」ものだけ。決着していないものは要耳へ回す
   （[[feedback-no-ear-checks-until-shisha]]＝途中で耳の確認を依頼せず、試写でまとめて聴いてもらう）。
"""
import pathlib
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import el_script as ES  # noqa: E402

# ── ① 「音は正しく、Scribe が字を当て違えているだけ」と実測で決着した語 ──────────────
#    値＝その根拠。行に当たれば「表記のゆれ」として扱う。
SCRIBE_ONLY = {
    "径間": "A/B『けいかん』で前『三計観』後『三径間』＝どちらも読みは ケイカン（音は同じ・字だけ違う）",
    "耐力": "聞取『体力』＝たいりょく（同じ読み）",
    "防衝工": "聞取『防衝構／某商工』＝ぼうしょうこう（同じ読み）。A/B で全部かなにすると逆に『王昭君』で悪化した",
    "遮断器": "聞取『遮断機』＝しゃだんき（同じ読み）",
    "解析器": "聞取『解析機』＝かいせきき（同じ読み）",
    "補修班": "聞取『保守班／保守派』だが el_probe_words の実測 0.681秒 ≒5.7モーラ＝ほしゅうはん（5）で ほしゅはん（4）でない",
    "航路": "聞取『坑道』だが el_probe_words の実測 0.280秒 ≒2.6モーラ＝こうろ（3）で こうどう（4）でない",
    "舶用軽油": "聞取『柏葉桂油』＝はくようけいゆ（同じ読み）",
    "操舵": "聞取『ソーダ／SODA』＝そうだ（同じ読み）。A/B でかなにすると『そうだ、ポンプ』と間が入って悪化",
    "航海": "聞取『後悔／公開』＝こうかい（同じ読み）",
    "外航船": "聞取『外交船』＝がいこうせん（同じ読み）。EL_YOMI『がいこう船』で送っている",
    "船首": "聞取『選手』＝せんしゅ（同じ読み）",
    "橋まで": "聞取『端まで』＝はし（同じ読み）",
    "橋までは": "聞取『端までは』＝はし（同じ読み）",
    "あいだ": "聞取『間』＝表記のゆれ",
    "このあと": "聞取『この後』＝表記のゆれ",
    "隻数": "EL_YOMI『せきすう』で送っている＝音は決まっている。聞取『積雪』は Scribe の字",
    "指針": "EL_YOMI『ししん』で送っている＝音は決まっている。聞取『地震』は Scribe の字（c815-1 では『指針』と出た）",
    "端子台": "A/B で『たんし台』にして 唐時代（とうじだい）→ 端次第（たんしだい）＝読みは直った",
    "引外し": "A/B『ひきはずし装置』で聞取『引き外し装置』＝直った",
    "録れる": "聞取『取れる』＝とれる（同じ読み）",
}

# ── ② 実測で決着せず、試写で耳に回す行（場面ID → 疑いの中身）──────────────────
#    ⚠️ 「直したつもり」で閉じない。ここに載せた行は要耳一覧に秒つきで出る。
YOUMIMI = {
    "c108-1": "文頭『両端（りょうたん）』が聞取『両橋』。A/B でかな化すると『ビョータン』でさらに悪化＝直す手が無い",
    "c313-3": "文頭『端子台』が聞取『探師台』。行中の端子台は『端次第』で正しいので、文頭だけ弱い",
    "c414-1": "『上級水先人』が聞取『上級推薦人』。EL_YOMI で かな『みずさきにん』を送っており音は決まっているが、同じ語で2行続けて出たので念のため",
    "c421-2": "同上（c414-1 と同じ型）。加えて『投げよ』が『投げよう』に伸びて聞こえた",
    "c423-2": "『主機関』が聞取『指揮官』＝しゅ→し。ほかの行では『手記感（しゅきかん）』で正しいのでテイク差",
    "c520-1": "『艇（てい）』が聞取『点（てん）』。A/B で空白を入れると『テイ』と直るが、同じ行の『橋脚』が『漂着』に崩れた＝差し引きで採らず",
    "c615-2": "文頭『寄与要因』。かな4通り（きよ要因／きよ よういん／きよよういん は／全部かな）すべて別語になり、決着せず",
    "c820-2": "文頭『外航船』が聞取『外港、船』＝語の途中に間が入った。かな『がいこうせん』にすると濁点が落ちて『海溝線』で悪化",
    "c821-1": "『当たられて』が聞取『渡られて』＝意味が変わる。空白・カナの2通りとも効かず",
    "c824-2": "文頭『キー橋』が聞取『ヒー橋』。ほかの行のキー橋は正しい＝文頭だけ弱い",
    "c916-3": "文頭『主航路』が聞取『西航路』。EL_YOMI で かな『しゅこうろ』を送っており、c104-2 では『主航路』と出た＝テイク差",
    "ca12-2": "文頭『寄与要因』（c615-2 と同じ語・同じ型）",
}


# ── ③ 機械で閉じられる型（語ごとの表ではなく、**別の検査の結果**で閉じる）──────────────
def _artifact_ok():
    """異音の語照合（el_artifact_words）で『重なる語』が見つかった行。
    🔴 過去2本と同じく、この回も **「語なし」＝本物の異音は 0件**（76行すべて促音・破裂音に重なった）。
    ⚠️ ログが1本でも欠けていたら止める（読めない物を「合格」にしない＝fail closed）。"""
    ok, seen = set(), set()
    logs = sorted(pathlib.Path("qa_out").glob("kb_artwords*.log"))
    if not logs:
        raise SystemExit("🔴 異音の語照合のログが無い（先に el_artifact_words.py）")
    for f in logs:
        cur = None
        for l in f.read_text(encoding="utf-8", errors="replace").splitlines():
            if l.startswith("=== "):
                cur = l.split(" ")[1]
                seen.add(cur)
            elif cur and ("重なる語" in l or "異音の所見なし" in l):
                if "（語なし）" not in l:
                    ok.add(cur)
    return ok, seen


def _reading_match():
    """el_reading_diff --all の『読み一致』行。**台本と聞取の読みが同じ＝誤読ではない**。"""
    import el_script as ES
    p = ES.qa_path("reading_diff.tsv")
    rows = p.read_text(encoding="utf-8").splitlines()[1:]
    if len(rows) < len(ES.lines()):
        raise SystemExit(f"🔴 reading_diff.tsv が全行ぶん無い（{len(rows)}／{len(ES.lines())}）。"
                         "`el_reading_diff.py --all` を回すこと")
    return {l.split("	")[0] for l in rows if l.split("	")[1] == "読み一致"}


def main():
    lines = ES.lines()
    art_ok, art_seen = _artifact_ok()
    rd_ok = _reading_match()
    print(f'異音の語照合 {len(art_seen)}行（語に重なる {len(art_ok)}）／読み一致 {len(rd_ok)}行')
    rows = []
    for ln in lines:
        if ln.lid in YOUMIMI:
            rows.append((ln.lid, "要耳（機械で決着せず）", YOUMIMI[ln.lid]))
            continue
        why = [f"{w}＝{r}" for w, r in SCRIBE_ONLY.items() if w in ln.text]
        if why:
            rows.append((ln.lid, "表記のゆれ（音は正しいと実測）", "／".join(why)[:300]))
            continue
        # ③ 別の検査の結果で閉じる（語の表に頼らない）
        m = []
        if ln.lid in art_ok:
            m.append("異音は語に重なる（促音・破裂音）＝el_artifact_words で『語なし』0件")
        if ln.lid in rd_ok:
            m.append("台本と聞取の**読みが一致**（el_reading_diff）＝字の当て方の違いだけ")
        if m:
            rows.append((ln.lid, "表記のゆれ（別の検査で決着）", "／".join(m)))
    miss = [k for k in YOUMIMI if k not in {l.lid for l in lines}]
    if miss:
        raise SystemExit(f"🔴 台本に無い行IDを要耳に書いている（書き損じ）: {miss}")
    out = ES.qa_path("verdicts_manual.tsv")
    out.write_text("行\t扱い\t理由\n" + "\n".join("\t".join(r) for r in rows) + "\n", encoding="utf-8")
    print(f"扱い {len(rows)}行（要耳 {len(YOUMIMI)}／表記のゆれ {len(rows)-len(YOUMIMI)}） -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
