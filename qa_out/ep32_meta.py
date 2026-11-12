# -*- coding: utf-8 -*-
"""32本目（USエアウェイズ1549便のハドソン川への着水）の `config/meta_ep32.json` を**機械で**組み立てる（2026-11-12・⑥）。

`qa_out/ep31_meta.py`（用語・目次・素材の点数・字数の網）を写し、素材の種類を32本目の出典の形に直した
（NTSB の報告書の頁・公開ドケットの調査の写真・連邦官報・Commons〈CC BY・BY-SA・CC0・PD〉・沿岸警備隊の映像・
FAA の管制の録音・Google の衛星写真・Pexels）。

🔴 手で書かない理由（ep7〜ep31 と同じ）
  ① 用語は `ref/ep32/yougo.md` の「## 貼る本文」の節が正本＝**そのまま**貼る。見出しの語が語りに出るかと、並びが語りに初めて出る順かを当てる
  ② 素材の点数は**章ファイルの実配線**（`cuts.SPEC` の写真／`footage.USE` の映像）から数え、権利は**画面の出典表記**
     （`ref/ep32/credits.json`・`clips.json`・衛星写真は `cuts.ss.SAT`）で照らす。名乗れない素材が出たら落ちる
  ③ 目次は `scene_jiko.CUTS` の秒を頭から積む＝**焼いた版と同じ秒**
  ④ タイトル 100字・説明 5,000字の上限と、入れてはいけない語を、書く前に確かめる

🔴 この回の線（台本 §1-4・記憶 project-jiko-ep32-us1549）
  - 説明に人の名前を書かない（機長と副操縦士の名前も説明には要らない）。Commons の作者だけは権利の表示＝git の外の表から
    `scene_jiko._ep32_person` で足す（`config/` は gitignore・`--dry` の写しは commit しない）
  - 「犠牲」「死亡」を使わない（全員が生きて帰った回）

    python -P qa_out/ep32_meta.py            # 組み立てて config/meta_ep32.json に書く
    python -P qa_out/ep32_meta.py --dry      # 書かずに中身と字数だけ出す
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

YOUGO = HERE / "ref" / "ep32" / "yougo.md"
CREDITS_JSON = HERE / "ref" / "ep32" / "credits.json"
ASSETS_JSON = HERE / "ref" / "ep32" / "assets.json"
CLIPS = HERE / "ref" / "ep32" / "clips.json"
OUT = HERE / "config" / "meta_ep32.json"

N_GLOSS = 12          # `ref/ep32/yougo.md` の「貼る本文」の語数（台本 §8 の12語）
# ⚠️ ⑥（11-12）の配線から数えた点数（変わったら止まる＝文の点数を当て直す）。None＝数えて出すだけ
N_COUNTS = {"own": 23, "pd_gov": 9, "report": 19, "sat": 8, "cc0": 4, "org_by": 2, "stock": 59, "docket": 13, "fr": 1,
            "vts_clips": 3, "vts_cuts": 13, "orig": 1}

# ✅ 承認①（11-10 カズヤくん「推奨どおり」）の題 A'（台本 第2版 §1-1・70字）。
#    【映像あり】＝沿岸警備隊の監視カメラの映像（PD-USCG・384×288）＝ルール 1-8 の例外（32本目だけ・承認①）
TITLE = ("【映像あり】ハドソン川の奇跡の真相。判断の35秒を足して空港へ戻るシミュレーターの試しは、"
         "滑走路に届かなかった。【事故検証】【ゆっくり解説】")
TITLE_LEN = 70        # 決めた題の字数（写し間違いの網）

# ⚠️ 本文（台本第2版 c101〜c108・§1-2 の3つの問い）で言っていることだけを書く
HEAD = """【この動画について】
2009年1月15日の午後、ニューヨークのラガーディア空港を飛び立ったUSエアウェイズ1549便（エアバスA320）は、飛び立って1分半あまりで鳥の群れとぶつかり、両方のエンジンの力を、ほとんど失いました。鳥とぶつかってから約3分半後、機体はハドソン川に降り、乗っていた乗客150人と乗員5人の155人は、全員が生きて帰りました（重いけがをした人は5人）。

