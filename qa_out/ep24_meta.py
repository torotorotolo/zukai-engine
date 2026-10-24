# -*- coding: utf-8 -*-
"""24本目（チェルノブイリ原発事故）の `config/meta_ep24.json` を**機械で**組み立てる（2026-10-24・⑥）。

`qa_out/ep17_meta.py`（用語・目次・点数・権利・字数の網）を写して、この回の形に合わせた。

🔴 手で書かない理由（ep7〜ep17 と同じ）
  ① 用語は `ref/ep24/yougo.md` の「## 貼る本文」の節が正本＝**そのまま**貼る（`**` だけ外す）。
     見出しの語が語り（`narration.SCRIPT`）に出るかと、並びが語りに初めて出る順かを1語ずつ当てる
  ② 素材の点数は**章ファイルの実配線**（`cuts.SPEC` の写真と頁／`footage.USE` の映像）から数え、
     権利は**画面の出典表記**（`ref/ep24/credits.json`・`clips.json`）で照らす。名乗れない素材が出たら落ちる
  ③ 目次は `scene_jiko.CUTS` の秒を頭から積む＝**焼いた版と同じ秒**（章の扉の秒は CUTS に入っている）
  ④ タイトル 100字・説明 5,000字の上限と、入れてはいけない語を、書く前に確かめる

🔴 この回のところ
  - 個人名義の写真（Wikimedia Commons）の作者の名前は**公開リポに書かない**＝焼くときと同じく git の外の表
    `ref/ep24/src/credits_private.tsv` から `scene_jiko._ep24_author`（名乗りの短い形）で足す（`config/` は gitignore＝説明の JSON は公開リポに入らない）
  - Commons の頁は番号の URL（`qa_out/ep24_commons_pageids.json`＝`qa_out/ep24_commons_pageids.py` が API で引いた）
  - IAEA Imagebank の写真39点は1点ずつ並べると5,000字に入らない・全点が入るチェルノブイリの分類も無い（API で照らした）
    ＝Commons の題名の番号（IAEA 027900NN・0271NNNN）を短く並べる
  - 報告書と会議録の頁＝引用（著作権法32条）。フリー素材の映像（Pexels）は「イメージ」の断りだけ（クレジットは書かない＝決め）
  - 語りの名前は記録にある5人だけ。【映像あり】は付けない（1986年の事故の動く記録映像は0本）

    python qa_out/ep24_meta.py            # 組み立てて config/meta_ep24.json に書く
    python qa_out/ep24_meta.py --dry      # 書かずに中身と字数だけ出す
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

YOUGO = HERE / "ref" / "ep24" / "yougo.md"
CREDITS_JSON = HERE / "ref" / "ep24" / "credits.json"
ASSETS_JSON = HERE / "ref" / "ep24" / "assets.json"
CLIPS = HERE / "ref" / "ep24" / "clips.json"
PAGEIDS = HERE / "qa_out" / "ep24_commons_pageids.json"
OUT = HERE / "config" / "meta_ep24.json"

N_GLOSS = 21          # `ref/ep24/yougo.md` の「貼る本文」の語数（台本 §8 の21語を語りの言い方にそろえた）
# ⚠️ 下の値は⑥（10-24）本編 r01（版 f9dafa53）の配線から数えた点数（変わったら止まる＝文の点数を当て直す）
N_COUNTS = {"iaea": 39, "own": 29, "cpd": 3, "cc0": 5, "nl": 1, "nasa": 1, "usgs": 6, "cia": 1, "page": 24,
            "stock_film": 6}

# ✅ 承認①（10-22）は題 C。⑥（10-24）「頭に事件の語」の型と割れていることを伝えたうえで、カズヤくん「C 承認①のまま」
TITLE = "「原因は運転員」とした報告書は、6年後に書き直された。チェルノブイリ原発事故の真相【事故検証】【ゆっくり解説】"
TITLE_LEN = 55        # 決めた題の字数（写し間違いの網）

# ⚠️ 本文（台本第2版 c101〜c107）で言っていることだけを書く
HEAD = """【この動画について】
1986年5月3日、東京と千葉と神奈川で、空気中のちりや雨水から、放射性のヨウ素131が見つかりました。出どころは、遠いソ連（いまのウクライナ）の原子力発電所。その1週間前の4月26日、チェルノブイリ原子力発電所の4号炉が、爆発で壊れていました。

