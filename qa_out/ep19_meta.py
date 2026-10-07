# -*- coding: utf-8 -*-
"""19本目（サーフサイドのマンション崩壊のリメイク）の `config/meta_ep19.json` を**機械で**組み立てる（2026-10-07・⑥）。

`qa_out/ep18_meta.py` を写して、この回の形に合わせた。

🔴 手で書かない理由（ep7〜ep18 と同じ）
  ① 用語は `ref/ep19/yougo.md` の「## 貼る本文」の節が正本＝**そのまま**貼る（`**` だけ外す）
  ② 素材の点数は**章ファイルの実配線**（`cuts.SPEC` の写真・頁・スライド＝尻や頭の差し込みも含む／`footage.USE` の映像）から数え、
     権利は**画面の出典表記**（`ref/ep19/credits.json`・`clips.json`）で照らす。名乗れない素材が出たら落ちる
  ③ 目次は `scene_jiko.CUTS` の秒を頭から積む＝**焼いた版と同じ秒**（章の扉の2秒は CUTS に入っている）
  ④ タイトル 100字・説明 5,000字の上限と、入れてはいけない語を、書く前に確かめる

🔴 この回が 18本目と違うところ
  - 権利が4種類：NIST・FEMA（DVIDS）・DHS＝米国政府の職務著作（PD）／マイアミ・デイド郡消防と大陪審の報告・2018年の調査の報告
    ＝フロリダ州の公記録（決め①＝「PD」と書かない）／CC BY 2.0 の1点（Steve Jurvetson・色調を変更）／フリー素材（Pexels・Pixabay）
  - 【映像あり】を付ける（映像方針の決め⑦）＝先頭
  - つかみ（c1）は章の印なし＝目次の 00:00 は「はじめに」を足す（YouTube の目次は 0:00 から）
  - 末尾に ※ でリメイクと記す（旧版＝4本目・2026年9月公開）

    python qa_out/ep19_meta.py            # 組み立てて config/meta_ep19.json に書く
    python qa_out/ep19_meta.py --dry      # 書かずに中身と字数だけ出す
"""
import json
import re
import sys
from collections import Counter, OrderedDict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
import scene_jiko as S            # noqa: E402

YOUGO = HERE / "ref" / "ep19" / "yougo.md"
CREDITS_JSON = HERE / "ref" / "ep19" / "credits.json"
CLIPS = HERE / "ref" / "ep19" / "clips.json"
OUT = HERE / "config" / "meta_ep19.json"

N_GLOSS = 10          # `ref/ep19/yougo.md` の「貼る本文」の語数（⑥で語りに当てて確定）
# ⚠️ 下の値は⑥で配線から数えた点数（変わったら止まる＝文の点数を当て直す）。版 0dcaa9c（10-07）
N_COUNTS = {"nist": 23, "slide": 13, "fema": 4, "dhs": 2, "mdfr": 3, "ccby": 1,
            "page:マイアミ・デイド郡の大陪審の報告": 3, "page:モラビトの調査の報告": 1, "film": 12, "stock": 14}

# ✅ 台本第2版 §1-1（④'・10-06 カズヤくん承認・92字）。「死亡」は使わない・【映像あり】は先頭（決め⑦）
TITLE = ("【映像あり】崩落の前日の朝、床に約10センチの隙間を見た人がいた。"
         "柱の上の鉄筋は4本のはずが2本の所も、"
         "98人が亡くなったサーフサイドのマンション崩落の真相【事故検証】【ゆっくり解説】")
TITLE_LEN = 92

# ⚠️ 本文（台本第2版 c101〜c107）で言っていることだけを書く。問いは c107 の言い方
HEAD = """【この動画について】
2021年6月24日、午前1時22分。アメリカ・フロリダ州の海辺の町サーフサイドで、12階建てのマンション「シャンプレーン・タワーズ・サウス」の真ん中と東の部分が崩れ落ちました。立ったまま残ったのは、西の部分だけでした。136戸の建物で、98人が亡くなりました。

調べたアメリカの国の研究所 NIST は、壊れ始めは崩れる約3週間前とみられる、としています。傷みは何年も前から見えていて、2018年の調査の報告は、プールデッキなどの下のコンクリートが大きく傷んでいると書いていました。でも、弱さの大部分は、建てた時の設計と工事に、最初からありました。

この動画は、NIST の技術的知見の動画（2026年6月）と文字起こし・諮問委員会の資料（2026年9月）、マイアミ・デイド郡の大陪審の報告（2021年12月）、2018年の調査の報告と理事会の議事録などを、原文の英語で読んで作っています。時刻は現地の時刻、長さや重さはメートル法に直して伝えます。

・この夜、何が起きたのか
・なぜ、建って40年の建物が崩れたのか
・見えていた傷みは、なぜ止められなかったのか
"""

