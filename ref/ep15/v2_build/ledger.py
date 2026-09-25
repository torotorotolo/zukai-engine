# -*- coding: utf-8 -*-
"""④'の所見の台帳を、照合の返り値（check_result.json）と直す係の記録（changes_G*.md）から組む（読むだけ）。
    python ref/ep15/v2_build/ledger.py [--review] [--items]   （14本目 ref/ep14/v2_build/ledger.py を写した）
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
OVR = {}
if (S / "ledger_ovr.json").exists():   # ④'（G0）が自分で決めた扱い＝{"G1-01": "直した（…）"}
    OVR = json.load(open(S / "ledger_ovr.json", encoding="utf-8"))
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
    # 第2版の直しを別の目2本が当て直した指摘。扱いは patch_review.py に当てたかどうか（当てなかったものは review_not.json）
    rv = json.load(open(S / "review_result.json", encoding="utf-8"))
    NOT = {}
    if (S / "review_not.json").exists():   # [["c909", "形", "不採用：…"], …]
        NOT = {(c, k): v for c, k, v in json.load(open(S / "review_not.json", encoding="utf-8"))}
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
