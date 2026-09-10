# -*- coding: utf-8 -*-
"""**変わるはずのカット**を、手で数えずに機械で出す。

やり方 ＝ 旧コミットの `tools/` を丸ごと別の場所へ取り出し、そこで `build_layers()` を回して
SVG を作り、いまの `tools/` の SVG と文字列で比べる。⚠️ 式を写さない・型から数えない。

  python qa_out/kb_u_predict.py <旧コミット>

⚠️ 出るのは **SVG の差**。焼いた絵の差ではない（実写のコマは入らないし、
   `footage.have()` はローカルでは偽になる＝出典行が別の枝に落ちる。§T-11-1）。
   ＝ **ここで「変わる」と出たカットは、焼いても変わる**（下限の見積もり）。
"""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent.parent
OLD = sys.argv[1] if len(sys.argv) > 1 else "HEAD~2"


def layers_of(tools_dir):
    """その `tools/` で `build_layers()` を回し、{cid: 連結した SVG} を返す。"""
    code = (
        "import sys, json\n"
        "sys.path.insert(0, r'%s')\n"
        "import scene_jiko as S\n"
        "jobs = S.build_layers()[0]\n"
        "out = {}\n"
        "for k, v in jobs.items():\n"
        "    cid = k.split('_')[0]\n"
        "    out.setdefault(cid, []).append(k + '=' + str(v))\n"
        "print(json.dumps({c: ''.join(sorted(v)) for c, v in out.items()}))\n"
    ) % tools_dir
    # ⚠️ Windows の子プロセスは既定が CP932。UTF-8 を強制し、読めない字は落とさず置き換える
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    r = subprocess.run([sys.executable, "-c", code], capture_output=True,
                       text=True, encoding="utf-8", errors="replace",
                       cwd=tools_dir, env=env)
    if r.returncode != 0:
        raise SystemExit(f"🔴 {tools_dir} で回らなかった:\n{r.stderr[-1500:]}")
    import json
    return json.loads(r.stdout.splitlines()[-1])


new = layers_of(str(HERE / "tools"))

with tempfile.TemporaryDirectory() as td:
    # 旧コミットの tools/ を、リポジトリと同じ形（親に ref/ と audio/ がある）で置く
    root = Path(td) / "repo"
    root.mkdir()
    subprocess.run(["git", "archive", OLD, "tools"], cwd=HERE, check=True,
                   stdout=open(root / "t.tar", "wb"))
    subprocess.run(["tar", "-xf", "t.tar"], cwd=root, check=True)
    (root / "t.tar").unlink()
    # ⚠️ `tools/` だけ差し替え、**それ以外の全部**は本物へ張る。
    #    最初は ref/audio/out/analytics だけ張って `fontmetrics` が
    #    「フォントの実測ができません」で fail closed した（＝正しい止まり方）。
    for src in HERE.iterdir():
        if src.name in ("tools", ".git"):
            continue
        os.symlink(src, root / src.name, target_is_directory=src.is_dir())
    old = layers_of(str(root / "tools"))

cids = sorted(set(old) | set(new))
diff = [c for c in cids if old.get(c) != new.get(c)]
print(f"旧 {OLD} と いま を突き合わせた（SVG の文字列）")
print(f"  カット {len(cids)}／**変わる {len(diff)}**／変わらない {len(cids) - len(diff)}")
print("\n変わるカット")
for i in range(0, len(diff), 12):
    print("  " + " ".join(diff[i:i + 12]))
