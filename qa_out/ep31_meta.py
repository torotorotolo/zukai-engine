# -*- coding: utf-8 -*-
"""31本目（全日空機雫石衝突事故）の `config/meta_ep31.json` を**機械で**組み立てる（2026-11-09・⑥）。

`qa_out/ep30_meta.py`（用語・目次・素材の点数・字数の網）を写し、素材の種類を31本目の出典の形に直した
（国会会議録の紙面・最高裁の判決・運輸白書・衆議院の頁・国交省の記者発表・地理院の空中写真・Google の衛星写真・
Commons・SDASM・防衛庁記録の静止画と映像・Pexels）。

🔴 手で書かない理由（ep7〜ep30 と同じ）
  ① 用語は `ref/ep31/yougo.md` の「## 貼る本文」の節が正本＝**そのまま**貼る。見出しの語が語りに出るかと、並びが語りに初めて出る順かを当てる
  ② 素材の点数は**章ファイルの実配線**（`cuts.SPEC` の写真／`footage.USE` の映像）から数え、権利は**画面の出典表記**
     （`ref/ep31/credits.json`・`clips.json`・衛星写真は `cuts.ss.SAT`）で照らす。名乗れない素材が出たら落ちる
  ③ 目次は `scene_jiko.CUTS` の秒を頭から積む＝**焼いた版と同じ秒**
  ④ タイトル 100字・説明 5,000字の上限と、入れてはいけない語を、書く前に確かめる

🔴 この回の線（台本 §0・記憶 project-jiko-ep31-shizukuishi）
  - 人の名前を書かない（立場だけ）。Commons の作者だけは git の外の表から `scene_jiko._ep31_person` で足す（`config/` は gitignore・
    `--dry` の写しは commit しない）
  - 判決の記号の字と「無罪」を書かない・「死亡」を使わない（亡くなった）
  - cc15「出典を示せば使ってよい、という決まりで公開」・cc16「置き場は、説明欄に書く」・cc17「読めていない」＝置き場と断りを入れる

    python -P qa_out/ep31_meta.py            # 組み立てて config/meta_ep31.json に書く
    python -P qa_out/ep31_meta.py --dry      # 書かずに中身と字数だけ出す
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

YOUGO = HERE / "ref" / "ep31" / "yougo.md"
CREDITS_JSON = HERE / "ref" / "ep31" / "credits.json"
ASSETS_JSON = HERE / "ref" / "ep31" / "assets.json"
CLIPS = HERE / "ref" / "ep31" / "clips.json"
OUT = HERE / "config" / "meta_ep31.json"

N_GLOSS = 9           # `ref/ep31/yougo.md` の「貼る本文」の語数
# ⚠️ ⑥（11-09）の配線から数えた点数（変わったら止まる＝文の点数を当て直す）。None＝数えて出すだけ
N_COUNTS = {"own": 7, "sat": 10, "stock": 46, "gsi": 5, "mod_still": 7, "sdasm": 1, "cc0": 3, "gov": 11, "kokkai": 11,
            "mod_clips": 2, "mod_cuts": 15}

# ✅ 承認①（11-08 カズヤくん「推奨どおり」）の題 A のまま（台本 第2版 §1-1・76字）。
#    【映像あり】＝防衛庁記録（CC BY 3.0）の動く映像 15カット（器は 1920×1080・実効は 640px 前後＝materials.md §0）
TITLE = ("【映像あり】全日空機雫石衝突事故の真相。その朝の訓練の空は、旅客機の道が載っていない地図の上で、"
         "幹部が指で示して決めていた。【事故検証】【ゆっくり解説】")
TITLE_LEN = 76        # 決めた題の字数（写し間違いの網）

# ⚠️ 本文（台本第2版 c101〜c107）で言っていることだけを書く
HEAD = """【この動画について】
1971年7月30日の午後、岩手県雫石町の上空で、全日空の旅客機と、航空自衛隊の戦闘機がぶつかりました。ぶつかった高さは、およそ8,500メートル。旅客機は地上へ落ち、乗っていた162人は、全員が亡くなりました。

