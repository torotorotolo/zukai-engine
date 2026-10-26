# -*- coding: utf-8 -*-
"""25本目（JR福知山線脱線事故）の `config/meta_ep25.json` を**機械で**組み立てる（2026-10-26・⑥）。

`qa_out/ep24_meta.py`（用語・目次・点数・権利・字数の網）と `qa_out/ep17_meta.py`（運輸安全委員会の報告書・衛星写真の書き方）を写して、
この回の形に合わせた。

🔴 手で書かない理由（ep7〜ep24 と同じ）
  ① 用語は `ref/ep25/yougo.md` の「## 貼る本文」の節が正本＝**そのまま**貼る（`**` だけ外す）。
     見出しの語が語り（`narration.SCRIPT`）に出るかと、並びが語りに初めて出る順かを1語ずつ当てる
  ② 素材の点数は**章ファイルの実配線**（`cuts.SPEC` の写真と頁／`footage.USE` の映像）から数え、
     権利は**画面の出典表記**（`ref/ep25/credits.json`・`clips.json`・`cuts.ss.SAT`）で照らす。名乗れない素材が出たら落ちる
  ③ 目次は `scene_jiko.CUTS` の秒を頭から積む＝**焼いた版と同じ秒**（章の扉の秒は CUTS に入っている）
  ④ タイトル 100字・説明 5,000字の上限と、入れてはいけない語を、書く前に確かめる

🔴 この回のところ
  - 運輸安全委員会（報告書・建議・検証報告書）と国土交通省の頁＝公共データ利用規約（第1.0版）（`ref/ep25/src/rights/` の写し）
  - 個人名義の写真（Wikimedia Commons・CC BY 3.0）は1点（C3）＝作者の名前は**公開リポに書かない**＝焼くときと同じく git の外の表
    `ref/ep25/src/credits_private.tsv` から `scene_jiko._ep25_author`（名乗りの短い形）で足す（`config/` は gitignore＝説明の JSON は公開リポに入らない）
  - 判決と決定の頁＝裁判所のウェブサイト（判決の文は著作権法13条）。会社の資料の写し（付図35・47・48）は報告書の付図として頁ごと
  - 地図の衛星写真＝Google（帰属は地図の右下）・線路の位置＝地理院地図Vector（国土地理院）
  - フリー素材の映像（Pexels）は「イメージ」の断りだけ（クレジットは書かない＝決め）
  - 人は役職だけ（①の決め）。【映像あり】は付けない（この事故の動く記録映像は0本）

    python qa_out/ep25_meta.py            # 組み立てて config/meta_ep25.json に書く
    python qa_out/ep25_meta.py --dry      # 書かずに中身と字数だけ出す
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

YOUGO = HERE / "ref" / "ep25" / "yougo.md"
CREDITS_JSON = HERE / "ref" / "ep25" / "credits.json"
ASSETS_JSON = HERE / "ref" / "ep25" / "assets.json"
CLIPS = HERE / "ref" / "ep25" / "clips.json"
OUT = HERE / "config" / "meta_ep25.json"

N_GLOSS = 12          # `ref/ep25/yougo.md` の「貼る本文」の語数（台本 §8 の13語から語りに無い「緩和曲線」を外した）
# ⚠️ 下の値は⑥（10-26）の配線（版 a1fdb813）から数えた点数（変わったら止まる＝文の点数を当て直す）。None＝数えて出すだけ
N_COUNTS = {"sat": 5, "rfig": 61, "mlit": 12, "rpage": 9, "s1": 4, "gsi": 3, "cc0": 4, "kengi": 1, "court": 3, "own": 1,
            "draft": 1, "stock_film": 18}

# ✅ 承認①（10-25）の題。頭の語「尼崎のカーブ」＝場所（17本目「名古屋空港」と同じ型の内）
TITLE = "尼崎のカーブに、運転士はわざと速く入ったのか。報告書の答えは「低いものと考えられる」だった。JR福知山線脱線事故の真相【事故検証】【ゆっくり解説】"
TITLE_LEN = 73        # 決めた題の字数（写し間違いの網）

# ⚠️ 本文（台本第2版 c101〜c107）で言っていることだけを書く。🔴「低いものと考えられる」は c106 の範囲（この曲線をわざと速く）だけ
HEAD = """【この動画について】
兵庫県尼崎市。JR福知山線の線路は、尼崎駅の手前で、急な右の曲線を描きます。制限速度は時速70キロ。2005年4月25日の朝、7両編成の上りの快速電車が、この曲線に時速約116キロで入りました。午前9時18分54秒ごろ、5両が脱線し、前の2両は線路の脇のマンションにぶつかりました。乗客106人と運転士、あわせて107人が亡くなり、562人がけがをしました。

