# -*- coding: utf-8 -*-
r"""el_artifacts.py — 合成音の「余計な音」を波形から見つける**純粋な関数**（2026-09-02 新設）。

  el_find_artifacts.py（CLI＝疑いを並べる道具）と el_tts.py（合成の中の門番＝検出→振り直し）の
  **両方がここを使う**。物差しを2か所に持たない（記憶: 測る小道具は1本にまとめる）。

⚠️ ここは el_tts / gen_audio を import しない（循環を避ける）。SR は 24000 固定。
   el_tts.SR と一致することは `python el_tts.py --selftest` が突き合わせる。

閾値の由来＝el_find_artifacts.py の 2026-08-26 の実測:
  - 本物の事故は s020=140ms（振幅31248・その行で最大）／s058=150ms／s054=80ms。**本文と同じかそれ以上に大きい**
  - 無音は 100ms しか無かった → TAIL_SILENCE=80ms（250ms にしていたら取り逃がした）
  - 本物の語尾「入っています。」は 430〜490ms が4回とも再現 → TAIL_BLIP=250ms 以下だけを候補に
  - 先頭は「ただし、」「つまり、」を拾うので 200ms まで

何が「振り直しの対象」か:
  kind = tail / head / mid（余計な音）→ 振り直す
  kind = gap（700ms 超の長い無音）→ 振り直さない。鉤括弧や溜めで説明がつくことが多い（ep007 s110）
"""
import struct

SR = 24000
WIN = SR // 100          # 10ms ごとに見る
LEVEL = 300              # これ未満を「無音」とみなす（el_tts.TRIM_LEVEL と同水準）
TAIL_SILENCE = 8         # 80ms
TAIL_BLIP = 25           # 250ms 以下の塊だけを「余計な音」の候補とする
HEAD_BLIP = 20           # 先頭は 200ms まで
MID_SILENCE = 70         # 700ms
RATIO = 0.9              # 本文の中央値の 0.9 倍以上の大きさ
BLIP_KINDS = ("tail", "head", "mid")


def envelope(pcm: bytes):
    """10ms ごとの最大振幅。"""
    n = len(pcm) // 2
    v = struct.unpack(f"<{n}h", pcm[: n * 2])
    out = []
    for i in range(0, n, WIN):
        w = v[i: i + WIN]
        out.append(max(abs(min(w)), abs(max(w))) if w else 0)
    return out


def runs(env):
    """[[loud?, 開始, 長さ], ...] に畳む。単位は 10ms。"""
    out = []
    for i, e in enumerate(env):
        loud = e >= LEVEL
        if out and out[-1][0] == loud:
            out[-1][2] += 1
        else:
            out.append([loud, i, 1])
    return out


