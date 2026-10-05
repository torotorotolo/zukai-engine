# -*- coding: utf-8 -*-
"""18本目（スレッシャー号のリメイク）の `config/meta_ep18.json` を**機械で**組み立てる（2026-10-05・⑥）。

`qa_out/ep16_meta.py` を写して、この回の形に合わせた。

🔴 手で書かない理由（ep7〜ep16 と同じ）
  ① 用語は `ref/ep18/yougo.md` の「## 貼る本文」の節が正本＝**そのまま**貼る（`**` だけ外す）
  ② 素材の点数は**章ファイルの実配線**（`cuts.SPEC` の写真・頁＝尻や頭の差し込みも含む／`footage.USE` の映像）から数え、
     権利は**画面の出典表記**（`ref/ep18/credits.json`・`clips.json`）で照らす。PD でない写真・頁が出たら落ちる
  ③ 目次は `scene_jiko.CUTS` の秒を頭から積む＝**焼いた版と同じ秒**（章の扉の2秒は CUTS に入っている）
  ④ タイトル 100字・説明 5,000字の上限と、入れてはいけない語を、書く前に確かめる

🔴 この回が 16本目と違うところ
  - 写真・頁・記録映画は**すべて米国政府の職務著作（PD）**＝CC の点は0＝許諾の URL は要らない
  - 動く映像あり：記録映画（NARA RG 428）と**フリー素材（Pexels・Pixabay）**＝フリー素材は「イメージ」と断る
    （ルール §2-5c・画面にも「イメージ（フリー素材）」）。【映像あり】は付けない（②③で確定＝記録映画は SD）
  - 米海軍・米国防総省の写真と映像＝「推奨・支持を意味しない」断り書き（ルール §5b-98⑧）
  - 末尾に ※ でリメイクと記す（09-30 カズヤくん）。14本目だけの「ゆっくりボイス」の一文は入れない（§6-53）
  - タイトル＝R（④'・10-01 カズヤくん承認・97字）＝末尾「…喪失事故の真相【事故検証】【ゆっくり解説】」は §B4-1 の**この回だけの例外**
  - サムネ＝A（旧版3本目と同じ物）＝記録映画 NARA 85185 のコマ（PD）。B1・B2 は公開のあとカズヤくんが手動で A/B テストに入れる

    python qa_out/ep18_meta.py            # 組み立てて config/meta_ep18.json に書く
    python qa_out/ep18_meta.py --dry      # 書かずに中身と字数だけ出す
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

YOUGO = HERE / "ref" / "ep18" / "yougo.md"
CREDITS_JSON = HERE / "ref" / "ep18" / "credits.json"
CLIPS = HERE / "ref" / "ep18" / "clips.json"
OUT = HERE / "config" / "meta_ep18.json"

N_GLOSS = 16          # `ref/ep18/yougo.md` の「貼る本文」の語数（⑥で本文に当てて確定＝ep18_yougo.py --spec）
# ⚠️ 下の4つは⑥で配線から数えた値（変わったら止まる＝文の点数を当て直す）。`ref/CREDITS.md` の表（写真31・頁23）との差は
#    使っていない5点＝記録映画のコマ film_a・b・c（⑤b-7c で動く映像に替えた）と c104 の控えの頁 pg2005・pg4204（⑤b-8）。
#    記録映画は NARA 12本のうち 83766 を使っていない（ca09 は 83757＝⑤b-7c）
N_PHOTOS, N_PAGES, N_FILMS, N_STOCK = 28, 21, 11, 11

# ✅ 台本第2版 §1-1 の R（④'・10-01 カズヤくん「出来る限り旧版に近いタイトル」）。「死亡」は使わない
TITLE = ("事故の約5か月前、前の艦長は「最も危険なのは試験深度付近での浸水」と書いていた。"
         "調べた継手の13.8%が落ちても保温材は外されず、"
         "スレッシャー号129名喪失事故の真相【事故検証】【ゆっくり解説】")

# ⚠️ 本文（台本第2版 c101〜c117）で言っていることだけを書く。問いは c114 の言い方
HEAD = """【この動画について】
1963年4月10日、午前9時13分。アメリカ東海岸の沖で、救難艦スカイラークに、海の中から声が届きました。声の主は、アメリカ海軍の原子力潜水艦スレッシャー。軽い問題が起き、浮き上がろうとしている、という知らせでした。数分後、声は途切れました。乗っていた129人は、全員が亡くなりました。沈んだ海の深さは、約2,600メートルです。

