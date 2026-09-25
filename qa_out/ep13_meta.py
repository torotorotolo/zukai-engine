# -*- coding: utf-8 -*-
"""13本目（トルコ航空981便）の `config/meta_ep13.json` を**機械で**組み立てる（2026-09-25・⑥）。

`qa_out/ep12_meta.py` を写して、この回の形に合わせた。

🔴 手で書かない理由（ep7〜ep12 と同じ）
  ① 用語は `ref/ep13/yougo.md` の「## 貼る本文」の節が正本＝**そのまま**貼る（`**` だけ外す）
  ② 素材の点数は**章ファイルの実配線**（`cuts.SPEC` の `photo`）から数え、権利・撮影者・素材の URL は
     `ref/ep13/assets.json`（⑤b の `qa_out/ep13_assets.py` が作った表＝画面の出典と同じ出どころ）で引く。
     **表に無い写真・読めない権利・撮影者が空の点が1つでもあれば落ちる**
  ③ 目次は `scene_jiko.CUTS` の秒を頭から積む＝**焼いた版と同じ秒**（章の扉の2秒は CUTS に入っている
     ＝`scene_jiko.py` の `cuts = [(c, … + CARD_SEC …)]`）
  ④ タイトル 100字・説明 5,000字の上限と、入れてはいけない語を、書く前に確かめる

🔴 この回が 12本目と違うところ
  - 動く映像 0本＝【映像あり】を**付けない**（付いていたら止める・`footage.USE` が空でなければ止める）
  - 写真の権利が**8つ**：CC0（オランダ国立公文書館 Anefo）／PD（FAA・ダグラス社の広報写真）／
    CC BY 2.0・3.0・4.0／**CC BY-SA 2.0・2.0 fr・4.0（6点＝額装・無改変＝`ss.FRAME_ONLY`）**。
    BY-SA は「撮影者・許諾の名前と URL・素材の URL・無改変」の4つが表示の条件
  - CC BY の写真は本編で切り出しと色調の変更（`build_jiko.duotone`）をしている＝その旨を書く。
    名前の壁（`names_wall`）は私人の名前にモザイク（`ref/ep13/masked.json`）
  - 頁は 23枚（仏 最終報告 10・米上院 報告 6・AIB 8/76 1・AD 3・官報 1・SB 52-37 2）＝`ref/ep13/pages.json` の `doc`
  - 🔴 よく語られる通説（ストライキ・表示板の言語・ヒースロー・335人）は**入れない**
    （台本第2版 §1-7＝否定のためにも持ち出さない）
  - 本文は「日本の商社」と言い、社名を出していない＝概要欄にも社名を出さない
  - 目次の最後に「おわりに」を置かない（共通エンディング `ed01` は10秒に満たない＝YouTube の目次の条件を割る）

    python qa_out/ep13_meta.py            # 組み立てて config/meta_ep13.json に書く（サムネが決まってから）
    python qa_out/ep13_meta.py --dry      # 書かずに中身と字数だけ出す
"""
import json
import re
import sys
from collections import Counter, OrderedDict
from pathlib import Path
from urllib.parse import quote

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
import scene_jiko as S            # noqa: E402

YOUGO = HERE / "ref" / "ep13" / "yougo.md"
ASSETS = HERE / "ref" / "ep13" / "assets.json"
CREDITS_JSON = HERE / "ref" / "ep13" / "credits.json"
PAGES = HERE / "ref" / "ep13" / "pages.json"
OUT = HERE / "config" / "meta_ep13.json"

N_GLOSS = 20          # `ref/ep13/yougo.md` の「貼る本文」の語数（⑤a で確定）
N_PHOTOS = 22         # 章ファイルが出している写真（⑥で実配線から数えた・1点1カット）
N_PAGES = 23          # 報告書などの頁を絵として出す欄（⑥で実配線から数えた）
PAGE_DOCS = {"仏 最終報告": 10, "米上院 報告": 6, "AIB 8/76": 1, "AD 74-08-04": 1,
             "AD 74-12-07": 1, "AD 75-15-05": 1, "官報 1974-04-02": 1, "SB 52-37": 2}

