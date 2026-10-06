# -*- coding: utf-8 -*-
"""check_illu.py — 案C の再現イラスト（`tools/illu.py`）の**守りの線**を機械で測る（2026-09-28 新設・14本目 ⑤b-2）。

■ なぜ要るか（ルール §5b-74・§5b-75＝規則を書いたら門番も＝[[feedback-rules-need-gates]]）
    再現イラストは「記録どおりに描いた絵」。記録を越えた物・人・数・時刻が1つでも混ざると、絵がそのまま嘘になり、
    亡くなった方の尊厳の線（乗客は顔の無い群れだけ・水が入った後の船内に乗客を描かない）も目で追うだけでは漏れる。

■ 測るもの（**描く側と同じ関数**＝`illu.scene` が組んだ部品・鍵・型紙の数・群れの並び＝SPEC の文字を読み比べない）
  ① 全部品に rec（出典の表 `cuts.ss.REC_DOCS` の資料名＋頁）・頁が資料の範囲にあり、原文（`cuts.ss.REC_PAGES`）に在る。
     記録の欄（傾き・波・コンテナ・群れ）を変える段と、出来事（board・rings）の段は rec を書く。頭を既定から変えたら場面の rec
  ② 人の影の役割＝船員・海洋警察・管制（型紙）／乗客は**群れの型だけ**（`crowd_layout`＝隣と2割以上重なる・枠の外まで続く
     ＝`illu.crowd_uncountable`）。群れを出す場面は時刻 `at` を宣言し、`cuts.ss.ILLU_CROWD_UNTIL` より前
  ③ 描いた人の数（型紙を置く inst の数）＝宣言（`people=`）＝記録（宣言の rec）。型紙の影どうしは重ならない（1人ずつ数えられる）
     ＝⑤b-3 から**部品をまたいで全部の組**を・型紙の背（`fig_h`）で測る（傾けた型紙は `fig_deg` の向きに戻して）
  ④ 「再現イラスト」の札と出典（`illu.overlay_svg`＝全面・冒頭の絵／`illu_pair` は段の層の札と骨格の出典）
  ⑤ 画面に出す文字（札・左上の見る向き・左下の出典）に、資料で割れる時刻（`cuts.ss.ILLU_SPLIT_TIMES`）が無い。
     時計の札は表 `cuts.ss.ILLU_CLOCK_OK` の時刻だけ・秒の札は表 `cuts.ss.ILLU_SEC_OK` の値だけ＝🔴 表が空なら全部止める
     （16本目 ⑤b-2 から＝`judge_labels`）
  ⑦ 写真・頁・決め所・文字の頁のカットに絵が無い（混ざりは冒頭の絵か小さく戻す絵だけ）。「再現イラスト」の PLAN の
     カットは全面の絵（`illu`）で書く（SPEC が在るものだけ）
  ⑧ 上から見た絵（view に「上から」）は縮尺 `scale`（メートル／画素）が 1.5 以上（人が1画素に満たない＝15本目の申し送り）
  ほかに touch＝記録の「どの甲板が水面に届いたか」を、描く側と同じ幾何（`illu.contact_y`）で ±0.35 メートル
  🆕 16本目 ⑤b-3（映像方針 16本目 §9＝断面 VB・VC。記録の値は門番の側に＝REC_ELEV・REC_GAP・REC_RANGE・REC_SEC＝§5b-88）：
     ⚠️ 番号の ⑨ は15本目の「空の機体は地面に触れて見えない（RB）」と同じ番号（置き場が違う＝ぶつからない）
  ⑨ 断面の札の数（「866m」「約700m」「25mあまり」「水平に300〜400m」）は記録の表の数だけ・札の指す高さ／寸法を断面の目盛りで読むと
     値と合う（±3m・寸法 ±1.5m・横の寸法は範囲の内）
  ⑩ 記録を越える絵を止める：北の岸の水 ≤ 930m・水は斜面に沿う帯だけ（谷の真ん中で盛り上がらない）・崩れたあとの谷の中の頂上
     846〜866m・塊の水平の動き 300〜400m・塊の厚さ ≤ 330m／天端の上の水 100〜140m・ダムの天端725.5m と底463.9m・水位の線
  ⑪ 1つの塊：形のあいだ（と形と形の真ん中＝描き手と同じ補間）で面積 ±5%・底の点が支えの線に乗る（≤1画素）・底の辺が支えから
     浮かない（≤3画素）・支えの線はつま先から先が地形の線と同じ
  ⑫ 壊れる物の境目：町と集落の建物の面が消える（towns／shore＝gone・mud）・水が町を覆う（flood）・湖の岸の集落へ届く波（wave_e）は
     表（cuts.ss.ILLU_DESTROY_CUTS）のカットだけ・ダムの部品は壊さない（全部の段で同じ＝消えない・動かない）
  ⑬ 夜の色：夜の場面の動く物・大事な物の色（型の FIX の色で場面に使ったもの）と夜の地の色（門番の表 NIGHT_GROUND）の差 ΔE 25 以上
  ⑭ 群れと水：群れの部品は、水の部品が触れる段までに消える・顔・1人だけの影・倒れた形・人数の札を持たない（16本目はいまの
     絵コンテに群れが無い＝陽性対照だけ）
  🆕 16本目 ⑤b-4（VD＝正面から見た斜面・記録は門番の側の REC_VD・REC_LEN_KM）：
     ⑨ 札の数はカンマを外して読む（「1,200m」を 200m と読んでいた）・「幅1.8km」＝矢印の長さが 1,800m ±3%
     ⑩ 亀裂の折れ目の標高＝1,200→930→1,260・東の端 1,030m（S1 p72）／1960年の崩落の上の端 ≤850m・大きい方はダムの 400〜600m 上流
        （S1 p72・p82）／模型の塊は 600〜1,200m・2つの境は沢（亀裂の 930m の谷）の真下（S1 p89・p224）／実際の塊が下がったあとの
        上の端 846〜866m（S1 p146）／波の高さの印 25m（S1 p97）は模型の場面だけ／湖の水位は記録の水位（600・650・700・722.5m）だけ
     ④ 模型の想定（model）は「想定」の札と一緒にだけ・小さく戻す絵ならパネルの文に「想定」
  🆕 18本目 ⑤b-2（SA＝横から見た海・映像方針 18本目 §12・記録は門番の側の REC_DEPTH・REC_UP_MAX・REC_BOOM_*）：
  ⑤ 時計の札は分の小数まで読む（「9時18.1分」＝"9:18.1"・表に無い小数／小数の無い 9:18 は止める）
  ⑦ 混ざりの本物の側のつなぎ待ち（cuts.ss.ILLU_MIX_TODO）は束（ILLU_MIX_BUNDLE）ができるまで全面の絵でよい（参考の行）＝束ができたら止める
    🆕 ⑤b-7c：本物の側＝頭の映像（intro foot）か尻の写真・頁（tail）をつないだら合格・つないだのに表に残る／種類が「再現イラスト」なら止める
  ⑫ 潜水艦の圧壊と破片（sub＝crush・destroy の部品）は表（ILLU_DESTROY_CUTS）のカットだけ
  ⑮ 潜水艦は記録の時刻 clk（読める形）つきで ILLU_SUB_UNTIL（例外 ILLU_SUB_EXC）まで・艦の絵を止めたカット（ILLU_SUB_STOP）より後に
     置かない・下がる／圧壊は例外のカットで「推定」の札と一緒に（段の途中の札は下がり始めより前）・艦首の上げは記録の上限まで・
     壊れた船体の破片は数を持たず、最後の段で見えず、見える長さ 1.6秒まで（数えられる前に暗がりへ）
  ⑯ 深さの数を幾何で漏らさない：深さの目盛り（縮尺どおりの段）と潜水艦・試験深度の線を同じ段に置かない・試験深度の線は切れ目1の向こう／
     切れ目の向こうの海底とのあいだに切れ目2・試験深度の札に数を書かない・深さの数の札は目盛りの段の記録の値（260・2,200・2,600m）だけ・
     縮尺どおりの線は海底との比で記録の値（±3%）・目盛りは 2,600÷260＝10区間（型の定数を壊す陽性対照で門番が型を読んでいないことを確かめた）
  ⑰ 9時18.1分の大きく低い音の輪：表（ILLU_BOOM_CUTS）のカットの圧壊の段だけ・時刻は記録 9:18.1・輪の中心は圧壊した船体・札は認定18 と
     意見45 の言い方（内破でありうる・大きく低い音・船体の圧壊・見立て）・光・泡・炎の部品と glow の出来事なし
  🆕 18本目 ⑤b-3（SB 上から見た海・SC 上から見た海の底・SD 横から見た海の底の捜索＝記録は門番の側の REC_SB・REC_SB_TS・REC_SB_OIL・
     REC_SC_CIRCLE・REC_SC_MARKERS・REC_SD_ON）：
  ⑱ SB：記録の緯度経度の点（待ち合わせ・基準の点・9時21分の測位）が記録の位置（±2画素）・スレッシャー→スカイラークは 147度・3,400ヤード
     （±1.5度・±3%）・油の帯は9時17分の位置から南東（±11.25度）へ 7マイルの幅（法定マイル〜海里・±3%）・距離の札は「約3.1km」「十数キロ」
     だけで、その線を指す
  ⑲ SC：円の直径は 400ヤード（±3%）・札に「約370m」と「より広くない」・目印は枠の外まで続き数を持たない・札に目印の数 900・札の数は
     900・370・5・6・710-64 だけ（広さの数・塊の数を1つに決めない）
  ⑳ SD：トリエステ2世は最後の段で船体の一部の真上に着く（球の下の端と船体の上 ±3画素・球が船体の幅の内）・深さの切れ目がある・札に数なし
  ㉑ 見る向きの合図：PLAN の順で、すぐ前の全面の絵とのあいだが1カットまでで置き場か向きが替わるカットに、切り替えの字・目の印・位置の
     小さな地図のどれか（main と selftest）
  ⑥ 陽性対照（わざと壊した場面で鳴るか）＝`--selftest`（本番の前に必ず回る）

■ 使い方
    python tools/check_illu.py              # 全カット（selftest のあと）
    python tools/check_illu.py --selftest   # 物差しの検算だけ
"""
from __future__ import annotations

import math
import re
import sys
from functools import lru_cache
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
sys.stdout.reconfigure(encoding="utf-8")

import titan_fig as F  # noqa: E402,F401  （illu より先に読む）
import illu as IL  # noqa: E402

# 🆕 18本目 ⑤b-2：分の小数（「9時18.1分」＝認定18・意見45 の 0918.1R）まで読む＝"9:18.1"。小数の無い時刻は前と同じ "H:MM"
TIME = re.compile(r"(\d{1,2})\s*[時:：]\s*(\d{1,2}(?:\.\d+)?)")
SEC = re.compile(r"(約)?\s*(\d+(?:\.\d+)?)\s*秒")          # 15本目：秒の札（「0.27秒」「約9.1秒」）
# 16本目 ⑤b-2：分の無い時計の札（「22時ごろ」）も時計の札（「1時間」の「時」と「22時39分」の「時」は外す）
CLOCK_HOUR = re.compile(r"(?<!\d)(\d{1,2})\s*時(?!\s*\d|間)")
CROWD_ROLES = ("passengers",)
NON_ILLU_KINDS = ("写真", "図・写真の頁", "決め所", "文字の頁", "図解", "パネル")


def _ss():
    import cuts.ss as ss
    return ss


@lru_cache(maxsize=1)
def _pages():
    ss = _ss()
    p = getattr(ss, "REC_PAGES", None)
    if not p or not Path(p).exists():
        return None
    return {int(m) for m in re.findall(r"^=== p(\d+) ===", Path(p).read_text(encoding="utf-8"), re.M)}


HMS = re.compile(r"(\d{1,2})\s*[時:：]\s*(\d{1,2})(?:\s*[分:：]\s*(\d{1,2}(?:\.\d+)?))?")


def _hms(s, end):
    """場面の時刻 at・群れの上限 until を秒まで（15本目 ⑤b-3）。秒が無い書き方は、at（end=True）はその分の終わり（59.99秒）
    ＝その分のどこかもしれない＝**遅い側に倒す**（fail closed）、上限（end=False）はその分の頭。14本目（"9:46" < "9:47"）は前と同じ答え"""
    m = HMS.search(str(s or ""))
    if not m:
        return None
    sec = float(m.group(3)) if m.group(3) else (59.99 if end else 0.0)
    return (int(m.group(1)), int(m.group(2)), sec)


def check_recs(recs, where, docs, pages):
    bad = []
    for r in recs:
        got = IL.parse_rec(r, docs)
        if not got:
            bad.append(f"①{where}：rec「{r}」に資料名と頁が無い（`資料 p頁` の形・資料名は cuts.ss.REC_DOCS）")
            continue
        for doc, ps in got:
            lo, hi = docs[doc]["range"]
            # 16本目 ⑤b-2：原文の頁ファイルに無い資料（#100＝地形図の画像）は `text=False`＝範囲だけ見る（頁の照合を飛ばす）
            in_text = docs[doc].get("text", True)
            for p in ps:
                if not lo <= p <= hi:
                    bad.append(f"①{where}：rec「{r}」の p{p} が {doc} の頁の範囲（p{lo}〜p{hi}）の外")
                elif in_text and pages is not None and p not in pages:
                    bad.append(f"①{where}：rec「{r}」の p{p} が原文（REC_PAGES）に無い")
    return bad


def judge_labels(texts, where, split, sec_ok, clock_ok):
    """⑤ 画面に出す文字の時計と秒の札。返り値＝(食い違いの一覧, 照合した件数)。
    🔴 2026-10-01（16本目 ⑤b-2）：前は時計の照合が `if sec_ok:` の中＝秒の表が空だと**時計も秒も照合しなかった**
       （16本目の決め「秒の札は出さない＝ILLU_SEC_OK は空・時計は 22:39 だけ」が効かない穴）→ 表が空なら**全部止める**
       （その回が「出してよい」と書いた値だけ通す＝fail closed）。14本目の見本の場面は秒・時計の札を出さない＝前と同じに通る。
       ほかに：1つの札の中の時刻と秒は全部（前は最初の時刻1つだけ）・分の無い時計（「22時ごろ」）も時計の札"""
    bad, n = [], 0
    for txt in texts:
        txt = str(txt or "")
        for m in TIME.finditer(txt):
            n += 1
            mm, _dot, frac = m.group(2).partition(".")
            hm = f"{int(m.group(1))}:{int(mm):02d}" + (f".{frac}" if frac else "")
            if hm in split:
                bad.append(f"⑤{where}：札「{txt}」の時刻は資料で割れる（{split}）＝画面に出さない")
            elif hm not in clock_ok:
                bad.append(f"⑤{where}：札「{txt}」の時刻 {hm} は表の時刻でない（cuts.ss.ILLU_CLOCK_OK＝{clock_ok}・"
                           "空なら時計の札は出さない）")
        for m in CLOCK_HOUR.finditer(txt):
            n += 1
            bad.append(f"⑤{where}：札「{txt}」の「{m.group(0)}」は分の無い時計（表の時刻 {clock_ok} の形で書く）")
        for m in SEC.finditer(txt):
            n += 1
            if m.group(2) not in sec_ok:
                bad.append(f"⑤{where}：札「{txt}」の「{m.group(0)}」は表の値でない（cuts.ss.ILLU_SEC_OK＝"
                           f"{sorted(sec_ok, key=float)}・空なら秒の札は出さない）")
    return bad, n


def judge_scene(sc, where, docs=None, pages=None, split=None, until=None, sec_ok=None, clock_ok=None, counts=None,
                roles=None):
    """場面1つを測る。返り値＝(食い違いの一覧, 照合した件数)。
    15本目 ⑤b-2 から：sec_ok（秒の札の表）・clock_ok（時計の札の表）・counts（描いてよい数）＝その回の表が空なら測らない
    15本目 ⑤b-3 から：roles（その回に置いてよい役割＝dict(sprite=(…), crowd=(…))・`cuts.ss.ILLU_ROLES`）。空なら型の既定
       （illu.ROLES・CROWD_ROLES＝14本目の船）"""
    ss = _ss()
    docs = docs if docs is not None else ss.REC_DOCS
    pages = pages if pages is not None else _pages()
    split = split if split is not None else ss.ILLU_SPLIT_TIMES
    until = until if until is not None else ss.ILLU_CROWD_UNTIL
    sec_ok = sec_ok if sec_ok is not None else (getattr(ss, "ILLU_SEC_OK", None) or {})
    clock_ok = clock_ok if clock_ok is not None else tuple(getattr(ss, "ILLU_CLOCK_OK", None) or ())
    counts = counts if counts is not None else (getattr(ss, "ILLU_COUNTS", None) or {})
    bad, n = [], 0
    # ① 部品の rec・段の rec
    for p in sc["parts"]:
        n += 1
        if p.get("signal"):
            # 16本目 ⑤b-2：見る向きの合図の部品（切り口の線・目の印・切り替えの字＝ルール §5b-80）は記録の物でない＝rec は要らない。
            #   ただし数（obj）と人（role）は持たせない（合図に記録の物を紛れ込ませない）
            if p.get("obj") or p.get("role"):
                bad.append(f"①{where}：合図の部品 {p['id']} が数か人を持つ（合図は記録の物を描かない）")
            continue
        if not p.get("rec"):
            bad.append(f"①{where}：部品 {p['id']} に rec が無い")
    bad += check_recs([p["rec"] for p in sc["parts"] if p.get("rec")], where, docs, pages)
    # ④ 16本目 ⑤b-2：会社の説明の想定（VA の split）は「想定」の札（assume）と一緒にだけ描く（起きた事ではない＝映像方針 §2③）
    if sc["place"] == "VA" and any(st["split"] != "off" for st in [sc["start"]] + sc["states"]):
        n += 1
        if "想定" not in (sc.get("assume") or ""):
            bad.append(f"④{where}：会社の説明の想定（split）を描いたのに「想定」の札が無い（assume=）")
    # 🆕 ⑤b-4：模型の想定（VD の model）も「想定」の札と一緒にだけ（小さく戻す絵＝box は judge_cut がパネルの文で見る）
    if sc["place"] == "VD" and not sc.get("box") and any(st["model"] != "off" for st in [sc["start"]] + sc["states"]):
        n += 1
        if "想定" not in (sc.get("assume") or ""):
            bad.append(f"④{where}：模型の想定（model）を描いたのに「想定」の札が無い（assume=）")
    prev = sc["start"]
    base = IL.FIELDS[sc["place"]]
    if any(sc["start"].get(k) != base.get(k) for k in IL.REC_FIELDS if k in base) and not sc.get("rec"):
        bad.append(f"①{where}：頭の状態を既定から変えた（{[k for k in IL.REC_FIELDS if sc['start'].get(k) != base.get(k)]}）"
                   "のに場面の rec が無い")
    for i, (st, sp) in enumerate(zip(sc["states"], sc["steps"])):
        n += 1
        changed = [k for k in IL.REC_FIELDS if k in st and st[k] != prev.get(k)]
        events = [k for k in IL.EVENTS if sp.get(k)]
        if (changed or events) and not sp.get("rec"):
            bad.append(f"①{where}：段{i + 1}で {changed + events} を変えた／起こしたのに rec が無い")
        prev = st
    bad += check_recs([sp["rec"] for sp in sc["steps"] if sp.get("rec")] + ([sc["rec"]] if sc.get("rec") else []),
                      where, docs, pages)
    # ② 人の役割・群れの型・群れの時刻
    #   🔴 15本目 ⑤b-3：置いてよい役割は回ごとの表（`ss.ILLU_ROLES`）＝15本目は型紙（1人ずつ数えられる影）0・群れは観客だけ
    #      （パイロット・審判・救護・検査員・整備の仲間を置くと止まる＝映像方針 §6②）。時刻は秒まで（`_hms`）
    roles = roles if roles is not None else (getattr(ss, "ILLU_ROLES", None) or {})
    sprite_ok = tuple(roles["sprite"]) if "sprite" in roles else IL.ROLES
    crowd_ok = tuple(roles["crowd"]) if "crowd" in roles else CROWD_ROLES
    at = _hms(sc.get("at"), end=True)
    for p in sc["parts"]:
        role = p.get("role")
        if role is None:
            continue
        n += 1
        if p.get("kind") == "sprite":
            if role not in sprite_ok:
                bad.append(f"②{where}：型紙の影（1人ずつ数えられる形）の役割「{role}」は {sprite_ok} だけ"
                           "（群れの人は群れの型でだけ＝1人を抜き出さない）")
        elif role in crowd_ok:
            if not p.get("crowd"):
                bad.append(f"②{where}：群れの部品 {p['id']} が群れの型（crowd_layout）で描かれていない")
            for c in p.get("crowd") or []:
                bad += [f"②{where}：{b}" for b in IL.crowd_uncountable(c["layout"], c["x0"], c["x1"])]
            shown = any(float(k.get("a", 1.0)) > 0.0 for k in p["keys"])
            if shown:
                lim = _hms(until, end=False)
                if at is None:
                    bad.append(f"②{where}：群れを出す場面なのに時刻 at が無い")
                elif lim is None or at >= lim:
                    bad.append(f"②{where}：群れを {sc['at']} の場面に出した（{until} より前だけ＝§5b-74②。"
                               "秒の無い時刻はその分の終わりとみなす）")
        else:
            bad.append(f"②{where}：この回に置けない役割「{role}」（型紙 {sprite_ok}・群れ {crowd_ok}）")
    # ③ 描いた人の数＝宣言＝記録
    #   ⑤b-3：重なりは**部品をまたいで**全部の組で・型紙の背の高さ（fig_h＝置き場ごとに違う）で測る
    #   （ゴムボートの海洋警察と乗り移る船員は別の部品＝部品の中だけ見ると重なりを見逃す）
    #   船内で傾けた型紙（fig_deg）は、影の立つ向き＝床に沿う向きに戻して測る（画面の縦横で測ると 45度の並びが全部「重なる」）
    drawn, ends = {}, []
    for p in sc["parts"]:
        if p.get("kind") == "sprite":
            drawn[p.get("role")] = drawn.get(p.get("role"), 0) + len(p.get("inst") or [])
            ends += [(tuple(i["path"][-1]), float(p.get("fig_h") or IL.FIG_H), float(p.get("fig_deg") or 0.0))
                     for i in p.get("inst") or []]

    def _near(a, fa, da, b, fb):
        r = math.radians(-da)
        dx, dy = b[0] - a[0], b[1] - a[1]
        u, v = dx * math.cos(r) - dy * math.sin(r), dx * math.sin(r) + dy * math.cos(r)
        return abs(u) < max(fa, fb) * 0.55 and abs(v) < max(fa, fb) * 0.5
    hit = next(((a, b) for j, (a, fa, da) in enumerate(ends) for (b, fb, _db) in ends[j + 1:] if _near(a, fa, da, b, fb)),
               None)
    if hit:
        bad.append(f"③{where}：型紙の影の立つ所 {hit[0]}・{hit[1]} が重なる（1人ずつ数えられない＝数の照合が目で出来ない）")
    decl = sc.get("people") or {}
    for role in set(drawn) | set(decl):
        n += 1
        d = decl.get(role)
        want = d[0] if isinstance(d, (tuple, list)) else d
        if want is None:
            bad.append(f"③{where}：{role} を {drawn.get(role)} 人描いたのに宣言（people=）が無い")
        elif drawn.get(role, 0) != want:
            bad.append(f"③{where}：{role} の描いた数 {drawn.get(role, 0)} ≠ 宣言 {want}")
        if d is not None and not (isinstance(d, (tuple, list)) and len(d) > 1 and d[1]):
            bad.append(f"③{where}：宣言 {role} に記録（rec）が無い＝people=dict({role}=(数, \"資料 p頁\"))")
        elif d is not None:
            bad += check_recs([d[1]], where, docs, pages)
    # ⑤ 画面に出す文字（段の札・左上の見る向き・左下の出典）の時計と秒＝表の値だけ（表が空なら全部止める＝judge_labels）。
    #   15本目〜：#42 の 5.3秒・EXIF から推した時刻を出さない（映像方針 §6 ⑤）／16本目：秒の札は出さない・時計は 22:39 だけ（§9 ⑤）
    texts = [txt for t in sc["tags"] for txt in (t.get("texts") or [])] + [sc.get("view") or "", sc.get("src") or ""]
    b, m = judge_labels(texts, where, split, sec_ok, clock_ok)
    bad += b
    n += m
    # ③' 15本目〜：描いた物の数（部品の obj の合計＝描く側の部品そのもの）＝記録の数（`cuts.ss.ILLU_COUNTS`）
    if counts:
        drawn_obj = {}
        for p in sc["parts"]:
            for k, v in (p.get("obj") or {}).items():
                drawn_obj[k] = drawn_obj.get(k, 0) + int(v)
        for k, v in drawn_obj.items():
            n += 1
            if k not in counts:
                bad.append(f"③{where}：{k} を {v} 描いたのに記録の数（cuts.ss.ILLU_COUNTS）が無い")
            elif v != counts[k][0]:
                bad.append(f"③{where}：{k} を {v} 描いた（記録は {counts[k][0]}＝{counts[k][1]}）")
            else:
                bad += check_recs([counts[k][1]], where, docs, pages)
    # ⑧ 上から見た絵の縮尺
    #   🔴 ⑤b-3：小さく戻す絵（illu_pair の枠 box）は、全面の絵を枠の幅へ縮めて置く（build_jiko.illu_minis）＝画面の上の縮尺は
    #      scale × 1920 ÷ 枠の幅（本番と同じ幾何で測る。c109 問い3 を寄せて×を読めるようにした＝枠 560 で 1.5÷2.4×3.43＝2.1）
    #   🆕 19本目 ⑤b-3：縮尺を持たない模式の上から見た絵（表 cuts.ss.ILLU_TOP_NOSCALE＝置き場: 理由）は、縮尺の代わりに
    #      「人が0（部品・people）」と左下の「模式」の断りを測る（決め⑤で人を描かない A2＝人が見える縮尺でも人のいない絵になる）
    noscale = dict(getattr(_ss(), "ILLU_TOP_NOSCALE", None) or {})
    if "上から" in (sc.get("view") or "") and sc["place"] in noscale:
        n += 1
        if any(p.get("role") or p.get("kind") == "sprite" or p.get("crowd") for p in sc["parts"]) or sc.get("people") \
                or "模式" not in (sc.get("src") or ""):
            bad.append(f"⑧{where}：縮尺を持たない上から見た絵（{noscale[sc['place']]}）に人を置いた／左下に「模式」の断りが無い")
    elif "上から" in (sc.get("view") or ""):
        n += 1
        eff =float(sc["scale"]) * (IL.W / float(sc["box"][2])) if sc.get("scale") and sc.get("box") else sc.get("scale")
        if not eff or float(eff) < 1.5:
            bad.append(f"⑧{where}：上から見た絵の画面の上の縮尺 {eff} メートル／画素（1.5 以上＝人が1画素に満たない縮尺だけ）")
    # 15本目 ⑤b-2：空の中の事故機（RB）は地面に触れて見えない（下見：90度前後の翼の下の先が地平線より下＝「翼が地面に触れた」絵
    #   ＝記録を越える＝落ちたのは約9.1秒）。後ろから見た段ごとに、描く側と同じ幾何（_rb_anchors）で翼の先が地平線より上か
    if sc["place"] == "RB":
        for i, st in enumerate([sc["start"]] + sc["states"]):
            if st["view"] == "rear":
                n += 1
                an = IL._rb_anchors(st)
                low = max(an["lwing"][1], an["rwing"][1])
                # 🔴 ⑤b-3：余白 8画素では、地平線の16画素上の翼の先が手前の丘と砂漠の境に乗って「触れた」絵に見えた（c307 の
                #    試し焼き）＝すき間の下限 RB_GAP（50画素）
                if low > IL.RB_HZ - IL.RB_GAP:
                    bad.append(f"⑨{where}：段{i}の傾き {st['roll']}度で翼の下の先 y={low:.0f} が地平線 {IL.RB_HZ:.0f} の"
                               f"{IL.RB_HZ - low:.0f}画素上（{IL.RB_GAP:.0f}画素未満＝地面に触れた絵に見える＝落ちたのは約9.1秒）")
    # touch：記録の「どの甲板が水面に」を同じ幾何で
    for i, (st, sp) in enumerate(zip(sc["states"], sc["steps"])):
        if sp.get("touch"):
            n += 1
            if sp["touch"] not in IL.CONTACTS:
                bad.append(f"touch {where}：段{i + 1}の「{sp['touch']}」は知らない点（{tuple(IL.CONTACTS)}）")
                continue
            h = IL.contact_y(sp["touch"], float(st["heel"]))
            if abs(h) > 0.35:
                bad.append(f"touch {where}：段{i + 1}の傾き {st['heel']}度で「{sp['touch']}」は水面から {h:+.2f} メートル"
                           "（記録は水面に届いた）")
    # 🆕 16本目 ⑤b-3：⑨⑩⑪（断面 VB・VC）・⑬（夜の色）・⑭（群れと水）
    b, m = judge_sec(sc, where, crowd_ok)
    return bad + b, n + m


