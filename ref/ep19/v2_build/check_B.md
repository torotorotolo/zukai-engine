# 19本目 台本 第1版 照合 係B（前半 × GJ・MC18・MIN18・EST18）

- 照合した日＝2026-10-06（④'）。台本＝`ref/ep19/daihon_v1.md`（読むだけ・書き換えていない）
- 原文＝通し頁 `ref/ep19/src/ep19_pages.txt`（GJ は p98xx の書き起こしを優先）。人の名前は書かない
- 画像は1枚も開いていない。ただし c406 の確かめのため、GJ の PDF p.20〜21 を 220dpi で scratchpad（このチャット）に PNG へ書き出し、`tools/ocr_win.ps1`（Windows の OCR）に通して**文字だけ**読んだ
  - 結果（PDF p.20 の29〜30行目）：`…it appears the building is in very good shape?" Assuming the Board minutes / accurately reflect the Building Official's comment* notwithstanding his opinion and comments'`
  - 通し頁 p3020 の OCR はこの `Assuming` を落としている（`" the Board minutes acctll ately reflect …` と小文字の the で始まる）＝通し頁の側も直すとよい
- 確かめたカット＝40（c103・c106・c201・c203・c210〜c213・c301・c308〜c319・c401〜c419）
- 結果＝🔴2・🟡4・🟢13

## カットごと

