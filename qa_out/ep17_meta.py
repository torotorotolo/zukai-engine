# -*- coding: utf-8 -*-
"""17本目（中華航空140便墜落事故）の `config/meta_ep17.json` を**機械で**組み立てる（2026-10-21・⑥）。

`qa_out/ep23_meta.py`（用語・目次・字数の網）と `qa_out/ep20_meta.py`（Commons の頁を番号の URL で）を写して、この回の形に合わせた。

🔴 手で書かない理由（ep7〜ep23 と同じ）
  ① 用語は `ref/ep17/yougo.md` の「## 貼る本文」の節が正本＝**そのまま**貼る（`**` だけ外す）。
     見出しの語が語り（`narration.SCRIPT`）に出るかと、並びが語りに初めて出る順かを1語ずつ当てる
  ② 素材の点数は**章ファイルの実配線**（`cuts.SPEC` の写真／`footage.USE` の映像／`cuts.ss.SAT` の衛星写真と空中写真）から数え、
     権利は**画面の出典表記**（`ref/ep17/credits.json`・`clips.json`・`ss.SAT`）で照らす。名乗れない素材が出たら落ちる
  ③ 目次は `scene_jiko.CUTS` の秒を頭から積む＝**焼いた版と同じ秒**（章の扉の秒は CUTS に入っている）
  ④ タイトル 100字・説明 5,000字の上限と、入れてはいけない語を、書く前に確かめる

🔴 この回のところ
  - 個人名義の写真（Wikimedia Commons）の作者の名前は**公開リポに書かない**＝焼くときと同じく git の外の表
    `ref/ep17/src/credits_private.tsv` から `scene_jiko._ep17_author`（HTML を外した字）で足す（`config/` は gitignore＝説明の JSON は公開リポに入らない）
  - Commons の頁は番号の URL（`qa_out/ep17_commons_pageids.json`＝`qa_out/ep17_commons_pageids.py` が API で1回引いた）
  - 乗員の実名は出さない（09-26 カズヤくん）＝🔴 commit の前に名前の網（作者の表の artist・credit の列）
  - 【映像あり】は付けない（10-13 の新しい題の型＝承認①の題 A に無い）

    python qa_out/ep17_meta.py            # 組み立てて config/meta_ep17.json に書く
    python qa_out/ep17_meta.py --dry      # 書かずに中身と字数だけ出す
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

YOUGO = HERE / "ref" / "ep17" / "yougo.md"
CREDITS_JSON = HERE / "ref" / "ep17" / "credits.json"
ASSETS_JSON = HERE / "ref" / "ep17" / "assets.json"
CLIPS = HERE / "ref" / "ep17" / "clips.json"
PAGEIDS = HERE / "qa_out" / "ep17_commons_pageids.json"
OUT = HERE / "config" / "meta_ep17.json"

N_GLOSS = 18          # `ref/ep17/yougo.md` の「貼る本文」の語数（台本 §8 の下書きを語りに当てて18語）
# ⚠️ 下の値は⑥（10-21）本編 r01（版 a39d6577）の配線から数えた点数（変わったら止まる＝文の点数を当て直す）
N_COUNTS = {"rphoto": 26, "own": 14, "rfig": 10, "sat": 5, "stock": 4, "cc0": 8, "faa": 3, "gsi": 1, "hel": 1, "rpage": 1,
            "loc": 1, "court": 2, "film": 3, "stock_film": 8}

# ✅ 承認①（10-19）は題 A。⑥（10-21）「頭に事件の語」の型と割れていることを伝えたうえで、カズヤくん「A 承認①のまま」
TITLE = ("名古屋空港へ降りようとする機体で、自動操縦は「着陸やり直し」のモードだった。"
         "中華航空140便墜落事故の真相【事故検証】【ゆっくり解説】")
TITLE_LEN = 67        # 決めた題の字数（写し間違いの網）

# ⚠️ 本文（台本第2版 c101〜c109）で言っていることだけを書く
HEAD = """【この動画について】
1994年4月26日の夜、台北から来た中華航空140便が、名古屋空港に着陸しようとして墜落しました。264人が亡くなりました。

この事故は「コンピュータが、パイロットの操縦に抵抗した」と紹介されることがあります。けれど、事故の報告書が選んだ言葉は「抵抗」ではありません。人は機首を下げようと押し、自動操縦は尾翼の板で機首を上げようとしました。押す操縦と自動操縦が、約30秒、「相反」したのです。

