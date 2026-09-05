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

■ 🔴 2026-09-06 に足した3つ（サーフサイド ⑤c の目視で素通りした形。型カットを目視しない案2の目）
  ① timeline の**目盛りの札**と**旗（top／t2）**が同じ語（c201「3週間前」・c218「9時間前」・c228「9分前」「崩落」）
     → 目盛りは日付か素の数字にする。旗はそのまま
  ② **副題（s）と図の札が同じ語**を持つ（4字以上の語、または3字以上の丸ごとの区切り）
     （c314 s「押し抜きの場合」× lead「押し抜きが起きたとき」／c309 s「…すり鉢を伏せた形の破壊面」×
     札「破壊面（すり鉢を伏せた形）」／c304 s「…（模式図・寸法なし）」× note「…（模式図）」）
     ⚠️ 7割の「覆う」規則はいちばん長い一致1つで測るので、語が2つに割れると 57% で黙っていた
     ⚠️ カタカナ1語・数字と単位・ひらがなだけの並び（「ている」）は語と見なさない
  ③ **制作の用語**が画面の文字にある（「次のカット」「ナレーション」「字幕」「台本」…）

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
                     r"週間か前後ごろ午初旬中末"          # 「3週間前」「1か月前」「6月初旬」＝時の語（副題の役目）
                     r"メートルインチフィートポンドマイルパーセントキロセンチミリ"   # 単位
                     r"／/・:：〜~\-−－(（)）]+$")

# 「見出し／副題に出てよい」語。図がラベルとして持つのが当たり前のもの。
# ⚠️ ここを広げすぎると道具が何も言わなくなる。**固有名詞1語だけ**に絞る。
KATAKANA1 = re.compile(r"^[ァ-ヶー]+$")
HIRAGANA = re.compile(r"^[ぁ-ゖー]+$")          # 助詞・活用語尾の並び。語ではない
WORDLEN = 4                                       # 副題と札の「同じ語」と見なす最短
SEGLEN = 3                                        # 丸ごとの区切り（「模式図」）ならここまで短くてよい
SEG = re.compile(r"[　 ・（）()／/、。:：=＝⇄→※]+")  # 副題・札を「区切り」に割る記号
PARTICLE = "のはがをにでともへやてっ"                 # 一致の両端に付いた助詞は語の一部でない
MARKER = re.compile(r"^\d+\s*/\s*\d+$")           # 章マーカー「3 / 7」
# 視聴者の画面に出てはいけない制作の用語（c312 c213「次のカット」で実際に出た）
PRODUCTION = re.compile(r"次のカット|前のカット|カット|ナレーション|字幕|台本|テロップ|レイヤー")


def frame_texts():
    """図の中の文字ではない、枠の文字（章名）。副題との同語の対象から外す。"""
    return {norm(v[1]) for v in getattr(S, "CHAPTERS", {}).values()}


def wordish(w):
    """比べてよい語か（数字と単位だけ・カタカナ1語・ひらがなだけの並びは語と見なさない）。"""
    return (len(w) >= WORDLEN and not DATAISH.match(w) and not KATAKANA1.match(w)
            and not HIRAGANA.match(w))


def segments(s):
    return {norm(x) for x in SEG.split(str(s)) if norm(x)}


def shared_word(a, b):
    """副題 a と札 b（生の文字列）が持つ同じ語。(語, "hard"|"soft") か None。

    hard … **どちらかの区切りを丸ごと**写している（札「コア抜き」が副題「コア抜き（記録映像）」に丸ごと／
           副題の「模式図」が note にも）。これは c310 と同じ「同じ文字列が2か所」＝直す
    soft … 語の一部だけ重なる（「集まる力」「錆び続け」）。--all で見せる参考。直すかは判断
    ① いちばん長い連続一致の両端の助詞を落とし、WORDLEN 字以上で語らしい → その語
    ② 区切りで割った片が丸ごと一致（SEGLEN 字以上・数字と単位だけでない） → その片（hard）
    """
    an, bn = norm(a), norm(b)
    sa, sb = segments(a), segments(b)
    best = ""
    for i in range(len(bn)):
        for j in range(i + WORDLEN, len(bn) + 1):
            w = bn[i:j]
            if j - i > len(best) and w in an:
                best = w
    best = best.strip(PARTICLE)
    if best and wordish(best):
        return best, ("hard" if best in sa or best in sb else "soft")
    for w in sorted(sa & sb, key=len, reverse=True):
        if len(w) >= SEGLEN and not DATAISH.match(w) and not KATAKANA1.match(w) \
                and not HIRAGANA.match(w):
            return w, "hard"
    return None


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


