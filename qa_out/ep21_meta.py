# -*- coding: utf-8 -*-
"""21本目（9.11 米国同時多発テロのリメイク）の `config/meta_ep21.json` を**機械で**組み立てる（2026-10-13・⑥）。

`qa_out/ep20_meta.py` を写して、この回の形に合わせた。

🔴 手で書かない理由（ep7〜ep20 と同じ）
  ① 用語は `ref/ep21/yougo.md` の「## 貼る本文」の節が正本＝**そのまま**貼る（`**` だけ外す）
  ② 素材の点数は**章ファイルの実配線**（`cuts.SPEC` の写真・頁＝尻や頭の差し込みも含む／`footage.USE` の映像）から数え、
     権利は**画面の出典表記**（`ref/ep21/credits.json`・`clips.json`）で照らす。名乗れない素材が出たら落ちる
  ③ 目次は `scene_jiko.CUTS` の秒を頭から積む＝**焼いた版と同じ秒**（章の扉の2秒は CUTS に入っている）
  ④ タイトル 100字・説明 5,000字の上限と、入れてはいけない語を、書く前に確かめる

🔴 この回が 20本目と違うところ
  - 権利：米連邦の職務（A）・議会図書館の撮影者不詳＝撮影者が権利を放棄（C'）・議会図書館「知られた制限なし」（D）・
    自主宣言（CC0・PD）・CC BY 2.0／2.0 de／3.0・CC BY-SA 3.0（額装・改変なし＝c204・c205）を**書き分ける**（materials §2-12b＝
    旧版は A・C・C'・D をまとめて「パブリックドメイン」と書いていた）
  - 【映像あり】は付けない（④＝実効1280以上の実写0本）
  - 乗っ取った側の名前・乗員・乗客・電話の相手の名前は出さない（台本 §1-4）＝🔴 commit の前に `ref/ep21/src/core_raw/namecheck.py`
  - 記録音声は鳴らさない（10-11 カズヤくん）・衝突の瞬間の映像は使わない（同）
  - 末尾に ※ でリメイクと記す（旧版＝7本目・2026年9月公開・10-05 に非公開）

    python qa_out/ep21_meta.py            # 組み立てて config/meta_ep21.json に書く
    python qa_out/ep21_meta.py --dry      # 書かずに中身と字数だけ出す
"""
import json
import re
import sys
from collections import OrderedDict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
import scene_jiko as S            # noqa: E402

YOUGO = HERE / "ref" / "ep21" / "yougo.md"
CREDITS_JSON = HERE / "ref" / "ep21" / "credits.json"
CLIPS = HERE / "ref" / "ep21" / "clips.json"
PAGEIDS = HERE / "qa_out" / "ep21_commons_pageids.json"   # Commons の頁の番号（10-13 に API で1回引いた）
OUT = HERE / "config" / "meta_ep21.json"

N_GLOSS = 14          # `ref/ep21/yougo.md` の「貼る本文」の語数（⑥で語りに当てて確定）
# ⚠️ 下の値は⑥で配線から数えた点数（変わったら止まる＝文の点数を当て直す）。10-13 の版（本編 4587321）
#    写真57＝束の57点（写真53・イメージ4）・頁10（NTSB 7・委員会報告 1・RG237 2）・映像7（DVIDS 3・大統領図書館 3・CC BY-SA 1）
N_COUNTS = {"loc_c2": 9, "us_gov": 30, "highsmith": 1, "ccbysa": 1, "ccby": 7, "loc_d": 6, "pg_ntsb": 7,
            "pg_rg237": 2, "pd_self": 1, "cc0": 2, "pg_comm": 1, "film": 7}

# ✅ 台本第2版 §1-1（承認① 2026-10-12 カズヤくん＝旧版の文・決まりだけ今・86字）で公開（10-13 21:47）
#    「軍が1機目の乗っ取りを知らされたのは衝突9分前。残る3機は墜ちるまで知らされなかった。2,977人が亡くなった9.11アメリカ同時多発テロの真相【事故検証】【ゆっくり解説】」
# 🔴 10-13 公開のあと：カズヤくん「タイトルも変更。『ツインタワー』等、一目で何の事件か分かる単語を最初に、もっとインパクトのある表現。
#    『ツインタワー━━━━━。9.11アメリカ同時多発テロの真相【事故検証】【ゆっくり解説】』の形」→ 4案から **案A**（60字）。
#    根拠＝委員会報告 p21（NEADS received notice of the hijacking nine minutes before it struck the North Tower・
#    That nine minutes' notice before impact was the most the military would receive）。「死亡」は使わない・【映像あり】は付けない
TITLE = ("ツインタワー激突まで、軍に残された時間はわずか9分だった。"
         "9.11アメリカ同時多発テロの真相【事故検証】【ゆっくり解説】")
