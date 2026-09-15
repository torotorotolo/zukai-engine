# -*- coding: utf-8 -*-
"""章ファイルが**本当に読めていて、台本と1対1か**を見る（2026-09-08 新設・6本目 ⑤b）。

■ なぜ要るか（この日に実際に踏んだ）
  `cuts/ss.py` から `scene_jiko` を import したせいで循環参照になり、
  **`cuts/pr.py` と `cuts/c1.py` が丸ごと読めなくなった。**
  ところが `cuts/__init__.py` は例外を握って `BROKEN` に入れるだけなので、
  `check_layout.py` は**空の SPEC を調べて「✓ 全部おさまっている」**を出した。
  ＝ [[feedback-gates-blind-to-the-new-material]] の「0件を調べて合格」そのもの。

■ 見るもの（どれか1つでも欠けたら exit 2）
  1. 🔴 `cuts.BROKEN` が空（章ファイルが1つも落ちていない）
  2. 🔴 カットIDが `audio/narration.json` と**過不足なく一致**する
     ＝ 台本にあって画が無い／画があって台本に無い、を両方向で見る
     ⚠️ カットIDは題材をまたいでぶつかるので、**前の題材の図が黙って出る**のを
        ここで止める（[[project-jiko-rules-index]] §0b）
  3. 🔴 写真映像の割合が **45〜50%**（事故検証chの規則。[[feedback-jiko-photo-ratio]]）
     写真映像＝`photo=` を持つカット（実写・報告書の図・地に敷いた図解のすべて）
  4. 🔴 全画面の写真で**切り落としが 12.8% を超えていない**（2026-09-08 ⑤b-5 に新設）
     `cuts/ss.py` の `kind()` は縦長しか額装に回しておらず、**横長の側に規則が無かった**。
     「Left to right: …」の2枚組の図（縦横比 2.6〜3.3）を全画面にすると
     **横の32〜45%が切れる**。p62 は c108／c604 で実際にそう出ていた。
     → [[feedback-kinsoku-needs-both-ends]]（片側だけの規則は粗を反対側へ移すだけ）
     ⚠️ 章ファイルが `**ss.kind(...)` を通していれば自動で額装になる。ここで鳴るのは
        **手で `panel` を書いた**か、`kind()` を通していないカット。

■ 使い方
    python tools/check_cuts.py
    python tools/check_cuts.py --selftest    # 物差しの検算（陽性対照つき）
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

HERE = Path(__file__).resolve().parent.parent
NARRATION = HERE / "audio" / "narration.json"

# 事故検証ch の規則（2026-08-03 カズヤくん）。⚠️ ここを緩めるときは記憶のほうも直す
PHOTO_MIN, PHOTO_MAX = 0.45, 0.50

# 全画面にしたときに許す切り落とし。`cuts/ss.py` の `PANEL_AR` と**同じ値**を別の言い方で
# 書いたもの（1 − PANEL_AR ÷ 画面の縦横比）。2つの数を別々に持たない。
#
# 🔴🔴 2026-09-15（8本目 ⑤b-2）：**ここは 0.128 が直書きされていて腐っていた。**
#   0.128 は 7本目の `PANEL_AR = 1.55` から出した数。8本目は額装の敷居を
#   **4:3（1.3333）へ取り直した**ので、対応する切り落としは **25.0%** になる。
#   直書きのままだと、上流を替えたのに物差しだけ前作のまま＝黙って間違った合格／不合格が出る。
#   → [[feedback-gates-go-stale-when-upstream-changes]]。`cuts/ss.py` から毎回引く。
def _crop_max():
    import cuts.ss as ss
    return 1.0 - ss.PANEL_AR / ss.SCREEN_AR


CROP_MAX = _crop_max()

# 🔴 物差しの陽性対照に使う**実在の図版**（2026-09-13 追加）。
#    「この回は図版を使わない」ときでも `crop_loss` が生きているかを毎回1件で確かめる。
#    ⚠️ **架空の名前にしてはいけない**（開けないので「測れていない」に落ち、
#       検算そのものが空振りする）。6本目キー橋の図版を据え置きで使う。
_CONTROL_FIG = "keybridge/kb_p064_fig27.png"


def _crop_loss(name):
    """`cuts/ss.py` の物差しをそのまま借りる（門番が独自に測ると2つの真実ができる）。"""
    import cuts.ss as ss
    return ss.crop_loss(name)


def _is_report_figure(name):
    """🔴 この門番は**報告書の図版だけ**を見る。写真は見ない。

    ⚠️ 規則の中身は「図の端の**凡例や寸法**が切れる」こと。写真には切れて困る端が無く、
       3:2 の写真を 16:9 にすれば必ず 15〜25% は落ちる（それが写真の当て方）。
       写真まで鳴らすと、額装に回して**写真が小さな枠に収まる**という別の粗になる。
       写真の寄せは `bias=` で決め、⑤c の目視で見る。
       → [[feedback-verify-your-own-instrument]]（全部NGなら道具のほうを疑う）
    """
    import cuts.ss as ss
    return name.split("/", 1)[-1].rsplit(".", 1)[0] in ss.BANDS


def script_cuts():
    """台本のカットID（`narration.json` の順）。**画の側ではなく音の側を正とする。**"""
    d = json.loads(NARRATION.read_text(encoding="utf-8"))
    ids = list(d.get("durations") or {})
    if not ids:
        raise RuntimeError(f"{NARRATION} からカットIDを取り出せない（鍵＝{list(d)}）")
    return ids


def check(spec=None, broken=None, want=None):
    """(見つけたことの一覧, 最悪の exit) を返す。"""
    import cuts
    spec = cuts.SPEC if spec is None else spec
    broken = cuts.BROKEN if broken is None else broken
    want = script_cuts() if want is None else want
    out, code = [], 0

    # 1. 章ファイルが読めているか
    if broken:
        for name, e in broken.items():
            out.append(f"🔴 cuts/{name}.py が読めていない: {e}")
        code = 2
    else:
        out.append(f"✓ 章ファイルは全部読めている（{len(spec)}カット）")

    # 2. 台本と1対1か
    miss = [c for c in want if c not in spec]           # 台本にあって画が無い
    extra = [c for c in spec if c not in want]          # 画があって台本に無い
    if miss:
        out.append(f"🔴 画が無いカット {len(miss)}件: {miss[:12]}"
                   + ("…" if len(miss) > 12 else ""))
        code = 2
    if extra:
        out.append(f"🔴 台本に無いカットID {len(extra)}件: {extra[:12]}"
                   + ("…" if len(extra) > 12 else ""))
        code = 2
    if not miss and not extra:
        out.append(f"✓ 台本と1対1（{len(want)}カット）")

    # 3. 写真映像の割合
    #    ⚠️ 台本と1対1でないうちは割合を出しても意味が無いので、そのときは測るだけ
    photo = [c for c, s in spec.items() if s.get("photo")]
    r = len(photo) / max(1, len(spec))
    ok = PHOTO_MIN <= r <= PHOTO_MAX
    mark = "✓" if ok else ("⚠️" if miss or extra else "🔴")
    out.append(f"{mark} 写真映像 {len(photo)}/{len(spec)} ＝ {r * 100:.1f}%"
               f"（規則 {PHOTO_MIN * 100:.0f}〜{PHOTO_MAX * 100:.0f}%）")
    if not ok and not (miss or extra) and not broken:
        code = max(code, 2)

    # 4. 全画面の写真の切り落とし
    #    ⚠️ 実物を開いて測る（縦横比を推定しない）。ファイルが無い欄は「測れていない」と言う。
    #       → [[feedback-a-gate-that-throws-measures-nothing]] 例外で止めず件数を出す
    over, unmeasured, measured = [], [], 0
    for cid, s in spec.items():
        name = s.get("photo")
        if not name or s.get("panel"):
            continue
        try:
            if not _is_report_figure(name):     # 写真は見ない（上の注記）
                continue
            loss = _crop_loss(name)
        except Exception:                                   # noqa: BLE001
            unmeasured.append(cid)
            continue
        measured += 1
        if loss > CROP_MAX + 1e-6:
            over.append((cid, name, loss))
    if over:
        for cid, name, loss in sorted(over, key=lambda x: -x[2]):
            out.append(f"🔴 {cid}: {name} を全画面にすると {loss * 100:.1f}% 切れる"
                       f"（上限 {CROP_MAX * 100:.1f}%）＝ ss.kind() を通す")
        code = max(code, 2)
    else:
        out.append(f"✓ 全画面の報告書の図版 {measured}件、切り落としは全部 "
                   f"{CROP_MAX * 100:.1f}% 以内")
    # 🔴 陽性対照が0件でないこと。「測る対象が0件で合格」を出させない
    #
    # 🔴🔴 2026-09-13（7本目⑤b）**「0件」には2つの意味がある。**分けないと正しいものを落とす。
    #   (a) この回は**報告書の図版を1枚も使わない**（`ss.BANDS` が空）。9/11委員会報告は
    #       文章の報告書で、画面に出すのは印字ページ番号だけ＝**0件が正しい状態**。
    #   (b) 図版は焼いてある（`ss.BANDS` に在る）のに1件も画面に来ていない＝**これが事故**
    #       （キー橋で塞いだ穴。門番が空の SPEC を調べて合格を出した型）。
    #   → 分岐の鍵は**カットの割り当てではなく、その回の図版の在庫**（`ss.BANDS`）。
    #   ⚠️ (a) でも**物差しそのものは毎回検算する**。在庫が空のときは
    #      「別の回の実在する図版」で `crop_loss` を1回走らせ、測れなければ落とす。
    #      ＝ 0件を合格にはするが、**道具が死んでいたら通さない**
    #      （[[feedback-verify-your-own-instrument]]）。
    if measured == 0 and not over:
        import cuts.ss as ss
        if ss.BANDS:
            out.append("🔴 全画面の図版を1件も測っていない＝この検査は何も見ていない"
                       f"（この回の図版の在庫は {len(ss.BANDS)}枚ある）")
            code = max(code, 2)
        else:
            probe, got = _CONTROL_FIG, None
            try:
                if (HERE / "ref" / probe).exists():
                    got = ss.crop_loss(probe)
            except Exception as e:                              # noqa: BLE001
                got = None
                out.append(f"🔴 陽性対照の図版を測れない（{probe}: {e}）＝物差しが死んでいる")
                code = max(code, 2)
            if got is None and (HERE / "ref" / probe).exists():
                out.append(f"🔴 陽性対照 {probe} の切り落としが出ない＝物差しが死んでいる")
                code = max(code, 2)
            elif got is not None:
                out.append(f"✓ この回は報告書の図版を使わない（在庫0枚）。物差しは生きている"
                           f"（陽性対照 {probe} の切り落とし {got * 100:.1f}%）")
            else:
                out.append(f"⚠️ 陽性対照の図版 {probe} が手元に無いので物差しを検算できない")
    if unmeasured:
        out.append(f"⚠️ 縦横比を測れなかった {len(unmeasured)}件: {unmeasured[:8]}"
                   + ("…" if len(unmeasured) > 8 else ""))
    return out, code


def _control_bands():
    """🔴 検算のあいだだけ `ss.BANDS` に**実在の図版の台帳**を入れる。

    2026-09-13（7本目⑤b）：7本目は報告書の図版を1枚も使わないので `ss.BANDS` が空。
    すると `_is_report_figure()` が**何に対しても False** を返し、切り落としの検算4本が
    「対象0件」で黙って落ちた（検算 7/11）。
    ＝ **検算は「その回の在庫」ではなく「道具」を試すもの**なので、
      6本目キー橋の台帳（`ref/keybridge/textbands.json`）を借りて当てる。
    ⚠️ `fig_box` まで入れる。入れないと切り出し前の紙の縦横比で測ってしまい、
       期待値（57%／32%／45%）が全部ずれる。
    ⚠️ `trimmed_size` は lru_cache なので、入れ替えの前後で**必ず捨てる**。
    """
    import cuts.ss as ss
    f = HERE / "ref" / "keybridge" / "textbands.json"
    keep = dict(ss.BANDS)

    class _Ctx:
        def __enter__(self):
            if f.exists():
                ss.BANDS.clear()
                ss.BANDS.update(json.loads(f.read_text(encoding="utf-8")))
            ss.trimmed_size.cache_clear()
            ss.size_of.cache_clear()
            return len(ss.BANDS)

        def __exit__(self, *_a):
            ss.BANDS.clear()
            ss.BANDS.update(keep)
            ss.trimmed_size.cache_clear()
            ss.size_of.cache_clear()
            return False

    return _Ctx()


def selftest():
    """🔴 物差しそのものを検算する。**陽性対照＝わざと壊した入力で鳴ること**。"""
    ok = []

    def chk(name, got):
        ok.append(bool(got))
        print(f"  {'✓' if ok[-1] else '🔴'} {name}")

    # 🔴 検算のあいだは図版の台帳を借りる（この回は在庫0枚なので、借りないと
    #    切り落としの検算が「対象0件」で黙って落ちる）。
    ctx = _control_bands()
    n_bands = ctx.__enter__()
    chk(f"検算用の図版の台帳を借りられた（{n_bands}枚）", n_bands > 0)

    want = ["a1", "a2", "a3", "a4"]
    # ⚠️ **実在の図版**を使う。架空の名前だと「測れていない」に落ちて、
    #    4番の検査（切り落とし）が何も見ないまま合格を出す。
    good = {c: dict(photo="keybridge/kb_p064_fig27.png") for c in want[:2]}
    good.update({c: dict(fig=("panel", {})) for c in want[2:]})
    _o, c = check(spec=good, broken={}, want=want)
    chk("陽性対照：50%ちょうどは通る", c == 0)

    _o, c = check(spec=good, broken={"c1": ValueError("boom")}, want=want)
    chk("陽性対照：章ファイルが落ちていたら止まる", c == 2)

    short = {c_: v for c_, v in list(good.items())[:3]}
    _o, c = check(spec=short, broken={}, want=want)
    chk("陽性対照：台本より画が少なければ止まる", c == 2)

    lean = {c: dict(fig=("panel", {})) for c in want}
    lean["a1"] = dict(photo="keybridge/kb_p064_fig27.png")
    _o, c = check(spec=lean, broken={}, want=want)
    chk("陽性対照：写真25%は止まる", c == 2)

    # 4. 切り落としの検算。⚠️ **実在の絵**で測る（架空の名前だと「測れていない」に落ちて
    #    黙って通ってしまう＝0件を調べて合格）。→ [[feedback-gates-blind-to-the-new-material]]
    WIDE = "keybridge/kb_p061_fig23.png"     # 縦横比 3.26 ＝ 横が 45% 切れる
    FIT = "keybridge/kb_p064_fig27.png"      # 縦横比 1.77 ＝ 画面とほぼ同じ
    try:
        chk(f"陽性対照：横長すぎる図（{_crop_loss(WIDE) * 100:.0f}%切れ）を全画面にしたら鳴る",
            check(spec={"a1": dict(photo=WIDE), "a2": dict(photo=FIT),
                        "a3": dict(fig=("panel", {})), "a4": dict(fig=("panel", {}))},
                  broken={}, want=want)[1] == 2)
        chk("陰性対照：同じ図でも panel なら鳴らない",
            check(spec={"a1": dict(photo=WIDE, panel=True), "a2": dict(photo=FIT),
                        "a3": dict(fig=("panel", {})), "a4": dict(fig=("panel", {}))},
                  broken={}, want=want)[1] == 0)
        chk("陰性対照：画面と同じ縦横比の図は鳴らない", _crop_loss(FIT) <= CROP_MAX)
        chk("ss.kind() と門番のしきい値がずれていない",
            abs(_crop_loss("keybridge/kb_p062_fig24.png") - 0.32) < 0.02)
        # 🔴 写真は見ない。3:2 の写真は必ず 22% 切れるが、それは粗ではない
        PHOTO = "keybridge/kb_pre_deck05.jpg"
        chk(f"陰性対照：写真（{_crop_loss(PHOTO) * 100:.0f}%切れ）では鳴らない",
            (not _is_report_figure(PHOTO))
            and check(spec={"a1": dict(photo=PHOTO), "a2": dict(photo=FIT),
                            "a3": dict(fig=("panel", {})), "a4": dict(fig=("panel", {}))},
                      broken={}, want=want)[1] == 0)
        # 🔴 測る対象が0件のときは「合格」でなく「何も見ていない」と言うこと
        chk("陽性対照：図版が1件も無ければ『何も見ていない』で止まる",
            check(spec={"a1": dict(photo=PHOTO), "a2": dict(photo=PHOTO),
                        "a3": dict(fig=("panel", {})), "a4": dict(fig=("panel", {}))},
                  broken={}, want=want)[1] == 2)
    except Exception as e:                                  # noqa: BLE001
        chk(f"🔴 切り落としの検算ができない（{e}）", False)
    finally:
        ctx.__exit__()

    # 🔴🔴 借りた台帳を戻したあとの状態も検算する（本番の分岐）。
    #    7本目は在庫0枚＝「使わないのが正しい」側に落ちること。
    import cuts.ss as ss
    _o, c = check(spec={"a1": dict(fig=("panel", {})), "a2": dict(photo=_CONTROL_FIG),
                        "a3": dict(fig=("panel", {})), "a4": dict(photo=_CONTROL_FIG)},
                  broken={}, want=want)
    chk(f"この回の在庫（BANDS {len(ss.BANDS)}枚）で "
        f"{'「使わない」側に落ちて通る' if not ss.BANDS else '図版を測る側に落ちる'}",
        c == 0)

    chk("台本のカットIDが読める（本番の narration.json）", len(script_cuts()) > 0)
    good_all = all(ok)
    print("  " + (f"✓ 検算 {len(ok)}/{len(ok)}" if good_all
                  else f"🔴 検算 {sum(ok)}/{len(ok)} で落ちた"))
    return good_all


if __name__ == "__main__":
    if "--selftest" in sys.argv[1:]:
        sys.exit(0 if selftest() else 1)
    rows, rc = check()
    print("■ 章ファイルと台本の照合")
    for r in rows:
        print("  " + r)
    print("  " + ("✓ 通った" if rc == 0 else "🔴 落ちた"))
    sys.exit(rc)
