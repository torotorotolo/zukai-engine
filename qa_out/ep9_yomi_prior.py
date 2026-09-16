# -*- coding: utf-8 -*-
"""9本目 テネリフェ ⑤a：前の回（7本目・8本目）の EL_YOMI を「候補の出どころ」として、この回の495行に当てる（2026-09-16）。

  python qa_out/ep9_yomi_prior.py --reset   … el_script.py の EL_YOMI（8本目）を空にする（前の辞書は json に控える）
  python qa_out/ep9_yomi_prior.py           … 7本目・8本目のキーが、この回のどの行に当たるかを数える（API 不使用）

🔴 **そのまま引き継がない。**同じ Koichi でも、当たる行が変われば結果が変わる
   （7本目の実測＝「ラングレー機の」は直り「ラングレー機が」は同じカナ化で 1.000 → 0.816 に壊れた）。
   ここで出るのは A/B（el_ab_yomi）にかける**候補**だけ。
⚠️ 当たりの判定は本番と同じ関数（el_script.yomi_pattern＝境界規則つき）を通す。自前の正規表現を持たない。
出力: audio/el_qa/ep9_yomi_prior.tsv（key / val / 出どころ / 当たる行数 / 行ID / 前の回の根拠のコメント）
"""
import json
import re
import subprocess
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
EL = ROOT / "tools" / "el_script.py"
SRC = {"ep7": "27606de", "ep8": "9c9e9a1"}      # 7本目＝公開版の辞書／8本目＝⑥の試写直しまで入った辞書
ENTRY = re.compile(r'^\s*("(?:[^"\\]|\\.)*")\s*:\s*("(?:[^"\\]|\\.)*")\s*,\s*(?:#\s*(.*))?$')

NEW_HEAD = '''# ── EL_YOMI（9本目 テネリフェ）───────────────────────────────
# 🔴 **空から始める**（8本目と同じ作法）。台本第2版 §6 は「危険の候補」であって、読みの正解は入っていない。
#    1語ずつ鳴らして（el_ab_yomi）確かめた語だけを、根拠を1行添えて入れる（feedback-yomi-dict-must-be-verified）。
# 🔴 7本目（git 27606de）・8本目（git 9c9e9a1）の辞書は**候補の出どころ**として当てる
#    （`qa_out/ep9_yomi_prior.py`＝この回の495行にどのキーが当たるかを数える）。**そのまま引き継がない**。
#    8本目の辞書の控え＝`audio/el_qa/ep8_el_yomi_dict.json`
EL_YOMI = {
}
'''


def block(src: str, tag: str):
    """EL_YOMI の見出し行から EL_YOMI_OPEN_RIGHT の直前までを切り出す。"""
    a = src.index("# ── EL_YOMI（")
    b = src.index("EL_YOMI_OPEN_RIGHT = frozenset()", a)
    return a, b


def entries(src: str, tag: str):
    a, b = block(src, tag)
    body = src[a:b]
    out = []
    for line in body.split("\n"):
        m = ENTRY.match(line)
        if m:
            out.append((json.loads(m.group(1)), json.loads(m.group(2)), (m.group(3) or "").strip()))
    # 検算＝行ごとの正規表現で拾った数と、辞書リテラルを数えた数が一致すること（取りこぼし／二重取りを止める）
    import ast
    lit = body[body.index("EL_YOMI = {") + len("EL_YOMI = "):]
    d = ast.literal_eval(lit[:lit.rindex("}") + 1])
    if len(d) != len(out) or any(d.get(k) != v for k, v, _ in out):
        raise SystemExit(f"🔴 {tag}: 行ごとの抽出 {len(out)} 件 ／ 辞書リテラル {len(d)} 件が一致しない")
    return out


def reset():
    src = EL.read_text(encoding="utf-8")
    ents = entries(src, "HEAD")
    (ROOT / "audio" / "el_qa" / "ep8_el_yomi_dict.json").write_text(
        json.dumps([{"key": k, "val": v, "why": w} for k, v, w in ents], ensure_ascii=False, indent=1),
        encoding="utf-8")
    a, b = block(src, "HEAD")
    EL.write_text(src[:a] + NEW_HEAD + src[b:], encoding="utf-8")
    print(f"EL_YOMI を空にした（8本目 {len(ents)}件は audio/el_qa/ep8_el_yomi_dict.json に控えた）")


def prior():
    import el_script as ES
    if ES.EL_YOMI:
        raise SystemExit(f"🔴 EL_YOMI が空でない（{len(ES.EL_YOMI)}件）。先に --reset")
    ls = ES.lines()
    rows, seen = [], {}
    for tag, rev in SRC.items():
        src = subprocess.run(["git", "show", f"{rev}:tools/el_script.py"], cwd=ROOT,
                             capture_output=True, text=True, encoding="utf-8", check=True).stdout
        ents = entries(src, tag)
        print(f"{tag}（{rev}）: {len(ents)}件")
        for k, v, w in ents:
            pat = ES.yomi_pattern(k)
            hit = [l.lid for l in ls if pat.search(l.text)]
            key = (k, v)
            if key in seen:
                seen[key][2] += "+" + tag
                continue
            row = [k, v, tag, len(hit), ",".join(hit), w]
            seen[key] = row
            rows.append(row)
    out = ROOT / "audio" / "el_qa" / "ep9_yomi_prior.tsv"
    with out.open("w", encoding="utf-8") as f:
        f.write("key\tval\t出どころ\t当たる行数\t行ID\t前の回の根拠\n")
        for r in rows:
            f.write("\t".join(str(x) for x in r) + "\n")
    hitrows = [r for r in rows if r[3]]
    print(f"前の回のキー {len(rows)}件のうち、この回の行に当たる {len(hitrows)}件 → {out.relative_to(ROOT)}")
    for r in hitrows:
        print(f"  {r[0]} → {r[1]}（{r[2]}）×{r[3]}行: {r[4]}")
    return 0


if __name__ == "__main__":
    if "--reset" in sys.argv:
        reset()
        sys.exit(0)
    sys.exit(prior())