運転士が遅れを取り戻そうと、わざと速く曲線に入った。よく語られる話です。けれども、国の事故調査委員会の報告書は、遅れを取り戻すため、この曲線をわざと速く通ろうとした可能性を、「低いものと考えられる」と書いています。

では、あの朝、何が起きていたのか。ブレーキは、なぜ遅れたのか。この動画は、車掌と指令の無線の録音と列車の記録を秒で重ね、報告書の言葉をその強さのまま読みながら追っていきます。
"""

# 台本第2版 §10（資料）と ①の取得記録（`ref/ep25/src/fetch_log.tsv`）から。⑥（10-26）URL は curl で開けるかを確かめる
PRIMARY = """【出典】
・航空・鉄道事故調査委員会『鉄道事故調査報告書 RA2007-3』（2007年6月28日・本文と別冊の付図）　https://jtsb.mlit.go.jp/railway/fukuchiyama/RA07-3-1-1.pdf
・建議（2005年9月6日・2007年6月28日）　https://jtsb.mlit.go.jp/railway/kyukengi/170906k.pdf　https://jtsb.mlit.go.jp/railway/kyukengi/190628k.pdf
・運輸安全委員会の検証報告書（2011年4月15日）と付録「事故調査報告書に関する解説」　https://jtsb.mlit.go.jp/fukuchiyama/kensyou/fu04-finalreport.pdf
・最高裁判所 第二小法廷 決定（2017年6月12日）　https://www.courts.go.jp/hanrei/86834/detail2/index.html
・神戸地方裁判所 判決（2012年1月）　https://www.courts.go.jp/hanrei/82178/detail4/index.html
・国土交通省の福知山線列車事故の頁と報道発表https://www.mlit.go.jp/fukuchiyama/index.html
・消防庁 第32報（2005年5月24日）　https://www.fdma.go.jp/disaster/info/assets/post364.pdf
・兵庫県『福知山線列車事故検証報告書』（2006年1月）　https://web.pref.hyogo.lg.jp/kk37/documents/000007823.pdf
・JR西日本（事故の概要・祈りの杜・安全性向上計画・建議と所見への取り組み・「将来にわたる鉄道の安全の実現に向けて」）　https://www.westjr.co.jp/fukuchiyama/
・国会会議録（2005年5月12日・5月17日 参議院 国土交通委員会、2013年11月13日 衆議院 法務委員会、2023年3月8日 参議院 予算委員会ほか）　https://kokkai.ndl.go.jp/"""

TAIL = """動画に出てくる数値・時刻・言葉は、これらの記録によります。
報告書の言い方（「推定される」「考えられる」「可能性が考えられる」）は、その強さのまま読んでいます。
※ 出どころの色分け（図と札）：報告書（2007年）＝青・建議＝桃・車掌＝橙・指令員＝緑・国会＝紫・消防庁と兵庫県＝水色・JR西日本＝茶・検証報告書（2011年）＝白
※ 画面の模式図・再現のイラスト・地図の線は、記録をもとに描いた図です。
※ 人は役職だけでお呼びしています。乗客・ご遺族・負傷された方・救助にあたった方のお名前とお言葉は出していません。"""

# ✅ ⑥（10-26）カズヤくん：地＝生成 AI（gen_thumb_ai fuk_b＝横倒しの車両に寄せた空撮・1.20倍）・H 型の反転版・大きな語「福知山線」を
#    中央揃え（帯 110〜1170）・「JR」は緑の字で左上に小さく（「福」に少し重なる＝JR の字の 44%）＝`qa_out/ep25_thumb_hx.py cand3` の L110・z120
THUMB = "out/thumb/ep25/ep25_Hinv_fuk_b_z120_L110.png"
THUMB_MD5 = "396949b4a08c126381f571b19de17712"
THUMB_NOTE = "※ サムネイルの絵は、生成AIで作った再現のイメージです（実際の写真ではありません）。"

TAGS = ["JR福知山線脱線事故", "福知山線", "尼崎", "JR西日本", "2005年", "脱線事故", "鉄道事故", "ATS", "運輸安全委員会",
        "事故調査報告書", "事故検証", "一次資料", "ゆっくり解説", "ドキュメンタリー", "解説"]

