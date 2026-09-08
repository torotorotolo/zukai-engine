# -*- coding: utf-8 -*-
"""theme_ledger.py — 題材の帳簿。**毎回1から調べ直さないための道具**（2026-09-08）。

■ なぜ要るか（カズヤくん指示 2026-09-08）
    ①題材のチャットは毎回、ジャンル走査＋広域＋素材の実測を1からやり直していた。
    6本目の実行で **約5,830／10,000単位**と、チャット1回ぶんのやり取りを使っている。
    しかも結果は `analytics/` に置かれ、そこは **`.gitignore` で git 管理外**なので、
    次のチャットからは「無かったこと」になっていた。
    → **競合の公開データだけを `ref/themes/` に置いて git に載せ、次回はここから始める。**

    ⚠️ `analytics/` を git に載せてはいけない（このchの内部数字＝再生・維持・CTR が入る）。
       ここに置くのは **他局の公開データと、素材の実測値だけ**。自分のchの動画は入っていない
       （`yt_genre_scan` は自分のchを母集団に入れない）。

■ 置いてあるもの
    ref/themes/pool.json      … ジャンル主要局の解説動画の母集団（id/題/局/秒/再生/公開日）
    ref/themes/ledger.json    … 題材ごとの実測と判定（需要・素材・採否・その理由・測った日）
    ref/themes/README.md      … 🔴 次の①題材チャットの手順（ここから読む）

■ 使い方
    python tools/theme_ledger.py table                 # 帳簿を表で見る（まずこれ）
    python tools/theme_ledger.py table --only-open     # まだ採否が付いていない題材だけ
    python tools/theme_ledger.py neighbor --words スレッシャー --words タイタン号
    python tools/theme_ledger.py neighbor --ledger     # 帳簿の全題材を母集団から測り直す
    python tools/theme_ledger.py merge --pool analytics/themes/ep7_pool.json
                                                       # 新しく走査した母集団を足す（重複は新しいほうを採る）

■ 近所比とは
    その動画の再生数 ÷ **同じ局が前後45日に出した動画の再生数の中央値**。
    素の再生数は「局の大きさ」と「経過日数」を写すので比べられない。
    広域の当たり率（`yt_theme_probe`）は窓が6か月前で終わるので**直近に伸びた題材を見られない**。
    近所比なら窓の外の新作も同じ物差しに乗る。
    ⚠️ **本数が少ないと暴れる**（小さい局の1本が7〜99倍を出す）。順位付けに使わず、
       **「1.0× を割っているか」の足切り**に使うこと。
    ⚠️ 公開30日未満は熟成前なので、分子にも分母にも入れない。
"""
from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from datetime import date, datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).parent.parent
DIR = HERE / "ref" / "themes"
POOL = DIR / "pool.json"
LEDGER = DIR / "ledger.json"
MATURE_DAYS = 30
NEAR_DAYS = 45


def _d(s: str) -> date:
    return datetime.strptime(s[:10], "%Y-%m-%d").date()


def load_pool():
    if not POOL.exists():
        raise SystemExit(f"[中止] {POOL} が無い。`yt_genre_scan.py scan --dump` の結果を merge すること")
    return json.loads(POOL.read_text(encoding="utf-8"))


def load_ledger():
    if not LEDGER.exists():
        raise SystemExit(f"[中止] {LEDGER} が無い")
    return json.loads(LEDGER.read_text(encoding="utf-8"))


def neighbor(rows, pattern, today=None):
    """pattern に当たる動画それぞれの近所比を返す。[(倍率, row), …]"""
    today = today or date.today()
    mature = [r for r in rows if (today - _d(r["published"])).days >= MATURE_DAYS]
    pat = re.compile(pattern)
    out = []
    for h in [r for r in mature if pat.search(r["title"])]:
        h0 = _d(h["published"])
        peers = [r["views"] for r in mature
                 if r["channel"] == h["channel"] and r["id"] != h["id"]
                 and abs((_d(r["published"]) - h0).days) <= NEAR_DAYS]
        if len(peers) < 3:          # 比較対象が薄いと物差しにならない
            continue
        out.append((h["views"] / statistics.median(peers), h))
    out.sort(key=lambda t: -t[0])
    return out


