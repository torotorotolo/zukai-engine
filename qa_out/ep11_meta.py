# -*- coding: utf-8 -*-
"""11本目（チャレンジャー号）の `config/meta_ep11.json` を**機械で**組み立てる（2026-09-22・⑥）。

`qa_out/ep10_meta.py` を写して、この回の形に合わせた。

🔴 手で書かない理由（ep7〜ep10 と同じ）
  ① 用語は `ref/ep11/yougo.md` の「貼る本文」の囲みが正本＝**囲みの中をそのまま**貼る
  ② クレジットは `ref/CREDITS.md` §チャレンジャー の表を読んで数える。
     **権利の欄に PD 以外が1行でも混ざったら書かずに落ちる**（CC BY は撮影者名が使用条件）
  ③ 目次は `scene_jiko.CUTS` の秒を頭から積む＝**焼いた版と同じ秒**
  ④ タイトル 100字・説明 5,000字の上限を、書く前に確かめる

🔴 この回が 10本目と違うところ
  - 権利の形が**1つだけ**＝Public domain（米連邦 §105 ／ Commons の PD）。
    継承（ShareAlike）つきの素材は**1点も使っていない**ので、BY-SA の表示欄は置かない
  - **動く映像が7欄ある**＝`【映像あり】` を末尾に付ける
  - 🔴 **BGM を付ける回**だが、`audio_mix.BGM_CREDIT` は**概要欄に入れない**
    （ライセンス原文「著作権表示・提供等の表示は不要です。」＝必須でないクレジットは書かない）
  - ⚠️ 表の見出しの「写真56点＋止め絵20点」は ⑤c-2 時点の数で**古い**。
    ここでは**表の行を数え直す**（[[feedback-per-episode-constants-go-stale]]）

    python qa_out/ep11_meta.py            # 組み立てて config/meta_ep11.json に書く
    python qa_out/ep11_meta.py --dry      # 書かずに中身と字数だけ出す
"""
import json
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
import scene_jiko as S            # noqa: E402

YOUGO = HERE / "ref" / "ep11" / "yougo.md"
CREDITS = HERE / "ref" / "CREDITS.md"
OUT = HERE / "config" / "meta_ep11.json"

SECTION = "## スペースシャトル・チャレンジャー号 空中分解事故"
N_GLOSS = 11          # `ref/ep11/yougo.md` の「貼る本文」の語数（⑤a で確定）

# ✅ ④' で決め直したタイトル（台本第2版 §1-1 の推奨A）。
#    ⚠️ 型の「→」は**構造を示す印**であって本文ではない（ep7〜ep10 の実物に矢印は無い）。
#    🔴 つかみは決め所 `pr04`（ch5 L654）＝原文に当ててある行から取った。
#    🔴 **「爆発」は使わない**（①で確定）。8本目コロンビア号との差し分けは「氷」と「教師」。
#    🔴 `【映像あり】` は末尾（動く映像7欄）。
#    ⚠️ 二つ目の事実の終わりは **`。`**（④' の下書きは `、`）。
#       7本目・8本目はどちらも二つ目が**過去の言い切り**で終わり、そこを `。` でつないでいる
#       （9本目・10本目が `、` なのは、二つ目が連用形／かぎかっこで終わるため）。字数は変わらない。
TITLE = ("打ち上げの前夜、技術者はひとりも賛成しなかった。"
         "発射台にはつららが下がっていた。"
         "7人が亡くなったチャレンジャー号空中分解事故の真相【事故検証】【映像あり】")

# ⚠️ 書いてはいけないこと（台本第2版 §1-2〜§1-8）を守る：
#    会議の出席者の名前を出さない（役で呼ぶ）／タイトル・サムネに「爆発」を使わない／
#    「250万人の子どもが中継を見ていた」を使わない／乗員がいつ亡くなったかは言わない／
#    ファインマンの氷水の実演は書かない／「32か月後に飛行が再開した」も書かない。
HEAD = """【この動画について】
1986年1月28日の朝、アメリカ、フロリダの発射台は凍っていました。鉄の足場から、30センチほどのつららが何本も下がっています。午前11時38分、スペースシャトル「チャレンジャー号」が飛び立ちました。打ち上げは、これで25回目でした。その73秒後、機体は空の上でばらばらに壊れ、乗っていた7人が全員亡くなりました。

止まる機会は、前の夜にありました。飛んでよいかを決める会議で、作った会社の技術者は、ひとりも賛成しなかったのです。それが朝までにひっくり返ります。

この動画が使うのは、大統領の委員会がまとめた事故調査報告書（1986年6月6日）です。その第1巻の全文を、英語の原文で当たっています。

・つららと氷は、その朝どこまで広がっていたのか
・乗員7人は、どんな人たちだったのか
・73秒のあいだに、何がどの順番で起きたのか
・これは「爆発」だったのか
・継ぎ目のゴムの輪は、なぜすきまをふさげなかったのか
・前の夜の反対は、なぜ朝までにひっくり返ったのか
・24回うまくいっていたことは、何を意味していたのか
・海から上がった部品は、何を語ったのか
"""

