# -*- coding: utf-8 -*-
"""18本目 ⑥：⑤b-7 で動画に加わった画面の**本番の時刻（分:秒）と秒**を、焼いた版の設計（scene_jiko.CUTS）から機械で出す。

台帳＝Vault `事故検証-18本目-⑤b-7で動画に加わった変更-台帳-20261005` §5（0.＝新しく加わった工程で変わった所を元からの予定と分けて／
1.＝工程ごとの時刻と割合）。**手で足さない**（§5 の 1.）。r01（Modal・`f8f92f2`）の mp4 の尺 2281.0 秒＝設計と一致（check_final）。

    python qa_out/ep18_b7_times.py         → 表（Markdown）を標準出力へ

数え方：
  - カットの「中身」＝扉（章の頭の2秒）を除いた区間。時刻は中身の始まり（＝動画でそこへ飛べる形）
  - 頭の差し込み（映像）＝中身の始まり〜 `head_secs`／尻の差し込み（写真・頁）＝`ins_sec(at)`〜中身の終わり
  - まるごと映像に替えたカット（②）＝映像の区間の長さ（使う区間 ÷ 速さ）
  - 合計は**区間の和**（同じ秒を二重に数えない）
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
sys.stdout.reconfigure(encoding="utf-8")
import cuts  # noqa: E402
import footage as F  # noqa: E402
import scene_jiko as S  # noqa: E402

START, T = {}, 0.0
for _c, _s in S.CUTS:
    START[_c] = T
    T += _s
DUR = dict(S.CUTS)
TOTAL = T

# §0 新しく加わった工程（10-04 の決定＝映像方針 §16・§17）
NEW2 = ["c212", "c301", "c601", "cb01"]                       # ② 記録映画のコマ（静止画）→ 同じ映画の動く映像
NEW3 = ["c109", "c114", "c215", "c220", "c511", "c805", "c812", "c903", "c906", "ca05", "ca06"]   # ③ フリー素材の頭
WHAT = {
    "c109": "意見書の頁 → 頭の1行だけフリー素材（書類の綴じ込み）→ 頁",
    "c114": "艦首の写真 → 頭だけフリー素材（水の中から見上げた光）",
    "c212": "記録映画の静止画 → 同じ映画の動く映像（雲の下を走る艦）",
    "c215": "就役の直前の写真 → 頭だけフリー素材（桟橋の杭と海面）",
    "c220": "走るスレッシャーの写真 → 頭だけフリー素材（桟橋の下の海面）",
    "c301": "記録映画の静止画 → 動く映像（岸を背に走る艦）",
    "c511": "スカイラークの写真 → 頭だけフリー素材（暗い沖の海面）",
    "c601": "記録映画の静止画 → 動く映像（セイルの「593」・⑤c' で区間を選び直した）",
    "c805": "外殻の写真 → 頭だけフリー素材（水の中の太陽）",
    "c812": "切れた船体の写真 → 頭だけフリー素材（光の筋）",
    "c903": "書簡の頁 → 頭だけフリー素材（タイプライターの活字）",
    "c906": "海の底のセイルの写真 → 頭だけフリー素材（カードを繰る手・⚠️ 寄せすぎは据え置き）",
    "ca05": "外殻の板の写真 → 頭だけフリー素材（砂の海底）",
    "ca06": "破片の写真 → 頭だけフリー素材（砂の動く海の底）",
    "cb01": "記録映画の静止画 → 動く映像（セイルの上の乗員・⑤c' で副題に「（事故の前）」）",
}
# 元からの予定（10-01 の映像方針 §13・§1-3）＝台帳 §2〜§4 のカット
P7A = ("c114 c116 c201 c203 c208 c215 c220 c423 c611 c627 c709 cb23 c212 c301 c601 cb01 c304 c306 c415 c511 c523 "
       "c722 c805 c812 c819 c822 c906 c911 c914 c920 ca05 ca06 ca13 ca20 ca10 ca11 ca14 ca17 ca18 cb09").split()
P7B = "c105 c109 c303 c307 c316 c414 c508 c516 c623 c712 c721 c814 c903 c905 c909 c910 ca15 cb12 cb21 cb22".split()
P7C = "c117 c202 c506 c514 c515 c607 c621 c701 ca01 ca03 ca07 ca08 ca09 ca12 cb07 cb14 cb19".split()
HEAD_FILM = ["c102"]
TAILS = ["c103", "c105", "cb21"]


def body(cid):
    c = S.card_of(cid)
    return START[cid] + c, DUR[cid] - c


def head(cid):
    h = S.head_secs(cid)
    return h or 0.0


def vid(cid):
    u = F.USE[cid]
    return (u["until"] - u["start"]) / u.get("rate", 1.0)


def tail_iv(cid):
    b0, bd = body(cid)
    at = int(cuts.SPEC[cid]["tail"]["at"])
    return b0 + S.ins_sec(cid, at), b0 + bd


def mmss(x):
    return f"{int(x // 60)}:{int(x % 60):02d}"


def union(ivs):
    tot, cur = 0.0, None
    for a, b in sorted(ivs):
        if cur is None or a > cur[1]:
            if cur:
                tot += cur[1] - cur[0]
            cur = [a, b]
        else:
            cur[1] = max(cur[1], b)
    return tot + ((cur[1] - cur[0]) if cur else 0.0)


def main():
    assert len(P7A) == 40 and len(P7B) == 20 and len(P7C) == 17, (len(P7A), len(P7B), len(P7C))
    print(f"本番 r01 の尺（設計）＝{TOTAL:.1f} 秒＝{mmss(TOTAL)}\n")
    print("### A. 🆕 新しく加わった工程（10-04 の決定）で変わった所＝本番の時刻\n")
    print("| 時刻 | カット | 変わる前 → 変わったあと | 工程 | 秒 |\n|---|---|---|---|---:|")
    rows, s2, s3, ivn = [], 0.0, 0.0, []
    for c in NEW2 + NEW3:
        b0, bd = body(c)
        if c in NEW2:
            sec, kind = vid(c), "② 動く映像"
            s2 += sec
        else:
            sec, kind = head(c), "③ フリー素材の頭"
            s3 += sec
        ivn.append((b0, b0 + sec))
        rows.append((b0, c, WHAT[c], kind, sec))
    for b0, c, w, k, sec in sorted(rows):
        print(f"| {mmss(b0)} | {c} | {w} | {k} | {sec:.1f} |")
    print(f"\n- 合計＝② {len(NEW2)}か所 **{s2:.1f}秒**・③ {len(NEW3)}か所 **{s3:.1f}秒**＝**{s2 + s3:.1f}秒"
          f"（{(s2 + s3) / 60:.0f}分{(s2 + s3) % 60:02.0f}秒）＝全長の {100 * (s2 + s3) / TOTAL:.1f}%**")
    print("- ① NARA の動く記録映像の再調査＝見つからず（画面の変化0）／④ フリー素材の門番＝数え方だけ（画面の変化0）\n")

    print("### B. ⑤b-7 で加わった画面（元からの予定を含む全部）＝本番の秒と割合\n")
    print("| 中身 | カット | 画面の秒 | 全長に対して |\n|---|---:|---:|---:|")
    cats, allv = [], []
    iv7a = [(body(c)[0] + head(c), sum(body(c))) for c in P7A]
    iv7b = [(body(c)[0] + head(c), sum(body(c))) for c in P7B]
    iv7c = [(body(c)[0], sum(body(c))) for c in P7C]
    ivh = [(body(c)[0], body(c)[0] + head(c)) for c in NEW3 + HEAD_FILM]
    ivt = [tail_iv("c103")]                                 # c105・cb21 の尻は頁のカット（7b）の中＝二重に数えない
    for name, n, ivs in (("7a 写真（うち4カットは ② で動く映像）", 40, iv7a), ("7b 頁（本物の記録の頁）", 20, iv7b),
                         ("7c 記録映画（画面が無かったカット）", 17, iv7c),
                         ("7c 頭の差し込み（フリー素材11＋記録映画1）", 12, ivh),
                         ("7c 尻の差し込み（c103 の写真・c105／cb21 の頁は 7b の内）", 3, ivt)):
        u = union(ivs)
        allv += ivs
        print(f"| {name} | {n} | {u:.1f}（{int(u // 60)}分{u % 60:04.1f}秒） | {100 * u / TOTAL:.1f}% |")
    ua = union(allv)
    print(f"| **合計（区間の和）** | | **{ua:.1f}（{int(ua // 60)}分{ua % 60:04.1f}秒）** | **{100 * ua / TOTAL:.1f}%** |")
    un = union(ivn)
    print(f"\n- うち新しい工程（A）＝{un:.1f}秒（{100 * un / TOTAL:.1f}%）・元からの予定＝{ua - un:.1f}秒"
          f"（{100 * (ua - un) / TOTAL:.1f}%）")


if __name__ == "__main__":
    main()
