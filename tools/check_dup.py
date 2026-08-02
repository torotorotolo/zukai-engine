# -*- coding: utf-8 -*-
"""**同じ画面の中で同じ言葉を二度出していないか**を機械で見る。

■ なぜ要るか
  `check_echo` は「図の文字 **対 ナレーション**」しか見ていない。
  r21 の目視で c310 が見つかった：

      副題         「2018年1月　品質検査の報告書」
      図の矢印の札 「2018年1月　品質検査の報告書」   ← **丸ごと同じ**

  同じ画面の中に同じ文字列が2か所ある。音とも字幕とも関係が無いので
  `check_echo` は素通りする。[[feedback-no-subtitle-when-onscreen]]
  「同じ言葉を複数か所に表示しても意味がない」に真正面から当たる。

■ 測り方
  カットごとに、画面に出る文字列を **出る場所つき**で集める。
    ・見出し（t）／副題（s）  … カット表から
    ・図の中の文字            … レイヤーの <text> から
  そのうえで **見出し・副題 と 図の中の文字** を突き合わせ、
  **短いほうが長いほうに丸ごと含まれる**なら二重表示とする。

  ⚠️ 図どうしの重複は見ない。凡例と軸名、棒の名前と注記が同じ語を持つのは
     図として自然（「ひずみ」が縦軸名と凡例に出るなど）。
     問題は **見出し／副題という「別の役目の場所」と重なる**こと。

■ この道具を疑うために（[[feedback-verify-your-own-instrument]]）
  `--check` で、**分かっている答え**を再現できるか先に確かめる。
    ・c310 は出る（実際に目視で見つけた）
    ・数字・単位だけ、4字未満、カタカナ語1語は出ない（部位名・固有名詞なので）

使い方： python tools/check_dup.py [--only=c3] [--check]
"""
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")

import scene_jiko as S

TEXT = re.compile(r'<text\s[^>]*>([^<]*)</text>')
UNESC = {"&amp;": "&", "&lt;": "<", "&gt;": ">"}
MINLEN = 4

# 数値・単位・記号だけで出来た文字列は、図と見出しの両方に出て当然。
DATAISH = re.compile(r"^[0-9０-９,.，．%％\s"
                     r"a-zA-Zａ-ｚＡ-Ｚ"
                     r"年月日時分秒回本個名人隻機層枚倍度円m"
                     r"／/・:：〜~\-−－(（)）]+$")

# 「見出し／副題に出てよい」語。図がラベルとして持つのが当たり前のもの。
# ⚠️ ここを広げすぎると道具が何も言わなくなる。**固有名詞1語だけ**に絞る。
KATAKANA1 = re.compile(r"^[ァ-ヶー]+$")


def unesc(t):
    for k, v in UNESC.items():
        t = t.replace(k, v)
    return t


def norm(s):
    if isinstance(s, (list, tuple)):
        s = "".join(str(x) for x in s)
    return re.sub(r"[、。，．\s「」『』（）()【】・…　]", "", str(s))


def collect(only=None):
    """カットごとに {図の中の文字列: [レイヤー名]} を返す。"""
    jobs, _ = S.build_layers(allow_missing=True)
    bycut = defaultdict(list)
    for k, svg in jobs.items():
        cid = k.rsplit("_", 1)[0]
        if only and not cid.startswith(only):
            continue
        # 見出しと章マーカーのレイヤーは「図の中」ではない。
        # ⚠️ 実写カットは見出しが _lab に入るので、レイヤー名では切れない。
        #    文字列の中身で突き合わせるので、ここでは全部集めてよい。
        for m in TEXT.finditer(svg):
            t = unesc(m.group(1)).strip()
            if t:
                bycut[cid].append((k, t))
    return bycut


def scan(only=None):
    bycut = collect(only)
    hits = []
    for cid in sorted(bycut):
        spec = S.SPEC.get(cid, {})
        heads = [("見出し", str(spec.get("t", "") or "")),
                 ("副題", str(spec.get("s", "") or ""))]
        heads = [(kind, v) for kind, v in heads if norm(v)]
        if not heads:
            continue
        # 図の中の文字。**見出し・副題そのものを描いているレイヤーは除く**
        # （見出しは画面に1回出るだけなので、それ自身とは比べない）。
        headn = {norm(v) for _, v in heads}
        seen = set()
        cover = {"見出し": {}, "副題": {}}
        for layer, t in bycut[cid]:
            n = norm(t)
            if n in headn:
                # 見出し／副題を描いているレイヤー本体。ただし
                # **同じ文字列が2回以上出てくる**なら、それは二重表示。
                if (cid, n) in seen:
                    hits.append((cid, "見出し/副題", t, layer, "同じ文字列が2か所に出ている"))
                seen.add((cid, n))
                continue
            if len(n) < MINLEN or DATAISH.match(t) or KATAKANA1.match(n):
                continue
            for kind, hv in heads:
                h = norm(hv)
                if len(h) < MINLEN:
                    continue
                if n in h or h in n:
                    cover[kind].setdefault(hv, []).append((t, n, layer))
                    break
        # 🔴 ここを「重なりが1つでもあれば言う」にしたら、**使えなかった**。
        #    見出し「毎分33メートルで降りていた」に対して図が「毎分33メートル」と
        #    数値を出すのは、この動画の設計そのもの（図が持つのは数値・部位名）。
        #    問題は **見出し／副題が、図のラベルを並べただけになっている**こと。
        #    → 図のラベルが見出し／副題の **7割以上を覆う**ときだけ言う。
        for kind, d in cover.items():
            for hv, got in d.items():
                h = norm(hv)
                covered = set()
                for t, n, layer in got:
                    i = h.find(n)
                    if i >= 0:
                        covered.update(range(i, i + len(n)))
                    elif n.find(h) >= 0:
                        covered.update(range(len(h)))
                r = len(covered) / len(h) if h else 0
                if r >= 0.70:
                    hits.append((cid, kind, hv, got[0][2],
                                 f"図のラベル {'／'.join(t for t, _, _ in got)} が"
                                 f"{r:.0%}を覆う＝{kind}が図の写しになっている"))
    return hits


