# -*- coding: utf-8 -*-
"""`ref/ep8/clips.json` と `ref/ep8/shots.json` を**実測から**書き出す（手で書かない）。

■ なぜ要るか
  `tools/footage.py` は `CLIPS`（素材の台帳）と `SHOTS`（1秒刻みのショット）を
  この2つのファイルから読む。**題材を替えたら、この2つも替える。**
  ⚠️ 7本目のまま残すと `footage.USE` の欄が 9.11 の映像を指したまま焼ける
  （→ [[feedback-per-episode-constants-go-stale]]）。

■ 🔴 `dispw`（絵が実際に写っている幅）は器の札ではなく ②の実測から書く
  ＝[[feedback-container-labels-lie-about-the-picture]]。
  `ref/ep8/kousei.md` §3 の表（コマごとに黒帯を除いて測った中央値）が正本。
  ⚠️ `fdcomm` は器が 1280 でも絵は **984**。`sts1` は **948**。

■ ⚠️ 権利の根拠は1種類ではない（→ [[feedback-pd-label-hides-two-different-grounds]]）
  9本とも Commons の札は「パブリックドメイン」だが、根拠が違う：
    ・NASA の職務著作 … `mct` `mc0201` `fdcomm` `cabin` `fd16` `fdbrief` `sts1` `tank`
    ・🔴 `guncam` … **訓練中のオランダ人搭乗員**が米陸軍 AH-64D の照準カメラで撮ったもの。
      「米連邦職員の職務著作」でそのまま説明できない。**出典には事実だけを書く**。
      ✅ 2026-09-15（⑥）に Commons の原文を取り直した。**出回っている版は NASA の録画**＝
        元の機密テープをバークスデール空軍基地で NASA 職員が一部録画し、
        **その録画が 2003年2月12日に公開された**。§105 で説明できるのはこの「NASA の録画」。
        → 画面の出典に**公開の経路**（NASA が同年2月12日に公開）を足した（カズヤくん判断）。
      ⚠️ **残る不確かさは消えていない**＝Commons の Author 欄は空・元の撮影は米連邦職員でない。
  `mct` は第三者が作った左右分割の編集物だが、説明文に
  「Copyrighted-portions of this film have been removed to maintain NASA Public-Domain status」
  とあり、**著作部分を除いたうえで PD**。そのことを注記に残す。

    python qa_out/ep8_clips.py            # 書き出す
    python qa_out/ep8_clips.py --check    # 書き出さずに突き合わせだけ
"""
from __future__ import annotations

import io
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

VID = HERE / 'ref' / 'ep8' / 'vid'
OUT_CLIPS = HERE / 'ref' / 'ep8' / 'clips.json'
OUT_SHOTS = HERE / 'ref' / 'ep8' / 'shots.json'
SRC_SHOTS = HERE / 'analytics' / 'materials' / 'ep8_shots.json'

# 🔴 ②の実測（`ref/ep8/kousei.md` §3）。**器の札ではない。**
DISPW = dict(mct=1918, tank=1280, fdcomm=984, sts1=948, mc0201=646,
             fd16=614, fdbrief=469, cabin=315, guncam=640)

CREDIT = {
    'mct': '出典：NASA／2003年2月1日の管制室と事後の遠隔測定の解析／パブリックドメイン',
    'mc0201': '出典：NASA／2003年2月1日 ジョンソン宇宙センター管制室／パブリックドメイン',
    'fdcomm': '出典：NASA／2003年2月1日 飛行主任の通信ループ／パブリックドメイン',
    'cabin': '出典：NASA／STS-107 機内の記録／パブリックドメイン',
    'fd16': '出典：NASA ジョンソン宇宙センター／2003年1月31日の説明会／パブリックドメイン',
    'fdbrief': '出典：NASA ジョンソン宇宙センター／事故後の説明会／パブリックドメイン',
    'sts1': '出典：NASA／1981年4月 STS-1 の記録映像／パブリックドメイン',
    'tank': '出典：NASA ケネディ宇宙センター／2011年 ナコドーチェス湖／パブリックドメイン',
    # 🔴 根拠が NASA の職務著作ではない。**分かっている事実だけを書く。**
    'guncam': '出典：2003年2月1日 テキサス州フォートフッド／'
              'AH-64D の照準カメラの記録／NASA が同年2月12日に公開／パブリックドメイン',
}

