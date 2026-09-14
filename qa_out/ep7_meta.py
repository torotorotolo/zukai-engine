# -*- coding: utf-8 -*-
"""7本目（9.11）の `config/meta_ep7.json` を**機械で**組み立てる。

🔴 なぜ手で書かないか
  ① 用語15語は `ref/ep7/yougo.md` の「貼る本文」が正本。手で写すと必ずどこかがずれる
     （→ [[feedback-jiko-description-glossary]]）。ここでは**囲みの中をそのまま**貼る。
  ② CC BY は**撮影者名が使用条件**。`ref/CREDITS.md` §8 の表（67行）から機械で拾い、
     1人も落ちないようにする。行数が 67 でなければ**書かずに落ちる**
     （→ [[feedback-parsers-fail-closed]]）。
  ③ タイトル 100字・説明 5,000字の上限を、書く前に自分で確かめる。

    python qa_out/ep7_meta.py            # 組み立てて config/meta_ep7.json に書く
    python qa_out/ep7_meta.py --dry      # 書かずに中身と字数だけ出す
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent.parent
YOUGO = HERE / "ref" / "ep7" / "yougo.md"
CREDITS = HERE / "ref" / "CREDITS.md"
OUT = HERE / "config" / "meta_ep7.json"

TITLE = ("【映像あり】軍が1機目の乗っ取りを知らされたのは衝突9分前。残る3機は墜ちるまで"
         "知らされなかった。2,973人が亡くなった2001年アメリカ同時多発テロの真相【事故検証】")

HEAD = """【この動画について】
2001年9月11日の朝、アメリカで4機の旅客機が続けざまに乗っ取られました。この動画が追うのは、その4機と、地上でそれを追っていた人たちです。空の道を見張る管制官と、防空の当直でした。

軍が1機目の乗っ取りを知らされたのは、ぶつかる9分前でした。残りの3機については、墜ちるまで知らされていません。猶予は9分、そのあとは0分だった、という順序の話です。

背骨にしたのは、アメリカの独立調査委員会が2004年に出した報告書（委員会報告）です。画面に出る時刻は、すべてこの報告書に書かれた値で、現地のアメリカ東部の時間です。建物がなぜ崩れたのかは別の役所が別に調べているので、ここでは扱いません。追いかけるのは空のほうです。

・軍が1機目の乗っ取りを知らされたのは、いつだったのか
・機体が名乗るのをやめたとき、管制官の画面には何が残ったのか
・「some planes」── 複数形は、いつ、誰の口から出たのか
・アメリカは、どうやって自分の国の空をいったん全部閉じたのか
・戦闘機の緊急発進と撃墜の許可は、なぜ間に合わなかったのか
・あの朝の記録は、どこに、どういう形で残ったのか

※ この動画では、当時の無線の音声は鳴らしません。逐語は文字で出します。
※ 亡くなった方は2,973人です（この数に、乗っ取った側の19人は入っていません）。
"""

TAIL_SRC = """【出典】
・9/11委員会報告（アメリカ同時多発テロに関する独立調査委員会・2004年・政府印刷局版）
・NTSB フライトパス・スタディ（アメリカン11便／ユナイテッド175便／アメリカン77便／ユナイテッド93便の4本）
・記録映像：アメリカ国立公文書館（NARA）所蔵 RG237 連邦航空局（FAA）naId 7419198（パブリックドメイン）
"""


def read_glossary() -> str:
    """`ref/ep7/yougo.md` の「## 1. 貼る本文」の囲みを**そのまま**返す。"""
    md = YOUGO.read_text(encoding="utf-8")
    m = re.search(r"## 1\. 貼る本文.*?\n```\n(.*?)\n```", md, re.S)
    if not m:
        raise SystemExit("🔴 yougo.md の「貼る本文」の囲みが見つからない。書かずに止めた。")
    body = m.group(1).strip()
    if "【この動画に出てくる言葉】" not in body:
        raise SystemExit("🔴 囲みの中身が用語の本文ではない。書かずに止めた。")
    # ⚠️ 2026-09-14（⑥）に数え直した。**14語が正**。
    #    引き継ぎと yougo.md §2 の「15語」は足し算の誤り
    #    （下書き14 − EDT（注へ落とした） ＋ 運航管理者 ＝ 14）。落ちた語は1つも無い。
    n = body.count("\n・")
    if n != 14:
        raise SystemExit(f"🔴 用語の行が {n} 語（仕様は 14）。書かずに止めた。")
    return body