def span(h, n):
    """ラベル `n` が見出し `h` のどこを覆っているか（連続一致の最長）。無ければ None。

    🔴 2026-08-02：**「どちらかがどちらかの部分文字列」で見ていたので取り逃していた。**
       quote の決め所は幅で折り返され、レイヤーに別々の <text> として入る。
         c516 … 見出し「受け台の中でずれた」／決め所は
                '金属の受け台の' ＋ '中でずれた' の2行
         '金属の受け台の' はどちらの向きでも部分文字列にならないので**丸ごと捨てられ**、
         '中でずれた' だけが当たって 56%。しきい値70%に届かず**黙っていた**。
       → 部分文字列かどうかでなく、**連続一致した部分がどこを覆ったか**で測る。
         上の例は '受け台の'(0-4) ＋ '中でずれた'(4-9) で 9/9 ＝ 100%。
       ⚠️ 「見出しの一部を図が数値として出す」設計（c113a）は覆う割合が
         70%に届かないので、これまでどおり黙る。
    """
    best = (0, 0)
    for i in range(len(n)):
        for j in range(i + MINLEN, len(n) + 1):
            k = h.find(n[i:j])
            if k >= 0 and j - i > best[0]:
                best = (j - i, k)
    return None if best[0] < MINLEN else (best[1], best[1] + best[0])