報告書は、操縦席の画面の上の端に、1分以上「ゴー・アラウンド」（着陸をやめて、上昇してやり直す飛び方）の文字が出ていた、と推定しています。けれど操縦席の2人は、着陸を続けようとしていました。

この動画は、事故の報告書と、のちの裁判の判決、アメリカの連邦航空局（FAA）の調査などをもとに、次の3つの問いをたどります。

・画面の文字の意味は、なぜ伝わらなかったのか
・機体は、なぜ立て直せなかったのか
・そして、事故は、なぜ前もって防げなかったのか

時刻は日本の時刻です。高さ・速さ・重さは、記録のフィート・ノット・ポンドを、メートル法に直しています。
"""

# 台本第2版 §10（出典一覧）から。⑥（10-21）URL は curl で 200 を確かめた
PRIMARY = """【出典】
・運輸省 航空事故調査委員会『航空事故調査報告書 96-5 中華航空公司所属 エアバス・インダストリー式A300B4-622R型B1816 名古屋空港 平成6年4月26日』（1996年7月15日）　https://jtsb.mlit.go.jp/jtsb/aircraft/detail.php?id=851
・名古屋地方裁判所 平成15年（2003年）12月26日判決（平成7年(ワ)第4179号）　https://www.courts.go.jp/hanrei/7587/detail4/index.html
・FAA Human Factors Team "The Interfaces Between Flightcrews and Modern Flight Deck Systems"（1996年6月18日）　https://www.faa.gov/sites/faa.gov/files/2022-11/interfac.pdf
・NTSB Safety Recommendation A-94-164 through -166（1994年8月31日）　https://www.ntsb.gov/safety/safety-recs/recletters/A94_164_166.pdf
・Federal Register 1994年10月18日（耐空性改善命令 AD 94-21-07）"""

TAIL = """動画に出てくる数値・時刻・言葉は、これらの記録によります。
記録が言い切っていないところ（報告書が「推定」としたところ、報告書と判決で答えが分かれるところ）は、画面と語りでそのまま断っています。
※ 画面の模式図・時間の帯・角度の図・再現のイラスト・地図の書き込みは、記録をもとに描いた図です。
※ 操縦室の声は、報告書に載っている文字の記録（CVR の記録）から読んでいます。音声は使っていません。
※ 亡くなった方、乗員、乗客、ご遺族のお名前は出していません。乗員は役職で呼んでいます。
※ 同じ型の機体や操縦室の写真は、事故機ではありません（画面の副題で断っています）。"""

# ✅ ⑥（10-21）カズヤくん：地＝生成 AI 案A（gen_thumb_ai cal_a）→「実際の 52.6度の異様さを出してほしい」→ 機体を 52.6度に回した地
#    （qa_out/ep17_ai_pitch.py・ep17_ai_plane.py）→「3をA、2をBとしてテストします」＝**A＝機体を大きな字の手前に重ねる版**（上げるときに貼る）・
#    B＝同じ地の反転版（`out/thumb/ep17-ab/ep17_Hinv_ai_a526c_b160.png`・md5 ab2c75f7…＝カズヤくんが Studio の「テストと比較」で入れる）
THUMB = "out/thumb/ep17-ab/ep17_Hinv_ai_a526c_over_b160.png"
THUMB_MD5 = "f98c98ff19ee76b945a793693cf1e7e9"
THUMB_NOTE = "※ サムネイルの絵は、生成AIで作った再現のイメージです（実際の写真ではありません。機首の角度は、報告書の約52.6度に合わせています）。"

TAGS = ["中華航空140便", "中華航空140便墜落事故", "名古屋空港", "中華航空機墜落事故", "1994年", "エアバスA300", "自動操縦",
        "ゴー・アラウンド", "航空事故", "事故検証", "一次資料", "ゆっくり解説", "ドキュメンタリー", "解説", "ヒューマンファクター"]

PDL = "公共データ利用規約（第1.0版）"
LIC_URL = {"CC BY 2.0": "https://creativecommons.org/licenses/by/2.0/deed.ja",
           "CC BY 3.0": "https://creativecommons.org/licenses/by/3.0/deed.ja",
           "CC BY 4.0": "https://creativecommons.org/licenses/by/4.0/deed.ja",
           "CC BY-SA 2.0": "https://creativecommons.org/licenses/by-sa/2.0/deed.ja",
           "CC BY-SA 3.0": "https://creativecommons.org/licenses/by-sa/3.0/deed.ja",
           "CC BY-SA 4.0": "https://creativecommons.org/licenses/by-sa/4.0/deed.ja",
           "GFDL 1.2": "https://www.gnu.org/licenses/old-licenses/fdl-1.2.html",
           "CC0": "https://creativecommons.org/publicdomain/zero/1.0/deed.ja"}
FILM_URL = "https://www.youtube.com/watch?v=WQTZQU1VOC4"      # 防衛省・自衛隊の公式チャンネル（台本 §10 の V1）


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
    """`ref/ep17/yougo.md` の「## 貼る本文」の節を**そのまま**返す（次の `---` か `## ` まで）。見出しの語が語りに出るかを当てる。"""
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
    """SPEC の値を辿って、素材の道（`ep17/…`）を全部出す（尻・頭の差し込み・地に敷く写真も含む）。"""
    if isinstance(v, str):
        if v.startswith("ep17/"):
            yield v
    elif isinstance(v, dict):
        for x in v.values():
            yield from _walk(x)
    elif isinstance(v, (list, tuple)):
        for x in v:
            yield from _walk(x)