旅客機は、北海道の千歳から羽田へ向かっていた全日空のボーイング727。戦闘機は、宮城県の松島基地を飛び立ったF-86Fの2機で、教官と訓練生が1機ずつ乗る、編隊の訓練でした。最高裁の判決は、その日の訓練の空は、旅客機の通り道が載っていない地図の上で、部隊の幹部が指で示して決めていた、と書いています。

刑事の裁判は、教官と訓練生の2人を被告として始まりました。最高裁は、幹部の計画に従った教官ひとりに、刑事責任をすべて負わせ、禁錮4年の実刑にするのは、事故の重大さを考えても「なお酷に過ぎる」と書きました。
訓練の空は、どう決まったのか。旅客機から、訓練機は見えていたのか。そして、刑事の責任は、なぜ教官に向かったのか。最高裁の判決、国会の会議録、運輸白書をもとに、順にたどります。
"""

# 🔴 cc15・cc16 の語り「出典を示せば使ってよい、という決まりで公開」「置き場は、説明欄に書く」＝11-09 に開けることを確かめたアドレス
WINDOW = """【資料の置き場】
・最高裁判所 第一小法廷 判決（1983年9月22日・裁判所ウェブサイト）　https://www.courts.go.jp/assets/hanrei/hanrei-pdf-58088.pdf
・運輸省『昭和47年度 運輸白書』航空 第2章 第6節（国土交通省の頁）　https://www.mlit.go.jp/hakusyo/transport/shouwa47/ind100206/001.html　https://www.mlit.go.jp/hakusyo/transport/shouwa47/ind100206/002.html
・国会会議録検索システム（国立国会図書館）　https://kokkai.ndl.go.jp/
・防衛省・自衛隊『昭和46年防衛庁記録』（防衛省・自衛隊の公式の動画・CC BY 3.0）　https://www.youtube.com/watch?v=HK0v9n-PTIM
"""

# 台本第2版の出典の欄の略（判・国・白・法・記・町・会）と `ref/ep31/sources.md` から
PRIMARY = """【出典】
・最高裁判所 第一小法廷 判決（1983年9月22日）
・国会会議録（衆議院・参議院の委員会の発言）
・運輸省『昭和47年度 運輸白書』（国土交通省の頁）
・衆議院の頁「法律第五十八号（昭和50年7月10日）」（航空法の改正）・e-Gov 法令検索（航空法 第71条の2）
・国土交通省 記者発表（2002年9月4日）
・雫石町の頁（2019年11月22日・2020年7月31日の記事）
・全日空の頁（ANAグループ安全教育センター）
・防衛省・自衛隊『昭和46年防衛庁記録』（映像）
・国土地理院 地理院タイル（空中写真）
"""

# ⚠️ ⑥ の頭（11-09）に頁を取り直して当て直した（ref/ep31/sources.md §8）。公開の直前にもう一度当てて RECHECK を直す
RECHECK = "11月9日"
TAIL = f"""動画に出てくる数字と日付は、最高裁の判決、国会の会議録、運輸白書、国と町と会社の頁によります（公開前の{RECHECK}に、町と会社と国の頁を見直しました）。
※ 事故の調査報告書の本文と、一審・二審・民事の判決の原文は、この動画では読めていません。報告書は運輸白書と国会での読み上げから、裁判は最高裁の判決と国会の発言から、お伝えしています。
※ 時速は、その高さの標準の気温（国際標準大気）として計算した目安です。
※ 報道によると、事故から55年の2026年7月30日にも、森のしずく公園で献花が行われました（動画では、町の頁にある2020年の献花までをお伝えしています）。
※ 亡くなった方、ご遺族、裁判の関係者のお名前は出していません（立場でお伝えしています）。
※ 画面の模式図と地図の線は、公の記録をもとに描いた図です。防衛庁記録の映像は、音を使っていません。"""

# ✅ 11-09 カズヤくん「文字縁は今回は赤で決定」・上の行＝「C3 乗員乗客162人／生存者なし」・機体は字の後ろ
#    → 地＝「当時の写真の質感を再現するように、白黒で作成」「生成AIで作り直し。構成も再考」→「案① 下から見上げる」→「もっと荒い質感に編集」→「r2 荒い」
#    ＝`qa_out/ep31_thumb_hx.py final`（地＝生成 AI `tools/gen_thumb_ai.py szk_c`＋荒さ `qa_out/ep31_thumb_bw.py c` の r2）
THUMB = "out/thumb/ep31/ep31_Hinv_C3cr2.png"
THUMB_MD5 = "2888ccecd57ef282a3d738d0fe8ba409"
# 🔧 11-09：1回目の「機体の色と形は…同じ型をもとに」は誤り（塗装はわざと実際と違う＝社名と印を描かせていない）→ 形だけ・位置と向きは記録で確かめていない
#    🔧 白黒の当時の写真に似せた地＝本物の写真と取り違えられやすい＝「似せて加工」を足した
THUMB_NOTE = ("※ サムネイルの絵は、生成AIで作り、当時の白黒写真に似せて加工した再現のイメージです（実際の写真ではありません。"
              "2機の形は同じ型をもとにしていますが、塗装と、2機の位置と向きは、記録で確かめたものではありません）。")

TAGS = ["全日空機雫石衝突事故", "雫石事故", "全日空", "航空自衛隊", "F-86F", "ボーイング727", "空中衝突", "航空事故",
        "1971年", "岩手県", "雫石町", "最高裁判決", "訓練空域", "事故検証", "ゆっくり解説", "解説"]

LIC_URL = {"CC BY 2.0": "https://creativecommons.org/licenses/by/2.0/deed.ja",
           "CC BY 2.5": "https://creativecommons.org/licenses/by/2.5/deed.ja",
           "CC BY 3.0": "https://creativecommons.org/licenses/by/3.0/deed.ja",
           "CC BY 4.0": "https://creativecommons.org/licenses/by/4.0/deed.ja",
           "CC BY-SA 2.0": "https://creativecommons.org/licenses/by-sa/2.0/deed.ja",
           "CC BY-SA 3.0": "https://creativecommons.org/licenses/by-sa/3.0/deed.ja",
           "CC BY-SA 4.0": "https://creativecommons.org/licenses/by-sa/4.0/deed.ja",
           "CC0": "https://creativecommons.org/publicdomain/zero/1.0/deed.ja"}
GSI_URL = "https://www.gsi.go.jp/kikakuchousei/kikakuchousei40182.html"


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
    """`ref/ep31/yougo.md` の「## 貼る本文」の節を**そのまま**返す（次の `---` か `## ` まで）。見出しの語が語りに出るかを当てる。"""
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
    """SPEC の値を辿って、素材の道（`ep31/…`）を全部出す（地に敷く写真も含む）。"""
    if isinstance(v, str):
        if v.startswith("ep31/"):
            yield v
    elif isinstance(v, dict):
        for x in v.values():
            yield from _walk(x)
    elif isinstance(v, (list, tuple)):
        for x in v:
            yield from _walk(x)


