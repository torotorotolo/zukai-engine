# -*- coding: utf-8 -*-
"""8本目（コロンビア号）の `config/meta_ep8.json` を**機械で**組み立てる。

7本目の `qa_out/ep7_meta.py` を写して、この回の素材の形に合わせた。

🔴 なぜ手で書かないか（ep7 と同じ3つ）
  ① 用語19語は `ref/ep8/yougo.md` の「貼る本文」が正本。手で写すと必ずどこかがずれる
     （→ [[feedback-jiko-description-glossary]]）。ここでは**囲みの中をそのまま**貼る。
  ② クレジットは `ref/CREDITS.md` §コロンビア号 から機械で拾う。
     行数が仕様と違えば**書かずに落ちる**（→ [[feedback-parsers-fail-closed]]）。
  ③ タイトル 100字・説明 5,000字の上限を、書く前に自分で確かめる。

🔴 この回が 7本目と違うところ
  - 写真は **74点すべて NASA の職務著作（PD）**＝ CC BY が1点も無い。
    ⚠️ だからといって CC BY の枝を消していない。**1点でも混ざったら落ちる**ようにしてある
    （撮影者名は使用条件そのものなので、黙って PD の一覧に混ぜてはいけない）。
  - 動く映像は9本のうち **8本が NASA**、`guncam` だけ経路が違う
    （元は米陸軍 AH-64D の照準カメラ。NASA が2003-02-12に公開した録画が出回っている版）。
    → 概要欄でもそこを**分けて**書く。

    python qa_out/ep8_meta.py            # 組み立てて config/meta_ep8.json に書く
    python qa_out/ep8_meta.py --dry      # 書かずに中身と字数だけ出す
    python qa_out/ep8_meta.py --titles   # タイトル候補の字数だけ出す
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent.parent
YOUGO = HERE / "ref" / "ep8" / "yougo.md"
CREDITS = HERE / "ref" / "CREDITS.md"
OUT = HERE / "config" / "meta_ep8.json"

N_GLOSS = 19          # `ref/ep8/yougo.md` §1 の語数（⑤a で確定）
N_PHOTO = 74          # §1 の表の行数
N_CLIP = 9            # §2 の表の行数

# ── タイトル候補 ──────────────────────────────────────────
# 🔴 既定値（記憶 `project-jiko-rules-index` §5）
#   ① **`【映像あり】` は末尾**（2026-09-14 カズヤくん・7本目で「先頭に」を上書き）
#   ② **世間で通っている短い呼び名は、タイトルとサムネの両方で使う**
#      ＝この回は「コロンビア号」。正式名（スペースシャトル・コロンビア号）だけにしない
#   ⚠️ 「隠蔽」0.80倍／「衝撃」0.83倍／「闇」0.92倍／「結末」0.60倍＝**逆効果**
#   ⚠️ 「即死・絶命」はタイトル・サムネには出さない（本編では原文どおり読む）
TITLES = {
    # A＝7本目と同じ型（この回の差 → 委員会の言葉 → 規模と通り名 → 札）
    "A": ("軌道の機体を撮ってくださいという求めは、三度とも退けられた。"
          "委員会はのちに「困難だが、実行可能だった」と書いた。"
          "7人が亡くなったコロンビア号空中分解事故の真相【事故検証】【映像あり】"),
    # B＝時間の順序を前に出す型（原因は当日ではなく16日前、という筋をそのまま言う）
    "B": ("壊れたのは再突入の日ではない。16日前の打ち上げ81.7秒後、"
          "断熱材のかけらが左の翼に当たっていた。"
          "7人が亡くなったコロンビア号空中分解事故の真相【事故検証】【映像あり】"),
    # C＝「助ける道はあったのか」を主にする型（第6章が核）
    "C": ("助ける道は「困難だが、実行可能」だった。"
          "だが軌道の機体を撮ってくださいという求めは、三度とも退けられた。"
          "7人が亡くなったコロンビア号空中分解事故の真相【事故検証】【映像あり】"),
}
TITLE_PICK = "A"      # ⚠️ 試写でカズヤくんが選んだら書き換える

HEAD = """【この動画について】
2003年2月1日の朝、スペースシャトル・コロンビア号は、フロリダの滑走路に降りてくるはずでした。降りてきませんでした。着陸の予定は午前9時16分。その前の9時00分18秒、機体はテキサスの空でばらばらになり、乗っていた7人全員が亡くなりました。

ですが、機体が壊れはじめたのは、この日ではありません。16日前の打ち上げ、81.7秒後です。燃料タンクを覆う断熱材のかけらがはがれ、0.2秒後に左の翼に当たっていました。気づいたのは翌日、一晩かけて現像したフィルムの中でした。

そこから16日間、地上では「軌道にいる機体を、望遠鏡か衛星で撮ってほしい」という求めが三度出て、三度とも取り消されます。事故のあと、委員会は「助ける道は、困難だが実行可能だった」と書きました。この動画は、その16日間を順番どおりにたどります。

背骨にしたのは、コロンビア号事故調査委員会が2003年に出した報告書（第1巻）です。画面に出る時刻・寸法・速さは、すべてこの報告書に書かれた値です。

・打ち上げの81.7秒後に、何がどこへ当たったのか
・翌日フィルムに写っていたものを、誰が、どう扱ったのか
・「撮ってください」は、なぜ三度とも退けられたのか
・助ける道は本当にあったのか。委員会は何を計算させたのか
・2月1日の管制室で、画面から何が消えていったのか
・テキサスに降ってきたものから、委員会は何を読み取ったのか

