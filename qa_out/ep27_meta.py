# -*- coding: utf-8 -*-
"""27本目（八田與一容疑者の事件）の `config/meta_ep27.json` を**機械で**組み立てる（2026-10-30・⑥'）。

`qa_out/ep26_meta.py`（用語・目次・字数の網）を写し、個人名義の写真の並べ方は `qa_out/ep24_meta.py`（作者・ライセンス・点数で
まとめる＝頁の URL を1点ずつ並べると 5,000字に入らない）に合わせた。

🔴 手で書かない理由（ep7〜ep26 と同じ）
  ① 用語は `ref/ep27/yougo.md` の「## 貼る本文」の節が正本＝**そのまま**貼る。見出しの語が語りに出るかと、並びが語りに初めて出る順かを当てる
  ② 素材の点数は**章ファイルの実配線**（`cuts.SPEC` の写真／`footage.USE` の映像）から数え、権利は**画面の出典表記**
     （`ref/ep27/credits.json`・`clips.json`・`cuts.ss.SAT`）で照らす。名乗れない素材が出たら落ちる
  ③ 目次は `scene_jiko.CUTS` の秒を頭から積む＝**焼いた版と同じ秒**
  ④ タイトル 100字・説明 5,000字の上限と、入れてはいけない語を、書く前に確かめる

🔴 事件の回（ルール §B2-10・記憶 feedback-jiko-incident-case-rules＝10-29 承認の7点）
  - 被害者・遺族・けがをした人の名前は書かない（年齢と立場だけ）／容疑者は必ず「八田與一容疑者」（犯人と書かない＝推定無罪）
  - **情報提供の窓口を出す**＝大分県警察の頁の言葉のまま（別府警察署・匿名通報窓口・緊急は110番・匿名などは報奨金の対象外）
  - 題の札＝【事件検証】【ゆっくり解説】・まだ終わっていない事件なので「真相」を使わない／「死亡」は題に使わない
  - 写真の作者（Commons の撮影者）の名前は**公開リポに書かない**＝焼くときと同じく git の外の表 `ref/ep27/src/credits_private.tsv` から
    `scene_jiko._ep27_author` で足す（`config/` は gitignore＝説明の JSON は公開リポに入らない）
  - 🔴 c608-2 は ⑥'（10-30）で差し替えた＝「10月30日、警察は、2022年に撮られた新しい写真を載せたチラシを、配り始めた。」＝説明も同じ事実まで

    python qa_out/ep27_meta.py            # 組み立てて config/meta_ep27.json に書く
    python qa_out/ep27_meta.py --dry      # 書かずに中身と字数だけ出す
"""
import hashlib
import json
import os
import re
import sys
import unicodedata
from collections import OrderedDict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
os.environ.pop("GITHUB_ACTIONS", None)      # 作者の名前を仮の字にしない（焼く道と同じ）
import scene_jiko as S            # noqa: E402

YOUGO = HERE / "ref" / "ep27" / "yougo.md"
CREDITS_JSON = HERE / "ref" / "ep27" / "credits.json"
ASSETS_JSON = HERE / "ref" / "ep27" / "assets.json"
CLIPS = HERE / "ref" / "ep27" / "clips.json"
OUT = HERE / "config" / "meta_ep27.json"

N_GLOSS = 3           # `ref/ep27/yougo.md` の「貼る本文」の語数（台本 §8 の12語から業界の専門語だけ＝⑥' の推奨）
# ⚠️ 下の値は⑥'（10-30）の配線（c608-2 を直した版）から数えた点数（変わったら止まる＝文の点数を当て直す）。None＝数えて出すだけ
N_COUNTS = {"own": 36, "cc0": 5, "sat": 7, "stock": 4, "pyt": 4, "phome": 2, "px": 1, "npa": 1, "film": 2,
            "mos_face": 3, "mos_shop": 5}