_D = r"\d{4}年\d+月\d+日"
# 画面の出典表記（credits.json の値＝作者は印 {作者} のまま）→ 種類（名乗れないものは None）。⚠️ 並びに意味がある（上から当てる）
KINDS = [
    ("mod_still", r"^出典：防衛省・自衛隊『昭和46年防衛庁記録』（CC BY 3\.0）／改変：切出$"),
    ("kokkai", r"^出典：国会会議録（" + _D + r" (?:衆議院|参議院) (?:決算委員会|内閣委員会|連合審査会)）／改変：切出(?:・名前を隠した)?$"),
    ("gov", r"^出典：(?:運輸省『昭和47年度 運輸白書』（国土交通省の頁）|最高裁判所 第一小法廷 判決（" + _D + r"）"
            r"|衆議院「法律第五十八号（昭和50年7月10日）」|国土交通省 記者発表（" + _D + r"）)／改変：切出(?:・記号を隠した)?$"),
    ("gsi", r"^出典：国土地理院ウェブサイト（地理院タイル・(?:空中写真 1974〜1978年|シームレス空中写真)）・加工して作成$"),
    ("own", r"^写真：\{作者\}／Wikimedia Commons（CC BY(?:-SA)? (?:[234]\.0|2\.5)）／改変なし$"),
    ("cc0", r"^写真：\{作者\}／Wikimedia Commons（CC0）$"),
    ("sdasm", r"^写真：SDASM Archives（著作権の制限は知られていない）$"),
    ("sat", r"^地図：Google マップの衛星写真（帰属は地図の右下）$"),
    ("stock", r"^イメージ（Pexels）$"),
]
# 映像（clips.json の credit）→ 種類。⚠️ 等速で止めなしのカットは画面で「再生速度」を言わない（footage.credit_of）＝表の元の字で当てる
FILM_KINDS = [("mod", r"^(?:出典：)?防衛省・自衛隊『昭和46年防衛庁記録』（CC BY 3\.0）・改変：切出")]


