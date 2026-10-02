# -*- coding: utf-8 -*-
"""16本目（バイオントダム災害）の `config/meta_ep16.json` を**機械で**組み立てる（2026-10-02・⑥）。

`qa_out/ep15_meta.py` を写して、この回の形に合わせた。

🔴 手で書かない理由（ep7〜ep15 と同じ）
  ① 用語は `ref/ep16/yougo.md` の「## 貼る本文」の節が正本＝**そのまま**貼る（`**` だけ外す）
  ② 素材の点数は**章ファイルの実配線**（`cuts.SPEC` の `photo`）から数え、権利・素材の URL は
     `ref/ep16/assets.json`（⑤b-7 の `qa_out/ep16_assets.py` が作った表）で引き、名前は
     **画面の出典表記**（`ref/ep16/credits.json`）から取る。**画面と表の権利が食い違えば落ちる**
  ③ 目次は `scene_jiko.CUTS` の秒を頭から積む＝**焼いた版と同じ秒**（章の扉の2秒は CUTS に入っている）
  ④ タイトル 100字・説明 5,000字の上限と、入れてはいけない語を、書く前に確かめる

🔴 この回が 15本目と違うところ
  - **動く映像 0本・引用の紙面 0点**（記録映像は使わない＝②③）＝【映像あり】なし・【映像】の節なし
  - 写真 46点（Commons・地形図 #100 を含む）。権利は **PD 39点**（根拠は点ごとに違う＝米連邦 §105・撮影者本人の宣言・
    伊の単純写真・1934年の地形図＝`ref/CREDITS.md`）／**CC BY 5点**（3.0 が3点・4.0・2.5＝画面で「改変：色調変更・切出」）／
    **CC BY-SA 4.0 2点**（Enel・Torno＝額装・無改変）
  - PD は**撮影者ごとの点数を1行**（URL なし＝14本目の形）。URL を付けるのは表示が許諾の条件の CC BY・BY-SA の7点だけ
    （46点に URL を付けると 5,000字を超える＝ルール §6-52）
  - 1968年の法廷（PD）は**顔にモザイク**（画面の表記「パブリックドメイン・顔にモザイク」）＝1行
  - 🔴 **米陸軍の写真**（画面の名前に「U.S. Army」がある PD の点）＝推奨・支持を意味しない断り書き（ルール §5b-98⑧）
  - 頁は 8枚＝すべて議会の調査委員会の最終報告（S1）＝`ref/ep16/pages.json` の `doc`
  - タイトル＝推奨A（④'・09-28 承認）＝末尾【ゆっくり解説】込み 86字。「決壊」「死亡」は使わない（§1-1・§B2-4）

    python qa_out/ep16_meta.py            # 組み立てて config/meta_ep16.json に書く（サムネが決まってから）
    python qa_out/ep16_meta.py --dry      # 書かずに中身と字数だけ出す
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

YOUGO = HERE / "ref" / "ep16" / "yougo.md"
ASSETS = HERE / "ref" / "ep16" / "assets.json"
CREDITS_JSON = HERE / "ref" / "ep16" / "credits.json"
PAGES = HERE / "ref" / "ep16" / "pages.json"
OUT = HERE / "config" / "meta_ep16.json"

N_GLOSS = 23          # `ref/ep16/yougo.md` の「貼る本文」の語数（⑥で本文に当てて確定＝ep16_yougo.py --spec）
N_PHOTOS = 46         # Commons の写真（地形図 #100 を含む・章ファイルの実配線）
N_PD, N_BY, N_SA = 39, 5, 2
N_MOSAIC = 1          # 顔にモザイク（1968年の法廷）
N_PAGES = 8           # 議会の報告書の頁を絵として出す種類
PAGE_DOCS = {"S1": 8}
PAGE_DOC_NAME = {"S1": "イタリア議会 調査委員会『最終報告』（1965年）"}

# ✅ 台本第2版 §1-1 の推奨A（④'・09-28 カズヤくん承認＝呼び名「バイオントダム」＋ B4-8【ゆっくり解説】）。
#    動く映像は使わない＝【映像あり】は付けない。「亡くなった」＝死の語の言い換え（§B2-4）。「決壊」は使わない
TITLE = ("模型の実験は「水位700メートルなら絶対に安全」と結論していた。"
         "その夜の水位は約700メートル、"
         "1,910人が亡くなったバイオントダム災害の真相【事故検証】【ゆっくり解説】")

# ⚠️ 本文（台本第2版 c101〜c117・c908・cb18）で言っていることだけを書く。問いは c108・c110・c920 の言い方
HEAD = """【この動画について】
1963年10月9日、22時39分。イタリア北東部の山あいの谷で、バイオントダムがせき止めた湖へ、南の岸のトック山の斜面が崩れ落ちました。押し出された水はダムの上を越え、谷の出口の先のロンガローネの町へ流れ下りました。亡くなった人は、1,900人を超えます（バイオント財団と歴史家の数で1,910人）。