# ✅ ⑥'（10-30 試写のあと）カズヤくんの題＝「上記をタイトルとして、予約投稿してください」（承認① の A2「…まだ得られていない。」から差し替え
#    ＝時点を題に入れた「（2026年10月時点）」・事件名のあとの空白は半角のまま＝カズヤくんの字）
TITLE = ("別府ひき逃げ殺傷事件 まとめ完全版（2026年10月時点）八田與一容疑者の4年。"
         "寄せられた情報は1万3978件【事件検証】【ゆっくり解説】")
TITLE_LEN = 69        # 決めた題の字数（写し間違いの網）

# ⚠️ 本文（台本第2版 c101〜c107・c608）で言っていることだけを書く。🔴 容疑者は「八田與一容疑者」・「犯人」と書かない
HEAD = """【この動画について】
2026年10月、大分県別府市。ヨットが並ぶ港のそばで、警察が2日間、海を調べ、ボートも出しました。4年前の夜、その港のあたりで、ひとりの男の足取りが途絶えました。警察は、その男を、いまも探し続けています。2026年9月末までに警察に寄せられた情報は、1万3978件。それでも、逮捕につながる有力な手がかりは、まだ得られていないといいます。

始まりは、2022年6月29日の夜。別府市の交差点で、赤信号で止まっていたバイク2台に、後ろから車が追突しました。19歳の大学2年生が亡くなり、友人の大学生がけがをしました。運転していた男は、車を残して逃げました。警察はこの男を八田與一容疑者とみて、殺人と殺人未遂などの疑いで、全国に指名手配しています。

この動画は、事件の夜から、2026年10月の海の捜索と新しいチラシまでを、起きた順にたどります。分かっていることと、まだ分かっていないことを、分けて見ていきます。
"""

# 🔴 事件の回の決まり⑤＝大分県警察の頁（satujinjiken.html・2025-12-11 更新・10-30 に原文で読んだ）の言葉のまま
WINDOW = """【情報提供の窓口】（大分県警察の頁より）
別府警察署（0977-21-2131（代表電話））または「匿名通報窓口（殺人等事件情報提供窓口）」に情報をお寄せください。
指名手配被疑者に似た人が目の前にいるなど緊急を要する場合は、110番通報をお願いします。
※ 匿名等のため個人の特定ができない場合等は、報奨金支払の除外事由となります。
・大分県警察「殺人等事件捜査にご協力を」　https://www.pref.oita.jp/site/keisatu/satujinjiken.html
・大分県警察「匿名通報窓口」　https://www.pref.oita.jp/site/keisatu/tokumeituho.html
※ 元刑事は、似た人を見ても、声をかけたり、写真や動画をSNSに上げたりせず、警察に知らせるよう勧めています（NEWSポストセブン 2026年10月25日）"""

# 台本第2版の出典の欄と `ref/ep27/sources.md` §1・§5 から。⑥'（10-30）URL は curl で開けるかを確かめた（4本＝200）
PRIMARY = """【出典】
・大分県警察「殺人等事件捜査にご協力を」（2025年12月11日更新）　https://www.pref.oita.jp/site/keisatu/satujinjiken.html
・大分県警察「指名手配被疑者の検挙にご協力を！」（2026年10月1日更新）　https://www.pref.oita.jp/site/keisatu/simeitehaigekkan.html
・警察庁「警察庁指定重要指名手配被疑者」　https://www.npa.go.jp/bureau/criminal/wanted/jyuyo1.html
・警察庁「捜査特別報奨金に関する広告」（2026年9月11日）　https://www.npa.go.jp/bureau/criminal/reward/contents117.html
・大分県別府市大学生ひき逃げ殺人事件早期解決を願う会「捜査協力者に対する謝礼金提供規約」　https://www.pref.oita.jp/uploaded/life/2323829_4634908_misc.pdf
・大分県警察 公式YouTube（2024年8月1日・2025年12月11日）・公式X（2026年6月29日）
・報道：OBS大分放送・OAB大分朝日放送・TOSテレビ大分・日本テレビ・FNN・ABEMA TIMES・NEWSポストセブン・共同通信・大分合同新聞ほか（2022年〜2026年10月30日）"""

