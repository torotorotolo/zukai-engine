# -*- coding: utf-8 -*-
"""④'の所見の台帳を、照合の返り値（check_result.json）と直す係の記録（changes_G*.md）から組む（読むだけ）。
    python ref/ep14/v2_build/ledger.py > ref/ep14/v2_build/ledger.md
扱い＝changes_G*.md の「不採用」の節に id があれば「不採用」、decisions.md の「直さない」に id があれば「直さない」、
      それ以外は「直した」。🔴 扱いの列は人が決めた結果を写すだけ＝数え直しは ledger の最後の行で
"""
import json, re, sys, collections
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
S = Path(__file__).resolve().parent
res = json.load(open(S / "check_result.json", encoding="utf-8"))

rej = {}
for f in sorted(S.glob("changes_G*.md")):
    on = None
    for ln in f.read_text(encoding="utf-8").splitlines():
        if re.match(r"^#+\s", ln) or re.match(r"^\*\*.*\*\*\s*$", ln):
            on = "不採用" if "不採用" in ln else ("一部" if "一部" in ln else None)
            continue
        if on:
            # 🔴 行の頭の番号だけを拾う（行の中で触れた別の所見の番号を拾わない）
            m = re.match(r"^[-*\s|]*(G\d-\d{2})", ln)
            if not m:
                continue
            txt = re.sub(r"^[-*\s|]+", "", ln).strip()
            part = on == "一部" or re.search(r"のうち|の部分|一部", txt[:40])
            rej.setdefault(m.group(1), ("一部だけ採った" if part else "不採用") + "：" + txt[:90])
# ④'（G0）が自分で直したもの・係の記録に書かれない決め
OVR = {"G1-01": "直した（④'＝`c105`「傾いたきっかけ」・`cc16` は G6）", "G1-03": "直した（④'＝`c102` のかぎ括弧を外した）",
       "G7-29": "直した（★は残し `c715` の頭に聞き役の質問＝乗客を責めて聞こえない形）",
       "G6-16": "直した（④'＝`cb15`「123艇の詳しい報告から10分あまりで、船に入れなくなるとは」。途中で「第一報」と縮めて起点がずれた＝照合し直し R2 の🔴で戻した）"}
rej.update({k: v for k, v in OVR.items()})
keep = {}
dec = (S / "decisions.md").read_text(encoding="utf-8")
for ln in dec.splitlines():
    if "直さない" in ln or "⑤bで原寸" in ln or "確かめるのは⑤b" in ln:
        for i in re.findall(r"G\d-\d{2}", ln):
            keep.setdefault(i, "直さない" if "直さない" in ln else "⑤bで原寸")
print("| id | カット | 深刻さ | 面 | 型 | 所見（要約） | 扱い |")
print("|---|---|---|---|---|---|---|")
cnt = collections.Counter(); sev = collections.Counter()
for g in res:
    for x in g["findings"]:
        i = x["id"]
        how = rej[i] if i in rej else keep.get(i, "直した")
        cnt[re.split(r"[（：]", how)[0]] += 1; sev[x["severity"]] += 1
        short = x["short"].replace("|", "／")
        print(f"| {i} | {x['cut']} | {x['severity']} | {x['face']} | {x['kind']} | {short} | {how.replace('|', '／')} |")
print()
print(f"計 {sum(sev.values())}件（" + "・".join(f"{k}{v}" for k, v in sev.items()) + "）／扱い：" + "・".join(f"{k} {v}" for k, v in cnt.items()))

if "--review" in sys.argv:
    # 第2版の直しを別の目2本（R1＝第1〜9章・R2＝第10〜13章）が当て直した指摘。扱いは patch_review.py に当てたかどうか
    rv = json.load(open(S / "review_result.json", encoding="utf-8"))
    NOT = {("c909", "形"): "不採用：聞き役の「？」で終わらない一言は句点で終える（門番の様式＝途中の行は句点か読点）"}
    print("\n| 係 | カット | 深刻さ | 指摘（要約） | 扱い |")
    print("|---|---|---|---|---|")
    n = collections.Counter()
    for h in rv:
        for x in h["issues"]:
            w = re.sub(r"\s+", " ", x["what"]).replace("|", "／")
            how = next((v for (c, k), v in NOT.items() if c == x["cut"] and k in w[:6]), "直した（`patch_review.py`）")
            n[how.split("（")[0].split("：")[0]] += 1
            print(f"| {h['half'][:2]} | {x['cut']} | {x['severity']} | {w[:110]} | {how} |")
    print(f"\n照合し直し {sum(n.values())}件：" + "・".join(f"{k} {v}" for k, v in n.items()))

if "--items" in sys.argv:
    # §1-8（足した事実）・§2（kousei との違い）・決め所の当て直し＝照合の係が1件1行で返した判定
    print("\n| 係 | カット | 項目 | 判定 |")
    print("|---|---|---|---|")
    n = collections.Counter()
    for g in res:
        for it in g.get("items", []):
            v = it["verdict"].replace("|", "／")
            n["OK" if v.startswith("OK") else "ずれ・頁"] += 1
            print(f"| {g['group']} | {it['cut']} | {it['item'].replace('|', '／')[:70]} | {v[:140]} |")
    print(f"\n項目 {sum(n.values())}件：" + "・".join(f"{k} {v}" for k, v in n.items()))
