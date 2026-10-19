# -*- coding: utf-8 -*-
"""23本目（三豊百貨店崩壊事故のリメイク）の `config/meta_ep23.json` を**機械で**組み立てる（2026-10-19・⑥）。

`qa_out/ep22_meta.py` を写して、この回の形に合わせた。

🔴 手で書かない理由（ep7〜ep22 と同じ）
  ① 用語は `ref/ep23/yougo.md` の「## 貼る本文」の節が正本＝**そのまま**貼る（`**` だけ外す）。
     見出しの語が語り（`narration.SCRIPT`）に出るかと、並びが語りに初めて出る順かを1語ずつ当てる（⑤a-1 の宿題の3語＝yougo.md の頭）
  ② 素材の点数は**章ファイルの実配線**（`cuts.SPEC` の写真／`footage.USE` の映像／`cuts.ss.SAT` の衛星写真）から数え、
     権利は**画面の出典表記**（`ref/ep23/credits.json`・`clips.json`・`ss.SAT`）で照らす。名乗れない素材が出たら落ちる
  ③ 目次は `scene_jiko.CUTS` の秒を頭から積む＝**焼いた版と同じ秒**（章の扉の秒は CUTS に入っている）
  ④ タイトル 100字・説明 5,000字の上限と、入れてはいけない語を、書く前に確かめる

🔴 この回が 22本目と違うところ
  - 権利：Wikimedia Commons の CC BY-SA 4.0（ソウル特別市 消防災難本部・個人名義）＝額装・改変なし／
    ソウル研究院（公共ヌリ第1類型＋CC BY 4.0）＝切り出し・1点は顔にモザイク／ソウル歴史編纂院（公共ヌリ第1類型）＝3点は顔（1点は名前も）にモザイク／
    地図の衛星写真＝Google（帰属は地図の右下）／イメージの写真と映像（Pexels・Pixabay）＝クレジットの要らないフリー素材＝点数を書かない（記憶 feedback-no-optional-credits）
  - 個人名義の作者の名前は**公開リポに書かない**（10-17「名前0」・了承② 決め4）＝焼くときと同じく git の外の表
    `ref/ep23/src/credits_private.tsv` から `scene_jiko.ep23_credit` で足す（`config/` は gitignore＝説明の JSON は公開リポに入らない）
  - 【映像あり】は付けない（事故の映像なし・映像方針の了承②）。題は⑥でカズヤくんの案に決めた（下の TITLE の注）
  - 関わった人の名前は出さない（台本 §1-4）＝🔴 commit の前に `python ref/ep23/v2_build/namecheck23.py qa_out/ep23_meta.py ref/ep23/yougo.md`
  - 末尾に ※ でリメイクと記す（旧版＝10本目・2026年9月公開・10-17 に非公開を確認）・サムネは生成 AI の再現のイメージと断る

    python qa_out/ep23_meta.py            # 組み立てて config/meta_ep23.json に書く
    python qa_out/ep23_meta.py --dry      # 書かずに中身と字数だけ出す
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

YOUGO = HERE / "ref" / "ep23" / "yougo.md"
CREDITS_JSON = HERE / "ref" / "ep23" / "credits.json"
CLIPS = HERE / "ref" / "ep23" / "clips.json"
OUT = HERE / "config" / "meta_ep23.json"

N_GLOSS = 16          # `ref/ep23/yougo.md` の「貼る本文」の語数（台本 §8 の16語）
# ⚠️ 下の値は⑥（10-19）本編 r01（版 2319b1d）の配線から数えた点数（変わったら止まる＝文の点数を当て直す）
N_COUNTS = {"fire": 58, "own": 10, "sire": 16, "hs": 9, "stock": 8, "sat": 2, "film": 17}

# 🔴 承認①（10-18）は題 A。⑥（10-19）の試写のあとカズヤくんが自分の案「崩壊した日の15時10分、技術者は「すぐに崩れる危険はない」と
#    診断していた。三豊百貨店崩壊事故の真相」＋【事故検証】【ゆっくり解説】に決めた。Claude の所見＝原文（K6-検 p.47「도착(15:10)」・
#    16:00 の会議「당장 붕괴위험은 없으니」・p.52「15:10경 안전진단…16:40경 대책회의에서 급박한 붕괴위험은 없다고 보고」）では 15時10分は
#    着いて診断を始めた時刻で、その言葉は 16時と16時40分の会議＝案のままだと「15時10分にそう診断した」と読める → 「現場に着いた」を足す案を
#    出し、カズヤくんが選んだ（本編 c105「午後3時10分に着いた構造技術者は、会議で…」・c306 と同じ事実）
TITLE = ("崩壊した日の15時10分、現場に着いた技術者は「すぐに崩れる危険はない」と診断していた。"
         "三豊百貨店崩壊事故の真相【事故検証】【ゆっくり解説】")
TITLE_LEN = 70        # 決めた題の字数（写し間違いの網）

# ⚠️ 本文（台本第2版 c101〜c109・c306・cb05・cb08）で言っていることだけを書く
HEAD = """【この動画について】
1995年6月29日、木曜日の夕方。韓国の首都ソウルにあった三豊百貨店の北の棟が、5階から地下まで、一気に崩れ落ちました。店を開いてから、まだ5年半の建物でした。502人が亡くなり、937人がけがをしました。地震でも火事でもなく、建物そのものが崩れた事故です。

