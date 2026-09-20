# -*- coding: utf-8 -*-
"""check_photo_mask.py — **焼く前に元画像そのものを直す点**が、本当に直っているかを見る
（2026-09-20 新設・10本目 ⑤b-2）。

⚠️ 名前が似ているが `tools/check_mask.py` は**音**の検査（語尾が BGM に埋もれていないか）。
   こちらは**写真**（私人の顔・名前を隠したか）。別物なので混ぜない。

■ なぜ要るか（この日に実際に踏んだ）
  10本目の `missing_board_01`（行方不明者の掲示板）には、**私人の顔写真と名前**が写っている。
  素材は公共ヌリ第1類型なので**手直しが許されている**＝ぼかして使う、と ②b・⑤b-1 が決めた。
  ところが──

      grep -rn "blur" tools/*.py  → 使っているのは `extract_photos.py`（取り込み時）だけ

  **`blur=` は cut の書き方として実装されていない。**`cuts/ss.py` の `_BREAKS_FRAME` に
  "blur" が並んでいるので書けるように見えるが、`scene_jiko` も `build_jiko` も読まない。
  ＝ 章ファイルに `blur=` と書いても、**エラーも出さずに素のまま焼ける**。
  しかも門番14本は**1本もこれを見ていない**（`check_credits` は年と撮影者しか見ない）。
  → [[feedback-rules-need-gates]]／[[feedback-gates-blind-spot-is-the-scan-direction]]

■ 測るもの（fail closed。どれか1つでも欠けたら exit 2）
  1. 🔴 `cuts/ss.py` の `NEEDS_MASK` に載っている点が、カットに当たっているか
  2. 🔴 その点について `ref/ep10/masked.json` に記録があるか
  3. 🔴 記録の md5 が、**いま `ref/` にあるファイルの md5** と一致するか
     （＝直したファイルがそのまま置かれているか。差し替え・取り直しで戻ると鳴る）
  ⚠️ **「直したつもり」では通らない。**直した画像を置いて、md5 を記録して初めて通る。

■ ⚠️ この門番が見ないこと
  **ぼかしの範囲が足りているか**は見ない（画素を見る判定ではない）。
  範囲は⑤cで原寸を見て決める（→ `ref/ep10/photos.md` §5）。

■ 使い方
    python tools/check_photo_mask.py
    python tools/check_photo_mask.py --selftest   # 物差しの検算（陽性対照つき）
    python tools/check_photo_mask.py --record     # 直したあとに md5 を記録する
"""
from __future__ import annotations

import hashlib
import json
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

RECORD = HERE / "ref" / "ep10" / "masked.json"


def md5_of(path):
    h = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def load_record():
    """記録を読む。**読めなければ空ではなく None**（「無い」と「壊れている」を分ける）。"""
    if not RECORD.exists():
        return {}
    try:
        return json.loads(RECORD.read_text(encoding="utf-8"))
    except Exception as e:                                  # noqa: BLE001
        print(f"🔴 {RECORD.name} が読めない（{e}）。0件にして素通りさせない", file=sys.stderr)
        return None


def used_photos():
    """カットに当たっている写真 → そのカットIDの一覧。"""
    import cuts
    out = {}
    for cid, s in sorted(cuts.SPEC.items()):
        p = s.get("photo")
        if p:
            out.setdefault(p, []).append(cid)
    return out


def check(quiet=False):
    import cuts.ss as ss

    need = getattr(ss, "NEEDS_MASK", {})
    used = used_photos()
    rec = load_record()
    if rec is None:
        return 2

    bad, ok = [], []
    for name, why in sorted(need.items()):
        cids = used.get(name)
        if not cids:
            ok.append(f"・{name} はどのカットにも当たっていない（隠す必要も出ない）")
            continue
        f = HERE / "ref" / name
        if not f.exists():
            bad.append(f"{name}：素材が `ref/` に無い（{cids[0]} に当てている）")
            continue
        now = md5_of(f)
        got = rec.get(name)
        if not got:
            bad.append(f"{name}（{'・'.join(cids)}）：{why}\n"
                       f"      → まだ直していない。直したうえで "
                       f"`python tools/check_photo_mask.py --record`")
        elif got.get("md5") != now:
            bad.append(f"{name}（{'・'.join(cids)}）：記録の md5 と合わない\n"
                       f"      記録 {got.get('md5')} ／ いま {now}\n"
                       f"      → 素材が差し替わった。直し直して記録も取り直す")
        else:
            ok.append(f"✓ {name}（{'・'.join(cids)}）直したファイルが置かれている"
                      f"　{got.get('when', '')}")

    if not quiet:
        print(f"■ 焼く前に元画像を直す点 {len(need)}件を、写真を出すカット {len(used)}欄と"
              f"突き合わせた")
        for line in ok:
            print("  " + line)
        for line in bad:
            print("  🔴 " + line)
    if bad:
        print(f"\n🔴 直していない素材がある（{len(bad)}件）。**合格にしない**")
        print("   ⚠️ `blur=` を章ファイルに書いても効かない（実装されていない）。"
              "元画像そのものを直すこと")
        return 2
    if not need:
        print("  🔴 `NEEDS_MASK` が空。この回に隠す素材が無いなら正しいが、"
              "**0件を調べて合格**にしていないか確かめること")
    if not quiet:
        print("\n✓ 通った")
    return 0


