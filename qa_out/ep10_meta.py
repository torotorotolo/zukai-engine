# -*- coding: utf-8 -*-
"""10本目（三豊百貨店）の `config/meta_ep10.json` を**機械で**組み立てる（2026-09-20・⑥）。

`qa_out/ep9_meta.py` を写して、この回の形に合わせた。

🔴 手で書かない理由（ep7〜ep9 と同じ）
  ① 用語17語は `ref/ep10/yougo.md` の「貼る本文」の囲みが正本＝**囲みの中をそのまま**貼る
  ② クレジットは **章ファイル（`cuts.SPEC`）が実際に出している写真**を拾い、
     `ref/CREDITS.md` §三豊 の表と突き合わせる。表に無い欄があれば**書かずに落ちる**
  ③ タイトル 100字・説明 5,000字の上限を、書く前に確かめる

🔴 この回が 9本目と違うところ
  - 権利の形が**3つ**ある＝CC BY-SA 4.0（額装のみ・無改変）／公共ヌリ第1類型／
    公共ヌリ第1類型＋CC BY 4.0。**CC BY-SA は「無改変であること」も表示の条件**
    （→ 記憶 reference-cc-by-sa-unmodified-in-video・`ref/ep10/materials.md` §1 に許諾の原文）
  - 🔴 **撮影者名は原語（ハングル）と片仮名を併記する**（2026-09-20 カズヤくん決定）。
    画面の隅は片仮名のまま＝本編のフォント（NotoSansJP・DelaGothicOne）に
    **ハングルの字形が1つも入っていない**ため（実測：`getBestCmap()` に 최/광/모 なし）。
    概要欄は Unicode で出るので、ここで原語を満たす。
  - 動く映像は0本（【映像あり】を付けない）
  - 🔴 **BGM を付けない回**（2026-09-20 カズヤくん決定・`--bgm none`）＝【音楽】の欄を置かない

    python qa_out/ep10_meta.py            # 組み立てて config/meta_ep10.json に書く
    python qa_out/ep10_meta.py --dry      # 書かずに中身と字数だけ出す
"""
import json
import re
import sys
from collections import OrderedDict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
import cuts                       # noqa: E402
import scene_jiko as S            # noqa: E402

YOUGO = HERE / "ref" / "ep10" / "yougo.md"
CREDITS = HERE / "ref" / "CREDITS.md"
OUT = HERE / "config" / "meta_ep10.json"

EP_PREFIX = "ep10/"
TABLE_HEAD = "| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | 素材の題名 |"
N_GLOSS = 17          # `ref/ep10/yougo.md` §1 の語数（⑤a で確定）
N_PHOTO_ROWS = 92     # §1 の表の行数
N_SLOTS_USED = 84     # 章ファイルが実際に出している写真の欄（⑤c' 時点の実測）

# ✅ ④' で決め直したタイトル（台本第2版 §1-1 の推奨・87字）。
#    🔴 `【映像あり】` は付けない（商用で使える1995年の動く映像が0本）
TITLE = ("その日の朝、5階の食堂の床はもう盛り上がっていた。午後3時10分に現場に着いた技術者の診断は"
         "「すぐに崩れる危険はない」、502人が亡くなった三豊百貨店崩壊事故の真相【事故検証】")

# ⚠️ 書いてはいけないこと（台本第2版 §1-2〜§1-8）を守る：
#    人の名前を出さない／「20秒で崩れた」と言わない／「4階建てを5階に増やした」と言わない／
#    「会長は懲役7年6月」と言わない／事故のあとの法律は「災難管理法」（特別法ではない）。
#    数は白書の最終値（502／937／1,439）で揃える（`c906` と同じ）。
HEAD = """【この動画について】
1995年6月29日、木曜日の夕方5時55分ごろ。韓国の首都ソウル、瑞草区にあった三豊百貨店が崩れ落ちました。502人が亡くなり、937人がけがをしています。あわせて1,439人。そのうち半分以上が、21歳から30歳でした。

建物は、その日の朝から合図を出していました。5階の食堂の床はもう盛り上がり、天井からは水が落ちていました。午後3時10分、構造の技術者が現場に着きます。その診断は「すぐに崩れる危険はない」。補強はその日の夕方からと決まり、店は開いたまま、客を入れつづけました。崩れたのは、その2時間45分ほどのちです。

この動画が使うのは、公の記録だけです。ソウル市がまとめた白書、国会と検察の調査報告、そして裁判所の判決文。報道は使っていません。

・朝から出ていた合図は、どんなものだったのか
・商店街として計画された建物は、なぜ百貨店になったのか
・屋上に載せられた冷却塔は、どれだけの重さだったのか
・柱は、図面と実物でどれだけ違っていたのか
・「すぐに崩れる危険はない」という診断は、何を見て出されたのか
・建物は、どこから、どの順番で崩れたのか
・十七日間の救助で、生きて出てきた人は何人いたのか
・裁判所は、何を罪と認めたのか
"""