c103 ずれ🟢 GJ p.1 p9801（`12-story 136-unit`・`98 known persons`）・TR0003・TR0060＝数は合う。語尾「亡くなりました」だけがです・ます調（台本の中でここ1か所）
c106 OK MC18 p.7 p9804（`major structural damage to the concrete structural slab below these areas`）。3行目「点検では見えない所」は §0 の④'項目1（係Aの範囲）
c201 OK TR0053・TR0005（Miami-Dade County の町・since 1981）・GJ p.1（12-story）
c203 ずれ🟢 大陪審の説明は GJ p.39（PDF p.42＝p3042 謝辞 `21 citizens … were selected as the 2021 Spring Term of the Miami-Dade County Grand Jury`・刑事の事件を扱った・州検事の頼みで崩落の調べを引き受けた）と GJ p.1（関わった人や役人の policies, procedures… を見る）の範囲で言える。出典欄に GJ p.39 が無い
c210 ずれ🟢 AC p.23（1979-1981 Design & Construction）OK。GJ p.2 p3005：`structurally sound and electrically safe`・`40 years old or older, and then, every ten years thereafter` OK。行う人は `licensed engineer or architect`＝「技術者が」だと建築士が落ちる
c211 OK GJ p.2 p9810（requirement … followed another tragic event・1974-08-05・7 DEA employees・rooftop parking lot caved in・1925年の建物＝49年）。★は「崩落の後」＝followed で言いすぎなし
c212 OK MIN18 p.7 p9805（due in 2021）・GJ p.18 p9802（the condo board hired an engineer to start the 40-year recertification process years before it was due）。雇ったのは原文では condo board（理事会）。転送メール p4104 では報告の宛先は Association＝「管理組合」で誤りではない
c213 OK MC18 p.7（橋の行）
c301 ずれ🟢 TR0441 p1441＝前置きが `corrosion of steel reinforcement of the pool deck slabs`。「鉄筋の錆は」だとプールデッキの限定が落ちる。1996〜97年の補修と防水は OK
c308 ずれ🟢 TR0442・TR0443 OK。2行目「2018年、40年の点検の準備で、技術者が調べた」の出典（GJ p.18・MC18 p.1）が出典欄に無い
c309 ずれ🟢 日付 2018-10-08・会計係（Treasurer）に渡した＝GJ p.17 p3020・MC18 p.1 p4001 OK。報告の範囲は屋上・外の壁・バルコニー・部屋の約68戸も含む（MC18 p.1）＝3つだけ挙げると狭く聞こえる（c316 の画に「外の壁」が出る）
c310 OK MC18 p.7 p9804（beyond it useful life … must all be completely removed and replaced）
c311 OK MC18 p.7 p9804 ★。メモ：failed waterproofing を「破れ」と言うのは少し狭い（効かなくなった防水）が、★と §2 の表の作り直しの手間に見合わないので指摘にしない
c312 OK MC18 p.7 p9804（Failure to replace the waterproofing in the near future will cause … to expand exponentially）
c313 OK MC18 p.7 p4007（main issue … laid on a flat structure・water sits … until it evaporates・major error in the development of the original contract documents）
c314 ずれ🟢 MC18 p.7 p4007：直し方は敷石・砂の層に加え topping slab と防水まで鉄筋コンクリートの構造まではがし、`repairing the concrete structure as deemed necessary`。台本は「床を直す」が落ち、はがす範囲も「敷石や砂」だけ。「高くつき…乱す」は (b) の `extremely expensive … major disturbance to the occupants` で OK
c315 ずれ🟡 MC18 p.7 p4007：`Though some of this damage is minor, most of the concrete deterioration needs to be repaired in a timely fashion`＝「多くは」の限定が落ちている。ひびと剥がれ（柱・梁・壁）・むき出しの鉄筋は OK
c316 OK EST18 p4318：合計 $9,128,433.60（7項目の足し算で一致）→約913万ドル。Garage, Entrance and Pool Deck $3,825,217.60→約383万ドル。Façade $3,191,312→約319万ドル。見積もりは報告に添付（MC18 p.1 `an estimate (that is attached to this report)`）
c317 OK MC18 p.1〜9 に collapse・imminent・unsafe・danger は0件（-g で確かめた）。legend L02 と同じ
c318 OK TR0441・MC18 p.7（exposed, deteriorating rebar）
c319 ずれ🔴 「報告が出てから、崩れるまでの29か月」＝GJ p.18 の29か月は報告（2018-10）から2021年4月まで。報告から崩落（2021-06-24）までは約2年8か月半（約32か月）
c401 ずれ🟢 語りは OK（GJ p.17 a month later・MIN18 p.7 の presented … to discuss 40 year certification＝招かれた・then Building Official＝当時の）。画の「29か月」の帯が 2021-06-24 まで伸びるなら誤り（帯は2021年4月で止める）
c402 OK GJ p.17 p3020（as early as October 8, 2018 … was aware of significant necessary repairs and maintenance）＝「遅くとも…には」で合う
c403 OK MIN18 p.7 p9805（although report was not in the format for the 40 year certification he determined the necessary data was collected）
c404 OK MIN18 p.7 p9805 ★（it appears the building is in very good shape）
c405 OK MIN18 p.7 p4107（Process and timeline … The permit process, balcony railings, concrete restoration, and waterproofing was discussed）
c406 ずれ🔴 GJ p.17 p3020 の文は `Assuming the Board minutes accurately reflect the Building Official's comments, notwithstanding …, the … Report clearly reveals …`（再OCR）。台本「議事録は、担当者の言葉を正しく記録している」は条件節の前提を大陪審の断定にした（意味のずれ①）。2行目は p3021 `clearly reveals that there were significant problems with the integrity of the building structure` で OK
c407 ずれ🟡 GJ p.18 p9802：`Champlain Towers owners failed to implement routine repairs and maintenance`＝誰がしなかったか（持ち主たち）が落ち、責任の語が弱い（意味のずれ②）。suggests＝「読んでいる」は OK
c408 ずれ🟡 GJ p.18 p9802：`The proposed costs for building repairs were more than $14,000,000`＝見積もりの額。「費用は…超えていた」だと実際にかかった額に聞こえる。換算は 1,400万×109円＝15.26億円→約15億円・÷136＝1,122万円→約1,100万円 で OK（いつの額かは GJ に無い＝2021年4月のレートは台本の仮定）
c409 ずれ🟢 語りは GJ p.18 p9802（more than 29 months after the engineer's report was received・had not begun any repair work）で OK。画の帯の起点「2018年11月」は原文に無い（語りは「報告から」）
c410 OK GJ p.18 p9802（nor had the City taken any steps to address those structural deficiencies or the safety of the building）＝2021年4月の時点の文。範囲を超えていない
c411 OK GJ p.18 p3021（the April 2021 letter from the then Board President to the condo owners）
c412 ずれ🟢 GJ p.18 p3021：1行目 `observable damage such as in the garage has gotten significantly worse since the initial inspection` OK。2行目 `the concrete damage observed would begin to multiply exponentially over the years` に「これから」は無い（2018年の報告の見立てを手紙が引いた可能性もある）
c413 ずれ🟢 GJ p.18 p3021（we must pull up almost the entire ground level of the lot … pool deck, the entire entry drive and ground level parking …）。「駐車場」は原文では ground level parking＝地上の駐車場（台本は地上／地下を分けて言っている）
c414 OK GJ p.18 p3021・p9802 ★（spalling (cracking) … rebar … rusting and deteriorating beneath the surface・The concrete deterioration is accelerating）
c415 OK GJ p.18 p9802（the Board was to hold a meeting to open the bids received from companies interested in making the repairs）
c416 OK GJ p.18 p9802 ★（Thirteen days after … was to hold … the building collapsed）
c417 ずれ🟢 「同じ年の会議」を知らせに数えているが、その会議の議事録は「とても良い状態に見える」（c404）。GJ の `put everyone on notice` の中身は報告そのもの
c418 ずれ🟢 GJ p.1 p3004 の題は `THE SURFSIDE CONDO COLLAPSE TRAGEDY: RECOMMENDATIONS TO MAKE BUILDINGS SAFER`＝台本は後半だけを「題は」と言う。2行目は p.1 の policies, procedures, protocols, systems and practices で OK
c419 ずれ🟡 「29か月のあいだ」→「最後の3週間」＝29か月は2021年4月で終わる（GJ p.18）。最後の3週間（6月）はその外（意味のずれ③）。NIST の合図は TR0107（timeline of structural distress starting approximately three weeks before the collapse）で OK
