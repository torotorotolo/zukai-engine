# -*- coding: utf-8 -*-
"""15本目（リノ・エアレース2011）の `config/meta_ep15.json` を**機械で**組み立てる（2026-09-30・⑥）。

`qa_out/ep14_meta.py` を写して、この回の形に合わせた。

🔴 手で書かない理由（ep7〜ep14 と同じ）
  ① 用語は `ref/ep15/yougo.md` の「## 貼る本文」の節が正本＝**そのまま**貼る（`**` だけ外す）
  ② 素材の点数は**章ファイルの実配線**（`cuts.SPEC` の `photo`）から数え、権利・撮影者・素材の URL は
     `ref/ep15/assets.json`（⑤b-6 の `qa_out/ep15_assets.py` が作った表）で引き、名前は
     **画面の出典表記**（`ref/ep15/credits.json`）から取る。**画面と表の権利が食い違えば落ちる**
  ③ 目次は `scene_jiko.CUTS` の秒を頭から積む＝**焼いた版と同じ秒**（章の扉の2秒は CUTS に入っている）
  ④ タイトル 100字・説明 5,000字の上限と、入れてはいけない語を、書く前に確かめる

🔴 この回が 14本目と違うところ
  - **動く映像 0本**（事故の動く映像は使わない＝09-25 カズヤくん）＝【映像あり】なし・【映像】の節なし
  - 写真の権利が**4つ**：CC BY-SA 2.0（16点＝額装・無改変）／CC BY 2.0（2点＝2010年の事故機・顔にモザイク）／
    CC BY 4.0（1点＝2016年の講習会）／**引用 8点**（NTSB 報告書の紙面に載った courtesy の写真＝図5〜10・15・17・
    頁の図・説明・撮影者の行ごと・額装・無改変＝ルール §2-6c・09-25 カズヤくん）
  - CC BY の3点は画面で「改変：…」を足している（`scene_jiko.credit_of`＝色調変更・切出／2010年の2点は顔にモザイク）
  - 頁は 28枚（NTSB 事故報告 17・資料 #33 3・#40 5・#14 1・#53 1・勧告書 1）＝`ref/ep15/pages.json` の `doc`
  - NTSB の図2点（#14 図12・#33 図7）は下地が Google Earth＝頁ごとの引用（`ref/CREDITS.md`）＝その旨を1行
  - ゆっくりの一文（「※今回からゆっくりボイスを…」）は**14本目だけ**＝入れない（ルール §6-53）
  - タイトル＝推奨A（④'・09-26 承認）80字＋【ゆっくり解説】（B4-8）＝88字

    python qa_out/ep15_meta.py            # 組み立てて config/meta_ep15.json に書く（サムネが決まってから）
    python qa_out/ep15_meta.py --dry      # 書かずに中身と字数だけ出す
"""
import json
import re
import sys
from collections import Counter, OrderedDict
from pathlib import Path
from urllib.parse import quote, unquote

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
import scene_jiko as S            # noqa: E402

YOUGO = HERE / "ref" / "ep15" / "yougo.md"
ASSETS = HERE / "ref" / "ep15" / "assets.json"
CREDITS_JSON = HERE / "ref" / "ep15" / "credits.json"
PAGES = HERE / "ref" / "ep15" / "pages.json"
OUT = HERE / "config" / "meta_ep15.json"

N_GLOSS = 21          # `ref/ep15/yougo.md` の「貼る本文」の語数（⑥で本文に当てて確定）
N_PHOTOS = 19         # Commons の写真（章ファイルの実配線）
N_PHOTO_SLOTS = 19    # 写真を出すカットの数（1点1カット）
N_QUOTE = 8           # 報告書の紙面に載った courtesy の写真（引用）
N_PAGES = 28          # 報告書などの頁を絵として出す種類（courtesy の紙面8は除く）
PAGE_DOCS = {"AAB": 17, "#14": 1, "#33": 3, "#40": 5, "#53": 1, "勧告書": 1}
PAGE_DOC_NAME = {"AAB": "NTSB 事故報告 AAB-12/01", "#33": "資料 #33（生存と運営）",
                 "#40": "資料 #40（材料の試験）", "#14": "資料 #14（データの記録）",
                 "#53": "資料 #53（性能の解析）", "勧告書": "安全勧告 A-12-08"}