PRIMARY = """【出典】
・大統領委員会（ロジャース委員会）『Report of the Presidential Commission on the Space Shuttle Challenger Accident』第I巻（1986年6月6日）
　https://www.nasa.gov/history/rogersrep/
・同 第IV章「事故の原因」／第V章「事故に寄与した原因」／第III章「事故」の各 Findings
・NASA 記録映画「Space Shuttle Challenger Accident Investigation」（44分44秒）
・米国立公文書館／USIA「REPORT ON THE SPACE SHUTTLE CHALLENGER ACCIDENT - KEEL, 1986」（Local ID 306-WNET-239）"""

# ⚠️ 温度と時刻の断りは**用語の節の末尾（※の2行）にすでにある**。ここで繰り返さない。
TAIL = """動画に出てくる数値・時刻・証言の言葉は、これらの記録によります。
資料によって数が違うところ、報告書が言い切っていないところは、画面でそのまま断っています。"""


def read_glossary() -> str:
    """`ref/ep11/yougo.md` の「## 貼る本文」の節を**そのまま**返す。

    ⚠️ この回の yougo.md は囲み（```）を使っていない。節の見出しから
       次の `---` か `## ` までを本文とする（区切りが無ければ落ちる）。
    """
    md = YOUGO.read_text(encoding="utf-8")
    m = re.search(r"^## 貼る本文[^\n]*\n(.*?)\n(?:---|## )", md, re.S | re.M)
    if not m:
        raise SystemExit("🔴 yougo.md の「貼る本文」の節が見つからない。書かずに止めた。")
    body = m.group(1).strip()
    if "【この動画に出てくる言葉】" not in body:
        raise SystemExit("🔴 囲みの中身が用語の本文ではない。書かずに止めた。")
    n = body.count("\n・")
    if n != N_GLOSS:
        raise SystemExit(f"🔴 用語の行が {n} 語（仕様は {N_GLOSS}）。書かずに止めた。")
    # 🔴 YouTube の概要欄は Markdown を解釈しない＝`**強調**` は**アスタリスクのまま出る**。
    #    正本（yougo.md）は読み物なので強調を残し、貼る側でだけ外す。
    body = body.replace("**", "")
    if "*" in body or "_" in body:
        raise SystemExit("🔴 外し切れない記号が残っている。書かずに止めた。")
    return body


def credit_rows() -> list:
    """§チャレンジャー の表の行を返す（欄・カット・年・権利・撮影者・出どころ）。"""
    lines = CREDITS.read_text(encoding="utf-8").splitlines()
    try:
        start = next(i for i, s in enumerate(lines) if s.startswith(SECTION))
    except StopIteration:
        raise SystemExit("🔴 CREDITS.md §チャレンジャー が見つからない。書かずに止めた。")
    rows = []
    for s in lines[start + 1:]:
        if s.startswith("## "):
            break
        if not s.startswith("| `"):
            continue
        c = [x.strip() for x in s.strip().strip("|").split("|")]
        if len(c) != 6:
            raise SystemExit(f"🔴 表の列が {len(c)} 個（仕様は 6）: {s}。書かずに止めた。")
        rows.append(c)
    if not rows:
        raise SystemExit("🔴 §チャレンジャー に表の行が1つも無い。書かずに止めた。")
    return rows


def read_credits() -> str:
    """素材のクレジットを組み立てる。**PD 以外が1行でもあれば落ちる。**"""
    rows = credit_rows()
    used = [c for c in rows if "未使用" not in c[1]]
    bad = [c[0] for c in used if not c[3].startswith("Public domain")]
    if bad:
        raise SystemExit(
            f"🔴 Public domain でない素材が {len(bad)} 点ある（CC BY/BY-SA は撮影者名や"
            f"継承が使用条件）。この道具は PD だけを前提に書いてある。書かずに止めた: {bad}")
    # 「記録映像 …」と名乗る欄＝動く映像から抜いた止め絵。写真とは出典が違う。
    stills = [c for c in used if c[5].startswith("記録映像")]
    photos = [c for c in used if not c[5].startswith("記録映像")]
    # 動く映像そのものの欄数は `footage.USE` から取る（表ではなく本番の配線を数える）
    import footage as F
    n_clip = len(F.USE)
    if n_clip == 0:
        raise SystemExit("🔴 `footage.USE` が空。【映像あり】を名乗れない。書かずに止めた。")
    return (
        "【素材】\n"
        f"・写真 {len(photos)}点：NASA（ケネディ宇宙センター／ジョンソン宇宙センター／"
        "マーシャル宇宙飛行センター）ほか。パブリックドメイン（合衆国法典17編105条）\n"
        f"・記録映像から抜いた静止画 {len(stills)}点：上の記録映画および米国立公文書館の"
        "記録映像より。パブリックドメイン（同上）\n"
        f"・動く映像 {n_clip}か所：NASA 記録映画「Space Shuttle Challenger Accident "
        "Investigation」より。パブリックドメイン（同上）\n"
        "※ 継承（ShareAlike）の条件が付く素材は、この回では1点も使っていません。")