# 権利の欄（`ref/CREDITS.md` の表の書き方）→ 概要欄に出す形
RIGHTS = OrderedDict([
    ("CC BY-SA 4.0（額装のみ・無改変）", dict(
        name="CC BY-SA 4.0",
        url="https://creativecommons.org/licenses/by-sa/4.0/deed.ja",
        note="この写真は、切らず・色を変えず・何も重ねず、そのままの形で額に入れて出しています（無改変）")),
    ("KOGL Type 1（手直し可）", dict(
        name="公共ヌリ 第1類型（出典表示）",
        url="https://www.kogl.or.kr/info/license.do",
        note="")),
    ("KOGL Type 1 + CC BY 4.0（手直し可）", dict(
        name="公共ヌリ 第1類型 ＋ CC BY 4.0",
        url="https://creativecommons.org/licenses/by/4.0/deed.ja",
        note="")),
])

# 🔴 撮影者名の原語（ハングル）。`tools/check_credits.py` の `WHO_JA` の逆引き。
#    ⚠️ 片仮名は機械的な転写であって、当人の名乗りではない（表と同じ断り）。
WHO_KO = {
    "ソウル特別市 消防災難本部": "서울특별시 소방재난본부",
    "ソウル歴史編纂院": "서울역사편찬원",
    "ソウル特別市／ソウル研究院": "서울특별시／서울연구원",
    "チェ・グァンモ": "최광모",
}

# 素材の置き場（BY-SA の表示に要る4つのうちの「素材の URL」）
SOURCE_URL = {
    "ソウル特別市 消防災難本部": "https://commons.wikimedia.org/wiki/Category:Sampoong_Department_Store_collapse",
    "チェ・グァンモ": "https://commons.wikimedia.org/wiki/Category:Sampoong_Department_Store_collapse",
    "ソウル歴史編纂院": "https://history.seoul.go.kr/archive/",
    "ソウル特別市／ソウル研究院": "https://data.si.re.kr/",
}

PRIMARY = """【出典】
・ソウル特別市『삼풍백화점 붕괴사고 백서』（三豊百貨店崩壊事故 白書）1996年6月・761頁（国家記録院）
・大韓民国国会「삼풍백화점붕괴사건조사특별위원회」会議録 第1号〜第6号（1995年）。第6号に国政調査結果報告書の全文と、添付のソウル特別市・瑞草区・ソウル地方検察庁の報告
・1995年度 国政監査 会議録（内務委員会 1995年10月10日／建設交通委員会 1995年10月11日。被監査機関＝ソウル特別市）
・大法院 1996年8月23日 宣告 96도1231 判決（刑事・全文）／大法院 1999年12月21日 宣告 98다29797 判決（民事）
・ソウル特別市 事故対策本部「措置状況報告（第31次）」1995年7月7日（ソウル記録院）"""

TAIL = """動画に出てくる数値・時刻・判決の言葉は、これらの記録によります。
資料によって数が違うところ（崩壊の時刻、冷却塔の数、亡くなった人の数）は、画面でそのまま断っています。"""


def read_glossary() -> str:
    """`ref/ep10/yougo.md` の「## 1. 貼る本文」の囲みを**そのまま**返す。"""
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


def photo_rows() -> dict:
    """§三豊 の写真の表を、欄の名前で引ける形にして返す。"""
    lines = CREDITS.read_text(encoding="utf-8").splitlines()
    try:
        start = next(i for i, s in enumerate(lines)
                     if s.strip() == TABLE_HEAD and i > 1400)
    except StopIteration:
        raise SystemExit("🔴 CREDITS.md §三豊 の写真の表が見つからない。書かずに止めた。")
    rows = []
    for s in lines[start + 1:]:
        if s.startswith("### ") or s.startswith("## "):
            break
        if s.startswith("| `"):
            rows.append([x.strip() for x in s.strip().strip("|").split("|")])
    if len(rows) != N_PHOTO_ROWS:
        raise SystemExit(f"🔴 写真の表が {len(rows)} 行（仕様は {N_PHOTO_ROWS}）。書かずに止めた。")
    return {r[0].strip("`"): r for r in rows}


