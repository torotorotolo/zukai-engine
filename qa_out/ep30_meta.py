# -*- coding: utf-8 -*-
"""30本目（地下鉄サリン事件）の `config/meta_ep30.json` を**機械で**組み立てる（2026-11-06・⑥）。

`qa_out/ep29_meta.py`（用語・目次・素材の点数・字数の網）を写し、素材の種類を30本目の出典の形に直した
（衛星写真は `qa_out/ep25_meta.py` の数え方）。

🔴 手で書かない理由（ep7〜ep29 と同じ）
  ① 用語は `ref/ep30/yougo.md` の「## 貼る本文」の節が正本＝**そのまま**貼る。見出しの語が語りに出るかと、並びが語りに初めて出る順かを当てる
  ② 素材の点数は**章ファイルの実配線**（`cuts.SPEC` の写真／`footage.USE` の映像）から数え、権利は**画面の出典表記**
     （`ref/ep30/credits.json`・`clips.json`・衛星写真は `cuts.ss.SAT`）で照らす。名乗れない素材が出たら落ちる
  ③ 目次は `scene_jiko.CUTS` の秒を頭から積む＝**焼いた版と同じ秒**
  ④ タイトル 100字・説明 5,000字の上限と、入れてはいけない語を、書く前に確かめる

🔴 判決が確定した事件の回（ルール §B2-12・記憶 feedback-jiko-incident-case-rules の 11-04）
  - 被害者・遺族・手記の筆者・裁判の関係者の名前は書かない（立場だけ）／教祖の名前も説明欄には書かない（本編 c210 だけ）
  - 後継の団体は「アレフ」だけ・公的資料の範囲／この回の線（ルール §B2-12）の語は書かない＝`linecheck30.py` で当てる
  - **窓口を出す**＝cc13・cc14 の語り「どの窓口も、説明欄に書く」・cc18「置き場は説明欄に書く」
  - 「死亡」は使わない（亡くなった方）・無線は自動字幕で読んだ＝耳で未確認と断る（承認① の4・台本 §8）
  - Commons の作者と資料館の個人の提供者の名前は**公開リポに書かない**＝作者は git の外の表から `scene_jiko._ep30_person` で足す
    （`config/` は gitignore）。個人の提供者は説明欄に名前を書かない（引用＝出典は画面に表示）

    python -P qa_out/ep30_meta.py            # 組み立てて config/meta_ep30.json に書く
    python -P qa_out/ep30_meta.py --dry      # 書かずに中身と字数だけ出す
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

YOUGO = HERE / "ref" / "ep30" / "yougo.md"
CREDITS_JSON = HERE / "ref" / "ep30" / "credits.json"
ASSETS_JSON = HERE / "ref" / "ep30" / "assets.json"
CLIPS = HERE / "ref" / "ep30" / "clips.json"
OUT = HERE / "config" / "meta_ep30.json"

N_GLOSS = 8           # `ref/ep30/yougo.md` の「貼る本文」の語数
# ⚠️ ⑥（11-06）の配線から数えた点数（変わったら止まる＝文の点数を当て直す）。None＝数えて出すだけ
N_COUNTS = {"quote": 19, "jsdf": 19, "sat": 11, "own": 10, "gov": 7, "stock": 31, "cc0": 2, "pd": 1, "kids": 2, "arc": 1,
            "mod_clips": 1, "stock_film_clips": 4, "mod_cuts": 6, "stock_film_cuts": 4, "mos_face": 1, "mos_plate": 1}

# ✅ 承認①（11-05 カズヤくん「推奨どおり」）の題 A のまま。【映像あり】＝防衛省の記録（1920×1080・当日の除染）＝ルール 1-8 の幅1280以上
TITLE = ("【映像あり】地下鉄サリン事件の真相。前の年に松本で同じ毒が使われ、4か月前には土から手がかりが出ていた。"
         "【事件検証】【ゆっくり解説】")
TITLE_LEN = 66        # 決めた題の字数（写し間違いの網）

# ⚠️ 本文（台本第2版 c101〜c108）で言っていることだけを書く
HEAD = """【この動画について】
1995年3月20日、月曜の朝。8時21分ごろ、警視庁の無線に「病人2名」の知らせが入りました。3分後には、築地駅の話として「ガソリンの匂い」。8時40分の手前には「爆発物を使用した」事件と流れ、現場の手記では、消防の指令も、病院への第一報も「爆発火災」でした。まかれたのは、猛毒の神経ガス、サリンでした。