その年の9月、国際原子力機関の専門家グループは、運転員の誤りと規則違反が炉の性質と重なって起きた、根本の原因は「人的要素」にある、とまとめました。ところが6年後の1992年、同じグループは報告を書き直します。「違反とされた行為のいくつかは、実は違反ではなかった」。止める棒の形にも欠陥があり、1991年のソ連の委員会によれば、それは事故の2年半ほど前の起動の試験で見つかっていました。

それでも、書き直した報告も、運転員の決定的な操作は、きわめて判断を誤っていた、と書いています。この動画は、新旧の報告を、事故の夜の時刻に沿って見比べます。
"""

# 台本第2版 §10（資料）と ①の取得記録（`ref/ep24/src/fetch_log.tsv`）から。⑥（10-24）URL は curl で 200 を確かめる
PRIMARY = """【出典】
・IAEA『INSAG-7 The Chernobyl Accident: Updating of INSAG-1』（1992年・付属書I＝1991年の委員会の報告）　https://www-pub.iaea.org/MTCD/Publications/PDF/Pub913e_web.pdf
・IAEA GC(SPL.I)/3（1986年9月24日・INSAG-1 の本文）　https://www.iaea.org/sites/default/files/gc/gc-spl1-3.pdf
・ソ連の報告 Part I（1986年8月・事故後検討会議の資料・PDF の3頁目から）　https://www.iaea.org/sites/default/files/gc/gc29inf-232-corr1_en.pdf
・チェルノブイリ・フォーラム『Chernobyl's Legacy』（2006年）　https://www.iaea.org/sites/default/files/chernobyl.pdf
・UNSCEAR（国連の科学委員会）1988年報告 付属書G・2000年報告 付属書J・2008年報告 付属書D（訂正版）・白書（2018年・甲状腺がん）　https://www.unscear.org/unscear/en/publications/
・国際がん研究機関（IARC）の説明資料（2006年）　https://www.iarc.who.int/wp-content/uploads/2018/07/IARCBriefingChernobyl.pdf
・INES User's Manual（2008年版）　https://www-pub.iaea.org/MTCD/Publications/PDF/INES2013web.pdf
・国会会議録（1986年5月7日 参議院 科学技術特別委員会・5月8日 衆議院 農林水産委員会・5月15日 参議院 内閣委員会・11月27日 衆議院 科学技術委員会）　https://kokkai.ndl.go.jp/
・USGS（Landsat の衛星写真と報告）　https://www.usgs.gov/media/images/landsat-chernobyl
・外務省 報道発表（2022年3月31日）・外交青書2022、チェルノブイリ原子力発電所（事業者）、欧州復興開発銀行（EBRD）、内閣府 防災白書（平成23年版）、国連ニュース（2025年2月14日）、NucNet（2025年12月8日）"""

TAIL = """動画に出てくる数値・時刻・言葉は、これらの記録によります。
報告によって答えが分かれるところは、どの報告の言い分かを、画面と語りで断っています。
※ 報告の色分け（図と札）：1986年の報告＝桃・1986年8月のソ連の報告＝橙・1991年の委員会＝紫・1992年の報告＝青
※ 画面の模式図・再現のイラスト・地図は、記録をもとに描いた図です。
※ 語りに出る名前は、記録にある5人（役職つき）だけです。運転員・消防士・作業員・住民のお名前は出していません。
※ 同じ型の炉（レニングラード・クルスク・イグナリナ）の写真は、事故の炉ではありません（画面の副題で断っています）。"""

# ✅ ⑥（10-24）カズヤくん：生成 AI 案A＋案B（gen_thumb_ai chn_a・chn_b）→「案A明るさ1.6をA、案B明るさ1.3をBサムネとして設定します。
#    サムネBの設定は私が手動でやる」＝**A＝事故の夜の4号炉（字の外の明るさ 1.60）**（上げるときに貼る）・
#    B＝数日後の昼のヘリ（`out/thumb/ep24-ab/ep24_B_Hinv_ai_b_b130.png`・md5 b3194d29…＝カズヤくんが Studio の「テストと比較」で入れる）
THUMB = "out/thumb/ep24-ab/ep24_A_Hinv_ai_a_b160.png"
THUMB_MD5 = "f93f733f47283f786a5e8aa22ba04e39"
THUMB_NOTE = "※ サムネイルの絵は、生成AIで作った再現のイメージです（実際の写真ではありません）。"
# ⚠️ ⑥（10-24）個人名義の写真29点の頁の URL を1点ずつ並べると、説明が 6,700字（上限 5,000）＝URL は外し、作者・ライセンス・点数を残す
#    （写真ごとの作者とライセンスは画面の出典の行にも出す）。True で17本目の形（作者ごとに頁の番号の URL）
OWN_URLS = False

TAGS = ["チェルノブイリ", "チェルノブイリ原発事故", "チョルノービリ", "原発事故", "1986年", "RBMK", "4号炉", "INSAG",
        "国際原子力機関", "事故検証", "一次資料", "ゆっくり解説", "ドキュメンタリー", "解説", "原子力"]

LIC_URL = {"CC BY 2.0": "https://creativecommons.org/licenses/by/2.0/deed.ja",
           "CC BY 3.0": "https://creativecommons.org/licenses/by/3.0/deed.ja",
           "CC BY-SA 2.0": "https://creativecommons.org/licenses/by-sa/2.0/deed.ja",
           "CC BY-SA 3.0": "https://creativecommons.org/licenses/by-sa/3.0/deed.ja",
           "CC BY-SA 4.0": "https://creativecommons.org/licenses/by-sa/4.0/deed.ja"}


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
    """`ref/ep24/yougo.md` の「## 貼る本文」の節を**そのまま**返す（次の `---` か `## ` まで）。見出しの語が語りに出るかを当てる。"""
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
    """SPEC の値を辿って、素材の道（`ep24/…`）を全部出す（尻・頭の差し込み・地に敷く写真も含む）。"""
    if isinstance(v, str):
        if v.startswith("ep24/"):
            yield v
    elif isinstance(v, dict):
        for x in v.values():
            yield from _walk(x)
    elif isinstance(v, (list, tuple)):
        for x in v:
            yield from _walk(x)


