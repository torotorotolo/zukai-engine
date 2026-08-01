# カットの「画」の書き方

`tools/cuts/<章>.py` の `SPEC` に、カットIDごとの dict を書く。
図の型は `tools/titan_fig.py`、置き場所の定数は `tools/jiko_style.py`。

---

## 0. 守ること（これを外すと作り直しになる）

0. 🔴 **チャンネル名・ハンドル・アイコン・ロゴを映像に出さない**（2026-08-01 カズヤくん指示）。
   透かし・隅のロゴ・エンドカードの「チャンネル登録」も置かない。
   **理由：名前とアイコンをあとから変えられるようにしておくため。**
   一度でも焼き込むと、改名したときに過去の全動画が古い名前を出し続けることになる。
   → 画面に出してよいのは **見出し・副題・章マーカー・図・出典・字幕**だけ。
   （2026-08-01 時点で違反はゼロ。`thumb_jiko.py` のサムネにも入っていない。）
1. **ナレーションの文を図にそのまま書かない。**
   図が持つのは**数値・部位名・関係・出どころ**。文はナレーションと字幕が持っている。
   同じ文が「音・字幕・図」で三重になると、画面が読むものだらけになって何も残らない。
2. **引用カットは言葉でなく出どころを図にする。**
   `quote()` は「誰が・誰に・いつ・どこに書かれていたか」を左の札に置き、
   右には**短い決め所だけ**（20字以内）を出す。長い引用文を貼らない。
3. **見出し（`t`）は22字まで。** Dela 62px で 1,364px。副題（`s`）は40字まで。
4. **段の数はナレーションの行数に合わせる**のが既定。
   行より多い段は行の間に挟まれ、少ない場合は最後の段が長く描かれる。
   `python tools/dump_script.py c3` で行数が出る。
5. **級数と余白を推定で置かない。** 型の中は `fontmetrics` で実測して収めてある。
   自分で `J.label()` を直接書くときは、必ず `check_layout.py` を通す。
6. **写真は8枚しか無い。** 割り当ては下記の12カットだけ。
   `titan_hull_pair.jpg` は出所が台帳に無いので**使わない**（使うとエラーで止まる）。

---

## 1. 1カットの書き方

```python
"c103": dict(
    t="乗っていたのは42人",                    # 見出し（必須・22字まで）
    s="ポーラープリンス　2023年6月18日",        # 副題（省略可・40字まで）
    fig=("breakdown", dict(total=42, parts=[...])),
),
```

実写カット：

```python
"pr01": dict(
    t="北大西洋、水深3,346メートル",
    s="潜水艇タイタン　2023年6月18日",
    photo="titan_rov_aft.jpg",
    bias=0.52,          # 縦の寄せ 0=上 0.5=中央 1=下
    side="right",       # 注記を出す側。写真の主題と反対側にする
    ann_y=356,          # 注記の始まり y
    ann=[dict(t="最後の記録", v="10:47:08", vc=J.INK_W, vs=104)],
),
```

`ann` は **4〜6ブロックまで**。`t`＝見出し／`v`＝数値（Dela）／`d`＝補足。
`ts` `vs` `ds` で級数の上限、`c` `vc` `dc` で色を指定できる（省略時は自動で収まる）。

### ★写真を「地」に敷いて、その上に図解を重ねるカット（2026-08-01 追加）

`photo` と `fig` を**両方**書くと、写真が地になり、暗幕を挟んで図が上に乗る。
（`photo` だけなら実写カット、`fig` だけなら図解カット、という従来の動きは変わらない。）

```python
"c115a": dict(t="6秒後、位置が自動で送られた", s="緯度経度つきの最後の記録",
              fig=("timeline", dict(...)),      # ← 図はそのまま
              photo="titan_rov_aft.jpg",        # ← 地に敷く写真
              veil=0.84,                        # ← 暗幕の濃さ（省略時 0.84）
              bias=0.40, xbias=0.95, zoom=1.30) # ← 切り方
```

