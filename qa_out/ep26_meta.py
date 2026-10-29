# -*- coding: utf-8 -*-
"""26本目（タイタニック号沈没事故）の `config/meta_ep26.json` を**機械で**組み立てる（2026-10-28・⑥）。

`qa_out/ep25_meta.py`（用語・目次・点数・権利・字数の網）を写して、この回の形に合わせた。

🔴 手で書かない理由（ep7〜ep25 と同じ）
  ① 用語は `ref/ep26/yougo.md` の「## 貼る本文」の節が正本＝**そのまま**貼る（`**` だけ外す）。
     見出しの語が語り（`narration.SCRIPT`）に出るかと、並びが語りに初めて出る順かを1語ずつ当てる
  ② 素材の点数は**章ファイルの実配線**（`cuts.SPEC` の写真と頁／`footage.USE` の映像）から数え、
     権利は**画面の出典表記**（`ref/ep26/credits.json`・`clips.json`・`cuts.ss.SAT`）で照らす。名乗れない素材が出たら落ちる
  ③ 目次は `scene_jiko.CUTS` の秒を頭から積む＝**焼いた版と同じ秒**（章の扉の秒は CUTS に入っている）
  ④ タイトル 100字・説明 5,000字の上限と、入れてはいけない語を、書く前に確かめる

🔴 この回のところ
  - 写真＝Commons ほかのパブリックドメイン（NARA・LOC・BnF・オランダ国立公文書館・北アイルランド国立博物館）・私人の顔の一部にモザイク
  - 頁＝英国の審問の報告（米国上院の刷り直し S. Doc. 933＝米国の公文書）・MAIB 1992（引用＝OGL v3.0 の帰属の文）・米国の法 37 Stat. 199
  - NOAA 2003 の写真（courtesy）の撮影者の名前は**公開リポに書かない**＝焼くときと同じく git の外の表 `ref/ep26/src/credits_private.tsv` から
    `scene_jiko._ep26_author` で足す（`config/` は gitignore＝説明の JSON は公開リポに入らない）
  - NOAA 2004 の残骸の映像（courtesy）・地図の衛星写真＝Google（帰属は地図の右下）・フリー素材の映像（Pexels）は「イメージ」の断りだけ
  - 🔴 言い切らない（記憶 project-jiko-ep26-titanic）：「救えなかった」は書かない・「見えていなかった」は c106 の次長の考え（帰属つき）の1回だけ・
    「1,500人」は使わない（英 1,490・米 1,517）・「死亡」は使わない
  - 人＝乗員・他の船の船長と航海士と通信士・審問の長は名前と役職／会社の人は役職だけ／乗客は名前なし（承認①）。【映像あり】は付けない

    python qa_out/ep26_meta.py            # 組み立てて config/meta_ep26.json に書く
    python qa_out/ep26_meta.py --dry      # 書かずに中身と字数だけ出す
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

YOUGO = HERE / "ref" / "ep26" / "yougo.md"
CREDITS_JSON = HERE / "ref" / "ep26" / "credits.json"
CLIPS = HERE / "ref" / "ep26" / "clips.json"
OUT = HERE / "config" / "meta_ep26.json"

N_GLOSS = 12          # `ref/ep26/yougo.md` の「貼る本文」の語数（台本 §8 の12語・見出しを語りの言い方に合わせた）
# ⚠️ 下の値は⑥（10-28）の配線（版 3dc05235）から数えた点数（変わったら止まる＝文の点数を当て直す）。None＝数えて出すだけ
N_COUNTS = {"cpd": 49, "nara": 3, "bnf": 2, "sat": 4, "hw": 2, "nl": 3, "g1": 9, "loc": 8, "noaa03": 2, "maib": 6, "law": 1,
            "noaa04": 13, "stock_film": 8, "mosaic": 6}

# ✅ 承認①（10-27）の題 A
TITLE = "タイタニック号沈没事故の真相。タイタニック号の白い信号弾を、北の方の船の甲板で8発数えた人たちがいた。【事故検証】【ゆっくり解説】"
TITLE_LEN = 65        # 決めた題の字数（写し間違いの網）＝10-29 試写のあとカズヤくんが「…の真相。」を頭へ（承認①の64字を並べ替え）

# ⚠️ 本文（台本第2版 c101〜c107）で言っていることだけを書く。🔴「救えたかもしれない」は1912年の審問の言葉・「見えていなかった」は次長の考え（どちらも帰属つき）
HEAD = """【この動画について】
1912年4月15日の未明、北大西洋。沈みかけたタイタニック号から、白い信号弾が打ち上げられました。助けを呼ぶ合図です。その光を、北の方にいた別の船から見ていた人たちがいました。カリフォルニアン号の船員たちです。その夜、タイタニック号では1,490人が亡くなりました（英国の審問が出した数）。

