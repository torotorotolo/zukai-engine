# -*- coding: utf-8 -*-
"""19本目①棚卸し：旧版（4本目サーフサイド・2026-09-06 公開）の台本と数を、git の版から機械で書き出す。

**手で写さない**ための道具。リポの作業ツリーには何も書かない（書くのはこのフォルダの3ファイルだけ）。
git は読むだけ（`ls-tree` と `cat-file` しか呼ばない）。

使い方（リポの直下で）:
    python ref/ep19/old/dump_old.py                      # 既定 --rev e6fe892
    python ref/ep19/old/dump_old.py --work <一時フォルダ>   # 写しの置き場（既定は OS の一時フォルダ）

なぜ e6fe892 か（詳細は ref/ep19/old_script_inventory.md §1）:
    公開したファイル out/jiko/titan_audio-ss2.mp4 の絵は検品画像 ss-r05（6562a17）と同じ版、
    音は a77ddc4 の audio_mix.py で混ぜ直したもの。6562a17〜e6fe892 のあいだに
    tools/narration.py・audio/narration.json・tools/cuts/・tools/footage.py・tools/scene_jiko.py は変わっていない。
    e6fe892 は ⑥の最後の commit（要耳一覧の最終版を含む）。

書き出すもの（このフォルダ）:
    old_script_published.md … 台本（章・カットID・秒・行・★決め所・画と出典の欄・画面の出典行）
    old_screen_text.md      … カットごとの「画面の文字」（描かれる全レイヤーの文字。check_dup.collect と同じ取り方）
    old_metrics.json        … 数（old_script_inventory.md の表のもと）
"""
import argparse
import json
import os
import re
import subprocess
import sys
import tempfile
from collections import Counter, OrderedDict
from pathlib import Path

HERE = Path(__file__).resolve().parent          # ref/ep19/old
REPO = HERE.parents[2]                           # リポの直下
PATHS = ["tools", "ref/surfside", "fonts", "audio/narration.json", "audio/el_qa"]

# 「句読点なし」＝チャンネルの数え方（tools/aq_build.py の PUNCT・ルール §5a-28）
PUNCT_CH = re.compile(r"[、。？！「」（）・]")
# 広い数え方（記号をほぼ全部除く）。ー（長音）・数字・英字・－（ハイフン）は字に数える
PUNCT_EXT = re.compile(r"[、。，．,.？！?!「」『』（）()・…‥：:；;“”\"'〜~―—─\s　]")

# 文字だけの画面（ルール：パネル・決め所・報告書の文字の頁）
TEXT_FIG_A = {"panel", "quote"}
TEXT_FIG_B_EXTRA = {"absent", "beforeafter", "process"}      # 文字の箱が主体の型（広い数え方だけ）
TEXT_SLIDES = {"surfside/tf_p016_q.jpg", "surfside/tf_p086_causes.jpg",
               "surfside/tf_p189_not.jpg", "surfside/tf_p191_closing.jpg"}
UNSURE_SLIDES = {"surfside/tf_p185_87park.jpg"}               # 文字が主か図があるか、文字の情報だけでは決まらない

YP_UNITS = ["平方フィート", "フィート", "インチ", "ポンド", "psi", "PSI", "マイル", "ヤード",
            "華氏", "°F", "ガロン", "エーカー", "ft", "in."]
METRIC = re.compile(r"(センチ|ミリ|メートル|キロ|平方メートル|メガパスカル|MPa|トン|℃|cm|mm|\bm\b|kg|㎝|㎜)")
DEATH = ["死亡", "亡くな", "犠牲", "遺体", "死者", "死ん", "命を落と", "遺族", "亡骸", "即死", "絶命", "死去", "殺"]
TIME_PATS = OrderedDict([
    ("午前/午後N時N分", re.compile(r"(午前|午後)\s*\d{1,2}時\d{1,2}分")),
    ("午前/午後N時（分なし）", re.compile(r"(午前|午後)\s*\d{1,2}時(?!\d)")),
    ("N時N分（午前午後なし）", re.compile(r"(?<![前後])\d{1,2}時\d{1,2}分")),
    ("H:MM / HH:MM（コロン）", re.compile(r"(?<![\d:])\d{1,2}:\d{2}(?::\d{2})?(?![\d:])")),
    # 報告書の4桁（0122・0125:59 など）。年（2021 など）を拾わないよう、後ろに時刻の印があるものだけ
    ("4桁の時刻（0122 など）", re.compile(r"(?<![\d年])[0-2]\d[0-5]\d(?=(:\d{2})?\s*(時|EDT|EST|Z|ごろ|頃))")),
])
RUMOR = ["地盤", "沈下", "陥没", "シンクホール", "87", "パーク", "工事", "振動", "塩", "海水", "海面",
         "ハリケーン", "高潮", "屋根", "噂", "言われ", "報じ", "うわさ", "通説", "雷", "テロ", "爆"]


