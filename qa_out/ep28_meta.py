# -*- coding: utf-8 -*-
"""28本目（タイムズカー情報漏えい）の `config/meta_ep28.json` を**機械で**組み立てる（2026-11-02・⑥）。

`qa_out/ep27_meta.py`（用語・目次・素材の点数・字数の網）を写し、素材の種類を28本目の出典の形に直した。

🔴 手で書かない理由（ep7〜ep27 と同じ）
  ① 用語は `ref/ep28/yougo.md` の「## 貼る本文」の節が正本＝**そのまま**貼る。見出しの語が語りに出るかと、並びが語りに初めて出る順かを当てる
  ② 素材の点数は**章ファイルの実配線**（`cuts.SPEC` の写真／`footage.USE` の映像）から数え、権利は**画面の出典表記**
     （`ref/ep28/credits.json`・`clips.json`）で照らす。名乗れない素材が出たら落ちる
  ③ 目次は `scene_jiko.CUTS` の秒を頭から積む＝**焼いた版と同じ秒**
  ④ タイトル 100字・説明 5,000字の上限と、入れてはいけない語を、書く前に確かめる

🔴 会社のシステムが攻撃された事件の回（ルール §B2-11・記憶 feedback-jiko-incident-case-rules＝10-31 承認の8点）
  - 会員・SNS の投稿者の名前は書かない／役員・弁護士は役職だけ（事務所の名前と頁の URL も書かない）
  - 攻撃した者は「第三者」「攻撃した者」／会社と役員を「犯人」「加害者」と言い切らない
  - **窓口を出す**＝第5報の言葉のまま（c701 の語りが「画面と説明欄に書いておく」と言っている）
  - 題の札＝【事件検証】【ゆっくり解説】・まだ終わっていない事件なので「真相」を使わない／題だけ「漏洩」（検索の語・語りと画面は「漏えい」）
  - 写真の作者（Commons の撮影者）の名前は**公開リポに書かない**＝git の外の表から `scene_jiko._ep28_author` で足す
    （`config/` は gitignore＝説明の JSON は公開リポに入らない）
  - ⚠️ 11-02 に当て直した＝海外の掲示板の「420万件を売る」投稿（専門のブログが偽物の可能性が高いと分析）は書かない（真偽の分からない話を広げない）

    python -P qa_out/ep28_meta.py            # 組み立てて config/meta_ep28.json に書く
    python -P qa_out/ep28_meta.py --dry      # 書かずに中身と字数だけ出す
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

YOUGO = HERE / "ref" / "ep28" / "yougo.md"
CREDITS_JSON = HERE / "ref" / "ep28" / "credits.json"
ASSETS_JSON = HERE / "ref" / "ep28" / "assets.json"
CLIPS = HERE / "ref" / "ep28" / "clips.json"
OUT = HERE / "config" / "meta_ep28.json"

N_GLOSS = 6           # `ref/ep28/yougo.md` の「貼る本文」の語数
# ⚠️ 下の値は⑥（11-02）の配線から数えた点数（変わったら止まる＝文の点数を当て直す）。None＝数えて出すだけ
N_COUNTS = {"own": 26, "company": 8, "pd": 5, "cc0": 7, "gov": 7, "film": 14, "mos_face": 1, "mos_plate": 12}

# ✅ ⑥（11-03）カズヤくん「A.（2026年11月時点）に変更」＝台本 §1-1 の A の時点だけ替えた（語りの「10月31日の時点」は公開の直前に当て直す）
TITLE = ("タイムズカー情報漏洩事件 まとめ完全版（2026年11月時点）退会した人の免許証の画像まで、7年間残されていた。"
         "【事件検証】【ゆっくり解説】")
TITLE_LEN = 70        # 決めた題の字数（写し間違いの網）

# ⚠️ 本文（台本第2版 c101〜c107）で言っていることだけを書く
HEAD = """【この動画について】
2026年9月25日、午前9時7分。カーシェアのタイムズカーを運営する会社が、システムへの、外からの不正なアクセスに気づきました。3日後、会社は、約660万件の個人の情報が漏えいしたと発表します。漏えいの対象には、退会した人まで含まれていました。そして会社は、運転免許証の画像を、退会してから7年間、持ち続けていました。