TITLE_LEN = 60

# ⚠️ 本文（台本第2版 c101〜c109・c201・cb15）で言っていることだけを書く
HEAD = """【この動画について】
2001年9月11日、火曜日の朝。アメリカで、旅客機4機が相次いで乗っ取られました。2機はニューヨークの世界貿易センターの2つの高層ビルに、1機は首都ワシントンの対岸にある国防総省（ペンタゴン）にぶつかり、4機目はペンシルベニア州の野原に墜ちました。いま数えられている犠牲者は2,977人です（乗っ取った側の19人は入っていません）。

アメリカ北東部の空を見張る軍の当直が、1機目の乗っ取りを知らされたのは、北のビルにぶつかる9分前でした。残る3機は、前もっての知らせがありませんでした。けれど地上の管制官のなかには、気づいていた人がいました。この動画は、その朝、管制官と軍の当直が何を見て、何を知らなかったのかを、調査委員会が集めた記録の時刻でたどります。

時刻はすべて、現地のアメリカ東部の夏の時間です（日本時間より13時間遅い）。長さや高さはメートル法に直して伝えます。建物がなぜ崩れたのかは、この動画では扱いません。

・軍が1機目の乗っ取りを知らされたのは、いつだったのか
・機体が名乗るのをやめたとき、管制官の画面には何が残ったのか
・アメリカは、どうやって国じゅうの空を閉じたのか
・「撃ち落とせ」という命令は、なぜ届かなかったのか
・「9分」という数は、どう分かったのか

※ 当時の無線・電話・操縦室の音声は鳴らしていません。言葉は語りと字幕で伝えています。
"""

# 台本第2版の出典の欄と `ref/ep21/sources.md`（§1・§2・§6・§11）・`src/new/`（④・④'で開いた写し）から（URL は 10-11〜13 に開いたもの）
PRIMARY = """【出典】
・9.11委員会「The 9/11 Commission Report」（2004年7月・政府印刷局版）　https://www.govinfo.gov/content/pkg/GPO-911REPORT/pdf/GPO-911REPORT.pdf
・9.11委員会のスタッフ声明 No.17「Improvising a Homeland Defense」（2004年6月17日）　https://govinfo.library.unt.edu/911/staff_statements/staff_statement_17.pdf
・9.11委員会の公聴会の記録（2003年5月23日・運輸長官の証言）　https://govinfo.library.unt.edu/911/archive/hearing2/9-11Commission_Hearing_2003-05-23.htm
・アメリカ国家運輸安全委員会（NTSB）「Flight Path Study」11便・175便・77便・93便の4本（2002年2月19日・元の頁は閉じられ、ウェブ・アーカイブに写しがあります）
・93便の操縦室の音声の記録の書き起こし（NTSB と FBI が作成・連邦地裁の裁判の証拠 P200056T・2006年）
・アメリカ運輸省 監察総監の報告 CC-2006-085（2006年8月31日）　https://www.oig.dot.gov/sites/default/files/cc2006085.pdf
・アメリカ国立標準技術研究所（NIST）NCSTAR 1（2005年9月）　https://nvlpubs.nist.gov/nistpubs/Legacy/NCSTAR/ncstar1.pdf
・アメリカの法律 107-71（2001年11月19日）　https://www.govinfo.gov/content/pkg/PLAW-107publ71/html/PLAW-107publ71.htm
・9.11記念館（9/11 Memorial & Museum）のよくある質問　https://www.911memorial.org/911-faqs
・ニューヨーク市の検視局の発表（2026年8月24日）　https://www.nyc.gov/site/ocme/news/cm0226/mayor-mamdani-office-chief-medical-examiner-new-identification-world
・アメリカ国立公園局「Phone Calls from Flight 93」　https://www.nps.gov/flni/learn/historyculture/phone-calls-from-flight-93.htm
・AP 通信の記事（2001年9月17日・Seattle Times の写し）　https://archive.seattletimes.com/archive/20010917/heroes17/last-words-from-victims-lets-roll"""

TAIL = """動画に出てくる数値・時刻・言葉は、これらの記録によります。
記録が言い切っていないところや、記録どうしで割れるところは、画面と語りでそのまま断っています。
※ 画面の地図・時刻の帯・模式図は、記録をもとに描いた図です。
※ 乗っ取った側の名前、乗員・乗客・電話の相手のお名前は出していません。
※ 衝突の瞬間の映像は使っていません。
※ この動画は、2026年9月に公開した9.11の動画を、作り直したものです。"""