# ✅ 台本第2版 §1-1 の推奨A（④'・09-26 カズヤくん承認）＋ B4-8【ゆっくり解説】（09-28 カズヤくん・全回）。
#    動く映像は使わない＝【映像あり】は付けない（②③・09-25）。「亡くなった」＝死の語の言い換え（§B2-4）
TITLE = ("4日前の検査で「ねじが短すぎる」と指摘されていた。"
         "ナットは少なくとも26年前から付いていたとみられ、"
         "11人が亡くなったリノ・エアレース墜落事故の真相【事故検証】【ゆっくり解説】")

# ⚠️ 本文（台本第2版 c101〜c112）で言っていることだけを書く。問いは c109 の3つをそのまま。
HEAD = """【この動画について】
2011年9月16日、アメリカ・ネバダ州リノのエアレース。改造した古い戦闘機（P-51D「ザ・ギャロッピング・ゴースト」・レースの番号177）が、観客のボックス席が並ぶ駐機場に落ちました。崩れ始めてから落ちるまで約9秒。パイロットと、地上の10人が亡くなりました。けがをした人は、少なくとも64人です。

当時は「尾翼の小さな板が外れて、機首が上がったのでは」と報じられました。でも報告書では、機首が上がり、体にかかる力Gが最大になったのが先。板の一片が離れたのは、その約3秒後でした。その板を留めていたナットは、塗装の跡から、26年以上前から付いていたとみられます。

この動画は、アメリカの国家運輸安全委員会（NTSB）の事故報告書と、調べた資料の束を、原文で読んで作っています。時刻は現地の時刻（日本より16時間遅い）で、長さや速さはメートル法に直して伝えます。

・9秒のあいだに、機体に何が起きたのか
・なぜ、板は震えたのか
・観客席との距離は、足りていたか
"""

# 台本第2版 §10 の出典一覧から
PRIMARY = """【出典】
・NTSB 事故報告 Aircraft Accident Brief NTSB/AAB-12/01「Pilot/Race 177, The Galloping Ghost, North American P-51D, N79111, Reno, Nevada, September 16, 2011」（2012年8月27日）　https://www.ntsb.gov/investigations/AccidentReports/Reports/AAB1201.pdf
・NTSB 公開ドケット WPR11MA454（#14 データの記録・#17 耐空性・#33 生存と運営・#40 材料の試験・#53 性能の解析）
・NTSB 安全勧告 A-12-08〜17（2012年4月10日）と、その後の記録（CAROL）
・Reno Air Racing Association の発表（2024年5月23日・2026年9月24日）
・当時の報道（Christian Science Monitor 2011年9月18日・CBS News 2011年9月19日・NPR 2011年9月19日）"""

TAIL_BASE = """動画に出てくる数値・時刻・証言の言葉は、これらの記録によります。
報告書が言い切っていないところは、画面でそのまま断っています。
※ 画面の「再現イラスト」と地図は、報告書と資料の記録をもとに描いた模式図です。"""

# サムネの断り書き（カズヤくんが選んだ案の地に合わせる）。🔴 選ぶまで THUMB は空＝書かずに止める
_T3 = ("※ サムネイルは、事故の前の年（2010年9月18日）にリノで撮られた事故機の写真（jeggernot・CC BY 2.0）"
       "を{how}、色調を整えて文字を重ねたものです。写り込んだ人の顔にはモザイクをかけています。")