その日の朝、5階の食堂の床は、もう盛り上がっていました。昼には、柱のまわりの床が15センチ沈んでいます。午後3時10分に現場に着いた構造技術者は、会議で「すぐに崩れる危険はない」と言い、店は開いたままでした。

この動画は、国会の調査の記録（検察・ソウル市・瑞草区の報告を含む）、ソウル市の白書、裁判所の判決をもとに、次の3つの問いをたどります。

・なぜ、店は開いたままだったのか
・なぜ、建物は崩れたのか
・そして、誰なら止められたのか

亡くなった人の数は、資料によって501人と502人に分かれます（動画の中で、そのわけを説明しています）。時刻は現地の時刻で、日本と同じです。ウォンの円の目安は、当時の為替の年平均で直しています。
"""

# 台本第2版 §10（資料）・旧版の概要欄から。⑥（10-19）URL は curl で 200 を確かめた（国家記録院は &sitePage= 付きで 200・無しは 400）
PRIMARY = """【出典】
・大韓民国国会「삼풍백화점붕괴사건조사특별위원회」会議録 第6号（1995年9月12日）＝国政調査の結果報告書と、添付のソウル特別市・瑞草区・ソウル地方検察庁の報告　https://record.assembly.go.kr/assembly/viewer/minutes/download/pdf.do?id=19114
・1995年度 国政監査の会議録（内務委員会 1995年10月10日・建設交通委員会 1995年10月11日／被監査機関＝ソウル特別市）　https://record.assembly.go.kr/assembly/viewer/minutes/download/pdf.do?id=19476　https://record.assembly.go.kr/assembly/viewer/minutes/download/pdf.do?id=19502
・大法院 1996年8月23日 宣告 96도1231 判決（刑事）　https://www.law.go.kr/precInfoP.do?precSeq=114109
・大法院 1999年12月21日 宣告 98다29797 判決（民事）　https://www.law.go.kr/precInfoP.do?precSeq=79152
・ソウル高等法院 1996年5月10日 宣告 96노118 判決（主文）
・ソウル特別市『삼풍백화점 붕괴사고 백서』（三豊百貨店崩壊事故 白書）1996年6月　https://dl.nanet.go.kr/detail/MONO1199606952
・国家記録院「삼풍백화점 붕괴사고」の主題説明　https://www.archives.go.kr/next/newsearch/listSubjectDescription.do?id=001922&sitePage=
・国家法令情報センター（災難管理法ほか）　https://www.law.go.kr/
・ソウル特別市「삼풍백화점 참사 노을공원 추모조형작품 공모」の公告（2026年6月）　https://news.seoul.go.kr/safe/archives/517985"""