def _kind(s: str):
    for k, pat in KINDS:
        if re.match(pat, s):
            return k
    return None


def _film_kind(s: str):
    for k, pat in FILM_KINDS:
        if re.match(pat, s or ""):
            return k
    return None


def used_material():
    """章ファイルの実配線から、写真・頁・衛星写真・映像を数える。権利は画面の出典表記で照らす。"""
    import cuts
    import cuts.ss as SS
    import footage as F
    cred = json.loads(CREDITS_JSON.read_text(encoding="utf-8"))
    for v in SS.SAT.values():                 # 衛星写真＝出典は表 SAT の credit（ep25_meta と同じ）
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
    films = OrderedDict()
    for cid, u in F.USE.items():
        c = clips.get(u["clip"])
        if c is None:
            bad.append(f"{cid}:{u['clip']}（clips.json に無い）")
            continue
        k = _film_kind(c.get("credit", ""))
        if k is None:
            bad.append(f"{cid}:{u['clip']}（名乗れない映像の出典：{c.get('credit')}）")
            continue
        films.setdefault(k, OrderedDict()).setdefault(u["clip"], []).append(cid)
    if bad:
        raise SystemExit(f"🔴 名乗れない素材がある。書かずに止めた: {bad}")
    counts = {k: len(v) for k, v in got.items()}
    counts.update({f"{k}_clips": len(v) for k, v in films.items()})
    counts.update({f"{k}_cuts": sum(len(x) for x in v.values()) for k, v in films.items()})
    print(f"■ 素材（配線から）：{counts}")
    if N_COUNTS is not None and counts != N_COUNTS:
        raise SystemExit(f"🔴 点数が⑥で数えた値 {N_COUNTS} と違う。文の点数を当て直すこと。書かずに止めた。")
    return got, counts