# ══════════════════════════════════════════════════════════
#  🆕 16本目 ⑤b-3（2026-10-01）：断面（VB・VC）の ⑨〜⑪・⑬・⑭（⑫ は judge_cut）
# ══════════════════════════════════════════════════════════
# 🔴 記録の値は門番の側に持つ（型の定数を読まない＝§5b-88）。頁は ss.REC_DOCS の通し番号
# 🔴 2026-10-04（18本目 スレッシャー号 ⑤b-1・§0b）：16本目の値（断面 VB・VC・VD の高さ・差・範囲・記録 REC_ELEV・REC_GAP・REC_RANGE・REC_SEC・
#    REC_VD・REC_LEN_KM／置き場 VA の記録 REC_VA・方眼 VA_GRID_PX）は selftest の見本 `tools/fixture_ep16.py`
#    （GATES["check_illu"]・値は1つも変えていない＝git の `b044b56`）へ移した＝空。selftest は `selftest_ep16()` が見本を差し込んで回す
#    （落ちても終わっても `restore()` で本番の値へ戻す）。18本目で断面（VB〜VD）・上から見た絵（VA）の型を使うときは、その回の
#    記録の値をここに別に持つ（§5b-88）。空のあいだ、断面の札の数・高さ・寸法は「記録の表に無い」で止まる（fail closed）。
#    許し（ELEV_TOL・GAP_TOL・KM_TOL・SPLIT_TOL）・場所の名（SEC_PLACES）・夜の色の表（NIGHT_*）は型の側の定数＝残す
REC_ELEV = {}
REC_GAP = {}
REC_RANGE = {}
REC_SEC = {}
ELEV_TOL, GAP_TOL = 3.0, 1.5
# 🆕 ⑤b-4：VD（正面から見た斜面）の記録（門番の側＝§5b-88。型の VD_CRACK・VD_1960・VD_MODEL_Z・VD_PEAK・VD_WAVE_H を読まない）
REC_VD = {}
REC_LEN_KM = {}
KM_TOL = 0.03
SPLIT_TOL = 12.0                     # 模型の2つの塊の境と沢（亀裂の 930m の谷）の横のずれの許し（画素）
SEC_PLACES = ("VB", "VC", "VD")
# ⑬ 夜の地の色（場面の地になる色の名＝門番の表）。型の FIX（動く物・大事な物の色）と、この地の色の差を全部の組で測る
NIGHT_GROUND = dict(VA=("VA_PAL", ("b0", "b1", "b2", "b3", "b4", "floor")), VB=("VB_PAL", ("sky0", "sky1", "ground")),
                    VC=("VC_PAL", ("sky0", "sky1", "ground", "far")), VD=("VD_PAL", ("face0", "face1")))
NIGHT_FIX = dict(VA="VA_FIX", VB="VB_FIX", VC="VC_FIX", VD="VD_FIX")
NIGHT_DE = 25.0
NUM_M = re.compile(r"(\d+(?:\.\d+)?)\s*m(?![²³2-3])")
RANGE_M = re.compile(r"(\d+(?:\.\d+)?)\s*〜\s*(\d+(?:\.\d+)?)\s*m")
KM_M = re.compile(r"(\d+(?:\.\d+)?)\s*km")


@lru_cache(maxsize=1)
def _map16():
    import json
    js = HERE / "ref" / "ep16" / "map16.json"
    return json.loads(js.read_text(encoding="utf-8")) if js.exists() else None


def _secz(r, y):
    """断面の目盛り（門番の式）：画面の y → 標高。"""
    return r["z0"] - (y - r["y0"]) / r["k"]


def _area(P):
    return abs(sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(P, list(P[1:]) + [P[0]]))) / 2.0


def _ypath(path, x):
    if x <= path[0][0]:
        return path[0][1]
    for (x0, y0), (x1, y1) in zip(path, path[1:]):
        if x0 <= x <= x1:
            return y0 + (y1 - y0) * (x - x0) / (x1 - x0) if x1 > x0 else y0
    return path[-1][1]


def _morph_at(p, m):
    """描き手（build_jiko._il_morph）と同じ補間：点ごとに直線＋底の点を支えの線へ。"""
    sh = p["shapes"]
    i = min(int(m), len(sh) - 2)
    f = m - i
    pts = [(a[0] + (b[0] - a[0]) * f, a[1] + (b[1] - a[1]) * f) for a, b in zip(sh[i], sh[i + 1])]
    sn = p.get("snap")
    if sn:
        for j in sn["idx"]:
            pts[j] = (pts[j][0], _ypath(sn["path"], pts[j][0]))
    return pts


def _poly_top_at(poly, x):
    """多角形の、縦の線 x との交わりのうち一番上の y（無ければ None）。"""
    ys = []
    for (x0, y0), (x1, y1) in zip(poly, list(poly[1:]) + [poly[0]]):
        if min(x0, x1) <= x <= max(x0, x1) and x1 != x0:
            ys.append(y0 + (y1 - y0) * (x - x0) / (x1 - x0))
    return min(ys) if ys else None


def judge_labels_sec(sc, where):
    """⑨ 断面の札の数と、札の指す高さ・寸法（断面の目盛りで読む＝型の定数を読まない）。"""
    bad, n = [], 0
    for i, t in enumerate(sc["tags"]):
        for txt, at, geo in zip(t.get("texts") or [], t.get("ats") or [None] * 9, t.get("ageo") or [None] * 9):
            # 🔴 ⑤b-4：カンマを外して読む（前は「1,200m」の「200m」だけを読んで、表に無い 200m と言っていた＝VD の札で見つけた）
            tn = str(txt).replace(",", "").replace("，", "")
            km = KM_M.search(tn)
            rg = None if km else RANGE_M.search(tn)
            singles = [] if (rg or km) else [float(v) for v in NUM_M.findall(tn)]
            if not rg and not singles and not km:
                continue
            n += 1
            if geo is None:
                bad.append(f"⑨{where}：段{i + 1}の札「{txt}」に数があるのに、指し先（at）が断面の点でない（高さを読めない）")
                continue
            if km:
                # 🆕 ⑤b-4：キロの横の寸法（「幅1.8km」＝矢印の長さ）
                v = float(km.group(1))
                if v not in REC_LEN_KM:
                    bad.append(f"⑨{where}：札「{txt}」の {v:g}km は記録の表（REC_LEN_KM）に無い")
                elif geo["kind"] != "len":
                    bad.append(f"⑨{where}：札「{txt}」（横の寸法）の指し先が寸法の矢印でない")
                else:
                    L = abs(geo["b"][0] - geo["a"][0]) / geo["k"]
                    want = REC_LEN_KM[v][0]
                    if abs(L - want) > want * KM_TOL:
                        bad.append(f"⑨{where}：札「{txt}」の矢印の長さ {L:.0f}m（記録 {want:g}m ±{KM_TOL * 100:g}%＝{REC_LEN_KM[v][1]}）")
                continue
            if rg:
                lo, hi = float(rg.group(1)), float(rg.group(2))
                if (lo, hi) not in REC_RANGE:
                    bad.append(f"⑨{where}：札「{txt}」の範囲 {lo:g}〜{hi:g}m は記録の表（REC_RANGE）に無い")
                if geo["kind"] != "len":
                    bad.append(f"⑨{where}：札「{txt}」（横の寸法）の指し先が寸法の矢印でない")
                else:
                    L = abs(geo["b"][0] - geo["a"][0]) / geo["k"]
                    if not lo <= L <= hi:
                        bad.append(f"⑨{where}：札「{txt}」の矢印の長さ {L:.0f}m が {lo:g}〜{hi:g}m の外")
                continue
            for v in singles:
                if geo["kind"] == "gap":
                    if v not in REC_GAP:
                        bad.append(f"⑨{where}：札「{txt}」の差 {v:g}m は記録の表（REC_GAP）に無い")
                        continue
                    dz = abs(geo["a"][1] - geo["b"][1]) / geo["k"]
                    ok = (v <= dz <= v + GAP_TOL) if "あまり" in txt else abs(dz - v) <= GAP_TOL
                    if not ok or abs(dz - REC_GAP[v][0]) > GAP_TOL:
                        bad.append(f"⑨{where}：札「{txt}」の寸法の線は {dz:.1f}m（記録 {REC_GAP[v][0]:g}m＝{REC_GAP[v][1]}）")
                elif geo["kind"] == "z":
                    if v not in REC_ELEV:
                        bad.append(f"⑨{where}：札「{txt}」の {v:g}m は記録の表（REC_ELEV）に無い")
                        continue
                    z = _secz(geo["view"], geo["xy"][1])
                    if abs(z - v) > ELEV_TOL:
                        bad.append(f"⑨{where}：札「{txt}」の指す高さは断面の目盛りで {z:.1f}m（札 {v:g}m・許し ±{ELEV_TOL:g}）")
                else:
                    bad.append(f"⑨{where}：札「{txt}」（高さの数）の指し先が横の寸法")
    return bad, n


def judge_records_sec(sc, where):
    """⑩ 記録を越える絵（断面の目盛りで読む）。"""
    bad, n = [], 0
    r = sc.get("ruler")
    if not r:
        return [f"⑩{where}：断面の場面に目盛り（ruler）が無い"], 1
    js = _map16()
    ground = next((p.get("geo") for p in sc["parts"] if (p.get("geo") or {}).get("kind") == "ground"), None)
    if ground is None:
        bad.append(f"⑩{where}：地形の線（ground の geo）が無い")
    for p in sc["parts"]:
        w = p.get("water")
        if not w:
            continue
        n += 1
        top = min(q[1] for q in w["poly"])
        if sc["place"] == "VB":
            z = _secz(r, top)
            if z > REC_SEC["north"][0] + 0.5:
                bad.append(f"⑩{where}：水 {p['id']} の上の縁 {z:.1f}m が北の岸の記録 930m を越える（{REC_SEC['north'][1]}）")
            if ground:
                gl = sorted(ground["line"])
                far = max(_ypath(gl, q[0]) - q[1] for q in w["poly"])
                if far > 24.0:                     # 帯の厚さ（⑤b-3 の下見で 18画素に太くした）＋余白
                    bad.append(f"⑩{where}：水 {p['id']} が地面から {far:.0f}画素上まで盛り上がる（斜面に沿う帯だけ＝谷の真ん中で"
                               "盛り上がる水は描かない）")
        if sc["place"] == "VC" and w.get("dam_x") is not None:
            ty = _poly_top_at(w["poly"], w["dam_x"])
            if ty is None:
                bad.append(f"⑩{where}：越える水がダムの所に無い")
            else:
                h = _secz(r, ty) - REC_SEC["crest"][0]
                lo, hi, rec = REC_SEC["over"]
                if not lo <= h <= hi:
                    bad.append(f"⑩{where}：天端の上の水 {h:.1f}m が {lo:g}〜{hi:g}m の外（{rec}）")
    for p in sc["parts"]:
        g = p.get("geo") or {}
        if g.get("kind") == "dam":
            n += 1
            zt, zb = _secz(r, min(q[1] for q in g["poly"])), _secz(r, max(q[1] for q in g["poly"]))
            want_t, want_b = REC_SEC["crest"][0], REC_SEC["crest"][0] - REC_SEC["height"][0]
            if abs(zt - want_t) > 0.6 or abs(zb - want_b) > 0.6:
                bad.append(f"⑩{where}：ダムの天端 {zt:.1f}m・底 {zb:.1f}m（記録 天端{want_t:g}m・高さ{REC_SEC['height'][0]:g}m＝"
                           f"{REC_SEC['crest'][1]}）")
        elif g.get("kind") in ("lake", "level"):
            n += 1
            z = _secz(r, g["y"])
            if sc["place"] == "VD":
                # 🆕 ⑤b-4：VD は場面ごとに水位が違う（1960年秋 650m・1961年2月 600m・模型 700m と最高 722.5m・その夜 700m）
                #   ＝記録の水位のどれかだけ（門番の側の表 REC_VD["water"]）
                if not any(abs(z - lv) <= 0.5 for lv in REC_VD["water"]):
                    bad.append(f"⑩{where}：湖の水位の線 {z:.1f}m は記録の水位（{sorted(REC_VD['water'])}m）でない")
                continue
            want = REC_SEC["l695"][0] if (p["id"] == "l695") else REC_SEC["lake"][0]
            if abs(z - want) > 0.5:
                bad.append(f"⑩{where}：{p['id']} の水位の線 {z:.1f}m（記録 {want:g}m）")
    for p in sc["parts"]:
        if p.get("kind") != "morph" or not (p.get("obj") or {}).get("block"):
            continue
        n += 1
        sh, nt = p["shapes"], None
        snap = set((p.get("snap") or {}).get("idx") or [])
        nt = min(snap - {0}) if snap else len(sh[0]) // 2
        top0, top1 = sh[0][:nt + 1], sh[-1][:nt + 1]
        shift = sum(b[0] - a[0] for a, b in zip(top0, top1)) / len(top0) / r["k"]
        lo, hi, rec = REC_SEC["shift"]
        if not lo <= shift <= hi:
            bad.append(f"⑩{where}：塊の水平の動き {shift:.0f}m が {lo:g}〜{hi:g}m の外（{rec}）")
        path = (p.get("snap") or {}).get("path")
        if path:
            th = max(_ypath(path, q[0]) - q[1] for q in top0) / r["k"]
            if th > REC_SEC["thick"][0]:
                bad.append(f"⑩{where}：塊の厚さ {th:.0f}m が記録の最大 330m を越える（{REC_SEC['thick'][1]}）")
        if js:
            b = js["sections"]["B"]
            ys = next(y for y, z, _h in b["pts"] if z == 700)               # 南の岸（湖の700mの線）
            xs = r["x0"] + (b["line"][0][1] - ys) * js["m_per_px"] * r["k"]
            pk = max(_secz(r, q[1]) for q in top1 if q[0] >= xs)
            lo, hi, rec = REC_SEC["peak"]
            if not lo <= pk <= hi:
                bad.append(f"⑩{where}：崩れたあとの谷の中の頂上 {pk:.1f}m が {lo:g}〜{hi:g}m の外（{rec}）")
    return bad, n


def judge_vd(sc, where):
    """⑩ VD（正面から見た斜面）：亀裂の折れ目の標高・1960年の崩落の高さと場所・模型の範囲と境・実際の塊の下がり方・波の高さ
    （🆕 ⑤b-4。札の無い絵の高さも、正面の目盛り＝ruler で読む）。"""
    if sc["place"] != "VD":
        return [], 0
    bad, n = [], 0
    r = sc["ruler"]
    k = r["k"]
    geo = {}
    for p in sc["parts"]:
        g = p.get("geo") or {}
        if g.get("kind"):
            geo.setdefault(g["kind"], []).append((p, g))
    crack = next((g for _p, g in geo.get("crack", [])), None)
    if crack:
        n += 1
        zs = [_secz(r, q[1]) for q in crack["line"]]
        turns = [zs[i] for i in range(1, len(zs) - 1) if (zs[i] - zs[i - 1]) * (zs[i + 1] - zs[i]) < 0]
        want, end, rec = REC_VD["crack"]
        if len(turns) != len(want) or any(abs(a - b) > ELEV_TOL for a, b in zip(turns, want)):
            bad.append(f"⑩{where}：亀裂の折れ目の標高 {[round(t) for t in turns]}m が記録 {[round(w) for w in want]}m と違う（{rec}）")
        if abs(zs[-1] - end) > ELEV_TOL:
            bad.append(f"⑩{where}：亀裂の東の端 {zs[-1]:.0f}m が記録 {end:g}m と違う（{rec}）")
        if zs[0] > want[0] + ELEV_TOL:
            bad.append(f"⑩{where}：亀裂の始まり {zs[0]:.0f}m が「1,200m まで上る」より高い（{rec}）")
    dam = next((g for _p, g in geo.get("dam", [])), None)
    dam_w = (sum(q[0] for q in dam["poly"]) / len(dam["poly"]) - r["x0"]) / k if dam else None
    for _p, g in geo.get("c1960", []):
        top_lim, rec = REC_VD["c1960_top"]
        for name, poly in g["polys"].items():
            n += 1
            top = _secz(r, min(q[1] for q in poly))
            if top > top_lim + 0.5:
                bad.append(f"⑩{where}：1960年の崩落（{name}）の上の端 {top:.0f}m が記録の {top_lim:g}m を越える（{rec}）")
        big = max(g["polys"].values(), key=_area)
        if dam_w is not None:
            n += 1
            d = dam_w - (sum(q[0] for q in big) / len(big) - r["x0"]) / k
            lo, hi, rec2 = REC_VD["c1960_from_dam"]
            if not lo <= d <= hi:
                bad.append(f"⑩{where}：1960年の崩落（大きい方）がダムの {d:.0f}m 上流（{lo:g}〜{hi:g}m＝{rec2}）")
    mods = geo.get("model", [])
    for p, g in mods:
        n += 1
        zt, zb = _secz(r, min(q[1] for q in g["poly"])), _secz(r, max(q[1] for q in g["poly"]))
        lo, hi, rec = REC_VD["model_z"]
        if zt > hi + 0.5 or zb < lo - 0.5:
            bad.append(f"⑩{where}：模型の塊 {p['id']} の高さ {zb:.0f}〜{zt:.0f}m が {lo:g}〜{hi:g}m の外（{rec}）")
    if mods:
        n += 1
        if len(mods) != 2:
            bad.append(f"⑩{where}：模型の塊が {len(mods)}つ（2つ＝{REC_VD['model_split']}）")
        elif crack:
            a, b = sorted(mods, key=lambda pg: min(q[0] for q in pg[1]["poly"]))
            gap_x = (max(q[0] for q in a[1]["poly"]) + min(q[0] for q in b[1]["poly"])) / 2.0
            dip = max(crack["line"], key=lambda q: q[1])                 # 亀裂の一番低い所（930m の谷＝沢）
            if abs(dip[0] - gap_x) > SPLIT_TOL:
                bad.append(f"⑩{where}：模型の2つの塊の境 x={gap_x:.0f} が沢（亀裂の 930m の谷 x={dip[0]:.0f}）からずれる"
                           f"（{REC_VD['model_split']}）")
    for p, g in geo.get("whole", []):
        dy = max(float(kk.get("dy", 0.0)) for kk in p["keys"])
        if dy <= 0.0:
            continue
        n += 1
        top = _secz(r, min(q[1] for q in g["poly"]) + dy)
        lo, hi, rec = REC_VD["peak"]
        if not lo <= top <= hi + 0.5:
            bad.append(f"⑩{where}：実際の塊が下がったあとの上の端 {top:.0f}m が {lo:g}〜{hi:g}m の外（{rec}）")
    for _p, g in geo.get("wave", []):
        n += 1
        h = abs(g["a"][1] - g["b"][1]) / k
        want, rec = REC_VD["wave"]
        if abs(h - want) > GAP_TOL:
            bad.append(f"⑩{where}：波の高さの印 {h:.1f}m（記録 {want:g}m＝{rec}）")
        if abs(g["a"][1] - g["level_y"]) > 0.6:
            bad.append(f"⑩{where}：波の高さの印の下の端が湖の水面に無い")
        if not mods:
            bad.append(f"⑩{where}：波の高さの印は模型の想定の場面だけ（{rec}＝模型の答え）")
    return bad, n


def judge_block(sc, where):
    """⑪ 1つの塊：面積を保つ・底が支えに乗る・底の辺が浮かない・支えはつま先から先が地形の線。"""
    bad, n = [], 0
    ground = next((p.get("geo") for p in sc["parts"] if (p.get("geo") or {}).get("kind") == "ground"), None)
    for p in sc["parts"]:
        if p.get("kind") != "morph":
            continue
        n += 1
        sh = p["shapes"]
        a0 = _area(sh[0])
        ms = [float(i) for i in range(len(sh))] + [i + 0.5 for i in range(len(sh) - 1)]
        sn = p.get("snap") or {}
        path = sn.get("path")
        for m in ms:
            pts = _morph_at(p, m)
            ar = _area(pts)
            if abs(ar / a0 - 1.0) > 0.05:
                bad.append(f"⑪{where}：塊の面積が形 {m:g} で {ar / a0 * 100 - 100:+.1f}%（±5% の外＝1つの塊の大きさを保たない）")
                break
            if not path:
                continue
            idx = sorted(sn.get("idx") or [])
            off = max(abs(pts[j][1] - _ypath(path, pts[j][0])) for j in idx)
            if off > 1.0:
                bad.append(f"⑪{where}：形 {m:g} で塊の底の点が支えの線から {off:.1f}画素（浮く・食い込む）")
                break
            base = sorted(pts[j] for j in idx)
            gap = 0.0
            for (x0, y0), (x1, y1) in zip(base, base[1:]):
                for q in path:
                    if x0 < q[0] < x1:
                        cy = y0 + (y1 - y0) * (q[0] - x0) / (x1 - x0)
                        gap = max(gap, q[1] - cy)
            if gap > 3.0:
                bad.append(f"⑪{where}：形 {m:g} で塊の底の辺が支えの線から {gap:.1f}画素浮く（≤3）")
                break
        if not path:
            bad.append(f"⑪{where}：塊の部品に支えの線（snap）が無い＝形のあいだで底が浮く・食い込むのを止められない")
        elif ground:
            gl = sorted(ground["line"])
            sl = sorted((ground.get("slip") or []))
            x_toe = max(q[0] for q in sl) if sl else None
            if x_toe is not None:
                d = max((abs(q[1] - _ypath(gl, q[0])) for q in path if q[0] > x_toe + 0.5), default=0.0)
                if d > 1.0:
                    bad.append(f"⑪{where}：塊の支えの線がつま先から先で地形の線と {d:.1f}画素ちがう（描いた地面の上に乗らない）")
    return bad, n


def judge_night(sc, where):
    """⑬ 夜の場面の動く物・大事な物の色と、夜の地の色の差。"""
    if sc["place"] not in NIGHT_GROUND or sc["start"].get("tod") != "night":
        return [], 0
    import check_color
    pal_name, keys = NIGHT_GROUND[sc["place"]]
    pal = getattr(IL, pal_name)["night"]
    fix = getattr(IL, NIGHT_FIX[sc["place"]])
    body = "".join(p.get("svg", "") for p in sc["parts"] if p["id"] not in ("ground", "sky") and not p.get("signal")).lower()
    bad, n = [], 0
    for nm, col in fix.items():
        if nm.endswith("_ln") or col.lower() not in body:
            continue
        for gk in keys:
            n += 1
            d = check_color.de(col, pal[gk])
            if d < NIGHT_DE:
                bad.append(f"⑬{where}：夜の {nm}（{col}）と地の {gk}（{pal[gk]}）の差 ΔE {d:.1f}（{NIGHT_DE:g} 以上）")
    return bad, n


def _key_end(keys, field, want):
    """鍵の並びで、field が want に着いた時刻（段, 秒）。着かなければ None。"""
    for k in keys:
        v = float(k.get(field, 0.0 if field == "u" else 1.0))
        if (want >= 0.5 and v >= want) or (want < 0.5 and v <= want):
            return (int(k["stage"]), float(k.get("delay", 0.0)) + float(k.get("dur", 0.0)))
    return None


