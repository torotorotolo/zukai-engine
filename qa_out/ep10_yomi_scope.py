# -*- coding: utf-8 -*-
r"""ep10_yomi_scope.py — EL_YOMI に入れる候補が「どの行に当たるか」と「その行は崩れていたか」を並べる。

  python qa_out/ep10_yomi_scope.py

🔴 なぜ要るか（feedback-yomi-dict-must-be-verified）:
   短いキーの一括置換は、**登録した回では正しくても別の文脈で誤読を作る**。
   この回でも実際に出た＝「白書」→「はくしょ」を一括で当てたら、崩れていなかった `c405-2` が
   **『博士』に悪化**した（A/B 94.7% → 87.7%）。
   だから「当たる行」と「2周の聞取でその語が崩れていたか」を**並べて見てから**キーの長さを決める。

⚠️ これは門番ではなく当たり。**崩れていない行に当たるキーは、その行での害をA/Bで確かめるまで入れない。**
"""
import csv
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import el_script as ES  # noqa: E402

# (キー, 値, 「聞取に在るべき字」) … 3つめは崩れ判定に使う語。None ならキーの先頭語
CAND = [
    ("床", "ゆか", "床"),
    ("北の棟", "きたのむね", "棟"),
    ("の棟", "のむね", "棟"),
    ("棟は2つ", "むねは2つ", "棟"),
    ("北がA棟", "きたがA棟", "北"),
    ("瓦礫", "がれき", "瓦礫"),
    ("竣工", "しゅんこう", "竣工"),
    ("瑞草区", "ソチョく", "瑞草区"),
    ("報道", "ほうどう", "報道"),
    ("裁判を", "さいばんを", "裁判"),
    ("国会の報告書は、完全", "こっかいの報告書は、完全", "国会"),
    ("押え", "おさえ", "押え"),
    ("止める力", "とめる力", "止める"),
    ("な店だったのか", "な店 だったのか", "だった"),
    ("建物の異変", "たてものの異変", "建物"),
    ("行方不明者の", "行方不明者 の", "行方不明者"),
    ("頁によって", "ページによって", "頁"),
    ("白書には、図面", "はくしょには、図面", "白書"),
    ("白書は17時", "はくしょは17時", "白書"),
    ("白書によれば", "はくしょによれば", "白書"),
    ("手作業", "てさぎょう", "手作業"),
    ("育った", "そだった", "育っ"),
    ("残った一つ", "のこった一つ", "残っ"),
    ("数は、この", "かずは、この", "数"),
    ("数が動いた", "かずが動いた", "数"),
    ("建ったあと", "たったあと", "建っ"),
    ("240キログラム", "ニヒャクヨンジュッキログラム", "240"),
    ("377時間", "サンビャクナナジュウナナ時間", "377"),
    ("全国で2番目", "全国でニバンメ", "2番目"),
    ("被害者は1,439人", "被害者はセンヨンヒャクサンジュウキュウニン", "1,439"),
    ("ときは7万1,136", "ときはナナマンセンヒャクサンジュウロク", "1,136"),
]


def heard(path):
    rows = [r for r in csv.reader(open(path, encoding="utf-8"), delimiter="\t")][1:]
    return {r[0]: r[3] for r in rows}


def main():
    p1 = heard(ROOT / "audio/el_qa/ep10_el_yomi_p1.tsv")
    p2 = heard(ROOT / "audio/el_qa/ep10_el_yomi_p2.tsv")
    ls = list(ES.lines())
    risky = 0
    for key, val, probe in CAND:
        hit = [l for l in ls if key in ES.el_text(l.text)]
        ok_lines = []
        for l in hit:
            broke = (probe not in p1.get(l.lid, "")) or (probe not in p2.get(l.lid, ""))
            if not broke:
                ok_lines.append(l.lid)
        mark = "⚠️" if ok_lines else "  "
        if ok_lines:
            risky += 1
        print(f"{mark}「{key}」→「{val}」  当たる {len(hit)}行"
              f"{'（うち崩れていない: ' + ','.join(ok_lines) + '）' if ok_lines else '（全部が崩れていた）'}")
    print(f"\n当たる行に「崩れていない行」を含むキー: {risky}件"
          f"{'  → その行での害をA/Bで確かめること' if risky else ''}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