外へ送られた跡がある画像は、146万件あまり。見舞金は、3000円分。訴えに加わりたい人は、弁護士側によると、10万人を超えました。攻撃したのがだれなのかは、10月31日の時点で、まだ明らかになっていません。

この動画は、会社の発表と、国や報道の記録をもとに、最初の朝から順にたどります。
"""

# 🔴 c701 の語りが「画面と説明欄に書いておく」＝第5報（2026-10-23）の言葉のまま・11-02 に頁で当て直した
WINDOW = """【問い合わせ先】（タイムズモビリティ 第5報より）
電話番号：0120-25-8924（24時間）※おかけ間違いにご注意ください。
問い合わせフォーム：https://share.timescar.jp/inquiry.html#contact
会員の方：10月23日17時から、タイムズカーのWebサイトのマイページで、ご自身のどの情報の漏えいが確認されたかを見られます。
退会された方：退会者様専用のお問い合わせフォーム　https://inquiry.timescar.jp/view/inquiry/mailAuth.html
※ 会社は、SMSの認証コード、パスワード、暗証番号などを聞くことはない、としています。会社や公的な機関を名乗る連絡には、ご注意ください。
"""

# 台本第2版の出典の欄と `ref/ep28/sources.md` から。⑥（11-02）URL は curl で開けるかを確かめた（10本＝200）
PRIMARY = """【出典】
・タイムズモビリティ「タイムズカーWebシステムへの不正アクセス」第1報〜第5報（2026年9月25日〜10月23日）　https://share.timescar.jp/news/2026/1023/1825.html
・タイムズモビリティ「本事案に関するご質問と回答」（2026年10月23日更新）　https://corp.timescar.jp/mail/announce/faq.pdf?20261023
・パーク24 適時開示（2026年9月28日・10月23日）・ニュースリリース　https://www.park24.co.jp/news/
・個人情報保護委員会「大規模な漏えい等事案を踏まえた対応について（注意喚起）」（2026年10月7日）　https://www.ppc.go.jp/news/press/2026/261007_houdou
・金融庁「サイバーセキュリティ対策の強化と各種取引申込等における対応」（2026年10月9日）　https://www.fsa.go.jp/news/r8/sonota/20261009/20261009.html
・国家サイバー統括室「不正アクセスによる漏えい等の事案を踏まえた対応について」（2026年10月9日）　https://www.cyber.go.jp/pdf/press/taiou.pdf
・首相官邸「サイバーセキュリティに関する関係閣僚会議」（2026年10月26日）　https://www.kantei.go.jp/jp/105/actions/202610/26kaigi_cyber.html
・警察庁「サイバー警察局便り」2026 Vol.19　https://www.npa.go.jp/bureau/cyber/pdf/R8_Vol.19cpal.pdf
・三重県警察・福岡県警察の免許証の再交付の案内・e-Gov パブリック・コメント結果（警察庁・2025年6月）
・報道：弁護士ドットコム・毎日新聞・時事通信・テレビ朝日・TBS・ITmedia・共同通信・NHK・読売新聞・日本テレビほか（2026年9月〜10月）
"""

# ⚠️ 語りは「10月31日の時点」のまま＝11-03（公開の直前）に会社の頁と報道へ当て直した＝第6報なし・提訴なし・逮捕なし・c701 の番号は第5報と一致
TAIL = """動画に出てくる数字と日付は、会社の発表と、国や報道の記録によります（2026年10月31日時点。公開前の11月3日に、会社の新着情報と報道を見直し、語りを変える新しい発表がないことを確かめました）。
※ 攻撃した者は、10月31日の時点で明らかになっていません。動画では「第三者」「攻撃した者」とお伝えしています。
※ 会員と SNS の投稿者のお名前は出していません。会社の役員と弁護士は役職でお伝えしています。
※ SNS の投稿は、確かめられた情報ではありません（画面に注記しています）。
※ 画面の模式図は、会社の発表と報道をもとに描いた図です。"""

# ✅ ⑥（11-03）カズヤくん「d2で黄色字を左詰め」＝d3（`qa_out/ep28_thumb.py`）。CM044＝本編 c410 と同じ写真・CC BY 3.0。作者は焼く道と同じ git の外の表から足す（main）
THUMB = "out/thumb/ep28/ep28_T_d3.png"
THUMB_MD5 = "3efe181e65f986b10a62ef423f6fd5b5"
THUMB_NOTE = ("※ サムネイルの写真は、Wikimedia Commons の {作者} の写真（CC BY 3.0）です。"
              "切り出し、左の一部を裏返してつなぎ、明るさと彩度を変えて、文字を重ねています。")

TAGS = ["タイムズカー", "タイムズカー情報漏洩", "情報漏えい", "個人情報漏洩", "不正アクセス", "パーク24", "タイムズモビリティ",
        "カーシェア", "運転免許証", "見舞金", "集団訴訟", "事件検証", "ゆっくり解説", "解説", "ニュース"]

LIC_URL = {"CC BY 2.0": "https://creativecommons.org/licenses/by/2.0/deed.ja",
           "CC BY 3.0": "https://creativecommons.org/licenses/by/3.0/deed.ja",
           "CC BY 4.0": "https://creativecommons.org/licenses/by/4.0/deed.ja",
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
    """`ref/ep28/yougo.md` の「## 貼る本文」の節を**そのまま**返す（次の `---` か `## ` まで）。見出しの語が語りに出るかを当てる。"""
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
    """SPEC の値を辿って、素材の道（`ep28/…`）を全部出す（地に敷く写真も含む）。"""
    if isinstance(v, str):
        if v.startswith("ep28/"):
            yield v
    elif isinstance(v, dict):
        for x in v.values():
            yield from _walk(x)
    elif isinstance(v, (list, tuple)):
        for x in v:
            yield from _walk(x)


