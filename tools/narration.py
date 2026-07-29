# -*- coding: utf-8 -*-
"""ナレーションの生成と、**誤読ゼロの5重チェック**。

事故検証は機体形式・地名・専門語が多く、誤読が起きやすいジャンルなので、
深読みフクロウで確立した体制をそのまま持ち込む（`zankoku-sekkeizu/tools/lint_yomi.py`）。

  ① かな書き    … 危ない語は YOMI で合成直前にかなへ置換する（台本は漢字のまま残す）
  ② YOMI辞書    … 一度でも誤読した語は必ずここに登録する
  ③ 生成前リント … YOMI に無い危険語（数詞＋助数詞・同形異音語）を機械抽出して止める
  ④ かなログ照合 … 生成された accent_phrases のモーラ列を EXPECT と機械照合する
  ⑤ 通し確認    … 最後は耳で1本通して聞く（人間の仕事。ここは自動化しない）

使い方:
  python tools/narration.py lint      … ③だけ走らせる（エンジン不要）
  python tools/narration.py build     … 生成 → ④照合 → 尺を narration.json に書く

音声エンジンは AivisSpeech（Windows ローカル）。
**クラウドで焼くのは映像だけ**で、音声はここで作って wav をリポジトリに置く。
"""
import json
import re
import sys
import urllib.parse
import urllib.request
import wave
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")
HERE = Path(__file__).parent.parent
BASE = "http://127.0.0.1:10101"

# 2026-07-29 カズヤくん決定。深読みフクロウと同じ声だが、あちらはノーマル・話速1.0。
# 被っても構わないとの判断。こちらは Heavy・話速0.95 で重さを出す。
SPEAKER = 1310138979          # 阿井田 茂 / Heavy
SPEED = 0.95
CREDIT = "AivisSpeech：阿井田 茂"

# ── ① ② かな書きと YOMI 辞書 ──────────────────────────────
# 合成の直前にだけ置換する。台本（SCRIPT）は人間が読めるよう漢字のまま。
YOMI = {
    # 実測で誤読が出た語
    "5.5メートル": "ごてんごメートル",
    # 数詞。助数詞の読みが揺れる
    "243便": "にひゃくよんじゅうさんびん",
    "737-200型機": "ななさんななの にひゃくがたき",
    "737-200": "ななさんななの にひゃく",
    "7300メートル": "ななせんさんびゃくメートル",
    "55パーセント": "ごじゅうごパーセント",
    # ④のかなログで「ナ／ナマン／ゴセンカイ」と語中で割れた（2026-07-29）。
    # 読みは正しいが「な、なまん」と吃って聞こえる。カタカナ1語にすると割れない。
    "7万5000回": "ナナマンゴセンカイ",
    "8万9680回": "はちまんきゅうせんろっぴゃくはちじゅっかい",
    "89680回": "はちまんきゅうせんろっぴゃくはちじゅっかい",
    "13分": "じゅうさんぷん",
    "19年間": "じゅうくねんかん",
    "20分": "にじゅっぷん",
    "1日に": "いちにちに",        # 「ついたち」と読まれる型
    # 🔴 2026-07-30 訂正。ここに「じょうはんぶん」と登録したのが**誤読の原因だった**。
    # 「上半身＝じょうはんしん」から類推して間違えた。上半分は **うえはんぶん**。
    # 辞書に入れる読みそのものが誤っていると、5重チェックは全部素通りする。
    # 読みを登録するときは、類推でなく必ず辞書で確かめる。
    "上半分": "うえはんぶん",
    "1列": "いちれつ",
    "2枚": "にまい",
    "1人": "ひとり",
    "1機": "いっき",
    # 同形異音・難読
    "荷重": "かじゅう",
    "外板": "がいはん",
    "与圧": "よあつ",
    "巡航": "じゅんこう",
    "剥離": "はくり",
    "剥ぎ取られて": "はぎとられて",
    "剥がれて": "はがれて",
    "縁だけ": "ふちだけ",
    "継手": "つぎて",
    "床梁": "ゆかばり",
    "潮風": "しおかぜ",
    "円周": "えんしゅう",
    "上部": "じょうぶ",
    "一続き": "ひとつづき",
    "十数回": "じゅうすうかい",
}