事故を調べた海軍の査問会は、機関室の浸水がおそらく始まりだったとみました。でも約2年後、海軍長官の最後の意見書には「スレッシャーを失った原因は決まっていない」とあります。一方で、前の艦長は事故の約5か月前に「最も危険なのは、試験深度かその近くでの海水の浸水だ」と書いていました。

この動画は、長く機密だった事故を調べた記録（2020年から海軍が23回に分けて公開・合わせて5,000頁を超える）と、アメリカ議会の公聴会の記録（1965年刊）を、原文の英語で読んで作っています。時刻は現地の時刻、深さや長さはメートルに直して伝えます。

・艦はなぜ浮き上がれなかったのか
・検査の結果や最後の声は、なぜ先へ伝わらなかったのか
・海の底に何が残ったのか
"""

# 台本第2版 §10 の出典一覧と `ref/ep18/sources.md`（S-J・L-S2・D・A-R・P-AP・棚）から
PRIMARY = """【出典】
・米海軍「THRESHER RELEASE」（情報公開の法律による公開・2020〜2023年・23回）＝査問会の記録（第1回）・認定と意見と勧告（第8回）・証拠（第9・10回）・上級の意見書（第18回）ほか　https://www.secnav.navy.mil/foia/readingroom/HotTopics/Forms/AllItems.aspx?RootFolder=%2Ffoia%2Freadingroom%2FHotTopics%2FTHRESHER%20RELEASE
・米議会 両院原子力合同委員会の公聴会記録『Loss of the U.S.S. "Thresher"』（1963・64年の公聴会・1965年刊）　https://purl.stanford.edu/yk130sc8375
・米国防総省の発表 No.710-64（1964年10月1日）・No.509-63（1963年4月10日）
・AP通信「Skipper: Docs show no coverup in submarine sinking」（2021年8月2日・Military Times 掲載）　https://www.militarytimes.com/news/your-navy/2021/08/02/skipper-docs-show-no-coverup-in-submarine-sinking/
・米海軍 NAVSEA「USS Thresher: A Loss, A Legacy」（2023年）　https://www.navsea.navy.mil/Media/News/Article/3354927/uss-thresher-a-loss-a-legacy/
・B. Rule の海軍作戦部次長あての書簡（2013年4月10日・元分析官の個人の見方）　https://www.iusscaa.org/articles/brucerule/letter_to_the_deputy_cno.htm
・J. W. Stierman『Public relations aspects of a major disaster: a case study of the loss of USS Thresher』（1964年・ボストン大学の修士論文）　https://archive.org/details/publicrelationsa00stie"""

TAIL = """動画に出てくる数値・日付・証言の言葉は、これらの記録によります。
記録が言い切っていないところは、画面でそのまま断っています。
※ 画面の再現イラスト・模式図・地図は、記録をもとに描いた図です。9時18分すぎに船体が押しつぶされた場面は、査問会の意見にもとづく推定の絵です。
※ サムネイルは、米海軍の記録映画（NARA 85185・パブリックドメイン）のコマを切り出し、色調を整えて文字を重ねたものです。
※ この動画は、2026年8月に公開したスレッシャー号の動画を、作り直したものです。"""

THUMB = "out/thumb/ep18-ab/ep18_A_rival.png"
THUMB_MD5 = "392074a9068fd14eabf47cc0be2192fa"      # 10-03 に公開中の旧版と画素で照らした A（差 2.51/255）

