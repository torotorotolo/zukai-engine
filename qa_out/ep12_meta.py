# -*- coding: utf-8 -*-
"""12本目（キャッスル・ブラボー）の `config/meta_ep12.json` を**機械で**組み立てる（2026-09-24・⑥）。

`qa_out/ep11_meta.py` を写して、この回の形に合わせた。

🔴 手で書かない理由（ep7〜ep11 と同じ）
  ① 用語は `ref/ep12/yougo.md` の「貼る本文」の節が正本＝**そのまま**貼る（`**` だけ外す）
  ② 素材の点数は**章ファイルの実配線**（`cuts.SPEC` の `photo`・`footage.USE`）から数え、
     権利は `ref/CREDITS.md` §キャッスル・ブラボー の表で引く。**表に無い写真・PD 以外が1点でもあれば落ちる**
  ③ 目次は `scene_jiko.CUTS` の秒を頭から積む＝**焼いた版と同じ秒**（⑥で完成尺を実測して突き合わせる）
  ④ タイトル 100字・説明 5,000字の上限と、入れてはいけない語を、書く前に確かめる

🔴 この回が 11本目と違うところ
  - 表の「使うカット」欄は「（章ファイル）」で、**表は素材の在庫（108行）**。使った点数ではない
    → 点数は `cuts.SPEC` から数える（在庫を数えると使っていない写真まで名乗る）
  - 権利の形が**3つ**：NARA RG 678（米連邦 §105）／Commons の米国の職務著作／
    **日本で1957年より前に公表された写真**（読売新聞・アサヒグラフ）
  - 動く映像は**2本の別の素材**：DOE の記録映像（§105）と、Commons の4K版
    （**§105 ではなく「米国で発行され著作権が更新されなかった」PD**・`ref/ep12/materials.md` §3-1）
  - 報告書の頁を21枚、絵として出している（`ss.page`）＝頁の番号帯で報告書を分ける
  - 🔴 BGM を付ける回だが、`audio_mix.BGM_CREDIT` は**概要欄に入れない**（表示は不要＝必須でないクレジットは書かない）
  - 🔴 「知りながら撃った」（本文で伝説として扱う言い回し）・「2.5倍」（計算した数）は入れない
  - 目次の最後に「おわりに」を置かない（共通エンディング `ed01` は10秒に満たない＝YouTube の目次の条件を割る）

    python qa_out/ep12_meta.py            # 組み立てて config/meta_ep12.json に書く
    python qa_out/ep12_meta.py --dry      # 書かずに中身と字数だけ出す
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
import scene_jiko as S            # noqa: E402

YOUGO = HERE / "ref" / "ep12" / "yougo.md"
CREDITS = HERE / "ref" / "CREDITS.md"
OUT = HERE / "config" / "meta_ep12.json"

SECTION = "## キャッスル・ブラボー水爆実験"
N_GLOSS = 14          # `ref/ep12/yougo.md` の「貼る本文」の語数（⑤a で確定）
N_PAGES = 21          # 報告書の頁を絵として出す欄（⑤b-4 で確定・⑥で実配線から数えて一致）
CLIPS = {"doe": 5, "bravo4k": 6}   # 動く映像の欄（`footage.USE`）。素材が替わったら権利の文も替える

# ✅ 台本第2版 §1-1 の推奨A（2026-09-23 カズヤくん承認）。90字・型の幅 67〜94。
#    1文目＝決め所 `c414`（p209 を画像で読んだ）／2文目＝帰属つきでひっくり返す（`c422`・`c521`・`c915`）。
TITLE = ("撃つ前の夜、高さ6キロの風は人の住む島へ向かっていた。"
         "だが後の報告書は、島の灰は雲の高い所から降ったとする。"
         "第五福竜丸の23人が被曝したビキニ水爆実験の真相【事故検証】【映像あり】")

# ⚠️ 本文（台本第2版 c101〜c111）で言っていることだけを書く。
#    船の位置（157キロ）は資料で2つある（日本政府の記録では約135キロ＝c605 の注）ので、ここには書かない。
#    実名は久保山愛吉さんだけ（④ の承認・台本第2版 §1-2）。乗組員は人数と役だけ。
HEAD = """【この動画について】
1954年3月1日、午前6時45分。太平洋のまん中のビキニ環礁で、アメリカが水素爆弾の実験を行いました。爆発は広島の原爆のおよそ1000倍、TNT火薬に直して1500万トンぶん。アメリカ国防総省の報告書も「爆発の威力は、予想よりはるかに大きかった」と書いています。