def judge_crowd_water(sc, where, crowd_ok):
    """⑭ 群れと水：群れは水が触れる段までに消える・顔／1人だけ／倒れた形／人数の札を持たない。"""
    if sc["place"] not in ("VA", "VB", "VC", "VD"):    # 16本目の置き場だけ（14・15本目の見本の答えは変えない）
        return [], 0
    crowds = [p for p in sc["parts"] if p.get("role") in crowd_ok and p.get("kind") != "sprite"]
    if not crowds:
        return [], 0
    bad, n = [], 0
    waters = [p for p in sc["parts"] if p.get("water")]
    for c in crowds:
        n += 1
        for flag in ("face", "single", "fallen"):
            if c.get(flag):
                bad.append(f"⑭{where}：群れ {c['id']} が「{flag}」（顔・1人だけの影・倒れた形は描かない）")
        pts = [q for cc in c.get("crowd") or [] for q in (cc.get("pts") or [])] or c.get("bbox_pts") or []
        if not pts:
            continue
        bx0, by0 = min(q[0] for q in pts), min(q[1] for q in pts)
        bx1, by1 = max(q[0] for q in pts), max(q[1] for q in pts)
        hide = _key_end(c["keys"][1:], "a", 0.0) if len(c["keys"]) > 1 else None
        for w in waters:
            wp = w["water"]["poly"]
            if max(q[0] for q in wp) < bx0 or min(q[0] for q in wp) > bx1 or max(q[1] for q in wp) < by0 or \
                    min(q[1] for q in wp) > by1:
                continue
            arrive = _key_end(w.get("go") or w["keys"], "u" if w.get("go") else "a", 1.0)
            if arrive is None:
                continue
            if hide is None or hide > arrive:
                bad.append(f"⑭{where}：群れ {c['id']} が水 {w['id']} の触れたあとも残る（消える {hide}・水 {arrive}）")
    for t in sc["tags"]:
        for txt in t.get("texts") or []:
            if re.search(r"\d+\s*人", txt):
                n += 1
                bad.append(f"⑭{where}：群れのある場面に人数の札「{txt}」（亡くなった人の数を人の形で見せない）")
    return bad, n


def judge_sec(sc, where, crowd_ok=()):
    """16本目 ⑤b-3：⑨⑩⑪（断面）・⑬（夜の色）・⑭（群れと水）。🆕 18本目 ⑤b-2：SA の ⑮⑯⑰（judge_sa）"""
    bad, n = [], 0
    if sc["place"] in SEC_PLACES:
        for fn in (judge_labels_sec, judge_records_sec, judge_block, judge_vd):
            b, m = fn(sc, where)
            bad += b
            n += m
    b, m = judge_night(sc, where)
    bad += b
    n += m
    b, m = judge_sa(sc, where)
    bad += b
    n += m
    # 🆕 18本目 ⑤b-3：SB ⑱・SC ⑲・SD ⑳
    for fn in (judge_sb, judge_sc, judge_sd):
        b, m = fn(sc, where)
        bad += b
        n += m
    b, m = judge_crowd_water(sc, where, crowd_ok)
    return bad + b, n + m


# ══════════════════════════════════════════════════════════
#  🆕 18本目 ⑤b-2（2026-10-04）：SA 横から見た海の ⑮⑯⑰（Vault 映像方針 18本目 §12）
# ══════════════════════════════════════════════════════════
# 🔴 2026-10-06（19本目 ⑤b-1・§0b）：18本目の記録の値（SA・SB・SC・SD の深さ・上げ・音の輪・点・円・目印・札の言い方 ＝下の REC_DEPTH〜REC_SD_ON と
#    SB_DIST_TAGS・SC_NUMS）は selftest の見本 `tools/fixture_ep18.py`（GATES["check_illu"]・値は1つも変えていない＝git の `2d627a2`）へ移した＝空。
#    selftest は `selftest_ep18()`・`selftest_ep18_sbcd()` が見本を差し込んで回す（落ちても終わっても `restore()` で本番の値へ戻す）。
#    19本目で SA〜SD の型を使うときは、その回の記録の値をここに別に持つ（§5b-88）。空のあいだ、深さ・点・円・目印の段は「記録の表に無い」で
#    止まる（fail closed）。許し（DEPTH_TOL・SB_*_TOL・SD_ON_TOL）・正規表現（DIST_NUM）・光の部品の名（SA_LIGHT）は型の側の定数＝残す
REC_DEPTH = {}                       # 記録の深さ（縮尺どおりの段の主体と塗られた線）＝空なら SA の深さの段は「記録の表に無い」で止まる
DEPTH_TOL = 0.03                     # 縮尺どおりの深さの許し（記録の値の 3%）
REC_UP_MAX = (0.0, "記録の表が空（REC_UP_MAX）")     # 艦首の上げの上限（度）
REC_BOOM_CLK = ("0:00", "記録の表が空（REC_BOOM_CLK）")   # 音の輪の時刻
REC_BOOM_WORDS = ()             # 音の輪の段の札に要る言い方（空でも、音の輪は ILLU_BOOM_CUTS と REC_BOOM_CLK で止まる）
SA_LIGHT = ("glow", "flash", "bubble", "fire", "flame", "light", "spark", "smoke")   # 光・泡・炎の部品（⑰＝記録に無い）
SA_DEBRIS_MAX = 1.6                  # 破片が見える（濃さ 0.5 以上）長さの上限＝秒（数えられる前に暗がりへ＝⑮）
DEPTH_NUM = re.compile(r"(\d+(?:\.\d+)?)\s*(m(?![²³2-3])|メートル|フィート|ft)")


def _clk(s):
    """記録の時刻 "9:17"・"9:18.1" → 分（小数まで）。読めなければ None（fail closed）。"""
    m = re.fullmatch(r"\s*(\d{1,2})\s*:\s*(\d{1,2}(?:\.\d+)?)\s*", str(s or ""))
    return int(m.group(1)) * 60 + float(m.group(2)) if m else None


def _stage_on(keys, nst, field="a"):
    """部品の鍵から、段ごとに「その欄が 0 より大きい瞬間があるか」（段の中の鍵と、前の段から持ち越した値）。鍵の無い部品は全部の段で見える。"""
    if not keys:
        return [True] * nst
    ks = sorted(keys, key=lambda k: (int(k["stage"]), float(k.get("delay", 0.0))))
    dflt = 1.0 if field == "a" else 0.0
    out = []
    for i in range(nst):
        before = [k for k in ks if int(k["stage"]) < i]
        inside = [k for k in ks if int(k["stage"]) == i]
        carry = float(before[-1].get(field, dflt)) if before else None
        out.append((carry is not None and carry > 0.004) or any(float(k.get(field, dflt)) > 0.004 for k in inside))
    return out


def _fade_window(keys, half=0.5):
    """破片の濃さの鍵（同じ段の中）から、濃さが half 以上の長さ（秒・余弦の半周の真ん中で half を越える）。"""
    ks = sorted(keys or [], key=lambda k: (int(k["stage"]), float(k.get("delay", 0.0))))
    t_on = t_off = None
    prev = None
    for k in ks:
        a, t0, d = float(k.get("a", 1.0)), float(k.get("delay", 0.0)), float(k.get("dur", 0.0))
        if prev is not None:
            if prev < half <= a and t_on is None:
                t_on = t0 + d / 2.0
            elif prev >= half > a and t_on is not None:
                t_off = t0 + d / 2.0
        prev = a
    return (t_off - t_on) if (t_on is not None and t_off is not None) else None


def judge_sa(sc, where):
    """SA（横から見た海）の場面の ⑮⑯⑰。カットの表（潜水艦の時刻の例外・止めるカット・音の輪のカット）は judge_sa_cut。"""
    if sc["place"] != "SA":
        return [], 0
    bad, n = [], 0
    allst = [sc["start"]] + list(sc["states"])
    nst = max(1, len(sc["states"]))
    P = {p["id"]: p for p in sc["parts"]}
    G = {p["id"]: (p.get("geo") or {}) for p in sc["parts"]}

    def on(pid):
        p = P.get(pid)
        if not p:
            return [False] * nst
        a = _stage_on(p.get("keys"), nst, "a")
        if p.get("kind") == "draw":
            a = [x and y for x, y in zip(a, _stage_on(p.get("go"), nst, "u"))]
        return a
    sub, test, b1, far, b2 = on("sub"), on("test"), on("break1"), on("seabed_far"), on("break2")
    lin = [any(t) for t in zip(on("ruler"), on("seabed"), on("rescue_line"), on("rope"))]
    # ⑯ 深さの目盛り（縮尺どおりの段）に潜水艦を置かない・試験深度の線は切れ目の向こう
    for i in range(nst):
        n += 1
        if sub[i] and lin[i]:
            bad.append(f"⑯{where}：段{i + 1}で深さの目盛り（縮尺どおりの深さ）と潜水艦が同じ段に＝潜水艦の位置から深さの数が"
                       "割り出せる（18本目 §2 ③'）")
        if test[i] and lin[i]:
            bad.append(f"⑯{where}：段{i + 1}で試験深度の線と深さの目盛りが同じ段に＝線の位置から塗られた数が割り出せる")
        if test[i] and not b1[i]:
            bad.append(f"⑯{where}：段{i + 1}の試験深度の線が切れ目（≈）の向こうでない（切れ目1が出ていない）")
        if far[i] and not b2[i]:
            bad.append(f"⑯{where}：段{i + 1}の切れ目の向こうの海底に、試験深度の線とのあいだの切れ目2が無い")
    if "test" in G:
        n += 1
        ty = G["test"].get("y")
        bb = G.get("break1") or {}
        if not bb or not (IL.SA_SURF < bb.get("y0", -1) < bb.get("y1", -1) < ty):
            bad.append(f"⑯{where}：切れ目1 {bb.get('y0')}〜{bb.get('y1')} が海面 {IL.SA_SURF:.0f} と試験深度の線 {ty} のあいだに無い")
        if "seabed_far" in G:
            b2g = G.get("break2") or {}
            if not b2g or not (ty < b2g.get("y0", -1) < b2g.get("y1", -1) < G["seabed_far"]["y"]):
                bad.append(f"⑯{where}：切れ目2 {b2g.get('y0')}〜{b2g.get('y1')} が試験深度の線と海底のあいだに無い")
    # ⑯ 数の札：深さの数は目盛りの段だけ（記録の 260・2,200・2,600m）・切れ目の向こうの海底は 2,600m だけ・試験深度の札に数を書かない
    for i, t in enumerate(sc["tags"]):
        k = min(i, nst - 1)
        for txt, at in zip(t.get("texts") or [], (t.get("ats") or []) + [None] * len(t.get("texts") or [])):
            n += 1
            tn = str(txt).replace(",", "")
            if at == "test" and re.search(r"\d", tn):
                bad.append(f"⑯{where}：試験深度の札「{txt}」に数（公開の記録でも塗られている＝札に数を書かない）")
            for v, unit in DEPTH_NUM.findall(tn):
                ok = (unit == "m" and lin[k] and any(abs(float(v) - r[0]) < 1e-6 for r in REC_DEPTH.values())) or \
                     (unit == "m" and far[k] and not lin[k] and abs(float(v) - REC_DEPTH["seabed"][0]) < 1e-6)
                if not ok:
                    bad.append(f"⑯{where}：段{i + 1}の札「{txt}」の深さの数 {v}{unit} は出せない（目盛りの段の記録の値"
                               f" {[r[0] for r in REC_DEPTH.values()]}m・切れ目の向こうの海底 2600m だけ）")
    # ⑯ 縮尺どおりの深さの幾何＝記録の比（海底 2,600m に対する 260m・2,200m）・目盛りは 260m ごとに 2,600÷260＝10区間
    ruler = G.get("ruler")
    depth = {g["what"]: g for g in G.values() if g.get("kind") == "depth"}
    if depth and not ruler:
        bad.append(f"⑯{where}：縮尺どおりの深さ {sorted(depth)} を描いたのに目盛りが無い")
    if ruler:
        n += 1
        surf, ticks = float(ruler["surf"]), [float(y) for y in ruler["ticks"]]
        want = round(REC_DEPTH["seabed"][0] / REC_DEPTH["rescue"][0])
        steps_px = [b - a for a, b in zip(ticks, ticks[1:])]
        if len(steps_px) != want or (steps_px and max(steps_px) - min(steps_px) > 1.0):
            bad.append(f"⑯{where}：目盛りの区間 {len(steps_px)}（等しい幅か {steps_px[:3]}…）が記録の比 2,600÷260＝{want} と違う")
        base = depth["seabed"]["y"] if "seabed" in depth else ticks[-1]
        if "seabed" in depth and abs(ticks[-1] - base) > 2.0:
            bad.append(f"⑯{where}：目盛りの終わり y{ticks[-1]:.0f} が海底 y{base:.0f} でない")
        for what in ("rescue", "rope"):
            if what in depth:
                n += 1
                m = (float(depth[what]["y"]) - surf) / (base - surf) * REC_DEPTH["seabed"][0]
                rv, rr = REC_DEPTH[what]
                if abs(m - rv) > DEPTH_TOL * rv:
                    bad.append(f"⑯{where}：{what} の線は海底との比で {m:.0f}m（記録 {rv:.0f}m＝{rr}）")
    # ⑮ 潜水艦：描いた段は記録の時刻 clk（読める形）・艦首の上げは記録の上限まで・下がる／圧壊は「推定」の札と一緒に
    for i, st in enumerate(allst):
        if st["sub"] == "off":
            continue
        n += 1
        if _clk(st.get("clk")) is None:
            bad.append(f"⑮{where}：{'頭' if i == 0 else f'段{i}'}で潜水艦を描いたのに記録の時刻 clk が無い／読めない（{st.get('clk')!r}）")
        if float(st["tilt"]) > REC_UP_MAX[0] + 1e-9:
            bad.append(f"⑮{where}：艦首の上げ {st['tilt']}度が記録の上限 {REC_UP_MAX[0]:.0f}度（{REC_UP_MAX[1]}）を越える")
    sink = next(((i, float(sp.get("delay", IL.KEY_DELAY))) for i, (st, sp) in enumerate(zip(sc["states"], sc["steps"]))
                 if st["sub"] in ("sink", "crush")), None)
    if sink or sc["start"]["sub"] in ("sink", "crush"):
        n += 1
        if "推定" not in (sc.get("assume") or ""):
            bad.append(f"⑮{where}：9:17 より後の潜水艦（下がる・圧壊）に「推定」の札が無い（assume=）")
        aa = sc.get("assume_at")
        if aa and sink and (int(aa[0]), float(aa[1])) > sink:
            bad.append(f"⑮{where}：「推定」の札（段{int(aa[0]) + 1}・{aa[1]}秒）が潜水艦の下がり始め（段{sink[0] + 1}・{sink[1]}秒）より遅い")
    for pid in ("debris", "crushed"):
        p = P.get(pid)
        if not p:
            continue
        n += 1
        ks = sorted(p.get("keys") or [], key=lambda k: (int(k["stage"]), float(k.get("delay", 0.0))))
        if not ks or float(ks[-1].get("a", 1.0)) > 0.004:
            bad.append(f"⑮{where}：{pid} が最後まで見えている（壊れた船体は数えられる前に暗がりへ＝最後の段で見える画素0）")
        if p.get("obj"):
            bad.append(f"⑮{where}：{pid} が数（obj）を持つ（塊の数「5か6」は描かない＝数えない形）")
        if pid == "debris":
            w = _fade_window(ks)
            if w is None or w > SA_DEBRIS_MAX:
                bad.append(f"⑮{where}：破片が見える長さ {w} 秒（{SA_DEBRIS_MAX}秒まで＝数えられる前に暗がりへ）")
    # ⑰ 9時18.1分の大きく低い音の輪：圧壊の段・記録の時刻・輪の中心は圧壊した船体・札は認定18 と意見45 の言い方
    boom = P.get("boom")
    if boom:
        for ev in boom.get("pulse") or []:
            n += 1
            i = int(ev["stage"])
            st = sc["states"][i] if i < len(sc["states"]) else sc["start"]
            if st["sub"] != "crush":
                bad.append(f"⑰{where}：段{i + 1}の音の輪が圧壊の段でない（輪は圧壊した船体から＝認定18「emanated from THRESHER」）")
            if _clk(st.get("clk")) != _clk(REC_BOOM_CLK[0]):
                bad.append(f"⑰{where}：段{i + 1}の音の輪の時刻 {st.get('clk')!r} が記録 {REC_BOOM_CLK[0]}（{REC_BOOM_CLK[1]}）でない")
            cc = IL._sa_anchors(st)["crush"]
            if math.hypot(boom["pivot"][0] - cc[0], boom["pivot"][1] - cc[1]) > 3.0:
                bad.append(f"⑰{where}：音の輪の中心 {boom['pivot']} が圧壊した船体 {tuple(round(v) for v in cc)} でない")
            texts = " ".join(sc["tags"][i].get("texts") or []) if i < len(sc["tags"]) else ""
            for w, rr in REC_BOOM_WORDS:
                if w not in texts:
                    bad.append(f"⑰{where}：段{i + 1}の札に「{w}」が無い（{rr}）")
    for p in sc["parts"]:
        if any(w in str(p["id"]).lower() for w in SA_LIGHT):
            bad.append(f"⑰{where}：光・泡・炎の部品 {p['id']}（記録に無い）")
    if any(sp.get("glow") for sp in sc["steps"]):
        bad.append(f"⑰{where}：光の出来事 glow（記録に無い）")
    return bad, n


def judge_sa_cut(scs, cid):
    """⑮⑰ のカットの表：潜水艦は ILLU_SUB_UNTIL（例外 ILLU_SUB_EXC）までの時刻だけ・艦の絵を止めたカット（ILLU_SUB_STOP）より後に
    潜水艦を置かない・下がる／圧壊は例外のカットだけ・9時18.1分の音の輪は ILLU_BOOM_CUTS だけ（表が無ければ空＝全部止める）"""
    ss = _ss()
    until = getattr(ss, "ILLU_SUB_UNTIL", None)
    exc = getattr(ss, "ILLU_SUB_EXC", None) or {}
    stop = getattr(ss, "ILLU_SUB_STOP", None)
    booms = tuple(getattr(ss, "ILLU_BOOM_CUTS", None) or ())
    try:
        import cuts
        order = list(cuts.PLAN)
    except Exception:                                   # noqa: BLE001
        order = []
    bad, n = [], 0
    for sc in scs:
        if sc["place"] != "SA":
            continue
        drawn = [st for st in [sc["start"]] + list(sc["states"]) if st["sub"] != "off"]
        if drawn:
            n += 1
            lim = exc.get(cid, until)
            if _clk(lim) is None:
                bad.append(f"⑮{cid}：潜水艦を描いたのに時刻の上限の表（cuts.ss.ILLU_SUB_UNTIL・ILLU_SUB_EXC）が無い")
            else:
                for st in drawn:
                    c = _clk(st.get("clk"))
                    if c is not None and c > _clk(lim) + 1e-9:
                        bad.append(f"⑮{cid}：{st.get('clk')} の潜水艦（{'例外の上限' if cid in exc else '上限'} {lim} より後）")
            if stop and cid in order and stop in order and order.index(cid) > order.index(stop):
                bad.append(f"⑮{cid}：艦の絵を止めたカット（cuts.ss.ILLU_SUB_STOP＝{stop}）より後に潜水艦")
            if any(st["sub"] in ("sink", "crush") for st in drawn) and cid not in exc:
                bad.append(f"⑮{cid}：潜水艦が下がる・圧壊するのは例外の表（cuts.ss.ILLU_SUB_EXC＝{sorted(exc) or '空'}）のカットだけ")
        if any(p["id"] == "boom" for p in sc["parts"]):
            n += 1
            if cid not in booms:
                bad.append(f"⑰{cid}：9時18.1分の音の輪は表のカット（cuts.ss.ILLU_BOOM_CUTS＝{booms or '空'}）だけ")
    return bad, n


# ══════════════════════════════════════════════════════════
#  🆕 18本目 ⑤b-3（2026-10-04）：SB 上から見た海 ⑱・SC 上から見た海の底 ⑲・SD 横から見た海の底の捜索 ⑳・見る向きの合図 ㉑
# ══════════════════════════════════════════════════════════
REC_SB = {}                        # 上から見た海の記録の点（空なら SB の点は「記録の表に無い」で止まる）
REC_SB_TS = (0.0, 0.0, "記録の表が空（REC_SB_TS）")       # 方位・距離
REC_SB_OIL = (0.0, (0.0, 0.0), "記録の表が空（REC_SB_OIL）")   # 方位・距離の幅
REC_SB_SQ = ((0.0, 0.0), "記録の表が空（REC_SB_SQ）")     # 四角の1辺の幅
SB_POS_TOL, SB_BRG_TOL, SB_DIST_TOL, SB_OIL_BRG_TOL = 2.0, 1.5, 0.03, 11.25   # 画素・度・割合・16方位の幅の半分
SB_DIST_TAGS = ()                 # 距離の札＝言ってよい言い方と、その札が指す線（空なら距離の数は出せない）
DIST_NUM = re.compile(r"(\d+(?:\.\d+)?)\s*(km|キロ|m(?![²³2-3])|メートル|マイル|ヤード|フィート)")
REC_SC_CIRCLE = (0.0, "記録の表が空（REC_SC_CIRCLE）")   # 円の直径
REC_SC_MARKERS = (0, "記録の表が空（REC_SC_MARKERS）")   # 目印の数
SC_NUMS = set()                       # SC の札に出してよい数（空なら数は出せない）
REC_SD_ON = "記録の表が空（REC_SD_ON）"
SD_ON_TOL = 3.0                                      # 船体の一部の真上に「着いた」＝球の下の端と船体の上のすき間（画素）


def _sb_px(ll, view):
    """門番の側の投影（北が上・その見え方の真ん中の緯度で東西を縮める）。見え方の真ん中・原点・縮尺は型の SB_VIEW（記録ではない）。"""
    v = IL.SB_VIEW[view]
    lon0, lat0 = v["c"]
    k = 111320.0 * math.cos(math.radians(lat0))
    return (v["o"][0] + (ll[0] - lon0) * k / v["mpp"], v["o"][1] - (ll[1] - lat0) * 111130.0 / v["mpp"])


def _brg(a, b):
    """画面の点 a → b の真方位（度・北が上）。"""
    return math.degrees(math.atan2(b[0] - a[0], -(b[1] - a[1]))) % 360.0


def _dang(a, b):
    return abs((a - b + 180.0) % 360.0 - 180.0)


def judge_sb(sc, where):
    """⑱ SB：記録の緯度経度の点が記録の位置・スレッシャー↔スカイラークは147度・3,400ヤード・油の帯は9時17分の位置から南東へ7マイルの幅・
    距離の札は言ってよい言い方と線だけ。"""
    if sc["place"] != "SB":
        return [], 0
    bad, n = [], 0
    G = {}
    for p in sc["parts"]:
        g = p.get("geo") or {}
        if g.get("kind") == "pt":
            G.setdefault(g["what"] if g["what"] != "skl" else "skl_" + g.get("at", ""), []).append((p, g))
    for what, rec_key in (("datum", "datum"), ("past", "loran"), ("skl_loran", "loran"), ("skl_meet", "meet"), ("meet", "meet")):
        for p, g in G.get(what, []):
            n += 1
            want = _sb_px(REC_SB[rec_key][0], g.get("view", "near"))
            if math.hypot(g["xy"][0] - want[0], g["xy"][1] - want[1]) > SB_POS_TOL:
                bad.append(f"⑱{where}：{p['id']} の位置 {tuple(round(v) for v in g['xy'])} が記録の緯度経度の位置 "
                           f"{tuple(round(v) for v in want)}（{REC_SB[rec_key][1]}）でない")
    mpp = IL.SB_VIEW["near"]["mpp"]
    meet = _sb_px(REC_SB["meet"][0], "near")
    for p, g in G.get("thr", []):
        n += 1
        b, d = _brg(g["xy"], meet), math.hypot(meet[0] - g["xy"][0], meet[1] - g["xy"][1]) * mpp
        if _dang(b, REC_SB_TS[0]) > SB_BRG_TOL or abs(d - REC_SB_TS[1]) > SB_DIST_TOL * REC_SB_TS[1]:
            bad.append(f"⑱{where}：スレッシャーから見たスカイラーク（待ち合わせの点）が {b:.1f}度・{d:.0f}m（記録 {REC_SB_TS[0]:.0f}度・"
                       f"{REC_SB_TS[1]:.0f}m＝{REC_SB_TS[2]}）")
    lor = _sb_px(REC_SB["loran"][0], "near")
    for p, g in G.get("oil", []):
        n += 1
        b, d = _brg(lor, g["xy"]), math.hypot(g["xy"][0] - lor[0], g["xy"][1] - lor[1]) * mpp
        lo, hi = REC_SB_OIL[1]
        if _dang(b, REC_SB_OIL[0]) > SB_OIL_BRG_TOL or not lo * (1 - SB_DIST_TOL) <= d <= hi * (1 + SB_DIST_TOL):
            bad.append(f"⑱{where}：油の帯が9時17分の位置から {b:.0f}度・{d:.0f}m（記録は南東＝{REC_SB_OIL[0]:.0f}±{SB_OIL_BRG_TOL}度・"
                       f"{lo:.0f}〜{hi:.0f}m＝{REC_SB_OIL[2]}）")
    # 🆕 ⑤b-8（ca02）：捜索の海域の四角＝**描いた線の座標**で測る（型の SB_SQ を読まない）。真ん中が基準の点・一辺が10マイルの幅・
    #   測る線（trk）は四角の中。縮尺は見え方の幾何（型の SB_VIEW＝記録ではない）
    sqs = [p for p in sc["parts"] if (p.get("geo") or {}).get("kind") == "sq"]
    for p in sqs:
        n += 1
        g = p["geo"]
        xs, ys = [q[0] for q in p["path"]], [q[1] for q in p["path"]]
        mpp_v = IL.SB_VIEW[g.get("view", "near")]["mpp"]
        c = ((min(xs) + max(xs)) / 2.0, (min(ys) + max(ys)) / 2.0)
        want = _sb_px(REC_SB["datum"][0], g.get("view", "near"))
        w_m, h_m = (max(xs) - min(xs)) * mpp_v, (max(ys) - min(ys)) * mpp_v
        lo, hi = REC_SB_SQ[0]
        if math.hypot(c[0] - want[0], c[1] - want[1]) > SB_POS_TOL:
            bad.append(f"⑱{where}：捜索の海域の四角の真ん中 {tuple(round(v) for v in c)} が基準の点 {tuple(round(v) for v in want)} でない"
                       f"（{REC_SB_SQ[1]}）")
        for nm, v in (("東西", w_m), ("南北", h_m)):
            if not lo * (1 - SB_DIST_TOL) <= v <= hi * (1 + SB_DIST_TOL):
                bad.append(f"⑱{where}：捜索の海域の四角の{nm}が {v:.0f}m（記録は10マイル＝{lo:.0f}〜{hi:.0f}m＝{REC_SB_SQ[1]}）")
    for p in [p for p in sc["parts"] if (p.get("geo") or {}).get("kind") == "trk"]:
        n += 1
        if not sqs:
            bad.append(f"⑱{where}：測る線（trk）があるのに捜索の海域の四角が無い")
            continue
        xs, ys = [q[0] for q in sqs[0]["path"]], [q[1] for q in sqs[0]["path"]]
        out = [q for q in p["path"] if not (min(xs) <= q[0] <= max(xs) and min(ys) <= q[1] <= max(ys))]
        if out:
            bad.append(f"⑱{where}：測る線が捜索の海域の四角の外に出る（{tuple(round(v) for v in out[0])}）")
    want_ts = f"約{REC_SB_TS[1] / 1000.0:.1f}km"
    for i, t in enumerate(sc["tags"]):
        for txt, at in zip(t.get("texts") or [], (t.get("ats") or []) + [None] * len(t.get("texts") or [])):
            n += 1
            ok = [w for w, a in SB_DIST_TAGS if w in txt]
            if ok and ok[0] == "約3.1km" and ok[0] != want_ts:
                bad.append(f"⑱{where}：札「{txt}」の距離が記録（{want_ts}）と合わない")
            if ok and dict(SB_DIST_TAGS)[ok[0]] != at:
                bad.append(f"⑱{where}：段{i + 1}の札「{txt}」が距離の線（{dict(SB_DIST_TAGS)[ok[0]]}）を指していない（指し先 {at}）")
            rest = txt
            for w, _a in SB_DIST_TAGS:
                rest = rest.replace(w, "")
            if DIST_NUM.search(rest.replace(",", "")):
                bad.append(f"⑱{where}：段{i + 1}の札「{txt}」の距離の数は出せない（言ってよいのは {[w for w, _a in SB_DIST_TAGS]} だけ）")
    return bad, n