PD_MARK = "パブリックドメイン"
DOC_ORDER = ["査問会の記録", "査問会の証拠", "上級の意見書", "米議会 両院原子力合同委員会の公聴会記録",
             "国防総省の発表 No.710-64"]


def read_glossary() -> str:
    """`ref/ep18/yougo.md` の「## 貼る本文」の節を**そのまま**返す（次の `---` か `## ` まで）。"""
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


def _doc_name(s: str) -> str:
    """頁の画面の出典表記 →資料名（「出典：査問会の記録 第1巻（第1回公開） PDF 38頁」→「査問会の記録」）。"""
    name = s.replace("出典：", "").split("（")[0].split(" PDF")[0]
    return re.sub(r"\s*第\d+巻$", "", name).strip()


def _walk(v):
    """SPEC の値を辿って、素材の道（`ep18/…`）を全部出す（尻・頭の差し込み・over も含む）。"""
    if isinstance(v, str):
        if v.startswith("ep18/"):
            yield v
    elif isinstance(v, dict):
        for x in v.values():
            yield from _walk(x)
    elif isinstance(v, (list, tuple)):
        for x in v:
            yield from _walk(x)


def used_material():
    """章ファイルの実配線から、写真・頁（資料ごと）・記録映画・フリー素材を数える。権利は画面の出典表記で照らす。"""
    import cuts
    import footage as F
    cred = json.loads(CREDITS_JSON.read_text(encoding="utf-8"))
    clips = json.loads(CLIPS.read_text(encoding="utf-8"))
    photos, pages, bad = OrderedDict(), OrderedDict(), []
    for cid, sp in cuts.SPEC.items():
        for p in _walk(sp):
            if not re.search(r"\.(jpe?g|png)$", p, re.I):
                continue
            # 動く映像の控えの静止画（`fb_<cid>`・`stock/fb_<cid>`）は取れなかったときだけ出る＝本番は映像（切り出し 33/33）
            if Path(p).stem.startswith("fb_"):
                continue
            s = cred.get(p)
            if s is None:
                bad.append(f"{cid}:{p}（credits.json に無い）")
                continue
            stem = Path(p).stem
            if stem.startswith("pg"):
                # 頁の画面の表記は資料名と頁だけ（PD の字は無い）＝資料名が米国政府の文書の一覧にあるかで照らす
                if _doc_name(s) not in DOC_ORDER:
                    bad.append(f"{cid}:{p}（資料名が米国政府の文書の一覧に無い：{s}）")
                    continue
                pages.setdefault(stem, (cid, s))
            elif PD_MARK in s:
                photos.setdefault(stem, (cid, s))
            else:
                bad.append(f"{cid}:{p}（PD でない：{s}）")
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
            if PD_MARK not in c.get("credit", "") or not k.startswith("nara"):
                bad.append(f"{cid}:{k}（記録映画が PD の NARA でない）")
            films.setdefault(k, c)
    if bad:
        raise SystemExit(f"🔴 名乗れない素材がある。書かずに止めた: {bad}")
    got = (len(photos), len(pages), len(films), len(stock))
    print(f"■ 素材：写真 {got[0]}点・頁 {got[1]}枚・記録映画 {got[2]}本・フリー素材 {got[3]}本（配線から）")
    if got != (N_PHOTOS, N_PAGES, N_FILMS, N_STOCK):
        raise SystemExit(f"🔴 点数が⑥で数えた値 {(N_PHOTOS, N_PAGES, N_FILMS, N_STOCK)} と違う。文の点数を当て直すこと。"
                         "書かずに止めた。")
    return photos, pages, films, stock