def used_slots() -> set:
    """🔴 章ファイルが**実際に出している**写真の欄（`check_credits.py` と同じ拾い方）。"""
    out = set()
    for spec in cuts.SPEC.values():
        photo = spec.get("photo") or ""
        if photo.startswith(EP_PREFIX) and "/fb_" not in photo:
            out.add(Path(photo).stem)
    if len(out) != N_SLOTS_USED:
        raise SystemExit(f"🔴 出している写真が {len(out)} 欄（仕様は {N_SLOTS_USED}）。書かずに止めた。")
    return out


def read_credits() -> str:
    table, used = photo_rows(), used_slots()
    missing = sorted(s for s in used if s not in table)
    if missing:
        raise SystemExit(f"🔴 表に無い写真を出している: {missing}。書かずに止めた。")
    # 権利 → 撮影者 → 点数
    groups = OrderedDict((k, OrderedDict()) for k in RIGHTS)
    for slot in sorted(used):
        right, who = table[slot][3], table[slot][4].strip()
        if right not in RIGHTS:
            raise SystemExit(f"🔴 権利の欄が読めない: {right}（{slot}）。書かずに止めた。")
        if not who:
            raise SystemExit(f"🔴 撮影者が空: {slot}。撮影者名は使用条件そのもの。書かずに止めた。")
        if who not in WHO_KO or who not in SOURCE_URL:
            raise SystemExit(f"🔴 撮影者「{who}」の原語か素材の URL が無い。書かずに止めた。")
        groups[right][who] = groups[right].get(who, 0) + 1

    out, total = ["【出典・写真】"], 0
    for right, by_who in groups.items():
        if not by_who:
            continue
        n = sum(by_who.values())
        total += n
        spec = RIGHTS[right]
        names = "／".join(f"{WHO_KO[w]}（{w}）" for w in by_who)
        out.append(f"・写真 {n}点：{names}")
        out.append(f"　{spec['name']}　{spec['url']}")
        for url in OrderedDict.fromkeys(SOURCE_URL[w] for w in by_who):
            out.append(f"　素材：{url}")
        if spec["note"]:
            out.append(f"　{spec['note']}")
    if total != len(used):
        raise SystemExit(f"🔴 点数の合計が合わない（{total} ≠ {len(used)}）。書かずに止めた。")
    out.append("⚠️ 撮影者名の片仮名は機械的な転写で、ご本人の名乗りではありません。")
    return "\n".join(out)


def chapters() -> str:
    starts, t = {}, 0.0
    for cid, sec in S.CUTS:
        starts[cid] = t
        t += sec
    rows = [("pr01", "はじめに")]
    for key, (n, name) in S.CHAPTERS.items():
        first = next((c for c, _ in S.CUTS
                      if c.startswith(key) and c[len(key):].isdigit()), None)
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
    desc = "\n".join([HEAD, chapters(), "", read_glossary(), "",
                      PRIMARY, "", read_credits(), "", TAIL])
    # 🔴 入れてはいけない語（④ の決めごと＋BGMなしの回＋動く映像0本）
    for bad in ("<", ">", "BGM", "DOVA", "【映像あり】", "20秒で崩れ",
                "特別法", "4階建てを5階", "懲役7年6月"):
        if bad in desc or bad in TITLE:
            raise SystemExit(f"🔴 入れてはいけない語「{bad}」が入っている。書かずに止めた。")
    print(f"タイトル {len(TITLE)} 字（上限 100）")
    print(f"説明     {len(desc)} 字（上限 5,000）")
    if len(TITLE) > 100 or len(desc) > 5000:
        raise SystemExit("🔴 上限を超えた。書かずに止めた。")
    thumb = "out/thumb/ep10-t1/ep10_a_matte.png"
    meta = {
        "slug": "ep10",
        "title": TITLE,
        "description": desc,
        "tags": ["三豊百貨店", "三豊百貨店崩壊事故", "サンプン百貨店", "ソウル", "韓国",
                 "1995年", "建築", "フラットスラブ", "せん断破壊", "事故検証", "図解",
                 "事故報告書", "解説", "ドキュメンタリー"],
        "thumbnail": thumb,
        "genre": "jiko",
        "playlist": "",
    }
    if "--dry" in sys.argv:
        print("\n" + TITLE + "\n\n" + desc)
        return 0
    if not (HERE / thumb).exists():
        raise SystemExit(f"🔴 サムネが無い: {thumb}。焼いてから書くこと。")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✓ 書いた → {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