# ✅ 10-12 の決め＝A＋E2＋案3・黄の3枚（地 a09）・最初に上げるのは A
# 🔴 10-13（⑥の試写のあと）カズヤくん「サムネイルは添付画像のものを設定。他のテスト用の2枚は私が後で設定」＝添付は
#    **H「9.11」の型抜き**（見本 `ep21-new/サムネテスト/ep21_H_knock911.png` と画素の差 平均1.5）＝`thumb_jiko.ep21_h()`
#    ＝10-13 の最終（H 1枚目・A 2枚目・E2 3枚目・地は3枚とも a01＝別のチャット「サムネ刷新の調べ」の記録）。2・3枚目はカズヤくんが Studio で
#    （公開の 21:47 の時点の置き場は `ep21_H.png`＝同じ md5。そのあと3枚を 1_H・2_A・3_E2 の名に揃えた）
# 🔴 10-13 公開のあと：カズヤくん「「9.11」が少し読みにくい・視認性を向上」→ 4案（v0 いま／v1／v2 白い輪／v3 影）→ 「v1」＝
#    公開のサムネを **1_H_v1**（地を暗く・字を明るく・赤を太く＝`thumb_jiko.ep21_v1_ground()`）に差し替えた（元の H は 176cd349…）
THUMB = "out/thumb/ep21-ab/ep21_1_H_v1.png"
THUMB_MD5 = "e70536496767ad874e6be4c15c7d85d1"   # ⑥（10-13）`thumb_jiko.py ep21` で焼いた＝比べた見本 v1 と画素まで同じ


def read_glossary() -> str:
    """`ref/ep21/yougo.md` の「## 貼る本文」の節を**そのまま**返す（次の `---` か `## ` まで）。"""
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


def _walk(v):
    """SPEC の値を辿って、素材の道（`ep21/…`）を全部出す（尻・頭の差し込み・over も含む）。"""
    if isinstance(v, str):
        if v.startswith("ep21/"):
            yield v
    elif isinstance(v, dict):
        for x in v.values():
            yield from _walk(x)
    elif isinstance(v, (list, tuple)):
        for x in v:
            yield from _walk(x)