爆発でまき上げられた、放射能を帯びた灰は、風に乗って東へ流れました。その先の海にいたのが、日本のマグロ漁船「第五福竜丸」です。乗っていた23人の上に、白い灰が降りました。その年の9月、無線長だった久保山愛吉さんが亡くなっています。灰が降ったのは船の上だけではありません。東の島々でも、住民239人とアメリカ兵28人が、灰の放射線を浴びました。

何が、灰を人の住む島へ運んだのか。よく語られる答えと、2013年にまとめられた報告書の答えは、同じではありません。この動画は、アメリカ国防総省の機関が1982年と2013年にまとめた2冊の報告書と、医師団の報告書を、英語の原文で当たっています。日本側の出来事は、日本政府の当時の記録と、国会の議事録で確かめました。

・水素爆弾とは何か。キャッスル作戦は、何を目指していたのか
・威力の見込みは、なぜ外れたのか
・撃つ前の夜、風はどちらへ向かっていたのか
・1500万トンの爆発は、何を空へまき上げたのか
・第五福竜丸の23人は、何を見て、何を浴びたのか
・島に降った灰は、住民とアメリカ兵に何をもたらしたのか
・日本に帰ってきた灰は、何を引き起こしたのか
・そのあと、何が変わったのか
"""

# 台本第2版 §10 の出典一覧から、本文の決め所と数を支えるものを挙げる。
PRIMARY = """【出典】
・米国防核兵器局（DNA）『CASTLE SERIES, 1954』（DNA 6035F・1982年）
・米国防脅威削減局（DTRA）Kunkle & Ristvet『Castle Bravo: Fifty Years of Legend and Lore』（2013年）
・『Operation Castle, Project 4.1』（WT-923・ロンゲラップの住民とアメリカ兵の医学的な所見）
・DASA 1251 Vol.II（降灰の数表）
・米原子力委員会 一般諮問委員会 第41回議事録（1954年7月）
・Hewlett & Holl『Atoms for Peace and War』（米原子力委員会の公式史・1989年）
・米エネルギー省『United States Nuclear Tests』（DOE/NV-209 Rev.16）
・Bates & Chadwick, Fusion Science and Technology 80（2024年）
・米国務省『Foreign Relations of the United States, 1952–1954』Vol.XIV Part 2
・National Security Archive「Castle BRAVO at 70」（2024年）
・国会会議録（国立国会図書館）／焼津市・高知県・杉並区の記録／都立第五福竜丸展示館 ほか"""

TAIL = """動画に出てくる数値・時刻・証言の言葉は、これらの記録によります。
資料によって数が違うところ、報告書が言い切っていないところは、画面でそのまま断っています。"""


def read_glossary() -> str:
    """`ref/ep12/yougo.md` の「## 貼る本文」の節を**そのまま**返す（次の `---` か `## ` まで）。"""
    md = YOUGO.read_text(encoding="utf-8")
    m = re.search(r"^## 貼る本文[^\n]*\n(.*?)\n(?:---|## )", md, re.S | re.M)
    if not m:
        raise SystemExit("🔴 yougo.md の「貼る本文」の節が見つからない。書かずに止めた。")
    body = m.group(1).strip()
    if "【この動画に出てくる言葉】" not in body:
        raise SystemExit("🔴 節の中身が用語の本文ではない。書かずに止めた。")
    n = body.count("\n・")
    if n != N_GLOSS:
        raise SystemExit(f"🔴 用語の行が {n} 語（仕様は {N_GLOSS}）。書かずに止めた。")
    # 🔴 YouTube の概要欄は Markdown を解釈しない＝`**` は文字のまま出る
    body = body.replace("**", "")
    if "*" in body or "_" in body:
        raise SystemExit("🔴 外し切れない記号が残っている。書かずに止めた。")
    return body


def credit_table() -> dict:
    """§キャッスル・ブラボー の表を {欄: (撮影年, 権利, 撮影者, 所蔵と識別子)} で返す。"""
    lines = CREDITS.read_text(encoding="utf-8").splitlines()
    try:
        start = next(i for i, s in enumerate(lines) if s.startswith(SECTION))
    except StopIteration:
        raise SystemExit("🔴 CREDITS.md §キャッスル・ブラボー が見つからない。書かずに止めた。")
    rows = {}
    for s in lines[start + 1:]:
        if s.startswith("## "):
            break
        if not s.startswith("| `"):
            continue
        c = [x.strip() for x in s.strip().strip("|").split("|")]
        if len(c) != 6:
            raise SystemExit(f"🔴 表の列が {len(c)} 個（仕様は 6）: {s}。書かずに止めた。")
        rows[c[0].strip("`")] = tuple(c[2:])
    if not rows:
        raise SystemExit("🔴 §キャッスル・ブラボー に表の行が1つも無い。書かずに止めた。")
    return rows