TAIL = """動画に出てくる数値・時刻・言葉は、これらの記録によります。
資料によって割れるところ（崩れた時刻、亡くなった人の数など）は、画面と語りでそのまま断っています。
※ 画面の断面図・平面図・模式図・時間の帯・地図の書き込みは、記録をもとに描いた図です。
※ 関わった方のお名前は出していません。役職でお伝えしています（会社の名は、建物を持ち、自分で仕上げた三豊建設産業だけ）。
※ 跡地のいま、慰霊塔のある公園の名、2026年の追悼の造形は、報道とソウル市の公告によります。
※ この動画は、2026年9月に公開した三豊百貨店の動画を、作り直したものです。
※ サムネイルの絵は、生成AIで作った再現のイメージです（実際の写真ではありません）。"""

# ✅ ⑥（10-19）カズヤくん：地＝旧版（10本目）の生成 AI の地 c（`ref/ep10/ai/ep10_c.jpg`）・「背景をもう少し明るく」→ 案2（明るさ+26%）
#    H 型の反転版1枚・A/B なし（10-15 の決め）＝`thumb_jiko.py ep23-h-bright` の `_b2`
THUMB = "out/thumb/ep23-ab/ep23_Hinv_ai10c_b2.png"
THUMB_MD5 = "9dece9ed6f24173acda2d1f53666854f"

TAGS = ["三豊百貨店", "三豊百貨店崩壊事故", "サンプン百貨店", "삼풍백화점", "ソウル", "韓国", "1995年", "建物崩壊",
        "フラットスラブ", "冷却塔", "事故検証", "一次資料", "ゆっくり解説", "ドキュメンタリー", "解説"]


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
    """`ref/ep23/yougo.md` の「## 貼る本文」の節を**そのまま**返す（次の `---` か `## ` まで）。見出しの語が語りに出るかを当てる。"""
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
    """SPEC の値を辿って、素材の道（`ep23/…`）を全部出す（尻・頭の差し込み・over も含む）。"""
    if isinstance(v, str):
        if v.startswith("ep23/"):
            yield v
    elif isinstance(v, dict):
        for x in v.values():
            yield from _walk(x)
    elif isinstance(v, (list, tuple)):
        for x in v:
            yield from _walk(x)


# 画面の出典表記（credits.json の値＝作者は印 {作者} のまま）→ 種類（名乗れないものは None）。⚠️ 並びに意味がある（上から当てる）
KINDS = [
    ("fire", r"^写真：ソウル特別市 消防災難本部（CC BY-SA 4\.0）・改変なし$"),
    ("own", r"^写真：\{作者\}（CC BY-SA 4\.0）・改変なし$"),
    ("sire", r"^写真：ソウル特別市／ソウル研究院（서울연구데이터서비스）（公共ヌリ第1類型・CC BY 4\.0）・改変：切出(・顔にモザイク)?$"),
    ("hs", r"^写真：ソウル歴史編纂院（公共ヌリ第1類型）(・改変：顔(と名前)?にモザイク)?$"),
    ("stock", r"^イメージ（Pexels）$"),
    ("sat", r"^地図：Google マップの衛星写真（帰属は地図の右下）$"),
]


def _kind(s: str):
    for k, pat in KINDS:
        if re.match(pat, s):
            return k
    return None


def used_material():
    """章ファイルの実配線から、写真・映像・衛星写真を数える。権利は画面の出典表記で照らす。"""
    import cuts
    import cuts.ss as SS
    import footage as F
    cred = json.loads(CREDITS_JSON.read_text(encoding="utf-8"))
    for v in SS.SAT.values():                 # 衛星写真＝出典は表 SAT の credit（scene_jiko.ep23_credit と同じ・22本目の型）
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
        if c.get("credit") not in ("イメージ（Pexels）", "イメージ（Pixabay）"):
            bad.append(f"{cid}:{k}（映像の出典がフリー素材の「イメージ」でない：{c.get('credit')}）")
        films.setdefault(k, c)
    if bad:
        raise SystemExit(f"🔴 名乗れない素材がある。書かずに止めた: {bad}")
    counts = {k: len(v) for k, v in got.items()}
    counts.update(film=len(films))
    print(f"■ 素材（配線から）：{counts}")
    if counts != N_COUNTS:
        raise SystemExit(f"🔴 点数が⑥で数えた値 {N_COUNTS} と違う。文の点数を当て直すこと。書かずに止めた。")
    return got, counts


