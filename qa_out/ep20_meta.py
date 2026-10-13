# -*- coding: utf-8 -*-
"""20本目（日本航空123便のリメイク）の `config/meta_ep20.json` を**機械で**組み立てる（2026-10-11・⑥）。

🔴 2026-10-13：公開中の 87-AJdfgvok は、この道具の値と**違う**＝この道具の出力で `retitle` しない（題が戻る）
   - 題＝公開のあとに替わった「生き残った4人は全員が最後尾にいた。…」（この道具は「全員が最後尾」を止める＝下の入れてはいけない語）
   - サムネ＝H 型 v1・地＝写真-124（`out/thumb/ep20-ab/ep20_H_p124_v1.png`・カズヤくんの選び）
   - 説明＝下の TAIL の「サムネイルの画像は、生成AIで作ったイメージです。…」の1行を外した（`qa_out/ep20_r01/drop_ai_line.py`・カズヤくんの決め）

`qa_out/ep19_meta.py` を写して、この回の形に合わせた。

🔴 手で書かない理由（ep7〜ep19 と同じ）
  ① 用語は `ref/ep20/yougo.md` の「## 貼る本文」の節が正本＝**そのまま**貼る（`**` だけ外す）
  ② 素材の点数は**章ファイルの実配線**（`cuts.SPEC` の写真・頁・図＝尻や頭の差し込みも含む／`footage.USE` の映像）から数え、
     権利は**画面の出典表記**（`ref/ep20/credits.json`・`clips.json`）で照らす。名乗れない素材が出たら落ちる
  ③ 目次は `scene_jiko.CUTS` の秒を頭から積む＝**焼いた版と同じ秒**（章の扉の2秒は CUTS に入っている）
  ④ タイトル 100字・説明 5,000字の上限と、入れてはいけない語を、書く前に確かめる

🔴 この回が 19本目と違うところ
  - 権利：運輸安全委員会の報告書と解説＝「公共データ利用規約（第1.0版）」（PDL1.0）＝出典と「加工して作成」を書く
    （sources.md §3）／写真-124 は委員会の外の人が撮った写真＝引用（PDL1.0 1.2・1.7）／CC BY 2.0・CC BY 3.0・CC BY-SA 2.0・3.0
    ／防衛省・自衛隊「昭和60年防衛庁記録」（CC BY 3.0）
  - 【映像あり】は付けない（了承② 10-08＝実効の幅 中央値544px）
  - 乗員・乗客・遺族の名前は出さない（台本 §1-4）
  - 末尾に ※ でリメイクと記す（旧版＝2本目・2026年8月公開）

    python qa_out/ep20_meta.py            # 組み立てて config/meta_ep20.json に書く
    python qa_out/ep20_meta.py --dry      # 書かずに中身と字数だけ出す
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

YOUGO = HERE / "ref" / "ep20" / "yougo.md"
CREDITS_JSON = HERE / "ref" / "ep20" / "credits.json"
CLIPS = HERE / "ref" / "ep20" / "clips.json"
OUT = HERE / "config" / "meta_ep20.json"

N_GLOSS = 19          # `ref/ep20/yougo.md` の「貼る本文」の語数（⑥で語りに当てて確定）
# ⚠️ 下の値は⑥で配線から数えた点数（変わったら止まる＝文の点数を当て直す）。10-11 の版（⑥の前の直しのあと）
N_COUNTS = {"ccby2": 1, "photo": 48, "ccby3": 6, "ccbysa": 2, "fig": 20, "page_report": 4, "quote124": 1,
            "page_kaisetsu": 1, "kfig": 1, "page_kankoku": 1, "film": 7}

# ✅ 台本第2版 §1-1 の B'（承認① 2026-10-08 カズヤくん・93字）。「死亡」は使わない・【映像あり】は付けない
TITLE = ("「ドーン」のあと約30分、機体はほとんどの操縦機能を失ったまま飛んだ。"
         "発端は7年前の不適切な修理と推定され、"
         "520人が亡くなった日本航空123便墜落事故の真相【事故検証】【ゆっくり解説】")
TITLE_LEN = 93

# ⚠️ 本文（台本第2版 c101〜c108）で言っていることだけを書く
HEAD = """【この動画について】
1985年8月12日、午後6時24分35秒。羽田を飛び立って約12分の日本航空123便で、「ドーン」というような音がしました。それから約30分、機体はほとんど思いどおりに操縦できないまま飛び、群馬県の山の中に墜落しました。乗っていた524人のうち、520人が亡くなりました。

