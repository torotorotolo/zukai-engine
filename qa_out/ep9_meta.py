# -*- coding: utf-8 -*-
"""9本目（テネリフェ）の `config/meta_ep9.json` を**機械で**組み立てる（2026-09-17・⑥）。

`qa_out/ep8_meta.py` を写して、この回の形に合わせた。

🔴 手で書かない理由（ep7・ep8 と同じ）
  ① 用語17語は `ref/ep9/yougo.md` の「貼る本文」の囲みが正本＝**囲みの中をそのまま**貼る
  ② クレジットは `ref/CREDITS.md` §テネリフェ の表から、**使うカットがある行だけ**を機械で拾う。
     行数・権利の欄が仕様と違えば**書かずに落ちる**
  ③ タイトル 100字・説明 5,000字の上限を、書く前に確かめる

🔴 この回が 8本目と違うところ
  - 写真 73点のうち **CC BY が30点**（2.0／2.5／3.0／4.0）＝**撮影者名が使用条件**。版ごとに名前と許諾の URL を載せる
  - 動く映像は0本（【映像あり】を付けない・映像の出典の行を置かない）
  - 🔴 **BGM を付けない回**（2026-09-17 カズヤくん指示）＝【音楽】の欄を置かない（`audio_mix.BGM_CREDIT` を入れない）
  - 目次（チャプター）を戻した（1〜6本目にはあり、7・8本目で抜けていた）。秒は `scene_jiko.CUTS` から積む
    ＝**焼いた版と同じ `audio/narration.json`** から出る値

    python qa_out/ep9_meta.py            # 組み立てて config/meta_ep9.json に書く
    python qa_out/ep9_meta.py --dry      # 書かずに中身と字数だけ出す
"""
import json
import re
import sys
from collections import OrderedDict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
import scene_jiko as S  # noqa: E402

YOUGO = HERE / "ref" / "ep9" / "yougo.md"
CREDITS = HERE / "ref" / "CREDITS.md"
OUT = HERE / "config" / "meta_ep9.json"

N_GLOSS = 17          # `ref/ep9/yougo.md` §1 の語数（⑤a で確定）
N_PHOTO_ROWS = 126    # §1 の表の行数
N_PHOTO_USED = 73     # そのうち使うカットがある行（⑥ ep03 の差し替えで 02→06・数は不変）

# ✅ ④' で決め直したタイトル（台本第2版 §1-1 の推奨・76字）。`【映像あり】` は付けない（動く映像0本）
TITLE = ("二機とも、来るはずのない空港にいた。「離陸は待て」という管制官の声は別の無線と重なって消え、"
         "583人が亡くなったテネリフェ空港衝突事故の真相【事故検証】")

# ⚠️ 書いてはいけないこと（記憶 project-jiko-ep9-tenerife）を守る：C-3 の角度・ILS の滑走路・
#    「副操縦士が止めた」・248/326/335 の内訳（報告書に印字されていない合算）は書かない。
#    583 はタイトルと同じ扱い（④'で承認）。一方だけを裁かない＝原因と「寄与した要因」を並べて紹介する
HEAD = """【この動画について】
1977年3月27日の夕方、スペインのカナリア諸島にあるテネリフェ島。ロス・ロデオス空港の滑走路の上で、2機のボーイング747がぶつかりました。KLMオランダ航空4805便と、パンアメリカン航空1736便です。583人が亡くなりました。航空機の事故で、いまも最も多い数です。

二機とも、この空港に来るはずではありませんでした。行き先だったグランカナリア島のラスパルマス空港で、二機が空を飛んでいるあいだに爆弾が爆発し、テネリフェ島の小さな空港へ回されていたのです。

滑走路は1本だけ。この日は誘導路が並んだ機体でふさがって使えず、離陸する機体は、滑走路を逆向きに走って端で向きを変えることになりました。そのあいだに、雲が滑走路へ降りてきます。そして「離陸は待て」という管制官の声は、別の無線と重なって聞き取れなくなりました。

この動画は、スペインが出した事故報告書と、操縦室の音声記録の書き起こしをもとに、その日の午後を順番どおりにたどります。報告書が挙げた原因と、それに寄与した要因を、報告書の言葉に沿って紹介します。

・二機はなぜ、来るはずのなかった空港にいたのか
・小さな空港で、誘導路はなぜ使えなかったのか
・雲が滑走路へ降りてきたとき、見通しはどれだけ落ちていたのか
・「ATCの許可」と「離陸の許可」は、何が違ったのか
・「離陸は待て」の声と別の無線が重なった30秒に、何が起きていたのか
・ぶつかったあと、61人はどうやって機体から逃げたのか
・報告書は、何を原因と書き、何を勧告したのか
"""

LICENSE_URL = {
    "2.0": "https://creativecommons.org/licenses/by/2.0/deed.ja",
    "2.5": "https://creativecommons.org/licenses/by/2.5/deed.ja",
    "3.0": "https://creativecommons.org/licenses/by/3.0/deed.ja",
    "4.0": "https://creativecommons.org/licenses/by/4.0/deed.ja",
}
# 撮影者名の表記（Commons の撮影者欄のまま出せないもの）
AUTHOR_FIX = {"Willy Pragher": "Willy Pragher（Landesarchiv Baden-Württemberg）"}


def read_glossary() -> str:
    """`ref/ep9/yougo.md` の「## 1. 貼る本文」の囲みを**そのまま**返す（末尾の注2つを含む）。"""
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