THUMB_NOTE = {
    "pit": _T3.format(how="切り出し"),
    "pitz": _T3.format(how="拡大して切り出し"),
}
# ✅ 2026-09-30 カズヤくん決定＝案 c「犠牲11人 改造機が観客席へ」＋実際の写真（T3・2010年の事故機・全幅）。
#    Actions 36712879523（版 83a7d6d）の ep15_c_kaizou_pit.png を同じ中身のまま写した（md5 0866c3d4fa9b78718b6f3f3a8893c122）。
#    ⚠️ 生成の地（案A・`ref/ep15/ai/`・約$0.2）は見比べたうえで**使わない**＝断り書きは写真の方（THUMB_NOTE["pit"]）
THUMB = "out/thumb/ep15-t1/ep15_c_kaizou_pit.png"

# 権利（`assets.json` の `lic`）→ 概要欄の許諾の URL。ここに無い権利が出たら止める
LICENSE_URL = OrderedDict([
    ("CC BY-SA 2.0", "https://creativecommons.org/licenses/by-sa/2.0/deed.ja"),
    ("CC BY 2.0", "https://creativecommons.org/licenses/by/2.0/deed.ja"),
    ("CC BY 4.0", "https://creativecommons.org/licenses/by/4.0/deed.ja"),
])
QUOTE = "引用"


def norm_lic(lic: str) -> str:
    """`assets.json` の生の `lic` → 概要欄の権利の名前。読めなければ止める。"""
    lic = (lic or "").strip()
    if lic.startswith("引用"):
        return QUOTE
    if lic in LICENSE_URL:
        return lic
    raise SystemExit(f"🔴 権利が読めない: {lic!r}。書かずに止めた。")


# 画面の出典表記（`ref/ep15/credits.json`＝`scene_jiko` が焼く文字列）の形
ONSCREEN = [
    (re.compile(r"^出典：(?P<who>.+?)／(?P<lic>CC BY-SA [\d.]+)（無改変）$"), lambda m: m.group("lic")),
    (re.compile(r"^出典：(?P<who>.+?)／(?P<lic>CC BY [\d.]+)(?:／改変：.+)?$"), lambda m: m.group("lic")),
    (re.compile(r"^出典：NTSB 事故報告 AAB-12/01 PDF \d+頁・図\d+（写真：(?P<who>.+?)・引用・無改変）$"),
     lambda m: QUOTE),
]


def onscreen(path: str, lic: str) -> str:
    """画面の出典表記から名前を返す。権利が `assets.json` と食い違えば止める。"""
    table = json.loads(CREDITS_JSON.read_text(encoding="utf-8"))
    s = table.get(path) or ""
    for rx, shown_of in ONSCREEN:
        m = rx.match(s)
        if m:
            shown = shown_of(m)
            if shown != lic:
                raise SystemExit(f"🔴 画面の権利「{shown}」と表の権利「{lic}」が食い違う: {path}。書かずに止めた。")
            return m.group("who").strip()
    raise SystemExit(f"🔴 画面の出典表記が読めない: {path} → {s!r}。書かずに止めた。")


def link(url: str) -> str:
    """🔴 Commons の URL の括弧を %28 %29 にする（YouTube の自動リンクが `)` で切れるのを防ぐ）。
    15本目は題名が全部 ASCII＝ページ番号の URL（14本目の curid）は要らない。非 ASCII が出たら止める。"""
    head, _, path = url.partition("/wiki/")
    if not path:
        raise SystemExit(f"🔴 Commons の URL の形ではない: {url}。書かずに止めた。")
    if not unquote(path).isascii():
        raise SystemExit(f"🔴 題名に非 ASCII がある（curid の URL にすること）: {url}。書かずに止めた。")
    return head + "/wiki/" + quote(unquote(path), safe=":_-.,/")     # 「'」も %27（Leeward's の題）


def read_glossary() -> str:
    """`ref/ep15/yougo.md` の「## 貼る本文」の節を**そのまま**返す（次の `---` か `## ` まで）。"""
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
    body = body.replace("**", "")          # 🔴 YouTube の概要欄は Markdown を解釈しない
    if "*" in body or "_" in body:
        raise SystemExit("🔴 外し切れない記号が残っている。書かずに止めた。")
    return body