報告書は、客室のいちばん後ろにある「壁」（後部圧力隔壁）が壊れたためと推定しています。そのもとは、7年前の不適切な修理とされます。そして41年たった2026年、その修理をめぐって新しい動きがありました。

この動画は、運輸安全委員会の航空事故調査報告書（1987年）と、同 報告書についての解説（2011年）を中心に、アメリカ連邦航空局（FAA）の資料、国土交通大臣の会見、報道を読んで作っています。時刻は日本の時刻、長さや高さはメートル法に直して伝えます。

・あの日、操縦室と客室で何が起きていたのか
・壁はなぜ壊れ、その傷はなぜ7年のあいだ見つからなかったのか
・よく言われる疑問に記録はどう答え、何がまだ分かっていないのか
"""

# 台本第2版 §10 の資料と `ref/ep20/sources.md`（§1-1・§2-1・§4-2・§5）から（URL は sources の写し）
PRIMARY = """【出典】
・運輸省航空事故調査委員会「航空事故調査報告書 日本航空株式会社所属 ボーイング式747SR-100型 JA8119 群馬県多野郡上野村山中 昭和60年8月12日」（1987年6月19日・運輸安全委員会が公開）　https://jtsb.mlit.go.jp/jtsb/aircraft/download/bunkatsu.html
・運輸安全委員会「日本航空123便の御巣鷹山墜落事故に係る航空事故調査報告書についての解説」（2011年7月）　https://jtsb.mlit.go.jp/kaisetsu/nikkou123.html
・アメリカ連邦航空局（FAA）「Lessons Learned」JA8119 の頁　https://www.faa.gov/lessons_learned/transport_airplane/accidents/JA8119
・国土交通大臣の会見（2026年8月25日）　https://www.mlit.go.jp/report/interview/daijin260825.html
・産経新聞の報道（2026年8月12日・ITmedia ビジネスオンラインに転載）　https://www.itmedia.co.jp/business/articles/2608/12/news087.html"""

TAIL = """動画に出てくる数値・時刻・言葉は、これらの記録によります。
記録が言い切っていないところは、画面でそのまま断っています。
※ 画面の再現イラスト・模式図・地図は、記録をもとに描いた図です。尾部が壊れていく順番の絵は、報告書の推定にもとづく推定の絵です。
※ 操縦室の声は、報告書に載っている文字の記録（CVR 記録）から読んでいます。音声は使っていません。
※ 亡くなった方、乗員、乗客、ご遺族のお名前は出していません。乗員は役職で呼んでいます。
※ サムネイルの画像は、生成AIで作ったイメージです。実際の写真ではありません。本編の写真と映像は、すべて実際の記録です。
※ サムネイルを比べるためのもう1枚には、Dennis HKG さんの写真（JA8119・1985年・CC BY 2.0）を切り出して使っています。
※ この動画は、2026年8月に公開した日本航空123便の動画を、作り直したものです。"""

# ✅ 承認①（10-08）＝旧版の型で2点だけ直す（赤「生存者4人 全員が後ろの席」・地＝JA8119 の CC BY 2.0）。B1 は公開のあとカズヤくんが手動で A/B に入れる
#    ⑥（10-11）：試写のあとカズヤくん「サムネAの写真がイマイチ」→ 生成 AI の地（案A「尾翼がはじける瞬間」・`gen_thumb_ai.py jal_a`）に替え、
#    「上下の文字帯の間ギリギリを飛行機で埋める」寄り＝`thumb_jiko.ep20()` の ep20_A_ai。実写の案（ep20_A.png・md5 c645b98c…）は使わない。
#    概要欄の断り書き＝ルール 6-55⑦（生成 AI のイメージ）。B1＝`thumb_docu.ep20_b1()`（JA8119 の写真の差し込み＝もう1枚の注）
#    → カズヤくん（10-11）「案Bの画像も生成（当時の写真の質感の粗さで）」「飛行機をもっと拡大。文字帯の間を飛行機で埋める」→ 公開のサムネは
#    **案B v3**（`thumb_jiko.ep20()` の ep20_B_ai_v3＝尾翼を失った機体・切り出し 横 587〜1440）に決まった。A/B のもう1枚は B1 のまま
THUMB = "out/thumb/ep20-ab/ep20_B_ai_v3.png"
THUMB_MD5 = "944f655eca14fda6116a0f9aed45a672"