def inspect_struct(pcm: bytes):
    """疑わしい所を構造で返す。各要素 = dict(kind, ms, at_ms, peak, ratio, before_ms, after_ms, msg)。"""
    env = envelope(pcm)
    r = runs(env)
    loud = [x for x in r if x[0]]
    if not loud:
        return [{"kind": "none", "ms": 0, "at_ms": 0, "peak": 0, "ratio": 0.0,
                 "before_ms": 0, "after_ms": 0, "msg": "音が見つからない"}]
    items = []
    body = sorted(e for e in env if e >= LEVEL)
    med = body[len(body) // 2] if body else 1
    if len(loud) >= 2:
        # ① 末尾のポツン。決め手は「大きさ」（減衰の尻尾を拾うと誤検知だらけになる）
        last = loud[-1]
        prev_gap = next((x for x in reversed(r) if x[1] < last[1] and not x[0]), None)
        if prev_gap and prev_gap[2] >= TAIL_SILENCE and last[2] <= TAIL_BLIP:
            peak = max(env[last[1]: last[1] + last[2]])
            ratio = peak / max(med, 1)
            if ratio >= RATIO:
                items.append({"kind": "tail", "ms": last[2] * 10, "at_ms": last[1] * 10,
                              "peak": peak, "ratio": ratio,
                              "before_ms": prev_gap[2] * 10, "after_ms": 0,
                              "msg": f"末尾に余計な音: {prev_gap[2]*10}ms の無音 → {last[2]*10}ms の音"
                                     f"（{last[1]*10/1000:.2f}秒地点・振幅{peak}＝本文の{ratio:.1f}倍）"})
        # ② 先頭のポツン（旧 CLI は大きさを見ていなかった。門番側は RATIO で絞る＝下の blips()）
        first = loud[0]
        next_gap = next((x for x in r if x[1] > first[1] and not x[0]), None)
        if next_gap and next_gap[2] >= TAIL_SILENCE and first[2] <= HEAD_BLIP:
            peak = max(env[first[1]: first[1] + first[2]])
            ratio = peak / max(med, 1)
            items.append({"kind": "head", "ms": first[2] * 10, "at_ms": first[1] * 10,
                          "peak": peak, "ratio": ratio,
                          "before_ms": 0, "after_ms": next_gap[2] * 10,
                          "msg": f"先頭に余計な音: {first[2]*10}ms の音（振幅{peak}＝本文の"
                                 f"{ratio:.1f}倍）のあと {next_gap[2]*10}ms の無音"})
    # ③ 文の途中に浮いた音（句点のあとの合間に紛れ込むやつ）
    for i, x in enumerate(r):
        if not x[0] or i == 0 or i == len(r) - 1:
            continue
        if x[2] > TAIL_BLIP:
            continue
        before, after = r[i - 1], r[i + 1]
        if before[0] or after[0]:
            continue
        if before[2] < TAIL_SILENCE or after[2] < TAIL_SILENCE:
            continue
        peak = max(env[x[1]: x[1] + x[2]])
        ratio = peak / max(med, 1)
        if ratio >= RATIO:
            items.append({"kind": "mid", "ms": x[2] * 10, "at_ms": x[1] * 10,
                          "peak": peak, "ratio": ratio,
                          "before_ms": before[2] * 10, "after_ms": after[2] * 10,
                          "msg": f"途中に浮いた音: {x[2]*10}ms（{x[1]*10/1000:.2f}秒地点・振幅{peak}"
                                 f"＝本文の{ratio:.1f}倍／前{before[2]*10}ms・後{after[2]*10}ms の無音）"})
    # ④ 途中の長すぎる無音（振り直しの対象ではない）
    for x in r:
        if not x[0] and x[2] >= MID_SILENCE and x[1] > 0 and x[1] + x[2] < len(env):
            items.append({"kind": "gap", "ms": x[2] * 10, "at_ms": x[1] * 10, "peak": 0, "ratio": 0.0,
                          "before_ms": 0, "after_ms": 0,
                          "msg": f"途中に {x[2]*10}ms の無音（{x[1]*10/1000:.2f}秒地点）"})
    return items


def inspect(pcm: bytes):
    """旧 CLI と同じ文字列の一覧（el_find_artifacts.py が使う）。"""
    return [x["msg"] for x in inspect_struct(pcm)]


def blips(items):
    """振り直しの対象＝余計な音（tail/head/mid）で、大きさが本文並み以上のもの。"""
    return [x for x in items if x["kind"] in BLIP_KINDS and x["ratio"] >= RATIO]


def signature(items):
    """テイク間で「同じ形か」を比べる指紋。kind と長さ（50ms 刻み）だけを見る。
    ⚠️ 3テイクとも同じ指紋なら偶発の混入ではなく本物の語（ep007 s110 の型）。"""
    return tuple(sorted((x["kind"], round(x["ms"] / 50)) for x in blips(items)))


def edge_fade(pcm: bytes, ms: int = 5) -> bytes:
    """行の頭と尻に直線フェード。長さは変えない。
    音をデジタル無音(0)に直接つなぐと、端のサンプルが 0 でないときに「プチ」というクリックが出る。
    5ms（120サンプル）は声には聞こえない長さ。"""
    n = len(pcm) // 2
    k = min(SR * ms // 1000, n // 2)
    if k <= 0:
        return pcm
    v = list(struct.unpack(f"<{n}h", pcm[: n * 2]))
    for i in range(k):
        g = i / k
        v[i] = int(v[i] * g)
        v[n - 1 - i] = int(v[n - 1 - i] * g)
    return struct.pack(f"<{n}h", *v)