def judge_sc(sc, where):
    """⑲ SC：円の直径は記録 400ヤード（±3%）・札は「約370m」と「より広くない」・目印は数えない形（枠の外まで続く・数を持たない）・
    札の数は SC_NUMS だけ。"""
    if sc["place"] != "SC":
        return [], 0
    bad, n = [], 0
    G = {p["id"]: (p, p.get("geo") or {}) for p in sc["parts"]}
    texts = [txt for t in sc["tags"] for txt in (t.get("texts") or [])]
    if "circle" in G:
        n += 1
        p, g = G["circle"]
        d = 2.0 * float(g["r"]) * float(g["mpp"])
        if abs(d - REC_SC_CIRCLE[0]) > DEPTH_TOL * REC_SC_CIRCLE[0]:
            bad.append(f"⑲{where}：円の直径 {d:.0f}m（記録 {REC_SC_CIRCLE[0]:.0f}m＝{REC_SC_CIRCLE[1]}）")
        if not any("より広くない" in t for t in texts):
            bad.append(f"⑲{where}：円の札に「より広くない」が無い（原文 certainly no greater than）")
    if "dia" in G:
        n += 1
        want = f"約{int(round(REC_SC_CIRCLE[0], -1))}m"
        if not any(want in t for t in texts):
            bad.append(f"⑲{where}：直径の線の札に「{want}」が無い（{REC_SC_CIRCLE[1]}）")
    if "markers" in G:
        n += 1
        p, g = G["markers"]
        x0, y0, x1, y1 = g["bbox"]
        if not (x0 < -10 and y0 < -10 and x1 > IL.W + 10 and y1 > IL.H + 10):
            bad.append(f"⑲{where}：目印の並び {tuple(round(v) for v in g['bbox'])} が枠の外まで続かない（数えられる形になる）")
        if p.get("obj"):
            bad.append(f"⑲{where}：目印が数（obj）を持つ（900個は数えない形＝札だけ）")
        if not any(str(REC_SC_MARKERS[0]) in t for t in texts):
            bad.append(f"⑲{where}：目印の札に記録の数 {REC_SC_MARKERS[0]}（{REC_SC_MARKERS[1]}）が無い")
    for t in texts:
        n += 1
        extra = set(re.findall(r"\d+", t.replace(",", ""))) - SC_NUMS
        if extra:
            bad.append(f"⑲{where}：札「{t}」の数 {sorted(extra)} は出せない（{sorted(SC_NUMS)} だけ＝広さの数・塊の数を1つに決めない）")
    return bad, n


def judge_sd(sc, where):
    """⑳ SD：トリエステ2世は最後の段で船体の一部の真上に着く（球の下の端と船体の上 ±3画素・球が船体の幅の内）・深さの切れ目がある・
    深さの数を札に書かない。"""
    if sc["place"] != "SD":
        return [], 0
    bad, n = [], 0
    G = {p["id"]: (p, p.get("geo") or {}) for p in sc["parts"]}
    last = (sc["states"] or [sc["start"]])[-1]
    if "trieste" in G and "hull" in G and last["tri"] == "on":
        n += 1
        p, g = G["trieste"]
        hg = G["hull"][1]
        ks = sorted(p.get("keys") or [], key=lambda k: (int(k["stage"]), float(k.get("delay", 0.0))))
        dy = float(ks[-1].get("dy", 0.0)) if ks else 0.0
        bottom, sx = float(g["bottom"]) + dy, float(g["sph"][0])
        if abs(bottom - float(hg["top"])) > SD_ON_TOL or not float(hg["x0"]) <= sx <= float(hg["x1"]):
            bad.append(f"⑳{where}：トリエステ2世の球の下の端 y{bottom:.0f}（x{sx:.0f}）が船体の一部の上 y{hg['top']:.0f}"
                       f"（x{hg['x0']:.0f}〜{hg['x1']:.0f}）に着いていない（{REC_SD_ON}）")
    n += 1
    if not any(g.get("kind") == "break" for _p, g in G.values()):
        bad.append(f"⑳{where}：深さの切れ目（≈）が無い（船とトリエステ2世と海の底を1枚に入れる＝深さは縮めてある）")
    for t in [txt for tg in sc["tags"] for txt in (tg.get("texts") or [])]:
        n += 1
        if DIST_NUM.search(t.replace(",", "")):
            bad.append(f"⑳{where}：札「{t}」に深さ・距離の数（SD は切れ目で縮めた絵＝数を書かない）")
    return bad, n


def view_dir(sc):
    v = sc.get("view") or ""
    return "上から" if "上から" in v else "横から" if "横から" in v else None


SIG_GAP = 1           # ㉑ あいだに挟まってよい全面の絵でないカットの数（映像方針 18本目 §4 #2＝c308 →〈c309 年表〉→ c310）


def judge_signals(specs, order=None):
    """㉑ 見る向きの合図（ルール 5b-80・映像方針 18本目 §4）：全面の絵のカットを PLAN の順に並べ、すぐ前の全面の絵とのあいだが SIG_GAP
    カットまでで、置き場か見る向き（横から／上から）が替わるカットに合図（切り替えの字 switch・目の印 prev・位置の小さな地図 inset のどれか）が
    あるか。あいだが長い（写真・頁が何枚も挟まる）所は向きの切り替えではない＝向きの札だけ（§4 #4 の注・⑤b-1 の make_plan の数え方を
    1カット広げた）。返り値＝(食い違い, 件数)。"""
    if order is None:
        import cuts
        order = list(cuts.PLAN)
    pos = {c: i for i, c in enumerate(order)}
    bad, n, prev = [], 0, None
    for cid, spec in specs:
        fig = spec.get("fig") or (None, None)
        if fig[0] != "illu" or cid not in pos:
            continue
        sc = getattr(F, "illu")(**fig[1]).illu["scenes"][0]
        d = view_dir(sc)
        if prev and pos[cid] - pos[prev[0]] - 1 <= SIG_GAP and (d != prev[1] or sc["place"] != prev[2]):
            n += 1
            sig = sc.get("inset") or any(p.get("signal") and p["id"] in ("switch", "prev") for p in sc["parts"])
            if not sig:
                bad.append(f"㉑{cid}：{prev[0]}（{prev[2]}・{prev[1]}）→ {sc['place']}（{d}）に替わるのに合図（切り替えの字・目の印・"
                           "位置の小さな地図）が無い")
        prev = (cid, d, sc["place"])
    return bad, n


DESTROY = dict(towns=("gone", "mud"), shore=("gone", "mud"), flood=("on", "recede"), wave_e=("on", "recede"))
DESTROY_SA = dict(sub=("crush",))      # 🆕 18本目 ⑤b-2：潜水艦の圧壊と破片


def judge_destroy(scs, cid, destroy=None):
    """⑫ 壊れる物の部品は表のカットだけ・ダムは壊さない（全部の段で同じ）。🆕 18本目 ⑤b-2：SA の圧壊（sub＝crush）も"""
    destroy = destroy if destroy is not None else tuple(getattr(_ss(), "ILLU_DESTROY_CUTS", None) or ())
    bad, n = [], 0
    for sc in scs:
        if sc["place"] in ("SA", "A1", "A2"):
            # 🆕 19本目 ⑤b-2：A1 の崩れ（真ん中・東・プールデッキ・がれき＝destroy の部品）も表のカットだけ
            #   🆕 ⑤b-3：A2 の落ちた地上の駐車場・デッキの一部・沈んだ車も
            n += 1
            used = sorted({f for st in [sc["start"]] + sc["states"] for f, vs in DESTROY_SA.items() if st.get(f) in vs})
            used += [p["id"] for p in sc["parts"] if p.get("destroy") and p["id"] not in used]
            if used and cid not in destroy:
                bad.append(f"⑫{cid}：壊れる物の部品 {used} は表のカット（cuts.ss.ILLU_DESTROY_CUTS＝{destroy or '空'}）だけ")
            continue
        if sc["place"] not in ("VA", "VB", "VC", "VD"):
            continue
        n += 1
        used = sorted({f for st in [sc["start"]] + sc["states"] for f, vs in DESTROY.items() if st.get(f) in vs})
        if used and cid not in destroy:
            bad.append(f"⑫{cid}：壊れる物の部品 {used} は表のカット（cuts.ss.ILLU_DESTROY_CUTS＝{destroy or '空'}）だけ")
        for p in sc["parts"]:
            if (p.get("obj") or {}).get("dam"):
                n += 1
                ks = p.get("keys") or []
                moved = any(abs(float(k.get(f, d)) - d) > 1e-6 for k in ks for f, d in
                            (("a", 1.0), ("dx", 0.0), ("dy", 0.0), ("rot", 0.0), ("sc", 1.0)))
                if moved or p.get("kind") not in (None, "layer"):
                    bad.append(f"⑫{cid}：ダムの部品が段で変わる（消える・動く）＝ダムは壊さない（S1 p171）")
        if sc["place"] in ("VA", "VC", "VD") and not any((p.get("obj") or {}).get("dam") for p in sc["parts"]):
            bad.append(f"⑫{cid}：ダムの部品が無い（ダムは残る＝S1 p171）")
    return bad, n


# 🆕 19本目 ⑤b-2：㉒ A1（南から見た塔）の記録の値＝門番の側に持つ（§5b-88＝型の定数を読まない）
REC_A1 = dict(
    story_m=33.8 / 12.0,      # TF p3「12 stories 110'-10" (33.8 m)」＝1階の高さ
    drop_m=2.54,              # TR0318「about 100 inches or approximately one story height」
    drop_tag="約2.5m",        # 札に出してよい言い方（台本 c618 と同じ）
    drift_tag="約53cm",       # TR0421「the 12th floor has moved west about 21 inches」（台本 ca18）
    sway_max=60.0,            # 揺れを大きく描く上限（画素・模式＝左下の断りと一緒に）
)


def judge_a1(sc, where):
    """㉒ A1：西の部分は動かない・消えない（TR0002）／屋上の線の下がり＝2.54m÷1階の高さ（±12%）／東は真ん中が落ち始めてから落ちる
    （TR0093・TR0424）／m と cm の札は記録の言い方だけ（約2.5m・約53cm）・cm の札は揺れの段に／揺れは左下の断りと一緒に／人を置かない"""
    if sc["place"] != "A1":
        return [], 0
    bad, n = [], 0
    P = {p["id"]: p for p in sc["parts"]}
    n += 1
    w = P.get("west")
    if not w:
        bad.append(f"㉒{where}：西の部分の部品が無い（立ったまま残った＝TR0002）")
    else:
        moved = any(abs(float(k.get(f, d)) - d) > 1e-6 for k in w.get("keys") or [] for f, d in
                    (("a", 1.0), ("dx", 0.0), ("dy", 0.0), ("rot", 0.0), ("sc", 1.0)))
        if moved or w.get("destroy") or w.get("kind") not in (None, "layer"):
            bad.append(f"㉒{where}：西の部分が段で変わる（消える・動く）＝西の部分は立ったまま残った（TR0002）")
    allst = [sc["start"]] + sc["states"]
    if any(st["a1mid"] == "drop" for st in allst):
        n += 1
        m = P.get("mid")
        fh = float((m or {}).get("geo", {}).get("fh") or 0.0)
        dys = [float(k.get("dy", 0.0)) for k in (m or {}).get("keys") or [] if 0.0 < float(k.get("dy", 0.0)) < 3 * fh]
        want = REC_A1["drop_m"] / REC_A1["story_m"]
        if not fh or not dys or any(abs(d / fh - want) > 0.12 * want for d in dys):
            bad.append(f"㉒{where}：屋上の線の下がり {[round(d / fh, 2) for d in dys] if fh else '?'} 階＝記録は "
                       f"{want:.2f} 階（2.54m÷{REC_A1['story_m']:.2f}m・±12%）")
    if any(st["a1east"] != "on" for st in allst):
        n += 1
        mk = [(int(k["stage"]), float(k.get("delay", 0.0))) for k in (P.get("mid") or {}).get("keys") or []
              if float(k.get("dy", 0.0)) >= 3 * A1FH(P)]
        ek = [(int(k["stage"]), float(k.get("delay", 0.0))) for k in (P.get("east") or {}).get("keys") or []
              if float(k.get("dy", 0.0)) > 0.0]
        mid_fell0 = sc["start"]["a1mid"] in ("fall", "fell")
        if ek and not mid_fell0 and (not mk or min(ek) <= min(mk)):
            bad.append(f"㉒{where}：東の部分が真ん中より先（同時）に落ち始める＝順番は真ん中→東（TR0093・TR0424）")
    texts = [t for tg in sc["tags"] for t in tg["texts"]]
    for i, tg in enumerate(sc["tags"]):
        for t in tg["texts"]:
            n += 1
            for m_ in re.finditer(r"約?\d+(?:\.\d+)?\s*(m|cm)(?![a-zA-Z])", t):
                ok = REC_A1["drop_tag"] if m_.group(1) == "m" else REC_A1["drift_tag"]
                if m_.group(0).replace(" ", "") != ok:
                    bad.append(f"㉒{where}：札「{t}」の {m_.group(0)}＝記録の言い方は「{ok}」だけ")
                if m_.group(1) == "cm" and float(sc["states"][i]["a1sway"]) == 0.0:
                    bad.append(f"㉒{where}：札「{t}」（12階のずれ）を揺れていない段に出した")
    if any(float(st["a1sway"]) != 0.0 for st in allst):
        n += 1
        if any(abs(float(st["a1sway"])) > REC_A1["sway_max"] for st in allst) or "揺れの幅は大きく描いた" not in sc.get("src", ""):
            bad.append(f"㉒{where}：揺れ（a1sway）は {REC_A1['sway_max']:g} 画素まで・左下に「揺れの幅は大きく描いた」の断り")
    if any(p.get("role") or p.get("kind") == "sprite" or p.get("crowd") for p in sc["parts"]):
        bad.append(f"㉒{where}：A1 に人を置いた（人は描かない）")
    return bad, n


# 🆕 19本目 ⑤b-3：㉓ A2（プールデッキと地上の駐車場）・A3（地下の駐車場）の記録の並び＝門番の側に持つ（§5b-88）
REC_A23 = dict(
    park_side="west",          # TR p1176「地上の駐車場の東」に崩れが広がった＝駐車場は西・デッキは東
    gate_row="13.1",           # TR p1123「K-13.1 の近くのプランターと門」
    water_row="13.1",          # TR p1131・p1132「プランターの真東の柱 L-13.1」
    rows_south_to_north=("15", "13.1", "11.1", "9.1"),
    gate_near=60.0,            # A3：門はプランターの箱のすぐ北（画素）
)


def _people(sc):
    return any(p.get("role") or p.get("kind") == "sprite" or p.get("crowd") for p in sc["parts"]) or bool(sc.get("people"))


def judge_a23(sc, where):
    """㉓ A2：駐車場は K の線の西・デッキは東（TR p1176）／つなぎ目は真ん中と東の部分だけ（TR p1059）／門は K の線の 13.1 の上
    （TR p1123）／プランターは K と L のあいだ＝デッキの側（TR p1131）／落ちた範囲は各自の側の中だけ・「推定」の札／ロビーは塔の帯の中。
    A3：右が北（柱の列が南→北＝左→右・塔は右の端）／水・天井・変色の印は柱 13.1（L-13.1）だけ／プランターはその柱の上・門はそのすぐ北／
    左上に位置の小さな地図（A2）。どちらも人を置かない"""
    if sc["place"] not in ("A2", "A3"):
        return [], 0
    bad, n = [], 0
    G = {}
    for p in sc["parts"]:
        g = p.get("geo") or {}
        if g.get("kind"):
            G.setdefault(g["kind"], []).append((p, g))

    def one(k):
        v = G.get(k) or []
        return v[0][1] if v else None
    n += 1
    if _people(sc):
        bad.append(f"㉓{where}：{sc['place']} に人を置いた（人は描かない）")
    if sc["place"] == "A2":
        z, tw = one("a2zones"), one("a2tower")
        n += 1
        if not z or not tw or not (z["x0"] < z["K"] < z["x1"]) or REC_A23["park_side"] != "west":
            bad.append(f"㉓{where}：駐車場とデッキの境（K の線）が描いた敷地の中に無い（駐車場は西・デッキは東＝TR p1176）")
            return bad, n
        j = one("a2join")
        if j:
            n += 1
            if j["x0"] < tw["w1"] - 1 or j["x1"] < tw["m1"] + 1:
                bad.append(f"㉓{where}：デッキのつなぎ目 x {j['x0']:.0f}〜{j['x1']:.0f}＝真ん中と東の部分（x {tw['w1']:.0f}〜）だけ"
                           "（西の部分にはつながない＝TR p1059）")
        gt = one("a2gate")
        if gt:
            n += 1
            r = z["rows"][REC_A23["gate_row"]]
            if abs(gt["x"] - z["K"]) > 1 or not (gt["y0"] <= r <= gt["y1"]):
                bad.append(f"㉓{where}：門 x {gt['x']:.0f}・y {gt['y0']:.0f}〜{gt['y1']:.0f}＝K の線（x {z['K']:.0f}）の "
                           f"{REC_A23['gate_row']}（y {r:.0f}）の上（TR p1123）")
        pl = one("a2planter")
        if pl:
            n += 1
            if not (pl["x0"] >= z["K"] and pl["x1"] <= pl["L"]):
                bad.append(f"㉓{where}：プランター x {pl['x0']:.0f}〜{pl['x1']:.0f}＝K の東（デッキの側）・L の西（柱 L-13.1 は真東＝TR p1131）")
        for p, h in G.get("a2hole") or []:
            n += 1
            x0, y0, x1, y1 = h["r"]
            if (h["zone"] == "park" and x1 > z["K"] + 1) or (h["zone"] == "deck" and x0 < z["K"] - 1):
                bad.append(f"㉓{where}：落ちた範囲（{h['zone']}）x {x0:.0f}〜{x1:.0f} が K の線（x {z['K']:.0f}）を越える")
            if "推定" not in (sc.get("assume") or ""):
                bad.append(f"㉓{where}：落ちた範囲を描いたのに「推定」の札が無い（範囲は記録に無い）")
        lb = one("a2lobby")
        if lb:
            n += 1
            if lb["y1"] > lb["ts"] + 1:
                bad.append(f"㉓{where}：ロビー y {lb['y0']:.0f}〜{lb['y1']:.0f} が塔の南の面（y {lb['ts']:.0f}）より南（塔の1階の外）")
        return bad, n
    rw = one("a3rows")
    n += 1
    if not rw:
        bad.append(f"㉓{where}：柱の列の部品が無い")
        return bad, n
    xs = [rw["rows"][k] for k in REC_A23["rows_south_to_north"]]
    if xs != sorted(xs) or rw["tower"] < xs[-1] - 1:
        bad.append(f"㉓{where}：柱の列 {dict(zip(REC_A23['rows_south_to_north'], xs))}・塔 x {rw['tower']:.0f}＝右が北（南→北が左→右・塔は右）")
    cx = rw["rows"][REC_A23["water_row"]]
    for p, h in G.get("a3mark") or []:
        n += 1
        if abs(h["x"] - cx) > 1:
            bad.append(f"㉓{where}：{h['what']} の印 x {h['x']:.0f}＝柱 L-{REC_A23['water_row']}（x {cx:.0f}）だけ（TR p1131〜p1135）")
    pl, gt = one("a3planter"), one("a3gate")
    if pl:
        n += 1
        if not (pl["x0"] <= cx <= pl["x1"]):
            bad.append(f"㉓{where}：プランターの箱 x {pl['x0']:.0f}〜{pl['x1']:.0f} が柱 L-13.1（x {cx:.0f}）の上に無い（柱はプランターの真東）")
        if gt and not (0.0 <= gt["x0"] - pl["x1"] <= REC_A23["gate_near"]):
            bad.append(f"㉓{where}：門 x {gt['x0']:.0f} がプランターの箱（x 〜{pl['x1']:.0f}）のすぐ北に無い（K-13.1 の近く＝TR p1123）")
    n += 1
    if (sc.get("inset") or {}).get("kind") != "A2":
        bad.append(f"㉓{where}：A3 の左上に位置の小さな地図（上から見た敷地・切り口・目の印）が無い")
    return bad, n


def A1FH(P):
    """真ん中の部分の1階の高さ（部品の geo＝描いた幾何。型の定数は読まない）。部品が無ければ 1（＝落ちた量の比べに使わない）"""
    return float((P.get("mid") or {}).get("geo", {}).get("fh") or 1.0)


def judge_fig(kind, kw, where):
    """型（illu・illu_pair）から場面と上の層を組み、①〜⑤⑧と④を測る。返り値＝(食い違い, 件数, 想定の札の一覧)。"""
    f = getattr(F, kind)(**kw)
    bad, n = [], 0
    for k, sc in enumerate(f.illu["scenes"]):
        b, m = judge_scene(sc, f"{where}#{k + 1}")
        bad += b
        n += m
        b, m = judge_a1(sc, f"{where}#{k + 1}")      # 🆕 19本目 ⑤b-2：㉒
        bad += b
        n += m
        b, m = judge_a23(sc, f"{where}#{k + 1}")     # 🆕 19本目 ⑤b-3：㉓
        bad += b
        n += m
    n += 1
    if f.illu.get("full"):
        asm = f.illu.get("assume", "")
        timed = bool(f.illu.get("assume_at"))
        ov = IL.overlay_svg(f.illu.get("view", ""), f.illu.get("src", ""), asm, timed=timed)
        if "再現イラスト" not in ov or not f.illu.get("src"):
            bad.append(f"④{where}：「再現イラスト」の札か出典が無い")
        if asm and not timed and asm not in ov:
            bad.append(f"④{where}：想定の札「{asm}」が上の層に出ない")
        if asm and timed:
            # 🆕 18本目 ⑤b-2：段の途中で出す想定の札＝絵の層の部品 assume_chip（札の言葉が入り・濃さが 1 まで上がる）
            chip = [p for sc in f.illu["scenes"] for p in sc["parts"] if p["id"] == "assume_chip"]
            if not chip or asm not in chip[0]["svg"] or max(float(k.get("a", 1.0)) for k in chip[0]["keys"]) < 0.999:
                bad.append(f"④{where}：段の途中で出す想定の札「{asm}」の部品が無い／出ない")
    else:
        stages = "".join(f.stages)
        if stages.count("再現イラスト") < len(f.illu["scenes"]) or "出典：" not in f.lab:
            bad.append(f"④{where}：小さく戻す絵の数だけ「再現イラスト」の札が無い／出典が無い")
        if any(sc.get("assume") for sc in f.illu["scenes"]):
            bad.append(f"④{where}：小さく戻す絵に想定の札（assume）は出せない（左上の札が無い）＝パネルの文で言う")
    return bad, n, [sc.get("assume") or "" for sc in f.illu["scenes"]]