def read_credits() -> str:
    photos, pages, films, stock = used_material()
    docs = Counter()
    for _, (cid, s) in pages.items():
        docs[_doc_name(s)] += 1
    nara = sorted(int(k[4:]) for k in films)
    by_site = OrderedDict()
    for k, c in stock.items():
        site = c["credit"].split("：", 1)[1].split("／")[0].strip()
        by_site.setdefault(site, [])
        if c["author"] not in by_site[site]:
            by_site[site].append(c["author"])
    out = ["【写真・頁・記録映画】すべて米国政府の職務著作（パブリックドメイン）"]
    out.append(f"・写真 {len(photos)}点：米海軍（NARA 289-T「Photographs Taken During the Search for the USS Thresher」・"
               "NARA 428-N・Wikimedia Commons の米海軍の写真）")
    out.append(f"・記録映画 {len(films)}本：米海軍の記録映画（NARA RG 428：" + "・".join(map(str, nara)) + "）")
    out.append(f"・報告書の頁 {len(pages)}枚：" + "・".join(f"{d} {docs[d]}枚" for d in DOC_ORDER if docs[d]))
    out.append("※ 米海軍・米国防総省の写真と映像を使っていますが、米海軍・米国防総省がこの動画を推奨・支持していることを"
               "意味するものではありません（The appearance of U.S. Department of Defense (DoD) visual information "
               "does not imply or constitute DoD endorsement.）")
    out.append(f"【映像（イメージ）】フリー素材 {len(stock)}本＝本編の画面に「イメージ（フリー素材）」と出した映像です"
               "（実際の記録ではありません）")
    for site, who in by_site.items():
        out.append(f"・{site}：" + "、".join(who))
    print(f"■ 頁の資料 {dict(docs)}／フリー素材 {[(s, len(w)) for s, w in by_site.items()]}")
    return "\n".join(out)


def chapters() -> str:
    starts, t = {}, 0.0
    for cid, sec in S.CUTS:
        starts[cid] = t
        t += sec
    rows = []
    for key, (n, name) in S.CHAPTERS.items():
        first = next((c for c, _ in S.CUTS
                      if c.startswith(key) and c[len(key):].isdigit()), None)
        if first is None:
            raise SystemExit(f"🔴 章 {key} の最初のカットが無い。書かずに止めた。")
        rows.append((first, f"第{n}章 {name}"))
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
    for bad in ("<", ">", "BGM", "DOVA", "OpenTracks", "疑惑の霧", "Keido", "陰鬱な灰色", "ﾀﾋ", "ゆっくりボイス",
                "AquesTalk", "即死", "絶命", "地獄", "1300"):
        if bad in desc or bad in TITLE:
            raise SystemExit(f"🔴 入れてはいけない語「{bad}」が入っている。書かずに止めた。")
    for bad in ("死亡",):
        if bad in TITLE:
            raise SystemExit(f"🔴 タイトルに「{bad}」が入っている。書かずに止めた。")
    if "【映像あり】" in TITLE:
        raise SystemExit("🔴 【映像あり】が付いている（この回は付けない＝②③）。書かずに止めた。")
    if not TITLE.endswith("【事故検証】【ゆっくり解説】"):
        raise SystemExit("🔴 タイトルの末尾が「【事故検証】【ゆっくり解説】」でない（B4-8）。書かずに止めた。")
    print(f"タイトル {len(TITLE)} 字（上限 100 ／ 承認は 97）")
    print(f"説明     {len(desc)} 字（上限 5,000）")
    if len(TITLE) > 100 or len(desc) > 5000:
        raise SystemExit("🔴 上限を超えた。書かずに止めた。")
    if len(TITLE) != 97:
        raise SystemExit("🔴 承認した題（97字）と字数が違う＝写し間違い。書かずに止めた。")

    meta = {
        "slug": "ep18",
        "title": TITLE,
        "description": desc,
        "tags": ["スレッシャー号", "スレッシャー", "USS Thresher", "SSN-593", "原子力潜水艦", "潜水艦事故",
                 "アメリカ海軍", "査問会", "サブセーフ", "1963年", "事故検証", "図解", "一次資料", "解説",
                 "ゆっくり解説"],
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
        raise SystemExit(f"🔴 サムネ A が無いか、10-03 に照らした物と違う: {THUMB}。書かずに止めた。")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✓ 書いた → {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
