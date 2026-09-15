# -*- coding: utf-8 -*-
"""ep8_credtable.py — `ref/CREDITS.md` §コロンビア号 の表を**機械で書き出す**（2026-09-15・⑤b-2）。

■ なぜ要るか
    `tools/check_credits.py` は「副題が名乗る年」と「表の撮影年」を突き合わせる門番で、
    **`| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | 元の題名 |` の6列**を読む。
    `qa_out/ep8_assets.py credits` が出すのは `scene_jiko.EP8_PHOTO` と別の列の表なので、
    門番が読める形を別に作る。**手で書かない**（74行を手で写すと必ずずれる）。

■ 「使うカット」は `cuts.SPEC` から数える
    ⚠️ **`BACKDROP` で地に敷いたカットも `photo=` を持つ**ので同じように拾われる。
       ここを落とすと、門番が見る欄と表の欄がずれる。

■ 使い方
    python qa_out/ep8_credtable.py            # 表だけ
    python qa_out/ep8_credtable.py --check    # 表に無い欄・使われていない欄を数える
"""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE / "tools"))
sys.path.insert(0, str(HERE / "qa_out"))
sys.stdout.reconfigure(encoding="utf-8")

import ep8_assets as A                                          # noqa: E402

# PD の根拠は1種類ではない（→ [[feedback-pd-label-hides-two-different-grounds]]）。
# 写真74点は**すべて NASA の職務著作＝合衆国法典17編105条**。
LIC = "PD（米連邦職員の職務著作・17 U.S.C. §105）"


def used_by():
    """欄の名前 → それを使っているカットID（実写も、地に敷いた図解も）。"""
    import cuts
    out = defaultdict(list)
    for cid in sorted(cuts.SPEC):
        p = cuts.SPEC[cid].get("photo") or ""
        if p.startswith("ep8/") and "/fb_" not in p:
            out[Path(p).stem].append(cid)
    return out


# 🔴 **7本目の表と同じ見出しにしない。**`check_credits.load_table()` は
#    `lines.index(HEADER)` で**最初に当たった行**から読むので、見出しが同じだと
#    8本目の表を足しても 7本目の表を読み続ける（＝黙って前の回を測る）。
HEADER = "| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | NASA の識別子 |"
SECTION = "## スペースシャトル・コロンビア号 空中分解事故（2003-02-01・8本目）"


def table_lines(led, use):
    rows = [HEADER, "|---|---|---:|---|---|---|"]
    missing, unused = [], []
    for name, nid in A.PICK.items():
        it = led.get(nid)
        if it is None:
            missing.append(name)
            continue
        y, _mo, _dd = A._date_of(it)
        cuts_ = " ".join(use.get(name, []))
        if not cuts_:
            unused.append(name)
        who = (it.get("creator") or "").strip()
        title = (it.get("title") or "").replace("|", "／").strip()
        rows.append(f"| `{name}` | {cuts_} | {y if y else '不明'} | {LIC} | "
                    f"{who} | {title} |")
    return rows, missing, unused


