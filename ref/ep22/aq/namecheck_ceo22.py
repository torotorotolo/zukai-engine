# -*- coding: utf-8 -*-
"""22本目 ⑤a-1（2026-10-14）：名前の網を「CEO の名前の語」と「ほかの名前」に分けて数える。

  python ref/ep22/aq/namecheck_ceo22.py <ファイル> [<ファイル> …]

なぜ：c207 の CEO の名前は、カズヤくんの決め（10-14「リポに名前を入れる」）で SCRIPT（tools/narration.py）・置き換えの表
（tools/el_script.py の MD_SUBS）・読み一覧（ref/ep22/aq/yomi_sheet.tsv）・⑤a-2 からの narration.json にだけ入れてよい。
元の網 `ref/ep22/v2_build/namecheck22.py` は名前を1つも許さない＝この4ファイルで必ず鳴る＝「鳴っているのは CEO の語だけか」を
見分けられない。ここでは、一覧（git の外の ref/ep22/src/names_private.txt）のうち CEO の名前（MD_SUBS の値）に当たる語と、
ほかの語を分けて、ファイルごとに数だけ出す（語そのものは出さない＝この出力をリポに写しても名前が漏れない）。
  ・ほかの名前が1件でもあれば exit 1（どのファイルでも）
  ・CEO の語は、ALLOW の4ファイルのほかに当たれば exit 1
  ・一覧が読めなければ exit 2（fail closed）
作業ツリーには src/ が無い＝一覧は本線のフォルダ（C:/Users/konar/Desktop/zukai-engine/ref/ep22/src/）から読む。
"""
import ast
import importlib.util
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))     # ref/ep22/aq → リポの根
MAIN = "C:/Users/konar/Desktop/zukai-engine"
ALLOW = {"tools/narration.py", "tools/el_script.py", "ref/ep22/aq/yomi_sheet.tsv", "audio/narration.json"}


def ceo_name():
    """tools/el_script.py の MD_SUBS["ep22"] の値（import せずにファイルの字から読む）。"""
    tree = ast.parse(open(os.path.join(ROOT, "tools", "el_script.py"), encoding="utf-8").read())
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", None) == "MD_SUBS" for t in node.targets):
            return "".join(ast.literal_eval(node.value).get("ep22", {}).values())
    return ""


def load_namecheck():
    """元の網 namecheck22.py を読む（一覧の場所は作業ツリーに無ければ本線のフォルダ）。"""
    for base in (ROOT, MAIN):
        nc_path = os.path.join(base, "ref", "ep22", "v2_build", "namecheck22.py")
        lst = os.path.join(base, "ref", "ep22", "src", "names_private.txt")
        if os.path.exists(nc_path) and os.path.exists(lst):
            spec = importlib.util.spec_from_file_location("namecheck22", nc_path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            mod.LIST = lst
            return mod
    return None


def main(files):
    nc = load_namecheck()
    pats = nc.load() if nc else None
    ceo = ceo_name()
    if not pats or not ceo:
        print("🔴 名前の一覧か CEO の名前（MD_SUBS）が読めない＝測れていない")
        return 2
    ceo_words = [w for w, rx in pats if rx.search(ceo)]
    others = [(w, rx) for w, rx in pats if w not in ceo_words]
    print(f"一覧 {len(pats)}語＝CEO の名前に当たる語 {len(ceo_words)}・ほか {len(others)}")
    bad = 0
    for f in files:
        rel = os.path.relpath(os.path.abspath(f), ROOT).replace("\\", "/")
        lines = open(f, encoding="utf-8", errors="replace").read().splitlines()
        hit_o = [(i, w) for i, ln in enumerate(lines, 1) for w, rx in others if rx.search(ln)]
        hit_c = [i for i, ln in enumerate(lines, 1) if any(rx.search(ln) for w, rx in pats if w in ceo_words)]
        ng_c = hit_c and rel not in ALLOW
        bad += bool(hit_o) + bool(ng_c)
        mark = "✗" if (hit_o or ng_c) else "✓"
        extra = "".join(f" {i}:{w[0]}○" for i, w in hit_o)
        print(f"{mark} {rel}: CEO の名前の行 {len(hit_c)}{'（許していないファイル）' if ng_c else ''}／ほかの名前 {len(hit_o)}{extra}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
