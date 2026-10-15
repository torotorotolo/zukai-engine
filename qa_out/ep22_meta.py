# -*- coding: utf-8 -*-
"""22本目（タイタン号のリメイク）の `config/meta_ep22.json` を**機械で**組み立てる（2026-10-15・⑥）。

`qa_out/ep21_meta.py` を写して、この回の形に合わせた。

🔴 手で書かない理由（ep7〜ep21 と同じ）
  ① 用語は `ref/ep22/yougo.md` の「## 貼る本文」の節が正本＝**そのまま**貼る（`**` だけ外す）。
     🆕 見出しの語が語り（`narration.SCRIPT`）に出るかを1語ずつ当てる（⑤a-1 の宿題＝見出しが本文の言い方と違った3語）
  ② 素材の点数は**章ファイルの実配線**（`cuts.SPEC` の写真・頁／`footage.USE` の映像）から数え、
     権利は**画面の出典表記**（`ref/ep22/credits.json`・`clips.json`・衛星写真は `cuts/ss.SAT`）で照らす。名乗れない素材が出たら落ちる
  ③ 目次は `scene_jiko.CUTS` の秒を頭から積む＝**焼いた版と同じ秒**（章の扉の秒は CUTS に入っている）
  ④ タイトル 100字・説明 5,000字の上限と、入れてはいけない語を、書く前に確かめる

🔴 この回が 21本目と違うところ
  - 権利：米連邦の職務（米沿岸警備隊・米運輸安全委員会の報告書の図・DVIDS の写真と映像）＝パブリックドメイン／
    第三者（Pelagic の ROV 映像・報告書に載った個人の写真2点）＝引用（出典を明記・額に入れて・改変なし）／
    NOAA と研究所の共同の写真（タイタニックの船首）＝額装／CC BY-SA 4.0（ホライゾン・アークティック）＝額装・改変なし／
    地図の衛星写真＝Google（帰属は地図の右下）
  - 【映像あり】を先頭に（映像方針の了承②）
  - 実名は CEO だけ（台本 §1-4）＝🔴 commit の前に `python ref/ep22/aq/namecheck_ceo22.py qa_out/ep22_meta.py ref/ep22/yougo.md`
  - 記録の音（NOAA の録音）・通信班の映像・遺族の映像は使わない（10-14）
  - 末尾に ※ でリメイクと記す（旧版＝1本目・2026年8月公開・10-13 に非公開）

    python qa_out/ep22_meta.py            # 組み立てて config/meta_ep22.json に書く
    python qa_out/ep22_meta.py --dry      # 書かずに中身と字数だけ出す
"""
import json
import re
import sys
import unicodedata
from collections import OrderedDict
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
import scene_jiko as S            # noqa: E402

YOUGO = HERE / "ref" / "ep22" / "yougo.md"
CREDITS_JSON = HERE / "ref" / "ep22" / "credits.json"
CLIPS = HERE / "ref" / "ep22" / "clips.json"
ASSETS = HERE / "ref" / "ep22" / "assets.json"
OUT = HERE / "config" / "meta_ep22.json"

N_GLOSS = 14          # `ref/ep22/yougo.md` の「貼る本文」の語数（台本 §8 の14語）
# ⚠️ 下の値は⑥で配線から数えた点数（変わったら止まる＝文の点数を当て直す）。None のあいだは数えて出すだけ
# ⑥（10-15）本編 r01（版 91c2490）の配線から数えた。⚠️ 試写の直し（cols の図の使いすぎ）で絵が変わったら数え直す
N_COUNTS = {"sat": 6, "noaa": 1, "mbi": 12, "ccbysa": 1, "dvids": 6, "mbi_other": 4, "lab": 9, "ntsb": 10,
            "third": 2, "film": 9}

# 🔴 承認①（2026-10-14）＝保留・最有力 A。⑥（10-15）でカズヤくんが自分の案に決めた（「題は私の案のまま」）。
#    決まりと割れる点（報告書は「傷んだ可能性が高い〈米2つ〉・決められない〈カナダ〉」・聞いたのは「中にいた人たちと海面の小舟の人たち」・
#    題だけ読むと事故当日の5人に読める恐れ）を伝えたうえでの選び＝選ばれた方で進める（記憶 feedback-jiko-thumbnail-rival-format の 10-13）
TITLE = ("【映像あり】船体が壊れる音を全員が聞いていた。"
         "タイタン号爆縮事故の真相【事故検証】【ゆっくり解説】")