def used_material():
    """章ファイルの実配線から、写真（権利ごと）・引用の紙面・頁（資料ごと）を数える。"""
    import cuts
    import footage as F
    if list(F.USE):
        raise SystemExit(f"🔴 動く映像の欄がある: {list(F.USE)}（15本目は0本）。書かずに止めた。")
    table = json.loads(ASSETS.read_text(encoding="utf-8"))
    pages = json.loads(PAGES.read_text(encoding="utf-8"))
    photos, quotes, pgs, bad, slots = OrderedDict(), OrderedDict(), set(), [], 0
    for cid, sp in cuts.SPEC.items():
        p = sp.get("photo")
        if not p:
            continue
        if "google" in p.lower() or "earth" in p.lower():
            bad.append(f"{cid}（Googleアースの絵が残っている）")
        stem = Path(p).stem
        r = table.get(stem)
        if r is not None and r.get("src") == "aab":       # courtesy の紙面（引用）
            quotes.setdefault(stem, (cid, r))
            continue
        if stem.startswith("pg"):
            if stem not in pages:
                bad.append(f"{stem}（pages.json に無い）")
            pgs.add(stem)
            continue
        if r is None:
            bad.append(f"{stem}（assets.json に無い）")
            continue
        if not (r.get("author") or "").strip():
            bad.append(f"{stem}（撮影者が空）")
        slots += 1
        photos.setdefault(stem, (cid, r))
    if bad:
        raise SystemExit(f"🔴 名乗れない素材がある。書かずに止めた: {bad}")
    if len(photos) != N_PHOTOS or slots != N_PHOTO_SLOTS:
        raise SystemExit(f"🔴 写真が {len(photos)} 点・{slots} カット（仕様は {N_PHOTOS} 点・{N_PHOTO_SLOTS} カット）。書かずに止めた。")
    if len(quotes) != N_QUOTE:
        raise SystemExit(f"🔴 引用の紙面が {len(quotes)} 点（仕様は {N_QUOTE}）。書かずに止めた。")
    docs = Counter(pages[s].get("doc", "?") for s in pgs)
    if len(pgs) != N_PAGES or dict(docs) != PAGE_DOCS:
        raise SystemExit(f"🔴 頁が {len(pgs)} 枚・{dict(docs)}（仕様は {N_PAGES} 枚・{PAGE_DOCS}）。書かずに止めた。")
    return photos, quotes, docs


