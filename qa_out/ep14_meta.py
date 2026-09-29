# -*- coding: utf-8 -*-
"""14本目（セウォル号）の `config/meta_ep14.json` を**機械で**組み立てる（2026-09-29・⑥）。

`qa_out/ep13_meta.py` を写して、この回の形に合わせた。

🔴 手で書かない理由（ep7〜ep13 と同じ）
  ① 用語は `ref/ep14/yougo.md` の「## 貼る本文」の節が正本＝**そのまま**貼る（`**` だけ外す）
  ② 素材の点数は**章ファイルの実配線**（`cuts.SPEC` の `photo`・`footage.USE`）から数え、権利・撮影者・
     素材の URL は `ref/ep14/assets.json`（⑤b-7a の `qa_out/ep14_assets.py` が作った表）で引き、名前は
     **画面の出典表記**（`ref/ep14/credits.json`）から取る。**画面と表の権利が食い違えば落ちる**
  ③ 目次は `scene_jiko.CUTS` の秒を頭から積む＝**焼いた版と同じ秒**（章の扉の2秒は CUTS に入っている）
  ④ タイトル 100字・説明 5,000字の上限と、入れてはいけない語を、書く前に確かめる

🔴 この回が 13本目と違うところ
  - **動く映像 2本**（`footage.USE`＝ca01・ca11＝米海軍・米海兵隊の DVIDS）。ただし事故の翌日以降の捜索の画
    ＝**【映像あり】は付けない**（②③ 引き継ぎ「これだけで【映像あり】は名乗らない＝題が動画より強くなる」・§B4-5）
  - 🔴 米国防総省（米海軍・米海兵隊）の写真と映像＝「推奨・支持を意味しない」断り書き（ルール §5b-98 ⑧）
  - 写真の権利が**8つ**：PD／CC0／CC BY 3.0／帰属表示（Commons の Attribution）／CC BY-SA 2.0・3.0・4.0
    （BY-SA 14点＝額装・無改変）／**引用 1点**（当日の沈む船＝韓国 海洋警察の撮影・額装・無改変）
  - 同じ写真を2カット以上で使う（仁川港の船＝c202・c306・c501）＝点数は**写真の数**で数える
  - CC BY と帰属表示の写真は、私人の顔を外す切り出し（`ss.TRIM`）と章の色（白黒）＝その旨を書く
  - 頁は 15枚（海審 8・判決 5・裁決 2）＝`ref/ep14/pages.json` の `doc`
  - 🔴 使わないもの（`ref/ep14/kousei.md` §5-1）＝下着姿・孟骨水道・日本で18年・ありあけ・潜水艦・
    大統領の7時間・監査院・1,077トン は入れない
  - タイトル＝B4-8 の【ゆっくり解説】を末尾に（+8字）＝推奨A 94字の「待つようにと」を「待つよう」にして 100字

    python qa_out/ep14_meta.py            # 組み立てて config/meta_ep14.json に書く（サムネが決まってから）
    python qa_out/ep14_meta.py --dry      # 書かずに中身と字数だけ出す
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

YOUGO = HERE / "ref" / "ep14" / "yougo.md"
ASSETS = HERE / "ref" / "ep14" / "assets.json"
CREDITS_JSON = HERE / "ref" / "ep14" / "credits.json"
PAGES = HERE / "ref" / "ep14" / "pages.json"
OUT = HERE / "config" / "meta_ep14.json"

N_GLOSS = 16          # `ref/ep14/yougo.md` の「貼る本文」の語数（⑥で本文に当てて確定）
N_PHOTOS = 22         # 章ファイルが出している写真の数（⑥で実配線から数えた・仁川港の船は3カット）
N_PHOTO_SLOTS = 24    # 写真を出すカットの数
N_FOOTAGE = 2         # 動く映像の欄（ca01・ca11）
N_PAGES = 15          # 報告書などの頁を絵として出す欄
PAGE_DOCS = {"海審": 8, "判決": 5, "裁決": 2}
PAGE_DOC_NAME = {"海審": "海洋安全審判院の特別調査報告書", "判決": "大法院の判決（2015年）",
                 "裁決": "中央海洋安全審判院の裁決（2026年）"}

# ✅ 台本第2版 §1-1 の推奨A（④'・09-25 カズヤくん承認）＋ B4-8【ゆっくり解説】（09-28 カズヤくん・全回）。
#    推奨A 94字＋8＝102字＞上限100 → 「待つようにと告げた」を「待つよう告げた」に（意味は同じ・2字減）＝100字。
#    動く映像は捜索の画だけ＝【映像あり】は付けない（②③・§B4-5）。「犠牲になった」＝行方不明を含む（§1-1）
TITLE = ("9時50分、最後の放送も船内で待つよう告げた。"
         "船長たちはその数分前、船員だと名乗らずに警備艇へ移っていた。"
         "高校生250人を含む304人が犠牲になったセウォル号沈没事故の真相【事故検証】【ゆっくり解説】")

# 🔴 2026-09-25 カズヤくん決定（競合分析のチャット）＝**ゆっくりの声で最初に公開する回だけ**、概要欄の最初に
#    この一文を置く。**文言はカズヤくん指定＝このまま**（記憶 project-jiko-yukkuri-voice-trial）。14本目がその回。
#    ⚠️ AquesTalk のライセンスIDは任意の表示＝書かない（§6-23・feedback-no-optional-credits）
#    🔴 2026-09-29（⑥）カズヤくんが文言を変更＝「※今回からゆっくりボイスを試験的に導入してみました。」
#    （この動画だけに当てる＝15本目以降の概要欄には入れない）
FIRST_YUKKURI = "※今回からゆっくりボイスを試験的に導入してみました。"

# ⚠️ 本文（台本第2版 c101〜c110）で言っていることだけを書く。問いは c108 の2つをそのまま。
HEAD = FIRST_YUKKURI + """

