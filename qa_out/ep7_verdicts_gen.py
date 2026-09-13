# -*- coding: utf-8 -*-
r"""ep7_verdicts_gen.py — ⑤a 台帳の「扱い」欄（verdicts_manual.tsv）を、根拠つきで組む（この回かぎり）。

🔴 なぜ手で書かずに道具にするか:
   扱いは「この行はこう決めた」という**判断の記録**なので、あとから「なぜそう決めたか」を
   1行ずつ引けないと意味がない。語ごとの根拠をここに1回だけ書き、当たる行には機械で配る。
   手で 170行並べると必ず取り違える。

⚠️ ここに書いてよいのは「**実測で決着した**」ものだけ。決着していないものは要耳へ回す
   （[[feedback-no-ear-checks-until-shisha]]＝途中で耳の確認を依頼せず、試写でまとめて聴いてもらう）。

  python qa_out/ep7_verdicts_gen.py
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import el_script as ES  # noqa: E402

# ── ① 「音は正しく、Scribe が字を当て違えているだけ」と実測で決着した語 ────────────────
SCRIBE_ONLY = {
    "交信": "聞取『更新』＝こうしん（同じ読み）。2行とも",
    "一次レーダー": "聞取『一時レーダー』＝いちじ（同じ読み）。⚠️ 同音なので c210-1 は要耳にも載せた",
    "二次レーダー": "聞取『虹レーダー』＝にじ（同じ読み）",
    "録られ": "聞取『撮られ』＝とられ（同じ読み）",
    "跡は": "聞取『後は』＝あと（同じ読み）",
    "あいだ": "聞取『間』＝表記のゆれ（janome が カン／マ と読むだけ）",
    "そのあと": "聞取『その後』＝表記のゆれ",
    "のあと": "聞取『の後』＝表記のゆれ",
    "じゅう": "聞取『中』＝じゅう（表記のゆれ）",
    "分から": "聞取『わから』＝表記のゆれ",
    "分かって": "聞取『わかって』＝表記のゆれ",
    "分かった": "聞取『わかった』＝表記のゆれ",
    "造り": "聞取『作り』＝つくり（同じ読み）",
    "無い": "聞取『ない』＝表記のゆれ",
    "行って": "EL_YOMI『おこなって』で送っている＝音は決まっている",
    "棟": "聞取『頭／等／塔』＝とう（同じ読み）。N棟＝ななとう／にとう で正しい",
    "機目": "聞取『期目』＝いっき／にき（同じ読み）",
    "減った": "EL_YOMI『へった』で送っている＝音は決まっている（前は『欠いた』『蹴った』）",
    # かな↔漢字の表記違いだけ（janome が別の読みを当てるので『読みが違う』側に落ちるが、耳では同じ）
    "エックス線": "聞取『X線』＝エックスせん（同じ読み）",
    "のちに": "聞取『後に』＝のちに（同じ読み）",
    "出どころ": "聞取『出所』＝でどころ（同じ読み）",
    "いちばん": "聞取『一番』＝いちばん（同じ読み）",
    "からになった": "聞取『空になった』＝からになった（同じ読み）",
    "そのほかに": "聞取『その他に』＝そのほかに（同じ読み）",
    "4万人": "聞取『四万人』＝よんまんにん（同じ読み。数の検査は 4 と 四 を別物に数える）",
}

# ── ①' EL_YOMI で **かな／カナを送っている**語（＝音は確定。Scribe の字は当てにしない）──────
#    🔴 これがこの回いちばん多い型。送信文が かな なら、聞取が別の字でも**読みは動かない**。
SENT_KANA = {
    "管制": "EL_YOMI『かんせい』で送信＝音は確定（聞取『感性／慣性／完成／官政』は Scribe の字）",
    "管制官": "EL_YOMI『かんせいかん』で送信＝音は確定",
    "防空司令部": "EL_YOMI『ぼうくう司令部』で送信＝音は確定（前は『航空司令部』で意味が反転していた）",
    "北棟": "EL_YOMI『きたとう』で送信＝音は確定（聞取『北塔』）。⚠️ 読み方の決定そのものは要耳へ",
    "南棟": "EL_YOMI『みなみとう』で送信＝音は確定",
    "報せ": "EL_YOMI『しらせ』で送信＝音は確定（聞取『知らせ』）",
    "墜ち": "EL_YOMI『おち』で送信＝音は確定（聞取『落ち』）",
    "便名": "EL_YOMI『びんめい』で送信＝音は確定",
    "客室": "EL_YOMI『きゃくしつ』で送信＝音は確定",
    "五角形": "EL_YOMI『ごかっけい』で送信＝音は確定",
    "猶予": "EL_YOMI『ゆうよ』で送信＝音は確定",
    "当直室": "EL_YOMI『とうちょく室』で送信＝音は確定",
    "滑走路": "EL_YOMI『かっそうろ』で送信＝音は確定",
    "誘導路": "EL_YOMI『ゆうどうろ』で送信＝音は確定",
    "分単位": "EL_YOMI『ふんたんい』で送信＝音は確定",
    "刃渡り": "EL_YOMI『はわたり』で送信＝音は確定",
    "言葉": "EL_YOMI『ことば』で送信＝音は確定",
    "首都の": "EL_YOMI『しゅとの』で送信＝音は確定",
    "2001年": "EL_YOMI『にせんいちねん』で送信＝音は確定（前は『2010年』）",
    "F-15": "EL_YOMI『エフじゅうご』で送信＝音は確定（前は『F3』）",
    "ボーイング757": "EL_YOMI『ボーイングななごなな』で送信＝音は確定（前は『707』）",
    "の側": "EL_YOMI『の がわ』で送信＝音は確定",
    "いつ火が": "EL_YOMI『いつ ひが』で送信＝音は確定（前は『木が』で意味が変わっていた）",
    "想定の外": "EL_YOMI『そうてい の外』で送信＝音は確定（前は『童貞』）",
}
# 数のかな固定（キーが数字なので上と分けて持つ）
SENT_KANA_NUM = ["77便と", "175便は", "175便と", "93便が", "93便は", "9時3分",
                 "43,150リットル", "11,400ガロン", "26,000フィート", "10,700メートル"]

# ── ② 実測で決着せず、試写で耳に回す行（行ID → 疑いの中身）──────────────────
#    ⚠️「直したつもり」で閉じない。ここに載せた行は要耳一覧に秒つきで出る。
YOUMIMI = {
    "c214-1": "🔴🔴 **読み方の決定そのものを耳で承認してほしい行。**「北棟と南棟」を "
              "**きたとう／みなみとう**（訓読み）に固定した。ほくとう だと聞取が『北東』＝方角に化けたため"
              "（A/B で実測）。この動画は西南西・南へ・東の海上と方角が多い",
    "c313-1": "同上。きたとう を送った最初の行（聞取『北塔の上の方から煙が上がっている』）",
    "c113-1": "🔴 **本文に全角括弧が出る4行のうちの1つ**（単位のメートル換算・2026-09-12 の恒久ルール）。"
              "「刃渡り10センチ（4インチ）未満」を、括弧が短い間になって自然に聞こえるか",
    "c417-1": "同上。「ペンタゴンの西南西8キロ（5マイル）まで」（★決め所の直前のカット）",
    "c623-3": "同上。「首都まで、およそ201キロ（125マイル）」",
    "c904-1": "同上。「刃渡り10センチ（4インチ）未満の刃物も」",
    "c209-2": "「電波に答えて返すのが、二次レーダーである」の助詞が、3回の聞取のうち1回だけ『返すのね』に"
              "聞こえた。A/B の前後とも『のが』なので Scribe の揺れと見たが、決着はしていない",
    "c210-1": "「一次レーダー」が聞取『一時レーダー』。**読みは いちじ で同じ**なので機械では直せない。"
              "字幕は出るが、耳だけだと『一時』と取り違える恐れ",
    "c811-2": "重複読みの門番が鳴った唯一の行（「8時46分40秒、8時46分30秒、8時46分26秒」）。"
              "語ごとの時刻では**重複なし＝誤報**と確定したが、時刻を3つ続けて読む間が自然か",
    "c120-2": "異音の門番が unsure（3テイクとも末尾に音）。語に重ねると『が|っ|た』＝促音に重なるので"
              "本物の語と見たが、テイクごとに形が違ったので念のため",
}

_NUM_RE = re.compile(r"[0-9０-９]")


def artifact_ok():
    """異音の語照合（el_artifact_words --retakes）で『重なる語』が見つかった行。fail closed。"""
    p = Path("/tmp/aw.txt")
    src = None
    for cand in (ROOT / "qa_out" / "ep7_artwords.log", p):
        if cand.exists():
            src = cand.read_text(encoding="utf-8", errors="replace")
            break
    if src is None:
        raise SystemExit("🔴 異音の語照合のログが無い（先に el_artifact_words.py --retakes）")
    ok, cur = set(), None
    for l in src.splitlines():
        if l.startswith("=== "):
            cur = l.split(" ")[1]
        elif cur and ("重なる語" in l or "異音の所見なし" in l) and "（語なし）" not in l:
            ok.add(cur)
    return ok


def reading_match():
    """el_reading_diff の『読み一致』行＝台本と聞取の読みが同じ＝誤読ではない。"""
    p = ES.qa_path("reading_diff.tsv")
    rows = p.read_text(encoding="utf-8").splitlines()[1:]
    return {l.split("\t")[0] for l in rows if l.split("\t")[1] == "読み一致"}


def main() -> int:
    lines = ES.lines()
    art_ok, rd_ok = artifact_ok(), reading_match()
    print(f"異音の語照合で語に重なる {len(art_ok)}行／読み一致 {len(rd_ok)}行")
    rows = []
    for ln in lines:
        if ln.lid in YOUMIMI:
            rows.append((ln.lid, "要耳（機械で決着せず）", YOUMIMI[ln.lid].replace("\t", " ")))
            continue
        why = [f"{w}＝{r}" for w, r in SENT_KANA.items() if w in ln.text]
        why += [f"{k}＝EL_YOMI でカナ／かな固定＝音は確定" for k in SENT_KANA_NUM if k in ln.text]
        if why:
            rows.append((ln.lid, "音は確定（EL_YOMI でかなを送っている）", "／".join(why)[:400]))
            continue
        why = [f"{w}＝{r}" for w, r in SCRIBE_ONLY.items() if w in ln.text]
        if why:
            rows.append((ln.lid, "表記のゆれ（音は正しいと実測）", "／".join(why)[:400]))
            continue
        m = []
        if ln.lid in art_ok:
            m.append("異音は語に重なる（促音）＝el_artifact_words で『語なし』0件")
        if ln.lid in rd_ok:
            m.append("台本と聞取の**読みが一致**（el_reading_diff）＝字の当て方の違いだけ")
        if m:
            rows.append((ln.lid, "表記のゆれ（別の検査で決着）", "／".join(m)))
    miss = [k for k in YOUMIMI if k not in {l.lid for l in lines}]
    if miss:
        raise SystemExit(f"🔴 台本に無い行IDを要耳に書いている（書き損じ）: {miss}")
    out = ES.qa_path("verdicts_manual.tsv")
    out.write_text("行\t扱い\t理由\n" + "\n".join("\t".join(r) for r in rows) + "\n", encoding="utf-8")
    print(f"扱い {len(rows)}行（要耳 {len(YOUMIMI)}／それ以外 {len(rows)-len(YOUMIMI)}） -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