def covers(head, labels):
    """図のラベル群が、見出し／副題の何割を覆うか。**判定の核**をここに出しておく。"""
    h = norm(head)
    if len(h) < MINLEN:
        return 0.0
    got = set()
    for t in labels:
        n = norm(t)
        if len(n) < MINLEN or DATAISH.match(t) or KATAKANA1.match(n):
            continue
        i = h.find(n)
        if i >= 0:
            got.update(range(i, i + len(n)))
        elif n.find(h) >= 0:
            got.update(range(len(h)))
    return len(got) / len(h)


def selfcheck():
    """★道具そのものを検算する。

    ⚠️ 最初は「c310 を拾えるか」で検算していたが、**c310 を直した瞬間に
       道具が壊れていると言い出した**（実データを基準にしていたため）。
       検算は**作り物の例**で行う。直した結果に影響されない。
    """
    print("── 道具の検算 ──")
    ok = True
    # 実際に目視で見つけた形（c310）を、そのまま作り物として持っておく
    fixtures = [
        ("副題が図の札と丸ごと同じ（c310 で実際に起きた形）",
         "2018年1月　品質検査の報告書", ["2018年1月　品質検査の報告書"], True),
        ("副題が2つの札を並べただけ（c202 の形）",
         "海面の気圧と、水深3,800メートルの水圧",
         ["海面の気圧", "水深3,800メートルの水圧"], True),
        ("見出しが言い、図は数値を出すだけ（c113a の形＝**直さない**）",
         "毎分33メートルで降りていた", ["毎分33メートル"], False),
        ("図が部位名を持つだけ（**直さない**）",
         "リングと円筒のあいだは接着剤", ["接着剤"], False),
    ]
    for name, head, labels, should in fixtures:
        r = covers(head, labels)
        hit = r >= 0.70
        mark = "✓" if hit == should else "✗"
        if hit != should:
            ok = False
        print(f"  {mark} {name}\n      覆う割合 {r:.0%} → "
              f"{'言う' if hit else '黙る'}（そうあるべき: {'言う' if should else '黙る'}）")

    cases = [("3,840", True), ("m", True), ("タイタン", True),
             ("2018年1月", True), ("品質検査の報告書", False)]
    for s, should_skip in cases:
        skipped = (len(norm(s)) < MINLEN or bool(DATAISH.match(s))
                   or bool(KATAKANA1.match(norm(s))))
        mark = "✓" if skipped == should_skip else "✗"
        if skipped != should_skip:
            ok = False
        print(f"  {mark} 「{s}」… {'見ない' if skipped else '見る'}"
              f"（そうあるべき: {'見ない' if should_skip else '見る'}）")
    print(f"── {'✓ 道具は使える' if ok else '🔴 道具が壊れている。直してから使う'} ──\n")
    return ok


def main(only=None, do_check=False):
    if do_check and not selfcheck():
        return 1
    hits = scan(only)
    # 🔴 引用カットは「見出し＝決め所」で作られている（c217 c227 c228 c317 c325 c518）。
    #    quote 型は**決め所を画面に大きく出すのが役目**なので、見出しがそれと同じだと
    #    必ず二度出る。これは粗ではなく**作りの選択**なので、分けて出す。
    #    ⚠️ 直すなら6カットまとめて（見出しを「誰が・何について」に振り替える）。
    #      カズヤくんの判断が要るので、ここでは失敗にしない。
    def is_quote(cid):
        f = S.SPEC.get(cid, {}).get("fig")
        return bool(f) and f[0] == "quote"

    real = [h for h in hits if not is_quote(h[0])]
    design = [h for h in hits if is_quote(h[0])]
    for cid, kind, hv, layer, why in real:
        print(f"  🔴 {cid} {kind}「{hv}」\n      {why}  [{layer}]")
    if design:
        print("\n  ── 引用カット（見出し＝決め所）。**作りの選択**なので別扱い ──")
        for cid, kind, hv, layer, why in design:
            print(f"  ・ {cid} {kind}「{hv}」")
        print("     直すなら6カットまとめて、見出しを「誰が・何について」に振り替える。")
    print(f"\n{'🔴 同じ画面に同じ言葉が二度出ている' if real else '✓ 二重表示は無い'}"
          f"（直すもの {len(real)}件／引用の作り {len(design)}件）")
    return 1 if real else 0


if __name__ == "__main__":
    only = next((a.split("=")[1] for a in sys.argv if a.startswith("--only=")), None)
    sys.exit(main(only, "--check" in sys.argv))