ダムは壊れていません。山の斜面が1つの塊のまま湖へ滑り込み、押し出された水がダムの上を越えたのです。しかも、斜面がゆっくり動いていることは、事故の3年以上前から、毎日の測量で分かっていました。模型の実験は「水位700メートルなら安全」と結論していて、その夜の水位はおよそ700メートルでした。

この動画は、1965年にイタリア議会の調査委員会がまとめた最終報告書（反対意見の報告2本も入れて248ページ）を、原文のイタリア語で読んで作っています。学術の総説と、バイオント財団の年表の数とも照らしました。時刻は現地の時刻、高さは海面からの高さ（標高）で伝えます。

・前もって見通すこと、予見はできたのか。防げたのか
・議会の報告と3回の判決は、それぞれどう答えたのか
・技術、組織、行政、法律に、足りない所は無かったか
"""

# 台本第2版 §10 の出典一覧から（S1・S2・S8・S9・S10）
PRIMARY = """【出典】
・イタリア議会 バイオント災害調査委員会『最終報告』Doc.76-bis（1965年）と少数派の報告2本（上院の公式サイト）　https://www.senato.it/service/PDF/PDFServer/DF/285307.pdf
・Genevois & Ghirotti「The 1963 Vaiont Landslide」Giornale di Geologia Applicata 1（2005年・学術の総説）　https://doi.org/10.1474/GGA.2005-01.0-05.0005
・バイオント財団の年表（F. Niccolini『Cronologia』）　https://fondazionevajont.org/wp-content/uploads/2024/10/Cronologia_italiano.pdf
・M. Reberschak ほか編『Vajont. La prima sentenza』（Cierre・2023年）の試し読み　https://edizioni.cierrenet.it/wp-content/uploads/2023/09/vajont_sentenza_anteprima.pdf
・破毀院 1971年3月25日の判決（Il Foro Italiano 1971年・要旨）"""

TAIL_BASE = """動画に出てくる数値・日付・証言の言葉は、これらの記録によります。
報告書が言い切っていないところは、画面でそのまま断っています。
※ 画面の再現イラスト・断面・地図は、報告書と資料の記録、1934年の地形図をもとに描いた模式図です。"""

# サムネの断り書き（カズヤくんが選んだ案の地に合わせる）。🔴 選ぶまで THUMB は空＝書かずに止める
_TA = ("※ サムネイルは、1963年に米陸軍が撮った写真（ダムとその奥の崩れた山・パブリックドメイン）を{how}、"
       "色調を整えて文字を重ねたものです。")
_TB = ("※ サムネイルは、1963年に上空から撮られた写真（撮影者不明・パブリックドメイン）を{how}、"
       "色調を整えて文字を重ねたものです。")
THUMB_NOTE = {
    # 🆕 10-02 カズヤくん：地は生成AI（gen_thumb_ai.py vaj_a）＝ルール §6-55⑦ の断り書き（本編に動く映像は無い＝「写真」だけ）
    "AI": ("※ サムネイルの画像は、生成AIで作ったイメージです。実際の写真ではありません。"
           "本編の写真は、すべて実際の記録です。"),
    "A": _TA.format(how="切り出し"),
    "A13": _TA.format(how="拡大して切り出し"),
    "A15": _TA.format(how="拡大して切り出し"),
    "B": _TB.format(how="切り出し"),
    "Bd": _TB.format(how="切り出し"),
    "C": ("※ サムネイルは、1963年にイタリアの消防が撮った写真（がれきの原と鐘楼・パブリックドメイン）を切り出し、"
          "色調を整えて文字を重ねたものです。"),
}
THUMB = ""

# 権利（`assets.json` の `lic`）→ 概要欄の許諾の URL。ここに無い権利が出たら止める
PD = "パブリックドメイン"
LICENSE_URL = OrderedDict([
    ("CC BY 3.0", "https://creativecommons.org/licenses/by/3.0/deed.ja"),
    ("CC BY 4.0", "https://creativecommons.org/licenses/by/4.0/deed.ja"),
    ("CC BY 2.5", "https://creativecommons.org/licenses/by/2.5/deed.ja"),
    ("CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0/deed.ja"),
])


def norm_lic(lic: str) -> str:
    """`assets.json` の生の `lic` → 概要欄の権利の名前。読めなければ止める。"""
    lic = (lic or "").strip()
    if lic == "Public domain":
        return PD
    if lic in LICENSE_URL:
        return lic
    raise SystemExit(f"🔴 権利が読めない: {lic!r}。書かずに止めた。")


# 画面の出典表記（`ref/ep16/credits.json`＝`scene_jiko` が焼く文字列）の形
ONSCREEN = [
    (re.compile(r"^出典：(?P<who>.+?)（パブリックドメイン(?P<mosaic>・顔にモザイク)?）$"), lambda m: PD),
    (re.compile(r"^出典：(?P<who>.+?)／(?P<lic>CC BY-SA [\d.]+)（無改変）$"), lambda m: m.group("lic")),
    (re.compile(r"^出典：(?P<who>.+?)／(?P<lic>CC BY [\d.]+)(?:／改変：.+)?$"), lambda m: m.group("lic")),
]


def onscreen(path: str, lic: str):
    """画面の出典表記から（名前, 顔にモザイクか）を返す。権利が `assets.json` と食い違えば止める。"""
    table = json.loads(CREDITS_JSON.read_text(encoding="utf-8"))
    s = table.get(path) or ""
    for rx, shown_of in ONSCREEN:
        m = rx.match(s)
        if m:
            shown = shown_of(m)
            if shown != lic:
                raise SystemExit(f"🔴 画面の権利「{shown}」と表の権利「{lic}」が食い違う: {path}。書かずに止めた。")
            return m.group("who").strip(), bool(m.groupdict().get("mosaic"))
    raise SystemExit(f"🔴 画面の出典表記が読めない: {path} → {s!r}。書かずに止めた。")


def link(url: str) -> str:
    """🔴 Commons の URL の括弧を %28 %29 にする（YouTube の自動リンクが `)` で切れるのを防ぐ）。
    16本目の CC の7点は題名が全部 ASCII＝ページ番号の URL（14本目の curid）は要らない。非 ASCII が出たら止める。"""
    head, _, path = url.partition("/wiki/")
    if not path:
        raise SystemExit(f"🔴 Commons の URL の形ではない: {url}。書かずに止めた。")
    if not unquote(path).isascii():
        raise SystemExit(f"🔴 題名に非 ASCII がある（curid の URL にすること）: {url}。書かずに止めた。")
    return head + "/wiki/" + quote(unquote(path), safe=":_-.,/")


def read_glossary() -> str:
    """`ref/ep16/yougo.md` の「## 貼る本文」の節を**そのまま**返す（次の `---` か `## ` まで）。"""
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
    """章ファイルの実配線から、写真（点ごとの最初のカット）・頁（資料ごと）・写真を出すカットの数を数える。"""
    import cuts
    import footage as F
    if list(F.USE):
        raise SystemExit(f"🔴 動く映像の欄がある: {list(F.USE)}（16本目は0本）。書かずに止めた。")
    table = json.loads(ASSETS.read_text(encoding="utf-8"))
    pages = json.loads(PAGES.read_text(encoding="utf-8"))
    photos, pgs, bad, slots = OrderedDict(), set(), [], 0
    for cid, sp in cuts.SPEC.items():
        p = sp.get("photo")
        if not p:
            continue
        if "google" in p.lower() or "earth" in p.lower():
            bad.append(f"{cid}（Googleアースの絵が残っている）")
        stem = Path(p).stem
        if stem.startswith("pg"):
            if stem not in pages:
                bad.append(f"{stem}（pages.json に無い）")
            pgs.add(stem)
            continue
        r = table.get(stem)
        if r is None:
            bad.append(f"{stem}（assets.json に無い）")
            continue
        if not (r.get("author") or "").strip():
            bad.append(f"{stem}（撮影者が空）")
        slots += 1
        photos.setdefault(stem, (cid, r))
    if bad:
        raise SystemExit(f"🔴 名乗れない素材がある。書かずに止めた: {bad}")
    if len(photos) != N_PHOTOS:
        raise SystemExit(f"🔴 写真が {len(photos)} 点（仕様は {N_PHOTOS} 点）。書かずに止めた。")
    docs = Counter(pages[s].get("doc", "?") for s in pgs)
    if len(pgs) != N_PAGES or dict(docs) != PAGE_DOCS:
        raise SystemExit(f"🔴 頁が {len(pgs)} 枚・{dict(docs)}（仕様は {N_PAGES} 枚・{PAGE_DOCS}）。書かずに止めた。")
    return photos, docs, slots