def write_section():
    """`ref/CREDITS.md` の §コロンビア号 を**入れ替える**（無ければ末尾に足す）。"""
    path = HERE / "ref" / "CREDITS.md"
    led, use = A.ledger(), used_by()
    rows, missing, unused = table_lines(led, use)
    body = [
        SECTION, "",
        "**2026-09-14（②素材の取り直し）に実測した。**写真74点は"
        "`qa_out/ep8_assets.py` の `PICK` が正本で、この表は"
        "`qa_out/ep8_credtable.py` が**機械で書き出している**（手で書かない）。", "",
        "### 1. 写真74点 ── すべて NASA の職務著作（PD）", "",
        "根拠＝**合衆国法典17編105条**。撮影機関（KSC／JSC／MSFC）は"
        "`tools/scene_jiko.py` の `EP8_PHOTO` が出典行に出す。",
        "⚠️ **末尾に年を書いた欄は別の年・別の飛行**（`slf_landing` `slf_approach` "
        "`columbia_middeck` `cargo_tool`＝2002年／`oex_recorder`＝**1988年**）。"
        "副題で必ずその年を名乗ること。**門番は年の食い違いだけを見ていて、"
        "被写体の食い違いは見ない。**", "",
        f"⚠️ 使っていない欄が **{len(unused)}件** ある（"
        + " ".join(f"`{n}`" for n in sorted(unused)) + "）。"
        "②で落としたが置き場が無かったもの。**捨てていない。**", "",
        *rows, "",
        "### 2. 動く映像9本", "",
        "正本＝`ref/ep8/clips.json`（`tools/footage.py` の `CLIPS` が読む）。"
        "ショットの境目＝`ref/ep8/shots.json`（502ショット・1秒刻みの実測）。", "",
        "| key | 出どころ | 権利の根拠 | 使うカット |",
        "|---|---|---|---|",
        "| `sts1` | NASA『STS-1 File Footage for 40th Anniversary』 | 米連邦職員の職務著作 |"
        " c101 c102 |",
        "| `fd16` | NASA『STS-107 Entry Status Briefing Flight Day 16』 |"
        " 米連邦職員の職務著作 | c418 |",
        "| `mc0201` | NASA『STS-107 Mission Control 02/01/2003』 |"
        " 米連邦職員の職務著作 | c622 c713 c727 |",
        "| `fdcomm` | NASA『Flight Director Communications Loop』 |"
        " 米連邦職員の職務著作 | c701 c720 c724 |",
        "| `mct` | NASA『STS-107 Mission Control & Telemetry 03/14/2003 Rev.5』 |"
        " 米連邦職員の職務著作 | c705 c711 c715 c717 |",
        "| `guncam` | Commons『Shuttle Columbia Disaster gun camera footage』 |"
        " 🔴 **要確認**（下記） | c725 |",
        "| `tank` | NASA『Columbia Tank Found on Lakebed』 | 米連邦職員の職務著作 |"
        " ep01 ep02 |",
        "| `cabin` | Commons『STS-107, final moments in cabin』 |"
        " 米連邦職員の職務著作 | **使わない**（⑤b-2 で外した） |",
        "| `fdbrief` | NASA『2003-02-14 Entry Flight Director Briefing』 |"
        " 米連邦職員の職務著作 | 使わない（台本に置き場が無い） |", "",
        "🔴🔴 **`guncam` だけ権利の根拠が弱い。**Commons の札は PD だが、説明文は"
        "「**訓練中のオランダ人搭乗員**が、テキサス州フォートフッドの米陸軍 AH-64D の"
        "照準カメラで撮った」。**米連邦職員の職務著作ではそのまま説明できない。**"
        "この回の要の映像（c725＝分解そのもの）なので、**⑥までに根拠を確かめること**。",
        "⚠️ `mct` は第三者の編集物だが、説明文に「Copyrighted portions … have been removed"
        " to maintain NASA Public-Domain status」とある。", "",
        "🔴 **`cabin` は⑤b-2 で外した。**640px のシートで中身を見たら、7人とも"
        "**再突入用の与圧服とヘルメット**を着けていた（10・45・270・375秒）。"
        "＝ 飛行11日目の絵ではなく **2月1日の再突入支度の絵**。"
        "台本 §1-2 が引いた線（再突入中の機内映像は画にも言葉にも出さない）の外側にある。",
        "",
    ]
    txt = path.read_text(encoding="utf-8")
    lines = txt.split("\n")
    if SECTION in lines:
        i = lines.index(SECTION)
        j = i + 1
        while j < len(lines) and not lines[j].startswith("## "):
            j += 1
        lines = lines[:i] + body + lines[j:]
    else:
        lines = lines + ["", *body]
    path.write_text("\n".join(lines), encoding="utf-8")
    print(f"  ✓ {path} に §コロンビア号 を書いた（{len(rows) - 2}行"
          f"／使っていない欄 {len(unused)}／台帳に無い欄 {len(missing)}）")
    return 0


def main():
    if "--write" in sys.argv:
        sys.exit(write_section())
    led = A.ledger()
    use = used_by()
    print(HEADER)
    print("|---|---|---:|---|---|---|")
    missing, unused = [], []
    for name, nid in A.PICK.items():
        it = led.get(nid)
        if it is None:
            missing.append(name)
            continue
        y, _mo, _dd = A._date_of(it)
        cuts_ = " ".join(use.get(name, []))
        if not cuts_:
            unused.append(name)
        who = (it.get("creator") or "").strip()
        title = (it.get("title") or "").replace("|", "／").strip()
        print(f"| `{name}` | {cuts_} | {y if y else '不明'} | {LIC} | {who} | {title} |")
    if "--check" in sys.argv:
        print(f"\n# 欄 {len(A.PICK)}／使われている {len(use)}"
              f"／使っていない {len(unused)}／台帳に無い {len(missing)}", file=sys.stderr)
        if unused:
            print("# 使っていない欄: " + " ".join(sorted(unused)), file=sys.stderr)
        if missing:
            print("# 🔴 台帳に無い欄: " + " ".join(missing), file=sys.stderr)


if __name__ == "__main__":
    main()