# 画面の出典表記（credits.json の値＝作者は印 {作者} のまま）→ 種類（名乗れないものは None）。⚠️ 並びに意味がある（上から当てる）
KINDS = [
    ("iaea", r"^写真：IAEA Imagebank(／Photo: USFCRFC)?（CC BY-SA 2\.0）・改変なし$"),
    ("own", r"^写真：(RIA Novosti archive／)?\{作者\}（CC BY(-SA)? [234]\.0）・改変(なし|：切出)$"),
    ("cpd", r"^写真：Wikimedia Commons（パブリックドメイン）$"),
    ("cc0", r"^写真：Wikimedia Commons（CC0）(・改変：切出)?$"),
    ("nl", r"^写真：オランダ国立公文書館（CC0）$"),
    ("nasa", r"^写真：NASA（パブリックドメイン）$"),
    ("usgs", r"^写真：USGS( EarthExplorer（アメリカの偵察衛星）)?（パブリックドメイン）(・改変：切出)?$"),
    ("cia", r"^出典：CIA（パブリックドメイン）$"),
    ("page", r"^出典：(INSAG-7|GC\(SPL\.I\)/3|ソ連の報告 Part I|国会会議録 1986-|チェルノブイリ・フォーラム)"),
]


def _kind(s: str):
    for k, pat in KINDS:
        if re.match(pat, s):
            return k
    return None


def used_material():
    """章ファイルの実配線から、写真・頁・映像を数える。権利は画面の出典表記で照らす。"""
    import cuts
    import footage as F
    cred = json.loads(CREDITS_JSON.read_text(encoding="utf-8"))
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


def _iaea_numbers(paths):
    """IAEA Imagebank の写真の Commons の題名の番号（例 IAEA_02790015_(…)＝02790015）を短く並べる。"""
    a = json.loads(ASSETS_JSON.read_text(encoding="utf-8"))
    s279, other, ctrl = [], [], 0
    for p in paths:
        u = a[Path(p).stem]["url"]
        m = re.search(r"IAEA_027900(\d\d)_", u)
        n = re.search(r"\((0271\d{4})\)\.jpg$", u)
        if m:
            s279.append(m.group(1))
        elif n:
            other.append(n.group(1))
        elif "Control_Room_of_Chernobyl_Nuclear_Power_Plant_Unit_3" in u:
            ctrl += 1
        else:
            raise SystemExit(f"🔴 IAEA の写真の題名の形が分からない: {u}。書かずに止めた。")
    return sorted(s279), sorted(other), ctrl