公安調査庁の数で、亡くなった方は14人、けがをした人は5,800人以上。同じ毒は、前の年に長野県の松本で使われていました。地下鉄の事件の4か月前には、山梨の、ある教団の施設の近くの土から、サリンが分解するときにもできる物質が見つかっていました。

なぜ、止められなかったのか。あの朝、現場は何を知らされていなかったのか。国の公安調査庁が公開した無線の記録と手記、判決、国会の記録、白書をもとに、順にたどります。
"""

# 🔴 cc13・cc14 の語り「どの窓口も、説明欄に書く」＝11-06 に頁で当て直した字（ref/ep30/sources.md §5・§8）
WINDOW = """【相談の窓口】
・消費者ホットライン（消費者庁）　188
・警察相談専用電話（警察庁）　#9110（受付の時間は都道府県の警察で異なります）
・法テラス 犯罪被害者支援ダイヤル　0120-079714（平日9時〜21時・土曜9時〜17時。祝日と年末年始を除く）
・公安調査庁 情報提供窓口　https://www.moj.go.jp/psia/report_to_psia.html
※ 公安調査庁は、団体の名前を隠したヨーガや心理学などの集まりへの勧誘に、注意を呼びかけています（オウム真理教特集ページ　https://www.moj.go.jp/psia/aum.top/index.html）。