def used_material():
    """章ファイルの実配線から、写真（権利の種類ごと）・頁・動く映像を数える。"""
    import cuts
    import footage as F
    table = credit_table()
    kinds, pages, stills, bad = Counter(), [], [], []
    seen = set()
    for cid, sp in cuts.SPEC.items():
        p = sp.get("photo")
        if not p or p in seen:
            continue
        seen.add(p)
        stem = Path(p).stem
        if re.fullmatch(r"fb_c\d+", stem):          # 動く映像の欄の控えの止め絵（同じ映像から抜いたもの）
            stills.append(stem)
            continue
        if p.endswith(".png") and stem.startswith("pg"):
            pages.append(int(stem[2:]))
            continue
        r = table.get(stem)
        if r is None:
            bad.append(f"{stem}（表に無い）")
            continue
        right = r[1]
        if right.startswith("Public domain (17 U.S.C. §105)"):
            kinds["nara"] += 1
        elif right.startswith("Public domain（米国の職務著作）"):
            kinds["us_commons"] += 1
        elif right.startswith("Public domain（日本・1957年より前に公表の写真）"):
            kinds["jp"] += 1
        else:
            bad.append(f"{stem}（{right}）")
    if bad:
        raise SystemExit(f"🔴 権利を名乗れない写真がある（この道具は3つの PD の形だけを前提に書いてある）。"
                         f"書かずに止めた: {bad}")
    if len(pages) != N_PAGES:
        raise SystemExit(f"🔴 報告書の頁が {len(pages)} 枚（仕様は {N_PAGES}）。書かずに止めた。")
    clips = Counter(v["clip"] for v in F.USE.values())
    if dict(clips) != CLIPS:
        raise SystemExit(f"🔴 動く映像の欄が {dict(clips)}（仕様は {CLIPS}）。素材が替わったら権利の文も"
                         "書き直すこと。書かずに止めた。")
    if len(stills) != sum(CLIPS.values()):
        raise SystemExit(f"🔴 映像の控えの止め絵が {len(stills)} 枚（映像の欄は {sum(CLIPS.values())}）。"
                         "書かずに止めた。")
    # 頁がどの報告書かは `ref/ep12/pages.json` の `doc` 欄で引く（番号帯で決め打ちしない）
    import cuts.ss as ss
    name = {"DNA 6035F": "dna", "WT-923": "wt", "DASA 1251": "dasa"}
    by_doc = Counter(name.get(ss.PAGES.get(f"pg{n}", {}).get("doc"), "?") for n in pages)
    if by_doc["?"]:
        raise SystemExit(f"🔴 どの報告書か分からない頁がある: {sorted(pages)}。書かずに止めた。")
    return kinds, by_doc, clips


def read_credits() -> str:
    kinds, by_doc, clips = used_material()
    n_photo = sum(kinds.values())
    print(f"■ 素材：写真 {n_photo}点（NARA {kinds['nara']}・Commons {kinds['us_commons']}・日本 {kinds['jp']}）"
          f"／頁 {sum(by_doc.values())}枚（DNA {by_doc['dna']}・WT {by_doc['wt']}・DASA {by_doc['dasa']}）"
          f"／動く映像 {sum(clips.values())}か所（DOE {clips['doe']}・4K版 {clips['bravo4k']}）")
    return (
        "【素材】\n"
        f"・写真 {n_photo}点：\n"
        f"　米国立公文書館（RG 678）{kinds['nara']}点＝パブリックドメイン（合衆国法典17編105条）\n"
        f"　米エネルギー省ほか米国政府の撮影 {kinds['us_commons']}点（ウィキメディア・コモンズ）"
        "＝パブリックドメイン（米国の職務著作）\n"
        f"　1954年の日本の報道写真 {kinds['jp']}点（読売新聞・アサヒグラフ／ウィキメディア・コモンズ）"
        "＝パブリックドメイン（日本で1957年より前に公表された写真）\n"
        f"・報告書の頁 {sum(by_doc.values())}枚：上の DNA 6035F・WT-923・DASA 1251 より"
        "＝パブリックドメイン（米国の職務著作）\n"
        f"・動く映像 {sum(clips.values())}か所：\n"
        f"　米エネルギー省の記録映像「Castle Bravo Detonation」{clips['doe']}か所"
        "＝パブリックドメイン（合衆国法典17編105条）\n"
        f"　「Castle Bravo 15 megaton detonation, 1954」{clips['bravo4k']}か所（ウィキメディア・コモンズ）"
        "＝パブリックドメイン（米国で発行され、著作権が更新されなかった映像）\n"
        "※ 継承（ShareAlike）の条件が付く素材は、この回では1点も使っていません。")


