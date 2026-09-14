# -*- coding: utf-8 -*-
r"""ep8_yougo.py — 概要欄に載せる用語（台本第2版 §11）を、本文へ機械で当てて仕上げる（⑤a・2026-09-14）。

  python qa_out/ep8_yougo.py            … 表を出す
  python qa_out/ep8_yougo.py --selftest … 陽性・陰性対照（台本を読まない）

🔴 なぜ作ったか（`qa_out/ep8_firstuse.py` をそのまま使わない理由）:
   ① あれは **台本第1版** を見ている（`P = …第1版…`）。正本は第2版。
   ② 見出しの正規表現に **🔧 が入っていない**＝第2版で 🔧 の付いた22カットを丸ごと取り逃がす
      （見出しが拾えないと、その字幕行は「前のカット」に混ざる＝黙って間違った初出が出る）。
      → [[feedback-gates-go-stale-when-upstream-changes]]
   ③ 台本を読む目を3つ目に増やさない。**`check_script.parse` を呼ぶ**（門番と同じ目）。

見るもの:
   A. §11 の用語が、本文に**いつ初めて出るか**と、そのカットに噛み砕きがあるか
   B. §11 にあるのに**本文に1度も出ない**用語（＝概要欄に載せる意味が薄い／落とした語の残骸）
   C. 本文に出るのに §11 に**無い**専門語（＝載せ漏れの候補）
⚠️ ここは「当たり」。⚠️ の行は目で確かめる（同格の噛み砕き「燃料タンクを**覆う**断熱材」を
   KUDAKI の正規表現は拾えない＝④'が §5-6 で書き残した道具の穴）。
"""
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

MD = Path.home() / "Documents" / "Obsidian Vault" / "Projects" / "事故検証-コロンビア号-台本第2版-20260914.md"
EXPECT_CUTS, EXPECT_LINES = 216, 489

# 噛み砕きの合図。⚠️ 同格（「〜を覆う断熱材」）は拾えない＝⚠️ は目で確かめる
KUDAKI = re.compile(r"という|とは|と呼ぶ|のことである|のこと。|＝|でできて|の略|である。")

# C の当たり用。§11 に無くても本文に出たら「載せ漏れの候補」として挙げる語
EXTRA = ["逸した機会", "マーシャル宇宙飛行センター", "米戦略軍", "国際宇宙ステーション",
         "ロボットアーム", "画像解析", "指揮系統", "大気圏", "軌道", "スペースハブ",
         "前のふち", "桁", "打ち上げ委員会", "安全部門", "飛行実績", "運用上の問題",
         "地上支援", "衛星", "望遠鏡", "風洞", "熱防護系"]


def terms_from_md(text):
    """§11 の箇条書きから用語を取る。行頭 `- **語** …` と `- 🔧 **語** …` の両方。"""
    sec = text.split("## 11.", 1)[1].split("\n## 12.", 1)[0]
    out = []
    for ln in sec.splitlines():
        m = re.match(r"^\s*-\s*(?:🔧\s*)?\*\*(.+?)\*\*", ln.strip())
        if m:
            out.append(m.group(1).strip())
    return out


def key_of(term):
    """本文を探すときの見出し語。「RCC（アールシーシー／強化炭素-炭素）」→「RCC」。"""
    return re.split(r"[（(]", term, 1)[0].strip()


def run():
    import check_script as C
    text = MD.read_text(encoding="utf-8")
    cuts = C.parse(text)
    lines_n = sum(len(ls) for _, _, ls in cuts)
    print(f"カット {len(cuts)} ／ 字幕行 {lines_n}  "
          f"（{EXPECT_CUTS}／{EXPECT_LINES} なら道具は正しい）")
    if (len(cuts), lines_n) != (EXPECT_CUTS, EXPECT_LINES):
        print("🔴 台本の数が食い違う。上流を替えたら定数を取り直す")
        return 1
    body = [(cid, [C.clean(l) for l in ls]) for cid, _, ls in cuts]

    terms = terms_from_md(text)
    print(f"\n§11 の用語 {len(terms)}件")

    def first_hit(k):
        hits = [(cid, ls) for cid, ls in body if any(k in l for l in ls)]
        return hits

    print("\n=== A. 初出と噛み砕き ===")
    print("%-24s %-7s %-5s %s" % ("語", "初出", "回数", "初出カットに噛み砕き"))
    dead = []
    for t in terms:
        k = key_of(t)
        hits = first_hit(k)
        if not hits:
            dead.append(t)
            print("%-24s %-7s %-5d %s" % (t, "-", 0, "🔴 本文に出ない"))
            continue
        cid, ls = hits[0]
        mark = "○" if KUDAKI.search("／".join(ls)) else "⚠️ 無し（目で見る）"
        print("%-24s %-7s %-5d %s" % (t, cid, len(hits), mark))

    print(f"\n=== B. §11 にあるが本文に出ない: {len(dead)}件 ===")
    for t in dead:
        print(f"  🔴 {t}")

    print("\n=== C. 本文に出るのに §11 に無い（載せ漏れの候補）===")
    have = {key_of(t) for t in terms}
    n = 0
    for k in EXTRA:
        if k in have:
            continue
        hits = first_hit(k)
        if hits:
            n += 1
            print("  ⚠️ %-22s 初出 %-6s 回数 %d" % (k, hits[0][0], len(hits)))
    if not n:
        print("  （候補なし）")
    return 0


def selftest():
    fails = []
    ok = lambda c, name: (None if c else fails.append(name))
    # 陽性対照＝§11 の書き方2通りを両方拾う
    sec = ("## 11. 用語\n"
           "- **オービタ** … 人が乗る部分。\n"
           "- 🔧 **速さの言い方** … 「音の◯倍」。\n"
           "- ふつうの行（太字なし）\n"
           "\n## 12. 変更台帳\n- **これは12節なので拾わない** … x\n")
    got = terms_from_md(sec)
    ok(got == ["オービタ", "速さの言い方"], f"§11 だけを拾う（got={got}）")
    # 陰性対照＝§12 に食い込まない
    ok("これは12節なので拾わない" not in got, "§12 へ食い込まない")
    # 見出し語の切り出し
    ok(key_of("RCC（アールシーシー／強化炭素-炭素）") == "RCC", "括弧の前だけを見出し語に")
    ok(key_of("記録装置（MADS）") == "記録装置", "括弧の前だけを見出し語に②")
    ok(key_of("オービタ") == "オービタ", "括弧が無ければそのまま")
    # 噛み砕きの合図
    ok(KUDAKI.search("これをデブリ評価チームという。"), "「という」を拾う")
    ok(not KUDAKI.search("燃料タンクを覆う断熱材がはがれた"), "🔴 同格は拾えない（既知の穴・⚠️で出す）")
    if fails:
        print(f"selftest: 落ちた: {fails}")
        return 1
    print("selftest: 7/7 合格（台本を読んでいない）")
    return 0


if __name__ == "__main__":
    unknown = [a for a in sys.argv[1:] if a.startswith("--") and a != "--selftest"]
    if unknown:
        raise SystemExit(f"🔴 知らない引数: {unknown}")
    sys.exit(selftest() if "--selftest" in sys.argv else run())