def scan(only=None):
    bycut = collect(only)
    frame = frame_texts()
    hits, softs = [], []
    for cid in sorted(bycut):
        spec = S.SPEC.get(cid, {})
        heads = [("見出し", str(spec.get("t", "") or "")),
                 ("副題", str(spec.get("s", "") or ""))]
        heads = [(kind, v) for kind, v in heads if norm(v)]

        # ── ③ 制作の用語（見出し・副題・図のどこに出ても言う） ──
        for layer, t in bycut[cid]:
            m = PRODUCTION.search(t)
            if m:
                hits.append((cid, "制作用語", t, layer,
                             f"視聴者の画面に制作の用語「{m.group(0)}」"))

        # ── ① timeline の目盛りの札 と 旗（top／t2）の同語 ──
        fig = spec.get("fig")
        if fig and fig[0] == "timeline":
            ticks = {norm(lbl) for _, lbl in fig[1].get("ticks", []) if norm(lbl)}
            for ev in fig[1].get("events", []):
                for key in ("top", "t2"):
                    v = str(ev.get(key, "") or "")
                    if len(norm(v)) >= 2 and norm(v) in ticks:
                        hits.append((cid, "目盛り", v, "timeline",
                                     f"軸の目盛りの札と旗の {key} が同じ語＝目盛りを日付か素の数字にする"))

        if not heads:
            continue
        # ── ② 副題 と 図の札 の同語 ──
        sv = str(spec.get("s", "") or "")
        if norm(sv):
            hn = {norm(v) for _, v in heads}
            found = {}
            for layer, t in bycut[cid]:
                n = norm(t)
                if not n or n in hn or n in frame or t.startswith("出典") or MARKER.match(t):
                    continue
                got = shared_word(sv, t)
                if got:
                    w, grade = got
                    found.setdefault((w, grade), []).append(t)
            for (w, grade), ts in found.items():
                row = (cid, "副題", sv, "同語",
                       f"図の札「{ts[0]}」{'ほか' + str(len(ts) - 1) + 'か所' if len(ts) > 1 else ''}"
                       f"と同じ語「{w}」＝"
                       + ("札か副題の区切りを丸ごと写している。副題を「何を見ている図か」に"
                          if grade == "hard" else "語の一部が重なる（参考）"))
                (hits if grade == "hard" else softs).append(row)
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
                sp = span(h, n)
                if sp:
                    cover[kind].setdefault(hv, []).append((t, sp, layer))
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
                for t, sp, layer in got:
                    covered.update(range(*sp))
                r = len(covered) / len(h) if h else 0
                if r >= 0.70:
                    hits.append((cid, kind, hv, got[0][2],
                                 f"図のラベル {'／'.join(t for t, _, _ in got)} が"
                                 f"{r:.0%}を覆う＝{kind}が図の写しになっている"))
    scan.softs = softs
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
        sp = span(h, n)
        if sp:
            got.update(range(*sp))
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
        # 🔴 2026-08-02 追加：**折り返しで割れた決め所**（c516 で実際に起きた形）。
        #    行ごとに部分文字列で見ていたころは '金属の受け台の' が丸ごと捨てられ、
        #    56% で黙っていた。割れる位置しだいで見つかったり見つからなかったりする、
        #    という**逆の道具**だった。
        ("決め所が折り返しで2行に割れている（c516 で実際に起きた形）",
         "受け台の中でずれた", ["金属の受け台の", "中でずれた"], True),
        # 折り返しても、**設計どおり数値だけを出している**場合は黙るままであること
        ("折り返した札が数値だけを出す（**直さない**）",
         "毎分33メートルで降りていた", ["毎分33", "メートル"], False),
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

    # 🔴 2026-09-06 追加：副題と札の同語（②）。⑤c で実際に目視で出た形と、黙るべき形
    words = [
        ("s と lead が同じ4字の語（c314 の形）", "押し抜きの場合", "押し抜きが起きたとき", "押し抜き"),
        ("語が2つに割れて7割に届かない（c309 の形）", "段6　すり鉢を伏せた形の破壊面",
         "破壊面（すり鉢を伏せた形）", "すり鉢を伏せた形"),
        ("3字の丸ごとの区切り（c304 の形）", "押し抜きせん断の断面　段1（模式図・寸法なし）",
         "柱の上に置かれているのではなく、つながっている（模式図）", "模式図"),
        ("カタカナ1語は部位名（**黙る**）", "プールデッキ上の位置（p57）", "プールデッキ", None),
        ("数字と単位だけ（**黙る**）", "2021年6月23日 朝　NIST の3D（p57）", "6月23日", None),
        ("ひらがなの並び（**黙る**）", "書き手が否定したこと（p58）", "したことで、ものが", None),
        ("2字の語（**黙る**）", "崩落までの時間", "崩落", None),
    ]
    for name, s, label, want in words:
        got = shared_word(s, label)
        w = got[0] if got else None
        mark = "✓" if w == want else "✗"
        if w != want:
            ok = False
        print(f"  {mark} {name}\n      「{s}」×「{label}」→ "
              f"{'「' + w + '」を言う（' + got[1] + '）' if got else '黙る'}"
              f"（そうあるべき: {'「' + want + '」を言う' if want else '黙る'}）")
    # 制作の用語（③）
    for s, should in [("曲げ破壊との違いは次のカット", True), ("書かれていたものは、次のカットで", True),
                      ("カッターで切った断面", False), ("字幕帯", True), ("押し抜き（punching）", False)]:
        hit = bool(PRODUCTION.search(s))
        mark = "✓" if hit == should else "✗"
        if hit != should:
            ok = False
        print(f"  {mark} 制作用語「{s}」… {'言う' if hit else '黙る'}"
              f"（そうあるべき: {'言う' if should else '黙る'}）")
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

    def is_design(h):
        # 引用カットの「見出し／副題＝決め所」（覆う規則）だけが作りの選択。①②③は引用でも直す
        return is_quote(h[0]) and h[1] in ("見出し", "副題") and "覆う" in h[4]

    real = [h for h in hits if not is_design(h)]
    design = [h for h in hits if is_design(h)]
    for cid, kind, hv, layer, why in real:
        print(f"  🔴 {cid} {kind}「{hv}」\n      {why}  [{layer}]")
    softs = getattr(scan, "softs", [])
    if softs and "--all" in sys.argv:
        print("\n  ── 副題と札で語の一部が重なる（参考。直すかは判断） ──")
        for cid, kind, hv, layer, why in softs:
            print(f"  ・ {cid} {kind}「{hv}」 {why}")
    if design:
        print("\n  ── 引用カット（見出し＝決め所）。**作りの選択**なので別扱い ──")
        for cid, kind, hv, layer, why in design:
            print(f"  ・ {cid} {kind}「{hv}」")
        print("     直すなら6カットまとめて、見出しを「誰が・何について」に振り替える。")
    print(f"\n{'🔴 同じ画面に同じ言葉が二度出ている' if real else '✓ 二重表示は無い'}"
          f"（直すもの {len(real)}件／引用の作り {len(design)}件／語の一部の重なり {len(softs)}件）")
    if softs and "--all" not in sys.argv:
        print("   （語の一部の重なりは --all で出る）")
    return 1 if real else 0


if __name__ == "__main__":
    only = next((a.split("=")[1] for a in sys.argv if a.startswith("--only=")), None)
    sys.exit(main(only, "--check" in sys.argv))