【この動画について】
2014年4月16日の朝。韓国の南西の海で、旅客船セウォル号が傾きました。乗っていた476人のうち、助かったのは172人。乗客443人のうち325人は、修学旅行中の高校生でした。生徒のうち246人が亡くなり、4人が行方不明になっています。

傾いてから、およそ1時間。9時50分の最後の放送も、船内で待つように告げていました。船長たちはその数分前、助けに来た海洋警察の船に乗り移っていました。乗客に、船から逃げるよう伝えないまま。韓国の最高裁判所の判決は、退船の命令が一度も出なかったと認めています。

傾いたきっかけは、12年たった今も決まっていません。でも、なぜ助からなかったかには、裁判の答えがあります。

この動画は、韓国の最高裁判所（大法院）の判決と、事故を調べる国の機関・海洋安全審判院の報告書を、原文で読んで作っています。2022年の特別調査委員会の報告書と、2026年の中央海洋安全審判院の裁決も確かめました。同じ出来事の時刻が資料によって数分ずれる所は、どちらの値かを言いながら進めます。

・なぜ、船は傾いたのか
・なぜ、これほど多くの人が助からなかったのか
"""

# 台本第2版 §10 の出典一覧から。題名は原語（ハングル）に日本語を添える（§6-25）
PRIMARY = """【出典】
・韓国 大法院（最高裁判所）2015도6809 判決（2015年11月12日・船員15人）
・韓国 海洋安全審判院 特別調査部『여객선 세월호 전복사고 특별조사 보고서』（旅客船セウォル号転覆事故 特別調査報告書・2014年12月／2018年の正誤表を反映した版）
・韓国 中央海洋安全審判院 裁決 중앙해심 제2026-001호「여객선 세월호 전복사건」（2026年1月28日）
・韓国 社会的惨事特別調査委員会『4·16세월호참사 종합보고서』ほか（2022年9月）
・123艇の艇長の判決：光州高等法院 2015노177（2015年7月）・大法院 2015도11610（2015年11月）
・海洋警察の幹部の判決：ソウル高等法院 2021노453（2023年2月）・大法院 2023도2364（2023年11月）
・清海鎮海運の判決：大法院 2015도7703（2015年10月）／船員の2審：光州高等法院 2014노490（2015年4月）
※ 判決は、大法院 2015도6809 のほかは判例サイト（casenote）に載った本文で読みました。"""

TAIL_BASE = """動画に出てくる数値・時刻・証言の言葉は、これらの記録によります。
資料によって時刻や数が違うところ、報告書や判決が言い切っていないところは、画面でそのまま断っています。
※ 画面の「再現イラスト」は、判決と報告書の記録をもとに描いたものです。"""

# サムネの断り書き（カズヤくんが選んだ案の地に合わせる）。🔴 選ぶまで THUMB は空＝書かずに止める
THUMB_NOTE = {
    "jackets": "※ サムネイルは、2017年1月にソウルの集会で並べられた救命胴衣の写真（Mathew Schwartz・CC BY 3.0）"
               "を切り出し、文字を重ねたものです。",
    "ship": "※ サムネイルは、沈む20日前のセウォル号の写真（2014年3月27日・仁川港／jinjoo2713・パブリックドメイン）"
            "に、文字を重ねたものです。",
    # ✅ 2026-09-29 カズヤくん「サムネOK・断り書きもOK」＝生成の地（案A）＋文言 a
    "meirei": "※ サムネイルの画像は、生成AIで作ったイメージです。実際の写真ではありません。"
              "本編の写真と映像は、すべて実際の記録です。",
}
# ✅ 2026-09-29 カズヤくん決定＝out/thumb/ep14-ai1/ep14ai_a_meirei.png（Actions 36560552438）
# 🆕 2026-09-30（公開のあと）カズヤくん「船をもっと大きく。上下の字の間いっぱいに」→ 見本2案 → 「案2に変更」
#    ＝案2（1.32倍・船の全体が収まる・thumb_jiko.EP14AI_ZOOM["z2"]＝out/thumb/ep14ai_a_meirei_z2.png を同じ中身のまま写した）。
#    ⚠️ ファイル名は `_meirei.png` で終える＝THUMB_NOTE の断り書き（生成AIのイメージ）が付く条件（`_z2.png` だと止まる）
THUMB = "out/thumb/ep14-ai2/ep14ai_a_meirei.png"

# 権利（`assets.json` の `lic` を正規化した値）→ 概要欄の許諾の URL。ここに無い権利が出たら止める
LICENSE_URL = OrderedDict([
    ("CC BY 3.0", "https://creativecommons.org/licenses/by/3.0/deed.ja"),
    ("帰属表示", "https://commons.wikimedia.org/wiki/Template:Attribution"),
    ("CC BY-SA 2.0", "https://creativecommons.org/licenses/by-sa/2.0/deed.ja"),
    ("CC BY-SA 3.0", "https://creativecommons.org/licenses/by-sa/3.0/deed.ja"),
    ("CC BY-SA 4.0", "https://creativecommons.org/licenses/by-sa/4.0/deed.ja"),
])
FREE = ("パブリックドメイン", "CC0")
QUOTE = "引用"


def norm_lic(lic: str) -> str:
    """`assets.json` の生の `lic` → 概要欄の権利の名前。読めなければ止める。"""
    lic = (lic or "").strip()
    if lic.startswith("Public domain"):
        return "パブリックドメイン"
    if lic.startswith("引用"):
        return QUOTE
    if lic == "Attribution":
        return "帰属表示"
    if lic == "CC0" or lic in LICENSE_URL:
        return lic
    raise SystemExit(f"🔴 権利が読めない: {lic!r}。書かずに止めた。")


# 画面の出典表記（`ref/ep14/credits.json`＝`scene_jiko` が焼く文字列）の4つの形
ONSCREEN = [
    (re.compile(r"^出典：(?P<who>.+?)（パブリックドメイン）$"), lambda m: "パブリックドメイン"),
    (re.compile(r"^出典：(?P<who>.+?)／(?P<lic>CC0|CC BY(?:-SA)? [\d.]+)(?:（無改変）)?$"),
     lambda m: m.group("lic")),
    (re.compile(r"^出典：(?P<who>.+?)（Wikimedia Commons・帰属表示）／改変：.+$"), lambda m: "帰属表示"),
    (re.compile(r"^出典：(?P<who>.+?)（引用・無改変）$"), lambda m: QUOTE),
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


PAGEIDS = HERE / "qa_out" / "ep14_commons_pageids.json"   # ⑥で Commons の API から引いた（22点）


def link(url: str) -> str:
    """🔴 Commons の URL の括弧・非 ASCII を %xx にする（YouTube の自動リンクが `)` で切れるのを防ぐ）。

    🆕 14本目：題名にハングルがある写真（韓国国防部の11点）は %xx にすると1本 約140字＝説明が 5,235字で
    上限 5,000 を超えた → **ページ番号の URL**（`/?curid=<番号>`＝約45字・同じファイルの頁が開く）にする。
    """
    head, _, path = url.partition("/wiki/")
    if not path:
        raise SystemExit(f"🔴 Commons の URL の形ではない: {url}。書かずに止めた。")
    title = unquote(path).replace("_", " ")
    if not title.isascii():
        ids = json.loads(PAGEIDS.read_text(encoding="utf-8"))
        pid = ids.get(title)
        if not pid:
            raise SystemExit(f"🔴 Commons のページ番号が無い: {title}。書かずに止めた。")
        return f"https://commons.wikimedia.org/?curid={pid}"
    return head + "/wiki/" + quote(path, safe=":_-.,/")


def read_glossary() -> str:
    """`ref/ep14/yougo.md` の「## 貼る本文」の節を**そのまま**返す（次の `---` か `## ` まで）。"""
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
    """章ファイルの実配線から、写真（権利ごと）・動く映像・頁（資料ごと）を数える。"""
    import cuts
    import footage as F
    use = list(F.USE)
    if len(use) != N_FOOTAGE:
        raise SystemExit(f"🔴 動く映像の欄が {len(use)}（仕様は {N_FOOTAGE}）。書かずに止めた。")
    table = json.loads(ASSETS.read_text(encoding="utf-8"))
    pages = json.loads(PAGES.read_text(encoding="utf-8"))
    photos, pgs, bad, slots = OrderedDict(), [], [], 0
    for cid, sp in cuts.SPEC.items():
        p = sp.get("photo")
        if not p or cid in use:          # 動く映像の欄の `photo` は取れなかったときの控えの静止画
            continue
        if "google" in p.lower() or "earth" in p.lower():
            bad.append(f"{cid}（Googleアースの絵が残っている＝表示の文を書き足すこと）")
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
        slots += 1
        photos.setdefault(stem, (cid, r))
    if bad:
        raise SystemExit(f"🔴 名乗れない素材がある。書かずに止めた: {bad}")
    if len(photos) != N_PHOTOS or slots != N_PHOTO_SLOTS:
        raise SystemExit(f"🔴 写真が {len(photos)} 点・{slots} カット（仕様は {N_PHOTOS} 点・{N_PHOTO_SLOTS} カット）。書かずに止めた。")
    docs = Counter(pages.get(s, {}).get("doc", "?") for s in pgs)
    if len(pgs) != N_PAGES or dict(docs) != PAGE_DOCS:
        raise SystemExit(f"🔴 頁が {len(pgs)} 枚・{dict(docs)}（仕様は {N_PAGES} 枚・{PAGE_DOCS}）。書かずに止めた。")
    clips = []
    for cid in use:
        stem = Path(cuts.SPEC[cid]["photo"]).stem
        r = table.get(stem) or {}
        if norm_lic(r.get("lic")) != "パブリックドメイン" or "dvidshub.net/video/" not in (r.get("url") or ""):
            raise SystemExit(f"🔴 動く映像 {cid} の権利か出どころが DVIDS の PD ではない: {r}。書かずに止めた。")
        clips.append((cid, r))
    return photos, clips, docs