def chapters() -> str:
    starts, t = {}, 0.0
    for cid, sec in S.CUTS:
        starts[cid] = t
        t += sec
    rows = []
    for key, (n, name) in S.CHAPTERS.items():
        first = next((c for c, _ in S.CUTS
                      if c.startswith(key) and c[len(key):].isdigit()), None)
        if first is None:
            raise SystemExit(f"🔴 章 {key} の最初のカットが無い。書かずに止めた。")
        rows.append((first, f"第{n}章 {name}"))
    lines, last = ["【目次】"], float("-inf")
    for cid, label in rows:
        x = starts[cid]
        if x <= last + 10:
            raise SystemExit(f"🔴 目次の秒が前と10秒以上離れていない／逆順: {cid}。書かずに止めた。")
        last = x
        lines.append(f"{int(x // 60):02d}:{int(x % 60):02d} {label}")
    if len(rows) < 3 or starts[rows[0][0]] != 0.0:
        raise SystemExit("🔴 YouTube の目次の条件（0:00 から・3つ以上）を満たさない。書かずに止めた。")
    if t - last < 10:
        raise SystemExit("🔴 最後の章が10秒に満たない。書かずに止めた。")
    print(f"■ 設計の完成尺 {t:.2f} 秒＝{int(t // 60)}分{t % 60:05.2f}秒（30fps で {round(t * 30):,} コマ）")
    return "\n".join(lines)


def main() -> int:
    desc = "\n".join([HEAD, chapters(), "", read_glossary(), "",
                      PRIMARY, "", read_credits(), "", TAIL])
    # 🔴 入れてはいけない語（BGM のクレジット・本文で伝説として扱う言い回し・計算した数）
    for bad in ("<", ">", "BGM", "DOVA", "OpenTracks", "疑惑の霧", "Keido",
                "知りながら", "2.5倍", "ﾀﾋ"):
        if bad in desc or bad in TITLE:
            raise SystemExit(f"🔴 入れてはいけない語「{bad}」が入っている。書かずに止めた。")
    if "死亡" in TITLE:
        raise SystemExit("🔴 タイトルに「死亡」が入っている。書かずに止めた。")
    if "【映像あり】" not in TITLE:
        raise SystemExit("🔴 動く映像がある回なのに【映像あり】が無い。書かずに止めた。")
    print(f"タイトル {len(TITLE)} 字（上限 100 ／ 型の幅 67〜94）")
    print(f"説明     {len(desc)} 字（上限 5,000）")
    if len(TITLE) > 100 or len(desc) > 5000:
        raise SystemExit("🔴 上限を超えた。書かずに止めた。")
    if not (67 <= len(TITLE) <= 94):
        raise SystemExit("🔴 タイトルが型の幅（67〜94字）から外れた。書かずに止めた。")

    # 🔴 サムネはカズヤくんが決める（1巡目＝`jiko-thumb-ep12-t1`）。決まるまで空＝書かずに止まる
    thumb = ""
    meta = {
        "slug": "ep12",
        "title": TITLE,
        "description": desc,
        "tags": ["キャッスル・ブラボー", "ビキニ水爆実験", "第五福竜丸", "水爆実験", "水素爆弾",
                 "1954年", "ビキニ環礁", "マーシャル諸島", "ロンゲラップ", "被曝", "事故検証",
                 "図解", "一次資料", "解説", "ドキュメンタリー"],
        "thumbnail": thumb,
        "genre": "jiko",
        "playlist": "",
    }
    if "--dry" in sys.argv:
        print("\n" + TITLE + "\n\n" + desc)
        return 0
    if not thumb or not (HERE / thumb).exists():
        raise SystemExit(f"🔴 サムネが決まっていない／無い: {thumb!r}。決めて焼いてから書くこと。")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✓ 書いた → {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
