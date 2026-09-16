# -*- coding: utf-8 -*-
r"""ep9_yougo.py — 概要欄に載せる用語の候補を、本文（narration.SCRIPT＝台本第2版と1字も違わない）へ機械で当てる（⑤a・2026-09-16）。

  python qa_out/ep9_yougo.py

🔴 なぜ要るか（記憶 feedback-jiko-description-glossary の「下書きが必ず外す3つの型」）:
   1. 本文に1行も出ない語を用語として並べてしまう（9.11 では EDT など4語が0行だった）
   2. 本文が言い換えた語に追いつけていない
   3. 下書きから語が漏れる
   この回は台本に §11（用語の下書き）が無い。1通目の候補9語＋載せ漏れの候補を、本文に当てて決める。
⚠️ 台本は narration.SCRIPT から読む（qa_out/ep9_script_copy.py --check で md と1字も違わないことを確かめてある）。
   台本を読む目を増やさない＝el_script.lines() を通す。
"""
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

# 1通目（④'の申し送り）の候補9語。本文を探すときの見出し語
FIRST = ["バックタクシー", "ATCの許可", "復唱", "視程", "露点", "RVR", "中心線灯", "V1", "固着"]
# 載せ漏れの候補（本文に出たら、初出カットの全文を見て入れるか決める）
EXTRA = ["滑走路視距離", "管制塔", "管制官", "誘導路", "待機", "無線標識", "フライトレベル", "旋回", "方位",
         "登録記号", "航空機関士", "副操縦士", "資格", "勤務時間", "電報", "迂回", "混信", "QAM",
         "地面についた雲", "雲の底", "教官", "訓練", "操縦室の録音", "書き起こし", "クリッパー", "パパ",
         "離陸の許可", "甲高い", "出力", "第1エンジン", "給油", "ATC", "許可", "了解", "待て",
         "三番目", "C-1", "C-3", "C-4", "駐機場", "エプロン", "バックトラック", "180度", "向きを変え",
         "視距離", "霧", "雲", "滑走路灯", "灯火", "運航規程", "法律", "審査", "検定", "機長の資格",
         "トレーニング", "シミュレーター", "パンナム", "KLM", "ボーイング747", "747"]


def main():
    import el_script as ES
    ls = ES.lines()
    by_cut = {}
    for l in ls:
        by_cut.setdefault(l.cid, []).append(l.text)
    order = list(dict.fromkeys(l.cid for l in ls))

    def hits(k):
        return [l for l in ls if k in l.text]

    for title, terms in (("1通目の候補9語", FIRST), ("載せ漏れの候補", EXTRA)):
        print(f"\n===== {title} =====")
        for k in terms:
            h = hits(k)
            if not h:
                print(f"🔴 {k}: 本文に0行")
                continue
            first = h[0].cid
            cuts = sorted({x.cid for x in h}, key=order.index)
            print(f"・{k}: {len(h)}行／{len(cuts)}カット／初出 {first}（ほか {','.join(cuts[1:6])}{'…' if len(cuts) > 6 else ''}）")
            if title.startswith("1通目") or len(h) <= 3:
                print("    " + "／".join(by_cut[first]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