def read_credits() -> str:
    photos, clips, docs = used_material()
    free = OrderedDict((k, Counter()) for k in FREE)
    by_lic = OrderedDict((k, []) for k in LICENSE_URL)
    quoted = []
    for stem, (cid, r) in sorted(photos.items(), key=lambda x: x[1][0]):
        lic = norm_lic(r["lic"])
        who = onscreen(f"ep14/{stem}.jpg", lic)
        if lic in FREE:
            free[lic][who] += 1
        elif lic == QUOTE:
            quoted.append((who, r))
        else:
            by_lic[lic].append((who, link(r["url"])))
    n_free = sum(sum(c.values()) for c in free.values())
    n_by = len(by_lic["CC BY 3.0"]) + len(by_lic["帰属表示"])
    n_sa = sum(len(v) for k, v in by_lic.items() if "-SA" in k)
    print(f"■ 素材：写真 {len(photos)}点（PD・CC0 {n_free}・CC BY と帰属表示 {n_by}・CC BY-SA {n_sa}・"
          f"引用 {len(quoted)}）／動く映像 {len(clips)}本／頁 {sum(docs.values())}枚 {dict(docs)}")
    if n_by != 2 or n_sa != 14 or len(quoted) != 1:
        raise SystemExit("🔴 権利ごとの点数が⑥で数えた値（CC BY と帰属表示 2・BY-SA 14・引用 1）と違う。"
                         "断り書きの文を当て直すこと。書かずに止めた。")
    out = ["【写真】"]
    for lic, whos in free.items():
        if whos:
            out.append("・" + "・".join(f"{w} {n}点" for w, n in whos.items()) + f"＝{lic}")
    for lic, rows in by_lic.items():
        if not rows:
            continue
        out.append(f"・{lic}（許諾 {LICENSE_URL[lic]}）")
        out += [f"　{who}　{url}" for who, url in rows]
    for who, r in quoted:
        out.append(f"・{who}（2014年4月16日・沈んでいくセウォル号）＝引用。事故の検証のための引用として、"
                   f"切らず・色を変えず・何も重ねず、額に入れて出しています")
    out.append("※ CC BY の写真と帰属表示の写真（2点）は、写り込んだ人の顔を外す切り出しと、色調の変更をしています。")
    out.append(f"※ CC BY-SA の写真 {n_sa}点は、切らず・色を変えず・何も重ねず、"
               "そのままの形で額に入れて出しています（無改変）。")
    out.append("【映像】")
    for cid, r in clips:
        out.append(f"・{r['author']}の記録映像（DVIDS）＝パブリックドメイン（米国の職務著作）　{r['url']}")
    out.append("※ 米国防総省（米海軍・米海兵隊）の写真と映像を使っていますが、米国防総省がこの動画を推奨・支持していることを"
               "意味するものではありません（The appearance of U.S. Department of Defense (DoD) visual information "
               "does not imply or constitute DoD endorsement.）")
    out.append("【報告書などの頁】")
    out.append("・" + "・".join(f"{PAGE_DOC_NAME[d]} {n}枚" for d, n in docs.items()) + "（上の出典の資料より）")
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
    # 🔴 入れてはいけない語（BGM のクレジット・kousei §5-1 の使わないもの・伏せ字）
    for bad in ("<", ">", "BGM", "DOVA", "OpenTracks", "疑惑の霧", "Keido", "ﾀﾋ",
                "下着", "孟骨", "日本で18年", "ありあけ", "潜水艦", "7時間", "監査院", "1,077", "1077"):
        if bad in desc or bad in TITLE:
            raise SystemExit(f"🔴 入れてはいけない語「{bad}」が入っている。書かずに止めた。")
    if "死亡" in TITLE:
        raise SystemExit("🔴 タイトルに「死亡」が入っている。書かずに止めた。")
    if "【映像あり】" in TITLE:
        raise SystemExit("🔴 【映像あり】が付いている（この回の動く映像は捜索の画だけ＝付けない）。書かずに止めた。")
    if not desc.startswith(FIRST_YUKKURI + "\n"):
        raise SystemExit("🔴 概要欄の最初がゆっくりの一文（09-25 カズヤくん指定）になっていない。書かずに止めた。")
    if not TITLE.endswith("【事故検証】【ゆっくり解説】"):
        raise SystemExit("🔴 タイトルの末尾が「【事故検証】【ゆっくり解説】」でない（B4-8）。書かずに止めた。")
    print(f"タイトル {len(TITLE)} 字（上限 100 ／ 型の幅 67〜94＋【ゆっくり解説】8）")
    print(f"説明     {len(desc)} 字（上限 5,000）")
    if len(TITLE) > 100 or len(desc) > 5000:
        raise SystemExit("🔴 上限を超えた。書かずに止めた。")
    if not (67 + 8 <= len(TITLE) <= 100):
        raise SystemExit("🔴 タイトルが型の幅から外れた。書かずに止めた。")

    meta = {
        "slug": "ep14",
        "title": TITLE,
        "description": desc,
        "tags": ["セウォル号", "セウォル号沈没事故", "旅客船", "フェリー", "海難事故", "韓国", "2014年",
                 "珍島", "修学旅行", "海洋警察", "フェリーなみのうえ", "事故検証", "図解", "一次資料",
                 "解説", "ゆっくり解説"],
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