def cmd_neighbor(a) -> int:
    rows = load_pool()
    if a.ledger:
        targets = [(t["name"], t.get("pattern") or "|".join(t.get("words", [])))
                   for t in load_ledger()["themes"]]
    elif a.words:
        targets = [(a.words[0], "|".join(a.words))]
    else:
        raise SystemExit("[中止] --words か --ledger のどちらかが要る")

    print(f"母集団 {len(rows)} 本 ／ 熟成の線 {MATURE_DAYS}日 ／ 近所の幅 ±{NEAR_DAYS}日")
    print(f"{'題材':<24}{'本':>3}{'局':>3}{'近所比':>8}{'最大':>7}   内訳")
    res = []
    for name, pat in targets:
        if not pat:
            continue
        rec = neighbor(rows, pat)
        if not rec:
            print(f"{name[:23]:<24}  —  近所比を出せる本が無い（同時期の比較対象が3本未満）")
            continue
        med = statistics.median([r for r, _ in rec])
        res.append((med, name, rec))
    for med, name, rec in sorted(res, reverse=True):
        detail = " ".join(f"{r:.2f}×/{h['views']//1000}k/{h['published'][2:7]}/{h['channel'][:6]}"
                          for r, h in rec[:4])
        ch = len({h["channel"] for _, h in rec})
        print(f"{name[:23]:<24}{len(rec):>3}{ch:>3}{med:>8.2f}{max(r for r, _ in rec):>7.2f}   {detail}")
    print("\n⚠️ 本数が少ないと暴れる。順位でなく **1.0× を割っているか** で足切りに使う")
    return 0


VERDICT = {"採用": "⭐採用", "保留": "△保留", "却下": "✕却下"}


def cmd_table(a) -> int:
    led = load_ledger()
    ts = led["themes"]
    if a.only_open:
        ts = [t for t in ts if t.get("verdict") not in ("採用", "却下")]
    ts.sort(key=lambda t: -(t.get("neighbor") or -1))
    print(f"# 題材の帳簿（{led['updated']} 時点・{len(led['themes'])}件）\n")
    print("| 題材 | 判定 | 近所比 | 棚 本/局 | 広域1万超(下限) | 全画面/PD | PD動画 | 一言 |")
    print("|---|---|---|---|---|---|---|---|")
    for t in ts:
        m = t.get("material", {})
        def _v(x):
            return "?" if x is None else x
        fs = f"{_v(m.get('fullscreen','?'))}/{_v(m.get('pd','?'))}" if m else "未測"
        vid = m.get("video_pd") or "未測" if m else "未測"
        nb = f"{t['neighbor']:.2f}×" if t.get("neighbor") is not None else "—"
        sh = f"{t.get('shelf_n','?')}/{t.get('shelf_ch','?')}"
        wd = t.get("wide", "—")
        print(f"| {t['name']} | {VERDICT.get(t.get('verdict'),'—')} | {nb} | {sh} | {wd} | "
              f"{fs} | {vid} | {t.get('note','')} |")
    print(f"\n🔴 詳しい理由は `ref/themes/ledger.json` の `reason`。手順は `ref/themes/README.md`")
    return 0


def cmd_merge(a) -> int:
    new = json.loads(Path(a.pool).read_text(encoding="utf-8"))
    old = json.loads(POOL.read_text(encoding="utf-8")) if POOL.exists() else []
    by = {r["id"]: r for r in old}
    added = sum(1 for r in new if r["id"] not in by)
    by.update({r["id"]: r for r in new})      # 同じ id は新しいほう（再生数が育っている）
    rows = sorted(by.values(), key=lambda r: r["published"], reverse=True)
    DIR.mkdir(parents=True, exist_ok=True)
    POOL.write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"母集団 {len(old)} → {len(rows)} 本（新規 {added}・更新 {len(new)-added}）")
    print(f"保存: {POOL.relative_to(HERE)}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="題材の帳簿（毎回1から調べ直さないための道具）")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("table", help="帳簿を表で見る")
    p.add_argument("--only-open", action="store_true", help="採否が付いていない題材だけ")
    p.set_defaults(fn=cmd_table)
    p = sub.add_parser("neighbor", help="母集団から近所比を測る")
    p.add_argument("--words", action="append", help="題名に含まれる語（複数可＝or）")
    p.add_argument("--ledger", action="store_true", help="帳簿の全題材を測り直す")
    p.set_defaults(fn=cmd_neighbor)
    p = sub.add_parser("merge", help="新しく走査した母集団を足す")
    p.add_argument("--pool", required=True)
    p.set_defaults(fn=cmd_merge)
    a = ap.parse_args()
    return a.fn(a)


if __name__ == "__main__":
    sys.exit(main())