# 画面の出典表記 → 種類（名乗れないものは None）。⚠️ 並びに意味がある（上から当てる）
KINDS = [
    ("pg_ntsb", r"^出典：NTSB .+便の飛行経路の調べ（2002年） PDF \d+頁／パブリックドメイン・切出$"),
    ("pg_comm", r"^出典：9\.11委員会報告書（2004年） \d+頁／パブリックドメイン・切出$"),
    ("pg_rg237", r"^出典：米連邦航空局のレーダーの再生（米国立公文書館 RG237）／パブリックドメイン・切出$"),
    ("loc_c2", r"^出典：米議会図書館蔵（撮影者不詳・パブリックドメイン）$"),
    ("loc_d", r"^出典：.+（米議会図書館蔵／知られた制限なし）$"),
    ("highsmith", r"^出典：Carol M\. Highsmith（米議会図書館蔵・パブリックドメイン）$"),
    ("cc0", r"^出典：.+（CC0）$"),
    ("pd_self", r"^出典：Tshevlin（パブリックドメイン）$"),
    ("ccbysa", r"^出典：.+／CC BY-SA 3\.0／改変なし$"),
    ("ccby", r"^出典：.+／CC BY (2\.0|2\.0 de|3\.0)／改変：切出$"),
    ("us_gov", r"^出典：(米空軍|米海軍|米海兵隊|米国防総省|米連邦緊急事態管理庁（FEMA・|米連邦航空局（FAA・|米環境保護庁（DOCUMERICA・|NASA|ジョージ・W・ブッシュ大統領図書館).*パブリックドメイン）$"),
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
    films = OrderedDict()
    for cid, u in F.USE.items():
        k = u["clip"]
        c = clips.get(k)
        if c is None:
            bad.append(f"{cid}:{k}（clips.json に無い）")
            continue
        if not c.get("credit", "").startswith("出典："):
            bad.append(f"{cid}:{k}（映像の出典の表記が無い）")
        films.setdefault(k, c)
    if bad:
        raise SystemExit(f"🔴 名乗れない素材がある。書かずに止めた: {bad}")
    counts = {k: len(v) for k, v in got.items()}
    counts.update(film=len(films))
    print(f"■ 素材（配線から）：{counts}")
    if N_COUNTS is not None and counts != N_COUNTS:
        raise SystemExit(f"🔴 点数が⑥で数えた値 {N_COUNTS} と違う。文の点数を当て直すこと。書かずに止めた。")
    return got, films, counts


LIC_URL = {"CC BY 2.0": "https://creativecommons.org/licenses/by/2.0/",
           "CC BY 2.0 de": "https://creativecommons.org/licenses/by/2.0/de/",
           "CC BY 3.0": "https://creativecommons.org/licenses/by/3.0/",
           "CC BY-SA 3.0": "https://creativecommons.org/licenses/by-sa/3.0/"}


def _who(s):
    """「出典：名前（…）」「出典：名前／CC…」→ 名前。"""
    body = s.split("：", 1)[1]
    return re.split(r"（|／", body, maxsplit=1)[0].strip()


def _pid(pid, key):
    """`assets.json` の鍵（ep21/ と拡張子を外した形）で Commons の頁の番号の URL。"""
    if key not in pid:
        raise SystemExit(f"🔴 {key} の Commons の頁の番号が無い（qa_out/ep21_commons_pageids.json）。書かずに止めた。")
    return pid[key]["url"]


def read_credits() -> str:
    got, films, n = used_material()
    pid = json.loads(PAGEIDS.read_text(encoding="utf-8"))
    key = lambda p: re.sub(r"\.(jpe?g|png)$", "", p.split("ep21/", 1)[1])      # noqa: E731
    out = ["【写真・映像・頁】"]
    # A＝米連邦の職務（17 U.S.C. §105）
    gov = OrderedDict()
    for p, (cid, s) in (got.get("us_gov") or {}).items():
        gov[_who(s)] = gov.get(_who(s), 0) + 1
    vid = OrderedDict()
    for k, c in films.items():
        if "CC BY" in c["credit"]:
            continue
        vid[_who(c["credit"])] = vid.get(_who(c["credit"]), 0) + 1
    out.append("・アメリカの連邦の機関が職務で撮った写真 " + "・".join(f"{w} {m}点" for w, m in gov.items())
               + "、映像 " + "・".join(f"{w} {m}本" for w, m in vid.items()) + "＝パブリックドメイン")
    dv = [c["url"] for k, c in films.items() if c.get("src") == "dvids"]
    if dv:
        out.append("　米空軍の映像（DVIDS）　" + "　".join(dv))
    if got.get("loc_c2"):
        out.append(f"・米議会図書館蔵の写真 {len(got['loc_c2'])}点（撮影者不詳・撮影者が権利を放棄した写真＝パブリックドメイン）")
    if got.get("highsmith"):
        out.append(f"・Carol M. Highsmith の写真 {len(got['highsmith'])}点（米議会図書館蔵・パブリックドメイン）")
    # D・自主宣言（CC0・PD）は帰属の表示が要らない＝名前と点数だけ（説明の 5,000字に収めるため頁の URL は CC だけに付ける）
    if got.get("loc_d"):
        by = OrderedDict()
        for p, (cid, s) in got["loc_d"].items():
            by[_who(s)] = by.get(_who(s), 0) + 1
        out.append("・米議会図書館蔵の写真（知られた制限なし）：" + "・".join(f"{w} {m}点" for w, m in by.items()))
    pdx = [(p, s) for k in ("pd_self", "cc0") for p, (cid, s) in (got.get(k) or {}).items()]
    if pdx:
        by = OrderedDict()
        for p, s in pdx:
            lic = "CC0" if "CC0" in s else "パブリックドメイン"
            by[(_who(s), lic)] = by.get((_who(s), lic), 0) + 1
        out.append("・" + "・".join(f"{w} の写真 {m}点（{lic}）" for (w, lic), m in by.items()))
    # CC BY はライセンスごとに1行（作者・点数・ライセンスの URL・改変・Commons の頁）
    by = OrderedDict()
    for p, (cid, s) in (got.get("ccby") or {}).items():
        lic = re.search(r"／(CC BY [^／]+)／", s).group(1)
        by.setdefault(lic, OrderedDict()).setdefault(_who(s), []).append(_pid(pid, key(p)))
    for lic, ws in by.items():
        out.append(f"・{lic}（{LIC_URL[lic]}）・切り出し：" + "・".join(f"{w} の写真 {len(u)}点" for w, u in ws.items())
                   + "　" + "　".join(u for us in ws.values() for u in us))
    for p, (cid, s) in (got.get("ccbysa") or {}).items():
        out.append(f"・{_who(s)} の写真 1点＝CC BY-SA 3.0（{LIC_URL['CC BY-SA 3.0']}）・加工なし・額に入れて表示　"
                   + _pid(pid, key(p)))
    for k, c in films.items():
        if "CC BY-SA" in c["credit"]:
            out.append(f"・{_who(c['credit'])} の映像（1999年9月の世界貿易センター）＝CC BY-SA 3.0"
                       f"（{LIC_URL['CC BY-SA 3.0']}）・加工なし・額に入れて表示・一部の区間　" + _pid(pid, "clip_" + k))
    pg = (n.get("pg_ntsb", 0), n.get("pg_comm", 0), n.get("pg_rg237", 0))
    out.append(f"・NTSB の飛行経路の調べの頁 {pg[0]}枚・9.11委員会報告の頁 {pg[1]}枚・アメリカ国立公文書館（NARA）所蔵 RG237"
               f" 連邦航空局のレーダーの再生の画面 {pg[2]}枚＝パブリックドメイン・切り出し　https://catalog.archives.gov/id/7419198")
    out.append("※ 画面に「イメージ」と出る写真は、その日・その便を写したものではありません")
    out.append("※ アメリカの国の機関の資料を使っていますが、これらの機関がこの動画を作ったり、推奨・支持したりしているものではありません")
    return "\n".join(out)


def chapters() -> str:
    starts, t = {}, 0.0
    for cid, sec in S.CUTS:
        starts[cid] = t
        t += sec
    rows = [(S.CUTS[0][0], "はじめに")]     # つかみ（c1）は章の印なし＝0:00 を足す
    for key, (n, name) in S.CHAPTERS.items():
        first = next((c for c, _ in S.CUTS
                      if c.startswith(key) and c[len(key):].isdigit()), None)
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
    desc = "\n".join([HEAD, chapters(), "", read_glossary(), "", PRIMARY, "", read_credits(), "", TAIL])
    # 🔴 入れてはいけない語（BGM のクレジット・伏せ字・ゆっくりの一文・煽り語・旧版の数）
    for bad in ("<", ">", "BGM", "DOVA", "OpenTracks", "陰鬱な灰色", "ﾀﾋ", "ゆっくりボイス",
                "AquesTalk", "即死", "絶命", "地獄", "陰謀", "撃墜", "2,973人が亡くなった", "Mike Goad"):
        if bad in desc or bad in TITLE:
            raise SystemExit(f"🔴 入れてはいけない語「{bad}」が入っている。書かずに止めた。")
    for bad in ("死亡",):
        if bad in TITLE or bad in desc:
            raise SystemExit(f"🔴 「{bad}」が入っている。書かずに止めた。")
    if TITLE.startswith("【映像あり】") or "【映像あり】" in TITLE:
        raise SystemExit("🔴 【映像あり】は付けない回（④）。書かずに止めた。")
    if not TITLE.endswith("【事故検証】【ゆっくり解説】"):
        raise SystemExit("🔴 タイトルの末尾が「【事故検証】【ゆっくり解説】」でない（B4-8）。書かずに止めた。")
    print(f"タイトル {len(TITLE)} 字（上限 100 ／ 承認は {TITLE_LEN}）")
    print(f"説明     {len(desc)} 字（上限 5,000）")
    if len(TITLE) > 100 or len(desc) > 5000:
        raise SystemExit("🔴 上限を超えた。書かずに止めた。")
    if len(TITLE) != TITLE_LEN:
        raise SystemExit(f"🔴 承認した題（{TITLE_LEN}字）と字数が違う＝写し間違い。書かずに止めた。")

    meta = {
        "slug": "ep21",
        "title": TITLE,
        "description": desc,
        "tags": ["9.11", "アメリカ同時多発テロ", "2001年", "航空管制", "ハイジャック", "NORAD", "FAA",
                 "ユナイテッド93便", "アメリカン11便", "9.11委員会", "事故検証", "一次資料", "解説",
                 "ゆっくり解説", "ドキュメンタリー"],
        "thumbnail": THUMB,
        "genre": "jiko",
        "playlist": "",
    }
    if "--dry" in sys.argv:
        print("\n" + TITLE + "\n\n" + desc)
        return 0
    if N_COUNTS is None or THUMB_MD5 is None:
        raise SystemExit("🔴 点数（N_COUNTS）かサムネの md5（THUMB_MD5）がまだ決まっていない。書かずに止めた。")
    import hashlib
    p = HERE / THUMB
    if not p.exists() or hashlib.md5(p.read_bytes()).hexdigest() != THUMB_MD5:
        raise SystemExit(f"🔴 サムネが無いか、⑥で決めた物と違う: {THUMB}。書かずに止めた。")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✓ 書いた → {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