_MOS = r"(?:顔|ナンバー|顔とナンバー)にモザイク"
# 画面の出典表記（credits.json の値＝作者は印 {作者} のまま）→ 種類（名乗れないものは None）。⚠️ 並びに意味がある（上から当てる）
KINDS = [
    ("own", r"^写真：\{作者\}／Wikimedia Commons（CC BY(?:-SA)? [234]\.0）／改変(?:なし|：切出(?:・" + _MOS + r")?|：" + _MOS + r")$"),
    ("cc0", r"^Wikimedia Commons（CC0）(?:／改変：(?:切出・)?" + _MOS + r"|／改変：切出)?$"),
    ("pd", r"^Wikimedia Commons（パブリックドメイン）(?:／改変：(?:切出・)?" + _MOS + r"|／改変：切出)?$"),
    ("company", r"^出典：(?:タイムズモビリティ 第[1-5]報|パーク24 適時開示)"),
    ("gov", r"^出典：(?:個人情報保護委員会|金融庁|国家サイバー統括室|首相官邸|e-Gov|福岡県警察|三重県警察)"),
]
STOCK = "イメージ（Pexels）"


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
                if f"{w}にモザイク" in s or "顔とナンバーにモザイク" in s:
                    mos[w].add(p)
    films = OrderedDict()
    for cid, u in F.USE.items():
        c = clips.get(u["clip"])
        if c is None:
            bad.append(f"{cid}:{u['clip']}（clips.json に無い）")
            continue
        if c.get("credit", "") != STOCK:
            bad.append(f"{cid}:{u['clip']}（名乗れない映像の出典：{c.get('credit')}）")
            continue
        films[cid] = c
    if bad:
        raise SystemExit(f"🔴 名乗れない素材がある。書かずに止めた: {bad}")
    counts = {k: len(v) for k, v in got.items()}
    counts.update(film=len(films), mos_face=len(mos["顔"]), mos_plate=len(mos["ナンバー"]))
    print(f"■ 素材（配線から）：{counts}")
    if N_COUNTS is not None and counts != N_COUNTS:
        raise SystemExit(f"🔴 点数が⑥で数えた値 {N_COUNTS} と違う。文の点数を当て直すこと。書かずに止めた。")
    return got, counts