TAIL = """動画に出てくる数字と日付は、警察の発表と報道によります（2026年10月30日時点）。
※ この動画は、裁判で罪が決まるまでは罪を犯した人として扱わない立場（推定無罪）で、八田與一容疑者についてお伝えしています。
※ 亡くなった方・けがをされた方・ご家族のお名前は出していません。
※ SNS の投稿は、確かめられた情報ではありません（画面に注記しています）。
※ 画面の模式図・地図の線は、報道と警察の発表をもとに描いた図です。"""

# ✅ ⑥'（10-30）カズヤくん：「v6 を A サムネ。紺を B サムネとしてテスト」＝A（Claude が貼る）＝v6（暗い赤の地・`--style=v6`）／
#    B＝紺（警察の青）`out/thumb/ep27/ep27_A6n_v6.png`（md5 974188cc…・`--style=v6c`）はカズヤくんが Studio の「テストと比較」で手動（24・26本目と同じ）
# 🆕 10-31（公開のあと）カズヤくん「k5 で差し替え」＝v7 の k5（黒い単色の地・顔を切り抜き・字なしのトラテープ・「容疑者」なし・
#    「八田與一」はキリンをもう一度「事態が動いています」のサムネの写し＝赤い字に白いぼかしの縁・縦 1.15倍＝`ep27_thumb.py --style=v7 --kinds=k5`）。
#    B（紺）は「青版は不要」＝作らない。v6（2e4a8ce1…）と途中の版は out/thumb/ep27/ に残す
THUMB = "out/thumb/ep27/ep27_A7k5_v7.png"
THUMB_MD5 = "5d4ed4da9337ccf59442f89a79a9c2d2"
THUMB_NOTE = "※ サムネイルの写真は、警察庁の重要指名手配の頁の写真（大分県警察手配）です。"

TAGS = ["八田與一容疑者", "八田與一", "別府ひき逃げ殺傷事件", "大分県別府市", "ひき逃げ", "重要指名手配", "指名手配",
        "捜査特別報奨金", "大分県警察", "未解決事件", "事件検証", "ゆっくり解説", "ドキュメンタリー", "解説", "ニュース"]

LIC_URL = {"CC BY 2.0": "https://creativecommons.org/licenses/by/2.0/deed.ja",
           "CC BY 3.0": "https://creativecommons.org/licenses/by/3.0/deed.ja",
           "CC BY-SA 2.0": "https://creativecommons.org/licenses/by-sa/2.0/deed.ja",
           "CC BY-SA 4.0": "https://creativecommons.org/licenses/by-sa/4.0/deed.ja",
           "CC0": "https://creativecommons.org/publicdomain/zero/1.0/deed.ja"}


def _nfkc(s):
    return unicodedata.normalize("NFKC", s)


def narration_rows():
    import narration as N
    return [(cid, _nfkc("".join(rows))) for cid, rows in N.SCRIPT]


def first_cut(head):
    """見出しの語が語りに初めて出るカット（無ければ None）。"""
    h = _nfkc(head)
    return next((cid for cid, t in narration_rows() if h in t), None)


def read_glossary() -> str:
    """`ref/ep27/yougo.md` の「## 貼る本文」の節を**そのまま**返す（次の `---` か `## ` まで）。見出しの語が語りに出るかを当てる。"""
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
    order = [c for c, _ in narration_rows()]
    seen, miss = [], []
    for ln in body.splitlines():
        if not ln.startswith("・"):
            continue
        head = re.split(r"（|…|＝", ln[1:], maxsplit=1)[0].strip()
        c = first_cut(head)
        print(f"  用語 {head} → 語りに初めて出る {c}")
        if c is None:
            miss.append(head)
        else:
            seen.append(order.index(c))
    if miss:
        raise SystemExit(f"🔴 見出しの語が語りに無い: {miss}（本文の言い方に合わせる・ルール 5a-10）。書かずに止めた。")
    if seen != sorted(seen):
        raise SystemExit("🔴 用語の並びが語りに初めて出る順でない。書かずに止めた。")
    return body


