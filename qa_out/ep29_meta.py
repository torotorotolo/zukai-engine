# -*- coding: utf-8 -*-
"""29本目（GMOへの不正アクセス）の `config/meta_ep29.json` を**機械で**組み立てる（2026-11-04・⑥）。

`qa_out/ep28_meta.py`（用語・目次・素材の点数・字数の網）を写し、素材の種類を29本目の出典の形に直した。

🔴 手で書かない理由（ep7〜ep28 と同じ）
  ① 用語は `ref/ep29/yougo.md` の「## 貼る本文」の節が正本＝**そのまま**貼る。見出しの語が語りに出るかと、並びが語りに初めて出る順かを当てる
  ② 素材の点数は**章ファイルの実配線**（`cuts.SPEC` の写真／`footage.USE` の映像）から数え、権利は**画面の出典表記**
     （`ref/ep29/credits.json`・`clips.json`）で照らす。名乗れない素材が出たら落ちる
  ③ 目次は `scene_jiko.CUTS` の秒を頭から積む＝**焼いた版と同じ秒**
  ④ タイトル 100字・説明 5,000字の上限と、入れてはいけない語を、書く前に確かめる

🔴 情報の公開と脅迫の加わった会社の事件の回（ルール §B2-11・§B2-11b）
  - 公開された人・SNS の投稿者の名前は書かない／役員は役職だけ／「顧客」と言い切らない
  - 攻撃した者は「第三者」「攻撃した者」／会社と役員を「犯人」「加害者」と言い切らない／特定の国や集団を書かない
  - 攻撃した者のサイトの名前と置き場を書かない＝「見に行かない・広めない」を書く
  - **窓口を出す**＝第16報の字のまま（c701・c703 の語りが「画面と説明欄に書く」と言っている）
  - 🔴 `group.gmo` へのリンクは事前に連絡が要る＝置かない（ルール §2-36）。`internet.gmo` は引用でもサイト名と URL を明記
  - 写真の作者の名前は**公開リポに書かない**＝git の外の表から `scene_jiko._ep29_author` で足す（`config/` は gitignore）

    python -P qa_out/ep29_meta.py            # 組み立てて config/meta_ep29.json に書く
    python -P qa_out/ep29_meta.py --dry      # 書かずに中身と字数だけ出す
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

YOUGO = HERE / "ref" / "ep29" / "yougo.md"
CREDITS_JSON = HERE / "ref" / "ep29" / "credits.json"
ASSETS_JSON = HERE / "ref" / "ep29" / "assets.json"
CLIPS = HERE / "ref" / "ep29" / "clips.json"
OUT = HERE / "config" / "meta_ep29.json"

N_GLOSS = 11          # `ref/ep29/yougo.md` の「貼る本文」の語数
# ⚠️ ⑥（11-04）の配線から数えた点数（変わったら止まる＝文の点数を当て直す）。None＝数えて出すだけ
N_COUNTS = {"company": 9, "own": 16, "cc0": 15, "gov": 5, "pd": 1, "film": 17, "mos_face": 2, "mos_plate": 3}

# ✅ ⑥（11-04）カズヤくんが案を選んで削った＝承認①の題（侵入から76日、会社は気づけなかった。きっかけは利用者の問い合わせ。）から替えた。
#    問いを事件名のすぐ後ろへ（サムネ J2 の「侵入から76日 気づけず」と重ねない）。根拠＝c409・c705
TITLE = ("GMOへの不正アクセス事件、なぜ76日も気づけなかったのか。まとめ完全版（2026年11月時点）"
         "【事件検証】【ゆっくり解説】")
TITLE_LEN = 62        # 決めた題の字数（写し間違いの網）

# ⚠️ 本文（台本第2版 c101〜c107）で言っていることだけを書く
HEAD = """【この動画について】
2026年10月27日の朝、ネットの会社が、利用者にこんなお願いを出しました。12時になる前に、電源を落とし、パソコンのコードを抜いてください。攻撃した者が、情報の公開と、データを人質に取る攻撃を、予告していました。

会社の説明では、最初の侵入は8月5日。異変を確かめたのは10月20日です。そのあいだ76日、およそ2カ月半。調べ始めたきっかけは、利用者からの問い合わせでした。2年前には、同じグループのセキュリティの専門家が、このサービスの改善点を指摘していました（侵入との関係は分かっていません）。