def _author(got) -> str:
    """個人名義の写真の作者欄の名前（git の外の表から＝焼くときと同じ道）。1人でなければ止める（文の形が1人ぶん）。"""
    names = set()
    for p, (cid, s) in got.get("own", {}).items():
        line = S.ep23_credit(p)
        m = re.fullmatch(r"写真：(.+?)（CC BY-SA 4\.0）・改変なし", line or "")
        if not m or m.group(1) in ("{作者}", S.EP23_AUTHOR_STANDIN):
            raise SystemExit(f"🔴 {p} の作者の名前が取れない（{line!r}）。書かずに止めた。")
        names.add(m.group(1))
    if len(names) != 1:
        raise SystemExit(f"🔴 個人名義の作者が {len(names)} 人＝文の形（1人ぶん）と合わない。書かずに止めた。")
    return names.pop()


def read_credits() -> str:
    got, n = used_material()
    who = _author(got)
    mos_sire = sum("モザイク" in s for _, s in got["sire"].values())
    mos_hs = sum("モザイク" in s for _, s in got["hs"].values())
    mos_name = sum("名前" in s for _, s in got["hs"].values())
    out = ["【写真・地図】",
           f"・写真 {n['fire']}点：ソウル特別市 消防災難本部（서울특별시 소방재난본부）／写真 {n['own']}点：{who}",
           "　CC BY-SA 4.0　https://creativecommons.org/licenses/by-sa/4.0/deed.ja",
           "　素材：Wikimedia Commons　https://commons.wikimedia.org/wiki/Category:Sampoong_Department_Store_collapse",
           "　切らず・色を変えず・何も重ねず、そのままの形で額に入れて出しています（改変なし）",
           f"・写真 {n['sire']}点：ソウル特別市／ソウル研究院（서울연구데이터서비스）",
           "　公共ヌリ 第1類型＋CC BY 4.0　https://creativecommons.org/licenses/by/4.0/deed.ja　素材：https://data.si.re.kr/",
           "　画面に合わせて切り出しています" + (f"（{mos_sire}点は人の顔にモザイク）" if mos_sire else ""),
           f"・写真 {n['hs']}点：ソウル歴史編纂院（서울역사편찬원）",
           "　公共ヌリ 第1類型　https://www.kogl.or.kr/info/license.do　素材：https://history.seoul.go.kr/archive/main.do"]
    if mos_hs:
        out.append(f"　{mos_hs}点は人の顔" + (f"（{mos_name}点は名前も）" if mos_name else "") + "にモザイクをかけています")
    out.append(f"・地図の衛星写真 {n['sat']}点＝Google マップ（帰属は地図の右下）")
    out.append("※ 画面に「イメージ」と出る写真・映像は、フリー素材です。その日・その場を写したものではありません")
    out.append("※ ソウル市・ソウル研究院・ソウル歴史編纂院・消防災難本部の資料を使っていますが、これらの機関がこの動画を作ったり、推奨・支持したりしているものではありません")
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
    # 🔴 入れてはいけない語（BGM のクレジット・伏せ字・ゆっくりの一文・煽り語・旧版の誤り）
    for bad in ("<", ">", "BGM", "DOVA", "OpenTracks", "ﾀﾋ", "ゆっくりボイス", "AquesTalk", "即死", "絶命", "地獄",
                "みとよ", "【映像あり】"):
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

    meta = {
        "slug": "ep23",
        "title": TITLE,
        "description": desc,
        "tags": TAGS,
        "thumbnail": THUMB,
        "genre": "jiko",
        "playlist": "",
    }
    if "--dry" in sys.argv:
        print("\n" + TITLE + "\n\n" + desc)
        return 0
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
