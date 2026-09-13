# -*- coding: utf-8 -*-
"""ep7_word_tally.py — 語ごとに「台本に出た行数 ÷ 聞取にその字が出た行数」を数える（この回かぎり）。

■ なぜ要るか
    `el_reading_diff` は**行**を仕分ける道具なので、同じ語が何行で崩れているかが分からない。
    ⑤a で直すのは**語**なので、語ごとに「何行中何行で崩れたか」「文頭だけか行中もか」を出す。
    ＝ [[feedback-scale-one-visual-finding-to-a-full-count]]（1件の所見は式にして全数へ広げる）。

■ ⚠️ 物差しの注意
    - **これは「字が聞取に出たか」しか見ない。**字が出なくても読みは正しいことがある
      （Scribe の当て違い＝「責める→攻める」）。逆に字が出ても読みが違うことがある（床＝ゆか／とこ）。
      ＝ **当たり付け**であって門番ではない。決めるのは el_take2 / el_probe_words / el_ab_yomi。
    - 陽性対照＝**必ず出るはずの語**（「便」など台本に91行ある語）を混ぜて、0/N にならないことを見る。

  python qa_out/ep7_word_tally.py
"""
import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.stdout.reconfigure(encoding="utf-8", errors="replace")
import el_script as ES  # noqa: E402

# 見る語（el_reading_diff の79行から拾った。⚠️ 台本に出ない語を並べても当たりにならない）
WORDS = ["管制官", "管制", "防空司令部", "北棟", "南棟", "棟", "墜ち", "便名", "報せ", "知らせ",
         "想定", "軍", "客室", "五角形", "滑走路", "誘導路", "命令", "符号", "分単位", "猶予",
         "刃渡り", "首都", "側", "言葉", "跳ね返り", "応答符号", "トランスポンダ", "一次レーダー",
         "コマンドセンター", "運航管理", "駐機場", "ニューアーク", "ダレス", "オーティス",
         "ラングレー", "シャンクスビル", "スライニー", "共通戦略", "西南西", "原則", "当直",
         "手引き", "迎撃", "撃墜", "無線", "交信", "操縦室", "委員会報告", "航空路管制センター",
         "連邦航空局", "連邦航空保安官", "大統領警護隊", "音声記録装置", "緊急発進", "便"]

rows = list(csv.DictReader((ROOT / "audio" / "el_qa" / "ep7_el_yomi.tsv")
                           .read_text(encoding="utf-8").splitlines(), delimiter="\t"))
heard = {r["場面"]: r["聞こえた文"] for r in rows}
lines = {l.lid: l.text for l in ES.lines()}

print(f"{'語':<20}{'台本':>4}{'崩れ':>5}{'率':>6}  {'文頭':>4}{'頭崩れ':>6}   崩れた行")
print("─" * 100)
out = []
for w in WORDS:
    hit = [lid for lid, t in lines.items() if w in t]
    if not hit:
        out.append((0, 0, w, [], []))
        continue
    bad = [lid for lid in hit if lid in heard and w not in heard[lid]]
    head = [lid for lid in hit if lines[lid].startswith(w)]
    hbad = [lid for lid in head if lid in bad]
    out.append((len(bad), len(hit), w, bad, hbad))
for nbad, nhit, w, bad, hbad in sorted(out, key=lambda x: (-x[0], -x[1])):
    if not nhit:
        print(f"🔴 {w:<18}台本に0行（当たりにならないので外す）")
        continue
    mark = "🔴" if nbad and nbad / nhit >= 0.5 else ("⚠️" if nbad else "  ")
    print(f"{mark}{w:<18}{nhit:>4}{nbad:>5}{nbad/nhit*100:>5.0f}%  {len(hbad):>4}/{len([l for l in [x for x in bad]]) and '':>0}"
          f"{'':<2}{' '.join(bad[:8])}{' …' if len(bad) > 8 else ''}")
print("\n⚠️ 「崩れ」＝**その字が聞取に1つも無い行**。字が無くても読みは正しいことがある（Scribe の当て違い）。")
print("⚠️ 陽性対照＝「便」は台本 91行。ここが 0/91 なら物差しが壊れている。")