# 台本第2版 §10 の資料と `ref/ep19/sources.md`・`sources_add_2026-10-05.md` から（URL は sources の表の写し）
PRIMARY = """【出典】
・NIST「Technical Findings in the NCST Investigation of the June 24, 2021, Partial Collapse of Champlain Towers South」（技術的知見の動画・2026年6月22日）　https://www.nist.gov/video/ncst-champlain-towers-south-investigation-technical-findings-june-2026
・同 文字起こし（2026年8月26日更新）　https://www.nist.gov/disaster-and-failure-studies/video-transcript-nists-technical-findings-ncst-investigation-june-24
・NIST 諮問委員会（NCST Advisory Committee）の資料（2026年9月23日）　https://www.nist.gov/system/files/documents/2026/09/23/03_MITRANI_BELL_NCSTAC_Sept2026_CTSupdate_FINAL.pdf
・NIST の発表（2021年7月16日・2024年11月21日・2025年6月・2026年6月22日）と記録映像（B-Roll）　https://www.nist.gov/disaster-and-failure-studies/champlain-towers-south-collapse/news-and-updates
・マイアミ・デイド郡の大陪審の報告（2021年12月15日・黒塗り版）　https://miamisao.com/wp-content/uploads/2022/03/Grand-Jury-Report-Spring-2021-Redacted.pdf
・2018年の建物の調査の報告（2018年10月8日・サーフサイド町が公開）　https://www.townofsurfsidefl.gov/docs/default-source/default-document-library/town-clerk-documents/champlain-towers-south-public-records/8777-collins-ave---structural-field-survey-report.pdf
・理事会の議事録（2018年11月15日・サーフサイド町が公開）　https://www.townofsurfsidefl.gov/docs/default-source/default-document-library/town-clerk-documents/champlain-towers-south-public-records/champlain-towers-south-board-meeting-november-15-2018.pdf
・サーフサイド町「Champlain Towers South News & Resources」　https://www.townofsurfsidefl.gov/departments-services/building/champlain-towers-south-news-and-resources
・マイアミ・デイド郡の発表（2021年7月4日）と「Tragedy in Surfside」（2022年）　https://www.miamidade.gov/global/government/mayor/state-of-the-county/2022/surfside.page
・FEMA「Federal Response to Surfside Building Collapse in Florida」（2021年7月17日）　https://www.fema.gov/fact-sheet/federal-response-surfside-building-collapse-florida
・米会計検査院 GAO-24-106558（2024年2月）　https://www.gao.gov/products/gao-24-106558
・フロリダ州の法律 SB 4-D（2022年）　https://www.flsenate.gov/Session/Bill/2022D/4D/BillText/er/PDF"""

TAIL = """動画に出てくる数値・日付・証言の言葉は、これらの記録によります。
記録が言い切っていないところは、画面でそのまま断っています。
※ 画面の再現イラスト・模式図・地図は、記録をもとに描いた図です。崩れていく順番の絵は、NIST の見立てにもとづく推定の絵です。
※ 亡くなった方、住民、関係者のお名前は出していません。
※ サムネイルは、NIST の記録映像（B-Roll #1・パブリックドメイン）のコマを切り出し、色調を整えて文字を重ねたものです。
※ この動画は、2026年9月に公開したサーフサイドの動画を、作り直したものです。"""

# ✅ 10-07 カズヤくん「旧版のまま」＝A は旧版 4本目と同じ物（`thumb_jiko.surfside()` の `ss_b_face_bars` を焼き直して
#    md5 まで一致＝`out/thumb/ss_b_face_bars.png` と同じ）。赤「98名犠牲 12階が数秒で」は NIST の資料に根拠の文が無いことを
#    添えて聞いたうえでの決め（台本 §1-2）。B1＝`out/thumb/ep19-ab/ep19_B1_docu.png`（公開のあとカズヤくんが手動で A/B に入れる）
THUMB = "out/thumb/ep19-ab/ep19_A_rival.png"
THUMB_MD5 = "75a8e9d2f51b0d61191fbf5f75e56306"