def read_credits() -> str:
    got, n = used_material()
    pid = json.loads(PAGEIDS.read_text(encoding="utf-8"))["pages"]
    out = ["【写真・図・頁・映像】"]
    s279, other, ctrl = _iaea_numbers(list((got.get("iaea") or {}).keys()))
    if len(s279) + len(other) + ctrl != n["iaea"]:
        raise SystemExit("🔴 IAEA の写真の数が合わない。書かずに止めた。")
    out.append(f"・IAEA Imagebank の写真 {n['iaea']}点（CC BY-SA 2.0・加工なし・額に入れて表示）＝Wikimedia Commons の題名の番号"
               f"「IAEA 027900」＋{'・'.join(s279)}（{len(s279)}点・Photo: USFCRFC）と、{'・'.join(other)}"
               + (f"・3号機の制御室（{len(other) + ctrl}点）" if ctrl else f"（{len(other)}点）"))
    # 個人名義（Commons）＝作者・ライセンス・改変ごとにまとめる（名前は git の外の表から＝焼く道と同じ）
    by = OrderedDict()
    for p, (cid, s) in (got.get("own") or {}).items():
        lic = re.search(r"（(CC BY(?:-SA)? [234]\.0)）", s).group(1)
        how = "加工なし・額に入れて表示" if "改変なし" in s else "切り出し"
        st = Path(p).stem
        if st not in pid or lic not in LIC_URL:
            raise SystemExit(f"🔴 {st} の Commons の頁かライセンスの URL が無い。書かずに止めた。")
        if pid[st]["license"] != lic:
            raise SystemExit(f"🔴 {st} のライセンスが台帳（{pid[st]['license']}）と画面（{lic}）で違う。書かずに止めた。")
        who = ("RIA Novosti archive／" if "RIA Novosti" in s else "") + S._ep24_author(p)    # 画面の出典の行と同じ順
        by.setdefault((who, lic, how), []).append(pid[st]["url"])
    if OWN_URLS:
        out.append(f"・Wikimedia Commons の写真 {n['own']}点（作者・ライセンス・頁）")
        for (who, lic, how), urls in by.items():
            out.append(f"　{who}（{lic}・{how}）{len(urls)}点　" + "　".join(urls) if len(urls) > 1
                       else f"　{who}（{lic}・{how}）　{urls[0]}")
    else:
        out.append(f"・Wikimedia Commons の写真 {n['own']}点（作者・ライセンス・点数＝CC BY-SA は加工なし・額に入れて表示／"
                   "CC BY は切り出し・写真ごとの作者とライセンスは画面の出典の行にも）")
        for (who, lic, how), urls in by.items():
            out.append(f"　{who}（{lic}）" + (f"{len(urls)}点" if len(urls) > 1 else ""))
    used_lic = sorted({lic for (_, lic, _) in by} | {"CC BY-SA 2.0"})
    out.append("　ライセンス：" + "　".join(f"{lic} {LIC_URL[lic]}" for lic in used_lic))
    pd = n.get("cpd", 0) + n.get("cc0", 0) + n.get("nl", 0) + n.get("nasa", 0)
    out.append(f"・パブリックドメインと CC0 の写真 {pd}点（Wikimedia Commons・NASA・オランダ国立公文書館）")
    out.append(f"・衛星写真 {n.get('usgs', 0)}点＝USGS（Landsat 5・アメリカの偵察衛星の写真〈EarthExplorer〉・パブリックドメイン）")
    out.append(f"・地図 {n.get('cia', 0)}点＝CIA（パブリックドメイン）")
    out.append(f"・報告書と会議録の頁 {n.get('page', 0)}枚＝引用（著作権法32条・資料名は画面の出典の行）")
    out.append("※ 画面に「イメージ」と出る映像は、フリー素材です。その日・その場を写したものではありません")
    out.append("※ 国際原子力機関（IAEA）・国連の機関・各国の政府の資料を使っていますが、これらの機関がこの動画を作ったり、"
               "推奨・支持したりしているものではありません")
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
    p = HERE / THUMB if THUMB else None
    if not p or not p.exists() or hashlib.md5(p.read_bytes()).hexdigest() != THUMB_MD5:
        raise SystemExit(f"🔴 サムネが無いか、⑥で決めた物と違う: {THUMB or '（未定）'}。書かずに止めた。")
    meta = {"slug": "ep24", "title": TITLE, "description": desc, "tags": TAGS, "thumbnail": THUMB,
            "genre": "jiko", "playlist": ""}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✓ 書いた → {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