def record():
    """直したあとに md5 を記録する。⚠️ 直す前に走らせると「素のまま」を記録してしまう。"""
    import cuts.ss as ss

    rec = load_record() or {}
    for name, why in sorted(getattr(ss, "NEEDS_MASK", {}).items()):
        f = HERE / "ref" / name
        if not f.exists():
            print(f"🔴 {name} が `ref/` に無い")
            continue
        rec[name] = dict(md5=md5_of(f), when=date.today().isoformat(), what=why)
        print(f"記録した: {name} → {rec[name]['md5']}")
    RECORD.parent.mkdir(parents=True, exist_ok=True)
    RECORD.write_text(json.dumps(rec, ensure_ascii=False, indent=2) + "\n",
                      encoding="utf-8")
    print(f"→ {RECORD}")
    return 0


def selftest():
    """🔴 物差しそのものを検算する。**鳴ることを数字で見る**（陽性対照）。"""
    import tempfile
    import cuts.ss as ss

    print("■ selftest（陽性対照つき）")
    need = getattr(ss, "NEEDS_MASK", {})
    assert need, "NEEDS_MASK が空では検算にならない"
    name = sorted(need)[0]
    f = HERE / "ref" / name
    assert f.exists(), f"{name} が `ref/` に無い"

    # ① md5 が本当に中身で変わることを、同じ道具で2つの中身を測って見る
    with tempfile.TemporaryDirectory() as d:
        a, b = Path(d) / "a.bin", Path(d) / "b.bin"
        a.write_bytes(b"x" * 1000)
        b.write_bytes(b"x" * 999 + b"y")
        ma, mb = md5_of(a), md5_of(b)
        assert ma != mb, "1バイト違うのに md5 が同じ＝測れていない"
        print(f"  ✓ 1バイト違えば md5 が変わる（{ma[:8]}… / {mb[:8]}…）")

    # ② いまの状態で、返ってくる exit が予定どおりか
    rec = load_record() or {}
    now = md5_of(f)
    has = bool(rec.get(name)) and rec[name].get("md5") == now
    want = 0 if has else 2
    print(f"  ・いまの状態: {name} の記録は "
          f"{'ある（md5 一致）' if has else 'まだ無い／合わない'} → exit {want} のはず")
    got = check(quiet=True)
    assert got == want, f"検算が合わない（返ってきたのは {got}、予定は {want}）"
    print(f"  ✓ 実際に exit {got} が返った")

    # ③ 陽性対照：記録を1バイト書き換えたものを渡すと、必ず 🔴 になる
    saved = rec.get(name)
    try:
        rec[name] = dict(md5="0" * 32, when="selftest", what="陽性対照")
        RECORD.parent.mkdir(parents=True, exist_ok=True)
        RECORD.write_text(json.dumps(rec, ensure_ascii=False, indent=2) + "\n",
                          encoding="utf-8")
        assert check(quiet=True) == 2, "md5 を壊したのに鳴らない＝門番が見ていない"
        print("  ✓ 陽性対照：記録の md5 を壊すと 🔴 になる")
    finally:
        if saved is None:
            rec.pop(name, None)
        else:
            rec[name] = saved
        if rec:
            RECORD.write_text(json.dumps(rec, ensure_ascii=False, indent=2) + "\n",
                              encoding="utf-8")
        elif RECORD.exists():
            RECORD.unlink()
    print("  ✓ 記録をもとに戻した")
    return 0


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        sys.exit(selftest())
    if "--record" in sys.argv:
        sys.exit(record())
    sys.exit(check())