TITLE_LEN = 49        # 決めた題の字数（写し間違いの網）

# ⚠️ 本文（台本第2版 c101〜c109・c203・c306）で言っていることだけを書く
HEAD = """【この動画について】
2023年6月22日、北大西洋、タイタニックの眠る深さ約3,800メートルの海の底で、無人の探査機のカメラが、潜水艇の尾部をとらえました。4日前に連絡が途絶えた潜水艇、タイタンの残骸でした。乗っていた5人は、全員が亡くなりました。潜水艇は、深い海の水の力に押しつぶされていました。

その11か月前、同じ潜水艇の中にいた人たちと、海面の小舟の人たちが、大きな音を聞いていました。会社は音の原因を「潜水艇が、枠の中でずれたため」とし、4日後、また潜りました。この動画は、アメリカ沿岸警備隊の海難調査委員会、アメリカの運輸安全委員会、カナダの運輸安全委員会がまとめた3つの報告書をもとに、次の3つの問いをたどります。

・この潜水艇は、深い海の中で、何が壊れたのか
・なぜ、潜り続けたのか
・そして、誰なら止められたのか

時刻はすべて、現地のニューファンドランドの夏の時間です（日本時間より11時間30分遅い）。長さや深さはメートル法に直して伝えます。
※ 事故のときの音の記録は鳴らしていません。潜水艇が壊れた瞬間を写した映像はありません。
"""

# 台本第2版 §10（資料）・旧版の概要欄（2冊の URL）から。⚠️ URL は⑥で開いて確かめる（TSB・ドケット）
PRIMARY = """【出典】
・アメリカ沿岸警備隊 海難調査委員会「Report of the Marine Board of Investigation into the Implosion of the Submersible TITAN」（2025年8月4日）　https://www.news.uscg.mil/News-by-Region/Headquarters/Titan-Submersible/
・アメリカ国家運輸安全委員会（NTSB）「Marine Investigation Report MIR-25-36」（2025年10月2日）　https://www.ntsb.gov/investigations/AccidentReports/Reports/MIR2536.pdf
・カナダ運輸安全委員会（TSB）「Marine Transportation Safety Investigation Report M23A0169」（2026年6月17日）　TSB_URL
・NTSB 研究所の報告 24-011（2024年7月5日・NTSB の調査の資料集＝ドケット DCA23FM036）　https://data.ntsb.gov/Docket/?NTSBNumber=DCA23FM036"""
# ⑥（10-15）内蔵ブラウザで開いて題を確かめた（curl は 403＝機械を断る作り・米沿岸警備隊の頁も同じ＝画面で「SUBMERSIBLE TITAN MBI REPORT (04AUG2025)」の載りを確かめた）
TSB_URL = "https://www.tsb-bst.gc.ca/eng/rapports-reports/marine/2023/m23a0169/m23a0169.html"

TAIL = """動画に出てくる数値・時刻・言葉は、これらの記録によります。
記録が言い切っていないところや、記録どうしで割れるところは、画面と語りでそのまま断っています。
※ 画面の地図・時刻の帯・模式図・断面の図は、記録をもとに描いた図です。
※ お名前を出しているのは、会社の CEO だけです。ほかの乗っていた方は、役割と人数でお伝えしています。
※ この動画は、2026年8月に公開したタイタン号の動画を、作り直したものです。
※ サムネイルの絵は、生成AIで作った再現のイメージです（実際の写真ではありません）。"""

# 🔴 ⑥（10-15）カズヤくん：国の写真の候補は「どれもイマイチ」→ OpenAI API で海底のタイタン号を再現した実写イラスト
#    （gen_thumb_ai titan_a・gpt-image-2.5-flare high 1枚）・上「乗員乗客5名 生還者なし」・まん中「タイタン号」（縦 1.8倍）・
#    下「最新の報告書」・本番は反転版・地は明るくしない（検品の所見＝尾部が横倒し〈実物は立った形〉を見たうえで）。
#    ✅ カズヤくん（10-15）「サムネOK。A/Bテストはしません。文字の外が明るい版のみを使ってください」＝反転版の1枚だけ（H 型は使わない）
THUMB = "out/thumb/ep22-ab/ep22_Hinv_ai_t.png"
THUMB_MD5 = "0673c04d7032330ca99b56230d632746"   # ⑥（10-15）`thumb_jiko.py ep22-h-ai` で焼いた


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
    """`ref/ep22/yougo.md` の「## 貼る本文」の節を**そのまま**返す（次の `---` か `## ` まで）。見出しの語が語りに出るかを当てる。"""
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
    """SPEC の値を辿って、素材の道（`ep22/…`）を全部出す（尻・頭の差し込み・over も含む）。"""
    if isinstance(v, str):
        if v.startswith("ep22/"):
            yield v
    elif isinstance(v, dict):
        for x in v.values():
            yield from _walk(x)
    elif isinstance(v, (list, tuple)):
        for x in v:
            yield from _walk(x)


