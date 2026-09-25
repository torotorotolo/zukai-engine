# -*- coding: utf-8 -*-
r"""check_aq_yomi.py — ゆっくり（AquesTalk）の読みの門番（2026-09-25・14本目⑤a 新設）。

  python tools/check_aq_yomi.py              … 門番（E があれば exit 1・fail closed）
  python tools/check_aq_yomi.py --propose    … 数の台帳の下書き（台本の数を全部拾い、語だけの読みと文の中の読みを並べる）
  python tools/check_aq_yomi.py --selftest   … 答えの分かっている入力で検算

■ なぜ要るか
  ElevenLabs の時代は「数は聞取で検証できない」（聞取が正しい字で書き戻す）ので、数を先回りでかなに固定し
  `check_yomi_numbers` が「固定されていない数」を拾っていた（ルール 5a-6）。
  ゆっくりは読みを**音声記号列で渡す**（tools/aq_kana.py）＝合成の前に読みが文字で見える。
  → **台本の数を1つ残らず台帳（人が1回確かめた読み）に当て、音声記号列の読みと突き合わせる**。
    台帳は pyopenjtalk の出力から下書きし（--propose）、人が台本 §6-1 を答えにして直してから置く。
    台帳が pyopenjtalk の写しのままだと自分の答えを自分で採点する形になる＝**下書きは必ず人が読む**。

■ 見るもの（全部 fail closed）
  ① 全行が音声記号列にできる（aq_kana の E＝表に無い音節・英数字の落ち）・手書き override が仕様の形
  ② 🔴 数：台本の数（算用数字の頭）ごとに、台帳 ref/<SLUG>/aq/numbers.tsv の**いちばん長い鍵**を当てる
       ・台帳に無い数＝E（新しい数が黙って通らない）
       ・台帳の読みが、その行の読みに**順番どおり**無い＝E
       ・台本のどこにも当たらない鍵＝E（前の版の残り）
  ③ 利用者辞書 userdict.csv の語が台本のどこかに当たる（当たらない語＝書き損じ・前の版の残り）
  ④ override.tsv の行IDが台本にある（aq_kana.sheet が数える）
"""
import csv
import re
import sys
import unicodedata
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import aq_kana as AQ  # noqa: E402

NUM_START = re.compile(r"(?<![0-9.,])[0-9]")
# 下書きの鍵＝数＋うしろの漢字・カタカナ（4字まで）＋送りの「り」「つ」。「4つ」「2通り」も拾う
PROPOSE_KEY = re.compile(r"[0-9][0-9.,]*(?:[一-鿿ァ-ヴー]{1,4}[りつ]?|つ)?")
PUNCT = re.compile(r"[、。？,;+/']")


def norm(text):
    """照合に使う文（聞き役の印・★・括弧を外し、全角の英数字を半角へ）。"""
    return unicodedata.normalize("NFKC", AQ._pre(text))


def flat(aq):
    """音声記号列 → 句切り・アクセントの印を外した読み。"""
    return PUNCT.sub("", aq)


def ledger_path():
    return AQ.ep_dir() / "numbers.tsv"


def load_ledger(p=None):
    p = p or ledger_path()
    if not p.exists():
        raise SystemExit(f"🔴 数の台帳が無い: {p}（先に --propose で下書きを作り、人が確かめてから置く）")
    out = {}
    for n, ln in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        if not ln.strip() or ln.startswith("#") or ln.startswith("鍵\t"):
            continue
        parts = ln.split("\t")
        if len(parts) < 2 or not parts[0] or not parts[1]:
            raise SystemExit(f"🔴 台帳 {n}行目の形が違う（鍵<TAB>読み<TAB>注）: {ln!r}")
        k, r = parts[0].strip(), parts[1].strip()
        if not NUM_START.match(k):
            raise SystemExit(f"🔴 台帳 {n}行目の鍵が数字で始まらない: {k!r}")
        if k in out and out[k] != r:
            raise SystemExit(f"🔴 台帳の鍵「{k}」が2つの読みを持つ（{out[k]} ／ {r}）")
        out[k] = r
    return out


def check_numbers(rows, ledger):
    """rows＝aq_kana.sheet() の行。戻り値＝(E の一覧, 当たった鍵の集合, 数えた数)。"""
    E, used, n = [], set(), 0
    keys = sorted(ledger, key=len, reverse=True)
    for lid, _who, body, aq, _pl, _src, _e, _w in rows:
        t = norm(body)
        rd = flat(aq)
        cur = end = 0
        for m in NUM_START.finditer(t):
            if m.start() < end:
                continue                  # 当てた鍵の中の数（「4月1日」の 1）は数え直さない
            n += 1
            k = next((k for k in keys if t.startswith(k, m.start())), None)
            if k is None:
                E.append(f"{lid} 台帳に無い数「{t[m.start():m.start() + 8]}」＝読みを確かめて台帳へ（{body}）")
                continue
            used.add(k)
            end = m.start() + len(k)
            i = rd.find(ledger[k], cur)
            if i < 0:
                E.append(f"{lid} 「{k}」の読みが台帳と違う：台帳「{ledger[k]}」／ 読み「{rd}」")
            else:
                cur = i + len(ledger[k])
    return E, used, n