PDL = "公共データ利用規約（第1.0版）"
LIC_URL = {"CC BY 3.0": "https://creativecommons.org/licenses/by/3.0/deed.ja",
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
    """`ref/ep25/yougo.md` の「## 貼る本文」の節を**そのまま**返す（次の `---` か `## ` まで）。見出しの語が語りに出るかを当てる。"""
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
    """SPEC の値を辿って、素材の道（`ep25/…`）を全部出す（尻・頭の差し込み・地に敷く写真も含む）。"""
    if isinstance(v, str):
        if v.startswith("ep25/"):
            yield v
    elif isinstance(v, dict):
        for x in v.values():
            yield from _walk(x)
    elif isinstance(v, (list, tuple)):
        for x in v:
            yield from _walk(x)


_JTSB = r"（運輸安全委員会の頁）(を加工して作成)?$"
# 画面の出典表記（credits.json の値＝作者は印 {作者} のまま）→ 種類（名乗れないものは None）。⚠️ 並びに意味がある（上から当てる）
KINDS = [
    ("rfig", r"^出典：鉄道事故調査報告書 RA2007-3 付図\d+" + _JTSB),
    ("rpage", r"^出典：鉄道事故調査報告書 RA2007-3( p\.\d+)?" + _JTSB),
    ("draft", r"^出典：事実調査に関する報告書の案" + _JTSB),
    ("kengi", r"^出典：建議（2005年9月6日・航空・鉄道事故調査委員会）" + _JTSB),
    ("s1", r"^出典：検証報告書 (p\.\d+|付録2-2「事故調査報告書に関する解説」)" + _JTSB),
    ("mlit", r"^出典：国土交通省ウェブサイト（https://www\.mlit\.go\.jp/fukuchiyama/index\.html）(を加工して作成)?$"),
    ("gsi", r"^出典：国土地理院ウェブサイト（地理院タイル）を加工して作成$"),
    ("court", r"^出典：(最高裁判所 第二小法廷 決定（2017年6月12日）|神戸地方裁判所 判決（2012年1月）)（裁判所ウェブサイト）$"),
    ("own", r"^写真：\{作者\}／Wikimedia Commons（CC BY 3\.0）・改変：切出$"),
    ("cc0", r"^写真：Wikimedia Commons（CC0）(・改変：顔にモザイク)?$"),
    ("sat", r"^地図：Google マップの衛星写真（帰属は地図の右下）$"),
]


def _kind(s: str):
    for k, pat in KINDS:
        if re.match(pat, s):
            return k
    return None


def used_material():
    """章ファイルの実配線から、写真・図・頁・衛星写真・映像を数える。権利は画面の出典表記で照らす。"""
    import cuts
    import cuts.ss as SS
    import footage as F
    cred = json.loads(CREDITS_JSON.read_text(encoding="utf-8"))
    for v in SS.SAT.values():                 # 衛星写真＝出典は表 SAT の credit（scene_jiko.ep25_credit と同じ）
        cred.setdefault(v["file"], v["credit"])
    clips = json.loads(CLIPS.read_text(encoding="utf-8"))
    got, bad = OrderedDict(), []
    for cid, sp in cuts.SPEC.items():
        for p in _walk(sp):
            if not re.search(r"\.(jpe?g|png)$", p, re.I):
                continue
            if Path(p).stem.startswith("fb_"):    # 動く映像の控えの静止画＝本番は映像
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
    stock_films = OrderedDict()
    for cid, u in F.USE.items():
        k = u["clip"]
        c = clips.get(k)
        if c is None:
            bad.append(f"{cid}:{k}（clips.json に無い）")
            continue
        if c.get("credit", "") == "イメージ（Pexels）":
            stock_films.setdefault(k, c)
        else:
            bad.append(f"{cid}:{k}（名乗れない映像の出典：{c.get('credit')}）")
    if bad:
        raise SystemExit(f"🔴 名乗れない素材がある。書かずに止めた: {bad}")
    counts = {k: len(v) for k, v in got.items()}
    counts.update(stock_film=len(stock_films))
    print(f"■ 素材（配線から）：{counts}")
    if N_COUNTS is not None and counts != N_COUNTS:
        raise SystemExit(f"🔴 点数が⑥で数えた値 {N_COUNTS} と違う。文の点数を当て直すこと。書かずに止めた。")
    return got, counts


def _asset(p):
    return json.loads(ASSETS_JSON.read_text(encoding="utf-8"))[Path(p).stem]


def read_credits() -> str:
    got, n = used_material()
    jt = n.get("rfig", 0) + n.get("rpage", 0) + n.get("draft", 0) + n.get("kengi", 0) + n.get("s1", 0)
    out = ["【写真・図・頁・映像】",
           f"・運輸安全委員会の資料 {jt}点（報告書の付図 {n.get('rfig', 0)}点・報告書の頁 {n.get('rpage', 0)}枚・"
           f"検証報告書と付録 {n.get('s1', 0)}枚・建議 {n.get('kengi', 0)}枚・報告書の案 {n.get('draft', 0)}枚）"
           f"＝{PDL}にもとづいて利用（出典：運輸安全委員会 https://jtsb.mlit.go.jp/ ・切り出しなどの加工をしたものは画面に「加工して作成」）",
           f"・国土交通省の写真と頁 {n.get('mlit', 0)}点＝{PDL}にもとづいて利用（出典：国土交通省ウェブサイト https://www.mlit.go.jp/fukuchiyama/index.html ）",
           "※ 報告書の付図のうち、会社の資料の写し（付図35・47・48）は、報告書の頁として引用しています（著作権法32条）"]
    if n.get("court"):
        out.append(f"・判決と決定の頁 {n['court']}枚＝最高裁判所・神戸地方裁判所（裁判所のウェブサイト）")
    for p, (cid, s) in (got.get("own") or {}).items():
        a = _asset(p)
        if a.get("lic") != "CC BY 3.0":
            raise SystemExit(f"🔴 {a.get('code')} のライセンスが台帳（{a.get('lic')}）と画面（CC BY 3.0）で違う。書かずに止めた。")
        out.append(f"・Wikimedia Commons の写真　{S._ep25_author(p)}（CC BY 3.0・切り出し）　{a['url']}")
    if n.get("cc0"):
        out.append(f"・Wikimedia Commons の CC0 の写真 {n['cc0']}点（祈りの杜・事故の現場の今・回り道の案内の看板）")
    out.append("　ライセンス：" + "　".join(f"{lic} {LIC_URL[lic]}" for lic in ("CC BY 3.0", "CC0")))
    if n.get("gsi"):
        out.append(f"・空中写真 {n['gsi']}点＝国土地理院ウェブサイト（地理院タイル）を加工して作成")
    if n.get("sat"):
        out.append(f"・地図の衛星写真 {n['sat']}点＝Google マップ（帰属は地図の右下）・線路の位置＝地理院地図Vector（国土地理院）")
    out.append("※ 画面に「イメージ」と出る映像は、フリー素材です。その日・その場を写したものではありません")
    out.append("※ 国の機関（運輸安全委員会・国土交通省・消防庁）・兵庫県・裁判所・JR西日本の資料を使っていますが、"
               "これらの機関や会社がこの動画を作ったり、推奨・支持したりしているものではありません")
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
    desc = "\n".join([HEAD, chapters(), "", read_glossary(), "", PRIMARY, "", read_credits(), "", tail])
    # 🔴 入れてはいけない語（BGM のクレジット・ゆっくりの一文・煽り語・タグの残り）
    for bad in ("<", ">", "BGM", "DOVA", "OpenTracks", "ゆっくりボイス", "AquesTalk", "即死", "絶命", "地獄",
                "【映像あり】", "{作者}", S.EP23_AUTHOR_STANDIN):
        if bad in desc or bad in TITLE:
            raise SystemExit(f"🔴 入れてはいけない語「{bad}」が入っている。書かずに止めた。")
    for bad in ("死亡",):
        if bad in TITLE or bad in desc:
            raise SystemExit(f"🔴 「{bad}」が入っている。書かずに止めた。")
    # 🔴「低いものと考えられる」は c106 の範囲（この曲線をわざと速く）だけ＝説明の中で2回目が出たら止める（記憶 project-jiko-ep25-fukuchiyama）
    if desc.count("低いものと考えられる") != 1:
        raise SystemExit("🔴 説明に「低いものと考えられる」が1回でない（範囲は c106 の一文だけ）。書かずに止めた。")
    if not TITLE.endswith("【事故検証】【ゆっくり解説】"):
        raise SystemExit("🔴 タイトルの末尾が「【事故検証】【ゆっくり解説】」でない（B4-8）。書かずに止めた。")
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
        raise SystemExit(f"🔴 サムネが無いか、⑥で決めた物と違う: {THUMB or '（未定）'}。書かずに止めた。")
    meta = {"slug": "ep25", "title": TITLE, "description": desc, "tags": TAGS, "thumbnail": THUMB,
            "genre": "jiko", "playlist": ""}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✓ 書いた → {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