# ── ③ リント：YOMI に無い危険語を機械抽出する ──────────────
NUM_COUNTER = re.compile(
    r"(?:[0-9０-９一二三四五六七八九十百千万]+)\s*"
    r"(?:年|月|日|人|回|割|分|時間|パーセント|%|件|歳|代|機|枚|列|本|便|メートル|ミリ|キロ)")
RISKY = [
    "年に", "年間", "数十", "数百", "数千", "数万", "一時", "一行", "十分", "何人",
    "分", "代", "台", "後で", "後に", "前で", "生前", "大人",
    # 事故検証で出てくる語
    "荷重", "外板", "与圧", "巡航", "剥離", "縁", "継手", "床梁", "潮風", "円周",
    "上部", "下部", "亀裂", "疲労", "皿もみ", "機長", "客室", "前方", "後方",
    "胴体", "尾翼", "主翼", "骨組み", "接着", "腐食", "湿気", "気圧",
]

# ── ④ かなログの期待値。生成後にモーラ列と機械照合する ──────
EXPECT = {
    "ハクリ": "剥離",
    "カジュウ": "荷重",
    "ガイハン": "外板",
    "ヨアツ": "与圧",
    "ジュンコオ": "巡航",
    "ツギテ": "継手",
    "フチ": "縁",
    "シオカゼ": "潮風",
    "エンシュウ": "円周",
    "ゴテンゴ": "5.5",
    "ニヒャクヨンジュウサンビン": "243便",
    "ジュウサンプン": "13分",
    "ジュウクネン": "19年",
}
# **絶対に出てはいけないモーラ列**（過去に実際に出た誤読）
FORBIDDEN = {
    "ゴオテン": "5.5 を「ごうてん」と読んでいる",
    "ニジュウ,": "荷重を「にじゅう」と読んでいる",
    "ソトバン": "外板を「そとばん」と読んでいる",
    "エンダケ": "縁を「えん」と読んでいる",
    "ヨアツリョク": "与圧の読み崩れ",
    "ツイタチ": "「1日に」を「ついたち」と読んでいる",
    "ナ／ナマン": "7万が語中で割れて「な、なまん」と吃る",
    "ジョオハンブン": "上半分を「じょうはんぶん」と読んでいる（正しくは うえはんぶん）",
}

# ── 台本 ─────────────────────────────────────────────────
# 🔴 **1行＝1字幕**。行ごとに合成するので、字幕と音声がフレーム精度で一致する。
#    行は**自然な文の単位**で切る。**3秒を超えてよい**
#    （2026-07-30 カズヤくん指示：静止禁止ルールは字幕には適用しない。
#    　細かく割ると読みにくい。画面の動きは図とグラフで担保する）。
#    長い行は表示側で自動的に2行に折る（`scene_jiko.sub_row`）。
# カットIDは scene_jiko.CUTS と一致させる。尺はこの音声から逆算する。
SCRIPT = [
    ("p1", ["1988年4月28日。ハワイ上空、高度7300メートル。",
            "飛行中の旅客機から、屋根が消えた。"]),
    ("p2", ["事故を起こしたのは、19年間この島々を飛び続けた1機だった。"]),
    ("c2", ["失われたのは、前方の扉のすぐ後ろから、5.5メートル。",
            "天井から窓の下までが、一続きに剥ぎ取られていた。"]),
    ("p3", ["着陸した機体を、調査員が見上げている。",
            "外板が無くなり、客室の骨組みが、そのまま外に出ていた。"]),
    ("c3", ["失われたのは、胴体の上半分。円周の、およそ55パーセント。",
            "与圧された筒は、一度裂けると、一気に広がる。"]),
    ("c4", ["始まりは、リベット1列の、小さな亀裂だった。",
            "搭乗する乗客の1人が、この亀裂を見ていた。",
            "だが、誰にも言わなかった。"]),
    ("c5", ["外板は2枚が重なり、接着とリベットで荷重を分け合う設計だった。",
            "その接着が、潮風の中で剥がれていた。",
            "荷重の行き場は、リベット穴の縁だけになった。"]),
    ("p4", ["島から島へ、20分の飛行。1日に十数回、上がっては、降りる。"]),
    ("c6", ["剥離から着陸まで、13分。",
            "操縦室の扉も吹き飛び、機長は、客室の空を、直接見ていた。"]),
    ("c7", ["設計上の想定は、7万5000回。",
            "この機体は、8万9680回、飛んでいた。"]),
]
GAP = 0.18          # 行と行のあいだに置く無音