def photo_rows() -> list[list[str]]:
    lines = CREDITS.read_text(encoding="utf-8").splitlines()
    try:
        start = next(i for i, s in enumerate(lines) if s.startswith("### 1. 写真 126点"))
    except StopIteration:
        raise SystemExit("🔴 CREDITS.md §テネリフェ の写真の表が見つからない。書かずに止めた。")
    rows = []
    for s in lines[start + 1:]:
        if s.startswith("### ") or s.startswith("## "):
            break
        if s.startswith("| `"):
            rows.append([x.strip() for x in s.strip().strip("|").split("|")])
    if len(rows) != N_PHOTO_ROWS:
        raise SystemExit(f"🔴 写真の表が {len(rows)} 行（仕様は {N_PHOTO_ROWS}）。書かずに止めた。")
    return rows


def read_credits() -> str:
    used = [r for r in photo_rows() if r[1]]
    if len(used) != N_PHOTO_USED:
        raise SystemExit(f"🔴 使う写真が {len(used)} 点（仕様は {N_PHOTO_USED}）。書かずに止めた。")
    free, by = 0, OrderedDict((v, []) for v in LICENSE_URL)
    for r in used:
        right, who = r[3], r[4].strip()
        if right == "CC0" or right.startswith("PD（"):
            free += 1
            continue
        m = re.fullmatch(r"CC BY（CC BY (\d\.\d)）", right)
        if not m or m.group(1) not in LICENSE_URL:
            raise SystemExit(f"🔴 権利の欄が読めない: {right}（{r[0]}）。書かずに止めた。")
        if not who:
            raise SystemExit(f"🔴 CC BY なのに撮影者が空: {r[0]}。書かずに止めた。")
        who = AUTHOR_FIX.get(who, who)
        if who not in by[m.group(1)]:
            by[m.group(1)].append(who)
    n_cc = len(used) - free
    out = ["【出典】",
           "・スペインの事故報告書 A-102/1977・A-103/1977（1978年11月6日付）と、その英訳（ICAO Circular 153-AN/56）",
           "・操縦室の音声記録（CVR）の書き起こし",
           f"・写真 {free}点：オランダ国立公文書館（Anefo）ほか。CC0／パブリックドメイン"]
    for v, names in by.items():
        if names:
            out.append(f"・写真（CC BY {v}）：" + "／".join(names))
            out.append(f"　{LICENSE_URL[v]}")
    out.append(f"（CC BY の写真 {n_cc}点は、色調の変更と切り出しをしています）")
    out.append("")
    out.append("動画に出てくる数値・時刻・無線の言葉は、この報告書と書き起こしによります。")
    return "\n".join(out)


def chapters() -> str:
    starts, t = {}, 0.0
    for cid, sec in S.CUTS:
        starts[cid] = t
        t += sec
    rows = [("pr01", "はじめに")]
    for key, (n, name) in S.CHAPTERS.items():
        first = next((c for c, _ in S.CUTS if c.startswith(key) and c[len(key):].isdigit()), None)
        if first is None:
            raise SystemExit(f"🔴 章 {key} の最初のカットが無い。書かずに止めた。")
        rows.append((first, f"第{n}章 {name}"))
    rows.append(("ep01", "おわりに"))
    lines, last = ["【目次】"], float("-inf")
    for cid, label in rows:
        x = starts[cid]
        if x <= last + 10:
            raise SystemExit(f"🔴 目次の秒が前と10秒以上離れていない／逆順: {cid}。書かずに止めた。")
        last = x
        lines.append(f"{int(x // 60):02d}:{int(x % 60):02d} {label}")
    if len(rows) < 3 or starts[rows[0][0]] != 0.0:
        raise SystemExit("🔴 YouTube の目次の条件（0:00 から・3つ以上）を満たさない。書かずに止めた。")
    return "\n".join(lines)


def main() -> int:
    desc = "\n".join([HEAD, chapters(), "", read_glossary(), "", read_credits()])
    for bad in ("<", ">", "BGM", "蒲鉾さちこ", "DOVA", "148度", "【映像あり】"):
        if bad in desc or bad in TITLE:
            raise SystemExit(f"🔴 入れてはいけない語「{bad}」が入っている。書かずに止めた。")
    print(f"タイトル {len(TITLE)} 字（上限 100）")
    print(f"説明     {len(desc)} 字（上限 5,000）")
    if len(TITLE) > 100 or len(desc) > 5000:
        raise SystemExit("🔴 上限を超えた。書かずに止めた。")
    meta = {
        "slug": "ep9",
        "title": TITLE,
        "description": desc,
        "tags": ["テネリフェ空港衝突事故", "テネリフェ", "ロス・ロデオス空港", "KLM", "パンアメリカン航空",
                 "ボーイング747", "航空事故", "1977年", "事故検証", "図解", "航空管制", "事故報告書",
                 "解説", "ドキュメンタリー"],
        # ✅ 2026-09-17 ⑥：t1 の3案から a＝「待ての声は届かず」（210px で3案とも読める・核心＝声が届かなかった）
        "thumbnail": "out/thumb/ep9-t1/ep9_a_matte.png",
        "genre": "jiko",
        "playlist": "",
    }
    if "--dry" in sys.argv:
        print("\n" + TITLE + "\n\n" + desc)
        return 0
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✓ 書いた → {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