# ✅ 台本第2版 §1-1 の推奨A（④'で「2年前」→「2年近く前」・⑤a でカズヤくん承認）。85字・型の幅 67〜94。
#    動く映像が無い回＝【映像あり】は付けない（§B4-3・12本目からの「先頭に」はある回だけ）。
TITLE = ("2年近く前にも、同じ型のドアが空中で外れていた。"
         "直す命令は、電話1本の約束で見送られた。"
         "日本人48人を含む346人が亡くなったトルコ航空981便墜落事故の真相【事故検証】")

# ⚠️ 本文（台本第2版 c101〜c107）で言っていることだけを書く。問いは c107 の3つをそのまま。
HEAD = """【この動画について】
1974年3月3日、日曜日の昼。パリの北東37キロの森に、トルコ航空981便が落ちました。乗っていた346人は、全員が亡くなっています。乗客のうち、日本人と確かめられたのは48人。その多くは、銀行や商社への入社が決まっていた、若い人たちでした。

原因は、機体の後ろにある、貨物室のドアでした。飛んでいる最中に、そのドアが外れたのです。実は2年近く前にも、同じ型の旅客機で、同じ位置のドアが空中で外れていました。フランスの事故報告書は、結論の最後に「危険は、前の事故ですでに明らかだった」と書いています。アメリカ上院の報告によれば、直すことは政府の命令にならず、航空の役所のトップとメーカーの社長の、電話1本の約束で決まりました。

この動画は、フランスの事故調査委員会の報告書を、原文で読んで作っています。アメリカ上院の調査報告と、日本の国会の記録も確かめました。

・なぜ、閉めたはずのドアが外れたのか
・なぜ、命令は出なかったのか
・なぜ、その直しが、この機体には入っていなかったのか
"""

# 台本第2版 §10 の出典一覧から、本文の決め所と数を支えるものを挙げる。
PRIMARY = """【出典】
・フランス 事故調査委員会の最終報告書（Rapport final・1976年2月・付属書つき）
・英国 航空事故調査局（AIB）『Aircraft Accident Report 8/76』（フランスの報告書の英訳）
・米上院 商業委員会 航空小委員会『Report on the oversight hearings and investigation of the DC-10 aircraft』（1974年6月）
・米国家運輸安全委員会（NTSB）『AAR-73-02』（ウィンザーの事故・1973年）
・米連邦航空局（FAA）耐空性改善命令 AD 74-08-04・AD 74-12-07・AD 75-15-05／米官報 1974年4月2日／ダグラス社 SB 52-37
・国会会議録（国立国会図書館）：衆議院の予算委員会・運輸委員会・交通安全対策特別委員会ほか（1972年・1974年・1976年）"""

TAIL = """動画に出てくる数値・時刻・証言の言葉は、これらの記録によります。
資料によって数が違うところ、報告書が言い切っていないところは、画面でそのまま断っています。"""

# 権利（`assets.json` の `lic`）→ 概要欄の許諾の URL。ここに無い権利が出たら止める
LICENSE_URL = OrderedDict([
    ("CC BY 2.0", "https://creativecommons.org/licenses/by/2.0/deed.ja"),
    ("CC BY 3.0", "https://creativecommons.org/licenses/by/3.0/deed.ja"),
    ("CC BY 4.0", "https://creativecommons.org/licenses/by/4.0/deed.ja"),
    ("CC BY-SA 2.0", "https://creativecommons.org/licenses/by-sa/2.0/deed.ja"),
    ("CC BY-SA 2.0 fr", "https://creativecommons.org/licenses/by-sa/2.0/fr/deed.ja"),
    ("CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0/deed.ja"),
])
FREE = ("CC0", "Public domain")