**割り当ては章ファイルではなく `tools/cuts/__init__.py` の `BACKDROP` に書く**
（章をまたぐ編集判断なので1か所にまとめる。消せば図だけに戻る）。

🔴 守ること
1. **全カットに敷かない。** 敷いた瞬間に「図解チャンネル」である意味が消える。
   競合との差は図があることなので、退屈になりやすいカットだけに絞る。
2. **その写真が、そのカットで話している対象そのものであること。**
   時刻の札の後ろに関係のない残骸を壁紙として敷くのはやらない
   （写真がその場面を写しているかのように読めてしまう）。
3. **出典は必ず出る**（`fig_base(ground=False)` が右上に出す）。消さない。
4. 全画面に耐える写真は**6枚だけ**（実測）。`rov_aft` `rov_tailcone` `titanic_bow`
   `cf_evidence` `hull_pair` `hull_inner`。ほかは 16:9 に切ると2倍に拡大されて眠くなる。
5. **ROV写真（rov_aft / rov_tailcone）は `zoom=1.30, xbias=0.95, bias≦0.45` が必須。**
   左上に "Depth (m): 3774.9"、左下に日付、下中央に HDG/Alt が焼き込まれている。
   実写カットでは出所の証拠として残すが、地に敷くと図の数字と別の数字が並ぶ。

```bash
python tools/check_veil.py                       # 暗幕の濃さを机上で測る
python tools/build_jiko.py veil --cuts=c115a     # 濃さ違いを1回で焼き並べる
```

---

## 2. 図の型（`titan_fig.py`）

| 型 | 何の図か | 主な引数 |
|---|---|---|
| `depth` | 海面から下へ伸びる深度目盛り。**いちばん多く使う** | `marks=[dict(d=3346,t="爆縮",c=J.ALERT,big=True,sub="10:47:09",hot=True)]`, `dmax=4400`, `seabed=3840`, `note` |
| `compare` | 2〜4個の数値を棒の長さで比べる | `items=[dict(v=13200,t="計算値",c=,disp="13,200",unit="m",sub="")]`, `ratio="およそ80%"`, `note` |
| `quote` | 引用の**出どころ**＋短い決め所 | `phrase`（20字以内）, `who`, `to`, `when`, `doc`, `ctx` |
| `timeline` | 横の時間軸に出来事を打つ | `events=[dict(t=647,top="10:47",t2="重り2つ",c=,big=True)]`, `t0`, `t1`, `ticks=[(v,"表示")]`, `band=[dict(a=,b=,t=,c=)]` |
| `moment` | 大きな時刻＋その時の事実（第1章の骨） | `clock="05:15"`, `label`, `facts=[dict(t="",v="",c=)]`, `day=5.25`, `dayspan=(4,20)`, `sub` |
| `breakdown` | 全体を内訳に分ける積み上げ棒 | `total=42`, `parts=[dict(v=17,t="船の乗組員",c=)]`, `unit="人"`, `note` |
| `graph` | XY 折れ線。**左から描かれる** | `series=[dict(pts=[(x,y)],t="",c=,dash="14 10",sw=6,dot=True)]`, `xr`, `yr`, `xticks`, `yticks`, `band`, `marks=[dict(x=,y=,t=,c=)]`, `xlab`, `ylab`, `note` |
| `dives` | 潜航番号×到達深度の棒 | `items=[dict(n=81,d=3840,c=,nt="81",t="",hot=True)]`, `dmax=4200`, `note` |
| `layers` | 積層断面（5層＋接着面4つ） | `n=5`, `bonds=[dict(i=1,t="1-2",c=)]`, `delam=[1,3]`, `voids=[1,3]`, `dims=[dict(a=.1,b=.5,t="0.6インチ")]`, `note` |
| `titan` | 潜水艇の側面／縦断面 | `mode="side"\|"section"`, `s=1.0`, `marks=[dict(at="cyl"\|"fore"\|"aft"\|"ring"\|"ring2"\|"win"\|"cylb", t="", v="", c=, up=True)]`, `window=True`, `bolts=True`, `note` |
| `process` | N 段の工程を左から右へ | `steps=[dict(t="巻く",d="1インチぶん",v="×5",c=)]`, `note` |
| `panel` | 構造のある文字パネル（結論・箇条） | `blocks=[dict(k="1",t="…",v="",c=)]`, `lead`, `note`, `cols=3` |
| `absent` | 「無い」ことを見せる（破線＋×） | `items=[dict(t="船級",d="受けていない",ok=False)]`, `lead`, `note` |
| `icons` | 個数を絵で見せる | `n=9`, `on=[0,1]` or `on=5`, `kind="dot"\|"person"\|"ship"\|"sub"`, `cols`, `lead`, `note`, `labels=[]` |
| `sound` | 2点で同じ音を聞いた | `rings=4`, `both=True`, `label_a`, `label_b`, `note` |
| `gauge` | 監視装置のしきい値（黄30・赤50） | `hits=12`, `yellow=30`, `red=50`, `vmax=60`, `lead`, `marks=["…"]`, `note` |
| `mapfig` | 位置関係（Google Maps は使えないので自作） | `points=[dict(x=0.2,y=0.3,t="",d="",c=,kind="wreck")]`, `link=(0,1)`, `scale="約 600 km"`, `lead`, `note` |
| `people` | 人と組織のあいだで起きたこと | `nodes=[dict(x=.2,y=.3,t="海洋運用部長",d="",c=)]`, `edges=[dict(a=0,b=1,t="1月19日 会話",c=)]`, `lead`, `note` |
| `beforeafter` | 前と後の2枚 | `a=dict(k="変更前",t="",lines=[],v="",c=)`, `b=...`, `lead`, `note` |
| `buckle` | 圧縮での壊れ方 | `kind="crush"\|"global"\|"local"\|"peel"\|"s"`, `lead`, `note` |
| `window` | のぞき窓の断面（中央が厚く縁が薄い） | `marks=["…"]`, `lead`, `note` |