# 画面の出典表記（credits.json の値＝作者は印 {作者} のまま）→ 種類（名乗れないものは None）。⚠️ 並びに意味がある（上から当てる）
KINDS = [
    ("rphoto", r"^出典：運輸省 航空事故調査委員会『航空事故調査報告書 96-5』写真\d+（加工して作成）$"),
    ("rfig", r"^出典：運輸省 航空事故調査委員会『航空事故調査報告書 96-5』付図\d+（加工して作成）$"),
    ("rpage", r"^出典：運輸省 航空事故調査委員会『航空事故調査報告書 96-5』本文（加工して作成）$"),
    ("court", r"^出典：名古屋地方裁判所 2003年12月26日判決（平成7年\(ワ\)第4179号）$"),
    ("faa", r"^出典：アメリカ連邦航空局『The Interfaces Between Flightcrews and Modern Flight Deck Systems』（1996年）(序文|図\d+|本文)（パブリックドメイン）$"),
    ("own", r"^写真：\{作者\}（(CC BY(-SA)? [234]\.0|GFDL 1\.2)）・改変(なし|：切出(・顔にモザイク)?)$"),
    ("cc0", r"^写真：Wikimedia Commons（CC0）$"),
    ("loc", r"^写真：米議会図書館（パブリックドメイン）$"),
    ("hel", r"^写真：ヘルシンキ市立博物館（CC BY 4\.0）・改変：切出$"),
    ("stock", r"^イメージ（Pexels）$"),
    ("sat", r"^地図：Google マップの衛星写真（帰属は地図の右下）$"),
    ("gsi", r"^国土地理院撮影の空中写真（1987〜1990年撮影）を加工して作成$"),
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
    for v in SS.SAT.values():                 # 衛星写真と空中写真＝出典は表 SAT の credit（scene_jiko.ep17_credit と同じ）
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
    films, stock_films = OrderedDict(), OrderedDict()
    for cid, u in F.USE.items():
        k = u["clip"]
        c = clips.get(k)
        if c is None:
            bad.append(f"{cid}:{k}（clips.json に無い）")
            continue
        cr = c.get("credit", "")
        if cr.startswith("出典：防衛省・自衛隊『平成6年防衛庁記録』（CC BY 3.0）"):
            films.setdefault(cid, c)
        elif cr == "イメージ（Pexels）":
            stock_films.setdefault(k, c)
        else:
            bad.append(f"{cid}:{k}（名乗れない映像の出典：{cr}）")
    if bad:
        raise SystemExit(f"🔴 名乗れない素材がある。書かずに止めた: {bad}")
    counts = {k: len(v) for k, v in got.items()}
    counts.update(film=len(films), stock_film=len(stock_films))
    print(f"■ 素材（配線から）：{counts}")
    if N_COUNTS is not None and counts != N_COUNTS:
        raise SystemExit(f"🔴 点数が⑥で数えた値 {N_COUNTS} と違う。文の点数を当て直すこと。書かずに止めた。")
    return got, counts


def _code(p):
    return json.loads(ASSETS_JSON.read_text(encoding="utf-8"))[Path(p).stem]["code"]


def read_credits() -> str:
    got, n = used_material()
    pid = json.loads(PAGEIDS.read_text(encoding="utf-8"))
    out = ["【写真・図・頁・映像】",
           f"・事故の報告書の写真 {n.get('rphoto', 0)}点・付図 {n.get('rfig', 0)}点・本文の頁 {n.get('rpage', 0)}枚"
           f"＝{PDL}にもとづいて利用（出典：運輸安全委員会 https://jtsb.mlit.go.jp/ ・切り出しなどの加工をして作成）"]
    if n.get("court"):
        out.append(f"・判決の頁 {n['court']}枚＝名古屋地方裁判所の判決（裁判所のウェブサイト）")
    if n.get("faa"):
        out.append(f"・アメリカ連邦航空局（FAA）の報告書の頁と図 {n['faa']}枚（パブリックドメイン）")
    # 個人名義（Commons）＝作者・ライセンス・改変ごとにまとめる（名前は git の外の表から＝焼く道と同じ）
    by = OrderedDict()
    for p, (cid, s) in (got.get("own") or {}).items():
        lic = re.search(r"（(CC BY(?:-SA)? [234]\.0|GFDL 1\.2)）", s).group(1)
        how = "加工なし・額に入れて表示" if "改変なし" in s else ("切り出し・顔にモザイク" if "モザイク" in s else "切り出し")
        code = _code(p)
        if code not in pid or lic not in LIC_URL:
            raise SystemExit(f"🔴 {code} の Commons の頁かライセンスの URL が無い。書かずに止めた。")
        if pid[code]["license"] != lic:
            raise SystemExit(f"🔴 {code} のライセンスが表（{pid[code]['license']}）と画面（{lic}）で違う。書かずに止めた。")
        who = S._ep17_author(p)
        by.setdefault((who, lic, how), []).append(pid[code]["url"])
    out.append("・Wikimedia Commons の写真（作者・ライセンス・頁）")
    for (who, lic, how), urls in by.items():
        out.append(f"　{who}（{lic}・{how}）{len(urls)}点　" + "　".join(urls) if len(urls) > 1
                   else f"　{who}（{lic}・{how}）　{urls[0]}")
    for p, (cid, s) in (got.get("hel") or {}).items():
        out.append(f"　ヘルシンキ市立博物館（CC BY 4.0・切り出し）　{pid[_code(p)]['url']}")
    for p, (cid, s) in (got.get("loc") or {}).items():
        out.append(f"　米議会図書館（パブリックドメイン）　{pid[_code(p)]['url']}")
    if n.get("cc0"):
        out.append(f"　ほかに CC0 の写真 {n['cc0']}点（エアバス社の本社・裁判所の庁舎・国家運輸安全委員会の本部・同じ系列の機体）")
    used_lic = sorted({lic for (_, lic, _) in by} | ({"CC BY 4.0"} if got.get("hel") else set()))
    out.append("　ライセンス：" + "　".join(f"{lic} {LIC_URL[lic]}" for lic in used_lic))
    if n.get("gsi"):
        out.append(f"・空中写真 {n['gsi']}点＝国土地理院撮影の空中写真（1987〜1990年撮影）を加工して作成")
    if n.get("sat"):
        out.append(f"・地図の衛星写真 {n['sat']}点＝Google マップ（帰属は地図の右下）")
    if n.get("film"):
        out.append(f"・映像＝防衛省・自衛隊『平成6年防衛庁記録』（CC BY 3.0　{LIC_URL['CC BY 3.0']}）・切り出し・再生速度の変更　{FILM_URL}")
    out.append("※ 画面に「イメージ」と出る写真・映像は、フリー素材です。その日・その場を写したものではありません")
    out.append("※ 国の機関（運輸安全委員会・防衛省）や裁判所の資料を使っていますが、これらの機関がこの動画を作ったり、推奨・支持したりしているものではありません")
    return "\n".join(out)


def chapters() -> str:
    starts, t = {}, 0.0
    for cid, sec in S.CUTS:
        starts[cid] = t
        t += sec
    rows = [(S.CUTS[0][0], "はじめに")]     # つかみ（c101〜c109）は章の印なし＝0:00 を足す
    # 🔴 17本目は章を扉の区切りで引く（`check_script.door_key`）＝第1章の鍵は "c1'"（c110〜c117）・つかみの "c1" は章の表に無い
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
    meta = {"slug": "ep17", "title": TITLE, "description": desc, "tags": TAGS, "thumbnail": THUMB,
            "genre": "jiko", "playlist": ""}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✓ 書いた → {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