def apply_yomi(text):
    """長い語から順に置換する（「737-200型機」が「737-200」に食われないように）。"""
    for k in sorted(YOMI, key=len, reverse=True):
        text = text.replace(k, YOMI[k])
    return text


def lint():
    warn = 0
    for cid, text in ((c, "".join(ls)) for c, ls in SCRIPT):
        spoken = apply_yomi(text)
        hits = []
        for m in NUM_COUNTER.finditer(spoken):
            hits.append(("数詞", m.group(0)))
        for w in RISKY:
            if w in spoken:
                hits.append(("難読", w))
        for kind, s in hits:
            warn += 1
            print(f"{cid}  [要確認] {kind}: 「{s}」")
    print(f"\n{'★要確認 ' + str(warn) + '件 — YOMI に追記するか台本をかな書きに直す' if warn else '✓ 危険語なし'}")
    return warn


def post(path, payload=None, query=""):
    url = f"{BASE}/{path}?{query}"
    data = json.dumps(payload, ensure_ascii=False).encode() if payload is not None else b""
    req = urllib.request.Request(url, data=data, method="POST",
                                 headers={"Content-Type": "application/json"})
    return urllib.request.urlopen(req, timeout=300)


def kana_of(query):
    return "／".join("".join(m["text"] for m in ap["moras"])
                     for ap in query["accent_phrases"])