色は `import jiko_style as J` で
`J.LINE`（技術線・既定）／`J.INK_W`（主図形）／`J.ALERT`（破壊・欠陥・赤）／
`J.AMBER`（数値）／`J.OK`（接着・正常・緑）／`J.LINE_DIM`（沈める）。

---

## 3. 実写カットの割り当て（この12カットだけ）

| カット | 写真 | 何を見せるか |
|---|---|---|
| `pr01` | `titan_rov_aft.jpg` | 海底の残骸（掴み） |
| `pr03` | `titan_cf_evidence.jpg` | 回収された炭素繊維の破片 |
| `pr09` | `titan_hull_edge.jpg` | 積層が刃のように裂けた破断面 |
| `c129` | `titan_rov_tailcone.jpg` | 海底の尾部。深度の焼き込みが証拠 |
| `c133` | `titan_rov_aft.jpg` | 別の寄り |
| `c201` | `titan_titanic_bow.jpg` | タイタニックの船首（深さの実感） |
| `c307` | `titan_delam_ruler.jpg` | 層間剥離の接写（定規つき） |
| `c422` | `titan_hull_inner.jpg` | 耐圧殻の内面。白い部分が繊維の破断 |
| `c429` | `titan_hull_edge.jpg` | 積層としわが見える破断面 |
| `c624` | `titan_rov_aft.jpg` | 残骸の状態 |
| `c627` | `titan_delam_ruler.jpg` | 擦れて平らになった接着面 |
| `ep07` | `titan_cf_evidence.jpg` | 証拠として並んだ破片 |

同じ写真を使い回すときは `bias` と `side` を変えて**寄りを変える**。

---

## 4. 書いたら必ず通す

```bash
python tools/dump_script.py c3          # 台本の行と尺（図の入力）
python -c "import sys;sys.path.insert(0,'tools');import cuts"   # 構文
python tools/check_layout.py --only=c3  # 画面外・重なり・豆腐を機械で見る
```

`check_layout` が「✓ 机上の検算はすべて通った」を出すまで直す。
**そのあとクラウドで焼いて拡大目視する**（この道具は目視の代わりではない）。