def _walk(v):
    """SPEC の値を辿って、素材の道（`ep27/…`）を全部出す（地に敷く写真も含む）。"""
    if isinstance(v, str):
        if v.startswith("ep27/"):
            yield v
    elif isinstance(v, dict):
        for x in v.values():
            yield from _walk(x)
    elif isinstance(v, (list, tuple)):
        for x in v:
            yield from _walk(x)


_MOS = r"(・(?:顔|店名|顔と店名)にモザイク)?"
# 画面の出典表記（credits.json の値＝作者は印 {作者} のまま）→ 種類（名乗れないものは None）。⚠️ 並びに意味がある（上から当てる）
KINDS = [
    ("own", r"^写真：\{作者\}／Wikimedia Commons（CC BY(?:-SA)? [234]\.0）／改変(?:なし|：切出" + _MOS + r")$"),
    ("cc0", r"^Wikimedia Commons（CC0）(?:／改変：店名にモザイク)?$"),
    ("sat", r"^地図：Google マップの衛星写真（帰属は地図の右下）$"),
    ("stock", r"^イメージ（Pexels）$"),
    ("pyt", r"^出典：大分県警察 公式YouTube（\d{4}年\d{1,2}月\d{1,2}日）$"),
    ("phome", r"^出典：大分県警察（ホームページ・\d{4}年\d{1,2}月）$"),
    ("px", r"^出典：大分県警察 公式X（\d{4}年\d{1,2}月\d{1,2}日）$"),
    ("npa", r"^出典：警察庁 重要指名手配の頁$"),
]
YT_POLICE = "出典：大分県警察 公式YouTube（2025年12月11日）"


def _kind(s: str):
    for k, pat in KINDS:
        if re.match(pat, s):
            return k
    return None


def used_material():
    """章ファイルの実配線から、写真・衛星写真・映像を数える。権利は画面の出典表記で照らす。"""
    import cuts
    import cuts.ss as SS
    import footage as F
    cred = json.loads(CREDITS_JSON.read_text(encoding="utf-8"))
    for v in SS.SAT.values():                 # 衛星写真＝出典は表 SAT の credit（scene_jiko.ep27_credit と同じ）
        cred.setdefault(v["file"], v["credit"])
    clips = json.loads(CLIPS.read_text(encoding="utf-8"))
    got, bad, mos = OrderedDict(), [], {"顔": set(), "店名": set()}
    for cid, sp in cuts.SPEC.items():
        for p in _walk(sp):
            if not re.search(r"\.(jpe?g|png)$", p, re.I):
                continue
            if Path(p).stem.startswith("fb_"):    # 動く映像の控えの静止画＝本番は映像（県警の動画 YT-C）
                continue
            s = cred.get(p)
            if s is None:
                bad.append(f"{cid}:{p}（credits.json に無い）")
                continue
            k = _kind(s)
            if k is None:
                bad.append(f"{cid}:{p}（名乗れない：{s}）")
                continue
            got.setdefault(k, OrderedDict()).setdefault(p, (cid, s))
            for w in mos:
                if f"{w}にモザイク" in s or (w in ("顔", "店名") and "顔と店名にモザイク" in s):
                    mos[w].add(p)
    films = OrderedDict()
    for cid, u in F.USE.items():
        c = clips.get(u["clip"])
        if c is None:
            bad.append(f"{cid}:{u['clip']}（clips.json に無い）")
            continue
        if c.get("credit", "") != YT_POLICE:
            bad.append(f"{cid}:{u['clip']}（名乗れない映像の出典：{c.get('credit')}）")
            continue
        films[cid] = c                            # 1本の動画から2区間（c106・c305）＝カットで数える
    if bad:
        raise SystemExit(f"🔴 名乗れない素材がある。書かずに止めた: {bad}")
    counts = {k: len(v) for k, v in got.items()}
    counts.update(film=len(films), mos_face=len(mos["顔"]), mos_shop=len(mos["店名"]))
    print(f"■ 素材（配線から）：{counts}")
    if N_COUNTS is not None and counts != N_COUNTS:
        raise SystemExit(f"🔴 点数が⑥'で数えた値 {N_COUNTS} と違う。文の点数を当て直すこと。書かずに止めた。")
    return got, counts