# 画面の出典表記 → 種類（名乗れないものは None）。⚠️ 並びに意味がある（上から当てる）
KINDS = [
    ("mbi_other", r"^出典：米沿岸警備隊 海難調査委員会の報告書 図\d+（(FBI|米運輸安全委員会) 撮影・パブリックドメイン）$"),
    ("mbi", r"^出典：米沿岸警備隊 海難調査委員会の報告書 図\d+（パブリックドメイン）$"),
    ("lab", r"^出典：米運輸安全委員会 研究所の報告 24-011 図\d+（パブリックドメイン）$"),
    ("ntsb", r"^出典：米運輸安全委員会の報告書 図\d+（パブリックドメイン）$"),
    ("third", r"^出典：米運輸安全委員会の報告書 図\d+（写真：(Garry Comber|Steven Taragel)）$"),
    ("dvids", r"^出典：米沿岸警備隊（DVIDS \d+・パブリックドメイン）$"),
    ("noaa", r"^出典：NOAA／Institute for Exploration／ロードアイランド大学$"),
    ("ccbysa", r"^出典：Gordon Leggett（Wikimedia Commons）／CC BY-SA 4\.0／改変なし$"),
    ("sat", r"^地図：Google マップの衛星写真（帰属は地図の右下）$"),
]


def _kind(s: str):
    for k, pat in KINDS:
        if re.match(pat, s):
            return k
    return None


def used_material():
    """章ファイルの実配線から、写真・頁・映像を数える。権利は画面の出典表記で照らす。"""
    import cuts
    import cuts.ss as SS
    import footage as F
    cred = json.loads(CREDITS_JSON.read_text(encoding="utf-8"))
    for v in SS.SAT.values():                 # 衛星写真＝出典は表 SAT の credit（scene_jiko.ep22_credit と同じ）
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


def _who(s):
    """「出典：名前（…）」「出典：名前／CC…」→ 名前。"""
    body = s.split("：", 1)[1]
    return re.split(r"（|／", body, maxsplit=1)[0].strip()


def _url(stem):
    a = json.loads(ASSETS.read_text(encoding="utf-8"))
    if stem not in a or not a[stem].get("url"):
        raise SystemExit(f"🔴 {stem} の頁の URL が assets.json に無い。書かずに止めた。")
    return a[stem]["url"]