【無線と手記の置き場】
公安調査庁「オウム真理教問題デジタルアーカイブ」　https://www.moj.go.jp/psia/aumarchive/
"""

# 台本第1版の出典の欄の略（白・判・国・手・声・公・特・消・東消・犯白・給・無線・OH）と `ref/ep30/sources.md` から
PRIMARY = """【出典】
・公安調査庁「オウム真理教問題デジタルアーカイブ」（警視庁の無線指令音声記録・現場の手記・遺族と被害者の手記・年表と各事件の頁・資料館の写真）
・公安調査庁「オウム真理教特集ページ」・報道発表（観察処分の期間の更新請求〈2026年11月2日〉・再発防止処分の決定〈2026年9月4日〉）
・警察庁『警察白書』平成8年版
・東京地方裁判所・東京高等裁判所・最高裁判所の判決（裁判所ウェブサイト）
・国会会議録（衆議院・参議院の委員会の発言）
・消防庁の検討会の資料と通知・東京消防庁 京橋消防署の沿革
・法務省『犯罪白書』令和元年版・警察庁『犯罪被害者白書』
・厚生労働省のオーラル・ヒストリー（聞き取りの配信の字幕）
・防衛省・自衛隊『平成6年防衛庁記録』（映像）
"""

# ⚠️ 語りは「11月4日の時点」のまま＝11-06 に公安調査庁の頁と報道へ当て直した（決定はまだ）。公開の直前にもう一度当てて RECHECK を直す
RECHECK = "11月6日"
TAIL = f"""動画に出てくる数字と日付は、公安調査庁の公開資料、判決、国会の記録、白書によります（2026年11月4日時点。公開前の{RECHECK}に、公安調査庁の頁と報道を見直しました）。
※ 観察処分の期間の更新について、公安審査委員会の決定は、{RECHECK}の時点でまだ出ていません（動画では「11月4日の時点で、決定は出ていない」とお伝えしています）。
※ 警視庁の無線の言葉は、公開された音声の自動字幕で読んだもので、耳では確かめていません。無線の時刻は、記録の時報から数えた目安です。手記の時刻は、書いた方の記憶です。
※ 今回読んだ範囲：国会の記録は選んだ発言だけ、判決は語で当たりを付けた部分です。手記の過去の版、消防白書（平成7年版）、東京消防庁と営団地下鉄の当日の記録は読んでいません。
※ 被害に遭われた方、ご遺族、手記を書いた方、裁判の関係者のお名前は出していません（立場でお伝えしています）。
※ 画面の模式図は、公の記録をもとに描いた図です。"""

# ✅ 11-06 カズヤくん「H反転A65で決まり。上の行は「前の年にも同じ毒」に変更」→「サムネ上部の赤字は「同じ毒」だけ」
#    ＝`qa_out/ep30_thumb_hx.py` の Ad65（地 #65＝本編 c104 と同じ写真）。1つ前の版（赤が句全体）は ep30_T_HinvA65.png に残した
THUMB = "out/thumb/ep30/ep30_T_HinvA65b.png"
THUMB_MD5 = "68c9592b2fa2fc1d77dfa5ed95987211"
THUMB_NOTE = ("※ サムネイルの写真は、公安調査庁「オウム真理教問題デジタルアーカイブ」の陸上自衛隊の提供の写真（PDL1.0）を"
              "切り出し、色と明るさを変えて（文字の中は白黒）、文字を重ねて作成しています。")

TAGS = ["地下鉄サリン事件", "サリン事件", "オウム真理教", "松本サリン事件", "サリン", "1995年", "霞ケ関駅", "築地駅",
        "警視庁", "公安調査庁", "陸上自衛隊", "除染", "アレフ", "事件検証", "ゆっくり解説", "解説"]

LIC_URL = {"CC BY 2.0": "https://creativecommons.org/licenses/by/2.0/deed.ja",
           "CC BY 2.5": "https://creativecommons.org/licenses/by/2.5/deed.ja",
           "CC BY 3.0": "https://creativecommons.org/licenses/by/3.0/deed.ja",
           "CC BY 4.0": "https://creativecommons.org/licenses/by/4.0/deed.ja",
           "CC BY-SA 3.0": "https://creativecommons.org/licenses/by-sa/3.0/deed.ja",
           "CC BY-SA 4.0": "https://creativecommons.org/licenses/by-sa/4.0/deed.ja",
           "CC0": "https://creativecommons.org/publicdomain/zero/1.0/deed.ja"}
PDL_URL = "https://www.digital.go.jp/resources/open_data/public_data_license_v1.0"


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
    """`ref/ep30/yougo.md` の「## 貼る本文」の節を**そのまま**返す（次の `---` か `## ` まで）。見出しの語が語りに出るかを当てる。"""
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
    """SPEC の値を辿って、素材の道（`ep30/…`）を全部出す（地に敷く写真も含む）。"""
    if isinstance(v, str):
        if v.startswith("ep30/"):
            yield v
    elif isinstance(v, dict):
        for x in v.values():
            yield from _walk(x)
    elif isinstance(v, (list, tuple)):
        for x in v:
            yield from _walk(x)