この動画は、会社の発表と、11月2日の説明会、国の記録、報道をもとに、順にたどります。
"""

# 🔴 c701・c703・c704 の語りが「画面と説明欄に書く」＝第16報（11-04 に頁で当て直した）の字のまま
WINDOW = """【相談の窓口】（第16報より）
電話：03-5456-2560（土日・祝日を含め24時間受付）※おかけ間違いにご注意ください。
問い合わせフォーム：https://help.onamae.com/contact/

【攻撃した者についての情報の窓口】（第16報より）
専用サイト：cybercrimebounty.gmo
メール：info@cybercrimebounty.gmo
※ 会社は、自分で特定や接触をしないこと、確証のない情報を投稿しないことを求めています。

【見に行かない・広めない】
公開された情報を見に行かないでください。URL や中身を広めないでください。見た人の情報は取られている、と会社は警告しています。

【成り済ましに注意】
会社は、パスワードや認証コードを尋ねることはない、「被害金を取り戻す」などとして費用を求める連絡には応じないように、と呼びかけています。
※ 補償の手続きについては、取引の履歴を確かめるための閲覧専用のパスワードの提示を、会社が別に案内しています（第4報）。手続きは会社の公式の案内で確かめてください。

【国の案内】
国家サイバー統括室「サイバー対応特設サイト」　https://www.cyber.go.jp/tokusetsu/contactpoint_advisory_hub/index.html
首相官邸「個人情報流出の被害に遭われた方・ご心配のある方の相談窓口」　https://www.kantei.go.jp/jp/headline/johoryushutsu_sodan/index.html
"""

# 台本第2版の出典の欄と `ref/ep29/sources.md` から。🔴 group.gmo の頁は同じ第N報が載る internet.gmo の一覧を示す
PRIMARY = """【出典】
・GMOインターネット「お名前.com デスクトップクラウド」への不正アクセスに関するお知らせ 第1報〜第16報（2026年10月21日〜29日）・お客様へのご案内（10月30日）　https://internet.gmo/news/
・GMOインターネット 適時開示（2026年10月23日・24日・28日・11月2日）　https://internet.gmo/ir/
・会社の説明会（2026年11月2日）の配信と、質疑の報道の配信の字幕
・財務省 大臣の会見の概要（2026年10月27日）　https://www.mof.go.jp/public_relations/conference/my20261027.html
・総務省 大臣の会見の概要（2026年10月30日）　https://www.soumu.go.jp/menu_news/kaiken/01koho01_02001587.html
・デジタル庁 大臣の記者会見（2026年10月27日）　https://www.digital.go.jp/speech/minister-261027-01
・国家サイバー統括室 報道発表（2026年10月1日）　https://www.cyber.go.jp/pdf/press/houdou_20261001.pdf
・首相官邸「サイバーセキュリティに関する関係閣僚会議」（2026年10月26日）　https://www.kantei.go.jp/jp/105/actions/202610/26kaigi_cyber.html
・報道：ITmedia・＠IT・東洋経済・産経新聞・TBS・日本テレビ・テレビ朝日・ABEMA・弁護士ドットコムほか（2026年10月〜11月）
"""

# ⚠️ 語りは「11月3日の時点」のまま＝11-04 に会社の頁と報道へ当て直した（c620 を TBS の報道で直した）。公開の直前にもう一度当てて日付を直す
RECHECK = "11月4日"
TAIL = f"""動画に出てくる数字と日付は、会社の発表と、国や報道の記録によります（2026年11月3日時点。公開前の{RECHECK}に、会社の新着情報と報道を見直しました）。
※ サーバーの設計の不備についての TBS の報道（2026年11月3日）は、関係者の話として伝えられたもので、会社の発表では確かめられていません。
※ 懸賞金への情報提供の 735件は、11月2日の時点の数です。会社の発表では、11月4日18時の時点で 822件です。
※ 攻撃した者は、11月3日の時点で公表されていません。動画では「第三者」「攻撃した者」とお伝えしています。
※ 情報を公開された人と SNS の投稿者のお名前は出していません。会社の役員と記者は役職でお伝えしています。
※ SNS の投稿は、確かめられた情報ではありません（画面に注記しています）。
※ 画面の模式図は、会社の発表と報道をもとに描いた図です。"""

# ✅ ⑥（11-04）カズヤくん「Jはもっとロゴを大きく」→「J2 で決定」＝`qa_out/ep29_thumb.py` の J2。CM003＝本編 c513・c703 の地と同じ写真・CC BY 4.0
THUMB = "out/thumb/ep29/ep29_T_J2.png"
THUMB_MD5 = "e78e0941c810b43a374754688ac74b56"
THUMB_NOTE = ("※ サムネイルの写真は、Wikimedia Commons の {作者} の写真（CC BY 4.0）です。"
              "切り出し、明るさと彩度を変え、周りを黒へぼかして、文字を重ねています。")

TAGS = ["GMO", "GMOインターネット", "GMOインターネットグループ", "お名前.com", "デスクトップクラウド", "不正アクセス", "サイバー攻撃",
        "FX自動売買", "VPS", "情報漏えい", "懸賞金", "能動的サイバー防御", "事件検証", "ゆっくり解説", "解説", "ニュース"]

LIC_URL = {"CC BY 2.0": "https://creativecommons.org/licenses/by/2.0/deed.ja",
           "CC BY 3.0": "https://creativecommons.org/licenses/by/3.0/deed.ja",
           "CC BY 4.0": "https://creativecommons.org/licenses/by/4.0/deed.ja",
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
    """`ref/ep29/yougo.md` の「## 貼る本文」の節を**そのまま**返す（次の `---` か `## ` まで）。見出しの語が語りに出るかを当てる。"""
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
    """SPEC の値を辿って、素材の道（`ep29/…`）を全部出す（地に敷く写真も含む）。"""
    if isinstance(v, str):
        if v.startswith("ep29/"):
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
    ("own", r"^写真：\{作者\}／Wikimedia Commons（CC BY(?:-SA)? [234]\.0）(?:／改変(?:なし|：切出(?:・" + _MOS + r")?|：" + _MOS + r"))?$"),
    ("cc0", r"^写真：\{作者\}／Wikimedia Commons（CC0）(?:／改変：(?:切出・)?" + _MOS + r"|／改変：切出)?$"),
    ("pd", r"^写真：\{作者\}／Wikimedia Commons（PD）(?:／改変：(?:切出・)?" + _MOS + r"|／改変：切出)?$"),
    ("company", r"^出典：(?:GMOインターネットグループ 第\d+報|GMOインターネット開示|お名前\.com)"),
    ("gov", r"^出典：(?:財務省|総務省|デジタル庁|国家サイバー統括室)"),
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
        by.setdefault((S._ep29_author(p), lic), []).append(p)
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
    out.append(f"・GMOインターネットグループ・GMOインターネット・お名前.com の頁と資料の画面 {n.get('company', 0)}点＝引用（加工なし・出典は画面に表示）")
    out.append(f"・国の頁と資料の画面 {n.get('gov', 0)}点（出典は画面に表示）")
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
    tail = TAIL + ("\n" + THUMB_NOTE.replace(S._EP29_AUTHOR, S._ep29_author("ep29/cm003.jpg")) if THUMB_NOTE else "")
    desc = "\n".join([HEAD, WINDOW, chapters(), "", read_glossary(), "", PRIMARY, read_credits(), "", tail])
    # 🔴 入れてはいけない語（BGM のクレジット・ゆっくりの一文・煽り語・タグの残り）
    for bad in ("<", ">", "BGM", "DOVA", "OpenTracks", "ゆっくりボイス", "AquesTalk", "即死", "絶命", "地獄",
                "【映像あり】", "{作者}", S.EP23_AUTHOR_STANDIN):
        if bad in desc or bad in TITLE:
            raise SystemExit(f"🔴 入れてはいけない語「{bad}」が入っている。書かずに止めた。")
    # 🔴 事件の回（ルール §B2-11・§B2-11b）＝犯人・加害者と書かない・「顧客」と言い切らない・まだ終わっていない事件で「真相」を使わない
    #    ・「死亡」「流出」を使わない（官邸の窓口の頁の題の「個人情報流出」だけは原文の字）・group.gmo へのリンクを置かない
    chk = desc.replace("個人情報流出の被害に遭われた方", "")
    for bad in ("犯人", "加害者", "真相", "死亡", "流出", "顧客", "group.gmo"):
        if bad in TITLE or bad in chk:
            raise SystemExit(f"🔴 「{bad}」が入っている。書かずに止めた。")
    for need in ("03-5456-2560", "https://help.onamae.com/contact/", "cybercrimebounty.gmo", "見に行かない"):
        if need not in desc:
            raise SystemExit(f"🔴 窓口の「{need}」が無い（c701・c702・c703 の語りと事件の回の決まり）。書かずに止めた。")
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
    meta = {"slug": "ep29", "title": TITLE, "description": desc, "tags": TAGS, "thumbnail": THUMB,
            "genre": "jiko", "playlist": ""}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✓ 書いた → {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