def check_userdict(rows):
    """利用者辞書の語が台本に当たるか（表層は全角で書く＝NFKC で揃えて比べる）。"""
    p = AQ.ep_dir() / "userdict.csv"
    if not p.exists():
        return [], 0
    texts = [unicodedata.normalize("NFKC", r[2]) for r in rows]
    E, n = [], 0
    for r in csv.reader(p.read_text(encoding="utf-8").splitlines()):
        if not r or r[0].startswith("#"):
            continue
        n += 1
        w = unicodedata.normalize("NFKC", r[0])
        if not any(w in t for t in texts):
            E.append(f"利用者辞書の語「{r[0]}」は台本のどの行にも当たらない（書き損じ・前の版の残り）")
    return E, n


def run():
    rows, n_dict, stale = AQ.sheet(write=False)
    E = [f"{r[0]} {e}" for r in rows for e in r[6]]
    W = [f"{r[0]} {w}" for r in rows for w in r[7]]
    E += [f"override.tsv の行ID {lid} は台本に無い" for lid in stale]
    ledger = load_ledger()
    e2, used, n_num = check_numbers(rows, ledger)
    E += e2
    E += [f"台帳の鍵「{k}」は台本のどこにも当たらない（前の版の残り）" for k in sorted(set(ledger) - used)]
    e3, n_ud = check_userdict(rows)
    E += e3
    for x in E:
        print("🔴 E", x)
    for x in W:
        print("⚠️ W", x)
    print(f"行 {len(rows)}・数 {n_num}（台帳 {len(ledger)}鍵・当たった {len(used)}）・利用者辞書 {n_ud}語")
    print(f"E {len(E)}件 / W {len(W)}件")
    return 1 if E else 0


def propose():
    """数の台帳の下書き。鍵ごとに（語だけの読み・文の中にあるか・行）を出す。**人が確かめてから台帳へ**。"""
    rows, _, _ = AQ.sheet(write=False)
    seen = {}
    for lid, _who, body, aq, _pl, _src, _e, _w in rows:
        t = norm(body)
        rd = flat(aq)
        for m in NUM_START.finditer(t):
            k = PROPOSE_KEY.match(t, m.start()).group(0)
            r0 = flat(AQ.to_aq(k)[0])
            ok = r0 in rd
            e = seen.setdefault(k, {"r0": r0, "ok": True, "lids": []})
            e["ok"] &= ok
            e["lids"].append(lid)
    print("鍵\t語だけの読み\t文の中\t行")
    for k in sorted(seen, key=lambda x: (not seen[x]["ok"], x)):
        e = seen[k]
        print(f"{k}\t{e['r0']}\t{'○' if e['ok'] else '✕要確認'}\t{','.join(e['lids'][:6])}"
              + (f" ほか{len(e['lids']) - 6}" if len(e["lids"]) > 6 else ""))
    return 0


def selftest():
    ok = True

    def chk(name, got, want):
        nonlocal ok
        good = got == want
        ok = ok and good
        print("  %s %-34s 期待 %-10r 実際 %r" % ("OK " if good else "🔴NG", name, want, got))

    led = {"9時": "くじ", "4人": "よにん", "4月1日": "しがつついたち", "1日": "いちにち"}

    def one(body, aq, ledger=led):
        e, used, n = check_numbers([("x-1", "", body, aq, "", "auto", [], [])], ledger)
        return len(e), sorted(used), n

    chk("台帳どおりなら E 0", one("9時に4人。", "く'じに/よ'にん。"), (0, ["4人", "9時"], 2))
    chk("🔴読みが違えば E", one("9時に4人。", "きゅ'ーじに/よ'にん。")[0], 1)
    chk("🔴台帳に無い数は E", one("7人が来た。", "なな'にんが/き'た。")[0], 1)
    chk("いちばん長い鍵を当てる（4月1日）", one("4月1日に。", "しがつ'/ついたち'に。"), (0, ["4月1日"], 1))
    chk("短い鍵は別の文で当たる（1日）", one("1日で。", "いちにち'で。"), (0, ["1日"], 1))
    chk("🔴順番どおりでなければ E", one("4人が9時に。", "く'じに/よ'にんが。")[0], 1)
    chk("小数の中の数字は数え直さない", len(list(NUM_START.finditer("約1.75メートル"))), 1)
    chk("全角の数字も拾う", len(list(NUM_START.finditer(norm("４人")))), 1)
    chk("下書きの鍵：数＋助数詞", PROPOSE_KEY.match("4通りの").group(0), "4通り")
    chk("下書きの鍵：4つ", PROPOSE_KEY.match("4つ備えて").group(0), "4つ")
    chk("下書きの鍵：小数＋単位", PROPOSE_KEY.match("2.4メートル、").group(0), "2.4メートル")
    print("check_aq_yomi selftest:", "PASS" if ok else "🔴FAIL")
    return ok


def main():
    if "--selftest" in sys.argv:
        return 0 if selftest() else 1
    if "--propose" in sys.argv:
        return propose()
    return run()


if __name__ == "__main__":
    sys.exit(main())