事故を調べたアメリカの国家運輸安全委員会（NTSB）の報告書は、空港をめざさず、川に降りた機長の判断が、生き残る見込みをいちばん高くした、と結論しています。事故のあとのシミュレーターの試しで、空港に降りられたのは、どれも、鳥とぶつかった直後に曲がった回でした。判断の35秒を足した1回は、滑走路に届きませんでした。報告書は「奇跡」という言葉を使わず、成功の多くは「一連の偶然」による、と書いています。
本当に、空港へは戻れなかったのか。3ページの手順書は、なぜ約3分の1で終わったのか。報告書は、成功の何を「偶然」と書き、その偶然に頼らないために、何を求めたのか。NTSBの報告書と調査の記録（公開ドケット）をもとに、順にたどります。
"""

# 11-12 に開けることを確かめたアドレス（ドケットの頁は中身に DCA09MA026 があることも確かめた）
WINDOW = """【資料の置き場】
・NTSB 事故調査報告書 NTSB/AAR-10/03（PDF）　https://www.ntsb.gov/investigations/AccidentReports/Reports/AAR1003.pdf
・NTSB 公開ドケット DCA09MA026（調査の記録）　https://data.ntsb.gov/Docket?ProjectID=73240
・NTSB 勧告のデータベース CAROL（勧告の番号 A-10-062〜095・A-09-112 で探せます）　https://data.ntsb.gov/carol-main-public/basic-search
・連邦官報 2023-06413（FAA の規則）　https://www.govinfo.gov/content/pkg/FR-2023-04-04/html/2023-06413.htm
"""

# 台本第2版の出典の欄の略（報・ド・勧・官・観・通・業・聞）と `ref/ep32/sources.md` から
PRIMARY = """【出典】
・NTSB 事故調査報告書「NTSB/AAR-10/03」（2010年5月4日採択）
・NTSB 公開ドケット DCA09MA026（聴取の要約、シミュレーターの試しの記録、調査の写真 ほか）
・NTSB 勧告のデータベース CAROL
・連邦官報 2023-06413（FAA の規則・2023年4月4日）
・ノースカロライナ州の観光の案内（Visit NC・サレンバーガー航空博物館の頁）
・AP 通信の記事（2016年9月・PBS の頁に転載）
・航空の業界紙 AIN（2023年1月13日・博物館の改名）
・当時の報道（州知事の会見の言葉）
"""

# ⚠️ ⑥ の頭（11-12 09:36）に CAROL の35本と観光の案内の頁を取り直して当て直した（ref/ep32/sources.md §10）。
#    公開の直前にもう一度当てて RECHECK を直す（記録＝ref/ep32/sources.md §10）
RECHECK = "11月12日"
TAIL = f"""動画に出てくる数字と日付は、NTSBの報告書と公開ドケット、勧告のデータベース、連邦官報によります（公開前の{RECHECK}に、勧告の状態と博物館の案内を見直しました）。
※ 勧告の状態は、2026年{RECHECK}に NTSB のデータベース（CAROL）で確かめたものです。
※ 操縦室と管制の言葉は、報告書の書き起こし（付録B）からの引用です。
※ メートル・キロ・時速は、報告書のフィート・マイル・ノットから換算した目安です。
※ 乗客、客室乗務員、管制官、救助にあたった方のお名前は出していません（立場でお伝えしています）。
※ 画面の模式図と地図の線は、公の記録をもとに描いた図です。"""

# ✅ 11-12 カズヤくん：H 反転版の1回目4枚（推奨 A×c26）→「c26の背景写真をもっと拡大して飛行機が大きく見えるように表示」
#    → 寄せ 1.5／1.75／2.0倍（推奨 1.75）→「2倍」＝`qa_out/ep32_thumb_hx.py zooms` の z200（上の行 A＝乗員乗客155人／全員生還）
THUMB = "out/thumb/ep32/ep32_Hinv_Ac26_z200.png"
THUMB_MD5 = "eaf74635121d9236b32bfcf492b19b4e"
THUMB_SRC = "ep32/c26.jpg"   # 地の写真（ref の下の道）。CC BY なら作者・ライセンス・改変を説明に書く
THUMB_NOTE_FMT = "※ サムネイルの写真：{who}／Wikimedia Commons（{lic}）。切り出し、文字入れ、色の調整をしています。"

TAGS = ["ハドソン川の奇跡", "USエアウェイズ1549便", "US Airways Flight 1549", "エアバスA320", "バードストライク", "着水",
        "ハドソン川", "ラガーディア空港", "NTSB", "航空事故", "2009年", "ニューヨーク", "シミュレーター", "事故検証", "ゆっくり解説", "解説"]

LIC_URL = {"CC BY 2.0": "https://creativecommons.org/licenses/by/2.0/deed.ja",
           "CC BY 2.5": "https://creativecommons.org/licenses/by/2.5/deed.ja",
           "CC BY 3.0": "https://creativecommons.org/licenses/by/3.0/deed.ja",
           "CC BY 4.0": "https://creativecommons.org/licenses/by/4.0/deed.ja",
           "CC BY-SA 2.0": "https://creativecommons.org/licenses/by-sa/2.0/deed.ja",
           "CC BY-SA 3.0": "https://creativecommons.org/licenses/by-sa/3.0/deed.ja",
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
    """`ref/ep32/yougo.md` の「## 貼る本文」の節を**そのまま**返す（次の `---` か `## ` まで）。見出しの語が語りに出るかを当てる。"""
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
    """SPEC の値を辿って、素材の道（`ep32/…`）を全部出す（地に敷く写真も含む）。"""
    if isinstance(v, str):
        if v.startswith("ep32/"):
            yield v
    elif isinstance(v, dict):
        for x in v.values():
            yield from _walk(x)
    elif isinstance(v, (list, tuple)):
        for x in v:
            yield from _walk(x)