PDL = "公共データ利用規約（第1.0版）"
REPORT = "運輸安全委員会「航空事故調査報告書 62-2（JA8119）」"
KAISETSU = "運輸安全委員会「報告書についての解説」"


def read_glossary() -> str:
    """`ref/ep20/yougo.md` の「## 貼る本文」の節を**そのまま**返す（次の `---` か `## ` まで）。"""
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
    """SPEC の値を辿って、素材の道（`ep20/…`）を全部出す（尻・頭の差し込み・over も含む）。"""
    if isinstance(v, str):
        if v.startswith("ep20/"):
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
        if s.startswith("出典：航空事故調査報告書（1987年）の勧告"):
            return "page_kankoku"
        if s.startswith("出典：航空事故調査報告書（1987年）"):
            return "page_report"
        if s.startswith("出典：運輸安全委員会の解説（2011年）"):
            return "page_kaisetsu"
        return None
    if "航空事故調査報告書 62-2（JA8119）写真-124" in s and "引用" in s:
        return "quote124"
    if "航空事故調査報告書 62-2（JA8119）写真-" in s or "航空事故調査報告書 62-2（JA8119）別添1 写真-" in s:
        return "photo"
    if "航空事故調査報告書 62-2（JA8119）別添1 付図-" in s or "航空事故調査報告書 62-2（JA8119）付図-" in s:
        return "fig"
    if "事故調査報告書についての解説（62-2 JA8119）図" in s:
        return "kfig"
    if "（Panoramio）／CC BY 3.0" in s:
        return "ccby3"
    if "／CC BY 2.0／" in s:
        return "ccby2"
    if "／CC BY-SA" in s and "改変なし" in s:
        return "ccbysa"
    return None


def used_material():
    """章ファイルの実配線から、写真・図・頁・映像を数える。権利は画面の出典表記で照らす。"""
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
            k = _kind(Path(p).stem, s)
            if k is None:
                bad.append(f"{cid}:{p}（名乗れない：{s}）")
                continue
            got.setdefault(k, OrderedDict()).setdefault(Path(p).stem, (cid, s))
    films = OrderedDict()
    for cid, u in F.USE.items():
        k = u["clip"]
        c = clips.get(k)
        if c is None:
            bad.append(f"{cid}:{k}（clips.json に無い）")
            continue
        if not c.get("credit", "").startswith("出典：防衛省・自衛隊『昭和60年防衛庁記録』／CC BY 3.0"):
            bad.append(f"{cid}:{k}（映像の出典が防衛庁記録でない：{c.get('credit')}）")
        films.setdefault(cid, c)
    if bad:
        raise SystemExit(f"🔴 名乗れない素材がある。書かずに止めた: {bad}")
    counts = {k: len(v) for k, v in got.items()}
    counts.update(film=len(films))
    print(f"■ 素材（配線から）：{counts}")
    if N_COUNTS is not None and counts != N_COUNTS:
        raise SystemExit(f"🔴 点数が⑥で数えた値 {N_COUNTS} と違う。文の点数を当て直すこと。書かずに止めた。")
    return got, films, counts


LIC_URL = {"CC BY 2.0": "https://creativecommons.org/licenses/by/2.0/", "CC BY 3.0": "https://creativecommons.org/licenses/by/3.0/",
           "CC BY-SA 2.0": "https://creativecommons.org/licenses/by-sa/2.0/", "CC BY-SA 3.0": "https://creativecommons.org/licenses/by-sa/3.0/"}
# Commons の頁は番号の URL（ルール 6-52＝題名の %xx で字数がふくらまない）＝`qa_out/ep20_commons_pageids.json`（10-11 に API で1回引いた）
PAGEIDS = HERE / "qa_out" / "ep20_commons_pageids.json"
FILM_URL = "https://www.youtube.com/watch?v=LKrLJc4R0X8"      # 防衛省・自衛隊の公式チャンネル（clips.json の BV）


