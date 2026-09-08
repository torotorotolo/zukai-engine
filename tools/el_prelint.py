# -*- coding: utf-8 -*-
r"""el_prelint.py — ElevenLabs で合成する**前**に、誤読が起きやすい型を台本から機械で拾う（2026-09-02 新設）。

  python tools/el_prelint.py ep009            → 台本/ep009_el_prelint.tsv と型ごとの件数
  python tools/el_prelint.py --selftest

🔴 これは「当たり」を付ける道具で、門番ではない。
   候補の直し方は tools/el_ab_yomi.py で A/B 文字起こしをして決める（辞書は類推で書かない＝
   feedback-yomi-dict-must-be-verified）。ここで挙がった語を耳で確かめずに EL_YOMI に足さないこと。

なぜ要るか:
   フクロウ（AivisSpeech）には「③生成前の全文リント」の層があるが、ElevenLabs 側には無かった。
   EL_YOMI は「誤読したと耳で確かめた語だけ」を事後に足す辞書なので、新しい語は毎回すり抜ける。
   合成の前に既知の型を並べておけば、el_check_yomi の --worst で聞く行の当たりが先に付く。

型の出所（EL_YOMI の履歴 ep005〜ep008・reference-elevenlabs-tts）:
   文頭の数字（ep007 s016「36人は」→「6人は」）／小数（ep008 s028「3.4周」→「三千四周」）／
   「いま」＋動詞（ep007「いま動かせる」→「胃腸を動かせる」）／1モーラ語＋助詞（ep008 s118「間を」）／
   同形異音語（話・歳・方・間・側・群・上・下・生・人・日・目・表・角・家・物・事）／
   数詞＋助数詞（点・周・回・年・人・％）／鉤括弧（長い間が入る＝ep007 s110）／
   EL_YOMI がすでに当たる語（直した行の確認用）
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent

PATTERNS = [
    ("文頭の数字",     re.compile(r"^[0-9０-９]")),
    ("小数",           re.compile(r"[0-9０-９]+[.．][0-9０-９]+")),
    ("いま＋動詞",     re.compile(r"いま[一-龥]")),
    ("1モーラ語＋助詞", re.compile(r"(?<![一-龥ぁ-んァ-ン])[間目手気日火子](を|に|が|は|で|も)")),
    # ⚠️ 2026-09-02 ep009 で試すと「同形異音語」を1つの型にしたら 92件 出て当たりが広すぎた。
    #    ElevenLabs で実際に誤読した実績のある字（群・間・側・方・話・歳）と、それ以外（一般）に分ける。
    #    一般のほうは el_check_yomi の --worst と重なった行だけ見ればよい。
    ("同形異音語（実績）", re.compile(r"[群間側方話歳](?![一-龥])")),
    ("同形異音語（一般）", re.compile(r"[上下生人日目表角家物事一](?![一-龥])")),
    ("数詞＋助数詞",   re.compile(r"[0-9０-９]+(点|周|回|年|人|％|%|分|秒|倍|個|枚|問|件|割|位|月|日|時|本|階|通り|つ|か月"
                                  r"|週間|段|センチ|ミリ|メートル|インチ|フィート|パーセント)")),
    ("鉤括弧",         re.compile(r"[「」『』]")),
    # ── 事故検証ch 4本目サーフサイド（2026-09-05）。台本第3版 §6-1 の「怪しい語」と、英字・記号（読みが崩れやすい）
    ("§6-1の語",      re.compile(r"サーフサイド|プールデッキ|押し抜き|パンチング|かぶり|下端筋|上端筋|定着|不同沈下"
                                  r"|衝撃荷重|エイティセブン|諮問|NIST|K|¾")),
    # ── 5本目 SL-1（2026-09-07）。台本第2版 §6-3 の難読・同形異音語のうち、**実際に本文に出る語だけ**
    #    （出ない語を並べても当たりにならない。件数は el_script.lines() に当てて数えた）
    ("§6の語（SL-1）", re.compile(r"棺|札|刃|更地|炸薬|遮蔽|覆い|覆う|汲|診た|被せ|踊り場|担架|蘇生|面体"
                                  r"|散水|歯棒|歯車|砂利|杭|溝|支所|当直|日勤|判読|臨界|反応度|上着|上の栓"
                                  r"|レントゲン|制御棒|中性子|ホウ素|立方フィート|SL-1|ALPR|AEC")),
    # ── 6本目 キー橋（2026-09-08）。台本第2版 §6 の候補のうち、**実際に本文に出る語だけ**を書く
    #    （出ない語を並べても当たりにならない。件数は el_script.lines() に当てて数えた＝「剛節」は0行なので外した）。
    #    §6 に無いが同じ型で危ない語（母線・水先・操舵・舵・遮断器・変圧器・積荷）も足した。
    #    ⚠️「積荷」は4本目の実測で かな も カナ も誤読（「積み荷」だけ通った）＝必ず A/B する。
    ("§6の語（キー橋）", re.compile(r"協会|ワゴ|ワイヤーワン|ワイヤースリー|州交通局|エムディーティーエー"
                                  r"|ダリ|パタプスコ|シーガート|マクヘンリー|ブルー・ナゴヤ|エボーン|ブラウナー"
                                  r"|径間|橋台|非冗長|キップ|喫水|分の1|母線|タグ|水先|操舵|舵|錨|主機"
                                  r"|発電機|遮断器|変圧器|積荷|冗長|NTSB")),
    ("英字・記号",    re.compile(r"[A-Za-z¾]+")),
    # 🔴 2026-09-07（5本目 SL-1）: 台本の注記の記号（⚠️・🔴・絵文字）が字幕行に紛れ込む事故（第1版で1件）。
    #    これだけは「当たり」ではなく**門番**＝1件でも run() が 1 を返して止める（feedback-rules-need-gates）。
    #    白名簿の外を全部拾う書き方にする。絵文字を1つずつ並べる書き方だと、次の未知の記号を見逃す。
    ("🔴記号・絵文字", re.compile(r"[^ぁ-ゖァ-ヺー々〆一-鿿㐀-䶿豈-﫿"
                                r"0-9A-Za-z、。「」『』・…％%？！　 .,\-–—〜／¾]")),
]
FATAL = "🔴記号・絵文字"     # この型だけは1件でも run() を落とす


def scan_line(text: str):
    """1行から該当を集める。[(型, 該当文字列)] を返す。"""
    out = []
    for name, rx in PATTERNS:
        for m in rx.finditer(text):
            out.append((name, m.group(0)))
    return out


def yomi_hits(text: str):
    """EL_YOMI がこの行のどのキーに当たるか（本番と同じ関数を通す）。"""
    import el_script
    hits = []
    el_script.el_text(text, hits=hits)
    return hits


def run() -> int:
    import el_script as ES     # 事故検証ch：台本は narration.SCRIPT（config/<slug>.json ではない）
    rows, counts, lines = [], {}, 0
    for ln in ES.lines():
        lines += 1
        text = ln.text
        found = scan_line(text)
        for name, s in found:
            counts[name] = counts.get(name, 0) + 1
            rows.append((ln.lid, name, s, text))
        for k, v, n in yomi_hits(text):
            counts["EL_YOMI 既存"] = counts.get("EL_YOMI 既存", 0) + 1
            rows.append((ln.lid, "EL_YOMI 既存", f"{k}→{v}×{n}", text))
    out = ES.qa_path("el_prelint.tsv")
    out.write_text("行\t型\t該当\t本文\n" + "".join(f"{a}\t{b}\t{c}\t{d}\n" for a, b, c, d in rows),
                   encoding="utf-8")
    print(f"{ES.SLUG}: {lines}行を走査 → 候補 {len(rows)}件（{len({r[0] for r in rows})}行） → {out}")
    for k, v in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {k:<12} {v}件")
    print("⚠️ これは当たり。直す前に el_ab_yomi.py で A/B 文字起こしをして、効いた書き方だけ EL_YOMI へ。")
    fatal = [r for r in rows if r[1] == FATAL]
    if fatal:
        print(f"\n🔴 E: 字幕行に記号・絵文字が {len(fatal)}件（台本の注記が本文に紛れています。台本を直す）")
        for lid, _, ch, text in fatal:
            print(f"   {lid}  U+{ord(ch):04X} {ch!r}  {text}")
        return 1
    print("✅ 字幕行の記号・絵文字 0件（門番）")
    return 0


def selftest() -> int:
    cases = [
        ("36人は、同じ8分間を過ごしました。", {"文頭の数字", "数詞＋助数詞"}),
        ("3.4周というのは、平均です。", {"小数", "数詞＋助数詞"}),
        ("いま動かせるものが、ひとつあります。", {"いま＋動詞"}),
        ("間をあけた学習のほうが、残ります。", {"1モーラ語＋助詞", "同形異音語（実績）"}),
        ("読んだ群が83点でした。", {"同形異音語（実績）", "数詞＋助数詞"}),
        ("その人の目には、上の段が見えます。", {"同形異音語（一般）"}),
        ("「わかった」という感覚です。", {"鉤括弧"}),
        ("これは、静かな朝でした。", set()),
        # 事故検証ch（2026-09-05）
        ("かぶりは、¾インチ。NIST が測った。", {"§6-1の語", "英字・記号"}),
        ("下に沈んだ量は、1.2センチほど。", {"小数", "数詞＋助数詞"}),
        ("場所は、Kと13.1という記号で呼ばれる柱のそば。", {"§6-1の語", "小数"}),
        # 🔴 記号・絵文字の門番（2026-09-07 SL-1）の**陽性対照**。第1版で実際に紛れた形を先頭に置く
        ("⚠️ 原因は、この報告書では決めない", {FATAL}),
        ("🔴 ここが決め所である。", {FATAL}),
        ("記録は、そこで途切れている✅", {FATAL}),
        ("🔧 直したカットである。", {FATAL}),
        ("★決め所の印は clean() が外すが、素で来たら止める", {FATAL}),
    ]
    fails = []
    for text, want in cases:
        got = {n for n, _ in scan_line(text)}
        if not want.issubset(got) or (not want and got):
            fails.append((text, want, got))
    # 🔴 **陰性対照**＝本物の台本に出る文字で門番が鳴ってはいけない
    #    （¾・鉤括弧・…・SL-1 のハイフン・全角空白＝el_retake が頭に足す「　、」）
    for text in ["かぶりは、¾インチ。「SL-1」という名前である…",
                 "1961年1月3日の午後9時1分。アイダホ州、SL-1。",
                 "　、棺は、更地になった。",
                 # ↓ SL-1 台本の実文（半角空白・ハイフン・中黒・鉤括弧が実際に出る行）
                 "名前は SL-1。定置式・低出力の原子炉、1号機という意味である。",
                 "その第8章F節の題は、「単一の誤り、という基準」。"]:
        got = {n for n, _ in scan_line(text)}
        if FATAL in got:
            fails.append((text, "陰性対照＝記号0のはず", got))
    if fails:
        print(f"selftest: {len(cases)-len(fails)}/{len(cases)} — 落ちた: {fails}")
        return 1
    print(f"selftest: {len(cases)}/{len(cases)} 合格")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    sys.exit(run())