# 画面の出典表記（credits.json の値＝作者は印 {作者} のまま）→ 種類（名乗れないものは None）。⚠️ 並びに意味がある（上から当てる）
KINDS = [
    ("stock", r"^イメージ（Pexels）$"),
    ("report", r"^出典：NTSB「NTSB/AAR-10/03」（2010）[^／]*／改変：切出$"),
    ("fr", r"^出典：連邦官報 2023-06413（FAA・2023年）／改変：切出$"),
    ("docket", r"^写真：NTSB 公開ドケット DCA09MA026（[^）]+）(?:／改変：(?:切出|字にモザイク))?$"),
    ("pd_gov", r"^(?:写真|図)：(?:U\.S\. Army Corps of Engineers|U\.S\. Coast Guard|NTSB|FAA)（public domain）／Wikimedia Commons"
               r"(?:／改変：(?:切出|字にモザイク))?$"),
    ("org_by", r"^写真：US Army Corps of Engineers／Wikimedia Commons（CC BY 2\.0）／改変：切出$"),
    ("own", r"^写真：\{作者\}(?: at English Wikipedia)?／Wikimedia Commons（CC BY(?:-SA)? (?:[234]\.0|2\.5)）"
            r"／改変(?:なし|：切出(?:・字にモザイク)?)$"),
    ("cc0", r"^写真：\{作者\}／Wikimedia Commons（CC0）(?:／改変：(?:顔|字)にモザイク)?$"),
    ("sat", r"^地図：Google マップの衛星写真（帰属は地図の右下）$"),
]
# 映像（clips.json の credit）→ 種類
FILM_KINDS = [("vts", r"^映像：U\.S\. Coast Guard（public domain）／Wikimedia Commons")]


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
    """章ファイルの実配線から、写真・頁・衛星写真・映像・原音を数える。権利は画面の出典表記で照らす。"""
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
    origs = [cid for cid, sp in cuts.SPEC.items() if (sp or {}).get("orig")]
    if bad:
        raise SystemExit(f"🔴 名乗れない素材がある。書かずに止めた: {bad}")
    counts = {k: len(v) for k, v in got.items()}
    counts.update({f"{k}_clips": len(v) for k, v in films.items()})
    counts.update({f"{k}_cuts": sum(len(x) for x in v.values()) for k, v in films.items()})
    counts["orig"] = len(origs)
    print(f"■ 素材（配線から）：{counts}・原音のカット {origs}")
    if N_COUNTS is not None and counts != N_COUNTS:
        raise SystemExit(f"🔴 点数が⑥で数えた値 {N_COUNTS} と違う。文の点数を当て直すこと。書かずに止めた。")
    return got, counts