def read_glossary() -> str:
    """`ref/ep13/yougo.md` の「## 貼る本文」の節を**そのまま**返す（次の `---` か `## ` まで）。"""
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


def link(url: str) -> str:
    """🔴 Commons の URL の括弧・非 ASCII を %xx にする（YouTube の自動リンクが `)` で切れるのを防ぐ）。"""
    head, _, path = url.partition("/wiki/")
    if not path:
        raise SystemExit(f"🔴 Commons の URL の形ではない: {url}。書かずに止めた。")
    return head + "/wiki/" + quote(path, safe=":_-.,/")


def used_material():
    """章ファイルの実配線から、写真（権利ごと）と頁（資料ごと）を数える。"""
    import cuts
    import footage as F
    if F.USE:
        raise SystemExit(f"🔴 動く映像の欄が {len(F.USE)} ある（この回は0の前提）。"
                         "【映像あり】と権利の文を書き直すこと。書かずに止めた。")
    table = json.loads(ASSETS.read_text(encoding="utf-8"))
    pages = json.loads(PAGES.read_text(encoding="utf-8"))
    photos, pgs, bad = [], [], []
    for cid, sp in cuts.SPEC.items():
        p = sp.get("photo")
        if not p:
            continue
        stem = Path(p).stem
        if stem.startswith("pg"):
            pgs.append(stem)
            continue
        r = table.get(stem)
        if r is None:
            bad.append(f"{stem}（assets.json に無い）")
            continue
        if not (r.get("author") or "").strip():
            bad.append(f"{stem}（撮影者が空）")
        if r.get("lic") not in LICENSE_URL and r.get("lic") not in FREE:
            bad.append(f"{stem}（権利が読めない: {r.get('lic')}）")
        photos.append((stem, cid, r))
    if bad:
        raise SystemExit(f"🔴 名乗れない写真がある。書かずに止めた: {bad}")
    if len(photos) != N_PHOTOS or len({s for s, _, _ in photos}) != N_PHOTOS:
        raise SystemExit(f"🔴 写真が {len(photos)} 欄（仕様は {N_PHOTOS}・1点1カット）。書かずに止めた。")
    docs = Counter(pages.get(s, {}).get("doc", "?") for s in pgs)
    if len(pgs) != N_PAGES or dict(docs) != PAGE_DOCS:
        raise SystemExit(f"🔴 頁が {len(pgs)} 枚・{dict(docs)}（仕様は {N_PAGES} 枚・{PAGE_DOCS}）。書かずに止めた。")
    return photos, docs


# 画面の出典表記（`ref/ep13/credits.json`＝`scene_jiko` が焼く文字列）から名前と権利を引く。
#   🔴 概要欄の名前は**画面と同じ**にする（`assets.json` の `author` は Commons の英語の生の値＝
#      「Photo n. C15-10 released by McDonnell Douglas」など・画面の「マクドネル・ダグラス社の広報写真」と食い違う）
#   名前の中に「／」がある（「Volker von Bonin／フィンランド文化遺産庁」）＝名前どうしを「／」で並べない＝1点1行
ONSCREEN = re.compile(r"^出典：(?P<who>.+?)(?:／(?P<lic>CC[^（]*)(?:（.*）)?|（パブリックドメイン）)$")


def onscreen(path: str, lic: str) -> str:
    """画面の出典表記から名前を返す。権利が `assets.json` と食い違えば止める。"""
    table = json.loads(CREDITS_JSON.read_text(encoding="utf-8"))
    s = table.get(path)
    m = ONSCREEN.match(s or "")
    if not m:
        raise SystemExit(f"🔴 画面の出典表記が読めない: {path} → {s!r}。書かずに止めた。")
    shown = (m.group("lic") or "Public domain").strip()
    if shown != lic:
        raise SystemExit(f"🔴 画面の権利「{shown}」と表の権利「{lic}」が食い違う: {path}。書かずに止めた。")
    return m.group("who").strip()