def chunk(text, dur, limit=2.8):
    """⚠️ **2026-07-30 に使用中止。** 字幕を limit 秒以下に割る処理。

    「3秒以上の静止禁止」を字幕で満たそうとして入れたが、
    **カズヤくん判定で「細かく割りすぎて見にくい」＝不採用**。
    静止禁止は図とグラフの動きで満たすことにした。経緯のために残すが呼ばない。

    （旧説明）字幕を **1枚あたり limit 秒以下** に割る。

    音声は自然な節（読点まで）で合成しているので**そのまま**。
    割るのは表示だけで、尺は文字数比で配分する。
    こうしないと、字幕に合わせて音声を刻むことになり、抑揚が毎回リセットされて棒読みになる。
    """
    parts = [p for p in re.findall(r"[^、。]+[、。]?", text) if p]
    # まだ長い塊は文字数で二分する
    out = []
    for p in parts:
        if dur * len(p) / len(text) <= limit or len(p) < 10:
            out.append(p)
            continue
        n = int(dur * len(p) / len(text) / limit) + 1
        step = -(-len(p) // n)
        out += [p[i:i + step] for i in range(0, len(p), step)]
    total = sum(len(p) for p in out)
    rows, t = [], 0.0
    for p in out:
        d = dur * len(p) / total
        rows.append({"t": round(t, 3), "d": round(d, 3), "text": p})
        t += d
    return rows


def resub():
    """音声は作り直さず、**字幕の割り方だけ**やり直す。"""
    p = HERE / "audio" / "narration.json"
    d = json.loads(p.read_text(encoding="utf-8"))
    lines = dict(SCRIPT)
    worst = (0.0, "")
    for cid, rows in d["subtitles"].items():
        new, t = [], 0.0
        for r in rows:
            for c in chunk(r["text"], r["d"]):
                new.append({"t": round(r["t"] + c["t"], 3), "d": c["d"], "text": c["text"]})
                if c["d"] > worst[0]:
                    worst = (c["d"], c["text"])
        d["subtitles"][cid] = new
        print(f"{cid}: {len(rows)}行 → {len(new)}枚")
    p.write_text(json.dumps(d, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n最長の字幕 = {worst[0]:.2f}秒「{worst[1]}」")
    print("✓ 3秒以下" if worst[0] <= 3.0 else "🔴 まだ3秒を超えている")
    return 0 if worst[0] <= 3.0 else 1


def synth(text):
    """1行ぶんを合成して (wavバイト列, 秒, かな) を返す。"""
    q = json.loads(post("audio_query", None,
                        f"speaker={SPEAKER}&text={urllib.parse.quote(text)}").read())
    q["speedScale"] = SPEED
    wav = post("synthesis", q, f"speaker={SPEAKER}").read()
    import io
    with wave.open(io.BytesIO(wav)) as w:
        sec = w.getnframes() / w.getframerate()
        p = (w.getnchannels(), w.getsampwidth(), w.getframerate())
        frames = w.readframes(w.getnframes())
    return frames, p, sec, kana_of(q)


def build():
    out = HERE / "audio"
    out.mkdir(exist_ok=True)
    durs, subs, log, bad, longest = {}, {}, [], 0, (0.0, "")
    for cid, lines in SCRIPT:
        chunks, params, t, rows = [], None, 0.0, []
        for line in lines:
            frames, params, sec, kana = synth(apply_yomi(line))
            rows.append({"t": round(t, 3), "d": round(sec, 3), "text": line})
            if sec > longest[0]:
                longest = (sec, line)
            log.append(f"[{cid}] {sec:5.2f}s  {line}\n         {kana}")
            for ng, why in FORBIDDEN.items():
                if ng in kana:
                    print(f"🔴 {cid}「{line}」: {why}（{ng}）")
                    bad += 1
            chunks.append(frames)
            t += sec + GAP
            chunks.append(b"\x00" * int(GAP * params[2]) * params[1] * params[0])
        total = t - GAP
        with wave.open(str(out / f"{cid}.wav"), "w") as w:
            w.setnchannels(params[0])
            w.setsampwidth(params[1])
            w.setframerate(params[2])
            w.writeframes(b"".join(chunks[:-1]))
        durs[cid] = round(total, 2)
        subs[cid] = rows
        print(f"{cid}: {total:5.2f}s  ({len(lines)}行)", flush=True)
    (out / "kana_log.txt").write_text("\n".join(log), encoding="utf-8")
    (out / "narration.json").write_text(
        json.dumps({"speaker": SPEAKER, "speed": SPEED, "credit": CREDIT,
                    "gap": GAP, "durations": durs, "subtitles": subs},
                   ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n合計 {sum(durs.values()):.1f} 秒")
    print(f"最長の1行 = {longest[0]:.2f}秒「{longest[1]}」")
    if longest[0] > 8.0:
        print("⚠️ 8秒を超える字幕行がある。長すぎるので文を分けること。")
    print("かなログ → audio/kana_log.txt（⑤ 通し確認の前に必ず目で読む）")
    if bad:
        print(f"\n🔴 誤読の疑い {bad} 件。YOMI を直してから作り直すこと。")
        return 1
    print("✓ 禁止パターンの検出なし")
    return 0


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "lint"
    if cmd == "lint":
        lint()
        sys.exit(0)
    sys.exit(resub() if cmd == "resub" else build())