def git(*a, binary=False):
    r = subprocess.run(["git", "-C", str(REPO), *a], capture_output=True, check=True)
    return r.stdout if binary else r.stdout.decode("utf-8")


def extract(rev, work):
    names = [n for n in git("ls-tree", "-r", "-z", "--name-only", rev, "--", *PATHS).split("\0") if n]
    for n in names:
        p = work / n
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(git("cat-file", "-p", f"{rev}:{n}", binary=True))
    return len(names)


def mmss(t):
    t = round(t, 1)                     # 先に丸める（59.96 秒が「:60.0」にならないように）
    m, s = divmod(t, 60)
    return f"{int(m)}:{s:04.1f}"


def parse_script_comments(src):
    """SCRIPT の中のコメント（章の見出し・カットごとの画と出典の欄）を拾う。"""
    lines = src.splitlines()
    i0 = next(i for i, l in enumerate(lines) if l.startswith("SCRIPT = ["))
    i1 = next(i for i in range(i0 + 1, len(lines)) if lines[i].startswith("]"))
    hdr, notes, pend, cur = {}, {}, [], None
    for l in lines[i0 + 1:i1]:
        s = l.strip()
        m = re.match(r"#\s*──\s*(.+?)\s*─{2,}", s)
        if m:
            cur, pend = m.group(1), []
            continue
        if s.startswith("#"):
            pend.append(s.lstrip("#").strip())
            continue
        m = re.match(r'\("([a-z]{1,2}\d{2,3})",', s)
        if m:
            cid = m.group(1)
            notes[cid], pend = pend, []
            if cur:
                hdr[cid], cur = cur, None
    return hdr, notes