def read_credits() -> str:
    photos, docs = used_material()
    free = OrderedDict()
    by_lic = OrderedDict((k, []) for k in LICENSE_URL)
    for stem, cid, r in sorted(photos, key=lambda x: x[1]):
        lic = r["lic"]
        who = onscreen(f"ep13/{stem}.jpg", lic)
        if lic in FREE:
            free.setdefault(lic, Counter())[who] += 1
            continue
        by_lic[lic].append((who, link(r["url"])))
    n_free = sum(sum(c.values()) for c in free.values())
    n_by = sum(len(v) for k, v in by_lic.items() if "-SA" not in k)
    n_sa = sum(len(v) for k, v in by_lic.items() if "-SA" in k)
    print(f"■ 素材：写真 {len(photos)}点（CC0・PD {n_free}・CC BY {n_by}・CC BY-SA {n_sa}）"
          f"／頁 {sum(docs.values())}枚 {dict(docs)}／動く映像 0")
    out = ["【写真】"]
    for lic, whos in free.items():
        name = "パブリックドメイン" if lic == "Public domain" else lic
        out.append("・" + "・".join(f"{w} {n}点" for w, n in whos.items()) + f"＝{name}")
    for lic, rows in by_lic.items():
        if not rows:
            continue
        out.append(f"・{lic}（許諾 {LICENSE_URL[lic]}）")
        out += [f"　{who}　{url}" for who, url in rows]
    out.append(f"※ CC BY の写真 {n_by}点は、切り出しと色調の変更をしています。"
               "慰霊の名前の壁の写真は、名前にモザイクをかけています。")
    out.append(f"※ CC BY-SA の写真 {n_sa}点は、切らず・色を変えず・何も重ねず、"
               "そのままの形で額に入れて出しています（無改変）。")
    out.append(f"・報告書などの頁 {sum(docs.values())}枚：上の出典の資料より")
    return "\n".join(out)


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
    # 🔴 入れてはいけない語（BGM のクレジット・通説・本文が出さない社名・伏せ字）
    for bad in ("<", ">", "BGM", "DOVA", "OpenTracks", "疑惑の霧", "Keido",
                "ストライキ", "ヒースロー", "335", "表示板", "三井物産", "ﾀﾋ"):
        if bad in desc or bad in TITLE:
            raise SystemExit(f"🔴 入れてはいけない語「{bad}」が入っている。書かずに止めた。")
    if "死亡" in TITLE:
        raise SystemExit("🔴 タイトルに「死亡」が入っている。書かずに止めた。")
    if "【映像あり】" in TITLE:
        raise SystemExit("🔴 動く映像が無い回なのに【映像あり】が付いている。書かずに止めた。")
    print(f"タイトル {len(TITLE)} 字（上限 100 ／ 型の幅 67〜94）")
    print(f"説明     {len(desc)} 字（上限 5,000）")
    if len(TITLE) > 100 or len(desc) > 5000:
        raise SystemExit("🔴 上限を超えた。書かずに止めた。")
    if not (67 <= len(TITLE) <= 94):
        raise SystemExit("🔴 タイトルが型の幅（67〜94字）から外れた。書かずに止めた。")

    # 🔴 サムネはカズヤくんが決めてから入れる（⑥ で候補を焼いて見てもらう）
    thumb = ""
    meta = {
        "slug": "ep13",
        "title": TITLE,
        "description": desc,
        "tags": ["トルコ航空981便", "トルコ航空981便墜落事故", "DC-10", "貨物ドア", "航空事故",
                 "飛行機事故", "1974年", "パリ", "エルムノンヴィル", "マクドネル・ダグラス",
                 "事故検証", "図解", "一次資料", "解説", "ドキュメンタリー"],
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