カリフォルニアン号は、夜のあいだ動きませんでした。1912年、英国の審問は、あの船が向かっていれば、多くの命を、もしかすると全員を救えたかもしれない、と書きました。

ところが80年後の1992年、英国の海難調査局がこの結論を調べ直すと、調べた2人の見方が割れました。外から呼ばれた調査官は、タイタニック号の姿も見えていた、と考えました。調査局の次長は、たぶん姿は見えていなかった、と考えました。

では、その船は、本当にみんなを救えたのか。この動画は、1912年と1992年の記録を起きた順にたどります。時刻は、どの船の時計かも添えて言います。
"""

# 台本第2版 §10（資料）と `ref/ep26/sources.md` の表（G1・G2・G4〜G7・T1〜T3・U1・N1・A1）から。⑥（10-28）URL は curl で開けるかを確かめる
PRIMARY = """【出典】
・英国の審問の報告（難破調査委員の正式調査・1912年7月30日）＝米国上院の刷り直し S. Doc. 933　https://www.govinfo.gov/content/pkg/SERIALSET-06179_00_00-019-0933-0000/pdf/SERIALSET-06179_00_00-019-0933-0000.pdf
・英国運輸省 海難調査局（MAIB）『RMS "TITANIC" Reappraisal of Evidence Relating to SS "CALIFORNIAN"』（1992年）　https://assets.publishing.service.gov.uk/media/54c15bf240f0b6158d000027/MAIBReport_ReappraisalOfEvidence-SSCalifornian-Titanic-1992.pdf
・米国上院 商務委員会の小委員会の公聴会 S. Doc. 726（1912年）　https://www.govinfo.gov/content/pkg/SERIALSET-06167_00_00-002-0726-0000/pdf/SERIALSET-06167_00_00-002-0726-0000.pdf
・英国の審問の証言と、米国上院の報告（S. Rept. 806）の書き起こし（有志のサイト Titanic Inquiry Project）　https://www.titanicinquiry.org/
・米国の法 37 Stat. 199（1912年）・37 Stat. 302（1912年）・36 Stat. 629（1910年）　https://www.govinfo.gov/link/statute/37/199　https://www.govinfo.gov/link/statute/37/302　https://www.govinfo.gov/link/statute/36/629
・米国沿岸警備隊の歴史の頁（国際氷山監視）　https://www.history.uscg.mil/Complete-Time-Line/Time-Line-1900-2000/
・NOAA Ocean Exploration（2003年・2004年の残骸の調査）　https://archive.oceanexplorer.noaa.gov/explorations/03titanic/welcome.html　https://archive.oceanexplorer.noaa.gov/explorations/04titanic/welcome.html
・米国立公文書館（NARA）の目録（水路部の日報ほか）　https://catalog.archives.gov/"""

TAIL = """動画に出てくる数値・時刻・言葉は、これらの記録によります。
報告書と証言の言い方（「たぶん」「〜かもしれない」など）は、原文の強さのまま訳しています。
※ 時刻は、その船の時計の時刻です（1912年の船の時計は、船ごとに少しずつ違います）。
※ 図の色：タイタニック号＝水色・カリフォルニアン号＝緑・アメリカ号＝橙・カルパチア号＝青
※ 画面の模式図・再現のイラスト・地図の線は、記録をもとに描いた図です。
※ 乗員と、ほかの船の船長・航海士・通信士、審問の長は名前と役職で、会社の人は役職だけでお呼びしています。乗客のお名前は出していません。"""