def judge_cut(cid, spec, kind_of):
    """カット1つ（SPEC）。⑦＝画面の種類と絵の置き方。"""
    bad, n = [], 0
    kind = kind_of.get(cid) or spec.get("kind")
    fig = spec.get("fig") or (None, None)
    it = (spec.get("intro") or {}).get("illu")
    has_full = fig[0] == "illu"
    has_mini = fig[0] == "illu_pair"
    n += 1
    if kind in NON_ILLU_KINDS and (has_full or has_mini or it):
        bad.append(f"⑦{cid}：画面の種類「{kind}」に再現イラストを置いた（写真・頁・決め所・文字の頁に絵を置かない）")
    # 🆕 18本目 ⑤b-7c：本物の側＝頭の映像（intro foot＝footage.USE の head）か尻の写真・頁（tail）
    real = bool((spec.get("intro") or {}).get("foot") or spec.get("tail"))
    if kind == "再現イラスト" and real:
        bad.append(f"⑦{cid}：全面の絵に本物の映像・写真を差し込んだのに画面の種類が「再現イラスト」＝「混ざり」に（PLAN）")
    if kind == "混ざり" and has_full:
        # 🆕 18本目 ⑤b-2：本物の側（映像・写真）のつなぎ待ちの表（cuts.ss.ILLU_MIX_TODO）のカットは、束ができるまで全面の絵でよい
        #   （参考の行を毎回出す）。束（ILLU_MIX_BUNDLE＝credits.json）ができたら、つないでいないカットは止める（忘れ防止）
        todo = (getattr(_ss(), "ILLU_MIX_TODO", None) or {}).get(cid)
        bundle = getattr(_ss(), "ILLU_MIX_BUNDLE", None)
        if real and todo:
            bad.append(f"⑦{cid}：本物の側をつないだのに cuts.ss.ILLU_MIX_TODO に残っている＝表から外す")
        elif real:
            pass                               # 🆕 ⑤b-7c：つないだ（c102＝頭の記録映画・c103＝尻の写真）
        elif todo and not (bundle and Path(bundle).exists()):
            NOTES.append(f"⚠️ ⑦{cid}：混ざりの本物の側がつなぎ待ち（{todo}）＝いまは SA の段だけを全面の絵で焼く")
        elif todo:
            bad.append(f"⑦{cid}：束（{Path(bundle).name}）ができたのに混ざりの本物の側をつないでいない（{todo}）"
                       "＝つないで cuts.ss.ILLU_MIX_TODO から外す")
        else:
            bad.append(f"⑦{cid}：混ざりに全面の絵（illu）＝画面の種類を「再現イラスト」にするか、冒頭の絵か小さく戻す絵に")
    if kind == "再現イラスト" and not has_full:
        bad.append(f"⑦{cid}：画面の種類「再現イラスト」なのに全面の絵（fig=(\"illu\", …)）で書いていない")
    # 冒頭の絵（intro の illu）＝画面ごと入れ替える（重ねない）。15本目 ⑤b-2 から、あとに来てよいのは
    #   決め所（quote＝14本目 c102・15本目 c104）・全面の絵（illu＝c101 B→A）・時間の帯（axis＝c312 A→帯）
    #   ⑤b-3：尾翼の模式図（tail＝c302 D→模式図）も（14本目の「写真→図」と同じ画面ごとの入れ替え）
    if it and fig[0] not in ("quote", "illu", "axis", "tail"):
        bad.append(f"⑦{cid}：冒頭の絵（intro の illu）のあとは 決め所（quote）・全面の絵（illu）・時間の帯（axis）・尾翼の模式図（tail）だけ")
    elif it and fig[0] == "illu" and kind != "再現イラスト":
        bad.append(f"⑦{cid}：冒頭の絵のあとが全面の絵なら画面の種類は「再現イラスト」（いまは「{kind}」）")
    elif it and fig[0] in ("quote", "axis", "tail") and kind != "混ざり":
        bad.append(f"⑦{cid}：冒頭の絵のあとが決め所・時間の帯・模式図なら画面の種類は「混ざり」（いまは「{kind}」）")
    asm = []
    scs = []
    if has_full or has_mini:
        b, m, asm = judge_fig(fig[0], fig[1], cid)
        bad += b
        n += m
        scs += list(getattr(F, fig[0])(**fig[1]).illu["scenes"])
    if it:
        sc = IL.scene(**it)
        scs.append(sc)
        b, m = judge_scene(sc, f"{cid}#冒頭")
        bad += b
        n += m + 1
        if "再現イラスト" not in IL.overlay_svg(sc["view"], sc["src"], sc.get("assume", "")) or not sc["src"]:
            bad.append(f"④{cid}#冒頭：「再現イラスト」の札か出典が無い")
        if any(t["texts"] for t in sc["tags"]):
            bad.append(f"④{cid}#冒頭：冒頭の絵に札を付けた（段の層は決め所のもの）")
        asm = asm + [sc.get("assume") or ""]
    # ④ 16本目 ⑤b-2：想定の札は表（cuts.ss.ILLU_ASSUME）のカットに、表の言葉で（表に無いカットに出さない・表のカットで落とさない）
    if has_full or has_mini or it:
        n += 1
        want = (getattr(_ss(), "ILLU_ASSUME", None) or {}).get(cid, "")
        got = [a for a in asm if a]
        if want and want not in got:
            bad.append(f"④{cid}：想定のカットなのに想定の札「{want}」が無い（cuts.ss.ILLU_ASSUME）")
        if any(a != want for a in got):
            bad.append(f"④{cid}：想定の札 {got} が表（cuts.ss.ILLU_ASSUME＝{want or 'なし'}）と違う")
    # 🆕 ⑤b-4：小さく戻す絵に模型の想定（VD の model）を描いたら、その問いのパネルの文（k・t）に「想定」（左上の札が出せない）
    if has_mini:
        for blk in fig[1].get("blocks") or []:
            scn = blk.get("scene") or {}
            sts = [dict(scn.get("start") or {})] + [dict(s.get("state") or {}) for s in scn.get("steps") or []]
            if scn.get("place") == "VD" and any(s.get("model", "off") != "off" for s in sts):
                n += 1
                if "想定" not in str(blk.get("k", "")) + str(blk.get("t", "")):
                    bad.append(f"④{cid}：小さく戻す絵に模型の想定を描いたのに、パネルの文（k・t）に「想定」が無い")
    # ⑫ 16本目 ⑤b-3：壊れる物の部品は表のカットだけ・ダムは壊さない
    b, m = judge_destroy(scs, cid)
    bad += b
    n += m
    # ⑮⑰ 18本目 ⑤b-2：潜水艦の時刻・止めるカット・音の輪のカット（表）
    b, m = judge_sa_cut(scs, cid)
    return bad + b, n + m


NOTES = []        # 🆕 18本目 ⑤b-2：止めない参考の行（つなぎ待ちの混ざり）＝main が最後に出す


def _run(cases, kw):
    ok = True
    for name, spec, want in cases:
        try:
            sc = IL.scene(**spec)
            bad, _ = judge_scene(sc, "selftest", **kw)
        except Exception as e:                           # noqa: BLE001
            bad = [f"組めない：{e}"]
        got = not bad
        ok &= got == want
        print(f"  {'OK' if got == want else '🔴 NG'} {name}: {'合格' if got else '不合格'}"
              f"（{'合格' if want else '不合格'}のはず）" + (f"  ← {bad[0]}" if bad else ""))
    return ok


def _expect(name, bad, head):
    good = any(b.startswith(head) for b in bad)
    print(f"  {'OK' if good else '🔴 NG'} {name}: {'不合格' if bad else '合格'}（不合格のはず）" + (f"  ← {bad[0]}" if bad else ""))
    return good


def selftest_ep15():
    """15本目（リノ・⑤b-2〜⑤b-3）の置き場 RA・RB・RC・RD の物差しの検算＝**見本 `fixture_ep15`（15本目の表）を差し込んで**回す。
    🔴 2026-10-01（16本目 ⑤b-1）：本番の表（cuts.ss の REC_DOCS・ILLU_ROLES・ILLU_SEC_OK・ILLU_CLOCK_OK・ILLU_COUNTS ほか）は
       16本目の空の器にした＝15本目の値は `fixture_ep15`（14本目と同じ作り＝記憶 project-jiko-rules-index §0b）。
       差し込んだら原文の頁の読み込み `_pages()`（lru_cache）を捨てて15本目の原文を読み直し、戻したらまた捨てる
       ＝落ちても終わっても `restore()` で本番の値へ戻す（try/finally）。本体は `_selftest_ep15`"""
    import fixture_ep15
    fixture_ep15.apply(sys.modules[__name__])
    _pages.cache_clear()          # 🔴 原文の頁の読み込みは覚えている（lru_cache）＝本番の（空の）原文を捨てて15本目を読み直す
    try:
        return _selftest_ep15()
    finally:
        fixture_ep15.restore()
        _pages.cache_clear()


def _selftest_ep15():
    """15本目の検算の本体（`fixture_ep15` を差し込んだ中で呼ぶ）。"""
    ss = _ss()
    kw = dict(docs=dict(ss.REC_DOCS), pages=_pages(), split=tuple(ss.ILLU_SPLIT_TIMES), until=ss.ILLU_CROWD_UNTIL,
              sec_ok=dict(ss.ILLU_SEC_OK), clock_ok=tuple(ss.ILLU_CLOCK_OK), counts=dict(ss.ILLU_COUNTS),
              roles=dict(ss.ILLU_ROLES))
    # ⑤b-3：RC（ボックス席とピット・地上から）＝観客の群れは落ちる瞬間（16:24:38）より前・役割は spectators だけ
    good_pits = dict(place="RC", at="16:24:28", start=dict(view="pits", crowd="on", fuel="on", cam=1.12, pan=-200.0),
                     rec="AAB p19（ピットのあたりにも多くの観客・燃料車）",
                     steps=[dict(state=dict(pan=200.0), dur=8.0), dict()])
    good_box = dict(place="RC", at="16:24:28", start=dict(view="box", crowd="on", cam=1.12), rec="AAB p19（観客のボックス席）",
                    steps=[dict(), dict()])
    good_fences = dict(place="RC", start=dict(view="fences"), steps=[dict(), dict(), dict()])
    good_near = dict(place="RA", at="16:24", start=dict(view="near", gg="p7"), rec="AAB p28",
                     steps=[dict(), dict(state=dict(gg="gone", path="on", x="on", box="on"), rec="AAB p28・p19",
                                         tag=[dict(t="パイロン8", at="p8"), dict(t="観客席（ボックス席）", at="box")])])
    good_trace = dict(place="RA", at="16:24", start=dict(view="near", gg="gone", path="on", x="on", box="on"), rec="AAB p28",
                      steps=[dict(state=dict(trace="on"), rec="AAB p28", tag=dict(t="崩れ始め 0秒", at="fall0")),
                             dict(tag=dict(t="約9.1秒", at="x"))])
    good_wide = dict(place="RA", at="16:24", start=dict(view="wide"),
                     steps=[dict(state=dict(laps="on", ring8="on"), rec="#14 p3014・AAB p29"),
                            dict(state=dict(seg67="on"), rec="AAB p29")])
    good_rear = dict(place="RB", at="16:24", start=dict(view="rear", roll=73.0), rec="AAB p28",
                     steps=[dict(state=dict(roll=77.0), rec="AAB p28", tag=dict(t="0秒", xy=(1300, 200))),
                            dict(state=dict(roll=81.0, ail="right"), rec="AAB p28", tag=dict(t="0.27秒", xy=(1300, 200)))])
    good_mix = dict(place="RB", at="16:24", start=dict(view="rear", ground="off", roll=86.0), rec="AAB p28",
                    steps=[dict(state=dict(roll=93.0), rec="AAB p28"),
                           dict(state=dict(view="side", pitch=32.0), rec="AAB p28", tag=dict(t="1.3秒 17.3G", xy=(1300, 200)))])
    good_tail = dict(place="RD", at="16:24", steps=[dict(state=dict(mark="on"), rec="AAB p14")])
    cases = [
        ("15本目 正しい RA near（印が7→8・消えて点線・×・ボックス席）", good_near, True),
        ("15本目 正しい RA near（琥珀の線・0秒と約9.1秒の札）", good_trace, True),
        ("15本目 正しい RA wide（3周の航跡・パイロン8の輪・6〜7の区間）", good_wide, True),
        ("15本目 正しい RB rear（73度から深まる・補助翼）", good_rear, True),
        ("15本目 正しい RB rear→side（93度→機首の上げ・17.3G）", good_mix, True),
        ("15本目 正しい RD tail（尾翼の輪）", good_tail, True),
        ("🔴 15本目 陽性対照⑤：札に表に無い秒（#42 の 5.3秒）",
         dict(good_trace, steps=[dict(state=dict(trace="on"), rec="AAB p28", tag=dict(t="5.3秒", at="x"))]), False),
        ("🔴 15本目 陽性対照⑤：札に表に無い時刻（16時25分）",
         dict(good_rear, steps=[dict(state=dict(roll=77.0), rec="AAB p28", tag=dict(t="16時25分", xy=(1300, 200)))]), False),
        ("🔴 15本目 陽性対照①：航跡を出した段に rec が無い", dict(good_wide, steps=[dict(state=dict(laps="on"))]), False),
        ("🔴 15本目 陽性対照①：傾きを変えた段に rec が無い", dict(good_rear, steps=[dict(state=dict(roll=80.0))]), False),
        ("🔴 15本目 陽性対照①：rec の資料名が表に無い（#42）", dict(good_tail, steps=[dict(state=dict(mark="on"), rec="#42 p5")]), False),
        ("🔴 15本目 陽性対照⑧：上から見た絵に寄りすぎ（cam 1.8＝1.39メートル／画素）",
         dict(good_near, start=dict(view="near", gg="p7", cam=1.8)), False),
        ("15本目 正しい RC pits（ピットの柵の奥の観客・燃料車1台・首振り）", good_pits, True),
        ("15本目 正しい RC box（ボックス席の幕の奥の観客・スタンド）", good_box, True),
        ("15本目 正しい RC fences（2つの柵の寄り・人なし・時刻なし）", good_fences, True),
        ("🔴 15本目 陽性対照②：観客の群れを落ちたあと（16:24:40）の場面に", dict(good_box, at="16:24:40"), False),
        ("🔴 15本目 陽性対照②：秒の無い時刻（16:24＝その分の終わりとみなす）", dict(good_box, at="16:24"), False),
        ("🔴 15本目 陽性対照②：群れを出すのに時刻 at が無い", dict(good_box, at=None), False),
        ("🔴 15本目 陽性対照①：群れを出したのに場面の rec が無い", dict(good_box, rec=None), False),
    ]
    ok = _run(cases, kw)
    # 🔴 陽性対照②（役割）：15本目に14本目の役割（乗客の群れ・船員の型紙）を置く＝回ごとの表で止まる
    sc = IL.scene(**good_box)
    next(p for p in sc["parts"] if p.get("role") == "spectators")["role"] = "passengers"
    ok &= _expect("🔴 15本目 陽性対照②：観客の群れの役割を passengers に（14本目の役割）", judge_scene(sc, "selftest", **kw)[0], "②")
    sc = IL.scene(**good_fences)
    sc["parts"].append(dict(IL._part("pilot", "", "AAB p11"), kind="sprite", role="crew", inst=[dict(path=[(900.0, 600.0)])]))
    ok &= _expect("🔴 15本目 陽性対照②：型紙の影（crew＝1人ずつ数えられる人）を置く", judge_scene(sc, "selftest", **kw)[0], "②")
    # 🔴 陽性対照②（形）：描く側の群れの間隔を壊す（1.15＝重ならない）＝1人ずつ数えられる群れ
    keep = IL.CROWD_STEP
    IL.CROWD_STEP = 1.15
    try:
        bad = judge_scene(IL.scene(**good_pits), "selftest", **kw)[0]
    finally:
        IL.CROWD_STEP = keep
    ok &= _expect("🔴 15本目 陽性対照②（描く側）：ピットの群れが重ならない（数えられる）", bad, "②")
    # 🔴 陽性対照③：RC の燃料車を2台に
    sc = IL.scene(**good_pits)
    g = next(q for q in sc["parts"] if (q.get("obj") or {}).get("fuel_truck"))
    g["obj"] = dict(g["obj"], fuel_truck=2)
    ok &= _expect("🔴 15本目 陽性対照③：RC の燃料車を2台描く", judge_scene(sc, "selftest", **kw)[0], "③")
    # 🔴 位置の正本（`ref/ep15/illu_reno.json`＝`ref/ep15/measure_reno.py` が図の画素から測った値）と `illu.py` の定数が同じか
    #    （写し間違い・手で動かした値を止める。⑤b-2 で scratchpad の手の丸めと 0〜1メートル違っていたのを直した）
    js = HERE / "ref" / "ep15" / "illu_reno.json"
    if js.exists():
        import json
        g = json.loads(js.read_text(encoding="utf-8"))
        diff = [k for k in IL.R_ORDER if tuple(float(x) for x in g["pylons"][k]) != IL.R_PYL[k]]
        diff += ["accident"] if tuple(float(x) for x in g["accident"]) != IL.R_ACC else []
        diff += ["S0"] if tuple(g["S0"]) != IL.R_S0 else []
        diff += [n for n in IL.R_LAPS if [tuple(p) for p in g["laps"][n]] != list(IL.R_LAPS[n])]
        diff += ["showline_deg"] if abs(g["showline_deg"] - IL.R_SHOW_DEG) > 1e-9 else []
        diff += ["R_GG・R_FALL の端"] if (IL.R_GG[-1] != tuple(float(x) for x in g["laps"]["lap3"][-1])
                                        or IL.R_FALL[0] != IL.R_GG[-1] or IL.R_FALL[-1] != IL.R_ACC) else []
        print(f"  {'OK' if not diff else '🔴 NG'} 15本目 位置の正本 illu_reno.json と illu.py の定数: "
              f"{'同じ' if not diff else '違う ' + str(diff)}")
        ok &= not diff
    else:
        print("  ⚠️ 15本目 位置の正本 ref/ep15/illu_reno.json が無い＝照合していない")
    # 🔴 陽性対照③（数）：事故機の印を2つ（部品を複写）・燃料車を2台（地面の obj を壊す）
    sc = IL.scene(**good_near)
    p = next(q for q in sc["parts"] if (q.get("obj") or {}).get("aircraft"))
    sc["parts"].append(dict(p, id="gg2"))
    ok &= _expect("🔴 15本目 陽性対照③：事故機を2つ描く", judge_scene(sc, "selftest", **kw)[0], "③")
    sc = IL.scene(**good_near)
    g = next(q for q in sc["parts"] if (q.get("obj") or {}).get("fuel_truck"))
    g["obj"] = dict(g["obj"], fuel_truck=2)
    ok &= _expect("🔴 15本目 陽性対照③：燃料車を2台描く", judge_scene(sc, "selftest", **kw)[0], "③")
    # 🔴 陽性対照⑧（描く側の定数を壊す）：near の縮尺を 1.2 メートル／画素に
    keep = IL.RA_VIEW["near"]["mpp"]
    IL.RA_VIEW["near"]["mpp"] = 1.2
    try:
        bad = judge_scene(IL.scene(**good_near), "selftest", **kw)[0]
    finally:
        IL.RA_VIEW["near"]["mpp"] = keep
    ok &= _expect("🔴 15本目 陽性対照⑧（描く側）：near の縮尺 1.2", bad, "⑧")
    # 🔴 陽性対照⑨（描く側）：後ろから見た機体を下げて大きく（⑤b-2 の下見の前の値）＝93度で翼の先が地平線に届く
    keep = (IL.RB_CR, IL.RB_KR)
    IL.RB_CR, IL.RB_KR = (960.0, 430.0), 62.0
    try:
        bad = judge_scene(IL.scene(**good_mix), "selftest", **kw)[0]
    finally:
        IL.RB_CR, IL.RB_KR = keep
    ok &= _expect("🔴 15本目 陽性対照⑨（描く側）：後ろから見た機体を下げる（翼の先が地平線に届く）", bad, "⑨")
    # 🔴 陽性対照⑦：冒頭の絵のあとがパネル／時間の帯なのに種類が「再現イラスト」
    for name, spec, kind in (("冒頭の絵のあとがパネル", dict(fig=("panel", dict(blocks=[])), intro=dict(illu=good_tail)), "混ざり"),
                             ("冒頭の絵→時間の帯なのに種類が「再現イラスト」",
                              dict(fig=("axis", dict()), intro=dict(illu=good_tail)), "再現イラスト")):
        bad = [b for b in judge_cut("x9", spec, {"x9": kind})[0] if b.startswith("⑦")]
        ok &= _expect(f"🔴 15本目 陽性対照⑦：{name}", bad, "⑦")
    bad = [b for b in judge_cut("x8", dict(fig=("illu", good_near), intro=dict(illu=good_mix)), {"x8": "再現イラスト"})[0]
           if b.startswith("⑦")]
    print(f"  {'OK' if not bad else '🔴 NG'} 15本目 正しい ⑦：冒頭の絵（B）→ 全面の絵（A）＝再現イラスト: "
          f"{'合格' if not bad else '不合格'}（合格のはず）" + (f"  ← {bad[0]}" if bad else ""))
    ok &= not bad
    return ok


def selftest_ep16():
    """16本目（バイオントダム災害）の検算＝**見本 `fixture_ep16`（16本目の表）を差し込んで**回す。
    🔴 2026-10-04（18本目 ⑤b-1）：本番の表（cuts.ss の REC_DOCS・ILLU_SPLIT_TIMES・ILLU_CLOCK_OK・ILLU_COUNTS ほか／この門番の REC_ELEV・
       REC_GAP・REC_RANGE・REC_SEC・REC_VD・REC_LEN_KM・REC_VA・VA_GRID_PX）は18本目の空の器にした＝16本目の値は `fixture_ep16`
       （14・15本目と同じ作り＝記憶 project-jiko-rules-index §0b）。差し込んだら原文の頁の読み込み `_pages()`（lru_cache）を捨てて
       16本目の原文を読み直し、戻したらまた捨てる＝落ちても終わっても `restore()` で本番の値へ戻す（try/finally）。本体は `_selftest_ep16`"""
    import fixture_ep16
    fixture_ep16.apply(sys.modules[__name__])
    _pages.cache_clear()          # 🔴 原文の頁の読み込みは覚えている（lru_cache）＝本番の（空の）原文を捨てて16本目を読み直す
    try:
        return _selftest_ep16()
    finally:
        fixture_ep16.restore()
        _pages.cache_clear()


def _selftest_ep16():
    """16本目の検算の本体（`fixture_ep16` を差し込んだ中で呼ぶ）。
    ⑤b-2：⑤ 時計と秒の札（映像方針 §9 ⑤＝秒の札は出さない〈ILLU_SEC_OK＝空〉・時計は 22:39 だけ・22:00 と 22:15 は割れる）"""
    ss = _ss()
    split, sec_ok, clock_ok = tuple(ss.ILLU_SPLIT_TIMES), dict(ss.ILLU_SEC_OK), tuple(ss.ILLU_CLOCK_OK)
    ok = True
    # 🔴 本番の表そのものが16本目の決めのとおりか（表を書き換えた・空のまま忘れたを止める＝門番の側に決めを持つ §5b-88）
    want = dict(split=("22:00", "22:15"), sec_ok={}, clock_ok=("22:39",))
    got = dict(split=split, sec_ok=sec_ok, clock_ok=clock_ok)
    diff = [k for k in want if want[k] != got[k]]
    print(f"  {'OK' if not diff else '🔴 NG'} 16本目 ⑤ の表（割れる時刻・秒・時計）が映像方針 §9 ⑤ のとおり: "
          f"{'同じ' if not diff else '違う ' + str({k: got[k] for k in diff})}")
    ok &= not diff
    cases = [
        ("16本目 正しい ⑤：時計「22:39」", ["22:39"], True),
        ("16本目 正しい ⑤：日付と時計「1963年10月9日 22:39」", ["1963年10月9日 22:39"], True),
        ("16本目 正しい ⑤：時計「22時39分」", ["22時39分"], True),
        ("16本目 正しい ⑤：時計でない「時」（約1時間・時速50〜60km）", ["約1時間", "時速50〜60km"], True),
        ("16本目 正しい ⑤：時刻も秒も無い札（ダム・930m・天端の上100〜140m）", ["ダム", "930m", "天端の上100〜140m"], True),
        ("🔴 16本目 陽性対照⑤：秒の札（45秒足らず）", ["45秒足らず"], False),
        ("🔴 16本目 陽性対照⑤：秒の札（約1秒）", ["約1秒"], False),
        ("🔴 16本目 陽性対照⑤：22:39 以外の時計（22:40）", ["22:40"], False),
        ("🔴 16本目 陽性対照⑤：22:39 以外の時計（9時45分）", ["9時45分"], False),
        ("🔴 16本目 陽性対照⑤：割れる時刻（22時15分＝電話）", ["22時15分"], False),
        ("🔴 16本目 陽性対照⑤：割れる時刻（22:00）", ["22:00"], False),
        ("🔴 16本目 陽性対照⑤：分の無い時計（22時ごろ）", ["22時ごろ"], False),
        ("🔴 16本目 陽性対照⑤：2つ目の時刻だけ表の外（22:39 と 22:41）", ["22:39 → 22:41"], False),
        ("🔴 16本目 陽性対照⑤：左下の出典の行の時刻（判定は札と同じ）", ["出典：…（22:15 の電話）"], False),
    ]
    for name, texts, want_ok in cases:
        bad, _ = judge_labels(texts, "selftest", split, sec_ok, clock_ok)
        got_ok = not bad
        ok &= got_ok == want_ok
        print(f"  {'OK' if got_ok == want_ok else '🔴 NG'} {name}: {'合格' if got_ok else '不合格'}"
              f"（{'合格' if want_ok else '不合格'}のはず）" + (f"  ← {bad[0]}" if bad else ""))
    ok_va = _selftest_ep16_va(ss)
    ok_sec = _selftest_ep16_sec(ss)
    ok_vd = _selftest_ep16_vd(ss)
    return ok_va and ok_sec and ok_vd and ok


