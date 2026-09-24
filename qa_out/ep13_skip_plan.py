# -*- coding: utf-8 -*-
"""13本目 ⑤a'：行を「数字のまま」送るとき、EL_YOMI_SKIP に並べる鍵を機械で求める（API 不使用・2026-09-24）。

  python qa_out/ep13_skip_plan.py c101-1,c202-2 [--keep "46704|52-37"]
    … 行ごとに「いまの送信文 → 数字に戻した送信文」と外す鍵を出し、最後に EL_YOMI_SKIP に貼る形を出す

🔴 長い鍵を外すと短い鍵が顔を出す（12本目⑥「国はさんがつ18日」）＝**数字を含む鍵が1つも当たらなくなるまで**外し続ける。
🔴 門番⑤は「外す鍵が台本の元の文に当たるか」を見る＝顔を出す短い鍵も元の文に当たるので、この形で通る。
⚠️ 型番・符号（DC-10・N103AA・46704 など）は数字に戻すと読み方が変わる＝--keep で外さない鍵を指定する。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import el_script as E  # noqa: E402

DIG = re.compile(r"[0-9０-９]")


def arg(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def plan(text, keep):
    skip = []
    while True:
        order = [k for k in E.EL_YOMI_ORDER if k not in skip]
        hits = []
        sent = E.apply_yomi(text, order, E.EL_YOMI_RE, E.EL_YOMI, hits)
        num = [k for k, v, n in hits if DIG.search(k) and k not in keep]
        if not num:
            return skip, sent, [k for k, v, n in hits]
        skip += num


def main():
    if len(sys.argv) < 2 or sys.argv[1].startswith("--"):
        raise SystemExit("使い方: python qa_out/ep13_skip_plan.py c101-1,c202-2 [--keep \"鍵|鍵\"]")
    keep = set((arg("--keep", "") or "").split("|")) - {""}
    by = E.by_id()
    ids = E.resolve_ids(sys.argv[1])
    out = []
    for lid in ids:
        t = by[lid].text
        skip, sent, rest = plan(t, keep)
        print(f"{lid}\n  いま: {E.el_text(t)}\n  数字: {sent}\n  外す: {skip}\n  残る: {rest}")
        if skip:
            out.append((t, skip))
    print("\n# ── EL_YOMI_SKIP に貼る形 ──")
    for t, skip in out:
        print(f"    {t!r}: {skip!r},")
    return 0


if __name__ == "__main__":
    sys.exit(main())
