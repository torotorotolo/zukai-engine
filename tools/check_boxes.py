# -*- coding: utf-8 -*-
"""check_boxes.py — 箱の型（流れ図・書類の再現図・並べ図＝`tools/boxes.py`）の**言葉・つながり・形**を記録と照らす
（2026-09-29 新設・14本目 ⑤b-6）。

■ なぜ要るか
  流れ図は「誰が・どの罪で・どうなったか」を箱のつながりで言う＝**つなぎ違い1本で事実が変わる**（1等航海士に7年の箱を
  つなぐ・無罪の箱を2審でなく1審に置く）。第11章は名前を出さない・人の形を使わない・赤を使わない（責める形にしない）。
  🔴 §5b-88・§5b-93：記録の値（役職・罪名・結果・刑・席の数・欄の名・原因の項目）は**この門番の側に持つ**（`REC_*`）。
  🔴 焼く直前の SVG を読む（画面の文字は `<text>` を全部・席は `data-q="seat"` の四角を数える）。

■ 測るもの
  流れ図 ① 画面の文字が全部、記録の表の言葉（`allowed()`）＝名前・記録に無い言葉が紛れ込まない
         ② 役職→罪名→結果（列＝裁判所）のつながり＝`REC_VERDICT`・役職→刑（点線・大法院の列）＝`REC_SENT`
         ③ 席の数＝裁判官の数（`REC_SEATS`）・灯した席は 0 か全部（全員一致）④ 甲板部・機関部の役職の数と並び＝`REC_CREW`
         ⑤ 赤（ALERT）を使わない・円（人の頭に読める形）を使わない ⑥ 部品の rec の頁
         ⑨ 🆕（15本目 ⑤c'）矢印の線分が箱の内側を通らない（c918＝問い→答えの横線が字の真ん中を通り打ち消し線に見えた）
  書類   ⑦ 表題・欄の名・行き来の箱＝`REC_FORM`（報告書の文にあるものだけ）・欄に値を書かない（記録が「未記入」）・「再現」の札
  並べ図 ⑧ 項目＝`REC_CAUSE`・2つ以上・全部同じ大きさと色（どれかを目立たせない）・項目のほかに絵を置かない（場面にしない）

■ 使い方
    python tools/check_boxes.py              # 全カット
    python tools/check_boxes.py --selftest   # 物差しの検算（陽性対照＝名前・つなぎ違い・席の数・赤・欄・形を壊す）
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE / "tools"))
sys.stdout.reconfigure(encoding="utf-8")

from check_qty import ATTR, EL, _els, _recs, _unesc  # noqa: E402

# ══════════════════════════════════════════════════════════
#  🔴 §0b（題材を替えるとき空にする場所）：記録の言葉・値と頁（この回）
#     🔴 2026-09-30（15本目 リノ ⑤b-1）：**空にした**。14本目（セウォル号）の表は selftest の見本 `tools/fixture_ep14.py`
#        （GATES["check_boxes"]・値は1つも変えていない）。15本目の書類の再現図（記録簿・参加書類・検査の用紙）を書くチャットで、
#        欄の名と頁を ref/ep15/src/ep15_pages.txt で当てて入れる（空のあいだ、箱のカットは「記録に無い言葉」で止まる）
#     🔴 2026-10-01（16本目 バイオントダム災害 ⑤b-1）：15本目の表（REC_OTHER_ROLE・REC_MECH・REC_CHIP・REC_FORM＝報告書の鎖・
#        実況の担当・3つの問いの答え・書類の再現図）も**空にした**。selftest の見本 `tools/fixture_ep15.py`
#        （GATES["check_boxes"]・値は1つも変えていない＝git の `c646174`）。16本目の箱を書くチャットで、言葉と頁を
#        ref/ep16/src/ep16_pages.txt で当てて入れる（空のあいだ、箱のカットは「記録に無い言葉」で止まる）
# ══════════════════════════════════════════════════════════
#     🆕 2026-10-01（16本目 ⑤b-6a）：第1〜6章の箱（流れ図・書類の再現図・並べ図）の言葉と頁を入れた（原文で当てた）
REC_CREW = {}
REC_ROLE_PAGES = set()
REC_OTHER_ROLE = {    # 流れ図の「role」の箱＝役職でない言葉（報告書の文の言葉）→ 頁の集合
    # c113：S1 p99「Il Ministro dei lavori pubblici, con suo decreto dell'11 ottobre 1963 … costituì una Commissione di inchiesta」・
    #   「l'ENEL nominò il 1° novembre 1963 altra Commissione di inchiesta」
    "国の調査委員会": {"S1 p99"}, "電力公社の調査委員会": {"S1 p99"}, "公共事業大臣": {"S1 p99"}, "電力公社": {"S1 p99"},
    # c418：S1 p232（少数派）「all'occultamento alle autorità, ai Prefetti, e al Genio civile di Belluno e di Udine della relazione
    #   Ghetti come delle relazioni Semenza-Giudici e Müller」・p179（多数派）「conosciuti alla Pubblica Amministrazione, benché non
    #   consti che le relazioni siano state ufficialmente trasmesse」
    "2人の地質学者の報告": {"S1 p232"}, "ミュラーの報告": {"S1 p232"}, "模型の報告": {"S1 p232"},
    "国の役所": {"S1 p179", "S1 p232"}, "地方の長官": {"S1 p232"}, "土木局": {"S1 p232"},
    # c510：S1 p89「le prove erano state svolte secondo due diversi indirizzi」＝①「facendolo avvenire per azione della gravità」
    #   ②「rimettersi alle previsioni che poteva fornire lo studio geologico」（④' の照合 G3＝2通りは p89）・S9 p2010「con invaso a
    #   quote comprese tra i 680 e 720 metri」
    "重力で崩す": {"S1 p89"}, "地質の予想どおりに崩す": {"S1 p89"}, "水位680〜720m": {"S9 p2010"},
    # c621：1960年と1962年は下げると止まった（S1 p85＝1961年1月にほぼ0・p93＝1963年3月にほぼ0）／1963年は下げても速まった
    #   （p96「il serbatoio sta calando un metro al giorno」と速さの増え）・p96〜p97（10月8日の報告）「hanno tempestivamente informato le
    #   Autorità competenti … il Sindaco, su invito del Prefetto e del Genio civile, ha emesso una ordinanza per la evacuazione di
    #   persone ed animali dalla zona pericolante」
    "下げると止まった": {"S1 p85", "S1 p93"}, "下げても速まった": {"S1 p96", "S1 p93"},
    "会社": {"S1 p96"}, "役所": {"S1 p96"}, "村長": {"S1 p96"}, "危ない区域から人を出す": {"S1 p96", "S1 p97"},
}
REC_CRIME = {}
REC_VERDICT = {}   # (役職, 罪名, 列) → (結果, 頁)
REC_SENT = {}      # 役職 → (確定した刑, 頁)
REC_SEATS = 0
REC_UNANIMOUS = set()
HEADS = set()
REC_MECH = {          # 流れ図に出してよい言葉のうち、役職・罪名でないもの（仕組み・鎖・問いの箱と矢印の札）
    "議会の報告書",                                         # c113（S1＝議会の調査委員会の最終報告）
    "ダムを高くする", "ためる水が増える", "つくれる電気が増える",   # c207（S1 p63「capacità … elevata」「producibilità annua」）
    "会社",                                                 # c418
    "22回の実験", "波の高さ",                               # c510（S1 p89「i 22 esperimenti compiuti」・S9 p2010「l'entità dell'onda」）
    "1960年", "1962年", "1963年", "10月8日の報告",          # c621（S1 p96＝国の監督の担当者の10月8日の報告）
}
REC_CHIP = {          # 札（chip）の言葉 → 頁の集合
    "1963年10月11日": {"S1 p99"}, "1963年11月1日": {"S1 p99"},                 # c113
    "少数派「隠した」": {"S1 p232"},                                            # c418（occultamento）
    "最も破局的な崩れ": {"S1 p89"},                                            # c510「il più catastrofico prevedibile crollo franoso」
    "いつも2つの塊（少数派）": {"S1 p224"},                                    # c510「sempre partendo dall'ipotesi che si trattasse di due frane distinte」
}
# 書類の再現図（表題 → dict(fields・ends・values＝記録の文にある値だけ・rec＝頁の集合)）。🆕 16本目は欄の値に**原文のイタリア語**を
#   そのまま書く（日本語は字幕だけ＝映像方針の c413・c422 の決め）。欄の名は原文の文の言葉（domanda→問い・risposto→答え・titolo→見出し・
#   prima preoccupazione→第一の心配・è necessario→必要なこと・ondate→波・concludeva→結論・nei riguardi→何に対して・parere→意見・
#   ricerche→研究・lago pieno→湖が満ちたとき・svaso rapido→急に下げるとき・versante→斜面）
REC_FORM = {
    "ミュラーの報告（少数派の報告が引く）": dict(                                       # c413：S1 p217
        fields={"問い", "答え"}, ends=set(), rec={"S1 p217"},
        values={"問い": "se questi franamenti possono venire arrestati mediante misure artificiali",
                "答え": "deve essere risposto negativamente in linea generale"}),
    "ウニタの記事（1961年2月21日）": dict(                                            # c422：S1 p39
        fields={"見出し"}, ends=set(), rec={"S1 p39"},
        values={"見出し": "Una enorme massa di 50 milioni di metri cubi minaccia la vita e gli averi degli abitanti di Erto"}),
    "会社の記録（1960年11月16日）": dict(                                             # c502：S1 p75（⚠️ 原文の PDF の文字は「divello」＝livello の崩れ）
        fields={"第一の心配", "必要なこと", "波"}, ends=set(), rec={"S1 p75"},
        values={"第一の心配": "garantire l'incolumità delle persone che abitano nella valle",
                "必要なこと": "abbassare il livello del serbatoio",
                "波": "non possano assolutamente raggiungere la zona abitata"}),
    "ゲッティの報告（1962年7月3日）": dict(                                           # c512：S1 p89
        fields={"結論", "何に対して"}, ends=set(), rec={"S1 p89"},
        values={"結論": "la quota 700 può considerarsi di assoluta sicurezza",
                "何に対して": "del più catastrofico prevedibile evento di frana"}),
    "模型の研究所の委員会": dict(                                                    # c517：S1 p225（4月30日）・S9 p2012（3月30日）＝月が割れる
        fields={"意見", "研究"}, ends=set(), rec={"S1 p225", "S9 p2012"},
        values={"意見": "almeno per il momento non siano da compiere ricerche",
                "研究": "propagarsi di una onda di piena a valle della diga"}),
    "土木局の手紙（1961年1月7日）": dict(                                             # c617：S1 p78〜p79（lettera 7 gennaio 1961）
        fields={"湖が満ちたとき", "急に下げるとき", "斜面"}, ends=set(), rec={"S1 p79", "S1 p78"},
        values={"湖が満ちたとき": "le acque, eventualmente infiltratesi nel terreno",
                "急に下げるとき": "possano mettersi in pressione",
                "斜面": "pregiudicando la stabilità del versante"}),
    # 🆕 2026-10-01（16本目 ⑤b-6b）：第7・10章の書類の再現図（欄の値＝原文のイタリア語）
    # c705・c707：S1 p96（議会の報告書が引くビアデーネの10月9日の手紙）「Le fessure sul terreno, gli avvallamenti sulla strada, la evidente
    #   inclinazione degli alberi sulla costa che sovrasta la " Pozza ", l'aprirsi della grande fessura che delimita la zona franosa, il
    #   muoversi dei punti anche verso la " Pineda " che finora erano rimasti fermi, fanno pensare al peggio」（Pineda の引用符は外した）・
    #   「questa mattina dovrebbe essere a quota 700. « Penso di raggiungere quota 695 sempre allo scopo di creare una fascia di sicurezza
    #   per le ondate」。欄の名＝fessure・avvallamenti・alberi→地面と道と木・grande fessura→大きな亀裂・punti→目印・questa mattina→
    #   今朝の水位・raggiungere quota→下げる先・allo scopo di→ねらい
    "ビアデーネの手紙（議会の報告書が引く）": dict(
        fields={"地面と道と木", "大きな亀裂", "目印"}, ends=set(), rec={"S1 p96"},
        values={"地面と道と木": "Le fessure sul terreno, gli avvallamenti sulla strada, la evidente inclinazione degli alberi",
                "大きな亀裂": "l'aprirsi della grande fessura che delimita la zona franosa",
                "目印": "il muoversi dei punti anche verso la Pineda che finora erano rimasti fermi"}),
    "ビアデーネの手紙（続き）": dict(
        fields={"今朝の水位", "下げる先", "ねらい"}, ends=set(), rec={"S1 p96"},
        values={"今朝の水位": "questa mattina dovrebbe essere a quota 700",
                "下げる先": "Penso di raggiungere quota 695",
                "ねらい": "creare una fascia di sicurezza per le ondate"}),
    # ca09：S1 p241（もう1つの少数派の報告）「dalla tesi, piuttosto affermata che dimostrata, secondo cui la sciagura del Vajont ha avuto
    #   tutti i caratteri della assòluta imprevedibilità」（⚠️ 原文の PDF の文字「assòluta」＝assoluta の崩れ＝直して書いた）。
    #   欄の名＝tesi→退ける説（「non accettazione … dei giudizi conclusivi」が退ける説）・piuttosto affermata→その説は
    "もう1つの少数派の報告": dict(
        fields={"退ける説", "その説は"}, ends=set(), rec={"S1 p241"},
        values={"退ける説": "la sciagura del Vajont ha avuto tutti i caratteri della assoluta imprevedibilità",
                "その説は": "piuttosto affermata che dimostrata"}),
    # ca19：S9 p2018（財団の年表が記す判決）「1969 … Non viene riconosciuta la prevedibilità della frana」・「1971 … colpevoli di un unico
    #   disastro: inondazione aggravata dalla previsione dell'evento compresa la frana e gli omicidi」。🔴 PLAN の S2 p.718（判決の複写＝
    #   画像だけ）は照らせない＝この頁に当て直した。欄の名＝processo di primo grado→一審・Processo di Cassazione→破毀院
    "判決（財団の年表が記す）": dict(
        fields={"一審", "破毀院"}, ends=set(), rec={"S9 p2018"},
        values={"一審": "Non viene riconosciuta la prevedibilità della frana",
                "破毀院": "inondazione aggravata dalla previsione dell'evento compresa la frana"}),
}
REC_CAUSE = {         # 並べ図の項目 → 頁（c419＝2つの見方を同じ形で並べる・どちらかに決めない）
    "多数派「確認できない」": {"S1 p179"}, "少数派「隠した」": {"S1 p232"},
    # 🆕 2026-10-01（16本目 ⑤b-6b）
    # ca04・ca10：S1 p26「La Commissione ha approvato — con 19 voti favorevoli e 8 contrari — la relazione … alla relazione finale siano
    #   allegate le due relazioni di minoranza」（多数派 p178・少数派 p207・もう1つの少数派 p241）
    "多数派の報告": {"S1 p26", "S1 p178"}, "少数派の報告": {"S1 p26", "S1 p207"}, "もう1つの少数派の報告": {"S1 p26", "S1 p241"},
    # ca17：S9 p2018（控訴審）「riconosce la totale colpevolezza di Biadene e Sensidoni … Frosini e Violin vengono assolti per insufficienza
    #   di prove; Marin e Tonini assolti perché il fatto non costituisce reato; Ghetti per non aver commesso il fatto」・「con lo stralcio
    #   della posizione di Batini, gravemente ammalato」＝有罪2・無罪5・外れた1（11−亡くなった3＝8）
    "有罪 2人": {"S9 p2018"}, "無罪 5人": {"S9 p2018"}, "裁判から外れた 1人": {"S9 p2018"},
    # cb12・cb13：多数派 S1 p178「l'evento, così come si è manifestato, non fu previsto da nessuno」・少数派 S1 p207「un evento prevedibile
    #   e probabile, e quindi evitabile」・破毀院 S9 p2018「inondazione aggravata dalla previsione dell'evento compresa la frana」
    "多数派「その形は誰も予見せず」": {"S1 p178"}, "少数派「予見でき、防げた」": {"S1 p207"},
    "破毀院「予見していた重い過失」": {"S9 p2018"},
}
MARKS = {"？"}
EXTRA = {"模式図"}


def allowed():
    """流れ図の画面に出してよい言葉＝**いまの**記録の表から組む（2026-09-30 15本目 ⑤b-1）。
    ⚠️ 以前は読み込みの瞬間に組んだ定数（ALLOWED）だった＝表を selftest の見本に差し替えても空のまま残る形だった。"""
    return ({t for v in REC_CREW.values() for t in v} | set(REC_OTHER_ROLE) | set(REC_CRIME) | {"有罪", "無罪"}
            | {s for s, _ in REC_SENT.values()} | HEADS | REC_MECH | set(REC_CHIP) | MARKS | EXTRA)
ALERTS = None     # jiko_style の赤（読み込んでから埋める）
TEXT = re.compile(r'<text([^>]*)>([^<]*)</text>')


def _texts(svg):
    """画面の文字（注と出典の行を除く）。"""
    out = []
    for m in TEXT.finditer(svg):
        q = dict(ATTR.findall(m[1])).get("data-q", "")
        if q != "note":
            out.append((q, _unesc(m[2])))
    return out


def _alert_bad(svg):
    import jiko_style as J
    return [f"赤（{c}）を使っている＝責める形にしない" for c in (J.ALERT, J.ALERT_DIM) if c.lower() in svg.lower()]


# ══════════════════════════════════════════════════════════
#  流れ図
# ══════════════════════════════════════════════════════════
def judge_flow(f):
    svg = f.lab + "".join(f.stages)
    bad, n = [], 0
    ok_words = allowed()
    for q, t in _texts(svg):
        n += 1
        if t not in ok_words:
            bad.append(f"画面の文字「{t}」（{q or '印なし'}）が記録の表の言葉に無い＝名前・記録に無い言葉を書かない")
    bad += _alert_bad(svg)
    if "<circle" in svg:
        bad.append("円を使っている（人の頭に読める形＝人の形を使わない）")
    els = _els(svg)
    seats = sum(1 for e in els if e["q"] == "seat")
    on = sum(1 for e in els if e["q"] == "seat_on")
    n += 2
    if seats not in (0, REC_SEATS):
        bad.append(f"席が {seats} 個（裁判官は {REC_SEATS} 人＝判決 p79〜81）")
    if on not in (0, seats):
        bad.append(f"灯した席が {on}／{seats}（全員一致なら全部・そうでなければ灯さない）")
    parts = [p for p in f.mech["parts"]]
    nodes = {p["id"]: p for p in parts if p["k"] in ("role", "crime", "res")}
    edges = [p for p in parts if p["k"] == "edge"]
    ins = {}
    for e in edges:
        for t in (e["to"] if isinstance(e["to"], list) else [e["to"]]):
            ins.setdefault(t, []).append(e)
    # ⑥ 部品の頁
    for p in nodes.values():
        n += 1
        if p["k"] == "role":
            ok = (p["t"] in REC_OTHER_ROLE and _recs(p["rec"]) & REC_OTHER_ROLE[p["t"]]) or \
                 (p["t"] not in REC_OTHER_ROLE and _recs(p["rec"]) & REC_ROLE_PAGES)
        elif p["k"] == "crime":
            ok = _recs(p["rec"]) & REC_CRIME.get(p["t"], set())
        else:
            ok = True     # 結果の頁は ② で組ごとに見る
        if not ok:
            bad.append(f"箱「{p['t']}」の rec {p['rec']} が記録の頁と合わない")

    def up(nid, seen=()):
        """nid から矢印を逆にたどった（役職の list, いちばん近い罪名, 点線か）。"""
        roles, crime, lead = [], None, False
        for e in ins.get(nid, []):
            lead |= e.get("style") == "leader"
            for fr in (e["fr"] if isinstance(e["fr"], list) else [e["fr"]]):
                if fr in seen:
                    continue
                p = nodes.get(fr)
                if not p:
                    continue
                if p["k"] == "role":
                    roles.append(p["t"])
                else:
                    r2, c2, _ = up(fr, seen + (nid,))
                    roles += r2
                    crime = crime or (p["t"] if p["k"] == "crime" else c2)
        return roles, crime, lead

    unanimous = False
    for p in nodes.values():
        if p["k"] != "res":
            continue
        roles, crime, lead = up(p["id"])
        n += 1
        if not roles:
            bad.append(f"結果の箱「{p['t']}」（{p['col']}）に役職がつながっていない")
            continue
        for r in roles:
            n += 1
            if crime:
                want = REC_VERDICT.get((r, crime, p["col"]))
                if not want:
                    bad.append(f"「{r}→{crime}→{p['t']}（{p['col']}）」は記録の表に無い組")
                elif want[0] != p["t"] or not (_recs(p["rec"]) & want[1]):
                    bad.append(f"「{r}→{crime}」の{p['col']}の結果が「{p['t']}」（記録は「{want[0]}」{sorted(want[1])}）")
                unanimous |= (r, crime) in REC_UNANIMOUS and p["col"] == "c3"
            else:
                want = REC_SENT.get(r)
                if not want or want[0] != p["t"] or p["col"] != "c3" or not (_recs(p["rec"]) & want[1]):
                    bad.append(f"「{r}」の刑の箱が「{p['t']}」（{p['col']}）（記録は {want and want[0]}・大法院の列）")
                if not lead:
                    bad.append(f"「{r}」の刑は点線でつなぐ（罪名の矢印と読み分ける）")
    if on and not unanimous:
        bad.append("席が灯っているのに、全員一致の記録（REC_UNANIMOUS）の結果が無い")
    # ④ 甲板部・機関部の役職（cb02）
    grp = {}
    for p in parts:
        if p["k"] == "role" and p.get("grp"):
            grp.setdefault(p["grp"], []).append(p["t"])
    for g, ts in grp.items():
        n += 1
        if sorted(ts) != sorted(REC_CREW.get(g, [])):
            bad.append(f"{g}の役職 {len(ts)}人 {ts} が記録（判決 p2〜3）の {len(REC_CREW.get(g, []))}人と違う")
    for p in parts:
        if p["k"] == "chip":
            n += 1
            if not (_recs(p["rec"]) & REC_CHIP.get(p["t"], set())):
                bad.append(f"札「{p['t']}」の rec {p['rec']} が記録の頁と合わない")
    # ⑨ 🆕 2026-09-30（15本目 ⑤c'）：矢印の線が箱の中を通らない。c918 の問い（上）→答え（真下）は横の線が両方の字の
    #    真ん中を通り、打ち消し線に見えた（原寸）＝型は「左→右」しか描けなかった。字は箱の中にある＝箱の内側（辺から3画素）
    #    に線分が入ったら止める。線分は型が描いたものそのもの（`segs`＝boxes._edge）
    rects = [(p["id"], p["x0"], p["x1"], p["cy"] - p["h"] / 2, p["cy"] + p["h"] / 2)
             for p in list(nodes.values()) + list(f.mech.get("heads") or [])]
    hit = set()
    for e in edges:
        ek = (str(e["fr"]), str(e["to"]))       # fr・to はリストのこともある（寄せる・分ける矢印）＝文字にして鍵に
        for x1, y1, x2, y2 in e.get("segs") or []:
            n += 1
            for bid, bx0, bx1, by0, by1 in rects:
                if ek + (bid,) not in hit and _seg_enters(x1, y1, x2, y2, bx0 + 3, bx1 - 3, by0 + 3, by1 - 3):
                    hit.add(ek + (bid,))
                    bad.append(f"矢印 {e['fr']}→{e['to']} の線が箱「{bid}」の中を通る（字に打ち消し線が引かれて見える）")
    return bad, n


def _seg_enters(x1, y1, x2, y2, bx0, bx1, by0, by1):
    """線分が箱の内側に入るか（2画素ごとに当てる）。"""
    k = max(1, int(max(abs(x2 - x1), abs(y2 - y1)) / 2))
    return any(bx0 < x1 + (x2 - x1) * i / k < bx1 and by0 < y1 + (y2 - y1) * i / k < by1 for i in range(k + 1))


# ══════════════════════════════════════════════════════════
#  書類の再現図
# ══════════════════════════════════════════════════════════
def judge_form(f):
    svg = f.lab + "".join(f.stages)
    els = _els(svg)
    bad, n = [], 3
    title = next((_unesc(e["text"]) for e in els if e["q"] == "ftitle"), "")
    r = REC_FORM.get(title)
    if not r:
        return [f"書類の表題「{title}」が記録の表に無い"], n
    fields = {_unesc(e["text"]) for e in els if e["q"].startswith("field|")}
    ends = {_unesc(e["text"]) for e in els if e["q"].startswith("ntext|role|")}
    if not fields <= r["fields"]:
        bad.append(f"欄 {sorted(fields - r['fields'])} は報告書の文に無い（無い欄を描かない）")
    if not ends <= r["ends"]:
        bad.append(f"行き来の箱 {sorted(ends - r['ends'])} が記録に無い")
    for e in els:
        if e["q"].startswith("fval|"):
            n += 1
            nm = e["q"].split("|", 1)[1]
            if r["values"].get(nm) != _unesc(e["text"]):
                bad.append(f"欄「{nm}」に値「{_unesc(e['text'])}」（記録は {r['values'].get(nm) or '未記入'}）")
    tag = next((_unesc(e["text"]) for e in els if e["q"] == "reprot"), "")
    if tag != "再現":
        bad.append(f"「再現」の札が無い（「{tag}」）＝自作の用紙だと画面で言う")
    for p in f.mech["parts"]:
        n += 1
        rs = _recs(p["rec"])
        if not (rs & r["rec"]):
            bad.append(f"{p['k']} の rec {p['rec']} が記録の頁 {sorted(r['rec'])} と合わない")
        for fd in p.get("fields") or []:
            n += 1
            if not (_recs(fd["rec"]) & r["rec"]):
                bad.append(f"欄「{fd['t']}」の rec {fd['rec']} が記録の頁と合わない")
    bad += _alert_bad(svg)
    return bad, n


# ══════════════════════════════════════════════════════════
#  並べ図
# ══════════════════════════════════════════════════════════
def judge_row(f):
    svg = f.lab + "".join(f.stages)
    els = _els(svg)
    bad, n = [], 2
    items = [e for e in els if e["q"].startswith("item|")]
    if len(items) < 2:
        bad.append(f"並べる項目が {len(items)} つ（2つ以上を同じ形で並べる）")
    forms = {(e["a"].get("width"), e["a"].get("height"), e["a"].get("stroke")) for e in items}
    if len(forms) > 1:
        bad.append(f"項目の箱の形か色が揃っていない {sorted(forms)}＝どれかを目立たせない")
    for q, t in _texts(svg):
        n += 1
        if not (q.startswith("itext|") and t in REC_CAUSE):
            bad.append(f"画面の文字「{t}」（{q or '印なし'}）が原因の項目の表に無い＝並べ図に項目のほかを書かない")
    for e in els:
        if e["q"] not in ("note",) and not e["q"].startswith(("item|", "itext|")):
            bad.append(f"並べ図に項目のほかの部品（{e['q']}）＝場面にしない")
    if re.search(r"<(circle|path|polygon)\b", svg):
        bad.append("並べ図に線や絵（path・circle）がある＝場面にしない")
    for p in f.mech["parts"]:
        n += 1
        if not (_recs(p["rec"]) & REC_CAUSE.get(p["t"], set())):
            bad.append(f"項目「{p['t']}」の rec {p['rec']} が記録の頁と合わない")
    bad += _alert_bad(svg)
    return bad, n


def judge(kw):
    import boxes as B
    f = B.boxes(**kw)
    return {"flow": judge_flow, "form": judge_form, "row": judge_row}[kw["view"]](f)


# ══════════════════════════════════════════════════════════
#  物差しの検算
# ══════════════════════════════════════════════════════════
def selftest_ep15():
    """15本目（⑤b-5）の書類の再現図・鎖・答えの図・実況の担当の検算＝**見本 `fixture_ep15`（15本目の表）を差し込んで**回す。
    🔴 2026-10-01（16本目 ⑤b-1）：本番の表（この門番の REC_*）は16本目の空の器にした＝15本目の値は
       `fixture_ep15.GATES["check_boxes"]`（14本目と同じ作り）。型の側の表（ss.FORM_ENTRY09・CHAIN2・ANS・MC ほか）と GEO も
       15本目の見本になる＝落ちても終わっても `restore()` で本番の値へ戻す（try/finally）。本体は `_selftest_ep15`"""
    import fixture_ep15
    fixture_ep15.apply(sys.modules[__name__])
    try:
        return _selftest_ep15()
    finally:
        fixture_ep15.restore()


def _selftest_ep15():
    """15本目の検算の本体（`fixture_ep15` を差し込んだ中で呼ぶ）。"""
    from cuts import ss
    entry = dict(view="form", form=ss.FORM_ENTRY09, note="n", src="s",
                 steps=[dict(add=dict(k="paper")), dict(add=dict(k="fill", f="大きな改造をしたか"))])
    bad_v = dict(ss.FORM_ENTRY09, fields=[dict(ss.FORM_ENTRY09["fields"][0], v="いいえ")])
    bad_f = dict(ss.FORM_ENTRY09, fields=[dict(t="飛んだ時間", rec="AAB p37")])     # 型は通す＝門番が止めるか
    chain = dict(view="flow", layout=ss.CHAIN2, steps=[dict(add=ss.chain_links())], note="n", src="s")
    bad_w = dict(chain, layout=dict(heads=ss.CHAIN2["heads"][:5] + [dict(ss.CHAIN2["heads"][5], t="墜落の原因")]))
    # 🆕 ⑤c'（2026-09-30）：答えと手がかり（c918）＝問い（上）→答え（真下）の矢印
    ans = dict(view="flow", layout=ss.ANS, steps=[dict(add=[ss.ANSP["a1"], ss.ANSP["a2"], ss.ANSP["a3"]] + ss.ans_links())],
               note="n", src="s")
    cases = [("15本目 正しい参加の書類（後から「はい」）", entry, True),
             ("🔴 15本目 陽性対照：書き込む値が記録と違う（いいえ）", dict(entry, form=bad_v), False),
             ("🔴 15本目 陽性対照：報告書の文に無い欄", dict(entry, form=bad_f, steps=[dict(add=dict(k="paper"))]), False),
             ("15本目 正しい報告書の鎖", chain, True),
             ("🔴 15本目 陽性対照：鎖に記録の表に無い言葉", bad_w, False),
             ("15本目 正しい答えの図（問い→真下の答えは縦の矢印）", ans, True),
             # ⚠️ ⑤c'：⑨ を足した最初の版は、fr・to がリストの矢印（分ける・寄せる）で門番ごと落ちた（本番の c806 で）
             #    ＝見本が1対1の矢印だけだった → 分ける矢印の見本を置く
             ("15本目 正しい実況の担当（1つから2つへ分ける矢印）",
              dict(view="flow", layout=ss.MC, note="n", src="s",
                   steps=[dict(add=[ss.MCP["a_help"], ss.MCP["a_med"], dict(k="edge", fr="mc", to=["a_help", "a_med"])])]),
              True)]
    ok = True
    for name, kw, want in cases:
        try:
            bad, _ = judge(kw)
        except ValueError as e:
            bad = [f"型が止まった：{e}"]
        got = not bad
        ok &= got == want
        print(f"  {'OK' if got == want else '🔴 NG'} {name}: {'合格' if got else '不合格'}"
              f"（{'合格' if want else '不合格'}のはず）" + (f"  ← {bad[0]}" if bad else ""))
    # 🔴 陽性対照（型を壊す）：縦の矢印を切る（VERT=False）＝⑤c の c918 と同じ絵（横の線が問いと答えの字を通る）→ ⑨ が鳴ること
    import boxes as B
    keep = B.VERT
    B.VERT = False
    try:
        bad, _ = judge(ans)
    finally:
        B.VERT = keep
    hit7 = any("の中を通る" in b for b in bad)
    ok &= hit7
    print(f"  {'OK' if hit7 else '🔴 NG'} 🔴 15本目 陽性対照（型を壊す）：縦の矢印を切る（VERT=False）: "
          f"{'不合格' if bad else '合格'}（⑨で不合格のはず）" + (f"  ← {bad[0]}" if bad else ""))
    return ok


def selftest():
    # 🔴 2026-09-30（15本目 ⑤b-5）：先に15本目の書類と鎖を検算してから、14本目の見本に差し替える
    #    （2026-10-01〜：15本目も見本 fixture_ep15 の表＝selftest_ep15 が差し込んで・終わったら戻す）
    ok15 = selftest_ep15()
    # 🔴 2026-09-30（15本目 ⑤b-1）：見本は14本目の実物（本番の表は回ごとに空にする＝§0b）＝この処理の中だけ14本目にする
    import fixture_ep14
    fixture_ep14.apply(sys.modules[__name__])
    import boxes as B
    from cuts import ss
    ok = True
    cap = [ss.ct("r_captain"), ss.ct("x_cap"), ss.ce("r_captain", "x_cap"), ss.ct("o_cap"), ss.ce("x_cap", "o_cap"),
           dict(k="seats_on", n=13, rec="判決 p39")]
    sent = [ss.ct("r_mate1"), ss.ct("s_mate1"), ss.ce("r_mate1", "s_mate1", style="leader")]
    flow = dict(view="flow", layout=ss.CT, steps=[dict(add=cap), dict(add=sent)], src="s")
    crew = dict(view="flow", layout=ss.CT, steps=[dict(add=ss.CREW15)], src="s")
    form = dict(view="form", form=ss.FORM_PRE, steps=[dict(add=[dict(k="end", id="ship"), dict(k="paper"),
                                                                dict(k="edge", fr="ship", to="paper")])], src="s")
    row = dict(view="row", slots=3, steps=[dict(add=[ss.cause("rudder"), ss.cause("fault")])], src="s")

    def run(name, kw, want):
        nonlocal ok
        try:
            bad, _ = judge(kw)
        except (ValueError, KeyError) as e:
            bad = [f"型が止まった：{type(e).__name__} {e}"]
        got = not bad
        ok &= got == want
        print(f"  {'OK' if got == want else '🔴 NG'} {name}: {'合格' if got else '不合格'}（{'合格' if want else '不合格'}のはず）"
              + (f"  ← {bad[0]}" if bad else ""))

    run("正しい流れ図（船長→殺人・殺人未遂→有罪・13席・1等航海士→懲役12年）", flow, True)
    run("正しい船員15人（甲板部8・機関部7）", crew, True)
    run("正しい書類の再現図（乗船人員・貨物量・空欄）", form, True)
    run("正しい並べ図（舵の使い方？・装置の故障？）", row, True)
    run("🔴 陽性対照：役職の箱に名前（山田船長）", dict(flow, steps=[dict(add=[ss.ct("r_captain", t="山田船長")] + cap[1:])]), False)
    run("🔴 陽性対照：刑のつなぎ違い（1等航海士→懲役7年）",
        dict(flow, steps=[dict(add=cap), dict(add=[ss.ct("r_mate1"), ss.ct("s_mate2", row="1等航海士"),
                                                   ss.ce("r_mate1", "s_mate2", style="leader")])]), False)
    run("🔴 陽性対照：無罪の箱を1審の列に（舵の過失）",
        dict(flow, steps=[dict(add=[ss.ct("r_mate3"), ss.ct("x_rudder"), ss.ce("r_mate3", "x_rudder"),
                                    ss.ct("o_rud2", col="c1"), ss.ce("x_rudder", "o_rud2")])]), False)
    run("🔴 陽性対照：席が12", dict(flow, layout=dict(ss.CT, seats=dict(ss.CT["seats"], n=12))), False)
    run("🔴 陽性対照：甲板部の役職が1人欠ける", dict(crew, steps=[dict(add=ss.CREW15[:2] + ss.CREW15[3:])]), False)
    run("🔴 陽性対照：書類に報告書に無い欄（船長の署名）",
        dict(form, form=dict(ss.FORM_PRE, fields=list(ss.FORM_PRE["fields"]) + [dict(t="船長の署名", rec="海審 p1037")])),
        False)
    run("🔴 陽性対照：書類の欄に値（乗船人員 476）",
        dict(form, form=dict(ss.FORM_PRE, fields=[dict(t="乗船人員", rec="海審 p1037", v="476人")])), False)
    run("🔴 陽性対照：並べ図に記録に無い項目（爆発？）",
        dict(row, steps=[dict(add=[ss.cause("rudder"), dict(k="item", t="爆発？", rec="特調委 p3013")])]), False)
    run("🔴 陽性対照：並べ図の項目が1つ", dict(row, steps=[dict(add=[ss.cause("rudder")])]), False)

    def broken(name, obj, attr, val, kw):
        nonlocal ok
        keep = getattr(obj, attr)
        setattr(obj, attr, val)
        try:
            bad, _ = judge(kw)
        except (ValueError, KeyError) as e:
            bad = [f"型が止まった：{e}"]
        finally:
            setattr(obj, attr, keep)
        ok &= bool(bad)
        print(f"  {'OK' if bad else '🔴 NG'} 🔴 陽性対照（型を壊す）：{name}: {'不合格' if bad else '合格'}（不合格のはず）"
              + (f"  ← {bad[0]}" if bad else ""))

    broken("結果の箱を赤で描く（KSTY）", B, "KSTY", dict(B.KSTY, res=("ALERT", 28, 40)), flow)
    broken("「再現」の札を書かない（REPRO）", B, "REPRO", "", form)
    import titan_fig as F
    rect0 = F.rect
    cnt = [0]

    def uneven(x, y, w, h, *a, **k):
        cnt[0] += 1
        return rect0(x, y, w + (40 if cnt[0] == 1 else 0), h, *a, **k)
    broken("並べ図の最初の箱だけ広く描く（F.rect）", F, "rect", uneven, row)
    ok = ok and ok15
    print("selftest:", "通った" if ok else "🔴 落ちた")
    return ok


def main():
    if not selftest():
        return 2
    if "--selftest" in sys.argv:
        return 0
    import fixture_ep14
    fixture_ep14.restore()       # 🔴 15本目 ⑤b-2：selftest で差し込んだ14本目の見本を本番の表に戻す（戻さないと14本目の表で本番を測る）
    import cuts
    targets = {c: s["fig"][1] for c, s in sorted(cuts.SPEC.items()) if s.get("fig") and s["fig"][0] == "boxes"}
    if not targets:
        print("⚠️ boxes のカットが0件（この回に流れ図・書類・並べ図が無いなら正しい。**0件を調べて合格**にしていないか確かめる）")
        return 0
    bad_all, n_all = 0, 0
    for cid, kw in targets.items():
        bad, n = judge(kw)
        n_all += n
        if bad:
            bad_all += len(bad)
            for b in bad:
                print(f"🔴 {cid}（boxes・{kw['view']}）: {b}")
        else:
            print(f"✓ {cid}（boxes・{kw['view']}）: 言葉・つながり・形 {n}件が記録と合う")
    print(f"\n{'✓' if not bad_all else '🔴'} 箱の型 {len(targets)}カット・照合 {n_all}件・食い違い {bad_all}件")
    return 1 if bad_all else 0


if __name__ == "__main__":
    sys.exit(main())