def read_credits() -> str:
    got, n = used_material()
    assets = json.loads(ASSETS_JSON.read_text(encoding="utf-8"))
    out = ["【写真・映像】"]
    # 個人名義（Commons）＝作者・ライセンスごとにまとめる（名前は git の外の表から＝焼く道と同じ）
    by = OrderedDict()
    for p, (cid, s) in (got.get("own") or {}).items():
        lic = re.search(r"（(CC BY(?:-SA)? [234]\.0)）", s).group(1)
        a = assets.get(Path(p).stem) or {}
        if a.get("lic") != lic:
            raise SystemExit(f"🔴 {Path(p).stem} のライセンスが台帳（{a.get('lic')}）と画面（{lic}）で違う。書かずに止めた。")
        by.setdefault((S._ep27_author(p), lic), []).append(p)
    out.append(f"・Wikimedia Commons の写真 {n.get('own', 0)}点（作者・ライセンス・点数＝CC BY-SA は加工なし・"
               "CC BY は切り出し・写真ごとの作者とライセンスは画面の出典の行にも）")
    for (who, lic), ps in by.items():
        out.append(f"　{who}（{lic}）" + (f"{len(ps)}点" if len(ps) > 1 else ""))
    for p, (cid, s) in (got.get("cc0") or {}).items():
        a = assets.get(Path(p).stem) or {}
        if a.get("lic") != "CC0":
            raise SystemExit(f"🔴 {Path(p).stem} のライセンスが台帳（{a.get('lic')}）と画面（CC0）で違う。書かずに止めた。")
    out.append(f"・Wikimedia Commons の写真 {n.get('cc0', 0)}点（CC0）")
    used_lic = sorted({lic for (_, lic) in by} | ({"CC0"} if n.get("cc0") else set()))
    out.append("　ライセンス：" + "　".join(f"{lic} {LIC_URL[lic]}" for lic in used_lic))
    out.append(f"　私人の顔が写る {n.get('mos_face', 0)}点は顔に、地元の店の名前が写る {n.get('mos_shop', 0)}点は店の名前に、モザイクをかけています")
    pol = n.get("pyt", 0) + n.get("phome", 0) + n.get("px", 0) + n.get("npa", 0)
    out.append(f"・警察の画像 {pol}点（大分県警察の公式YouTubeの手配の動画のコマ {n.get('pyt', 0)}点・ホームページの似顔絵 {n.get('phome', 0)}点・"
               f"公式Xの画像 {n.get('px', 0)}点・警察庁の重要指名手配の頁の写真 {n.get('npa', 0)}点）と、"
               f"大分県警察の公式YouTubeの手配の動画 {n.get('film', 0)}か所＝引用（加工なし・出典は画面に表示）")
    out.append(f"・地図の衛星写真 {n.get('sat', 0)}点＝Google マップ（帰属は地図の右下）")
    out.append(f"※ 画面に「イメージ」と出る写真（{n.get('stock', 0)}点）は、フリー素材です。その日・その場を写したものではありません")
    out.append("※ 警察庁・大分県警察の資料を使っていますが、これらの機関がこの動画を作ったり、推奨・支持したりしているものではありません")
    return "\n".join(out)