def _selftest_ep16_sec(ss):
    """16本目 ⑤b-3：断面 VB・VC の検算（⑨〜⑭）＝本番の表で回す。陽性対照は**型の定数を壊す形**（§5b-88）。"""
    kw = dict(docs=dict(ss.REC_DOCS), pages=_pages(), split=tuple(ss.ILLU_SPLIT_TIMES), until=ss.ILLU_CROWD_UNTIL,
              sec_ok=dict(ss.ILLU_SEC_OK), clock_ok=tuple(ss.ILLU_CLOCK_OK), counts=dict(ss.ILLU_COUNTS),
              roles=dict(ss.ILLU_ROLES))
    RB_, RC_ = IL.VB_REC, IL.VC_REC
    g101 = dict(place="VB", at="22:39", start=dict(view="wide"), rec="S1 p98・S1 p96",
                steps=[dict(tag=dict(t="1963年10月9日 22:39", xy=(1840, 178), anchor="end")),
                       dict(state=dict(move=1.0, runup="on"), rec=RB_["block"] + "・" + RB_["runup"], run_hold=0.5)])
    g806 = dict(place="VB", start=dict(view="wide", move=0.35, other="C"), rec=RB_["block"],
                steps=[dict(state=dict(move=1.0), rec=RB_["block"]),
                       dict(state=dict(dim="on"), rec=RB_["dim"], tag=dict(t="水平に300〜400m", at="dim", anchor="middle"))])
    g810 = dict(place="VB", start=dict(view="wide", move=1.0, other="C"), rec=RB_["block"],
                steps=[dict(state=dict(ghost="on", path="on"), rec=RB_["block"]),
                       dict(state=dict(ghost="off", path="off"), rec=RB_["peak"], tag=dict(t="866m", at="peak")),
                       dict(state=dict(level="on", bracket="on"), rec=RB_["level"],
                            tag=[dict(t="崩れる前の水面", at="level"), dict(t="165m", at="rise")])])
    g811 = dict(place="VB", start=dict(view="wide", move=1.0, other="C"), rec=RB_["block"],
                steps=[dict(state=dict(level="on"), rec=RB_["level"]), dict(state=dict(runup="over"), rec=RB_["runup"])])
    g106 = dict(place="VC", at="22:39", start=dict(view="wide", other="B"), rec=RC_["lake"] + "・" + RC_["gap"],
                steps=[dict(state=dict(south="on"), rec=RC_["south"],
                            tag=[dict(t="天端725.5m", at="crest"), dict(t="水位約700m", at="lake"), dict(t="南の岸から", at="south")]),
                       dict(state=dict(over="on"), rec=RC_["over"])])
    g721 = dict(place="VC", start=dict(view="near", switch="on", other="B"), rec=RC_["lake"],
                steps=[dict(tag=dict(t="約700m", at="lake")), dict(),
                       dict(state=dict(gap="on"), rec=RC_["gap"],
                            tag=[dict(t="天端725.5m", at="crest"), dict(t="25mあまり", at="gap")])])
    g708 = dict(place="VC", start=dict(view="near", tod="day", other="B"), rec=RC_["lake"],
                steps=[dict(tag=dict(t="約700m", at="lake")), dict(state=dict(l695="on"), rec=RC_["l695"],
                                                                 tag=dict(t="695m", at="l695"))])
    g817 = dict(place="VC", start=dict(view="wide", over="on", other="B"), rec=RC_["over"],
                steps=[dict(), dict(state=dict(hbr="on"), rec=RC_["over"], tag=dict(t="天端", at="crest"))])
    cases = [("16本目 正しい VB c101（崩れる前→塊が北の岸へ・水が930mまで→引く）", g101, True),
             ("16本目 正しい VB c806（水平に300〜400m の矢印）", g806, True),
             ("16本目 正しい VB c810（866m・崩れる前の水面・165m）", g810, True),
             ("16本目 正しい VB c811（崩れたあとの絵の上で水が930mまで）", g811, True),
             ("16本目 正しい VC c106（天端725.5m・水位約700m・南の岸から・天端を越える水）", g106, True),
             ("16本目 正しい VC c721（near・約700m・天端725.5m・25mあまり）", g721, True),
             ("16本目 正しい VC c708（near・昼・約700m・695m）", g708, True),
             ("16本目 正しい VC c817（越えた水・天端・寸法の線＝数なし）", g817, True),
             ("🔴 16本目 陽性対照⑨：「866m」を湖の水面（700m）に付ける",
              dict(g810, steps=[dict(state=dict(level="on"), rec=RB_["level"], tag=dict(t="866m", at="lake"))]), False),
             ("🔴 16本目 陽性対照⑨：記録の表に無い高さ「900m」",
              dict(g810, steps=[dict(state=dict(level="on"), rec=RB_["level"], tag=dict(t="900m", at="peak"))]), False),
             ("🔴 16本目 陽性対照⑨：「25mあまり」を天端→水の上（120m）の線に付ける",
              dict(g817, steps=[dict(), dict(state=dict(hbr="on"), rec=RC_["over"], tag=dict(t="25mあまり", at="hbr"))]), False),
             ("🔴 16本目 陽性対照⑨：横の寸法「水平に300〜400m」を高さの点に付ける",
              dict(g806, steps=[dict(state=dict(move=1.0), rec=RB_["block"]),
                                dict(state=dict(dim="on"), rec=RB_["dim"], tag=dict(t="水平に300〜400m", at="peak"))]), False)]
    ok = _run(cases, kw)
    # 🔴 型の定数を壊す陽性対照（門番が型の定数を読まない＝§5b-88）
    breaks = [
        ("⑨⑩ 天端を 735.5m で描く型（VC_DAM の crest）", "VC_DAM", dict(IL.VC_DAM, crest=735.5), g721, ("⑨", "⑩")),
        ("⑩ ダムの高さを 250m で描く型", "VC_DAM", dict(IL.VC_DAM, height=250.0), g106, ("⑩",)),
        ("⑩ 天端の上の水を 160m で描く型（VC_OVER）", "VC_OVER", 160.0, g106, ("⑩",)),
        ("⑨⑩ 塊を水平に 450m 運ぶ型（VB_D）", "VB_D", 450.0, g806, ("⑨", "⑩")),
        ("⑩ 北の岸の水の上限を 960m にした型（VB_RUN_TOP）", "VB_RUN_TOP", 960.0, g101, ("⑩",)),
        ("⑩ すべり面の座を 470m に下げた型（頂上が866mを越える）", "VB_SLIP", IL.vb_slip_of(470.0), g810, ("⑩",)),
        ("⑬ 塊を夜の地に近い色で描く型（VB_FIX の block）", "VB_FIX", dict(IL.VB_FIX, block="#2f3a4c"), g101, ("⑬",)),
    ]
    for name, attr, val, spec, heads in breaks:
        keep = getattr(IL, attr)
        setattr(IL, attr, val)
        try:
            bad = judge_scene(IL.scene(**spec), "selftest", **kw)[0]
        except Exception as e:                           # noqa: BLE001
            bad = [f"組めない：{e}"]
        finally:
            setattr(IL, attr, keep)
        good = all(any(b.startswith(h) for b in bad) for h in heads)
        print(f"  {'OK' if good else '🔴 NG'} 16本目 陽性対照（型）{name}: {'不合格' if bad else '合格'}（{'・'.join(heads)}で不合格のはず）"
              + (f"  ← {bad[0]}" if bad else ""))
        ok &= good
    # 🔴 陽性対照⑩：谷の真ん中で盛り上がる水（斜面に沿わない水の部品を足す）
    sc = IL.scene(**g101)
    r = sc["ruler"]
    x0, x1 = r["x0"] + 1450 * r["k"], r["x0"] + 1600 * r["k"]
    ytop = r["y0"] + (r["z0"] - 800.0) * r["k"]
    sc["parts"].append(dict(id="mound", svg="", rec=IL.VB_REC["runup"], keys=[dict(stage=0, delay=0.0)], kind="layer",
                            pivot=[0, 0], water=dict(poly=[[x0, 700.0], [(x0 + x1) / 2, ytop], [x1, 700.0]])))
    ok &= _expect("🔴 16本目 陽性対照⑩：谷の真ん中で盛り上がる水", judge_scene(sc, "selftest", **kw)[0], "⑩")
    # 🔴 陽性対照⑪：底を支えの線へ乗せ直さない塊（形のあいだで谷底の上に浮く）・面積を 1.1倍にした形
    sc = IL.scene(**g101)
    blk = next(p for p in sc["parts"] if p["id"] == "block")
    blk.pop("snap")
    ok &= _expect("🔴 16本目 陽性対照⑪：支えの線（snap）の無い塊", judge_block(sc, "selftest")[0], "⑪")
    sc = IL.scene(**g101)
    blk = next(p for p in sc["parts"] if p["id"] == "block")
    cx = sum(q[0] for q in blk["shapes"][5]) / len(blk["shapes"][5])
    cy = sum(q[1] for q in blk["shapes"][5]) / len(blk["shapes"][5])
    blk["shapes"][5] = [[cx + (q[0] - cx) * 1.1, cy + (q[1] - cy) * 1.1] for q in blk["shapes"][5]]
    ok &= _expect("🔴 16本目 陽性対照⑪：途中の形を真ん中から1.1倍に広げる（底は支えへ乗せ直される）", judge_block(sc, "selftest")[0], "⑪")
    # 🔴 陽性対照⑫：表に無いカットで町の面を消す・ダムが段で消える・表が空
    g823 = dict(place="VA", start=dict(view="west", block="on"), rec=IL.VA_REC["block"],
                steps=[dict(state=dict(wave_w="on", flood="on", towns="gone"), rec=IL.VA_REC["flood"])])
    sc = IL.scene(**g823)
    b, _ = judge_destroy([sc], "c823")
    print(f"  {'OK' if not b else '🔴 NG'} 16本目 正しい⑫：c823（表のカット）で町の面が消える: {'合格' if not b else b[0]}")
    ok &= not b
    ok &= _expect("🔴 16本目 陽性対照⑫：表に無いカット（c815）で町の面を消す", judge_destroy([sc], "c815")[0], "⑫")
    ok &= _expect("🔴 16本目 陽性対照⑫：表が空（fail closed）", judge_destroy([sc], "c823", destroy=())[0], "⑫")
    sc = IL.scene(**g106)
    dam = next(p for p in sc["parts"] if (p.get("obj") or {}).get("dam"))
    dam["keys"] = [dict(stage=0, delay=0.0, a=1.0), dict(stage=1, delay=0.5, dur=0.5, a=0.0)]
    ok &= _expect("🔴 16本目 陽性対照⑫：ダムが段で消える", judge_destroy([sc], "c106")[0], "⑫")
    # 🔴 陽性対照⑭（いまの絵コンテに群れは無い＝陽性対照だけ）：水が触れたあとも残る群れ・顔・人数の札
    lay = IL.crowd_layout(120.0, 300.0, 560.0, 26.0)
    crowd = dict(id="crowd", svg="", rec=IL.VA_REC["towns"], kind="layer", pivot=[0, 0], role="residents",
                 crowd=[dict(layout=lay, x0=120.0, x1=300.0)], bbox_pts=[[130, 480], [290, 560]],
                 keys=[dict(stage=0, delay=0.0, a=1.0)])
    sc = IL.scene(**g823)
    sc["parts"].append(dict(crowd))
    ok &= _expect("🔴 16本目 陽性対照⑭：水が触れたあとも残る群れ", judge_crowd_water(sc, "selftest", ("residents",))[0], "⑭")
    sc = IL.scene(**g823)
    sc["parts"].append(dict(crowd, keys=[dict(stage=0, delay=0.0, a=1.0), dict(stage=0, delay=0.3, dur=0.3, a=0.0)]))
    b, _ = judge_crowd_water(sc, "selftest", ("residents",))
    print(f"  {'OK' if not b else '🔴 NG'} 16本目 正しい⑭：水が触れる前に消える群れ: {'合格' if not b else b[0]}")
    ok &= not b
    sc = IL.scene(**g823)
    sc["parts"].append(dict(crowd, face=True, keys=[dict(stage=0, delay=0.0, a=1.0), dict(stage=0, delay=0.3, dur=0.3, a=0.0)]))
    ok &= _expect("🔴 16本目 陽性対照⑭：顔のある群れ", judge_crowd_water(sc, "selftest", ("residents",))[0], "⑭")
    sc = IL.scene(**dict(g823, steps=[dict(state=dict(wave_w="on", flood="on", towns="gone"), rec=IL.VA_REC["flood"],
                                           tag=dict(t="約300人", at="longarone"))]))
    sc["parts"].append(dict(crowd, keys=[dict(stage=0, delay=0.0, a=1.0), dict(stage=0, delay=0.3, dur=0.3, a=0.0)]))
    ok &= _expect("🔴 16本目 陽性対照⑭：群れのある場面に人数の札", judge_crowd_water(sc, "selftest", ("residents",))[0], "⑭")
    # 🔴 正本（map16.json の sections）と illu.py の断面の定数が同じか
    js = _map16()
    if js:
        b = js["sections"]["B"]
        c = js["sections"]["C"]
        diff = [] if [(float(y), float(z)) for y, z, _h in b["pts"]] == [(float(y), float(z)) for y, z in IL.VB_PTS] else ["B.pts"]
        diff += [] if float(b["line"][0][1]) == IL.VB_Y0 and float(b["line"][0][0]) == IL.VA_CUT["B"]["a"][0] else ["B.line"]
        diff += [] if float(c["line"][0][0]) == IL.VC_X0E and float(c["line"][0][1]) == IL.VA_CUT["C"]["a"][1] else ["C.line"]
        diff += [] if abs(c["dam_base"] - IL.VC_BED_REC["base"]) < 1e-6 else ["C.dam_base"]
        diff += [] if (tuple(c["gorge_exit"][:2]), float(c["gorge_exit"][2])) == IL.VC_BED_REC["exit"] else ["C.gorge_exit"]
        diff += [] if (tuple(c["lake_end"][:2]), float(c["lake_end"][2])) == IL.VC_BED_REC["end"] else ["C.lake_end"]
        print(f"  {'OK' if not diff else '🔴 NG'} 16本目 正本 map16.json の sections と illu.py の断面の定数: "
              f"{'同じ' if not diff else '違う ' + str(diff)}")
        ok &= not diff
    else:
        print("  🔴 NG 16本目 正本 ref/ep16/map16.json が無い＝断面を照合できない")
        ok = False
    return ok


def _selftest_ep16_vd(ss):
    """16本目 ⑤b-4：VD（正面から見た斜面）の検算＝本番の表で回す。陽性対照は**型の定数を壊す形**（§5b-88）。"""
    kw = dict(docs=dict(ss.REC_DOCS), pages=_pages(), split=tuple(ss.ILLU_SPLIT_TIMES), until=ss.ILLU_CROWD_UNTIL,
              sec_ok=dict(ss.ILLU_SEC_OK), clock_ok=tuple(ss.ILLU_CLOCK_OK), counts=dict(ss.ILLU_COUNTS),
              roles=dict(ss.ILLU_ROLES))
    R = IL.VD_REC
    g306 = dict(place="VD", start=dict(crack="on"), rec=R["water"]["650"],
                steps=[dict(state=dict(trace="on"), rec=R["crack"],
                            tag=[dict(t="1,200m", at="p1200"), dict(t="930m", at="p930")]), dict()])
    g312 = dict(place="VD", start=dict(crack="on"), rec=R["water"]["650"],
                steps=[dict(state=dict(c1960="fall"), rec=R["c1960"]), dict(state=dict(area="on"), rec=R["area"]), dict()])
    g408 = dict(place="VD", start=dict(crack="on", water="600", c1960="fell", switch="on"), rec=R["water"]["600"] + "・" + R["c1960"],
                steps=[dict(state=dict(area="on"), rec=R["area"]), dict(state=dict(pip="on"), rec=R["pip"])])
    g507 = dict(place="VD", start=dict(crack="on", water="700", switch="on"), assume="模型の想定", rec=R["water_model"],
                steps=[dict(state=dict(model="area"), rec=R["model"]),
                       dict(state=dict(dim="on", bracket="on"), rec=R["dim"],
                            tag=[dict(t="幅1.8km", at="dim"), dict(t="1,200m", at="b1200"), dict(t="600m", at="b600")]), dict()])
    g508 = dict(place="VD", start=dict(crack="on", water="700", model="area"), assume="模型の想定", rec=R["water_model"],
                steps=[dict(state=dict(model="split"), rec=R["model"]), dict(state=dict(model="fall"), rec=R["model"])])
    g513 = dict(place="VD", start=dict(crack="on", water="722.5", model="split"), assume="模型の想定", rec=R["water"]["722.5"],
                steps=[dict(), dict(state=dict(wave="on"), rec=R["wave"], tag=dict(t="模型の波の高さ", at="wave")),
                       dict(tag=dict(t="いちばん高い水位", at="water"))])
    g809 = dict(place="VD", start=dict(tod="night", water="700", crack="on", whole="on"), rec=R["water"]["700"],
                steps=[dict(state=dict(whole="fall"), rec=R["whole"]), dict(), dict()])
    cases = [("16本目 正しい VD c306（亀裂をなぞる・1,200m・930m）", g306, True),
             ("16本目 正しい VD c312（1960年の崩落の2か所が湖へ・範囲に色）", g312, True),
             ("16本目 正しい VD c408（1961年2月・水位600m・小さな断面と線）", g408, True),
             ("16本目 正しい VD c507（模型の範囲・幅1.8km・1,200m・600m）", g507, True),
             ("16本目 正しい VD c508（沢の東と西の2つの塊が2回に）", g508, True),
             ("16本目 正しい VD c513（最高水位・波の高さの印＝数なし）", g513, True),
             ("16本目 正しい VD c809（夜・実際の塊がまるごと下がる）", g809, True),
             ("🔴 16本目 陽性対照⑨：「1,200m」を 930m の谷に付ける（カンマの数を 1200 と読む）",
              dict(g306, steps=[dict(state=dict(trace="on"), rec=R["crack"], tag=dict(t="1,200m", at="p930")), dict()]), False),
             ("🔴 16本目 陽性対照⑨：記録に無い幅「幅2.5km」",
              dict(g507, steps=[dict(state=dict(model="area"), rec=R["model"]),
                                dict(state=dict(dim="on"), rec=R["dim"], tag=dict(t="幅2.5km", at="dim")), dict()]), False),
             ("🔴 16本目 陽性対照④：模型の想定を「想定」の札なしで描く", dict(g508, assume=""), False)]
    ok = _run(cases, kw)
    breaks = [
        ("⑩ 亀裂の西の山を 1,240m で描く型（VD_CRACK）", "VD_CRACK",
         tuple((x, 1240.0 if z == 1200.0 else z) for x, z in IL.VD_CRACK), g306, ("⑩",)),
        ("⑩ 1960年の崩落の上の端を 900m で描く型（VD_1960）", "VD_1960",
         dict(IL.VD_1960, niche=dict(IL.VD_1960["niche"], top=900.0)), g312, ("⑩",)),
        ("⑩ 1960年の崩落をダムの約1km上流に置く型（VD_1960 の x）", "VD_1960",
         dict(IL.VD_1960, niche=dict(IL.VD_1960["niche"], x=(700.0, 730.0))), g312, ("⑩",)),
        ("⑩ 実際の塊の下がったあとの上の端を 900m にする型（VD_PEAK）", "VD_PEAK", 900.0, g809, ("⑩",)),
        ("⑩ 模型の範囲を 1,260m まで描く型（VD_MODEL_Z）", "VD_MODEL_Z", (600.0, 1260.0), g508, ("⑩",)),
        ("⑩ 模型の2つの塊の境を沢からずらす型（VD_MASS_X）", "VD_MASS_X", 760.0, g508, ("⑩",)),
        ("⑩ 波の高さの印を 40m で描く型（VD_WAVE_H）", "VD_WAVE_H", 40.0, g513, ("⑩",)),
        ("⑩ 1960年の水位を 680m で描く型（VD_WATER）", "VD_WATER", dict(IL.VD_WATER, **{"650": 680.0}), g312, ("⑩",)),
        ("⑨ 模型の幅を 2.0km に広げる型（VD_FLANK_W の西の端）", "VD_FLANK_W",
         tuple((500.0 if x == 553.0 else x, z) for x, z in IL.VD_FLANK_W), g507, ("⑨",)),
        ("⑬ 塊を夜の地に近い色で描く型（VD_FIX の block）", "VD_FIX", dict(IL.VD_FIX, block="#2f3a4c"), g809, ("⑬",)),
    ]
    for name, attr, val, spec, heads in breaks:
        keep = getattr(IL, attr)
        setattr(IL, attr, val)
        try:
            bad = judge_scene(IL.scene(**spec), "selftest", **kw)[0]
        except Exception as e:                           # noqa: BLE001
            bad = [f"組めない：{e}"]
        finally:
            setattr(IL, attr, keep)
        good = all(any(b.startswith(h) for b in bad) for h in heads)
        print(f"  {'OK' if good else '🔴 NG'} 16本目 陽性対照（型）{name}: {'不合格' if bad else '合格'}（{'・'.join(heads)}で不合格のはず）"
              + (f"  ← {bad[0]}" if bad else ""))
        ok &= good
    # 🔴 型の見張り（門番より前で止まる）：波の印を実際の場面に・模型と実際を同じ場面に・塊を戻す
    for name, spec in (("波の高さの印を実際の場面に描く", dict(g809, steps=[dict(state=dict(wave="on"), rec=R["wave"]), dict(), dict()])),
                       ("模型と実際を同じ場面に描く", dict(g508, start=dict(g508["start"], whole="on"))),
                       ("下がった模型の塊を戻す", dict(g508, steps=[dict(state=dict(model="fell"), rec=R["model"]),
                                                            dict(state=dict(model="split"), rec=R["model"])]))):
        try:
            IL.scene(**spec)
            got = False
        except ValueError:
            got = True
        print(f"  {'OK' if got else '🔴 NG'} 16本目 型の見張り：{name}: {'組めない（止まった）' if got else '🔴 組めた'}")
        ok &= got
    # ④ 小さく戻す絵（c807）：パネルの文に「想定」が無いと止まる
    pair = dict(blocks=[dict(k="模型", t="2つの塊が2回に", stage=0, stages=2, scene=dict(g508, assume="", steps=[dict(), dict()])),
                        dict(k="実際", t="1つの塊のまま", stage=1, stages=2, scene=dict(g809, steps=[dict(), dict()]))])
    b, _ = judge_cut("c807", dict(fig=("illu_pair", pair)), {"c807": "混ざり"})
    ok &= _expect("🔴 16本目 陽性対照④：小さく戻す模型の絵のパネルに「想定」が無い", b, "④")
    return ok


# 🔴 16本目 ⑤b-2：置き場 VA の記録の値を**門番の側に**持つ（型の定数を読まない＝ルール §5b-88。型の点を壊すと捕まる）
# 🔴 2026-10-04（18本目 ⑤b-1・§0b）：16本目の値（REC_VA・方眼 VA_GRID_PX）は `tools/fixture_ep16.py` の GATES["check_illu"] へ移した
#    （値は1つも変えていない＝git の `b044b56`）。本番は空（`va_records()` は見本を差し込んだ selftest の中だけで呼ぶ）。
#    VA_GRID_PX は #100（1934年の地形図）の 1 km 方眼の画素の実測＝その地図の値（未設定は None）
REC_VA = {}
VA_GRID_PX = None


def va_records(il=None):
    """型 VA の点と形（#100 の画素）から、記録の距離・面積・塊の動きを測って REC_VA と照らす。返り値＝食い違いの一覧。"""
    il = il or IL
    m = 1000.0 / VA_GRID_PX
    bad = []
    if abs(il.VA_MPX - m) > 0.005:
        bad.append(f"記録：型の縮尺 {il.VA_MPX}m/画素が方眼（1 km＝{VA_GRID_PX}画素＝{m:.3f}m）と違う")
    P = il.VA_PTS

    def km(a, b):
        return math.hypot(P[a][0] - P[b][0], P[a][1] - P[b][1]) * m / 1000.0
    for name, val in (("tunnel_km", km("dam", "tunnel_in")), ("marks_km", km("north_dam", "north_1100")),
                      ("slide_km", km("slide_w", "slide_e"))):
        want, tol, rec = REC_VA[name]
        if abs(val - want) > tol:
            bad.append(f"記録：{name} {val:.2f}km（記録 {want}±{tol}＝{rec}）")
    pts = il.va_slide_pts()
    km2 = abs(sum(a[0] * b[1] - b[0] * a[1] for a, b in zip(pts, pts[1:] + pts[:1]))) / 2 * m * m / 1e6
    want, tol, rec = REC_VA["slide_km2"]
    if abs(km2 - want) > tol:
        bad.append(f"記録：崩れた範囲の面積 {km2:.2f}km²（記録 {want}±{tol}＝{rec}）")
    lo, hi, rec = REC_VA["shift_m"]
    if not lo <= il.VA_SHIFT * m <= hi:
        bad.append(f"記録：塊の北への動き {il.VA_SHIFT * m:.0f}m（記録 {lo:.0f}〜{hi:.0f}m＝{rec}）")
    return bad


