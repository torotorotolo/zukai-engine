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

CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
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
            f"--window-size={w},{h}", f"--screenshot={out_path}",
            src.resolve().as_uri(),
        ]
        # Chrome の stderr は日本語が混ざる。cp932 で落ちないよう置換読みする
        r = subprocess.run(cmd, capture_output=True, text=True,
                           encoding="utf-8", errors="replace")
    if not out_path.exists():
        sys.exit(f"PNG を書き出せませんでした:\n{r.stderr[:1200]}")
    return out_path