PD_MARK = "パブリックドメイン"
CC_BY_URL = "https://creativecommons.org/licenses/by/2.0/"
JURVETSON = ("Steve Jurvetson「Remains of the Collapsed Florida Surfside Condo (2021-10-04)」"
             "（Wikimedia Commons）＝CC BY 2.0（" + CC_BY_URL + "）・色調を変更")
DOCS = OrderedDict([("マイアミ・デイド郡の大陪審の報告", "大陪審の報告（2021年12月）"),
                    ("モラビトの調査の報告", "2018年の調査の報告（サーフサイド町が公開）")])


def read_glossary() -> str:
    """`ref/ep19/yougo.md` の「## 貼る本文」の節を**そのまま**返す（次の `---` か `## ` まで）。"""
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
    """SPEC の値を辿って、素材の道（`ep19/…`）を全部出す（尻・頭の差し込み・over も含む）。"""
    if isinstance(v, str):
        if v.startswith("ep19/"):
            yield v
    elif isinstance(v, dict):
        for x in v.values():
            yield from _walk(x)
    elif isinstance(v, (list, tuple)):
        for x in v:
            yield from _walk(x)


def _kind(stem: str, s: str):
    """画面の出典表記 → 種類（名乗れないものは None）。"""
    if stem.startswith("pg"):
        for d in DOCS:
            if s.startswith("出典：" + d):
                return "page:" + d
        return None
    if "技術的知見の動画のスライド" in s or "諮問委員会の資料" in s:
        return "slide"
    if "NIST" in s and PD_MARK in s:
        return "nist"
    if "FEMA" in s and PD_MARK in s:
        return "fema"
    if "DHS" in s and PD_MARK in s:
        return "dhs"
    if "マイアミ・デイド郡消防（フロリダ州の公記録）" in s:
        return "mdfr"
    if "Steve Jurvetson（CC BY 2.0）" in s:
        return "ccby"
    return None


def used_material():
    """章ファイルの実配線から、写真・スライド・頁・映像・フリー素材を数える。権利は画面の出典表記で照らす。"""
    import cuts
    import footage as F
    cred = json.loads(CREDITS_JSON.read_text(encoding="utf-8"))
    clips = json.loads(CLIPS.read_text(encoding="utf-8"))
    got, bad = OrderedDict(), []
    for cid, sp in cuts.SPEC.items():
        for p in _walk(sp):
            if not re.search(r"\.(jpe?g|png)$", p, re.I):
                continue
            # 動く映像の控えの静止画（`fb_<cid>`）は取れなかったときだけ出る＝本番は映像
            if Path(p).stem.startswith("fb_"):
                continue
            s = cred.get(p)
            if s is None:
                bad.append(f"{cid}:{p}（credits.json に無い）")
                continue
            k = _kind(Path(p).stem, s)
            if k is None:
                bad.append(f"{cid}:{p}（名乗れない：{s}）")
                continue
            got.setdefault(k, OrderedDict()).setdefault(Path(p).stem, (cid, s))
    films, stock = OrderedDict(), OrderedDict()
    for cid, u in F.USE.items():
        k = u["clip"]
        c = clips.get(k)
        if c is None:
            bad.append(f"{cid}:{k}（clips.json に無い）")
            continue
        if c.get("stock"):
            if "イメージ（フリー素材）" not in c.get("credit", "") or not c.get("author"):
                bad.append(f"{cid}:{k}（フリー素材の出典表記か撮影者が無い）")
            stock.setdefault(k, c)
        else:
            if not c.get("credit", "").startswith("出典：NIST"):
                bad.append(f"{cid}:{k}（映像が NIST でない：{c.get('credit')}）")
            films.setdefault(k, c)
    if bad:
        raise SystemExit(f"🔴 名乗れない素材がある。書かずに止めた: {bad}")
    counts = {k: len(v) for k, v in got.items()}
    counts.update(film=len(films), stock=len(stock))
    print(f"■ 素材（配線から）：{counts}")
    if N_COUNTS is not None and counts != N_COUNTS:
        raise SystemExit(f"🔴 点数が⑥で数えた値 {N_COUNTS} と違う。文の点数を当て直すこと。書かずに止めた。")
    return got, films, stock, counts