def read_credits() -> str:
    got, n = used_material()
    assets = json.loads(ASSETS_JSON.read_text(encoding="utf-8"))
    out = ["【写真・映像】"]
    # 個人名義（Commons）＝作者・ライセンスごとにまとめる（名前は git の外の表から＝焼く道と同じ）
    by = OrderedDict()
    for p, (cid, s) in (got.get("own") or {}).items():
        lic = re.search(r"（(CC BY(?:-SA)? [234]\.0)）", s).group(1)
        a = assets.get(Path(p).stem) or {}
        if a.get("lic") != lic:
            raise SystemExit(f"🔴 {Path(p).stem} のライセンスが台帳（{a.get('lic')}）と画面（{lic}）で違う。書かずに止めた。")
        by.setdefault((S._ep28_author(p), lic), []).append(p)
    out.append(f"・Wikimedia Commons の写真 {n.get('own', 0)}点（作者・ライセンス・点数＝CC BY-SA は加工なし・"
               "CC BY は切り出し・写真ごとの作者とライセンスは画面の出典の行にも）")
    for (who, lic), ps in by.items():
        out.append(f"　{who}（{lic}）" + (f"{len(ps)}点" if len(ps) > 1 else ""))
    for p, (cid, s) in (got.get("cc0") or {}).items():
        a = assets.get(Path(p).stem) or {}
        if a.get("lic") != "CC0":
            raise SystemExit(f"🔴 {Path(p).stem} のライセンスが台帳（{a.get('lic')}）と画面（CC0）で違う。書かずに止めた。")
    out.append(f"・Wikimedia Commons の写真 {n.get('cc0', 0)}点（CC0）・{n.get('pd', 0)}点（パブリックドメイン）")
    used_lic = sorted({lic for (_, lic) in by} | ({"CC0"} if n.get("cc0") else set()))
    out.append("　ライセンス：" + "　".join(f"{lic} {LIC_URL[lic]}" for lic in used_lic))
    out.append(f"　顔が写る {n.get('mos_face', 0)}点は顔に、車のナンバーが写る {n.get('mos_plate', 0)}点はナンバーに、モザイクをかけています")
    out.append(f"・タイムズモビリティ・パーク24 の頁と資料の画面 {n.get('company', 0)}点＝引用（加工なし・出典は画面に表示）")
    out.append(f"・国と警察の頁と資料の画面 {n.get('gov', 0)}点（出典は画面に表示）")
    out.append(f"※ 画面に「イメージ」と出る映像（{n.get('film', 0)}本）は、フリー素材です。その日・その場を写したものではありません")
    out.append("※ 会社と国の資料を使っていますが、これらがこの動画を作ったり、推奨・支持したりしているものではありません")
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
    tail = TAIL + ("\n" + THUMB_NOTE.replace(S._EP28_AUTHOR, S._ep28_author("ep28/cm044.jpg")) if THUMB_NOTE else "")
    desc = "\n".join([HEAD, WINDOW, chapters(), "", read_glossary(), "", PRIMARY, read_credits(), "", tail])
    # 🔴 入れてはいけない語（BGM のクレジット・ゆっくりの一文・煽り語・タグの残り）
    for bad in ("<", ">", "BGM", "DOVA", "OpenTracks", "ゆっくりボイス", "AquesTalk", "即死", "絶命", "地獄",
                "【映像あり】", "{作者}", S.EP23_AUTHOR_STANDIN):
        if bad in desc or bad in TITLE:
            raise SystemExit(f"🔴 入れてはいけない語「{bad}」が入っている。書かずに止めた。")
    # 🔴 会社の事件の回（ルール §B2-11）＝犯人・加害者と書かない・まだ終わっていない事件で「真相」を使わない・「死亡」を使わない
    #    ・語りにない売買の話を書かない・弁護士側の頁の URL を書かない
    for bad in ("犯人", "加害者", "真相", "死亡", "420万", "timescar-lawsuit", "流出"):
        if bad in TITLE or bad in desc:
            raise SystemExit(f"🔴 「{bad}」が入っている。書かずに止めた。")
    for need in ("0120-25-8924", "https://share.timescar.jp/inquiry.html", "マイページ", "退会者様専用"):
        if need not in desc:
            raise SystemExit(f"🔴 窓口の「{need}」が無い（c701 の語りと事件の回の決まり）。書かずに止めた。")
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
    meta = {"slug": "ep28", "title": TITLE, "description": desc, "tags": TAGS, "thumbnail": THUMB,
            "genre": "jiko", "playlist": ""}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✓ 書いた → {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