NOTE = {
    'mct': '⚠️ 第三者が作った左右分割の編集物。著作部分を除いて PD として公開されている。'
           '画面の時刻は **GMT**（−5時間で EST）',
    'mc0201': 'VHS からの取り込み。飛行主任 LeRoy Cain。額装パネル',
    'fdcomm': '⚠️ 器は 1280×720 だが絵は **984px**（4:3 を黒帯で埋めたもの）',
    'cabin': '⚠️ 使うのは `c411` だけ。**再突入中の機内映像は画にも言葉にも出さない**'
             '（CAIB p232／台本 §1-2）',
    'fd16': '飛行16日目の会見。額装パネル',
    'fdbrief': 'この回では使わない（台本 §5-1）',
    'sts1': '⚠️ **0〜10秒は NASA の表紙**（連絡先つき）。使えるのは10秒以降',
    'tank': '⚠️ **タンクが写るのは 12〜22秒と34〜44秒だけ。**残りは2011年の解説者',
    'guncam': '🔴 **0〜9秒は投稿者が付けた英語の表紙。**使えるのは9秒以降。'
              'HUD の時刻は **Zulu**（−5時間で EST）。英字は隠すか切る',
}

DATE = dict(mct='2003-02-01', mc0201='2003-02-01', fdcomm='2003-02-01',
            cabin='2003-02-01', fd16='2003-01-31', fdbrief='2003-02-14',
            sts1='1981-04-12', tank='2011-07-29', guncam='2003-02-01')


def probe(path):
    """ffprobe で秒・寸法・fps・SAR・音声の有無を測る。**札を信じないで測る。**"""
    cmd = ['ffprobe', '-v', 'error', '-print_format', 'json',
           '-show_streams', '-show_format', str(path)]
    d = json.loads(subprocess.run(cmd, capture_output=True, text=True,
                                  check=True).stdout)
    vs = [s for s in d['streams'] if s['codec_type'] == 'video'][0]
    has_a = any(s['codec_type'] == 'audio' for s in d['streams'])
    num, den = (vs.get('r_frame_rate') or '0/1').split('/')
    fps = round(float(num) / float(den), 3) if float(den) else 0.0
    return dict(sec=round(float(d['format']['duration']), 3),
                w=int(vs['width']), h=int(vs['height']), fps=fps,
                sar=vs.get('sample_aspect_ratio') or '1:1', has_audio=has_a)


def main():
    check = '--check' in sys.argv
    src = json.loads((VID / 'sources.json').read_text(encoding='utf-8'))
    clips, bad = {}, []
    for key in sorted(src):
        f = VID / f'{key}.webm'
        if not f.exists():
            bad.append(f'{key}: {f} が無い')
            continue
        m = probe(f)
        if m['sar'] not in ('1:1', '0:1'):
            bad.append(f'{key}: SAR が {m["sar"]}（②は9本とも 1:1 と実測している）')
        dw = DISPW[key]
        if dw > m['w']:
            bad.append(f'{key}: dispw {dw} が器の幅 {m["w"]} を超えている')
        clips[key] = dict(
            url=src[key]['url'], sec=m['sec'], w=m['w'], h=m['h'], fps=m['fps'],
            date=DATE[key], credit=CREDIT[key], note=NOTE[key],
            stream=True, sar='1:1', dispw=dw, has_audio=m['has_audio'],
            local=f'ref/ep8/vid/{key}.webm')
        print(f'  {key:<9} {m["w"]}x{m["h"]} 絵の幅 {dw:>4}  {m["sec"]:>8.1f}秒  '
              f'{m["fps"]:>6}fps  音声{"あり" if m["has_audio"] else "なし"}')
    if bad:
        print('\n🔴 ' + '\n🔴 '.join(bad))
        return 1

    shots = json.loads(SRC_SHOTS.read_text(encoding='utf-8'))
    n_sh = sum(len(v['shots']) for v in shots.values())
    # 🔴 ショット表の `src` は「guncam.webm」。`footage.SHOTS` の鍵はクリップ名なので合わせる
    for k, v in shots.items():
        v['src'] = f'{k}.webm'
    miss = [k for k in clips if k not in shots]
    if miss:
        print(f'\n🔴 ショット表に無いクリップ: {miss}')
        return 1
    print(f'\nショット {n_sh} 本 ／ クリップ {len(clips)} 本')
    if check:
        print('（--check なので書き出していない）')
        return 0
    OUT_CLIPS.write_text(json.dumps(clips, ensure_ascii=False, indent=1),
                         encoding='utf-8')
    OUT_SHOTS.write_text(json.dumps(shots, ensure_ascii=False, indent=1),
                         encoding='utf-8')
    print(f'✓ {OUT_CLIPS.relative_to(HERE)} と {OUT_SHOTS.relative_to(HERE)} を書いた')
    return 0


if __name__ == '__main__':
    sys.exit(main())