def read_credits() -> str:
    photos, docs, slots = used_material()
    pd_who = OrderedDict()                       # 名前 → 点数（PD は URL を付けない）
    by_lic = OrderedDict((k, OrderedDict()) for k in LICENSE_URL)
    mosaic, army = [], []
    for stem, (cid, r) in sorted(photos.items(), key=lambda x: x[1][0]):
        lic = norm_lic(r["lic"])
        who, mos = onscreen(f"ep16/{stem}.jpg", lic)
        if mos:
            mosaic.append(stem)
        if lic == PD:
            pd_who[who] = pd_who.get(who, 0) + 1
            if "U.S. Army" in who:
                army.append(stem)
        else:
            by_lic[lic].setdefault(who, []).append(link(r["url"]))
    n_pd = sum(pd_who.values())
    n_by = sum(len(u) for k in LICENSE_URL if k.startswith("CC BY ") for u in by_lic[k].values())
    n_sa = sum(len(u) for k in LICENSE_URL if k.startswith("CC BY-SA") for u in by_lic[k].values())
    print(f"■ 素材：写真 {len(photos)}点・{slots}カット（PD {n_pd}・CC BY {n_by}・CC BY-SA {n_sa}・顔にモザイク {len(mosaic)}・"
          f"米陸軍 {len(army)} {army}）／頁 {sum(docs.values())}枚 {dict(docs)}")
    if (n_pd, n_by, n_sa, len(mosaic)) != (N_PD, N_BY, N_SA, N_MOSAIC) or not army:
        raise SystemExit(f"🔴 権利ごとの点数が⑥で数えた値（PD {N_PD}・CC BY {N_BY}・BY-SA {N_SA}・モザイク {N_MOSAIC}・"
                         "米陸軍1点以上）と違う。断り書きの文を当て直すこと。書かずに止めた。")
    out = ["【写真】"]
    out.append("・" + "・".join(f"{w} {n}点" for w, n in pd_who.items()) + f"＝{PD}")
    for lic, whos in by_lic.items():
        if not whos:
            continue
        out.append(f"・{lic}（許諾 {LICENSE_URL[lic]}）")
        for who, urls in whos.items():
            out += [f"　{who}　{u}" for u in urls]
    out.append(f"※ CC BY の写真（{n_by}点）は、切り出しと色調の変更をしています。")
    out.append(f"※ CC BY-SA の写真 {n_sa}点は、切らず・色を変えず・何も重ねず、そのままの形で額に入れて出しています（無改変）。")
    out.append("※ 1968年の法廷の写真（パブリックドメイン）は、写っている人の顔にモザイクをかけています。")
    out.append("※ 米陸軍の写真を使っていますが、米陸軍・米国防総省がこの動画を推奨・支持していることを"
               "意味するものではありません（The appearance of U.S. Department of Defense (DoD) visual information "
               "does not imply or constitute DoD endorsement.）")
    out.append("【報告書の頁】")
    out.append("・" + "・".join(f"{PAGE_DOC_NAME[d]} {docs[d]}枚" for d in PAGE_DOCS) + "（上の出典の資料より）")
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
    # 🔴 入れてはいけない語（BGM のクレジット・伏せ字・ゆっくりの一文＝14本目だけ・煽り語）
    for bad in ("<", ">", "BGM", "DOVA", "OpenTracks", "疑惑の霧", "Keido", "ﾀﾋ", "ゆっくりボイス",
                "AquesTalk", "即死", "絶命", "地獄"):
        if bad in desc or bad in TITLE:
            raise SystemExit(f"🔴 入れてはいけない語「{bad}」が入っている。書かずに止めた。")
    for bad in ("死亡", "決壊"):
        if bad in TITLE:
            raise SystemExit(f"🔴 タイトルに「{bad}」が入っている。書かずに止めた。")
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
        "slug": "ep16",
        "title": TITLE,
        "description": desc,
        "tags": ["バイオントダム", "バイオント", "ヴァイオント・ダム", "Vajont", "Vaiont", "ダム災害", "地すべり",
                 "トック山", "ロンガローネ", "イタリア", "1963年", "事故検証", "図解", "一次資料", "解説", "ゆっくり解説"],
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