def _selftest_ep16_va(ss):
    """16本目の置き場 VA（上から見た谷）の検算＝本番の表（cuts.ss の16本目の値）で回す。"""
    kw = dict(docs=dict(ss.REC_DOCS), pages=_pages(), split=tuple(ss.ILLU_SPLIT_TIMES), until=ss.ILLU_CROWD_UNTIL,
              sec_ok=dict(ss.ILLU_SEC_OK), clock_ok=tuple(ss.ILLU_CLOCK_OK), counts=dict(ss.ILLU_COUNTS),
              roles=dict(ss.ILLU_ROLES))
    R = IL.VA_REC
    good_c102 = dict(place="VA", at="22:39", start=dict(view="wide", block="on", prev="B", switch="on", cam=1.05),
                     rec="S1 p98（22時39分）・S1 p147（1つの塊）",
                     steps=[dict(state=dict(wave_w="on", flood="on", towns="gone"), rec=R["wave_w"],
                                 tag=[dict(t="ダム", at="dam"), dict(t="ロンガローネ", at="longarone")]),
                            dict(state=dict(wave_w="recede", flood="recede", towns="mud", cam=1.0), rec=R["dawn"])])
    good_c116 = dict(place="VA", start=dict(view="wide", tod="day", prev="C", switch="on"), rec="#100 p1",
                     steps=[dict(tag=[dict(t="湖", at="lake"), dict(t="エルト", at="erto")]), dict(tag=dict(t="ダム", at="dam"))])
    good_c315 = dict(place="VA", start=dict(view="near", tod="day", prev="D", switch="on"), rec="#100 p1",
                     steps=[dict(state=dict(tunnel="on"), rec=R["tunnel"]),
                            dict(tag=[dict(t="入り口", at="tunnel_in"), dict(t="出口", at="tunnel_out")])])
    good_c316 = dict(place="VA", start=dict(view="near", tod="day", tunnel="on"), rec=R["tunnel"], assume="会社の説明（想定）",
                     steps=[dict(state=dict(split="on"), rec=R["split"]), dict(state=dict(split="flow"), rec=R["split"])])
    good_c716 = dict(place="VA", start=dict(view="wide", road="low"), rec=R["road"],
                     steps=[dict(state=dict(gates="on"), rec=R["gates"], tag=dict(t="上の入り口", at="road_up")),
                            dict(state=dict(nxt="C"), delay=2.0)])
    good_c802 = dict(place="VA", start=dict(view="wide"),
                     steps=[dict(state=dict(slide="on"), rec=R["slide"]), dict(state=dict(nxt="B"), delay=1.0)])
    good_c812 = dict(place="VA", start=dict(view="near", block="on", prev="B"), rec=R["block"],
                     steps=[dict(state=dict(marks="on"), rec=R["marks"]),
                            dict(tag=[dict(t="930m", at="mark1"), dict(t="930m", at="mark2")])])
    good_c814 = dict(place="VA", start=dict(view="wide", block="on"), rec=R["block"],
                     steps=[dict(state=dict(wave_e="on"), rec=R["wave_e"]), dict(state=dict(shore="mud"), rec=R["shore"])])
    good_c823 = dict(place="VA", start=dict(view="west", block="on", prev="C"), rec=R["block"],
                     steps=[dict(state=dict(wave_w="on", flood="on", towns="gone"), rec=R["flood"]),
                            dict(state=dict(tod="dawn", wave_w="recede", flood="recede", towns="mud"), rec=R["dawn"])])
    cases = [
        ("16本目 正しい VA c102（夜・ダムを越えた水が谷へ・町の面が消える・泥の色）", good_c102, True),
        ("16本目 正しい VA c116（昼・場所の札）", good_c116, True),
        ("16本目 正しい VA c315（昼・トンネル・D の目の印）", good_c315, True),
        ("16本目 正しい VA c316（会社の説明の想定＝想定の札つき）", good_c316, True),
        ("16本目 正しい VA c716（道の入口2か所・次の断面の線）", good_c716, True),
        ("16本目 正しい VA c802（崩れた範囲・次の断面の線）", good_c802, True),
        ("16本目 正しい VA c812（北の岸の印2・930m）", good_c812, True),
        ("16本目 正しい VA c814（東へ向かった波・岸の集落が消える）", good_c814, True),
        ("16本目 正しい VA c823（峡谷の出口の先・夜明けの色）", good_c823, True),
        ("🔴 16本目 陽性対照①：水を出した段に rec が無い",
         dict(good_c812, steps=[dict(state=dict(wave_w="on"))]), False),
        ("🔴 16本目 陽性対照①：rec の頁が資料の範囲の外（S1 p300）",
         dict(good_c802, steps=[dict(state=dict(slide="on"), rec="S1 p300")]), False),
        ("🔴 16本目 陽性対照①：#100 の頁が範囲の外（#100 p2）", dict(good_c116, rec="#100 p2"), False),
        ("🔴 16本目 陽性対照①：頭を昼にしたのに場面の rec が無い", dict(good_c116, rec=None), False),
        ("🔴 16本目 陽性対照⑤：札に 22:39 以外の時計（22:40）",
         dict(good_c812, steps=[dict(state=dict(marks="on"), rec=R["marks"], tag=dict(t="22:40", at="mark1"))]), False),
        ("🔴 16本目 陽性対照⑤：札に秒（45秒足らず）",
         dict(good_c812, steps=[dict(state=dict(marks="on"), rec=R["marks"], tag=dict(t="45秒足らず", at="mark1"))]), False),
        ("🔴 16本目 陽性対照⑧：near に寄りすぎ（cam 1.4＝1.36m/画素）",
         dict(good_c812, start=dict(view="near", block="on", prev="B", cam=1.4)), False),
        ("🔴 16本目 陽性対照④：会社の説明の想定なのに想定の札が無い", dict(good_c316, assume=None), False),
    ]
    ok = _run(cases, kw)
    # 🔴 陽性対照（組めない形＝型が止める）：前の図の線を段で出す・夜明けから始める・昼から夜明けへ
    for name, spec in (("prev（前の図の線）を段で変える", dict(good_c812, steps=[dict(state=dict(prev="C"))])),
                       ("頭を夜明けにする", dict(good_c823, start=dict(view="west", tod="dawn"))),
                       ("昼から夜明けへ", dict(good_c116, steps=[dict(state=dict(tod="dawn"), rec=R["dawn"])]))):
        try:
            IL.scene(**spec)
            print(f"  🔴 NG 16本目 陽性対照（型）：{name}: 組めた（止まるはず）")
            ok = False
        except ValueError as e:
            print(f"  OK 16本目 陽性対照（型）：{name}: 止まった  ← {e}")
    # 🔴 陽性対照③'（数）：北の岸の印を3つ・道の入口を1つ・ダムを2つ（部品の obj を壊す）
    for name, spec, key, val in (("北の岸の印を3つ", good_c812, "north_marks", 3), ("道の入口を1つ", good_c716, "road_gates", 1),
                                 ("ダムを2つ", good_c802, "dam", 2)):
        sc = IL.scene(**spec)
        p = next(q for q in sc["parts"] if key in (q.get("obj") or {}))
        p["obj"] = dict(p["obj"], **{key: val})
        ok &= _expect(f"🔴 16本目 陽性対照③：{name}", judge_scene(sc, "selftest", **kw)[0], "③")
    # 🔴 陽性対照①（合図の部品に数を持たせる）
    sc = IL.scene(**good_c102)
    next(q for q in sc["parts"] if q.get("signal"))["obj"] = dict(dam=1)
    ok &= _expect("🔴 16本目 陽性対照①：合図の部品が数（obj）を持つ", judge_scene(sc, "selftest", **kw)[0], "①")
    # 🔴 陽性対照⑧（描く側の定数を壊す）：near の縮尺を 1.2m/画素に
    keep = IL.VA_VIEW["near"]["mpp"]
    IL.VA_VIEW["near"]["mpp"] = 1.2
    try:
        bad = judge_scene(IL.scene(**good_c812), "selftest", **kw)[0]
    finally:
        IL.VA_VIEW["near"]["mpp"] = keep
    ok &= _expect("🔴 16本目 陽性対照⑧（描く側）：near の縮尺 1.2", bad, "⑧")
    # 🔴 陽性対照④（カットの表）：想定の札を表に無いカットに出す・表のカットで落とす
    #   （2つ目は想定の帯を描かない絵＝場面の規則〈帯があるのに札が無い〉では鳴らない形で、表の規則だけを測る）
    for name, cid, spec, head in (("表に無いカットに想定の札", "x16", good_c316, "④x16：想定の札"),
                                  ("表のカット（c316）で想定の札を落とす", "c316", good_c315, "④c316：想定のカットなのに")):
        bad = [b for b in judge_cut(cid, dict(fig=("illu", spec)), {cid: "再現イラスト"})[0] if b.startswith("④")]
        ok &= _expect(f"🔴 16本目 陽性対照④：{name}", bad, head)
    # 🔴 記録の距離・面積・塊の動き（門番の側の記録 REC_VA）と、型の定数を壊したら鳴るか
    bad = va_records()
    print(f"  {'OK' if not bad else '🔴 NG'} 16本目 VA の点と形が記録の距離・面積・塊の動きのとおり: "
          f"{'合格' if not bad else bad}")
    ok &= not bad
    keep = dict(IL.VA_PTS)
    IL.VA_PTS["tunnel_in"] = (900.0, 507.0)
    try:
        bad = va_records()
    finally:
        IL.VA_PTS.clear()
        IL.VA_PTS.update(keep)
    ok &= _expect("🔴 16本目 陽性対照（記録）：トンネルの入口を約2.0kmに", bad, "記録")
    keep = IL.VA_SHIFT
    IL.VA_SHIFT = 90.0
    try:
        bad = va_records()
    finally:
        IL.VA_SHIFT = keep
    ok &= _expect("🔴 16本目 陽性対照（記録）：塊を北へ約480m動かす", bad, "記録")
    # 🔴 正本（`ref/ep16/map16.json`＝#100 を目で読んだ点）と illu.py の定数が同じか（写し間違い・手で動かした値を止める）
    js = HERE / "ref" / "ep16" / "map16.json"
    if js.exists():
        import json
        g = json.loads(js.read_text(encoding="utf-8"))
        diff = [k for k, v in IL.VA_PTS.items() if (float(g["points"][k]["x"]), float(g["points"][k]["y"])) != v]
        diff += [k for k, v in IL.VA_LINES.items() if [tuple(q) for q in g["lines"][k]] != [tuple(q) for q in v]]
        diff += ["lake_stations"] if [tuple(r) for r in g["lake_stations"]["rows"]] != [tuple(r) for r in IL.VA_LAKE] else []
        diff += [k for k, v in IL.VA_POLY.items() if [tuple(q) for q in g["polys"][k]] != [tuple(q) for q in v]]
        diff += ["m_per_px"] if abs(g["m_per_px"] - IL.VA_MPX) > 1e-9 else []
        print(f"  {'OK' if not diff else '🔴 NG'} 16本目 正本 map16.json と illu.py の定数: {'同じ' if not diff else '違う ' + str(diff)}")
        ok &= not diff
    else:
        print("  🔴 NG 16本目 正本 ref/ep16/map16.json が無い＝照合できない（git の中にある＝無ければ止める）")
        ok = False
    return ok


def selftest_ep18():
    """🆕 18本目 ⑤b-2（2026-10-04）：置き場 SA（横から見た海）の ⑤⑦⑫⑮⑯⑰ と ④（段の途中の想定の札）の検算＝**見本 `fixture_ep18`
    （18本目の表）を差し込んで**回す（SB〜SD の `selftest_ep18_sbcd` も、この差し込みの中で呼ぶ）。
    ✅ 2026-10-06（19本目 ⑤b-1・§0b）：本番の表（cuts.ss の REC_DOCS・ILLU_*／この門番の REC_DEPTH〜REC_SD_ON・SB_DIST_TAGS・SC_NUMS）は
       19本目の空の器にした＝18本目の値は `fixture_ep18`（15・16本目と同じ作り）。差し込んだら原文の頁の読み込み `_pages()`（lru_cache）を捨てて
       18本目の原文を読み直し、戻したらまた捨てる＝落ちても終わっても `restore()` で本番の値へ戻す（try/finally）。本体は `_selftest_ep18`。
    ⚠️ 見本が持つのは**表の値**だけ。正しい側の絵（c101・c103・c106・c314・c318・c411・c502 ほか）は**18本目の章ファイルの SPEC そのもの**を
       `cuts.SPEC` から読む＝18本目の章ファイル（git の `b11797a` の `tools/cuts/c*.py`）が live のときだけ通る（本線は19本目の空の器なので
       `KeyError: 'c101'` で落ちる＝19本目 ⑤b-1（1）で章ファイルを空にした時点から。見本の値のせいではない）"""
    import fixture_ep18
    fixture_ep18.apply(sys.modules[__name__])
    fixture_ep18.apply_cuts()     # ✅ 2026-10-06 チャット6：18本目の章ファイル（git の b11797a）の PLAN・SPEC をこの処理の中だけ入れる
    _pages.cache_clear()          # 🔴 原文の頁の読み込みは覚えている（lru_cache）＝本番の（空の）原文を捨てて18本目を読み直す
    try:
        return _selftest_ep18()
    finally:
        fixture_ep18.restore()
        _pages.cache_clear()


def _selftest_ep18():
    """18本目の検算の本体（`fixture_ep18` を差し込んだ中で呼ぶ）。陽性対照は**型の定数を壊す**形も入れる（SA_RESCUE_M・SA_ROPE_M・SA_BREAK1・SA_T＝§5b-88）"""
    import copy
    import cuts
    ss = _ss()
    ok = True
    S = {c: copy.deepcopy(cuts.SPEC[c]["fig"][1]) for c in ("c101", "c103", "c106", "c314", "c318", "c405", "c411", "c502")}
    kinds = {c: cuts.PLAN[c]["kind"] for c in S}

    def scn(kw):
        return IL.scene(**kw)

    def run_scene(name, kw, head, mutate=None):
        nonlocal ok
        try:
            sc = scn(kw)
            if mutate:
                mutate(sc)
            bad = judge_scene(sc, "selftest")[0]
        except Exception as e:                           # noqa: BLE001
            bad = [f"組めない：{e}"]
        ok &= _expect(f"🔴 18本目 陽性対照{head}：{name}", bad, head)

    def run_cut(name, cid, kw, kind, head):
        nonlocal ok
        bad = [b for b in judge_cut(cid, dict(fig=("illu", kw)), {cid: kind})[0] if b.startswith(head)]
        ok &= _expect(f"🔴 18本目 陽性対照{head}：{name}", bad, head)
    # 正しい側（本番の SPEC）。🆕 ⑤b-7c：差し込み（頭の映像 intro foot・尻の写真 tail）も本番の SPEC のまま渡す
    for c, kw in S.items():
        sp = cuts.SPEC.get(c) or {}
        extra = {k: sp[k] for k in ("intro", "tail") if sp.get(k)}
        bad = judge_cut(c, dict(fig=("illu", kw), **extra), kinds)[0]
        print(f"  {'OK' if not bad else '🔴 NG'} 18本目 正しい SA {c}: {'合格' if not bad else bad[0]}")
        ok &= not bad
    # ⑤ 時計：分の小数まで（9時18分・9時18.2分は表に無い）・秒の札・表が空なら全部止める
    k103 = S["c103"]

    def with_tag(kw, i, t):
        kw = copy.deepcopy(kw)
        kw["steps"][i]["tag"] = dict(t=t, at="sk_rx")
        return kw
    run_scene("札に 9時18分（小数なし＝表に無い）", with_tag(k103, 1, "9時18分　船体の圧壊（査問会の見立て）"), "⑤")
    run_scene("札に 9時18.2分（表に無い小数）", with_tag(k103, 1, "9時18.2分"), "⑤")
    run_scene("札に秒（約0.1秒）", with_tag(S["c101"], 1, "約0.1秒"), "⑤")
    sc = scn(S["c101"])
    ok &= _expect("🔴 18本目 陽性対照⑤：時計の表が空（c101 の 9:13）",
                  judge_scene(sc, "selftest", clock_ok=())[0], "⑤")
    # ⑮ 潜水艦の時刻・止めるカット・推定の札・破片
    k405 = S["c405"]
    late = copy.deepcopy(k405)
    late["start"]["clk"] = "9:20"
    run_cut("9:20 の潜水艦（例外でないカット）", "x18", late, "再現イラスト", "⑮")
    run_cut("艦の絵を止めた c411 より後のカット（c420）に潜水艦", "c420", k405, "再現イラスト", "⑮")
    run_cut("例外でないカットで潜水艦が下がる・圧壊する", "x18", k103, "再現イラスト", "⑮")
    run_scene("c103 の圧壊に「推定」の札が無い", dict(k103, assume=None, assume_at=None), "⑮")
    run_scene("「推定」の札が下がり始めより遅い（1.5秒）", dict(k103, assume_at=(0, 1.5)), "⑮")
    noclk = copy.deepcopy(k405)
    noclk["start"]["clk"] = ""
    run_scene("潜水艦を描いた段に記録の時刻が無い", noclk, "⑮")
    up20 = copy.deepcopy(S["c411"])
    up20["start"]["tilt"] = 20.0
    run_scene("艦首の上げ 20度（記録 15°を越える）", up20, "⑮")

    def keep_debris(sc):
        p = next(q for q in sc["parts"] if q["id"] == "debris")
        p["keys"] = [dict(k, a=1.0) for k in p["keys"]]
    run_scene("破片が最後まで見えている", k103, "⑮", keep_debris)
    run_scene("破片が数（obj）を持つ", k103, "⑮",
              lambda sc: next(q for q in sc["parts"] if q["id"] == "debris").update(obj=dict(pieces=6)))
    keep_t = dict(IL.SA_T)
    IL.SA_T["debris"] = 4.0
    try:
        run_scene("破片が見える長さ 2秒あまり（型の定数 SA_T を壊す）", k103, "⑮")
    finally:
        IL.SA_T.clear()
        IL.SA_T.update(keep_t)
    # ⑯ 深さの数を幾何で漏らさない
    lin_sub = copy.deepcopy(S["c314"])
    lin_sub["start"].update(sub="on", clk="9:09")
    run_scene("目盛りの段（約260m）に潜水艦", lin_sub, "⑯")
    t_rope = copy.deepcopy(S["c106"])
    t_rope["steps"][0]["state"]["rope"] = "on"
    run_scene("試験深度の線と綱の目盛りが同じ段", t_rope, "⑯")
    run_scene("試験深度の線に切れ目1が無い", S["c106"], "⑯",
              lambda sc: sc["parts"].remove(next(q for q in sc["parts"] if q["id"] == "break1")))
    run_scene("切れ目の向こうの海底に切れ目2が無い", S["c106"], "⑯",
              lambda sc: sc["parts"].remove(next(q for q in sc["parts"] if q["id"] == "break2")))
    t_num = copy.deepcopy(S["c106"])
    t_num["steps"][0]["tag"][0]["t"] = "試験深度 約400m"
    run_scene("試験深度の札に数", t_num, "⑯")
    run_scene("潜水艦の段に深さの数（約1,000m）", with_tag(k405, 0, "約1,000m"), "⑯")
    for name, attr, val in (("救難室の限界を 300m で描く型", "SA_RESCUE_M", 300.0), ("綱を 2,400m で描く型", "SA_ROPE_M", 2400.0),
                            ("切れ目1を試験深度の線の下に置く型", "SA_BREAK1", (600.0, 618.0))):
        keep = getattr(IL, attr)
        setattr(IL, attr, val)
        try:
            run_scene(name, S["c318"] if attr == "SA_ROPE_M" else S["c106"] if attr == "SA_BREAK1" else S["c314"], "⑯")
        finally:
            setattr(IL, attr, keep)
    # ⑰ 9時18.1分の大きく低い音の輪
    run_cut("音の輪を c405 に（表のカットの外）", "c405", k103, "再現イラスト", "⑰")
    run_scene("音の輪の中心が圧壊した船体でない", k103, "⑰",
              lambda sc: next(q for q in sc["parts"] if q["id"] == "boom").update(pivot=[900.0, 400.0]))
    nowords = copy.deepcopy(k103)
    nowords["steps"][1]["tag"] = [dict(t="9時18.1分　船体の圧壊（査問会の見立て）", at="crush")]
    run_scene("音の輪の段の札に「内破でありうる」「大きく低い音」が無い", nowords, "⑰")
    c918 = copy.deepcopy(k103)
    c918["steps"][1]["state"]["clk"] = "9:18"
    run_scene("音の輪の段の時刻が 9:18（記録は 9:18.1）", c918, "⑰")
    run_scene("光の部品（flash）を足す", S["c101"], "⑰",
              lambda sc: sc["parts"].append(dict(IL._part("flash", "<rect/>", "R08 p4185"))))
    # ⑫ 壊れる物は表のカットだけ
    run_cut("圧壊を c405 に", "c405", k103, "再現イラスト", "⑫")
    # ②③ 人は置かない・数は記録の数
    run_scene("人の型紙（crew）を置く", S["c101"], "②",
              lambda sc: sc["parts"].append(dict(IL._part("crew", "<rect/>", "R08 p4185"), kind="sprite", role="crew",
                                                 inst=[dict(path=[[1300, 280]], stage=0, delay=0.0)])))
    run_scene("スカイラークを2隻", S["c101"], "③",
              lambda sc: next(q for q in sc["parts"] if q["id"] == "skylark").update(obj=dict(skylark=2)))
    # ④ 段の途中の想定の札（部品の札の言葉が抜けた型）
    keep = IL.assume_chip_svg
    IL.assume_chip_svg = lambda view, assume: "<rect/>"
    try:
        bad = [b for b in judge_cut("c103", dict(fig=("illu", k103)), kinds)[0] if b.startswith("④")]
    finally:
        IL.assume_chip_svg = keep
    ok &= _expect("🔴 18本目 陽性対照④：段の途中の想定の札に言葉が無い型", bad, "④")
    # ⑦ 混ざりのつなぎ待ち：束ができたら止まる・表に無い混ざりの全面の絵は止まる
    keep = ss.ILLU_MIX_BUNDLE
    ss.ILLU_MIX_BUNDLE = HERE / "ref" / "ep18" / "make_plan.py"         # 在るファイル＝束ができた見立て
    try:
        run_cut("束ができたのに c102 をつないでいない", "c102", copy.deepcopy(cuts.SPEC["c102"]["fig"][1]), "混ざり", "⑦")
    finally:
        ss.ILLU_MIX_BUNDLE = keep
    run_cut("つなぎ待ちの表に無い混ざりの全面の絵", "x19", k405, "混ざり", "⑦")
    # 🆕 ⑤b-7c：本物の側をつないだ（尻の写真）のに表に残る／つないだ絵の種類が「再現イラスト」のまま
    keep_t = ss.ILLU_MIX_TODO
    ss.ILLU_MIX_TODO = {"x20": "（検算用）"}
    try:
        bad = [b for b in judge_cut("x20", dict(fig=("illu", k405), tail=dict(photo="ep18/sail_t16.jpg", t="x", at=2)),
                                    {"x20": "混ざり"})[0] if b.startswith("⑦")]
    finally:
        ss.ILLU_MIX_TODO = keep_t
    ok &= _expect("🔴 18本目 陽性対照⑦：つないだのにつなぎ待ちの表に残る", bad, "⑦")
    bad = [b for b in judge_cut("x21", dict(fig=("illu", k405), intro=dict(foot=True, until=1)),
                                {"x21": "再現イラスト"})[0] if b.startswith("⑦")]
    ok &= _expect("🔴 18本目 陽性対照⑦：頭に本物の映像を差し込んだのに種類が「再現イラスト」", bad, "⑦")
    # 型が止める形
    for name, kw in (("圧壊のあとに潜水艦を戻す", dict(k103, steps=k103["steps"][:2] + [dict(state=dict(sub="on"), rec="R08 p4185")])),
                     ("圧壊の無い場面に音の輪", dict(k405, steps=[dict(boom=1, rec="R08 p4185"), dict()])),
                     ("艦首の上げ 40度", dict(k405, start=dict(k405["start"], tilt=40.0))),
                     ("想定の札なしで assume_at", dict(k103, assume=None)),
                     ("assume_at の場面でカメラを寄せる", dict(k103, start=dict(k103["start"], cam=1.05)))):
        try:
            IL.scene(**kw)
            print(f"  🔴 NG 18本目 陽性対照（型）：{name}: 組めた（止まるはず）")
            ok = False
        except ValueError as e:
            print(f"  OK 18本目 陽性対照（型）：{name}: 止まった  ← {e}")
    print(f"  18本目 SA の検算: {'通った' if ok else '🔴 落ちた'}")
    ok = selftest_ep18_sbcd() and ok
    return ok


