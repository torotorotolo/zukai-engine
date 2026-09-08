# -*- coding: utf-8 -*-
"""🔴 実写の欄が**全部埋まっているか**を、カットの側から数える門番（2026-09-08 ⑤b-4 新設）。

■ なぜ要るか（この日に実際に踏んだ）
  `python tools/footage.py fetch --check` は
    「✓ 全 35 欄に until= があり…」
  と**合格を出す**。しかし 35 は `USE` に書いた欄の数であって、
  **実写が要るカットの数（66）ではない**。
  ＝ 31欄が空のままでも、この門番は「0件を調べて合格」を出す
     → [[feedback-gates-blind-to-the-new-material]]

■ 何を数えるか
  章ファイルで `photo=ss.fb("<cid>")` と書いてあるカット ＝ 実写の欄。
  そのカットが `footage.USE` にあるか。**両側から突き合わせる**（片側だけだと
  「USE に在るがカットに無い」欄＝台本を直したあとの取り残しが見えない）。

■ 使い方
    python tools/check_footage_slots.py
    python tools/check_footage_slots.py --selftest
"""
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

HERE = Path(__file__).parent
FB = re.compile(r'photo=ss\.fb\("(\w+)"\)')


def slots(cutdir=None):
    """章ファイルから「実写が要るカット」を拾う。**SPEC ではなく本文を読む**。

    ⚠️ `scene_jiko` 経由で読むと、章ファイルが1本落ちていても
       「残った分で0件」になりうる。ここは .py の本文を直接読む。
    """
    d = Path(cutdir) if cutdir else HERE / "cuts"
    out = {}
    for f in sorted(d.glob("*.py")):
        if f.name in ("__init__.py", "ss.py"):
            continue
        for cid in FB.findall(f.read_text(encoding="utf-8")):
            out[cid] = f.name
    return out


def main(only=None):
    import footage as F
    need = slots()
    use = set(F.USE)
    if not need:
        print("🔴 実写の欄が1つも見つからない＝**章ファイルを読めていない**（合格にしない）")
        return 2
    missing = sorted(set(need) - use)
    extra = sorted(use - set(need))
    print(f"■ 実写が要るカット {len(need)} 欄／`footage.USE` に書けている {len(use & set(need))} 欄")
    if missing:
        print(f"🔴 まだ埋まっていない {len(missing)} 欄:")
        for i in range(0, len(missing), 10):
            print("   " + " ".join(missing[i:i + 10]))
    if extra:
        print(f"🔴 USE に在るのに実写のカットでない {len(extra)} 欄: {' '.join(extra)}")
    if not missing and not extra:
        print("✓ 実写の欄とカットが1対1")
    return 0 if not missing and not extra else 1


def selftest():
    """陽性対照＝**本番の中身が空でも回ること**と、欠けをちゃんと鳴らすこと。"""
    ok = True
    n = len(slots())
    print(f"  章ファイルから拾えた実写の欄 {n}")
    if n == 0:
        print("🔴 0件＝読めていない"); ok = False
    tmp = Path(__file__).parent.parent / "out" / "jiko" / "_slots_selftest"
    tmp.mkdir(parents=True, exist_ok=True)
    (tmp / "z.py").write_text('photo=ss.fb("zz01")\nphoto=ss.fb("zz02")\n',
                              encoding="utf-8")
    got = slots(tmp)
    if sorted(got) != ["zz01", "zz02"]:
        print(f"🔴 拾い方が違う: {got}"); ok = False
    else:
        print("  当て木の章ファイル2欄を拾えた")
    (tmp / "z.py").unlink()
    tmp.rmdir()
    print("✓ selftest 通過" if ok else "🔴 selftest 失敗")
    return ok


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        raise SystemExit(0 if selftest() else 1)
    raise SystemExit(main())