# ✅ ⑥（10-28）カズヤくん：A/B テスト＝A（Claude が貼る）＝生成 AI `gen_thumb_ai ttn_b`（案A「船尾が空へ立ち上がる」・誇張は承認の内）を
#    H 型の反転版・寄せなし・字の外 1.60（船尾に描かれた字のような印は `qa_out/ep26_thumb_hx.py fix` で消した）／B＝T1（S1-002・PD）はカズヤくんが Studio で手動
THUMB = "out/thumb/ep26/ep26_A_Hinv_ttn_b_fix_z100_b160.png"
THUMB_MD5 = "eecbd2e906f44f15aea88645545b94c8"
THUMB_NOTE = "※ サムネイルの夜の絵は、生成AIで作ったイメージです（実際の写真ではありません・場面は誇張しています）。"

TAGS = ["タイタニック号沈没事故", "タイタニック号", "タイタニック", "カリフォルニアン号", "1912年", "沈没事故", "海難事故",
        "英国の審問", "海難調査局", "事故検証", "一次資料", "ゆっくり解説", "ドキュメンタリー", "解説", "北大西洋"]

OGL = ("Contains public sector information licensed under the Open Government Licence v3.0. "
       "https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/")


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
    """`ref/ep26/yougo.md` の「## 貼る本文」の節を**そのまま**返す（次の `---` か `## ` まで）。見出しの語が語りに出るかを当てる。"""
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
    """SPEC の値を辿って、素材の道（`ep26/…`）を全部出す（尻・頭の差し込み・地に敷く写真も含む）。"""
    if isinstance(v, str):
        if v.startswith("ep26/"):
            yield v
    elif isinstance(v, dict):
        for x in v.values():
            yield from _walk(x)
    elif isinstance(v, (list, tuple)):
        for x in v:
            yield from _walk(x)


_MOS = r"(・改変：顔にモザイク)?$"
# 画面の出典表記（credits.json の値＝作者は印 {作者} のまま）→ 種類（名乗れないものは None）。⚠️ 並びに意味がある（上から当てる）
KINDS = [
    ("cpd", r"^Wikimedia Commons（パブリックドメイン）" + _MOS),
    ("loc", r"^出典：米国議会図書館（LOC）" + _MOS),
    ("nara", r"^出典：米国立公文書館（NARA）" + _MOS),
    ("nl", r"^出典：オランダ国立公文書館（Spaarnestad Photo）" + _MOS),
    ("bnf", r"^出典：フランス国立図書館（BnF）" + _MOS),
    ("hw", r"^出典：北アイルランド国立博物館（Harland & Wolff Collection）" + _MOS),
    ("g1", r"^出典：英国の審問の報告（米国上院の刷り直し S\. Doc\. 933）p\.\d+$"),
    ("maib", r'^英国海難調査局『RMS "TITANIC" Reappraisal of Evidence Relating to SS "CALIFORNIAN"』1992年 (p\.\d+ |表紙|送り状)より引用$'),
    ("law", r"^出典：米国の法 37 Stat\. 199（1912年7月23日）$"),
    ("noaa03", r"^Image courtesy of \{作者\}, RMS Titanic Expedition 2003, NOAA-OE\.$"),
    ("sat", r"^地図：Google マップの衛星写真（帰属は地図の右下）$"),
]
NOAA04 = "Video courtesy of the RMS Titanic Team Expedition 2004, ROI, IFE, NOAA-OE."


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
    for v in SS.SAT.values():                 # 衛星写真＝出典は表 SAT の credit（scene_jiko.ep26_credit と同じ）
        cred.setdefault(v["file"], v["credit"])
    clips = json.loads(CLIPS.read_text(encoding="utf-8"))
    got, bad, mosaic = OrderedDict(), [], set()
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
            if "顔にモザイク" in s:
                mosaic.add(p)
    films = {"noaa04": OrderedDict(), "stock_film": OrderedDict()}
    for cid, u in F.USE.items():
        k = u["clip"]
        c = clips.get(k)
        if c is None:
            bad.append(f"{cid}:{k}（clips.json に無い）")
            continue
        if c.get("credit", "") == "イメージ（Pexels）":
            films["stock_film"].setdefault(k, c)
        elif c.get("credit", "") == NOAA04:
            films["noaa04"].setdefault(cid, c)     # NOAA 2004 は1本の素材から13区間＝カットで数える
        else:
            bad.append(f"{cid}:{k}（名乗れない映像の出典：{c.get('credit')}）")
    if bad:
        raise SystemExit(f"🔴 名乗れない素材がある。書かずに止めた: {bad}")
    counts = {k: len(v) for k, v in got.items()}
    counts.update(noaa04=len(films["noaa04"]), stock_film=len(films["stock_film"]), mosaic=len(mosaic))
    print(f"■ 素材（配線から）：{counts}")
    if N_COUNTS is not None and counts != N_COUNTS:
        raise SystemExit(f"🔴 点数が⑥で数えた値 {N_COUNTS} と違う。文の点数を当て直すこと。書かずに止めた。")
    return got, counts