def read_credits() -> str:
    photos, quotes, docs = used_material()
    by_lic = OrderedDict((k, OrderedDict()) for k in LICENSE_URL)
    for stem, (cid, r) in sorted(photos.items(), key=lambda x: x[1][0]):
        lic = norm_lic(r["lic"])
        if lic == QUOTE:
            raise SystemExit(f"🔴 Commons の写真に引用の権利: {stem}。書かずに止めた。")
        who = onscreen(f"ep15/{stem}.jpg", lic)
        by_lic[lic].setdefault(who, []).append(link(r["url"]))
    qwho = OrderedDict()
    for stem, (cid, r) in sorted(quotes.items(), key=lambda x: (x[1][1]["page"], x[1][1]["fig"])):
        who = onscreen(f"ep15/{stem}.jpg", norm_lic(r["lic"]))
        qwho.setdefault(who, []).append(r["fig"])
    n_sa = sum(len(u) for w in by_lic["CC BY-SA 2.0"].values() for u in [w])
    n_by = sum(len(u) for k in ("CC BY 2.0", "CC BY 4.0") for u in by_lic[k].values())
    n_q = sum(len(v) for v in qwho.values())
    print(f"■ 素材：写真 {len(photos)}点（CC BY-SA {n_sa}・CC BY {n_by}）／引用の紙面 {n_q}点／"
          f"頁 {sum(docs.values())}枚 {dict(docs)}")
    if n_sa != 16 or n_by != 3 or n_q != 8:
        raise SystemExit("🔴 権利ごとの点数が⑥で数えた値（BY-SA 16・CC BY 3・引用 8）と違う。"
                         "断り書きの文を当て直すこと。書かずに止めた。")
    out = ["【写真】"]
    for lic, whos in by_lic.items():
        if not whos:
            continue
        out.append(f"・{lic}（許諾 {LICENSE_URL[lic]}）")
        for who, urls in whos.items():
            out += [f"　{who}　{u}" for u in urls]
    out.append("・NTSB 事故報告の紙面に載った写真（引用）："
               + "・".join(f"{w}（図{'・'.join(str(f) for f in figs)}）" for w, figs in qwho.items())
               + "。事故の検証のための引用として、頁の図・説明・撮影者の行ごと、切らず・色を変えず・何も重ねず、額に入れて出しています")
    out.append(f"※ CC BY の写真（{n_by}点）は、切り出しと色調の変更をしています。2010年の2点は、写り込んだ人の顔にモザイクをかけています。")
    out.append(f"※ CC BY-SA の写真 {n_sa}点は、切らず・色を変えず・何も重ねず、そのままの形で額に入れて出しています（無改変）。")
    out.append("【報告書などの頁】")
    # 並びは PAGE_DOCS の順（docs は集合から数えた Counter＝回すたびに順が変わる）
    out.append("・" + "・".join(f"{PAGE_DOC_NAME[d]} {docs[d]}枚" for d in PAGE_DOCS) + "（上の出典の資料より）")
    out.append("※ 資料 #14 の図12と #33 の図7は、下地が Google Earth の画像です（NTSB の図のまま、頁ごとに出しています）。")
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
    kind = next((k for k in THUMB_NOTE if THUMB.endswith(f"_{k}.png")), "")
    tail = TAIL_BASE + ("\n" + THUMB_NOTE[kind] if kind else "")
    desc = "\n".join([HEAD, chapters(), "", read_glossary(), "",
                      PRIMARY, "", read_credits(), "", tail])
    # 🔴 入れてはいけない語（BGM のクレジット・伏せ字・ゆっくりの一文＝14本目だけ）
    for bad in ("<", ">", "BGM", "DOVA", "OpenTracks", "疑惑の霧", "Keido", "ﾀﾋ", "ゆっくりボイス",
                "AquesTalk", "即死", "絶命", "避けた"):
        if bad in desc or bad in TITLE:
            raise SystemExit(f"🔴 入れてはいけない語「{bad}」が入っている。書かずに止めた。")
    if "死亡" in TITLE:
        raise SystemExit("🔴 タイトルに「死亡」が入っている。書かずに止めた。")
    if "【映像あり】" in TITLE:
        raise SystemExit("🔴 【映像あり】が付いている（この回は動く映像を使わない）。書かずに止めた。")
    if not TITLE.endswith("【事故検証】【ゆっくり解説】"):
        raise SystemExit("🔴 タイトルの末尾が「【事故検証】【ゆっくり解説】」でない（B4-8）。書かずに止めた。")
    print(f"タイトル {len(TITLE)} 字（上限 100 ／ 型の幅 67〜94＋【ゆっくり解説】8）")
    print(f"説明     {len(desc)} 字（上限 5,000）")
    if len(TITLE) > 100 or len(desc) > 5000:
        raise SystemExit("🔴 上限を超えた。書かずに止めた。")
    if not (67 + 8 <= len(TITLE) <= 100):
        raise SystemExit("🔴 タイトルが型の幅から外れた。書かずに止めた。")

    meta = {
        "slug": "ep15",
        "title": TITLE,
        "description": desc,
        "tags": ["リノ・エアレース", "リノ", "エアレース", "墜落事故", "航空事故", "P-51", "P-51D",
                 "ギャロッピング・ゴースト", "Galloping Ghost", "NTSB", "2011年", "アメリカ",
                 "事故検証", "図解", "一次資料", "解説", "ゆっくり解説"],
        "thumbnail": THUMB,
        "genre": "jiko",
        "playlist": "",
    }
    if "--dry" in sys.argv:
        print("\n" + TITLE + "\n\n" + desc)
        return 0
    if not THUMB or not kind or not (HERE / THUMB).exists():
        raise SystemExit(f"🔴 サムネが決まっていない／無い: {THUMB!r}。決めて焼いてから書くこと。")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✓ 書いた → {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