def read_credits() -> str:
    got, n = used_material()
    assets = json.loads(ASSETS_JSON.read_text(encoding="utf-8"))
    out = ["【写真・映像】"]
    out.append(f"・映像＝防衛省・自衛隊『昭和46年防衛庁記録』（CC BY 3.0）{n.get('mod_cuts', 0)}カット＋同じ記録の静止画 {n.get('mod_still', 0)}点"
               f"（切り出し・一部は再生の速さを変えています）　{LIC_URL['CC BY 3.0']}")
    out.append(f"・国会会議録の紙面 {n.get('kokkai', 0)}点、最高裁の判決・運輸白書・衆議院の頁・国土交通省の記者発表の画面 {n.get('gov', 0)}点"
               "（出典は画面に表示・人の名前と判決の記号を隠しています）")
    # 個人名義（Commons）＝作者・ライセンスごとにまとめる（名前は git の外の表から＝焼く道と同じ）
    by = OrderedDict()
    for k in ("own", "cc0"):
        for p, (cid, s) in (got.get(k) or {}).items():
            st = Path(p).stem
            a = assets.get(st) or {}
            lic = "CC0" if k == "cc0" else re.search(r"（(CC BY(?:-SA)? (?:[234]\.0|2\.5))）", s).group(1)
            if a.get("lic") != lic:
                raise SystemExit(f"🔴 {st} のライセンスが台帳（{a.get('lic')}）と画面（{lic}）で違う。書かずに止めた。")
            by.setdefault((S._ep31_person(p, "{作者}"), lic), []).append(p)
    nc = sum(len(v) for v in by.values())
    out.append(f"・Wikimedia Commons の写真 {nc}点（加工なし・写真ごとの作者とライセンスは画面の出典の行にも）")
    for (who, lic), ps in by.items():
        out.append(f"　{who}（{lic}）" + (f"{len(ps)}点" if len(ps) > 1 else ""))
    used_lic = sorted({lic for (_, lic) in by if lic in LIC_URL})
    out.append("　ライセンス：" + "　".join(f"{lic} {LIC_URL[lic]}" for lic in used_lic))
    if n.get("sdasm"):
        out.append(f"・SDASM Archives の写真 {n['sdasm']}点（Flickr の The Commons・著作権の制限は知られていない）")
    out.append(f"・国土地理院の空中写真 {n.get('gsi', 0)}点（地理院タイル・加工して作成）＝国土地理院コンテンツ利用規約　{GSI_URL}")
    if n.get("sat"):
        out.append(f"・地図の衛星写真 {n['sat']}点＝Google マップ（帰属は地図の右下）")
    out.append(f"※ 画面に「イメージ」と出る写真（{n.get('stock', 0)}点）は、フリー素材（Pexels）です。その日・その場を写したものではありません")
    out.append("※ 国の機関（裁判所・国会・国土交通省・防衛省・国土地理院）・雫石町・全日空の資料を使っていますが、"
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
    desc = "\n".join([HEAD, WINDOW, chapters(), "", read_glossary(), "", PRIMARY, read_credits(), "", tail])
    # 🔴 入れてはいけない語（BGM のクレジット・ゆっくりの一文・煽り語・印の残り）
    for bad in ("<", ">", "BGM", "DOVA", "OpenTracks", "ゆっくりボイス", "AquesTalk", "即死", "絶命", "地獄",
                "【映像あり】", "{作者}", "{個人}", S.EP23_AUTHOR_STANDIN):
        if bad in desc:
            raise SystemExit(f"🔴 入れてはいけない語「{bad}」が説明に入っている。書かずに止めた。")
    # 🔴 この回の線＝「死亡」を使わない・「無罪」と判決の記号の字を書かない・「犯人」と言わない
    for bad in ("死亡", "無罪", "犯人", "三佐", "一尉"):
        if bad in TITLE or bad in desc:
            raise SystemExit(f"🔴 「{bad}」が入っている。書かずに止めた。")
    for need in ("hanrei-pdf-58088", "kokkai.ndl.go.jp", "hakusyo", "HK0v9n-PTIM", "読めていません", "CC BY 3.0"):
        if need not in desc:
            raise SystemExit(f"🔴「{need}」が無い（cc15・cc16・cc17 の語りの約束）。書かずに止めた。")
    if not TITLE.endswith("【事故検証】【ゆっくり解説】"):
        raise SystemExit("🔴 タイトルの末尾が「【事故検証】【ゆっくり解説】」でない（事故の回の決まり）。書かずに止めた。")
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
    meta = {"slug": "ep31", "title": TITLE, "description": desc, "tags": TAGS, "thumbnail": THUMB,
            "genre": "jiko", "playlist": ""}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✓ 書いた → {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