def selftest_ep18_sbcd():
    """🆕 18本目 ⑤b-3（2026-10-04）：SB ⑱・SC ⑲・SD ⑳・合図 ㉑ の検算＝見本 fixture_ep18 の表（`selftest_ep18` の差し込みの中で呼ぶ）と
    18本目の章ファイルの SPEC（c308・c503・c513・c519・ca19・ca21・ca22）。
    🔴 陽性対照は型の定数を壊す形も入れる（SB_TS・SB_OIL・SB_PTS・SC_CIRCLE_M・sc_marker_pts・sd_tri_on_y＝§5b-88）"""
    import copy
    import cuts
    ok = True
    C7 = ("c308", "c503", "c513", "c519", "ca19", "ca21", "ca22", "ca02")    # 🆕 ⑤b-8：ca02（SB の捜索の海域）
    S = {c: copy.deepcopy(cuts.SPEC[c]["fig"][1]) for c in C7}
    kinds = {c: cuts.PLAN[c]["kind"] for c in S}
    for c, kw in S.items():
        bad = judge_cut(c, dict(fig=("illu", kw)), kinds)[0]
        print(f"  {'OK' if not bad else '🔴 NG'} 18本目 正しい {kw['place']} {c}: {'合格' if not bad else bad[0]}")
        ok &= not bad

    def run(name, kw, head, mutate=None):
        nonlocal ok
        try:
            sc = IL.scene(**kw)
            if mutate:
                mutate(sc)
            bad = judge_scene(sc, "selftest")[0]
        except Exception as e:                           # noqa: BLE001
            bad = [f"組めない：{e}"]
        ok &= _expect(f"🔴 18本目 陽性対照{head}：{name}", bad, head)

    def broken(name, obj, key, val, kw, head):
        """型の定数（dict の欄か、モジュールの名）を壊して組む＝門番が型の定数を読んでいないこと（§5b-88）。"""
        if isinstance(obj, dict):
            keep = obj[key]
            obj[key] = val
            try:
                run(name, kw, head)
            finally:
                obj[key] = keep
        else:
            keep = getattr(IL, key)
            setattr(IL, key, val)
            try:
                run(name, kw, head)
            finally:
                setattr(IL, key, keep)

    def tag(kw, i, t, at=None):
        kw = copy.deepcopy(kw)
        kw["steps"][i]["tag"] = dict(t=t, at=at) if at else dict(t=t, xy=(960, 300))
        return kw
    # ⑱ SB
    broken("スレッシャーを 3,600ヤードに置く型（SB_TS）", IL.SB_TS, "m", 3600 * 0.9144, S["c308"], "⑱")
    broken("スレッシャーを 157度に置く型（SB_TS）", IL.SB_TS, "brg", 157.0, S["c308"], "⑱")
    broken("油の帯を北東に置く型（SB_OIL）", IL.SB_OIL, "brg", 45.0, S["c513"], "⑱")
    broken("油の帯を 15km に置く型（SB_OIL）", IL.SB_OIL, "m", 15000.0, S["c513"], "⑱")
    broken("基準の点を 65度05分西に置く型（SB_PTS）", IL.SB_PTS, "datum", ((-65.0833, 41.75), "R08 p4065"), S["c503"], "⑱")
    run("札に「約3.4km」", tag(S["c308"], 1, "約3.4km", "mid_ts"), "⑱")
    run("「十数キロ」の札が線を指していない", tag(S["c513"], 2, "南東へ 十数キロ", "datum"), "⑱")
    run("札に距離の数「約12km」", tag(S["c513"], 2, "約12km", "mid_se"), "⑱")
    # 🆕 ⑤b-8（ca02）：捜索の海域の四角＝一辺を 15km（法定マイルの10マイルより短い）・基準の点からずらした型／広さの数の札
    broken("捜索の海域の四角を一辺 15km で描く型（SB_SQ）", IL.SB_SQ, "m", 15000.0, S["ca02"], "⑱")
    broken("捜索の海域の四角を一辺 20km で描く型（SB_SQ）", IL.SB_SQ, "m", 20000.0, S["ca02"], "⑱")
    broken("基準の点を 65度05分西に置く型（SB_PTS）＝四角も動く", IL.SB_PTS, "datum", ((-65.0833, 41.75), "R08 p4065"), S["ca02"], "⑱")
    run("札に広さの数「約17km」", tag(S["ca02"], 0, "一辺 約17km", "sq_n"), "⑱")
    run("測る線が四角の外へ出る", S["ca02"], "⑱",
        lambda sc: [p.update(path=[[q[0] + 600.0, q[1]] for q in p["path"]]) for p in sc["parts"] if p.get("id") == "trk"])
    zoom = copy.deepcopy(S["c503"])
    zoom["start"]["cam"] = 16.0
    run("上から見た海に寄りすぎ（cam 16＝1.44m／画素）", zoom, "⑧")
    run("札に 7:46（表に無い時刻）", tag(S["c308"], 0, "7:46", "meet_w"), "⑤")
    run("捜索の艦（数の記録が無い）を足す", S["c519"], "③",
        lambda sc: sc["parts"].append(dict(IL._part("search", "<rect/>", "R08 p4188"), obj=dict(search_ship=3))))
    # ⑲ SC
    broken("円を直径 400m で描く型（SC_CIRCLE_M）", IL, "SC_CIRCLE_M", 400.0, S["ca21"], "⑲")
    run("札に「直径 約400m」", dict(S["ca21"], steps=S["ca21"]["steps"][:2] + [
        dict(S["ca21"]["steps"][2], tag=[dict(t="直径 約400m", at="dia_mid"), dict(t="この円より広くない", at="edge_r")])]), "⑲")
    run("「より広くない」の札が無い", dict(S["ca21"], steps=S["ca21"]["steps"][:2] + [
        dict(S["ca21"]["steps"][2], tag=dict(t="直径 約370m", at="dia_mid"))]), "⑲")
    broken("目印を枠の中だけに並べる型（sc_marker_pts）", IL, "sc_marker_pts",
           (lambda f=IL.sc_marker_pts: [p for p in f() if 40 < p[0] < 1880 and 40 < p[1] < 1040]), S["ca19"], "⑲")
    run("目印が数を持つ", S["ca19"], "⑲", lambda sc: next(q for q in sc["parts"] if q["id"] == "markers").update(obj=dict(marker=900)))
    run("札に広さの数（1,200）", tag(S["ca19"], 2, "1,200平方ヤード"), "⑲")
    run("大きな塊を6つ描く", S["ca21"], "③",
        lambda sc: sc["parts"].append(dict(IL._part("pieces", "<rect/>", "R17書 p9802"), obj=dict(large_piece=6))))
    # ⑳ SD
    run("トリエステ2世が船体の上に着いていない（40画素浮く）", S["ca22"], "⑳",
        lambda sc: next(q for q in sc["parts"] if q["id"] == "trieste")["keys"][-1].update(
            dy=next(q for q in sc["parts"] if q["id"] == "trieste")["keys"][-1]["dy"] - 40.0))
    broken("着く高さを 40画素上にずらす型（sd_tri_on_y）", IL, "sd_tri_on_y",
           (lambda f=IL.sd_tri_on_y: f() - 40.0), S["ca22"], "⑳")
    run("深さの切れ目が無い", S["ca22"], "⑳", lambda sc: sc["parts"].remove(next(q for q in sc["parts"] if q["id"] == "break")))
    run("札に深さの数（海底 約2,600m）", tag(S["ca22"], 0, "海底 約2,600m", "floor"), "⑳")
    run("The Fish を足す（ca22 の語りに無い）", S["ca22"], "③",
        lambda sc: sc["parts"].append(dict(IL._part("fish", "<rect/>", "R17書 p9802"), obj=dict(fish=1))))
    run("人の型紙を置く", S["ca22"], "②",
        lambda sc: sc["parts"].append(dict(IL._part("crew", "<rect/>", "R17書 p9802"), kind="sprite", role="crew",
                                           inst=[dict(path=[[800, 250]], stage=0, delay=0.0)])))
    # ㉑ 見る向きの合図（本番の並び＋合図を外した SPEC）
    specs = [(c, cuts.SPEC[c]) for c in cuts.PLAN if c in cuts.SPEC]
    bad, m = judge_signals(specs)
    print(f"  {'OK' if not bad else '🔴 NG'} 18本目 正しい ㉑ 合図: {'合格（' + str(m) + 'か所）' if not bad else bad[0]}")
    ok &= not bad and m >= 3
    for cid, fld, val in (("c503", "prev", "off"), ("ca22", "mini", "off"), ("c310", "map", "off")):
        sp = copy.deepcopy(cuts.SPEC[cid])
        sp["fig"][1]["start"][fld] = val
        if cid == "c310":
            sp["fig"][1]["start"]["switch"] = "off"
        b = judge_signals([(c, sp if c == cid else s) for c, s in specs])[0]
        ok &= _expect(f"🔴 18本目 陽性対照㉑：{cid} の合図を外す（{fld}={val}）", b, "㉑")
    # 型が止める形
    for name, kw in (("広い図の頭で近い図の点", dict(S["c308"], start=dict(view="wide", thr="on"))),
                     ("近い図で zin", dict(S["c503"], steps=[dict(state=dict(zin="on"))] + S["c503"]["steps"][1:])),
                     ("円の無い直径の線", dict(S["ca21"], start=dict(dia="on"))),
                     ("着いたトリエステ2世を戻す", dict(S["ca22"], start=dict(mini="SC", tri="on"),
                                                     steps=[dict(state=dict(tri="down"), rec="R17書 p9802")])),
                     ("段で小さな地図を出す", dict(S["ca22"], start=dict(tri="down"),
                                                 steps=[dict(state=dict(mini="SC", tri="on"), rec="R17書 p9802")]))):
        try:
            IL.scene(**kw)
            print(f"  🔴 NG 18本目 陽性対照（型）：{name}: 組めた（止まるはず）")
            ok = False
        except ValueError as e:
            print(f"  OK 18本目 陽性対照（型）：{name}: 止まった  ← {e}")
    print(f"  18本目 SB・SC・SD・合図の検算: {'通った' if ok else '🔴 落ちた'}")
    return ok


def selftest_a1():
    """🆕 19本目 ⑤b-2：㉒ A1 の物差しの検算（本番の表＝19本目のまま）。正しい場面が通り、わざと壊した場面が落ちること"""
    print("■ selftest A1（19本目 ⑤b-2・㉒）")
    ok = True
    good = IL.scene("A1", [dict(state=dict(a1mid="drop"), rec="TR p1318",
                                tag=dict(t="約2.5m（ほぼ1階分）", at="roof_mid")),
                           dict(state=dict(a1mid="fall"), rec="TR p1363"),
                           dict(state=dict(a1sway=-40.0), rec="TR p1421", tag=dict(t="12階が西へ約53cm", at="east12")),
                           dict(state=dict(a1east="fall"), rec="TR p1424")], rec="TR p1330")
    b, _ = judge_a1(good, "selftest")
    print(f"  {'OK' if not b else '🔴 NG'} 正しい A1（下がる→真ん中→揺れ→東）: {'合格' if not b else '不合格'}（合格のはず）"
          + (f"  ← {b[0]}" if b else ""))
    ok &= not b
    # 陽性対照（描く側の型が拒むものは、組んだ部品を壊して門番だけで落ちるかを見る）
    import copy
    sc = copy.deepcopy(good)
    next(p for p in sc["parts"] if p["id"] == "west")["keys"].append(dict(stage=1, delay=0.0, dy=40.0))
    ok &= _expect("陽性対照㉒：西の部分を下げる", judge_a1(sc, "x")[0], "㉒")
    sc = copy.deepcopy(good)
    for k in next(p for p in sc["parts"] if p["id"] == "mid")["keys"]:
        if 0.0 < float(k.get("dy", 0.0)) < 100.0:
            k["dy"] = 80.0                      # 2階分＝記録（ほぼ1階分）を越える
    ok &= _expect("陽性対照㉒：屋上の線を2階分下げる", judge_a1(sc, "x")[0], "㉒")
    sc = copy.deepcopy(good)
    sc["tags"][0]["texts"] = ["約3m（ほぼ1階分）"]
    ok &= _expect("陽性対照㉒：札の数を記録と違う言い方に", judge_a1(sc, "x")[0], "㉒")
    sc = copy.deepcopy(good)
    for k in next(p for p in sc["parts"] if p["id"] == "east")["keys"]:
        if float(k.get("dy", 0.0)) > 0.0:
            k["stage"] = 0
    ok &= _expect("陽性対照㉒：東を真ん中より先に落とす", judge_a1(sc, "x")[0], "㉒")
    sc = copy.deepcopy(good)
    sc["src"] = sc["src"].replace("揺れの幅は大きく描いた", "揺れ")
    ok &= _expect("陽性対照㉒：揺れの断りを外す", judge_a1(sc, "x")[0], "㉒")
    b, _ = judge_destroy([good], "c999")
    ok &= _expect("陽性対照⑫：表に無いカットで A1 を崩す", b, "⑫")
    return ok


def selftest_a23():
    """🆕 19本目 ⑤b-3：㉓ A2・A3 と ⑧（縮尺を持たない上から見た絵）の物差しの検算。正しい場面が通り、壊した場面が落ちること"""
    print("■ selftest A2・A3（19本目 ⑤b-3・㉓）")
    import copy
    ok = True
    top = IL.scene("A2", [dict(state=dict(a2park="fall", a2plant="gap", a2gate="on", a2lobby="walk"), rec="TR p1170")],
                   start=dict(a2cars="on", a2deck="part"), rec="TR p1170", assume="崩れた範囲は推定")
    ob = IL.scene("A2", [dict(state=dict(a2zone="both", a2join="on"), rec="TR p1059")], start=dict(view="oblique"), rec="TR p1005")
    a3 = IL.scene("A3", [dict(state=dict(a3water="on", a3ceil="on", a3funnel="on", a3gate="on", a3cars="on"), rec="TR p1132")],
                  rec="TR p1132")
    for nm, sc in (("A2 上から", top), ("A2 南西の上から", ob), ("A3", a3)):
        b = judge_a23(sc, "selftest")[0] + [x for x in judge_scene(sc, "selftest")[0] if x.startswith("⑧")]
        print(f"  {'OK' if not b else '🔴 NG'} 正しい {nm}: {'合格' if not b else '不合格'}（合格のはず）" + (f"  ← {b[0]}" if b else ""))
        ok &= not b

    def geo(sc, kind):
        return next(p["geo"] for p in sc["parts"] if (p.get("geo") or {}).get("kind") == kind)
    sc = copy.deepcopy(top)
    geo(sc, "a2gate")["x"] += 80.0
    ok &= _expect("陽性対照㉓：門を K の線から外す", judge_a23(sc, "x")[0], "㉓")
    sc = copy.deepcopy(top)
    geo(sc, "a2planter").update(x0=860.0, x1=910.0)
    ok &= _expect("陽性対照㉓：プランターを駐車場の側（K の西）へ", judge_a23(sc, "x")[0], "㉓")
    sc = copy.deepcopy(top)
    next(p["geo"] for p in sc["parts"] if (p.get("geo") or {}).get("zone") == "park")["r"][2] = 1200.0
    ok &= _expect("陽性対照㉓：駐車場の落ちた範囲をデッキへはみ出す", judge_a23(sc, "x")[0], "㉓")
    sc = copy.deepcopy(top)
    sc["assume"] = ""
    ok &= _expect("陽性対照㉓：落ちた範囲に推定の札が無い", judge_a23(sc, "x")[0], "㉓")
    sc = copy.deepcopy(top)
    geo(sc, "a2lobby")["y1"] = 420.0
    ok &= _expect("陽性対照㉓：ロビーを塔の外（南）へ", judge_a23(sc, "x")[0], "㉓")
    sc = copy.deepcopy(ob)
    geo(sc, "a2join")["x0"] = 460.0
    ok &= _expect("陽性対照㉓：つなぎ目を西の部分まで延ばす", judge_a23(sc, "x")[0], "㉓")
    sc = copy.deepcopy(a3)
    for p in sc["parts"]:
        if (p.get("geo") or {}).get("what") == "water":
            p["geo"]["x"] = 1180.0
    ok &= _expect("陽性対照㉓：水の筋を別の柱（11.1）に", judge_a23(sc, "x")[0], "㉓")
    sc = copy.deepcopy(a3)
    geo(sc, "a3rows")["rows"] = {"15": 1510.0, "13.1": 1180.0, "11.1": 850.0, "9.1": 520.0}
    ok &= _expect("陽性対照㉓：左右を逆に（左が北）", judge_a23(sc, "x")[0], "㉓")
    sc = copy.deepcopy(a3)
    sc["inset"] = None
    ok &= _expect("陽性対照㉓：A3 の位置の小さな地図を外す", judge_a23(sc, "x")[0], "㉓")
    sc = copy.deepcopy(top)
    sc["people"] = {"resident": (1, "TR p1200")}
    ok &= _expect("陽性対照⑧：縮尺を持たない上から見た絵に人を置く", judge_scene(sc, "x")[0], "⑧")
    b, _ = judge_destroy([top], "c999")
    ok &= _expect("陽性対照⑫：表に無いカットで A2 の駐車場を落とす", b, "⑫")
    return ok


def selftest():
    """物差しの検算。正しい場面が通り、わざと壊した場面（陽性対照）が落ちること。"""
    ok19 = selftest_a1()          # 🆕 19本目 ⑤b-2（本番の表のまま＝見本の差し込みより前）
    ok19 = selftest_a23() and ok19     # 🆕 19本目 ⑤b-3
    # 🆕 2026-10-04（18本目 ⑤b-2）：先に18本目を検算する＝見本の差し込み（16・15・14本目）より前
    #    （2026-10-06〜：18本目も見本 fixture_ep18 の表＝selftest_ep18 が差し込んで・終わったら戻す）
    ok18 = selftest_ep18() and ok19
    # 🔴 2026-10-01（16本目 ⑤b-2）：先に16本目を検算する（2026-10-04〜：16本目も見本 fixture_ep16 の表＝selftest_ep16 が差し込んで・
    #    終わったら戻す）
    ok16 = selftest_ep16() and ok18
    # 🔴 2026-09-30（15本目 ⑤b-2）：先に15本目で RA・RB・RC・RD を検算してから、14本目の見本に差し替える
    #    （2026-10-01〜：15本目も見本 fixture_ep15 の表＝selftest_ep15 が差し込んで・終わったら戻す）
    ok15 = selftest_ep15() and ok16
    # 🔴 2026-09-30（15本目 ⑤b-1）：見本は14本目の実物（置き場 A〜E の部品の既定の rec が14本目の資料を指す）。
    #    本番の表は回ごとに空にする（§0b）＝この処理の中だけ14本目の資料の表・原文・時刻にする
    import fixture_ep14
    fixture_ep14.apply(sys.modules[__name__])
    _pages.cache_clear()          # 🔴 原文の頁の読み込みは覚えている（lru_cache）＝15本目の原文を捨てて14本目を読み直す
    try:
        ok = _selftest_ep14() and ok15
    finally:
        # 🔴 2026-09-30（15本目 ⑤b-2）：selftest のあと本番の表に戻す（戻さないと、本番の照合が14本目の出典の表で15本目の絵を
        #    測る＝⑤b-1 から ⑤b-2 まで本番に案C が無かったので表に出なかった穴）
        fixture_ep14.restore()
        _pages.cache_clear()
    print("selftest:", "通った" if ok else "🔴 落ちた")
    return ok


def _selftest_ep14():
    """14本目（セウォル号）の見本での検算（fixture_ep14 を差し込んだ中で呼ぶ）。"""
    # 資料の表と原文の頁はこの回のもの（置き場の部品の既定の rec がこの回の資料を指すため）
    docs, pages = _ss().REC_DOCS, _pages()
    split = ("9:46", "9:48")
    until = "9:47"
    kw = dict(docs=docs, pages=pages, split=split, until=until)
    good_D = dict(place="D", at="9:46", start=dict(heel=61.2), rec="判決 p18",
                  people=dict(crew=(8, "判決 p11")),
                  steps=[dict(board=8, rec="判決 p18"), dict(state=dict(mark="on", crowd="on"), rec="判決 p18")])
    good_A = dict(place="A", at="9:34", start=dict(heel=52.2, wake="off"), rec="海審 p1057",
                  steps=[dict(touch="3階（B甲板）の左舷"),
                         dict(state=dict(heel=61.2), rec="海審 p1057", touch="船橋甲板の左舷")])
    good_B = dict(place="B", at="8:56", start=dict(view="cabin", heel=30.0, crowd="on"), rec="判決 p12",
                  steps=[dict(rings=2, rec="海審 p1053")])
    good_C = dict(place="C", at="9:25", start=dict(view="room", heel=45.0, crew=8), rec="判決 p14",
                  people=dict(crew=(8, "判決 p11")),
                  steps=[dict(asks=3, rec="判決 p14"), dict(walkie=3, rec="判決 p14"), dict()])
    good_E = dict(place="E", at="9:06", steps=[dict(state=dict(sel="on"), rings=2, rec="海審 p1059"),
                                               dict(rings=1, rec="海審 p1059")])
    good_far = dict(place="D", at="9:30", start=dict(view="far", heel=47.5), rec="艇長の判決 p5002",
                    steps=[dict(), dict(state=dict(binoc="on"), rec="艇長の判決 p5002")])
    good_rail = dict(place="D", at="9:39", start=dict(view="rail", rboat="on", cg="on"), rec="艇長の判決 p5002",
                     people=dict(coast_guard=(1, "艇長の判決 p5002"), crew=(7, "判決 p17")),
                     steps=[dict(board=7, rec="判決 p17"), dict()])
    cases = [
        ("正しい D（8人・群れ 9:46）", good_D, True),
        ("正しい A（52.2度で3階・61.2度で船橋甲板が水面）", good_A, True),
        ("正しい B（客室の群れ 8:56）", good_B, True),
        ("🔴 陽性対照①：傾きを変えた段に rec が無い", dict(good_A, steps=[dict(state=dict(heel=61.2))]), False),
        ("🔴 陽性対照①：rec の頁が資料の範囲の外（判決 p1018）", dict(good_B, rec="判決 p1018"), False),
        ("🔴 陽性対照②：群れを 9:48 の場面に出す", dict(good_D, at="9:48"), False),
        ("🔴 陽性対照③：描いた人 8 ≠ 宣言 7", dict(good_D, people=dict(crew=(7, "判決 p11"))), False),
        ("🔴 陽性対照③：宣言に記録が無い", dict(good_D, people=dict(crew=8)), False),
        ("🔴 陽性対照⑤：札に割れる時刻（9時46分）",
         dict(good_A, steps=[dict(touch="3階（B甲板）の左舷", tag=dict(t="9時46分", at="b_port"))]), False),
        ("🔴 陽性対照⑧：上から見た絵が細かすぎる（1.0 メートル／画素）", dict(good_B, view="上から見た図", scale=1.0), False),
        ("🔴 陽性対照 touch：45度で「3階の左舷が水面に」", dict(good_A, start=dict(heel=45.0, wake="off")), False),
        # ── ⑤b-3（2026-09-29）：置き場 C（操舵室）・E（管制センター）・D の見え方 far／rail ──
        ("正しい C（操舵室に8人・問いかけの印・3階からの無線機）", good_C, True),
        ("正しい E（管制の画面の点に印・交信の輪）", good_E, True),
        ("正しい D far（双眼鏡で甲板→海）", good_far, True),
        ("正しい D rail（立った海洋警察1人・機関部7人がボートへ）", good_rail, True),
        ("🔴 陽性対照①：問いかけの印（asks）の段に rec が無い",
         dict(good_C, steps=[dict(asks=3), dict(walkie=3, rec="判決 p14"), dict()]), False),
        ("🔴 陽性対照①：双眼鏡を上げた段に rec が無い", dict(good_far, steps=[dict(), dict(state=dict(binoc="on"))]), False),
        ("🔴 陽性対照③：操舵室の影 8 ≠ 宣言 9", dict(good_C, people=dict(crew=(9, "判決 p11"))), False),
        ("🔴 陽性対照③：ゴムボートの海洋警察（1人）を宣言しない", dict(good_rail, people=dict(crew=(7, "判決 p17"))), False),
        ("🔴 陽性対照②：乗客の群れを far（遠くの船）に置く",
         dict(good_far, start=dict(view="far", heel=47.5, crowd="on")), False),
    ]
    ok = True
    for name, spec, want in cases:
        try:
            sc = IL.scene(**spec)
            bad, _ = judge_scene(sc, "selftest", **kw)
        except Exception as e:                           # noqa: BLE001
            bad = [f"組めない：{e}"]
        got = not bad
        ok &= got == want
        print(f"  {'OK' if got == want else '🔴 NG'} {name}: {'合格' if got else '不合格'}"
              f"（{'合格' if want else '不合格'}のはず）" + (f"  ← {bad[0]}" if bad else ""))
    # 🔴 陽性対照②（描く側の定数を壊す）：群れの間隔を広げて1人ずつ数えられる形にしたら落ちるか
    keep = IL.CROWD_STEP
    IL.CROWD_STEP = 1.15
    bad, _ = judge_scene(IL.scene(**good_B), "selftest", **kw)
    IL.CROWD_STEP = keep
    good = bool(bad)
    ok &= good
    print(f"  {'OK' if good else '🔴 NG'} 🔴 陽性対照②（描く側）：群れの間隔 1.15＝重ならない影の列: "
          f"{'不合格' if bad else '合格'}（不合格のはず）" + (f"  ← {bad[0]}" if bad else ""))
    # 🔴 陽性対照③（⑤b-3・部品をまたぐ重なり）：乗り移る船員の7人目の立つ所を、ボートで立った海洋警察（別の部品）に重ねる
    keep = IL.RAIL_SPOTS
    IL.RAIL_SPOTS = keep[:6] + ((IL.RAIL_CG[0] + 8.0, IL.RAIL_FLOOR),)
    bad, _ = judge_scene(IL.scene(**good_rail), "selftest", **kw)
    IL.RAIL_SPOTS = keep
    good = any(b.startswith("③") and "重なる" in b for b in bad)
    ok &= good
    print(f"  {'OK' if good else '🔴 NG'} 🔴 陽性対照③（部品をまたぐ重なり）：船員の影を海洋警察の影に重ねる: "
          f"{'不合格' if good else '合格'}（不合格のはず）" + (f"  ← {bad[0]}" if bad else ""))
    # 🔴 陽性対照③（⑤b-3・45度の床）：45度の操舵室で影を床に沿って 60画素ずつに詰めたら「重なる」で落ちるか
    #   （C の影は立てたまま＝fig_deg 0。fig_deg を持つ型紙〈傾けた影〉は、その向きに戻して測る）
    keep = IL.ROOM_FIG
    IL.ROOM_FIG = tuple((700.0 + 60.0 * j, 600.0) for j in range(8))
    bad, _ = judge_scene(IL.scene(**good_C), "selftest", **kw)
    IL.ROOM_FIG = keep
    good = any(b.startswith("③") and "重なる" in b for b in bad)
    ok &= good
    print(f"  {'OK' if good else '🔴 NG'} 🔴 陽性対照③（45度の床）：影を床に沿って 60画素ずつに詰める: "
          f"{'不合格' if good else '合格'}（不合格のはず）" + (f"  ← {bad[0]}" if bad else ""))
    # 🔴 陽性対照②（型紙の役割）：乗客を型紙（1人の影）で置いたら落ちるか
    sc = IL.scene(**good_D)
    for p in sc["parts"]:
        if p.get("kind") == "sprite":
            p["role"] = "passengers"
    bad, _ = judge_scene(sc, "selftest", **kw)
    good = bool(bad)
    ok &= good
    print(f"  {'OK' if good else '🔴 NG'} 🔴 陽性対照②：乗客を1人ずつの型紙で置く: "
          f"{'不合格' if bad else '合格'}（不合格のはず）" + (f"  ← {bad[0]}" if bad else ""))
    # 🔴 陽性対照⑦：決め所・写真のカットに絵
    for name, cid, spec, kind in (("決め所に全面の絵", "x1", dict(fig=("illu", good_B)), "決め所"),
                                  ("写真のカットに冒頭の絵", "x2", dict(photo="a.jpg", intro=dict(illu=good_B)), "写真"),
                                  ("「再現イラスト」の種類なのにパネルで書いた", "x3",
                                   dict(fig=("panel", dict(blocks=[]))), "再現イラスト")):
        bad = [b for b in judge_cut(cid, spec, {cid: kind})[0] if b.startswith("⑦")]
        good = bool(bad)
        ok &= good
        print(f"  {'OK' if good else '🔴 NG'} 🔴 陽性対照⑦：{name}: {'不合格' if bad else '合格'}（不合格のはず）"
              + (f"  ← {bad[0]}" if bad else ""))
    # 🔴 陽性対照④：出典の無い場面（上の層に出典が出ない）
    f = F.illu(**dict(good_B))
    f.illu["src"] = ""
    ov = IL.overlay_svg(f.illu["view"], f.illu["src"])
    good = "出典" not in ov
    ok &= good
    print(f"  {'OK' if good else '🔴 NG'} 🔴 陽性対照④：出典を空にすると上の層に出典が出ない（門番が拾う前提）")
    return ok


def main():
    if not selftest():
        return 2
    if "--selftest" in sys.argv:
        return 0
    import cuts
    kind_of = {c: p.get("kind") for c, p in cuts.PLAN.items()}
    targets = {c: s for c, s in sorted(cuts.SPEC.items())
               if (s.get("fig") or ("",))[0] in ("illu", "illu_pair") or (s.get("intro") or {}).get("illu")
               or kind_of.get(c) == "再現イラスト"}
    others = {c: s for c, s in cuts.SPEC.items() if c not in targets}
    if not targets:
        print("⚠️ 再現イラストのカットが0件（この回に案C が無いなら正しい。**0件を調べて合格**にしていないか確かめる）")
    bad_all, n_all = 0, 0
    for cid, spec in list(targets.items()) + list(others.items()):
        bad, n = judge_cut(cid, spec, kind_of)
        n_all += n
        if bad:
            bad_all += len(bad)
            for b in bad:
                print(f"🔴 {b}")
        elif cid in targets:
            print(f"✓ {cid}（{kind_of.get(cid)}）: 照合 {n}件")
    # 🆕 18本目 ⑤b-3：㉑ 見る向きの合図（PLAN の順に、すぐ前の全面の絵と見る向きが替わるカット）
    b, m = judge_signals([(c, cuts.SPEC[c]) for c in cuts.PLAN if c in cuts.SPEC])
    n_all += m
    if b:
        bad_all += len(b)
        for x in b:
            print(f"🔴 {x}")
    else:
        print(f"✓ ㉑ 見る向きの合図：向きが替わる {m} か所すべてに合図")
    miss = sorted(c for c, k in kind_of.items() if k == "再現イラスト" and c not in cuts.SPEC)
    print(f"\n（参考）PLAN が「再現イラスト」でまだ SPEC の無いカット {len(miss)}：{' '.join(miss)}")
    for t in dict.fromkeys(NOTES):
        print(f"（参考）{t}")
    print(f"{'✓' if not bad_all else '🔴'} 再現イラスト {len(targets)}カット・照合 {n_all}件・食い違い {bad_all}件")
    return 1 if bad_all else 0


if __name__ == "__main__":
    sys.exit(main())