def read_credits() -> str:
    got, n = used_material()
    assets = json.loads(ASSETS_JSON.read_text(encoding="utf-8"))
    out = ["【写真・映像・音声】"]
    out.append(f"・映像＝アメリカ沿岸警備隊の監視カメラ（public domain・Wikimedia Commons）{n.get('vts_cuts', 0)}カット"
               f"（{n.get('vts_clips', 0)}本から切り出し・一部を拡大。毎秒3〜4コマの記録です）")
    if n.get("orig"):
        out.append("・管制の音声＝FAA の録音（public domain・Wikimedia Commons）の一部（1.55秒）")
    out.append(f"・NTSB の報告書の頁 {n.get('report', 0)}点・連邦官報の頁 {n.get('fr', 0)}点（切り出し）")
    out.append(f"・NTSB 公開ドケットの調査の写真 {n.get('docket', 0)}点（一部の字にモザイク）")
    out.append(f"・アメリカの陸軍工兵隊・沿岸警備隊・NTSB・FAA の写真と図（public domain・Wikimedia Commons）{n.get('pd_gov', 0)}点")
    # 個人と組織の名義（Commons・CC BY／BY-SA／CC0）＝作者・ライセンスごとにまとめる（名前は git の外の表から＝焼く道と同じ）
    by = OrderedDict()
    for k in ("org_by", "own", "cc0"):
        for p, (cid, s) in (got.get(k) or {}).items():
            st = Path(p).stem
            a = assets.get(st) or {}
            lic = "CC0" if k == "cc0" else re.search(r"（(CC BY(?:-SA)? (?:[234]\.0|2\.5))）", s).group(1)
            if a.get("lic") != lic:
                raise SystemExit(f"🔴 {st} のライセンスが台帳（{a.get('lic')}）と画面（{lic}）で違う。書かずに止めた。")
            if k == "org_by":
                who = "US Army Corps of Engineers"
            else:
                who = S._ep32_person(p, "{作者}") + (" at English Wikipedia" if " at English Wikipedia" in s else "")
            by.setdefault((who, lic), []).append(p)
    nc = sum(len(v) for v in by.values())
    out.append(f"・Wikimedia Commons の写真 {nc}点（一部は切り出し・字や顔にモザイク。写真ごとの作者・ライセンス・改変は画面の出典の行にも）")
    for (who, lic), ps in by.items():
        out.append(f"　{who}（{lic}）" + (f"{len(ps)}点" if len(ps) > 1 else ""))
    used_lic = sorted({lic for (_, lic) in by if lic in LIC_URL})
    out.append("　ライセンス：" + "　".join(f"{lic} {LIC_URL[lic]}" for lic in used_lic))
    if n.get("sat"):
        out.append(f"・地図の衛星写真 {n['sat']}点＝Google マップ（帰属は地図の右下）")
    out.append(f"※ 画面に「イメージ」と出る写真（{n.get('stock', 0)}点）は、フリー素材（Pexels）です。その日・その場を写したものではありません")
    out.append("※ アメリカの国の機関（NTSB・FAA・沿岸警備隊・陸軍工兵隊）の資料を使っていますが、"
               "これらの機関がこの動画を作ったり、推奨・支持したりしているものではありません")
    return "\n".join(out)


def chapters() -> str:
    starts, t = {}, 0.0
    for cid, sec in S.CUTS:
        starts[cid] = t
        t += sec
    rows = [(S.CUTS[0][0], "はじめに")]     # つかみ（冒頭13カット）は章の印なし＝0:00 を足す
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


def thumb_note() -> str:
    if not THUMB_SRC:
        return ""
    a = json.loads(ASSETS_JSON.read_text(encoding="utf-8"))[Path(THUMB_SRC).stem]
    lic = a["lic"]
    if lic.startswith("PD"):
        return ""                                   # PD＝表示の義務なし（本編の出典の行と同じく画面の外では書かない）
    if "SA" in lic:
        raise SystemExit("🔴 サムネの地が BY-SA＝字を重ねると翻案（サムネ自体が BY-SA になる）。書かずに止めた。")
    return THUMB_NOTE_FMT.format(who=S._ep32_person(THUMB_SRC, "{作者}"), lic=lic)


def main() -> int:
    tn = thumb_note()
    tail = TAIL + ("\n" + tn if tn else "")
    desc = "\n".join([HEAD, WINDOW, chapters(), "", read_glossary(), "", PRIMARY, read_credits(), "", tail])
    # 🔴 入れてはいけない語（BGM のクレジット・ゆっくりの一文・煽り語・印の残り）
    for bad in ("<", ">", "BGM", "DOVA", "OpenTracks", "ゆっくりボイス", "AquesTalk", "即死", "絶命", "地獄",
                "【映像あり】", "{作者}", "{帰属}", "{個人}", S.EP23_AUTHOR_STANDIN):
        if bad in desc:
            raise SystemExit(f"🔴 入れてはいけない語「{bad}」が説明に入っている。書かずに止めた。")
    # 🔴 この回の線＝「犠牲」「死亡」を使わない（全員が生きて帰った回）・説明に機長と副操縦士の名前も書かない
    for bad in ("死亡", "犠牲", "犯人", "チェスリー", "ジェフリー", "スカイルズ", "Sullenberger", "Skiles"):
        if bad in TITLE or bad in desc:
            raise SystemExit(f"🔴 「{bad}」が入っている。書かずに止めた。")
    for need in ("AAR1003.pdf", "ProjectID=73240", "carol-main-public", "2023-06413", "CC BY 2.0", "public domain"):
        if need not in desc:
            raise SystemExit(f"🔴「{need}」が無い（置き場と権利の表示）。書かずに止めた。")
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
    meta = {"slug": "ep32", "title": TITLE, "description": desc, "tags": TAGS, "thumbnail": THUMB,
            "genre": "jiko", "playlist": ""}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✓ 書いた → {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