※ 亡くなったのは乗員7名です。地上でけがをした人は出ていません。
※ 捜索の途中でヘリコプターが1機落ち、2名が亡くなっています。
"""


def read_glossary() -> str:
    """`ref/ep8/yougo.md` の「## 1. 貼る本文」の囲みを**そのまま**返す。"""
    md = YOUGO.read_text(encoding="utf-8")
    m = re.search(r"## 1\. 貼る本文.*?\n```\n(.*?)\n```", md, re.S)
    if not m:
        raise SystemExit("🔴 yougo.md の「貼る本文」の囲みが見つからない。書かずに止めた。")
    body = m.group(1).strip()
    if "【この動画に出てくる言葉】" not in body:
        raise SystemExit("🔴 囲みの中身が用語の本文ではない。書かずに止めた。")
    n = body.count("\n・")
    if n != N_GLOSS:
        raise SystemExit(f"🔴 用語の行が {n} 語（仕様は {N_GLOSS}）。書かずに止めた。")
    return body


def _rows(head_re: str, want: int) -> list[list[str]]:
    """`ref/CREDITS.md` の見出しから次の見出しまでの表の行を返す（fail closed）。"""
    lines = CREDITS.read_text(encoding="utf-8").splitlines()
    try:
        start = next(i for i, s in enumerate(lines) if re.match(head_re, s))
    except StopIteration:
        raise SystemExit(f"🔴 見出しが見つからない: {head_re}。書かずに止めた。")
    rows = []
    for s in lines[start + 1:]:
        if s.startswith("### ") or s.startswith("## "):
            break
        if not s.startswith("| `"):
            continue
        rows.append([x.strip() for x in s.strip().strip("|").split("|")])
    if len(rows) != want:
        raise SystemExit(f"🔴 {head_re} の表が {len(rows)} 行（仕様は {want}）。書かずに止めた。")
    return rows


def read_credits() -> str:
    """写真74点・動く映像9本のクレジットを組み立てる。"""
    # ① 写真。**CC BY が1点でも混ざったら撮影者名を出さねばならない**ので、そこで止める。
    pd_n, cc = 0, {}
    for c in _rows(r"^### 1\. 写真74点", N_PHOTO):
        right, who = c[3], c[4].strip().rstrip(".").strip()
        if right.startswith("PD（"):
            pd_n += 1
        elif right.startswith("CC BY"):
            cc.setdefault(right, set()).add(who)
        else:
            raise SystemExit(f"🔴 権利の欄が読めない: {right}。書かずに止めた。")
    if pd_n != N_PHOTO:
        raise SystemExit(
            f"🔴 PD でない写真が {N_PHOTO - pd_n} 点ある（CC BY は撮影者名が使用条件）。"
            f"この道具は PD だけを前提に書いてある。書かずに止めた。: {sorted(cc)}")

    # ② 動く映像。`guncam` だけ経路が違うので**分けて**書く。
    nasa, other = [], []
    for c in _rows(r"^### 2\. 動く映像9本", N_CLIP):
        key, src, right = c[0].strip("` "), c[1], c[2]
        if c[3].startswith("**使わない") or c[3].startswith("使わない"):
            continue
        (nasa if "米連邦職員の職務著作" in right else other).append((key, src))
    if len(nasa) + len(other) != 7:
        raise SystemExit(f"🔴 使っている映像が {len(nasa) + len(other)} 本（仕様は 7）。書かずに止めた。")
    if [k for k, _ in other] != ["guncam"]:
        raise SystemExit(f"🔴 経路の違う映像が guncam 以外にある: {other}。書かずに止めた。")

    return (
        "【出典】\n"
        "・コロンビア号事故調査委員会 報告書 第1巻（2003年8月）\n"
        f"・写真 {N_PHOTO}点：NASA（ケネディ宇宙センター／ジョンソン宇宙センター／"
        "マーシャル宇宙飛行センター）。パブリックドメイン（合衆国法典17編105条）\n"
        f"・記録映像 {len(nasa)}本：NASA。パブリックドメイン（同上）\n"
        "・空中分解の記録映像：2003年2月1日、テキサス州フォートフッドで"
        "AH-64D の照準カメラが記録したもの。NASA が同年2月12日に公開した録画。"
        "パブリックドメイン\n")


def main() -> int:
    if "--titles" in sys.argv:
        for k, t in TITLES.items():
            mark = "🔴 超過" if len(t) > 100 else "✓"
            print(f"{k}  {len(t):3d}字 / 上限100  {mark}\n    {t}\n")
        return 0

    title = TITLES[TITLE_PICK]
    desc = "\n".join([HEAD, read_glossary(), "", read_credits()])

    print(f"タイトル（{TITLE_PICK}案） {len(title)} 字（上限 100）")
    print(f"説明                 {len(desc)} 字（上限 5,000）")
    if len(title) > 100 or len(desc) > 5000:
        raise SystemExit("🔴 上限を超えた。書かずに止めた。")

    meta = {
        "slug": "ep8",
        "title": title,
        "description": desc,
        "tags": ["コロンビア号", "スペースシャトル", "2003年", "NASA", "事故検証",
                 "図解", "事故調査委員会", "STS-107", "宇宙開発", "断熱材",
                 "再突入", "一次資料", "解説", "ドキュメンタリー"],
        # ⚠️ サムネは試写でカズヤくんが選んでから書き換える
        "thumbnail": "out/thumb/ep8-t1/ep8_a_saved.png",
        "genre": "jiko",
        "playlist": "",
    }
    if "--dry" in sys.argv:
        print("\n" + desc)
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✓ 書いた → {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
