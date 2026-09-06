# -*- coding: utf-8 -*-
"""⑤c 検品の「見た枚」と「疑いの一覧」を機械で持つ（2026-09-07・`qa_out/ss_seen.py` の一般化）。

■ なぜ機械で持つか
    手で数えると必ず間違える。実例：4本目で「34枚／次は cap037」と報告したが、
    道具を入れたら「35枚／次は cap036」だった（[[feedback-split-chats-by-stage]]）。

■ 2つの帳（単位が違うので分けてある）
    **シート**（⑤c-1）… `out/jiko/sheet_<ver>/sheet_NN_*.jpg` を1枚ずつ。40枚で1チャット
    **原寸**  （⑤c-2）… `out/jiko/qa_<ver>/cut_<cid>.jpg` を1カットずつ。40枚で1チャット
    ⚠️ 引数の形で自動的に振り分けるが、**どちらの帳に書いたか必ず表示する**。
       混ぜて渡すと止まる（`01 c101` のような書き方は受け取らない）。

■ 🔴 「見たあとに焼き直された」を自分で見つける（4本目の事故の型）
    `cap_restale.py` は比べるフォルダ名が本文に焼き付いていて、**前の絵どうしを比べて
    「1枚も変わっていません」と嘘をついた**（[[feedback-verify-your-own-instrument]] 8例目）。
    → ここでは**フォルダを `qa_out/<slug>_qa.json` に置き**（本文に書かない）、
      見た時点の **md5 を1枚ずつ記録**する。`check` は今のファイルと突き合わせ、
      違っていれば「見た枚」から自動で落とす（＝もう一度見る）。
      ⚠️ 更新時刻では決まらない（上書き保存でも新しくなる）ので md5 で見る。

■ 疑いの一覧（`qa_out/<slug>_suspects.md`）
    ⑤c-1（シート）で気になった所を書き、⑤c-2（原寸）で決着を付ける。
    所見そのものは台帳へ。ここに持つのは「まだ原寸で見ていない疑い」だけ。

■ 使い方
    python tools/qa_seen.py ss init --src out/jiko/qa_ss-r05   # 帳を作る（1回だけ）
    python tools/qa_seen.py ss check
    python tools/qa_seen.py ss mark 01 02 03 04                # シートを4枚見た
    python tools/qa_seen.py ss mark c101 c102                  # 原寸で2カット見た
    python tools/qa_seen.py ss unmark 04
    python tools/qa_seen.py ss suspect add c204 "注記が写真の外に出ている"
    python tools/qa_seen.py ss suspect list
    python tools/qa_seen.py ss suspect done c204 "原寸で確認・粗なし"
    python tools/qa_seen.py --selftest
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent.parent
QA_OUT = HERE / "qa_out"
OUT = HERE / "out" / "jiko"
PER_CHAT = 40

SHEET = "sheet"
FULL = "full"


def md5(p: Path) -> str:
    h = hashlib.md5()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()[:12]


# ── 帳の場所（🔴 本文にフォルダ名を焼き付けない）──────────────────
def cfg_path(slug):
    return QA_OUT / f"{slug}_qa.json"


def load_cfg(slug):
    p = cfg_path(slug)
    if not p.exists():
        raise SystemExit(f"🔴 {p.relative_to(HERE)} が無い。先に\n"
                         f"   python tools/qa_seen.py {slug} init --src out/jiko/qa_<ver>")
    c = json.loads(p.read_text(encoding="utf-8"))
    for key in ("src", "sheets"):
        d = HERE / c[key]
        if not d.is_dir():
            # 🔴 fail closed：見ているフォルダが無いのに「0枚見た」と答えない
            raise SystemExit(f"🔴 {key} のフォルダが無い: {c[key]}（焼き直しで消えた？ init し直す）")
    return c


def do_init(slug, src, sheets):
    src_p = HERE / src if not Path(src).is_absolute() else Path(src)
    if not src_p.is_dir():
        raise SystemExit(f"🔴 --src が無い: {src_p}")
    ver = src_p.name[3:] if src_p.name.startswith("qa_") else src_p.name
    sh_p = (HERE / sheets) if sheets else (OUT / f"sheet_{ver}")
    if not sh_p.is_dir():
        raise SystemExit(f"🔴 シートのフォルダが無い: {sh_p}\n"
                         f"   先に python tools/qa_sheet.py {slug} --src {src}")
    QA_OUT.mkdir(exist_ok=True)
    cfg = dict(slug=slug, ver=ver,
               src=str(src_p.relative_to(HERE)).replace("\\", "/"),
               sheets=str(sh_p.relative_to(HERE)).replace("\\", "/"),
               made=datetime.now().strftime("%Y-%m-%d %H:%M"))
    cfg_path(slug).write_text(json.dumps(cfg, ensure_ascii=False, indent=1),
                              encoding="utf-8")
    n_c, n_s = len(items(cfg, FULL)), len(items(cfg, SHEET))
    print(f"✓ {cfg_path(slug).relative_to(HERE)} を作った")
    print(f"   版 {ver} ／ 原寸 {n_c}カット ／ シート {n_s}枚")
    return 0


def items(cfg, track):
    """その帳が扱う物の名前（**並べ方はファイル名の昇順**。qa_sheet.py と同じ）。"""
    if track == SHEET:
        return sorted(f.name[6:-4] for f in (HERE / cfg["sheets"]).glob("sheet_*.jpg"))
    return sorted(f.name[4:-4] for f in (HERE / cfg["src"]).glob("cut_*.jpg"))


def path_of(cfg, track, name):
    if track == SHEET:
        return HERE / cfg["sheets"] / f"sheet_{name}.jpg"
    return HERE / cfg["src"] / f"cut_{name}.jpg"


def seen_path(slug, track):
    return QA_OUT / f"{slug}_seen_{track}.tsv"


def read_seen(slug, track):
    """[(名前, 見たときの md5)]。順番は書いた順（＝見た順）。"""
    p = seen_path(slug, track)
    if not p.exists():
        return []
    out = []
    for ln in p.read_text(encoding="utf-8").splitlines():
        if not ln.strip():
            continue
        parts = ln.split("\t")
        out.append((parts[0].strip(), parts[1].strip() if len(parts) > 1 else ""))
    return out


def write_seen(slug, track, rows):
    seen_path(slug, track).parent.mkdir(exist_ok=True)
    seen_path(slug, track).write_text(
        "".join(f"{n}\t{h}\n" for n, h in rows), encoding="utf-8")


def track_of(cfg, names):
    """引数の形から帳を決める。⚠️ 混ぜて渡されたら止める（取り違えを構造上なくす）。"""
    sheets, cuts = set(items(cfg, SHEET)), set(items(cfg, FULL))
    # シートは「01」「sheet_01_c101-c106」「01_c101-c106」のどれでも受ける
    got = set()
    resolved = []
    for n in names:
        n = n.strip()
        key = n[6:] if n.startswith("sheet_") else n
        if key in sheets:
            got.add(SHEET); resolved.append((SHEET, key)); continue
        hit = [s for s in sheets if s.split("_")[0] == key.zfill(2)]
        if len(hit) == 1:
            got.add(SHEET); resolved.append((SHEET, hit[0])); continue
        if n in cuts:
            got.add(FULL); resolved.append((FULL, n)); continue
        raise SystemExit(f"🔴 「{n}」はシートにもカットにも無い（打ち間違い？）")
    if len(got) > 1:
        raise SystemExit("🔴 シートとカットを混ぜて渡された。どちらの帳に書くか決まらない")
    return got.pop(), [r[1] for r in resolved]


def do_mark(slug, cfg, names, remove=False):
    track, resolved = track_of(cfg, names)
    rows = read_seen(slug, track)
    have = {n for n, _ in rows}
    if remove:
        rows = [(n, h) for n, h in rows if n not in resolved]
        write_seen(slug, track, rows)
        print(f"✓ {'シート' if track == SHEET else '原寸'}の帳から {len(resolved)}件 消した")
        return
    for n in resolved:
        if n in have:
            raise SystemExit(f"🔴 {n} は記録ずみ（二重に数えない）")
    rows += [(n, md5(path_of(cfg, track, n))) for n in resolved]
    write_seen(slug, track, rows)
    print(f"✓ {'シート' if track == SHEET else '原寸'}の帳に {len(resolved)}件 足した: "
          f"{' '.join(resolved)}")


def restale(slug, cfg, track):
    """見たあとに焼き直された物を返し、帳から落とす（🔴 黙って「見た」ままにしない）。"""
    rows = read_seen(slug, track)
    stale, keep = [], []
    for n, h in rows:
        p = path_of(cfg, track, n)
        if not p.exists():
            stale.append((n, "消えた"))
            continue
        now = md5(p)
        if h and now != h:
            stale.append((n, f"{h}→{now}"))
        else:
            keep.append((n, h or now))
    if stale:
        write_seen(slug, track, keep)
    return stale


def do_check(slug, cfg):
    print(f"■ {cfg['slug']}（版 {cfg['ver']}）  原寸 {cfg['src']} ／ シート {cfg['sheets']}")
    for track, label in ((SHEET, "シート（⑤c-1）"), (FULL, "原寸（⑤c-2）")):
        all_ = items(cfg, track)
        stale = restale(slug, cfg, track)
        s = [n for n, _ in read_seen(slug, track)]
        rest = [n for n in all_ if n not in s]
        n_chat = len(s) % PER_CHAT or (PER_CHAT if s else 0)
        print(f"  {label}: 全 {len(all_)} ／ 見た {len(s)}"
              f"（このチャット {n_chat}/{PER_CHAT}）／ 残り {len(rest)}")
        if stale:
            print(f"    🔴 見たあとに焼き直された {len(stale)}件＝帳から落とした（もう一度見る）: "
                  + " ".join(f"{n}({w})" for n, w in stale[:6])
                  + (" …" if len(stale) > 6 else ""))
        nxt = [n for n in all_ if n not in s][:4]
        print(f"    次の4枚: {' '.join(nxt) if nxt else '（全数完了）'}")
    sus = read_suspects(slug)
    open_ = [r for r in sus if not r["done"]]
    print(f"  疑い: {len(sus)}件（未決 {len(open_)}）"
          + (f" → {' '.join(r['cut'] for r in open_[:8])}" if open_ else ""))
    return 0


# ── 疑いの一覧 ────────────────────────────────────────────
SUS_HEAD = ("| カット | 理由 | 出どころ | 原寸で見たか | 決着 |\n"
            "|---|---|---|---|---|\n")


def sus_path(slug):
    return QA_OUT / f"{slug}_suspects.md"


def read_suspects(slug):
    p = sus_path(slug)
    if not p.exists():
        return []
    out = []
    for ln in p.read_text(encoding="utf-8").splitlines():
        if not ln.startswith("|") or ln.startswith("|---") or "カット |" in ln:
            continue
        c = [x.strip() for x in ln.strip().strip("|").split("|")]
        while len(c) < 5:
            c.append("")
        out.append(dict(cut=c[0], why=c[1], src=c[2], seen=c[3], done=c[4]))
    return out


def write_suspects(slug, rows):
    sus_path(slug).parent.mkdir(exist_ok=True)
    body = "".join(f"| {r['cut']} | {r['why']} | {r['src']} | {r['seen']} | {r['done']} |\n"
                   for r in rows)
    sus_path(slug).write_text(
        f"# 疑いの一覧（{slug}）\n\n"
        f"⑤c-1（シート）で気になった所。⑤c-2（原寸）で決着を付ける。\n"
        f"所見そのものは台帳へ。ここに残すのは**まだ原寸で見ていない疑い**。\n\n"
        + SUS_HEAD + body, encoding="utf-8")


def do_suspect(slug, cfg, argv):
    sub = argv[0] if argv else "list"
    rows = read_suspects(slug)
    cuts = set(items(cfg, FULL))
    if sub == "list":
        open_ = [r for r in rows if not r["done"]]
        print(f"■ 疑い {len(rows)}件（未決 {len(open_)}／決着 {len(rows) - len(open_)}）")
        for r in rows:
            mark = "✓" if r["done"] else ("👁" if r["seen"] else "・")
            print(f"  {mark} {r['cut']:<6} {r['why'][:52]}"
                  + (f"  → {r['done'][:40]}" if r["done"] else ""))
        if not rows:
            print("  （まだ1件も無い）")
        return 0
    if sub == "add":
        if len(argv) < 3:
            raise SystemExit('🔴 使い方: suspect add <カット> "理由" [--src シート名]')
        cut, why = argv[1], argv[2]
        if cut not in cuts:
            raise SystemExit(f"🔴 {cut} は検品画像に無い（打ち間違い？）")
        if any(r["cut"] == cut and r["why"] == why for r in rows):
            raise SystemExit(f"🔴 {cut} に同じ理由の疑いがすでにある")
        src = argv[argv.index("--src") + 1] if "--src" in argv else ""
        rows.append(dict(cut=cut, why=why, src=src, seen="", done=""))
        write_suspects(slug, rows)
        print(f"✓ 疑いに足した: {cut}「{why}」（未決 "
              f"{len([r for r in rows if not r['done']])}件）")
        return 0
    if sub == "done":
        if len(argv) < 2:
            raise SystemExit('🔴 使い方: suspect done <カット> ["決着の一言"]')
        cut = argv[1]
        note = argv[2] if len(argv) > 2 else "原寸で確認"
        hit = [r for r in rows if r["cut"] == cut and not r["done"]]
        if not hit:
            raise SystemExit(f"🔴 {cut} に未決の疑いが無い")
        seen_now = {n for n, _ in read_seen(slug, FULL)}
        for r in hit:
            # ⚠️ 「原寸で見たか」は自己申告でなく**原寸の帳**から取る
            r["seen"] = "✓" if cut in seen_now else "🔴 未（原寸の帳に無い）"
            r["done"] = note
        write_suspects(slug, rows)
        left = len([r for r in rows if not r["done"]])
        print(f"✓ {cut} を決着（{hit[0]['seen']}）／ 未決 残り {left}件")
        if cut not in seen_now:
            print(f"  🔴 {cut} は原寸の帳に無い。先に `mark {cut}` してから決着させる")
            return 1
        return 0
    raise SystemExit(f"🔴 suspect の使い方は add / done / list（もらった値: {sub}）")


# ── 検算 ─────────────────────────────────────────────────
def selftest():
    """物差しの検算。**本番の関数そのもの**を、作り物のフォルダに当てる。"""
    import shutil
    import tempfile
    global HERE, QA_OUT, OUT
    keep = (HERE, QA_OUT, OUT)
    tmp = Path(tempfile.mkdtemp(prefix="qaseen_"))
    ok = True

    def say(cond, msg):
        nonlocal ok
        ok &= bool(cond)
        print(f"  {'✓' if cond else '🔴'} {msg}")

    try:
        HERE = tmp
        QA_OUT = tmp / "qa_out"
        OUT = tmp / "out" / "jiko"
        src = OUT / "qa_zz-r01"
        shd = OUT / "sheet_zz-r01"
        src.mkdir(parents=True); shd.mkdir(parents=True)
        for i in range(12):
            (src / f"cut_c{101 + i}.jpg").write_bytes(b"x" * (100 + i))
        for i in range(2):
            (shd / f"sheet_{i + 1:02d}_a-b.jpg").write_bytes(b"y" * (50 + i))

        do_init("zz", str(src.relative_to(tmp)), str(shd.relative_to(tmp)))
        cfg = load_cfg("zz")
        say(len(items(cfg, FULL)) == 12 and len(items(cfg, SHEET)) == 2,
            "init がカット12・シート2を数えた")

        do_mark("zz", cfg, ["c101", "c102"])
        say([n for n, _ in read_seen("zz", FULL)] == ["c101", "c102"], "原寸の帳に2件")
        do_mark("zz", cfg, ["01"])
        say([n for n, _ in read_seen("zz", SHEET)] == ["01_a-b"],
            "「01」だけでシートの帳に入る")

        # 🔴 陽性対照1：混ぜて渡したら止まる
        try:
            do_mark("zz", cfg, ["01", "c103"]); say(False, "混ぜても止まらなかった")
        except SystemExit:
            say(True, "シートとカットを混ぜると止まる")
        # 🔴 陽性対照2：打ち間違いは黙って通らない
        try:
            do_mark("zz", cfg, ["c999"]); say(False, "無いカットを受け取った")
        except SystemExit:
            say(True, "無いカットは止まる")
        # 🔴 陽性対照3：二重に数えない
        try:
            do_mark("zz", cfg, ["c101"]); say(False, "二重に数えた")
        except SystemExit:
            say(True, "記録ずみは二重に数えない")

        # 🔴 陽性対照4：**焼き直したら「見た」から落ちる**（4本目の嘘の型）
        (src / "cut_c101.jpg").write_bytes(b"NEW-CONTENT")
        stale = restale("zz", cfg, FULL)
        say([n for n, _ in stale] == ["c101"], "焼き直した c101 を見つけた")
        say([n for n, _ in read_seen("zz", FULL)] == ["c102"], "帳から自動で落ちた")
        # ⚠️ 中身が同じなら落とさない（鳴りすぎの検算）
        say(restale("zz", cfg, FULL) == [], "2回目は鳴らない（同じ中身では落とさない）")

        # 疑いの一覧
        do_suspect("zz", cfg, ["add", "c104", "注記が写真の外"])
        say(len(read_suspects("zz")) == 1, "疑いを1件足した")
        try:
            do_suspect("zz", cfg, ["add", "c104", "注記が写真の外"])
            say(False, "同じ疑いを二重に足した")
        except SystemExit:
            say(True, "同じ疑いは二重に足さない")
        # 🔴 陽性対照5：原寸で見ていないのに「決着」させたら鳴る
        rc = do_suspect("zz", cfg, ["done", "c104", "見た"])
        say(rc == 1 and read_suspects("zz")[0]["seen"].startswith("🔴"),
            "原寸の帳に無いまま決着させると鳴る（自己申告を信じない）")
    finally:
        HERE, QA_OUT, OUT = keep
        shutil.rmtree(tmp, ignore_errors=True)
    print("  " + ("✓ 物差しは正しい" if ok else "🔴 物差しに落ちた"))
    return ok


def main():
    if "--selftest" in sys.argv:
        return 0 if selftest() else 1
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("cmd", nargs="?", default="check",
                    choices=["check", "init", "mark", "unmark", "suspect"])
    ap.add_argument("rest", nargs="*")
    ap.add_argument("--src", default="")
    ap.add_argument("--sheets", default="")
    a, _ = ap.parse_known_args()
    rest = [x for x in a.rest if x not in ("--src", a.src, "--sheets", a.sheets) or x == ""]

    if a.cmd == "init":
        if not a.src:
            raise SystemExit("🔴 init には --src out/jiko/qa_<ver> が要る")
        return do_init(a.slug, a.src, a.sheets)
    cfg = load_cfg(a.slug)
    if a.cmd == "check":
        return do_check(a.slug, cfg)
    if a.cmd in ("mark", "unmark"):
        if not rest:
            raise SystemExit(f"🔴 {a.cmd} に名前が無い")
        do_mark(a.slug, cfg, rest, remove=(a.cmd == "unmark"))
        return do_check(a.slug, cfg)
    if a.cmd == "suspect":
        return do_suspect(a.slug, cfg, rest)
    return 0


if __name__ == "__main__":
    sys.exit(main())