_ARC = "出典：公安調査庁 オウム真理教問題デジタルアーカイブ"
# 画面の出典表記（credits.json の値＝作者は印 {作者}・{個人} のまま）→ 種類（名乗れないものは None）。⚠️ 並びに意味がある（上から当てる）
KINDS = [
    ("jsdf", r"^" + _ARC + r"（提供：陸上自衛隊）・PDL1\.0・加工して作成$"),
    ("arc", r"^" + _ARC + r"・PDL1\.0・加工して作成$"),
    ("quote", r"^" + _ARC + r"（提供：(?:\{個人\}|東京地下鉄|東京消防庁)）$"),
    ("own", r"^写真：\{作者\}／Wikimedia Commons（CC BY(?:-SA)? (?:[234]\.0|2\.5)）／改変(?:なし|：切出(?:・(?:顔|ナンバー)にモザイク)?)$"),
    ("cc0", r"^写真：\{作者\}／Wikimedia Commons（CC0）$"),
    ("pd", r"^写真：\{作者\}／Wikimedia Commons（パブリックドメイン）$"),
    ("kids", r"^出典：法務省 キッズルーム（公安調査庁の写真）／Wikimedia Commons・加工して作成$"),
    ("gov", r"^出典：(?:公安調査庁 (?:オウム真理教特集ページ|アーカイブ年表|\d{4}年\d+月\d+日|オウム真理教問題デジタルアーカイブ moj)"
            r"|消防庁 検討会の資料|警察白書 平成\d+年|東京地裁 平成\d+年\d+月\d+日判決)"),
    ("sat", r"^地図：Google マップの衛星写真（帰属は地図の右下）$"),
    ("stock", r"^イメージ（Pexels）$"),
]
FILM_KINDS = {"出典：防衛省・自衛隊『平成6年防衛庁記録』（CC BY 3.0）・改変：切出・再生速度": "mod", "イメージ（Pexels）": "stock_film"}


def _kind(s: str):
    for k, pat in KINDS:
        if re.match(pat, s):
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
    got, bad, mos = OrderedDict(), [], {"顔": set(), "ナンバー": set()}
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
            for w in mos:
                if f"{w}にモザイク" in s:
                    mos[w].add(p)
    films = OrderedDict()
    for cid, u in F.USE.items():
        c = clips.get(u["clip"])
        if c is None:
            bad.append(f"{cid}:{u['clip']}（clips.json に無い）")
            continue
        k = FILM_KINDS.get(c.get("credit", ""))
        if k is None:
            bad.append(f"{cid}:{u['clip']}（名乗れない映像の出典：{c.get('credit')}）")
            continue
        films.setdefault(k, OrderedDict()).setdefault(u["clip"], []).append(cid)
    if bad:
        raise SystemExit(f"🔴 名乗れない素材がある。書かずに止めた: {bad}")
    counts = {k: len(v) for k, v in got.items()}
    counts.update({f"{k}_clips": len(v) for k, v in films.items()})
    counts.update({f"{k}_cuts": sum(len(x) for x in v.values()) for k, v in films.items()})
    counts.update(mos_face=len(mos["顔"]), mos_plate=len(mos["ナンバー"]))
    print(f"■ 素材（配線から）：{counts}")
    if N_COUNTS is not None and counts != N_COUNTS:
        raise SystemExit(f"🔴 点数が⑥で数えた値 {N_COUNTS} と違う。文の点数を当て直すこと。書かずに止めた。")
    return got, counts


