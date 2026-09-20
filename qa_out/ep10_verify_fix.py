# -*- coding: utf-8 -*-
r"""ep10_verify_fix.py — 辞書を入れて焼き直したあと、**狙った音が本当に出たか**を行ごとに検算する。

  python qa_out/ep10_verify_fix.py

やること:
  ① EL_YOMI が当たる 97行について、**焼き直し後の聞取**に「出てほしい字」が在るかを見る
  ② 直す前（p1・p2）と並べて、**直った／変わらない／悪くなった**を機械で分ける
  ③ 数の照合（el_ledger.numbers_missing）を焼き直し後の聞取でやり直す

🔴 なぜ要るか: A/B は**その1行にそのキーだけ**を当てた音で見ている。本番は**複数のキーが同じ行に重なる**
   （例 c306-1 は「ときは7万1,136」と「床」の2つが当たる）。A/B が通っても本番で崩れうるので、
   **出荷する音の聞取でもう一度当てる**（feedback-local-render-path-differs-from-the-baked-one と同じ筋）。
⚠️ 門番ではない。字が違っても読みが同じなら正解のことがある（ソチョク・春高・胸）ので、最後は人が読む。
"""
import csv
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import el_script as ES            # noqa: E402
from el_ledger import numbers_missing  # noqa: E402

# キー → 焼き直し後の聞取に「在ってほしい字」。⚠️ 字が変わるのが正解のものは別表へ
WANT = {
    # ⚠️ 棟は Scribe が「胸」「宗」と書くことがある。**音は むね なので正解**（字では決まらない型）
    "北の棟": ("棟", "胸", "宗", "むね", "ムネ"), "の棟": ("棟", "胸", "宗"), "棟は2つ": ("棟", "胸", "宗"), "北がA棟": "北",
    "瓦礫": "瓦礫", "報道": "報道", "裁判を": "裁判", "手作業": "手作業",
    "建物の異変": "建物", "数が動いた": "数", "残った一つ": "残った",
    "押え": "押さ", "止める力": "止める", "育った": "育った", "建ったあと": ("たっ", "建った", "立った"),
    "頁によって": "ページ", "白書には、図面": "白書", "白書は17時": "白書", "白書によれば": "白書",
    "国会の報告書は、完全": "国会", "な店だったのか": "だった", "行方不明者の": "行方不明者",
}
# 字が変わるのが正解のもの（読みは合っている）。値＝在ってよい字のどれか1つ
OK_OTHER = {
    # 🔴 送っているのは かな なので、Scribe がどの字を当てるかは決まらない。**音が同じ字なら合格**。
    #    例 c413-3「ゆかのひび」→『由香の日々』＝音は正しい（一致率は下がるが読みは合っている）。
    "床": ("床", "ゆか", "ユカ", "由香", "由佳", "湯加"),   # ⚠️ 人名の字が当たることがある。どれも ゆか の音／直す前は「トカ・渡河・戸・束」だった
    "三豊": ("三分", "三豊", "サンプン"),
    "竣工": ("春高", "竣工", "しゅんこう", "シュンコウ"),
    "瑞草区": ("ソチョ", "瑞草"),
    "数は、この": ("カズ", "数"),
}
NUM_KEYS = {"240キログラム", "377時間", "全国で2番目", "被害者は1,439人", "ときは7万1,136",
            "女性が396人", "その30分前"}


def heard(path):
    rows = [r for r in csv.reader(open(path, encoding="utf-8"), delimiter="\t")][1:]
    return {r[0]: r[3] for r in rows}


def main():
    now = heard(ROOT / "audio/el_qa/ep10_el_yomi.tsv")
    p1 = heard(ROOT / "audio/el_qa/ep10_el_yomi_p1.tsv")
    ls = {l.lid: l for l in ES.lines()}

    ng, changed = [], 0
    for lid, l in ls.items():
        hits = []
        ES.el_text(l.text, hits)
        if not hits:
            continue
        changed += 1
        h = now.get(lid)
        if h is None:
            ng.append((lid, "起こし直していない", "", ""))
            continue
        for k in {a for a, _, _ in hits}:
            if k in NUM_KEYS:
                miss = numbers_missing(l.text, h)
                if miss:
                    ng.append((lid, f"数が無い:{miss}", l.text, h))
            elif k in OK_OTHER:
                if not any(w in h for w in OK_OTHER[k]):
                    ng.append((lid, f"「{k}」の音が出ていない", l.text, h))
            elif k in WANT:
                want = WANT[k]
                want = (want,) if isinstance(want, str) else want
                if not any(w in h for w in want):
                    ng.append((lid, f"「{k}」→聞取に {'/'.join(want)} が無い", l.text, h))
            else:
                ng.append((lid, f"🔴 WANT に「{k}」の期待値が無い（fail closed）", l.text, h))

    print(f"辞書が当たる行 {changed}／期待どおりでない {len(ng)}")
    for lid, why, s, h in ng:
        print(f"\n🔴 {lid}  {why}")
        if s:
            print(f"   台本  : {s}")
            print(f"   直す前: {p1.get(lid, '—')}")
            print(f"   直した後: {h}")
    if not ng:
        print(f"✅ {changed}行すべてで狙った音が出ています")
    return 1 if ng else 0


if __name__ == "__main__":
    sys.exit(main())
