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
    ("英字・記号",    re.compile(r"[A-Za-z¾]+")),
]


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
    ]
    fails = []
    for text, want in cases:
        got = {n for n, _ in scan_line(text)}
        if not want.issubset(got) or (not want and got):
            fails.append((text, want, got))
    if fails:
        print(f"selftest: {len(cases)-len(fails)}/{len(cases)} — 落ちた: {fails}")
        return 1
    print(f"selftest: {len(cases)}/{len(cases)} 合格")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    sys.exit(run())