def read_credits() -> str:
    got, films, n = used_material()
    stem = lambda p: re.sub(r"\.(jpe?g|png)$", "", p.split("ep22/", 1)[1])      # noqa: E731
    out = ["【写真・映像・頁】"]
    # A＝米連邦の職務（17 U.S.C. §105）
    figs = [f"米沿岸警備隊 海難調査委員会の報告書の図 {n.get('mbi', 0) + n.get('mbi_other', 0)}点"
            + (f"（うち FBI・米運輸安全委員会が撮った写真 {n['mbi_other']}点）" if n.get("mbi_other") else ""),
            f"米運輸安全委員会の報告書の図 {n.get('ntsb', 0)}点", f"同 研究所の報告 24-011 の図 {n.get('lab', 0)}点",
            f"米沿岸警備隊の写真 {n.get('dvids', 0)}点（DVIDS）"]
    vid = OrderedDict()
    for k, c in films.items():
        if c.get("src") == "dvids":
            vid[_who(c["credit"])] = vid.get(_who(c["credit"]), 0) + 1
    out.append("・アメリカの連邦の機関の資料＝パブリックドメイン：" + "・".join(figs)
               + "、映像 " + "・".join(f"{w} {m}本" for w, m in vid.items()) + "（DVIDS）")
    dv = [c["url"] for k, c in films.items() if c.get("src") == "dvids"]
    if dv:
        out.append("　" + "　".join(dv))
    rov = [c for k, c in films.items() if c.get("src") == "ntsb"]
    if rov:
        out.append(f"・ROV の映像 {len(rov)}本（Pelagic Research Services の無人探査機・米沿岸警備隊と米運輸安全委員会が公開）"
                   f"＝引用（加工なし・額に入れて表示・一部の区間）　{rov[0]['url']}")
    if got.get("third"):
        ws = "・".join(dict.fromkeys(re.search(r"写真：([^）]+)", s).group(1) for _, s in got["third"].values()))
        out.append(f"・米運輸安全委員会の報告書に載った写真 {len(got['third'])}点（写真：{ws}）＝引用（額に入れて表示）")
    for p, (cid, s) in (got.get("noaa") or {}).items():
        out.append(f"・タイタニックの船首の写真 1点（NOAA／Institute for Exploration／ロードアイランド大学・2004年）"
                   f"＝額に入れて表示　{_url(stem(p))}")
    for p, (cid, s) in (got.get("ccbysa") or {}).items():
        out.append(f"・{_who(s)} の写真 1点（ホライゾン・アークティック）＝CC BY-SA 4.0"
                   f"（https://creativecommons.org/licenses/by-sa/4.0/）・加工なし・額に入れて表示　{_url(stem(p))}")
    if got.get("sat"):
        out.append(f"・地図の衛星写真 {len(got['sat'])}点＝Google マップ（帰属は地図の右下）")
    out.append("※ 画面に「イメージ」と出る写真は、その日・その場を写したものではありません")
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
    primary = PRIMARY.replace("TSB_URL", TSB_URL or "（URL は⑥で確かめる）")
    desc = "\n".join([HEAD, chapters(), "", read_glossary(), "", primary, "", read_credits(), "", TAIL])
    # 🔴 入れてはいけない語（BGM のクレジット・伏せ字・ゆっくりの一文・煽り語・旧版の誤り）
    for bad in ("<", ">", "BGM", "DOVA", "OpenTracks", "陰鬱な灰色", "ﾀﾋ", "ゆっくりボイス",
                "AquesTalk", "即死", "絶命", "地獄", "陰謀", "海難審判", "乗員5名"):
        if bad in desc or bad in TITLE:
            raise SystemExit(f"🔴 入れてはいけない語「{bad}」が入っている。書かずに止めた。")
    for bad in ("死亡",):
        if bad in TITLE or bad in desc:
            raise SystemExit(f"🔴 「{bad}」が入っている。書かずに止めた。")
    if not TITLE.startswith("【映像あり】"):
        raise SystemExit("🔴 【映像あり】が先頭に無い（映像方針の了承②）。書かずに止めた。")
    if not TITLE.endswith("【事故検証】【ゆっくり解説】"):
        raise SystemExit("🔴 タイトルの末尾が「【事故検証】【ゆっくり解説】」でない（B4-8）。書かずに止めた。")
    print(f"タイトル {len(TITLE)} 字（上限 100 ／ 承認は {TITLE_LEN}）")
    print(f"説明     {len(desc)} 字（上限 5,000）")
    if len(TITLE) > 100 or len(desc) > 5000:
        raise SystemExit("🔴 上限を超えた。書かずに止めた。")

    meta = {
        "slug": "ep22",
        "title": TITLE,
        "description": desc,
        "tags": ["タイタン号", "潜水艇タイタン", "タイタニック", "オーシャンゲート", "OceanGate", "爆縮", "炭素繊維",
                 "深海", "米沿岸警備隊", "NTSB", "カナダ運輸安全委員会", "事故検証", "一次資料", "ゆっくり解説",
                 "ドキュメンタリー"],
        "thumbnail": THUMB,
        "genre": "jiko",
        "playlist": "",
    }
    if "--dry" in sys.argv:
        print("\n" + TITLE + "\n\n" + desc)
        return 0
    if N_COUNTS is None or THUMB_MD5 is None or TITLE_LEN is None or TSB_URL is None:
        raise SystemExit("🔴 点数・サムネの md5・題の字数・TSB の URL のどれかがまだ決まっていない。書かずに止めた。")
    if len(TITLE) != TITLE_LEN:
        raise SystemExit(f"🔴 決めた題（{TITLE_LEN}字）と字数が違う＝写し間違い。書かずに止めた。")
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