def chapters() -> str:
    starts, t = {}, 0.0
    for cid, sec in S.CUTS:
        starts[cid] = t
        t += sec
    rows = [(S.CUTS[0][0], "はじめに")]     # つかみ（c101〜c107）は章の印なし＝0:00 を足す
    import check_script as CSC
    for key, (n, name) in S.CHAPTERS.items():
        first = next((c for c, _ in S.CUTS if CSC.door_key(c) == key), None)
        if first is None:
            raise SystemExit(f"🔴 章 {key} の最初のカットが無い。書かずに止めた。")
        rows.append((first, f"第{n}章 {name}" if str(n).isdigit() else f"{n} {name}".strip()))
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
    tail = TAIL + ("\n" + THUMB_NOTE if THUMB_NOTE else "")
    desc = "\n".join([HEAD, WINDOW, "", chapters(), "", read_glossary(), "", PRIMARY, "", read_credits(), "", tail])
    # 🔴 入れてはいけない語（BGM のクレジット・ゆっくりの一文・煽り語・タグの残り）
    for bad in ("<", ">", "BGM", "DOVA", "OpenTracks", "ゆっくりボイス", "AquesTalk", "即死", "絶命", "地獄",
                "【映像あり】", "{作者}", S.EP23_AUTHOR_STANDIN):
        if bad in desc or bad in TITLE:
            raise SystemExit(f"🔴 入れてはいけない語「{bad}」が入っている。書かずに止めた。")
    # 🔴 事件の回（記憶 feedback-jiko-incident-case-rules）＝犯人と書かない・まだ終わっていない事件で「真相」を使わない・題に「死亡」を使わない
    for bad in ("犯人", "真相", "死亡", "逮捕された", "逮捕した"):
        if bad in TITLE or bad in desc:
            raise SystemExit(f"🔴 「{bad}」が入っている。書かずに止めた。")
    for where, txt in (("題", TITLE), ("説明", desc)):
        loose = re.findall(r"八田與一(?!容疑者)", txt)
        if loose:
            raise SystemExit(f"🔴 {where}に「容疑者」の付かない「八田與一」が {len(loose)} か所。書かずに止めた。")
    for need in ("0977-21-2131", "110番", "匿名通報窓口", "報奨金支払の除外事由"):
        if need not in desc:
            raise SystemExit(f"🔴 情報提供の窓口の「{need}」が無い（事件の回の決まり⑤）。書かずに止めた。")
    if not TITLE.endswith("【事件検証】【ゆっくり解説】"):
        raise SystemExit("🔴 タイトルの末尾が「【事件検証】【ゆっくり解説】」でない（事件の回の決まり⑥）。書かずに止めた。")
    print(f"タイトル {len(TITLE)} 字（上限 100 ／ 決めた題は {TITLE_LEN}）")
    print(f"説明     {len(desc)} 字（上限 5,000）")
    if len(TITLE) > 100 or len(desc) > 5000:
        raise SystemExit("🔴 上限を超えた。書かずに止めた。")
    if len(TITLE) != TITLE_LEN:
        raise SystemExit(f"🔴 決めた題（{TITLE_LEN}字）と字数が違う＝写し間違い。書かずに止めた。")
    if "--dry" in sys.argv:
        print("\n" + TITLE + "\n\n" + desc)
        return 0
    if N_COUNTS is None:
        raise SystemExit("🔴 N_COUNTS が未記入（--dry で数えて書いてから）。書かずに止めた。")
    p = HERE / THUMB if THUMB else None
    if not p or not p.exists() or hashlib.md5(p.read_bytes()).hexdigest() != THUMB_MD5:
        raise SystemExit(f"🔴 サムネが無いか、⑥'で決めた物と違う: {THUMB or '（未定）'}。書かずに止めた。")
    meta = {"slug": "ep27", "title": TITLE, "description": desc, "tags": TAGS, "thumbnail": THUMB,
            "genre": "jiko", "playlist": ""}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✓ 書いた → {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