def analyze(work, rev):
    sys.path.insert(0, str(work / "tools"))
    os.chdir(work)
    import narration as N           # noqa: E402
    import scene_jiko as S          # noqa: E402
    import footage as FO            # noqa: E402
    import check_dup as D           # noqa: E402

    script = OrderedDict(N.SCRIPT)
    order = list(S.ORDER)
    assert list(script) == order, "SCRIPT と narration.json の並びが違う"
    for c in order:
        got = [r["text"] for r in S.SUBS[c]]
        assert got == list(script[c]), f"{c}: 字幕と SCRIPT が違う"
    length = dict(S.CUTS)
    nj = json.loads((work / "audio" / "narration.json").read_text(encoding="utf-8"))
    dur = nj["durations"]
    start, t = {}, 0.0
    for c in order:
        start[c] = t
        t += length[c]
    total = t
    speech = sum(dur[c] for c in order)
    hdr, notes = parse_script_comments((work / "tools" / "narration.py").read_text(encoding="utf-8"))

    SPEC, USE = S.SPEC, FO.USE
    moving = [c for c in order if c in USE and not USE[c].get("still")]
    still_fb = [c for c in order if c in USE and USE[c].get("still")]

    def kind(c):
        sp = SPEC[c]
        if sp.get("photo") and not sp.get("fig"):
            return "photo"
        return sp["fig"][0] + ("+写真" if sp.get("photo") else "")

    def picture(c):
        sp = SPEC[c]
        if c in USE:
            u = USE[c]
            cl = FO.CLIPS[u["clip"]]
            if u.get("still"):
                return f"記録映像 {u['clip']} の {u['start']}秒の1コマ（静止画・{sp.get('photo')}）"
            extra = []
            if "rate" in u:
                extra.append(f"rate {u['rate']}")
            if "until" in u:
                extra.append(f"until {u['until']}")
            return f"記録映像（動く）{u['clip']} {u['start']}秒〜（{'・'.join(extra) or '等速'}）{cl['w']}x{cl['h']}"
        ph = sp.get("photo")
        if ph:
            m = re.match(r"surfside/tf_p(\d{3})_", ph)
            if m:
                base = f"NIST 技術的知見 スライド p{int(m.group(1))}（{ph}）"
            else:
                base = f"記録映像の1コマ（静止画・{ph}）"
            if sp.get("fig"):
                return f"図 {sp['fig'][0]}＋地に写真 {base}"
            return base
        return f"図 {sp['fig'][0]}"

    bycut = D.collect()
    screen = {}
    for c in order:
        seen = []
        for _lay, tx in bycut.get(c, []):
            if tx not in seen:
                seen.append(tx)
        screen[c] = seen

    def credit_line(c):
        if c in moving:
            return FO.credit_of(c)
        cr = [x for x in screen[c] if x.startswith("出典：")]
        return " ／ ".join(cr) if cr else ""

    def chap_key(c):
        if c.startswith("pr"):
            return "pr"
        if c.startswith("ep"):
            return "ep"
        return c[:2]

    chap_name = {"pr": "プロローグ", "ep": "エピローグ"}
    for k, (n, nm) in S.CHAPTERS.items():
        chap_name[k] = f"第{n}章 {nm}"

    def is_text(c, broad):
        sp = SPEC[c]
        f = sp.get("fig", (None,))[0] if sp.get("fig") else None
        if f in TEXT_FIG_A:
            return True
        if not sp.get("fig") and sp.get("photo") in TEXT_SLIDES:
            return True
        if broad and f in TEXT_FIG_B_EXTRA:
            return True
        return False

    def runs(flags):
        out, cur = [], []
        for c in order:
            if flags[c]:
                cur.append(c)
            else:
                if len(cur) >= 3:
                    out.append(cur)
                cur = []
        if len(cur) >= 3:
            out.append(cur)
        return out

    # ── 数 ─────────────────────────────────────────────
    all_lines = [(c, i, x) for c in order for i, x in enumerate(script[c])]
    ch_all = sum(len(x) for _, _, x in all_lines)
    ch_np = sum(len(PUNCT_CH.sub("", x)) for _, _, x in all_lines)
    ch_np2 = sum(len(PUNCT_EXT.sub("", x)) for _, _, x in all_lines)

    chapters = []
    for key in ["pr"] + sorted(S.CHAPTERS) + ["ep"]:
        cs = [c for c in order if chap_key(c) == key]
        if not cs:
            continue
        chapters.append(dict(
            key=key, name=chap_name[key], first=cs[0], last=cs[-1], n_cuts=len(cs),
            start=round(start[cs[0]], 2), sec=round(sum(length[c] for c in cs), 2),
            n_lines=sum(len(script[c]) for c in cs),
            chars_nopunct=sum(len(PUNCT_CH.sub("", x)) for c in cs for x in script[c]),
            photo=sum(1 for c in cs if SPEC[c].get("photo")),
            footage_moving=sum(1 for c in cs if c in moving),
            text_A=sum(1 for c in cs if is_text(c, False)),
            text_B=sum(1 for c in cs if is_text(c, True)),
            planned_header=hdr.get(cs[0], "")))

    line_times = []
    for c in order:
        for i, r in enumerate(S.SUBS[c]):
            line_times.append((round(start[c] + S.LEAD + r["t"], 2), c, i + 1, r["text"]))

    quotes = []
    for c in order:
        sp = SPEC[c]
        if sp.get("fig") and sp["fig"][0] == "quote":
            q = sp["fig"][1]
            rows = S.SUBS[c]
            quotes.append(dict(
                cid=c, cut_start=round(start[c], 2),
                appears=round(start[c] + S.LEAD + rows[-1]["t"], 2),
                phrase=q.get("phrase", ""), rows=[list(r[:2]) for r in q.get("rows") or []],
                ctx=q.get("ctx", ""), star_in_script=any("★" in n for n in notes.get(c, [])),
                heading=sp.get("t", "")))
    star_only = [c for c in order if any("★" in n for n in notes.get(c, []))
                 and not (SPEC[c].get("fig") and SPEC[c]["fig"][0] == "quote")]

    photo_cuts = [c for c in order if SPEC[c].get("photo")]
    src_kind = Counter()
    for c in photo_cuts:
        ph = SPEC[c]["photo"]
        if c in moving:
            src_kind["記録映像（動く）"] += 1
        elif c in still_fb:
            src_kind["記録映像の1コマ（静止画・fb_）"] += 1
        elif ph.startswith("surfside/tf_"):
            src_kind["NIST スライド（tf_）"] += 1
        elif ph.startswith("surfside/ss_"):
            src_kind["記録映像の1コマ（静止画・ss_）"] += 1
        else:
            src_kind["その他"] += 1
    photo_files = Counter(SPEC[c]["photo"] for c in photo_cuts if c not in moving)

    flagA = {c: is_text(c, False) for c in order}
    flagB = {c: is_text(c, True) for c in order}

    # 単位
    def unit_hits(text):
        hits = []
        t2 = text
        for u in YP_UNITS:
            if u == "フィート":
                n = len(re.findall(r"(?<!平方)フィート", t2))
            elif u in ("ft",):
                n = len(re.findall(r"(?<![A-Za-z])ft(?![A-Za-z])", t2))
            elif u in ("in.",):
                n = len(re.findall(r"(?<![A-Za-z])in\.", t2))
            else:
                n = t2.count(u)
            hits += [u] * n
        return hits

    nxt = {c: (order[k + 1] if k + 1 < len(order) else None) for k, c in enumerate(order)}
    unit_narr = []
    for c, i, x in all_lines:
        h = unit_hits(x)
        if h:
            same_line = bool(METRIC.search(x))
            same_cut = any(METRIC.search(y) for y in script[c])
            n = nxt[c]
            next_cut = bool(n) and any(METRIC.search(y) for y in script[n])
            unit_narr.append(dict(cid=c, line=i + 1, text=x, units=h,
                                  metric_same_line=same_line, metric_same_cut=same_cut,
                                  metric_next_cut=next_cut))
    chap_names = {nm for _n, nm in S.CHAPTERS.values()}
    unit_screen = []
    for c in order:
        for x in screen[c]:
            if x.startswith("出典："):
                continue
            h = unit_hits(x)
            if h:
                same = bool(METRIC.search(x))
                same_cut = any(METRIC.search(y) for y in screen[c])
                unit_screen.append(dict(cid=c, text=x, units=h, metric_same_text=same,
                                        metric_same_cut=same_cut, chapter_marker=(x in chap_names)))

    def pat_hits(texts):
        res = OrderedDict((k, []) for k in TIME_PATS)
        for c, x in texts:
            for k, p in TIME_PATS.items():
                for m in p.finditer(x):
                    res[k].append(dict(cid=c, match=m.group(0), text=x))
        return res

    narr_texts = [(c, x) for c, _, x in all_lines]
    scr_texts = [(c, x) for c in order for x in screen[c] if not x.startswith("出典：")]
    time_narr = pat_hits(narr_texts)
    time_scr = pat_hits(scr_texts)

    def word_hits(texts, words):
        res = OrderedDict((w, []) for w in words)
        for c, x in texts:
            for w in words:
                n = x.count(w)
                for _ in range(n):
                    res[w].append(dict(cid=c, text=x))
        return res

    death_narr = word_hits(narr_texts, DEATH)
    death_scr = word_hits(scr_texts, DEATH)
    rumor = word_hits(narr_texts, RUMOR)

    kata = Counter()
    for c, x in narr_texts + scr_texts:
        for m in re.finditer(r"[ァ-ヴー]+(?:・[ァ-ヴー]+)+", x):
            kata[m.group(0)] += 1
    latin = Counter()
    for c, x in scr_texts:
        for m in re.finditer(r"[A-Z][a-z]+(?:[ .-][A-Z][a-z]+)+", x):
            latin[m.group(0)] += 1

    no_src = [c for c in order if notes.get(c) and re.search(r"／\s*―\s*$", notes[c][0])]

    metrics = OrderedDict(
        rev=rev, n_cuts=len(order), n_lines=len(all_lines),
        n_subtitles=sum(len(S.SUBS[c]) for c in order),
        total_sec=round(total, 2), total_mmss=mmss(total), speech_sec=round(speech, 2),
        structure_sec=round(total - speech, 2),
        lead=S.LEAD, tail=S.TAIL, tail_extra=S.TAIL_EXTRA, gap=nj.get("gap"),
        voice=dict(engine=nj.get("engine"), voice=nj.get("voice"), voice_name=nj.get("voice_name"),
                   model=nj.get("model"), settings=nj.get("settings"), speed=nj.get("speed")),
        chars_with_punct=ch_all, chars_nopunct_channel=ch_np, chars_nopunct_ext=ch_np2,
        cpm_channel=round(ch_np / (total / 60), 1), cpm_channel_speech_only=round(ch_np / (speech / 60), 1),
        cpm_with_punct=round(ch_all / (total / 60), 1),
        chapters=chapters,
        opening_60s=[lt for lt in line_times if lt[0] < 60.0],
        first_quote=quotes[0] if quotes else None,
        first_chapter_cut=next((c for c in order if c.startswith("c1")), None),
        first_chapter_start=round(start[next(c for c in order if c.startswith("c1"))], 2),
        quotes=quotes, star_without_quote_fig=star_only,
        fig_kinds=Counter(kind(c) for c in order).most_common(),
        photo_cuts=len(photo_cuts), photo_ratio=round(len(photo_cuts) / len(order), 4),
        photo_source_kinds=src_kind.most_common(), photo_files_static=photo_files.most_common(),
        footage_moving=moving, footage_still=still_fb,
        text_A=sum(flagA.values()), text_A_ratio=round(sum(flagA.values()) / len(order), 4),
        text_B=sum(flagB.values()), text_B_ratio=round(sum(flagB.values()) / len(order), 4),
        text_A_secs=round(sum(length[c] for c in order if flagA[c]), 1),
        text_B_secs=round(sum(length[c] for c in order if flagB[c]), 1),
        runs_A=runs(flagA), runs_B=runs(flagB),
        text_A_cuts=[c for c in order if flagA[c]], text_B_cuts=[c for c in order if flagB[c]],
        unsure_text_slides=[c for c in order if SPEC[c].get("photo") in UNSURE_SLIDES and not SPEC[c].get("fig")],
        units_narration=unit_narr, units_screen=unit_screen,
        time_narration=time_narr, time_screen=time_scr,
        death_narration={k: len(v) for k, v in death_narr.items()},
        death_screen={k: len(v) for k, v in death_scr.items()},
        death_narration_hits=death_narr, death_screen_hits=death_scr,
        rumor_hits=rumor, katakana_names=kata.most_common(), latin_names=latin.most_common(),
        no_source_cuts=no_src, has_ed01=("ed01" in order),
        last_cut=order[-1], last_lines=list(script[order[-1]]),
        question_lines=[(c, x) for c, x in narr_texts if "？" in x or "?" in x],
        start={c: round(start[c], 2) for c in order}, length={c: length[c] for c in order},
        photo_by_file={ph: [c for c in order if SPEC[c].get("photo") == ph]
                       for ph in sorted({SPEC[c]["photo"] for c in photo_cuts})},
        footage_use={c: dict(USE[c]) for c in order if c in USE},
        footage_clips={k: {kk: vv for kk, vv in v.items() if kk in ("entry", "sec", "w", "h", "credit", "note", "url")}
                       for k, v in FO.CLIPS.items()},
        screen_credit={c: credit_line(c) for c in order},
    )
    (HERE / "old_metrics.json").write_text(json.dumps(metrics, ensure_ascii=False, indent=1), encoding="utf-8")

    # ── 台本 ──────────────────────────────────────────
    out = []
    out.append("---\ntitle: 19本目①棚卸し — 旧版（4本目サーフサイド）公開版の台本\n"
               "created: 2026-10-05\ntags: [project/jiko-kensho, ep19]\n---\n")
    out.append("# 旧版（4本目・2026-09-06 公開）サーフサイドの台本 ── 公開した版の写し\n")
    out.append(f"> **機械で書き出したもの（手で写していない）**＝`ref/ep19/old/dump_old.py`（git の `{rev}` を読む）。\n"
               "> 台本の正本＝その版の `tools/narration.py` の `SCRIPT`。秒＝その版の `audio/narration.json` と "
               "`scene_jiko` の組み立て（LEAD 0.35＋TAIL 0.50＋決め所 quote は末尾 +2.0秒）。\n"
               "> 公開ファイル＝`out/jiko/titan_audio-ss2.mp4`（絵＝ss-r05＝`6562a17` と同じ・音＝`a77ddc4` で混ぜ直し）。\n"
               f"> {len(order)}カット／{len(all_lines)}行／完成尺 {mmss(total)}（{total:.1f}秒）。\n")
    out.append("## 凡例\n"
               "- `### cid ［開始〜終了］ 画の種類` … 秒は**完成した動画の中の時刻**（分:秒）\n"
               "- **★** … 決め所（`fig=quote`。台本のコメントの「★quote」と同じ12カット）。★の秒＝決め所が出はじめる時刻（最後の行の読み始め）\n"
               "- 「画と出典の欄」… 台本 SCRIPT のコメント（台本第3版 §4 の画の欄と出典）をそのまま\n"
               "- 「画面の出典行」… 焼いた画面に出た出典の文字（動く記録映像のカットは `footage.credit_of`）\n"
               "- 行の頭の［秒］… その行を読み始める時刻\n")
    cur = None
    for c in order:
        k = chap_key(c)
        if k != cur:
            cur = k
            ch = next(x for x in chapters if x["key"] == k)
            out.append(f"\n## {ch['name']}（{ch['first']}〜{ch['last']}・{ch['n_cuts']}カット・"
                       f"{mmss(ch['start'])}〜{mmss(ch['start'] + ch['sec'])}・尺 {mmss(ch['sec'])}）\n")
            if ch["planned_header"]:
                out.append(f"> 台本の章見出しのコメント：{ch['planned_header']}\n")
        sp = SPEC[c]
        star = "★" if (sp.get("fig") and sp["fig"][0] == "quote") else ""
        out.append(f"### {star}{c} ［{mmss(start[c])}〜{mmss(start[c] + length[c])}］ {kind(c)}\n")
        out.append(f"- 画：{picture(c)}")
        if sp.get("t"):
            out.append(f"- 見出し：{sp['t']}" + (f"　／　副題：{sp['s']}" if sp.get("s") else ""))
        for n in notes.get(c, []):
            out.append(f"- 画と出典の欄（台本のコメント）：{n}")
        cr = credit_line(c)
        if cr:
            out.append(f"- 画面の出典行：{cr}")
        if star:
            q = sp["fig"][1]
            out.append(f"- ★決め所の句：「{q.get('phrase', '')}」（{mmss(start[c] + S.LEAD + S.SUBS[c][-1]['t'])} に出はじめ）")
            if q.get("ctx"):
                out.append(f"- ★原文の欄：{q['ctx']}")
        out.append("")
        for i, r in enumerate(S.SUBS[c], 1):
            out.append(f"{i}. ［{mmss(start[c] + S.LEAD + r['t'])}］ {r['text']}")
        out.append("")
    (HERE / "old_script_published.md").write_text("\n".join(out) + "\n", encoding="utf-8")

    # ── 画面の文字 ─────────────────────────────────────
    sc = ["---\ntitle: 19本目①棚卸し — 旧版（4本目サーフサイド）画面の文字\ncreated: 2026-10-05\n"
          "tags: [project/jiko-kensho, ep19]\n---\n",
          "# 旧版（4本目）の画面の文字 ── カットごとに描かれる全レイヤーの文字\n",
          f"> 機械で書き出したもの＝`ref/ep19/old/dump_old.py`（git `{rev}`・`check_dup.collect()` と同じ取り方）。\n"
          "> ⚠️ 写真・スライドに**焼き込まれた英字**（NIST の図の中の文字）は入らない＝こちらが重ねた文字だけ。\n"
          "> ⚠️ 動く記録映像のカットの出典行は、ここでは控えの静止画の出典（末尾「（静止画）」）で出ている。"
          "焼いた本編では `footage.credit_of` の出典（「（静止画）」なし）が出た。\n"]
    for c in order:
        sc.append(f"## {c} ［{mmss(start[c])}］ {kind(c)}")
        for x in screen[c]:
            sc.append(f"- {x}")
        sc.append("")
    (HERE / "old_screen_text.md").write_text("\n".join(sc) + "\n", encoding="utf-8")
    print(f"✓ {len(order)}カット／{len(all_lines)}行／{mmss(total)} → old_script_published.md・old_screen_text.md・old_metrics.json")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", default="e6fe892")
    ap.add_argument("--work", default=None)
    ap.add_argument("--analyze", default=None, help="（内部用）写しのフォルダを読んで書き出す")
    a = ap.parse_args()
    if a.analyze:
        analyze(Path(a.analyze), a.rev)
        return
    work = Path(a.work) if a.work else Path(tempfile.mkdtemp(prefix="ep19_old_"))
    work.mkdir(parents=True, exist_ok=True)
    n = extract(a.rev, work)
    print(f"写し {n}ファイル（{a.rev}）→ {work}")
    env = dict(os.environ, PYTHONIOENCODING="utf-8", PYTHONUTF8="1")
    r = subprocess.run([sys.executable, str(Path(__file__).resolve()), "--analyze", str(work), "--rev", a.rev],
                       env=env, cwd=str(work))
    sys.exit(r.returncode)


if __name__ == "__main__":
    main()
