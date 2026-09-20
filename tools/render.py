# -*- coding: utf-8 -*-
"""SVG → PNG。Chrome/Edge の headless を使う（追加インストール不要）。

ローカル(Windows)  … Microsoft Edge
クラウド(Ubuntu)   … google-chrome / chromium-browser
どちらも同じ Blink エンジンなので描画は一致する。
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

# 🔴🔴 2026-09-20（10本目⑥）：**Chrome を Edge より先にした。**
#    この日、手元の Edge は `--headless=new/old/（既定）` のどれでも
#    **終了コード 0・stderr 空のまま PNG を1枚も書かなくなっていた**（Chrome は同じ引数で通る）。
#    `png()` は最後に `out_path.exists()` を見て落ちるので黙って合格はしないが、
#    Edge が先だと**毎回1回空振りしてから気づく**ことになる。
#    ⚠️ Edge を使いたいときは `MK_BROWSER` で明示する（環境変数が最優先のまま）。
CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]


def browser() -> str:
    env = os.environ.get("MK_BROWSER")
    if env and Path(env).exists():
        return env
    for name in ("google-chrome", "google-chrome-stable", "chromium-browser", "chromium"):
        p = shutil.which(name)
        if p:
            return p
    for p in CANDIDATES:
        if Path(p).exists():
            return p
    sys.exit("Chrome/Edge が見つかりません。MK_BROWSER に実行ファイルのパスを設定してください。")


def png(html_text: str, out_path: str | Path, w: int = 1920, h: int = 1080) -> Path:
    out_path = Path(out_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory() as td:
        src = Path(td) / "page.html"
        src.write_text(html_text, encoding="utf-8")
        cmd = [
            browser(), "--headless=new", "--disable-gpu", "--no-sandbox",
            "--hide-scrollbars", "--force-device-scale-factor=1",
            "--default-background-color=00000000",
            # 🔴 2026-09-09（6本目キー橋 ⑤c'）：**プロファイルを1回ごとに分ける。**
            #    既定のプロファイルを使うと、`scene_jiko.render_all()` の並列4本が
            #    **プロファイルの錠を取り合って固まる**。実測（Windows / Edge）：
            #      1本ずつ    … 1.8 秒/枚
            #      並列4本    … **9.5分で2枚**（＝ほぼ進まない。落ちもしないので気づけない）
            #    さらに、固まった Edge が残ったまま次を回すと**全体が 20.9 秒/枚まで落ちる**
            #    （ゾンビ27個の状態で実測。門番の `check_layout` が MemoryError で
            #      「測れていない」と出たのも、このときのメモリ不足）。
            #    ⚠️ 描画そのものには影響しない（まっさらなプロファイルのほうが
            #      拡張機能や設定が混ざらないぶん、むしろ決定的になる）。
            f"--user-data-dir={Path(td) / 'profile'}",
            f"--window-size={w},{h}", f"--screenshot={out_path}",
            src.resolve().as_uri(),
        ]
        # Chrome の stderr は日本語が混ざる。cp932 で落ちないよう置換読みする
        # ⚠️ **timeout を付ける。** 付けないと固まった1本が永久に待ち、
        #    `ThreadPoolExecutor` の枠を潰したまま全体が止まる（上の「9.5分で2枚」）。
        try:
            r = subprocess.run(cmd, capture_output=True, text=True,
                               encoding="utf-8", errors="replace", timeout=120)
        except subprocess.TimeoutExpired:
            sys.exit(f"PNG の書き出しが 120 秒で終わりませんでした: {out_path}")
    if not out_path.exists():
        sys.exit(f"PNG を書き出せませんでした:\n{r.stderr[:1200]}")
    return out_path