def read_credits() -> str:
    got, n = used_material()
    pd = sum(n.get(k, 0) for k in ("cpd", "loc", "nara", "nl", "bnf", "hw"))
    out = ["【写真・頁・映像】",
           f"・写真 {pd}点＝パブリックドメイン（Wikimedia Commons {n.get('cpd', 0)}点・米国議会図書館 {n.get('loc', 0)}点・"
           f"米国立公文書館 {n.get('nara', 0)}点・オランダ国立公文書館 {n.get('nl', 0)}点・フランス国立図書館 {n.get('bnf', 0)}点・"
           f"北アイルランド国立博物館 {n.get('hw', 0)}点）。私人の顔が写る {n.get('mosaic', 0)}点は、顔にモザイクをかけています",
           f"・英国の審問の報告の頁 {n.get('g1', 0)}枚＝米国上院の刷り直し S. Doc. 933（米国の公文書）",
           f"・英国海難調査局の報告の頁 {n.get('maib', 0)}枚＝引用。{OGL}",
           f"・米国の法の頁 {n.get('law', 0)}枚＝37 Stat. 199（米国の公文書）"]
    names = []
    for p, (cid, s) in (got.get("noaa03") or {}).items():
        c = s.replace("{作者}", S._ep26_author(p))
        if c not in names:
            names.append(c)
    out.append(f"・海の底の写真 {n.get('noaa03', 0)}点＝" + "／".join(names))
    out.append(f"・海の底の映像 {n.get('noaa04', 0)}か所＝{NOAA04}")
    out.append(f"・地図の衛星写真 {n.get('sat', 0)}点＝Google マップ（帰属は地図の右下）")
    out.append(f"※ 画面に「イメージ」と出る映像（{n.get('stock_film', 0)}本）は、フリー素材です。その夜・その場を写したものではありません")
    out.append("※ 証言の一部は、有志のサイトの書き起こしによります（画面に「書き起こし・有志のサイト」と断っています）")
    out.append("※ 国や公的な機関（英国海難調査局・米国議会・米国立公文書館・米国議会図書館・NOAA・米国沿岸警備隊）と図書館・博物館の資料を使っていますが、"
               "これらの機関がこの動画を作ったり、推奨・支持したりしているものではありません")
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
    # 🔴 26本目＝言い切らない・数を割らない（記憶 project-jiko-ep26-titanic）
    for bad in ("死亡", "救えなかった", "1,500人", "1500人", "火箭"):
        if bad in TITLE or bad in desc:
            raise SystemExit(f"🔴 「{bad}」が入っている。書かずに止めた。")
    if desc.count("見えていなかった") != 1 or "次長は、たぶん姿は見えていなかった" not in desc:
        raise SystemExit("🔴 「見えていなかった」が c106 の次長の考え（帰属つき）の1回でない。書かずに止めた。")
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
    meta = {"slug": "ep26", "title": TITLE, "description": desc, "tags": TAGS, "thumbnail": THUMB,
            "genre": "jiko", "playlist": ""}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✓ 書いた → {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
