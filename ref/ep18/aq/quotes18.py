# -*- coding: utf-8 -*-
"""18本目 ⑤a-1：「」の前で句がつながる所を数える（ルール 5a-35 ②・2026-10-04）＋手書き override の照合。

  python ref/ep18/aq/quotes18.py            … 「」の開きごとに、前の語と「」の中身が1つの句につながっていないかを2つの方法で見る
  python ref/ep18/aq/quotes18.py --check-ov … override.tsv の行が、自動の読みとかなで1字も違わないか（違いは / と ' だけ）

16本目の `ref/ep16/aq/quotes16.py` を写した。足したのは「行をまたぐ「」」を機械で全部出すこと（16本目は目で探した）。
なぜ：aq_kana は「」を外すだけ＝前の語と「」の中身が1つのアクセント句になることがある（15本目 c215-2「そーちてれめ'とりーを」）。
  棒読みでも句の切れ目 / は音に効く（ルール 5a-29・5a-35）。直すのはその回の手書き override.tsv（共有の道具は触らない）。
2つの方法（15本目 ⑤a-2 と同じ考え・1つだけだと物差しが崩れる所で見落とす）：
  B（表層）：「」の中身の頭の字が、どれかの句の表層の頭に出るか（数字で始まる中身は見られない＝要目視）
  A（拍の数）：「」の手前までを単独で変換した拍の数が、行全体の句の切れ目（拍の累計）のどれかと一致するか
  2つが食い違う所・どちらかが判定できない所は「要目視」で出す
"""
import re
import sys
import unicodedata
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import aq_kana as AQ   # noqa: E402
import narration       # noqa: E402

OPEN = re.compile(r"「([^」]*)」")


def norm(s):
    return unicodedata.normalize("NFKC", s)


def judge(text):
    """[(「」の中身, B, A)]。B・A は "切れ" / "つながり" / "?"。"""
    AQ.load_userdict()
    ps = AQ.phrases(text)
    surf = [norm(w) for _, _, _, w in ps]
    bounds, acc = set(), 0
    for ms, _, _, _ in ps:
        bounds.add(acc)
        acc += len(ms)
    out = []
    for m in OPEN.finditer(text):
        q = m.group(1)
        head = norm(AQ._pre(q))[:2]
        if not head or re.match(r"[0-9]", head):
            b = "?"
        elif any(s.startswith(head) for s in surf):
            b = "切れ"
        elif any(head in s for s in surf):
            b = "つながり"
        else:
            b = "?"
        pre = AQ._pre(text[:m.start()])
        if not pre:
            a = "切れ"                      # 行の頭の「」＝前に語が無い
        else:
            try:
                n = sum(len(ms) for ms, _, _, _ in AQ.phrases(pre))
                a = "切れ" if n in bounds else "つながり"
            except AQ.AqError:
                a = "?"
        out.append((q, b, a))
    return out


def main():
    AQ.load_userdict()
    ov = AQ.load_override()
    lines = [(f"{cid}-{i}", t) for cid, ls in narration.SCRIPT for i, t in enumerate(ls, 1)]
    rows = [(lid, t) for lid, t in lines if "「" in t]
    span = [(lid, t) for lid, t in lines if t.count("「") != t.count("」")]   # 行をまたぐ「」＝目で見る
    n = bad = unsure = 0
    for lid, t in rows:
        for q, b, a in judge(t):
            n += 1
            if b == a == "切れ":
                continue
            if b == a == "つながり" and lid in ov:
                mark = "✓ つながり（手書きで直しずみ）"
            elif b == a == "つながり":
                bad += 1
                mark = "🔴 つながり"
            else:
                unsure += 1
                mark = "⚠️ 要目視"
            print(f"{mark}  {lid}「{q}」 B={b} A={a}｜{AQ.to_aq(t)[0]}")
    for lid, t in span:
        print(f"👁 行をまたぐ「」  {lid}｜{t}｜{AQ.to_aq(t)[0]}")
    print(f"「」の開き {n}か所（{len(rows)}行）／直していないつながり {bad}／要目視 {unsure}／"
          f"行をまたぐ「」の行 {len(span)}（2つの方法の外＝上の 👁 を目で見る）")
    return 1 if bad else 0


FIX = re.compile(r"【読みを直す：([^→】]+)→([^】]+)】")


def check_override():
    """手書きの行のかなが自動と1字も違わないか。理由の欄に【読みを直す：A→B】がある行だけは、
    自動のかなの A を B に1回置き換えたものと一致すればよい（＝その置き換えのほかは違わない）。"""
    AQ.load_userdict()
    ov = AQ.load_override()
    reason = {}
    for ln in (AQ.ep_dir() / "override.tsv").read_text(encoding="utf-8").splitlines():
        if ln.strip() and not ln.startswith("#"):
            p = ln.split("\t")
            reason[p[0]] = p[2] if len(p) > 2 else ""
    script = {f"{cid}-{i}": t for cid, ls in narration.SCRIPT for i, t in enumerate(ls, 1)}
    cont = {f"{cid}-{i}": i < len(ls) for cid, ls in narration.SCRIPT for i, _ in enumerate(ls, 1)}
    bad = 0
    for lid, aq in ov.items():
        auto = AQ.to_aq(script[lid], lid, cont[lid])[0]
        a, h = re.sub(r"['/]", "", auto), re.sub(r"['/]", "", aq)
        m = FIX.search(reason.get(lid, ""))
        if m:
            same = a.count(m.group(1)) >= 1 and a.replace(m.group(1), m.group(2), 1) == h
            mark = "OK（読みを直した：" + m.group(1) + "→" + m.group(2) + "）" if same else "NG"
        else:
            same = a == h
            mark = "OK" if same else "NG"
        bad += not same
        print(f"{mark}  {lid}\n   自動 {auto}\n   手書き {aq}")
    print(f"手書き {len(ov)}行／かなが自動と違う（直すと書いた所のほか） {bad}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(check_override() if "--check-ov" in sys.argv else main())
