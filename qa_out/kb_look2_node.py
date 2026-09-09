# -*- coding: utf-8 -*-
"""`people`（箱を並べる図）で、箱の「題」が箱の「小見出し」より小さくなっていないかを全数で測る。
（2026-09-10・⑤c 検品【見る】2周目 2/3）

なぜ：`titan_fig.people()` は 題＝`cap=TS_CAP(56×)`／小見出し＝`cap=DS_CAP(34×)` と
      **題のほうを大きく取る設計**だが、どちらも `fm.fit()` で幅に合わせて縮む。
      題が長いカットでは題だけが縮み、**小見出しのほうが大きい**画になる。

陽性対照：`c711`（箱1「高圧の遮断器 HR1」＝原寸で見て、小見出し「ここより上流」のほうが大きい）
"""
import re
import sys

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "tools")

import titan_fig as T  # noqa: E402
import jiko_style as J  # noqa: E402
from cuts import SPEC  # noqa: E402

PAT = re.compile(r'font-size="([0-9.]+)"[^>]*fill="(%s|%s)"'
                 % (re.escape(J.INK_W), re.escape(J.TICK)))


def main():
    bad, cuts = [], 0
    for cid, spec in SPEC.items():
        fig = spec.get("fig")
        if not fig or fig[0] != "people":
            continue
        cuts += 1
        f = T.people(**fig[1])
        svg = "".join(getattr(f, "stages", None) or [str(f)])
        pairs = [(float(a), b) for a, b in PAT.findall(svg)]
        # 題(INK_W) の直後に来る小見出し(TICK) が、その箱の組
        for i, (sz, col) in enumerate(pairs):
            if col != J.INK_W or i + 1 >= len(pairs):
                continue
            nsz, ncol = pairs[i + 1]
            if ncol != J.TICK:
                continue
            if nsz >= sz:
                bad.append((sz - nsz, cid, sz, nsz))
    bad.sort()
    print(f"people カット {cuts} 枚を測った")
    print(f"🔴 小見出しが題と同じか大きい箱 ＝ {len(bad)} 組 / "
          f"{len({b[1] for b in bad})} カット")
    for d, cid, sz, nsz in bad:
        print(f"  {cid}  題 {sz:.0f} 対 小見出し {nsz:.0f}")
    print(f"\n陽性対照 c711 = "
          f"{'出た' if any(b[1] == 'c711' for b in bad) else '🔴出ない＝測れていない'}")


if __name__ == "__main__":
    main()