def read_credits() -> tuple[str, str]:
    """§8 の表（67行）から、PD と CC BY のクレジット行を組み立てる。"""
    lines = CREDITS.read_text(encoding="utf-8").splitlines()
    start = next(i for i, s in enumerate(lines) if s.startswith("### 8.") and "67点" in s)
    rows = []
    for s in lines[start:]:
        if s.startswith("### ") and not s.startswith("### 8."):
            break
        if not s.startswith("| `"):
            continue
        c = [x.strip() for x in s.strip().strip("|").split("|")]
        rows.append({"right": c[3], "who": c[4].strip().rstrip(".").strip()})
    if len(rows) != 67:
        raise SystemExit(f"🔴 §8 の表が {len(rows)} 行（仕様は 67）。書かずに止めた。")

    pd, cc = [], {}
    for r in rows:
        m = re.match(r"(PD|CC BY)（(.+)）", r["right"])
        if not m:
            raise SystemExit(f"🔴 権利の欄が読めない: {r['right']}。書かずに止めた。")
        if m.group(1) == "PD":
            if r["who"] not in pd:
                pd.append(r["who"])
        else:
            cc.setdefault(m.group(2), [])
            if r["who"] not in cc[m.group(2)]:
                cc[m.group(2)].append(r["who"])

    pd_txt = ("・写真（パブリックドメイン）\n　"
              + "／".join(sorted(pd, key=str.lower)) + "\n")
    out = ["・写真（クリエイティブ・コモンズ表示ライセンス。色調の調整と切り出しをしています）"]
    for lic in sorted(cc):
        # ⚠️ 版ごとに条文の URL が違う。4.0 の1本で代表させない。
        m = re.match(r"CC BY (\d\.\d)(?: (\w+))?$", lic)
        if not m:
            raise SystemExit(f"🔴 ライセンス名が読めない: {lic}。書かずに止めた。")
        url = f"https://creativecommons.org/licenses/by/{m.group(1)}/"
        if m.group(2):
            url += f"{m.group(2)}/"
        out.append(f"　{lic}（{url}）")
        out.append("　　" + "／".join(sorted(cc[lic], key=str.lower)))
    return pd_txt, "\n".join(out) + "\n"


def main() -> int:
    gloss = read_glossary()
    pd_txt, cc_txt = read_credits()
    desc = "\n".join([HEAD, gloss, "", TAIL_SRC + pd_txt + cc_txt])

    print(f"タイトル {len(TITLE)} 字（上限 100）")
    print(f"説明     {len(desc)} 字（上限 5,000）")
    if len(TITLE) > 100 or len(desc) > 5000:
        raise SystemExit("🔴 上限を超えた。書かずに止めた。")

    meta = {
        "slug": "ep7",
        "title": TITLE,
        "description": desc,
        "tags": ["9.11", "アメリカ同時多発テロ", "2001年", "航空管制", "ハイジャック",
                 "事故検証", "図解", "委員会報告", "ユナイテッド93便", "アメリカン11便",
                 "NORAD", "FAA", "一次資料", "解説", "ドキュメンタリー"],
        "thumbnail": "out/thumb/ep7-t1/ep7_a_smoke_9min.png",
        "genre": "jiko",
        "playlist": "",
    }
    if "--dry" in sys.argv:
        print("\n" + desc)
        return 0
    OUT.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✓ 書いた → {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