def read_credits() -> str:
    got, films, stock, n = used_material()
    by_site = OrderedDict()
    for k, c in stock.items():
        site = c["credit"].split("：", 1)[1].split("／")[0].strip()
        by_site.setdefault(site, [])
        if c["author"] not in by_site[site]:
            by_site[site].append(c["author"])
    pages = Counter(k.split(":", 1)[1] for k in got if k.startswith("page:") for _ in got[k])
    out = ["【写真・スライド・映像・頁】"]
    out.append(f"・NIST（アメリカ国立標準技術研究所）の写真 {n.get('nist', 0)}点・技術的知見の動画と諮問委員会の資料のスライド "
               f"{n.get('slide', 0)}枚・記録映像（B-Roll・タイムラプス ほか）{n['film']}本"
               "＝米国政府の職務著作（パブリックドメイン）。スライドの一部は、下地の図（管財人の原図・町の図面）"
               "と映像のコマ（© 2021 Used with permission）を引用しています")
    out.append(f"・FEMA（DVIDS）の写真 {n.get('fema', 0)}点・米国土安全保障省（DHS）の写真 {n.get('dhs', 0)}点"
               "＝米国政府の職務著作（パブリックドメイン）")
    out.append(f"・マイアミ・デイド郡消防の写真 {n.get('mdfr', 0)}点＝フロリダ州の公記録（Wikimedia Commons）")
    if n.get("ccby"):
        out.append("・" + JURVETSON)
    out.append("・報告書の頁：" + "・".join(f"{DOCS[d]} {pages[d]}枚" for d in DOCS if pages[d]))
    out.append("※ 米国の政府機関（NIST・FEMA・国土安全保障省）の写真と映像を使っていますが、"
               "これらの機関がこの動画を推奨・支持していることを意味するものではありません")
    out.append(f"【映像（イメージ）】フリー素材 {n['stock']}本＝本編の画面に「イメージ（フリー素材）」と出した映像です"
               "（実際の記録ではありません）")
    for site, who in by_site.items():
        out.append(f"・{site}：" + "、".join(who))
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
    # 🔴 入れてはいけない語（BGM のクレジット・伏せ字・ゆっくりの一文＝14本目だけ・煽り語・旧版の BGM の名）
    for bad in ("<", ">", "BGM", "DOVA", "OpenTracks", "陰鬱な灰色", "蒲鉾", "ﾀﾋ", "ゆっくりボイス",
                "AquesTalk", "即死", "絶命", "地獄", "再認証", "数秒で"):
        if bad in desc or bad in TITLE:
            raise SystemExit(f"🔴 入れてはいけない語「{bad}」が入っている。書かずに止めた。")
    for bad in ("死亡",):
        if bad in TITLE or bad in desc:
            raise SystemExit(f"🔴 「{bad}」が入っている。書かずに止めた。")
    if not TITLE.startswith("【映像あり】"):
        raise SystemExit("🔴 【映像あり】が先頭に無い（決め⑦）。書かずに止めた。")
    if not TITLE.endswith("【事故検証】【ゆっくり解説】"):
        raise SystemExit("🔴 タイトルの末尾が「【事故検証】【ゆっくり解説】」でない（B4-8）。書かずに止めた。")
    print(f"タイトル {len(TITLE)} 字（上限 100 ／ 承認は {TITLE_LEN}）")
    print(f"説明     {len(desc)} 字（上限 5,000）")
    if len(TITLE) > 100 or len(desc) > 5000:
        raise SystemExit("🔴 上限を超えた。書かずに止めた。")
    if len(TITLE) != TITLE_LEN:
        raise SystemExit(f"🔴 承認した題（{TITLE_LEN}字）と字数が違う＝写し間違い。書かずに止めた。")

    meta = {
        "slug": "ep19",
        "title": TITLE,
        "description": desc,
        "tags": ["サーフサイド", "シャンプレーン・タワーズ", "Champlain Towers South", "マンション崩落", "NIST",
                 "押し抜きせん断", "鉄筋コンクリート", "大陪審", "フロリダ", "2021年", "事故検証", "図解", "一次資料",
                 "解説", "ゆっくり解説"],
        "thumbnail": THUMB,
        "genre": "jiko",
        "playlist": "",
    }
    if "--dry" in sys.argv:
        print("\n" + TITLE + "\n\n" + desc)
        return 0
    if N_COUNTS is None or THUMB is None:
        raise SystemExit("🔴 点数（N_COUNTS）かサムネ（THUMB）がまだ決まっていない。書かずに止めた。")
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