def read_credits() -> str:
    got, films, n = used_material()
    pid = json.loads(PAGEIDS.read_text(encoding="utf-8"))
    by = OrderedDict()
    for k in ("ccby3", "ccby2", "ccbysa"):
        for stem, (cid, s) in (got.get(k) or {}).items():
            who, lic, mod = [x.strip() for x in s.split("：", 1)[1].split("／")[:3]]
            if stem not in pid or lic not in LIC_URL:
                raise SystemExit(f"🔴 {stem} の Commons の頁かライセンスの URL が無い。書かずに止めた。")
            by.setdefault((who, lic, mod), []).append(pid[stem]["url"])
    pages = n.get("page_report", 0) + n.get("page_kankoku", 0)
    still = sum(1 for c in films if c.endswith("~t") and __import__("footage").USE[c].get("still"))
    out = ["【写真・図・頁・映像】"]
    out.append(f"・{REPORT}の写真 {n.get('photo', 0) + n.get('quote124', 0)}点・付図 {n.get('fig', 0)}点・頁 {pages}枚、"
               f"{KAISETSU}の図 {n.get('kfig', 0)}点・頁 {n.get('page_kaisetsu', 0)}枚"
               f"＝{PDL}にもとづいて利用（出典：運輸安全委員会 https://jtsb.mlit.go.jp/ ・縮小・切り出しなどの加工をして作成）")
    if n.get("quote124"):
        out.append("・報告書の写真-124（奥多摩町の上空を飛ぶ事故機・地上で撮影）は、撮った方が委員会の外の方のため、"
                   "引用として加工せずに使っています")
    out.append("・報告書の写真-14 は、写っている方の顔にモザイクをかけています")
    for (who, lic, mod), urls in by.items():
        how = "加工なし・額に入れて表示" if "改変なし" in mod else "切り出し"
        out.append(f"・{who}の写真 {len(urls)}点＝{lic}（{LIC_URL[lic]}）・{how}　" + "　".join(urls))
    out.append(f"・防衛省・自衛隊「昭和60年防衛庁記録」の映像 {n['film'] - still}か所と静止画 {still}枚＝CC BY 3.0"
               f"（{LIC_URL['CC BY 3.0']}）・切り出し・再生速度の変更　{FILM_URL}")
    out.append("※ 国の機関（運輸安全委員会・防衛省）の資料を使っていますが、これらの機関がこの動画を作ったり、推奨・支持したりしているものではありません")
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
    # 🔴 入れてはいけない語（BGM のクレジット・伏せ字・ゆっくりの一文＝14本目だけ・煽り語・旧版の BGM の名・乗員の実名の代わりの語）
    for bad in ("<", ">", "BGM", "DOVA", "OpenTracks", "陰鬱な灰色", "蒲鉾", "ﾀﾋ", "ゆっくりボイス",
                "AquesTalk", "即死", "絶命", "地獄", "全員が最後尾", "ミサイルが", "撃墜", "陰謀"):
        if bad in desc or bad in TITLE:
            raise SystemExit(f"🔴 入れてはいけない語「{bad}」が入っている。書かずに止めた。")
    for bad in ("死亡",):
        if bad in TITLE or bad in desc:
            raise SystemExit(f"🔴 「{bad}」が入っている。書かずに止めた。")
    if TITLE.startswith("【映像あり】"):
        raise SystemExit("🔴 【映像あり】は付けない回（了承②）。書かずに止めた。")
    if not TITLE.endswith("【事故検証】【ゆっくり解説】"):
        raise SystemExit("🔴 タイトルの末尾が「【事故検証】【ゆっくり解説】」でない（B4-8）。書かずに止めた。")
    print(f"タイトル {len(TITLE)} 字（上限 100 ／ 承認は {TITLE_LEN}）")
    print(f"説明     {len(desc)} 字（上限 5,000）")
    if len(TITLE) > 100 or len(desc) > 5000:
        raise SystemExit("🔴 上限を超えた。書かずに止めた。")
    if len(TITLE) != TITLE_LEN:
        raise SystemExit(f"🔴 承認した題（{TITLE_LEN}字）と字数が違う＝写し間違い。書かずに止めた。")

    meta = {
        "slug": "ep20",
        "title": TITLE,
        "description": desc,
        "tags": ["日航123便", "日本航空123便", "御巣鷹", "JA8119", "後部圧力隔壁", "修理ミス", "航空事故",
                 "運輸安全委員会", "事故調査報告書", "ボイスレコーダー", "1985年", "事故検証", "一次資料",
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