def read_credits() -> str:
    got, n = used_material()
    assets = json.loads(ASSETS_JSON.read_text(encoding="utf-8"))
    out = ["【写真・映像】"]
    out.append(f"・公安調査庁「オウム真理教問題デジタルアーカイブ」の写真 {n.get('jsdf', 0) + n.get('arc', 0)}点（うち陸上自衛隊の提供 {n.get('jsdf', 0)}点）"
               f"＝公共データ利用規約 第1.0版（PDL1.0）　{PDL_URL}　切り出しと寄り・暗さを変えて使っています")
    out.append(f"・同じアーカイブの、ほかの機関と個人の提供の写真 {n.get('quote', 0)}点＝引用（加工なし・出典と提供は画面に表示）")
    # 個人名義（Commons）＝作者・ライセンスごとにまとめる（名前は git の外の表から＝焼く道と同じ）
    by = OrderedDict()
    for k in ("own", "cc0", "pd"):
        for p, (cid, s) in (got.get(k) or {}).items():
            st = Path(p).stem
            a = assets.get(st) or {}
            lic = {"cc0": "CC0", "pd": "PD"}.get(k) or re.search(r"（(CC BY(?:-SA)? (?:[234]\.0|2\.5))）", s).group(1)
            if a.get("lic") != lic:
                raise SystemExit(f"🔴 {st} のライセンスが台帳（{a.get('lic')}）と画面（{lic}）で違う。書かずに止めた。")
            by.setdefault((S._ep30_person(p, "{作者}"), lic), []).append(p)
    nc = sum(len(v) for v in by.values())
    out.append(f"・Wikimedia Commons の写真 {nc}点（CC BY は切り出し・CC BY-SA は加工なし・写真ごとの作者とライセンスは画面の出典の行にも）")
    for (who, lic), ps in by.items():
        out.append(f"　{who}（{'パブリックドメイン' if lic == 'PD' else lic}）" + (f"{len(ps)}点" if len(ps) > 1 else ""))
    used_lic = sorted({lic for (_, lic) in by if lic in LIC_URL})
    out.append("　ライセンス：" + "　".join(f"{lic} {LIC_URL[lic]}" for lic in used_lic))
    if n.get("mos_face") or n.get("mos_plate"):
        out.append(f"　顔が写る {n.get('mos_face', 0)}点は顔に、車のナンバーが写る {n.get('mos_plate', 0)}点はナンバーに、モザイクをかけています")
    if n.get("kids"):
        out.append(f"・法務省 キッズルームの公安調査庁の写真 {n['kids']}点（Wikimedia Commons の同じ写真・PDL1.0 の読み・切り出し）")
    out.append(f"・国の頁と資料の画面 {n.get('gov', 0)}点（公安調査庁・消防庁・警察白書・判決＝出典は画面に表示・名前と一部の文を隠しています）")
    if n.get("sat"):
        out.append(f"・地図の衛星写真 {n['sat']}点＝Google マップ（帰属は地図の右下）")
    out.append(f"・映像＝防衛省・自衛隊『平成6年防衛庁記録』（CC BY 3.0・切り出しと再生速度）{n.get('mod_cuts', 0)}カット　{LIC_URL['CC BY 3.0']}")
    out.append(f"※ 画面に「イメージ」と出る写真（{n.get('stock', 0)}点）と映像（{n.get('stock_film_clips', 0)}本）は、フリー素材（Pexels）です。"
               "その日・その場を写したものではありません")
    out.append("※ 国の機関（公安調査庁・警察庁・消防庁・防衛省・裁判所）・東京消防庁・東京地下鉄の資料と写真を使っていますが、"
               "これらの機関や会社がこの動画を作ったり、推奨・支持したりしているものではありません")
    return "\n".join(out)


def chapters() -> str:
    starts, t = {}, 0.0
    for cid, sec in S.CUTS:
        starts[cid] = t
        t += sec
    rows = [(S.CUTS[0][0], "はじめに")]     # つかみ（c101〜c108）は章の印なし＝0:00 を足す
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
    # 🔴 判決が確定した事件の回（ルール §B2-12）＝「死亡」を使わない・教祖と団体の幹部の名前を説明欄に書かない
    for bad in ("死亡", "犯人", "麻原", "松本智津夫", "尊師", "グル"):
        if bad in TITLE or bad in desc:
            raise SystemExit(f"🔴 「{bad}」が入っている。書かずに止めた。")
    for need in ("188", "#9110", "0120-079714", "report_to_psia", "aumarchive", "自動字幕"):
        if need not in desc:
            raise SystemExit(f"🔴「{need}」が無い（cc13・cc14・cc18 の語りと事件の回の決まり・無線の断り）。書かずに止めた。")
    if not TITLE.endswith("【事件検証】【ゆっくり解説】"):
        raise SystemExit("🔴 タイトルの末尾が「【事件検証】【ゆっくり解説】」でない（事件の回の決まり）。書かずに止めた。")
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
    meta = {"slug": "ep30", "title": TITLE, "description": desc, "tags": TAGS, "thumbnail": THUMB,
            "genre": "jiko", "playlist": ""}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✓ 書いた → {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