def chapters() -> str:
    starts, t = {}, 0.0
    for cid, sec in S.CUTS:
        starts[cid] = t
        t += sec
    rows = [("pr01", "はじめに")]
    for key, (n, name) in S.CHAPTERS.items():
        first = next((c for c, _ in S.CUTS
                      if c.startswith(key) and c[len(key):].isdigit()), None)
        if first is None:
            raise SystemExit(f"🔴 章 {key} の最初のカットが無い。書かずに止めた。")
        rows.append((first, f"第{n}章 {name}"))
    rows.append(("ep01", "おわりに"))
    lines, last = ["【目次】"], float("-inf")
    for cid, label in rows:
        x = starts[cid]
        if x <= last + 10:
            raise SystemExit(f"🔴 目次の秒が前と10秒以上離れていない／逆順: {cid}。書かずに止めた。")
        last = x
        lines.append(f"{int(x // 60):02d}:{int(x % 60):02d} {label}")
    if len(rows) < 3 or starts[rows[0][0]] != 0.0:
        raise SystemExit("🔴 YouTube の目次の条件（0:00 から・3つ以上）を満たさない。書かずに止めた。")
    print(f"■ 設計の完成尺 {t:.2f} 秒＝{int(t // 60)}分{t % 60:05.2f}秒（30fps で {round(t * 30):,} コマ）")
    return "\n".join(lines)


def main() -> int:
    desc = "\n".join([HEAD, chapters(), "", read_glossary(), "",
                      PRIMARY, "", read_credits(), "", TAIL])
    # 🔴 入れてはいけない語（④ の決めごと。BGM のクレジットも入れない）
    for bad in ("<", ">", "BGM", "DOVA", "OpenTracks", "疑惑の霧",
                "250万", "ファインマン", "32か月"):
        if bad in desc or bad in TITLE:
            raise SystemExit(f"🔴 入れてはいけない語「{bad}」が入っている。書かずに止めた。")
    # 🔴🔴 「爆発」はタイトルに使わない（本文の第4章の章名は原文の語なので説明側には出る）
    if "爆発" in TITLE:
        raise SystemExit("🔴 タイトルに「爆発」が入っている。書かずに止めた。")
    if "【映像あり】" not in TITLE:
        raise SystemExit("🔴 動く映像がある回なのに【映像あり】が無い。書かずに止めた。")
    print(f"タイトル {len(TITLE)} 字（上限 100 ／ 型の幅 67〜94）")
    print(f"説明     {len(desc)} 字（上限 5,000）")
    if len(TITLE) > 100 or len(desc) > 5000:
        raise SystemExit("🔴 上限を超えた。書かずに止めた。")
    if not (67 <= len(TITLE) <= 94):
        raise SystemExit("🔴 タイトルが型の幅（67〜94字）から外れた。書かずに止めた。")

    # ✅ 2026-09-22 カズヤくん決定＝**P（写真は M のマコーリフ・赤は c210 の決め所）**。
    #    4巡して決めた。t1 の d は絵と文字が食い違い、t2 の g は赤が目を隠し、
    #    t3 の m で顔が出て、t4 で赤の行だけを4案くらべた。
    thumb = "out/thumb/ep11-t4/ep11_p_jugyou.png"
    meta = {
        "slug": "ep11",
        "title": TITLE,
        "description": desc,
        "tags": ["チャレンジャー号", "スペースシャトル", "1986年", "NASA", "事故検証",
                 "図解", "事故調査委員会", "STS-51-L", "Oリング", "宇宙開発",
                 "ロジャース委員会", "一次資料", "解説", "ドキュメンタリー"],
        "thumbnail": thumb,
        "genre": "jiko",
        "playlist": "",
    }
    if "--dry" in sys.argv:
        print("\n" + TITLE + "\n\n" + desc)
        return 0
    if not (HERE / thumb).exists():
        raise SystemExit(f"🔴 サムネが無い: {thumb}。焼いてから書くこと。")
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"✓ 書いた → {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
