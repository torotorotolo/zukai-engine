# -*- coding: utf-8 -*-
"""check_credits.py — **画面に出る副題の主張**と**素材の出どころ**を突き合わせる（2026-09-14 新設・14本目）。

■ なぜ要るか（7本目 ⑤c §A-7）
    ```
    grep -l CREDITS tools/check_*.py tools/qa_all.py   → 0件
    ```
    門番13本は**カット表と台本しか見ていない**。「副題が名乗る年・場所」を
    **クレジット表（＝素材の出どころ）と突き合わせる向きの走査が存在しなかった**
    （[[feedback-gates-blind-spot-is-the-scan-direction]]＝測る線の向きの穴）。
    そのせいで 7本目は、

      - `pr10`「降ろされた旅客機 **2001年9月11日**」に **2024年の Alaska 737-9 MAX**
      - `c309`「客室の座席にある電話 **2001年以前**」に **2018年の A220 の客室**
      - `c320`「空港の出発案内板 **2001年以前**」に **2011年のジュネーブの板**

    が入ったまま、**門番13本が1本も鳴らずに**検品画像まで来た（12欄）。

■ 測るもの
    1. 🔴 **年の主張**。副題の `NNNN年撮影` と `2001年以前` を表の撮影年と突き合わせる
    2. 🔴 **表に無い写真**（fail closed。0件を「問題なし」と読ませない）
    3. 🔴 **CC BY なのに撮影者が空**（撮影者名は使用条件そのもの）
    4. ⚠️ **原題の地名・機種と、副題が名乗る地名・機種**を並べて出す（**自動で判定しない**）

■ ⚠️ わざと judge しないもの（誤報を作らないため）
    `NNNN年ごろ` は **撮影年の主張ではない**ことがある。`c803` は写真が2013年でも
    副題は「1978年ごろの**機種**」で、⑤c の台帳が「正しい書き方の見本」と書いている。
    → `ごろ` は ⚠️ の一覧に出すだけ。**目で決める。**

■ 使い方
    python tools/check_credits.py            # 突き合わせ
    python tools/check_credits.py --full     # ⚠️ の一覧も全部出す
    python tools/check_credits.py --selftest # 物差しの検算（陽性対照つき）
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
sys.stdout.reconfigure(encoding="utf-8")

CREDITS = HERE / "ref" / "CREDITS.md"
# 🔴 **題材ごとに書き換える定数**（→ [[feedback-per-episode-constants-go-stale]]）。
#    いまは7本目（9.11）のまま。8本目（コロンビア号）へ移すときは
#    `EP_PREFIX` と `HEADER` と `CLAIM_DAY` の3つを一緒に替える。
#    ⚠️ 1つでも替え忘れると「0件を合格」にする。下の `EP_PREFIX` の使い所で止めてある。
#    🔴🔴 2026-09-15（8本目 ⑤b-2）：**8本目へ切り替えた。**7本目の値は
#       `EP_PREFIX="ep7/"` ／ 見出しの最後の列が「元の題名」／
#       `CLAIM_DAY=re.compile(r"2001年9月(\d{1,2})日")`。
#    ⚠️ **見出しを7本目と同じ文字列にしてはいけない。**`load_table()` は
#       `lines.index(HEADER)` で**最初に当たった行**から読むので、同じ文字列だと
#       8本目の表を足しても **`ref/CREDITS.md` の中の7本目の表を読み続ける**
#       （＝黙って前の回を測る）。8本目は最後の列を「NASA の識別子」にして分けた。
#    🔴🔴 2026-09-20（10本目 三豊百貨店 ⑤b-1）：**10本目へ切り替えた。**9本目の値は
#       `EP_PREFIX="ep9/"` ／ 見出しの最後の列が「Commons の題名」。
#       10本目は**権利の形が2つある**（CC BY-SA 4.0 と 公共ヌリ第1類型）ので、
#       最後の列を「**素材の題名**」にして 9本目（Commons の題名）と分けた。
#       ⚠️ `ref/CREDITS.md` に §三豊百貨店 の表を足すまで `load_table()` は**止まる**（正しい）。
#    🔴🔴 2026-09-21（11本目 チャレンジャー号 ⑤c-2）：**11本目へ切り替えた。**10本目の値は
#       `EP_PREFIX="ep10/"` ／ 見出しの最後の列が「素材の題名」。
#       11本目は**実名を出す回なので、動く映像3本ぶんの出典も画面に出す**
#       （記憶 `project-jiko-rules-index` §5）。写真は米連邦 §105 と Commons の PD。
#       最後の列を「**出どころ**」にして 10本目（素材の題名）と分けた。
EP_PREFIX = "ep11/"
HEADER = "| 欄 | 使うカット | 撮影年 | 権利 | 撮影者 | 出どころ |"
ROW = re.compile(r"^\|\s*`([a-z0-9_]+)`\s*\|([^|]*)\|([^|]*)\|([^|]*)\|([^|]*)\|(.*)\|\s*$")

# 副題が名乗る「年」。⚠️ ここに足すときは必ず陽性対照も足す
CLAIM_YEAR = re.compile(r"(1[89]\d\d|20\d\d)年撮影")
CLAIM_PRE = "2001年以前"
CLAIM_SOFT = re.compile(r"(1[89]\d\d|20\d\d)年ごろ")
# 🔴 8本目は事故が **2003年2月1日**。⚠️ この回の副題は「2003年1月16日」「2002年3月12日」
#    のように**月から書く**ので、日の主張は「NNNN年N月N日」で拾う。
CLAIM_DAY = re.compile(r"(1[89]\d\d|20\d\d)年\d{1,2}月\d{1,2}日")

# ④ 目で決めるために並べる語。原題の側にこれが出たら副題と並べて出す
PLACE = re.compile(
    r"\b(Kadena|Ramstein|Geilenkirchen|Lithuania|Siauliai|Kunsan|Incirlik|Lakenheath|"
    r"Geneva|Melbourne|Lahore|Domodedovo|Mogadishu|Taoyuan|Helsinki|Manchester|"
    r"Boston|Logan|Dulles|Newark|Atlanta|Chicago|ORD|DCA|Prince Sultan|Shanksville|"
    r"Pentagon|New York|Washington|Houston|"
    # 🔴 2026-09-16（9本目）：テネリフェの回の素材に出る地名。
    #    ⚠️ 「いまの空港」を1977年の空港と名乗らせないために、原題の地名を副題と並べる
    r"Tenerife|Los Rodeos|Gran Canaria|Las Palmas|Schiphol|Amsterdam|Sydney|"
    r"San Francisco|Los Angeles|JFK|Kennedy|Frankfurt|Seattle|Everett|Honolulu)\b", re.I)
MODEL = re.compile(
    r"\b(7[0-9]{2}-?[0-9]{0,3}(?:ER|F|MAX)?|A2?[0-9]{2,3}(?:-[0-9]{3})?|"
    r"F-1[56][A-Z]*|C-40|CS100|E190|MD-?[0-9]{2})\b")


def load_table():
    """§8 の表を読む。**読めなければ止める**（0件を合格にしない）。"""
    if not CREDITS.exists():
        raise SystemExit(f"🔴 {CREDITS} が無い（fail closed）")
    # 🔴 `ref/CREDITS.md` には1〜7本目の表が全部入っている。
    #    **見出しの行から始めて、表が切れるところで止める**（他の回の表を読まない）。
    #    2026-09-14 に、これを付けずに全文へ正規表現を当てたら、
    #    5本目の「24分55秒（1,494.71秒）」を撮影年として `int()` に渡して落ちた。
    lines = CREDITS.read_text(encoding="utf-8").split("\n")
    try:
        h = lines.index(HEADER)
    except ValueError:
        raise SystemExit(f"🔴 §8 の表の見出しが無い（fail closed）：{HEADER}")
    body = []
    for ln in lines[h + 1:]:
        if not ln.startswith("|"):
            break
        body.append(ln)
    rows = {}
    for ln in body:
        m = ROW.match(ln)
        if not m:
            continue
        slot, cuts, year, lic, who, title = (x.strip() for x in m.groups())
        # ⚠️ `slot` が同じ行が2つあったら、あとの回の表を拾っている＝止める
        if slot in rows:
            raise SystemExit(f"🔴 `{slot}` の行が2つある（表が二重になっている）")
        rows[slot] = dict(cuts=cuts.split(), year=(None if year in ("不明", "") else int(year)),
                          lic=lic, who=who, title=title)
    if not rows:
        raise SystemExit("🔴 §8 の表が1行も読めなかった（fail closed）")
    return rows


def judge(sub, row):
    """その副題が表と食い違っているか。(🔴の理由, ⚠️の理由) を返す。"""
    hard, soft = [], []
    y = row["year"]
    m = CLAIM_YEAR.search(sub)
    if m:
        if y is None:
            hard.append(f"副題が「{m.group(0)}」と名乗るのに、表の撮影年が**不明**")
        elif int(m.group(1)) != y:
            hard.append(f"副題「{m.group(0)}」に対し、表の撮影年は **{y}**")
    if CLAIM_PRE in sub:
        if y is None:
            hard.append("副題が「2001年以前」と名乗るのに、表の撮影年が**不明**")
        elif y > 2001:
            hard.append(f"副題「2001年以前」に対し、表の撮影年は **{y}**")
    d = CLAIM_DAY.search(sub)
    if d:
        # 🔴 2026-09-15（8本目）：ここは **2001 と直に比べていた**（7本目専用）。
        #    8本目は 2002年・2003年・1988年の写真が混じるので、
        #    **副題が名乗った年そのもの**と突き合わせる。
        if y is None:
            hard.append(f"副題が「{d.group(0)}」と名乗るのに、表の撮影年が**不明**")
        elif y != int(d.group(1)):
            hard.append(f"副題「{d.group(0)}」に対し、表の撮影年は **{y}**")
    s = CLAIM_SOFT.search(sub)
    if s and y is not None and abs(int(s.group(1)) - y) > 3:
        soft.append(f"副題「{s.group(0)}」と表の撮影年 {y} が {abs(int(s.group(1)) - y)}年 離れている"
                    f"（⚠️ 機種や場面の年を言っていることがある。目で決める）")
    if row["lic"].startswith("CC BY") and not row["who"]:
        hard.append("CC BY なのに撮影者が空（撮影者名は使用条件そのもの）")
    return hard, soft


def words(title, sub):
    """原題に出る地名・機種のうち、副題に出てこないもの。**判定はしない。**"""
    got = {w for w in PLACE.findall(title)} | {w for w in MODEL.findall(title)}
    return sorted(w for w in got if w.lower() not in sub.lower())


def run(full=False):
    import cuts                                                 # noqa: PLC0415
    rows = load_table()
    hits, softs, seen = [], [], 0
    for cid in sorted(cuts.SPEC):
        spec = cuts.SPEC[cid]
        photo = spec.get("photo") or ""
        # 🔴🔴 2026-09-14（8本目 ⑤b-1）**この門番は題材を名指しで見ている。**
        #    `ep7/` しか見ないので、8本目の `ep8/` 74点には**1件も鳴らず、
        #    しかも「✓ 全部合っている」と出る**（黙って間違った合格）。
        #    → [[feedback-gates-blind-to-the-new-material]]／
        #      [[feedback-per-episode-constants-go-stale]]
        #    ⚠️ 直しきる（`ref/CREDITS.md` に §コロンビア号 の表を足して `EP_PREFIX` と
        #      `HEADER` と `CLAIM_DAY` を切り替える）のは⑤b-2 だが、
        #      それまで**黙って通す状態にはしない**ので、ここで止める。
        if photo and "/fb_" not in photo and not photo.startswith(EP_PREFIX):
            raise SystemExit(
                f"🔴 {cid}: 写真 `{photo}` は、この門番が見ている題材"
                f"（`{EP_PREFIX}`）と違う。**この門番はいま何も測っていない**。\n"
                f"   直し方＝`ref/CREDITS.md` にその回の表を足し、`HEADER` と\n"
                f"   `EP_PREFIX` と `CLAIM_DAY` を差し替える（fail closed）")
        if not photo.startswith(EP_PREFIX) or "/fb_" in photo:
            continue                      # 実写のひかえは動画の出典を借りる＝別の門番
        seen += 1
        slot = Path(photo).stem
        row = rows.get(slot)
        if row is None:
            hits.append((cid, slot, f"`{slot}` が §8 の表に無い（fail closed）"))
            continue
        sub = str(spec.get("s") or "")
        hard, soft = judge(sub, row)
        for h in hard:
            hits.append((cid, slot, h))
        for s in soft:
            softs.append((cid, slot, s))
        w = words(row["title"], sub)
        if w:
            softs.append((cid, slot, f"原題にあって副題に無い語：{' '.join(w)}"
                                     f"／副題「{sub}」"))
    print(f"■ 写真を出すカット {seen} 欄を、`ref/CREDITS.md` §8 の表 {len(rows)} 行と突き合わせた")
    # 🔴 2026-09-16（9本目 ⑤b-1）**0欄でも「✓ 年の主張はどの欄も合っている」を出していた。**
    #    章ファイルがまだ無い（あるいは読めていない）ときに、この門番だけが緑だった
    #    （[[feedback-parsers-fail-closed]]＝0件を合格にしない）。
    if seen == 0:
        print("🔴 写真を出すカットが0欄＝**章ファイルを読めていない**か、この回の写真を1枚も当てていない"
              "（合格にしない・exit 2）")
        return 2
    for cid, slot, why in hits:
        print(f"  🔴 {cid}（{slot}）{why}")
    if full or not hits:
        for cid, slot, why in softs:
            print(f"  ・ {cid}（{slot}）{why}")
    if hits:
        print(f"🔴 副題の主張と出どころが食い違う欄が {len(hits)} 件（exit 1）")
        return 1
    print(f"✓ 年の主張はどの欄も表と合っている（目で決める ⚠️ は {len(softs)} 件"
          f"{'・--full で出る' if not full else ''}）")
    return 0


def selftest():
    ok = True

    def chk(what, cond):
        nonlocal ok
        print(("  ✓ " if cond else "  🔴 ") + what)
        ok = ok and bool(cond)

    rows = load_table()
    chk(f"表が読めている（{len(rows)}行）", len(rows) >= 60)
    # ── 陽性対照＝**値**で見る（[[feedback-verify-your-own-instrument]]）
    r24 = dict(year=2024, lic="PD（Public domain）", who="X", title="")
    r99 = dict(year=1999, lic="PD（Public domain）", who="X", title="")
    chk("陽性対照①：『2001年以前』×表2024 → 鳴る",
        len(judge("空港の搭乗口　2001年以前", r24)[0]) == 1)
    chk("陽性対照②：『2001年以前』×表1999 → 鳴らない",
        judge("空港の搭乗口　2001年以前", r99)[0] == [])
    chk("陽性対照③：『2023年撮影』×表2024 → 鳴る",
        len(judge("空港の搭乗口　2023年撮影", r24)[0]) == 1)
    chk("陽性対照④：『2024年撮影』×表2024 → 鳴らない",
        judge("空港の搭乗口　2024年撮影", r24)[0] == [])
    chk("陽性対照⑤：『2001年9月11日』×表2024 → 鳴る",
        len(judge("降ろされた旅客機　2001年9月11日", r24)[0]) == 1)
    chk("陽性対照⑥：撮影年が不明なのに年を名乗る → 鳴る",
        len(judge("空港の搭乗口　2024年撮影", dict(r24, year=None))[0]) == 1)
    chk("陽性対照⑦：年を名乗らない副題は、撮影年が不明でも鳴らない",
        judge("航空路管制センターの卓　連邦航空局の写真", dict(r24, year=None))[0] == [])
    chk("陽性対照⑧：CC BY で撮影者が空 → 鳴る",
        len(judge("旅客機の客室", dict(r24, lic="CC BY（CC BY 2.0）", who=""))[0]) == 1)
    chk("陽性対照⑨：『1978年ごろ』は 🔴 にせず ⚠️ に出す（c803 の型）",
        judge("飛行記録装置　1978年ごろの機種", dict(r24, year=2013))[0] == []
        and len(judge("飛行記録装置　1978年ごろの機種", dict(r24, year=2013))[1]) == 1)
    chk("陽性対照⑩：原題の地名が副題に無ければ拾う（Kadena）",
        "Kadena" in words("F-15C Eagle ... at Kadena Air Base, Japan", "待機中のF-15　2024年撮影"))
    chk("陽性対照⑪：副題に出ている地名は拾わない",
        words("Departure Board at ORD", "空港の出発案内板 ORD　2017年撮影") == [])
    print(f"\n{'✓ 物差しは通った' if ok else '🔴 物差しが壊れている'}")
    return 0 if ok else 2


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--full", action="store_true")
    p.add_argument("--selftest", action="store_true")
    a = p.parse_args()
    return selftest() if a.selftest else run(a.full)


if __name__ == "__main__":
    sys.exit(main())
