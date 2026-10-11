# 21本目（9.11 のリメイク）旧版の主張113行の当て直し ── 一次資料の原文で照合

- 作成：2026-10-11（21本目 ①棚卸しの「照合の係」・サブエージェント）。主張の表＝[old_script_inventory.md](old_script_inventory.md) §8（K001〜K113）。113行の字が公開版の語り（`be3dc65:tools/narration.py` の SCRIPT・202カット454行）と一致することを機械で確かめてから当てた（食い違い0件）
- 照合の元（すべて読むだけ）：
  - **委員会報告**＝`analytics/materials/ep7/GPO-911REPORT.pdf`（政府印刷局版・585頁）。PyMuPDF で頁ごとに文字の層を取り直し、**NFKC＋引用符と合字の正規化＋空白を全部潰す＋行末ハイフンを「消す／残す」の2通り**で検索した（道具＝`src/claims_raw/kchk.py`）。陽性対照5件（“The plane took off at 7:59”→p4 など）は全部当たり、陰性対照は0件
  - **NIST**＝`analytics/materials/ep7/nist/ncstar1.pdf`・`ncstar1-6v1.pdf`（文字の層は OCR 並み＝「detemiine」「comers」などの誤字がある）
  - **NTSB 飛行経路の研究**（4機）＝文字の層0。②で作った OCR の文字（`analytics/materials/ep7/s2/ocr/*.ocr.txt`・300dpi・Windows OCR）を読んだ。**数字だけ取り、画像は見ていない**
  - 旧版の台本第2版（Vault `Projects/事故検証-9.11-台本第2版-20260913.md`）の §9・§10・§12 は**参考に並べただけ**（旧版の「照合ずみ」は引き写していない）
- **頁の書き方**：委員会報告は **p7（PDF p25）**＝印字の頁と PDF の頁。本文（PDF p19〜585）は **PDF＝印字＋18** で全頁一定（頁ごとの数字の行から機械で確かめた＝551頁で一定）。旧版は走りヘッダからの内挿（±1頁）だったので、**旧版の頁と違う所はメモに書いた**。注は「第1章 注42 p454（PDF p472）」の形。NIST は「NCSTAR 1 p84（PDF p134）」、NTSB は「NTSB 77便 PDF p2」
- 引用は文字の層のまま（空白の欠け「flight.The」は1つ空けた）。**私人（乗客・乗員・ご遺族）と乗っ取った側の個人名は引用の中でも [ ] で役割に置き換えた**
- 時刻は「8:46:40」の形。換算・引き算は「計算」と書いた

## 判定の決め方

| 判定 | 意味 |
|---|---|
| **一致** | 数・時刻・主語・因果が原文と合う（言い換えの範囲）。細かい注はメモに。「一致（推論）」＝原文の数から言えるが、その文自体は無い |
| **言いすぎ** | 原文の限定（about／approximately／probably／may have／we believe／推定）が落ちた・一般化・断定・因果を足した。（軽い）＝言葉を足せば直る |
| **ずれ** | 数・時刻・秒・主語・順番・場所・中身が原文と違う。（軽い）＝1分・言い方の範囲 |
| **見つからない** | 一次資料に当たる記述が無い（探した語と範囲をメモに） |
| **一次資料の外** | 一次資料が扱っていない（いま＝2026年の話・報道） |

1行に所見が複数あるときは、**直す必要の一番大きいものを主の判定**にし、残りはメモに書いた。

---

## 0. 数え（主の判定・113行）

（§1 の表から機械で数え直した＝`src/claims_raw/count_check.py`）

| 判定 | 件数 | ID |
|---|---|---|
| 一致 | **85** | K001 K002 K003 K004 K007 K008 K009 K010 K011 K012 K013 K014 K015 K016 K017 K018 K019 K020 K021 K022 K024 K026 K028 K029 K030 K032 K033 K034 K036 K037 K038 K039 K040 K041 K042 K043 K044 K046 K049 K051 K052（推論） K054 K055 K056 K058 K060 K062 K063 K064 K065 K066 K068 K071 K075 K076 K077 K079 K080 K081 K082 K083 K084 K086 K087 K088 K089 K090 K091 K093 K094 K095 K096 K097 K098 K099 K100 K101 K102 K103 K104 K106 K107 K108 K109 K113 |
| 言いすぎ | **18** | K005（軽い） K006（軽い） K025 K031 K035（軽い） K050（軽い） K053 K057 K059（軽い） K061（軽い） K067（軽い） K069（軽い） K072（軽い） K073 K078（軽い） K085（軽い） K092（軽い） K105（軽い） |
| ずれ | **5** | K023 K027（軽い） K045 K048 K074（軽い） |
| 見つからない | **2** | K047 K070 |
| 一次資料の外 | **3** | K110 K111 K112 |

- 言いすぎ18件のうち（軽い）＝13件、ずれ5件のうち（軽い）＝2件
- **一致でも出典の頁が旧版と違う行**：K002（注1・p245）・K008（NIST 表紙／第9章 注30）・K012・K035・K036・K046（p277→**p278**）・K016（p84→**p2**＋p84）・K030（p5→＋**p85**）・K042（＋**注42**）・K052（p25→**p29**）・K058（p26→**p25**・p1）・K065（p26→**p34**・p27）・K099（p42・p43→**p44**）・K101（p279→**p280**）・K102（＋注168・注120）・K103（＋**注76**）・K106・K107（NIST の頁）
- **時刻が資料で割れるもの**＝§3-1 の表（語りはすべて**委員会報告の本文の値**。例外は93便への警告＝注79 側の 9:24）

---

## 1. 照合の表（113行）

| ID | カット | 主張（短く） | 判定 | 原文（短い引用） | 資料と頁 | メモ（④への注・旧版の出典との差） |
|---|---|---|---|---|---|---|
| K001 | pr01 | 2001-09-11（火）東部はよく晴れた朝・4機が続けざまに乗っ取られた | 一致 | “Tuesday, September 11, 2001, dawned temperate and nearly cloudless in the eastern United States.” | 委員会 p1（PDF p19）／p4（PDF p22） | 4機＝p4 “The 19 men were aboard four transcontinental flights.” 乗っ取りは 8:14ごろ・8:42〜8:46・8:51〜8:54・9:28（p4・p7・p8・p11） |
| K002 | pr02 | 4機とも東海岸→西海岸の長い路線・長い路線ほど燃料を多く積む・そこが狙われた | 一致 | “they simply booked heavily fueled east-to-west transcontinental flights of the large Boeing aircraft they trained to fly” | 第1章 注1 p451（PDF p469）／p4（PDF p22）／p245（PDF p263） | 旧版の p4・p7・p8・p10 は路線だけで「狙った理由」が無い→**注1** を出典に。p245 は実行役の1人が共謀者に「長距離便は燃料が多いので選びたい」と語った（取り調べに基づく又聞き）。「長い路線ほど多く積む」という一般則の文は無い |
| K003 | pr04 | 軍が1機目の乗っ取りを知らされたのは、ぶつかる9分前 | 一致 | “NEADS received notice of the hijacking nine minutes before it struck the North Tower.” | p21（PDF p39） | 主語は NEADS（北東航空防衛セクター）。実差は 8:37:52→8:46:40＝8分48秒（計算）。“the most the military would receive of any of the four hijackings” |
| K004 | pr04★ | 残り3機は墜ちるまで知らされていない・猶予は9分、そのあとは0分 | 一致 | “nine minutes' notice on the first hijacked plane, no advance notice on the second, no advance notice on the third, and no advance notice on the fourth.” | p31（PDF p49）／p34（PDF p52） | 「0分」は “no advance notice” の言い換え。77便は 9:34「見失った」、9:36「正体不明機がホワイトハウスの南西6マイル」と伝わった（p27・p34）＝乗っ取りとしての知らせではない |
| K005 | pr05 | 検査で探していたのは主に爆弾と拳銃 | 言いすぎ（軽い） | “The screening was in place to identify and confiscate weapons and other items prohibited from being carried onto a commercial flight.” | p2（PDF p20）／p84（PDF p102） | 「主に爆弾と拳銃」という文は無い（台本のまとめ）。原文＝探知機は「.22口径の拳銃ぶんの金属」に合わせた（p2）、当時の主な脅威は自爆でない爆破と見られていた（p84 “nonsuicide sabotage was the primary threat”）。旧版の p84 の文は「何を探していたか」を直接は言っていない |
| K006 | pr06 | ハイジャックは要求をのんで着陸させるもの・乗員も管制も何十年もそう訓練・犯人と戦うことは手引きのどこにも無い | 言いすぎ（軽い） | “It taught flight crews that the best way to deal with hijackers was to accommodate their demands, get the plane to land safely” | p85（PDF p103） | 共通戦略が教えたのは**乗員**（flight crews）。管制は「FAA と NORAD の手順が伝統的な形の乗っ取りを前提にしていた」（p18）で、「そう訓練された」とは書いていない。「戦うことは書かれていない」の原文は “FAA training material provided no guidance for flight crews should violence occur.”（暴力が起きたときの指針が無い） |
| K007 | pr07 | 米国の独立調査委員会が2004年に出した | 一致 | “We have sought to be independent, impartial, thorough, and nonpartisan.” | p.xv（PDF p15） | 設置＝“Public Law 107-306, November 27, 2002”（p.xv）。**刊行年 2004 は文字の層の前付けに無い**（注の日付が2004年7月まで＝推論）→§4 #10 |
| K008 | pr08 | 建物がなぜ崩れたかは別の役所が別に調べている | 一致 | “Final Report on the Collapse of the World Trade Center Towers” | NIST NCSTAR 1 表紙（PDF p1・p3）／委員会 第9章 注30 p543（PDF p561）・p316（PDF p334） | 旧版の「§4 p1」に該当文は無い。委員会報告は NIST の調査（“Federal Building Fire Safety Investigation of the World Trade Center”・注30）を引くだけで、崩壊の原因は扱っていない |
| K009 | pr10 | その朝、自国の空をいったん全部閉じた・飛んでいた機すべてに最寄りの空港へ降りろと命じた | 一致 | “ordered all FAA facilities to instruct all aircraft to land at the nearest airport.” | p29（PDF p47）／p327（PDF p345） | 「閉じた」は p327 “On the morning of September 13, the national airspace reopened”（再開）からも言える |
| K010 | pr11 | 2,973人が亡くなった・自国の土地で受けた攻撃で最多・乗っ取った19人は入っていない | 一致 | “the nation suffered the largest loss of life—2,973—on its soil as a result of hostile attack in its history.” | p311（PDF p329）／第9章 注188 p552（PDF p570） | 注188＝WTC 2,749＋ペンタゴン 184＋93便 40、いずれも “nonterrorists”。数は **2004年7月9日時点**（注188）＝§3-2 |
| K011 | c101 | 時刻はすべて米国東部時間 | 一致 | “All times are Eastern Daylight Time.” | 第10章 注1 p554（PDF p572）／第1章 注121 p459（PDF p477） | 第1章には「全部東部時間」の一文は無い（第10章の注と第1章の注の “EDT” から）。東部**夏時間** |
| K012 | c103 | 7棟と地下の商店街をまとめて世界貿易センター | 一致 | “The WTC actually consisted of seven buildings, including one hotel, spread across 16 acres of land. The buildings were connected by an underground mall (the concourse).” | p278（PDF p296） | 旧版 p278 で可 |
| K013 | c104 | 出発地は3か所（ボストン・ワシントン・ニューアーク）・行き先は LA と SF | 一致 | “United Airlines Flight 93 took off from Newark (New Jersey) Liberty International Airport bound for San Francisco.” | p2〜p4（PDF p20〜22）・p7〜p10（PDF p25〜28）・図表 p32〜33（PDF p50〜51） | ⚠️ **報告書の中で割れる**：p4 は93便を “going to Los Angeles”、p10・図表 p33 は San Francisco＝語りは p10 側。ワシントン＝ダレス空港（バージニア州） |
| K014 | c108・c109 | 11便・175便は767、77便・93便は757 | 一致 | “piloted the Boeing 767”（p4）／“The aircraft was a Boeing 757”（p8） | p4（PDF p22）・p7（PDF p25）・p8（PDF p26）・p10（PDF p28） | 通路2本／1本は 第1章 注43 p454 “Boeing 767 double-aisled aircraft”・“Boeing 757 single-aisle aircraft” |
| K015 | c110 | 175便と93便は客が少なかった・93便は182席に37人、175便は168席に56人 | 一致 | “Flights 175 and 93 were well below their averages.” | 第1章 注21 p452（PDF p470）・注40 p454（PDF p472）・注72 p456（PDF p474） | 注40 “a load factor of 33.33 percent of the airplane's seating capacity of 168”、注72 “20.33 percent of the plane's seating capacity of 182”。人数は乗っ取った側を含む（p11 “33 in addition to the 4 hijackers”） |
| K016 | c111・c112 | 金属探知機とX線・小型の拳銃ぶんで鳴る・鳴った人だけ棒で再検査 | 一致 | “a walk-through metal detector calibrated to detect items with at least the metal content of a .22-caliber handgun.” | p2（PDF p20）／p84（PDF p102） | 旧版は p84 だけ→探知機の設定と棒（hand wand）は **p2**。「鳴った人だけ」は p84 “secondary screening ... was nonexistent, except for passengers who triggered the metal detectors.” |
| K017 | c113・c904 | 刃渡り10cm（4インチ）未満は持ち込めた・航空会社の手引きがはっきり認めていた／いまは持ち込めない | 一致 | “While FAA rules did not expressly prohibit knives with blades under 4 inches long, the airlines' checkpoint operations guide ... explicitly permitted them.” | p84（PDF p102） | 手引きは “developed in cooperation with the FAA”。c904 の「いまは持ち込めない」は一次資料の外（報告書は2004年まで） |
| K018 | c114★ | 武装した保安要員はほとんどいない・連邦航空保安官は全米で33人・国内線には原則いない | 一致 | “there were only 33 armed and trained federal air marshals as of 9/11. They were not deployed on U.S. domestic flights, except when in transit to provide security on international departures.” | p85（PDF p103） | 「原則」＝原文の例外（国際線へ向かう移動中）を受けている |
| K019 | c115 | 7:59 11便がボストンを離陸・乗客81人と乗員11人 | 一致 | “Eighty-one passengers boarded the flight with them (including the five terrorists). The plane took off at 7:59.” | p4（PDF p22） | 乗員＝機長・副操縦士＋客室乗務員9人。81人は乗っ取った5人を含む。⚠️ NTSB（OCR）は離陸を “approximately 8:00 AM”＝§3-1 |
| K020 | c116 | 8:14 175便が同じ空港を離陸・乗客56人と乗員9人 | 一致 | “departed Logan Airport at 8:14.” ／ “Fifty-six passengers boarded the flight.” | p7（PDF p25） | 乗員＝操縦士2＋客室乗務員7。56人は乗っ取った5人を含む。NTSB（OCR）も 8:14 |
| K021 | c117 | 8:20 77便がダレスを離陸・乗客58人と乗員6人・計64人 | 一致 | “took off at 8:20.” ／ “On September 11, the flight carried 58 passengers.” | p8（PDF p26）／p314（PDF p332） | 乗員＝操縦士2＋客室乗務員4。64人＝p314 “All 64 people aboard the airliner”。58人は乗っ取った5人を含む |
| K022 | c118 | 8:42 93便がニューアークを離陸・朝の混雑で離陸は25分あまり遅れた | 一致 | “When it left the ground at 8:42, the flight was running more than 25 minutes late.” | p10（PDF p28）／第1章 注63 p455（PDF p473） | 遅れの理由＝p10 “the airport's typically heavy morning traffic” |
| K023 | c119 | 4機とも燃料を満載・積める量は最大でおよそ43,150L（11,400ガロン） | ずれ | “turn them into large guided missiles, loaded with up to 11,400 gallons of jet fuel.” | p4（PDF p22） | 🔴 原文は「（実際に）最大 11,400 ガロンを**積んでいた**」。語りは「**積める量**（容量）」に変わっている。「満載」も原文に無い（注1 は “heavily fueled”）。換算 11,400 gal≒43,154 L（計算） |
| K024 | c120 | 7:59〜8:42 の43分で4機すべて離陸 | 一致 | “The plane took off at 7:59.”（p4）／“When it left the ground at 8:42”（p10） | p4（PDF p22）・p10（PDF p28） | 43分は計算 |
| K025 | c121 | 名前は共通戦略・交渉して安全に着陸させるのが最優先・1986年からの15年、アメリカ機は1機も乗っ取られていない | 言いすぎ | “no terrorist had hijacked a U.S. commercial aircraft anywhere in the world since 1986.” | p85（PDF p103）／第1章 注91 p457（PDF p475）／p14（PDF p32）・注90 p457 | 🔴 原文は「**テロリストによる**乗っ取りが1986年以来無い」。注91 は “no plane had been hijacked inside the United States since 1991”（＝国内では1991年まであった）。p14 “The most recent hijacking that involved U.S. air traffic controllers, FAA management, and military coordination had occurred in 1993.”（注90＝ルフトハンザ機・JFK）。「交渉」は原文 “accommodate their demands”（要求をのむ） |
| K026 | c122 | 管制官→上司→FAA本部→国防総省→軍の指揮系統→戦闘機 | 一致 | “Controllers would notify their supervisors, who in turn would inform management all the way up to FAA headquarters in Washington.” | p17〜18（PDF p35〜36）／第1章 注102 p458 | 本部の乗っ取り担当→国防総省の NMCC→国防長官室の承認→NORAD の指揮系統（p18）。手順が想定したのは随伴で “The protocols did not contemplate an intercept.”（p18） |
| K027 | c123・c908 | すぐ飛べる戦闘機は全米7か所に2機ずつ・計14機／外から来る敵を止めるための冷戦のころの配置 | ずれ（軽い） | “by 9/11 there were only seven alert sites left in the United States, each with two fighter aircraft on alert.” | p17（PDF p35）／p16（PDF p34） | 14機は計算で可。🔴「冷戦のころの配置」は逆向き：7か所は「冷戦期の最大26か所から**減った残り**」（p16 “reduced from its Cold War high of 26”）。冷戦由来なのは「外からの攻撃に備える」任務の考え方（p16） |
| K028 | c124★ | 国内を飛ぶ旅客機が武器になることは想定に無い・想定の外から始まった | 一致 | “The threat of terrorists hijacking commercial airliners within the United States—and using them as guided missiles—was not recognized by NORAD before 9/11.” | p17（PDF p35） | 主語は NORAD。1990年代末に「航空機を武器に使う」脅威は挙がり演習もあったが「国外から来る」想定（p17）＝言うなら「国内で」を落とさない |
| K029 | c201 | 8:14の少し前、11便は高度約7,900m（26,000ft）・ここまで異常なし | 一致 | “Just before 8:14, it had climbed to 26,000 feet, not quite its initial assigned cruising altitude of 29,000 feet. All communications and flight profile data were normal.” | p4（PDF p22） | NTSB（OCR）も 8:13:29 に 26,000ft 通過 |
| K030 | c202 | 当時も扉は飛行中は閉めて施錠・ただし緊急時にすぐ開けられる造りが求められていた | 一致 | “Prior to 9/11, FAA regulations mandated that cockpit doors permit ready access into and out of the cockpit in the event of an emergency.” | p85（PDF p103）／p5（PDF p23） | 旧版は p5 だけ→後半は **p85**。原文は施錠の決まりについて “This requirement was not always observed or vigorously enforced.” とも書く |
| K031 | c203・c204 | 乗っ取ったのは19人（5・5・5・4）・全員が当日の保安検査を通過・検査係で、あとから彼らを思い出せた人はいない | 言いすぎ | “None of the checkpoint supervisors recalled the hijackers or reported anything suspicious regarding their screening.” | p2（PDF p20）／p3（PDF p21）／p4（PDF p22）／p11（PDF p29） | 19人・5/5/5/4・全員通過は一致。🔴「思い出せた人はいない」はボストンの**監督者**の話（p2）。ダレスは “the screeners recalled nothing out of the ordinary”（p3）、ニューアークは “none recalled anything unusual or suspicious”（p4）＝「変わった点を覚えていない」で、「彼らを思い出せない」ではない |
| K032 | c205・c206 | 8:19 11便の客室乗務員が予約窓口に電話・操縦室が応答しない／電話は長く続いた・座席番号まで落ち着いて伝えた | 一致 | “The emergency call lasted approximately 25 minutes” ／ “At 8:19, [the flight attendant] reported: ‘The cockpit is not answering’” | p5（PDF p23）／p6（PDF p24） | **旧版 §10-3「報告書は25分と書いていない」は誤り**＝p5 に “approximately 25 minutes”。電話は乗っ取りの「約5分後」に始まった（p5）。座席番号＝p6 “passed on some of the seat numbers of those who had gained unauthorized access to the cockpit” |
| K033 | c207・c209・c210 | 8:21 11便のトランスポンダが切られた・管制官がふだん見るのは二次レーダー・一次の点はふだん出さず、出すには設定の切り替えが要る | 一致 | “Controllers at centers rely so heavily on transponder signals that they usually do not display primary radar returns on their radar scopes. But they can change the configuration of their scopes so they can see primary radar returns.” | p18（PDF p36）・p16（PDF p34） | 8:21＝p18 “At 8:21, American 11 turned off its transponder”・図表 p32・第1章 注54 |
| K034 | c211★・c212 | 8:24:38 11便から無線に声「複数の飛行機がある」・担当の管制官は聞き取れず、何か言っているとだけ分かった | 一致 | “American 11: We have some planes. Just stay quiet, and you'll be okay. We are returning to the airport. The controller only heard something unintelligible” | p19（PDF p37）／第1章 注65 p455 | 時刻は p19・注65（8:24:38）、NTSB（OCR）も同じ。訳の注は §3-3 |
| K035 | c214・c215・c218 | 110階建て・事務所は2棟で約97万m²・1辺約63m（208ft）の正方形・火曜の8時台は人がまだ入りきっていない | 言いすぎ（軽い） | “containing 10.4 million square feet of office space. Both towers had 110 stories, were about 1,350 feet high, and were square; each wall measured 208 feet in length.” | p278（PDF p296）／p316（PDF p334） | 旧版の p277 は1頁ずれ（**p278**）。最後の行は原文に無い推論→言うなら p316 “between 16,400 and 18,800 civilians were in the WTC complex as of 8:46 A.M.”（NIST の暫定値）と p278 “up to 50,000 office workers” を並べる。換算（966,190m²・63.4m）は計算。NIST は1辺 “about 210 ft”（NCSTAR 1 p5） |
| K036 | c216 | 高さは約411m・委員会報告は1,350ft・東京タワー333mの1.2倍 | 一致 | “were about 1,350 feet high” | p278（PDF p296） | 旧版の p277 は1頁ずれ。411m は換算。東京タワー333m は一次資料の外（比 1.24 は計算） |
| K037 | c217 | NIST の資料では北棟の屋上まで417m・アンテナの先まで527m | 一致 | “The roof of WTC 1 was 1,368 ft above the Concourse Level, 6 ft taller than WTC 2, and supported a 360 ft tall antenna mast” | NIST NCSTAR 1 p5（PDF p55） | 基準は地面でなく「コンコース階から」。527m は 1,368＋360＝1,728ft の計算（NIST は合計を書いていない）。文字の層は OCR 並み→§4 #6 |
| K038 | c219・c220・c221 | 8:34 ボストンの管制センターが手順を飛ばして自分で軍へ・8:37:52 防空の当直につながる・「訓練ではない」・つながった先は NEADS（ニューヨーク州ローマ） | 一致 | “Boston Center did not follow the protocol in seeking military assistance through the prescribed chain of command.” ／ “At 8:37:52, Boston Center reached NEADS.” | p20（PDF p38）／p17（PDF p35）／p38（PDF p56） | p38 も “bypassed the chain of command”。FAA 内の報告もしている（p20 “In addition to notifications within the FAA”）。話したのはボストンセンターの TMU（運航管理） |
| K039 | c222・c702・c703 | 8:46 オーティスの F-15（2機）に発進命令・行き先が決まっていない・離陸まで7分・離陸8:53＝衝突の約6分後 | 一致 | “F-15 fighters were scrambled at 8:46 from Otis Air Force Base. But NEADS did not know where to send the alert fighter aircraft” ／ “Radar data show the Otis fighters were airborne at 8:53.” | p20（PDF p38） | 7分・約6分は計算（8:46:40→8:53＝6分20秒） |
| K040 | c224★ | 防空司令部が知らされてから8分48秒後・8:46:40 1機目が北棟に | 一致 | “At 8:46:40, American 11 crashed into the North Tower” | p7（PDF p25）／p20（PDF p38） | 8分48秒は計算。⚠️ 衝突時刻は資料で割れる＝語りは委員会の値（§3-1） |
| K041 | c302 | 175便は11便の15分あとに同じ空港を出た・8:33に約9,400m | 一致 | “departed Logan Airport at 8:14. By 8:33, it had reached its assigned cruising altitude of 31,000 feet.” | p7（PDF p25） | 31,000ft＝9,449m（計算） |
| K042 | c303・c304・c305 | 管制が175便に11便を探すよう頼んだ・見つけたうえで妙な無線を聞いたと伝えた・それが最後の交信・数分のうちに乗っ取り・8:47 応答符号が2回変わった・乗っ取りはこの前後 | 一致 | “Asked by air traffic controllers at 8:37 to look for an American Airlines 767 (Flight 11), United 175 reported spotting the aircraft at 8:38.” | 第1章 注42 p454（PDF p472）／p7（PDF p25）／p21（PDF p39） | 前半は本文に無く**注42**にある（旧版の p7・p21 だけでは出ない）。乗っ取りは “between 8:42 and 8:46”（p7）＝符号が変わる**前**→「この前後」は §3-2 |
| K043 | c306・c307 | 担当の管制官はほかの便の相手で手が離せない・気づいたのは8:51・8:53 同僚に「乗っ取られたかもしれない、機体が見つからない」 | 一致 | “the same New York Center controller was assigned to both American 11 and United 175.” ／ “contacted another controller at 8:53, saying that ‘we may have a hijack’ and that he could not find the aircraft.” | p21〜22（PDF p39〜40） | 「ほかの便」＝11便（同じ管制官が両方を担当し、11便を探していた）。担当は**ニューヨークセンター**＝c307 の札「ボストンセンターの管制官」は誤り（§2-B） |
| K044 | c308 | 約28分前に11便から流れた一言は複数形 | 一致 | “Planes, as in plural.” | p23（PDF p41）／p19（PDF p37） | 28分は 8:24:38→8:53 の計算（28分22秒） |
| K045 | c309・c310 | 175便からも乗務員と乗客が電話・内容は操縦室の乗員が動かない／航空会社には2機ぶんの通報・その情報は管制にも軍にも回っていない | ずれ | “The flight attendant reported that the flight had been hijacked, both pilots had been killed, a flight attendant had been stabbed, and the hijackers were probably flying the plane.” | p7〜8（PDF p25〜26）／p5（PDF p23） | 🔴 電話の中身は「乗っ取られた・操縦士2人が殺された・乗っ取った側が操縦しているらしい」で、「動かない」は原文に無い。🔴「管制に回っていない」も11便については逆：アメリカン航空は 8:29 ごろボストンセンターへ連絡（p5 “The center was already aware of the problem.”）。2機ぶんは別々の会社（11便＝アメリカン、175便＝ユナイテッド） |
| K046 | c311・c312 | 1970年から入居・30年街の顔・多い日で約5万人・ほかに4万人が毎日通り抜け | 一致 | “tenants began to occupy its space in 1970.” ／ “On any given workday, up to 50,000 office workers occupied the towers, and 40,000 people passed through the complex.” | p278（PDF p296） | 旧版の p277 は1頁ずれ。入居1970年は「複合施設」の話。街の顔＝“a unique and symbolic place in the culture of New York City and America”。30年は計算（1970→2001＝31年） |
| K047 | c313・c314 | 街の人もテレビも、この時点ではまだ事故だと思っていた・17分のあいだ街じゅうの関心が北棟に | 見つからない | “the 17 minutes from the crash of the hijacked American Airlines Flight 11 into 1 World Trade Center (the North Tower) at 8:46 until the South Tower was hit” | p285（PDF p303）／p293（PDF p311）／p35（PDF p53） | 「17分」は原文どおり（p293 にも “the 17-minute period”）。🔴「街の人もテレビも事故だと思っていた」は無い：“accident” 全38件・第9章 p285〜300 は0件。事故と見ていたのは**ホワイトハウスの職員**（p35 “In the absence of information that the crash was anything other than an accident”）と大統領の最初の反応（p35 “pilot error”） |
| K048 | c315・c316 | 175便はトランスポンダを切らず符号だけ書き換え・管制の画面にちゃんと映っていた・「乗っ取られた便」としては誰も見ていない | ずれ | “At about 8:55, the controller in charge notified a New York Center manager that she believed United 175 had also been hijacked.” | p21〜22（PDF p39〜40）／第1章 注66 p455（PDF p473） | 前半（切らずに符号を変えた）は一致（p16・p21・注54）。🔴 後半は**原文と逆**：8:53「we may have a hijack」、8:55「175便も乗っ取られたと思う」、8:58「two of them」、9:01〜9:02 コマンドセンターへ（p22）。注66 “The FAA knew or strongly suspected that ... Flight 175, 9 minutes after it was taken over.” 8:53 に担当の管制官は “could not find the aircraft”（p22）＝「ちゃんと映っていた」とも合わない。旧版の出典は NARA RG237（映像）だけ |
| K049 | c317 | 9:03:11 175便が南棟に | 一致 | “At 9:03:11, United Airlines Flight 175 struck the South Tower of the World Trade Center.” | p8（PDF p26）／第1章 注130 p460（PDF p478） | ⚠️ 時刻は割れる：NIST 9:02:59・NTSB 約9:02:40（OCR）・NORAD の証言 9:02（注130）＝語りは委員会の値（§3-1） |
| K050 | c317・c318 | 防空司令部がこの便を知ったのはこの瞬間・事前に聞いていない・ニューヨークの管制からの電話ではじめて | 言いすぎ（軽い） | “came in a phone call from New York Center to NEADS at 9:03. The notice came at about the time the plane was hitting the South Tower.” | p23（PDF p41） | 「この瞬間」は原文 “at about the time”（ほぼ同じころ）＝「ごろ」を足す |
| K051 | c319 | 9:07 ボストンの管制が全機への警告を求めた・操縦室の守りを固めろ・実行された跡は無い | 一致 | “requested at 9:07 that Herndon Command Center ‘get messages to airborne aircraft to increase security for the cockpit.’ There is no evidence that Herndon took such action.” | p10（PDF p28）／p23（PDF p41）／第1章 注67 p455 | 全機＝注67 “the pilots of all commercial aircraft”。ボストンセンターは**自分の空域**の便には警告を出した（p23・注67）＝実行されなかったのは全国への警告 |
| K052 | c320 | この時点で全米の空には数千機の民間機 | 一致（推論） | “about 4,500 commercial and general aviation aircraft soon landed without incident.” | p29（PDF p47） | 9:07 時点の機数は原文に無い。9:42 の命令のあと約4,500機が降りた（p29）ことからの推論。旧版の p25 には無い |
| K053 | c321・c322 | 1機目から2機目まで17分・2機目がぶつかった瞬間に事故ではないと誰もが分かった・175便は符号の変化から衝突まで16分ほど | 言いすぎ | “When they learned a second plane had struck the World Trade Center, nearly everyone in the White House told us, they immediately knew it was not an accident.” | p35（PDF p53）／p285（PDF p303） | 🔴 主語は「**ホワイトハウスの**ほぼ全員」＝「誰もが」は一般化。17分＝p285（8:46→9:03。秒では16分31秒＝計算）。16分ほど＝8:47→9:03:11（計算） |
| K054 | c402・c403 | 77便は8:20に出発・8:46に約10,700m・8:51 定時交信が最後の無線 | 一致 | “At 8:46, the flight reached its assigned cruising altitude of 35,000 feet. ... At 8:51, American 77 transmitted its last routine radio communication.” | p8（PDF p26） | 原文は「最後の**定時の**交信」。NTSB（OCR）も 8:51 “final routine radio transmission”。35,000ft＝10,668m |
| K055 | c404 | 8:54 南へそれた・乗っ取りは8:51〜8:54 | 一致 | “The hijacking began between 8:51 and 8:54.” ／ “At 8:54, the aircraft deviated from its assigned course, turning south.” | p8〜9（PDF p26〜27） | ⚠️ NTSB（OCR）は “approximately 8:55”＝§3-1 |
| K056 | c405・c406 | 8:56 トランスポンダが切られ一次レーダーも失う・インディアナポリスの管制センター・何度呼んでも応答無し | 一致 | “Two minutes later the transponder was turned off and even primary radar contact with the aircraft was lost. The Indianapolis Air Traffic Control Center repeatedly tried and failed to contact the aircraft.” | p9（PDF p27）／p24（PDF p42） | 一次レーダーの情報は 8:56〜9:05 の8分13秒、画面に出ていなかった（p25） |
| K057 | c407・c408 | 管制は墜落と考えた・西側の地上を探した・州警察に問い合わせ／9:05 航空会社が77便も乗っ取られたと把握・同じ会社はすでに11便を失っていた | 言いすぎ | “Shortly before 9:10, suspecting that American 77 had been hijacked, American headquarters concluded that the second aircraft to hit the World Trade Center might have been Flight 77.” | p9（PDF p27）／p24〜25（PDF p42〜43）／図表 p33（PDF p51） | 🔴 本文は「9:10少し前・乗っ取られたと**疑い**」。9:05 “AA headquarters aware that Flight 77 is hijacked” は図表 p33 の字＝本文より強い。⚠️「西側の地上」も合わない：管制がレーダーで探したのは予定の航路の西・南西（p25 “looked to the west and southwest along the flight's projected path”）。地上の捜索は空軍の捜索救難と州警察への依頼（p24）。墜落と考えた＝p24 “had possibly crashed” |
| K058 | c409 | 実際に向かっていたのは東・首都の川を挟んだ対岸 | 一致 | “American 77 traveled undetected for 36 minutes on a course heading due east for Washington, D.C.” | p25（PDF p43）／p1（PDF p19） | 対岸＝p1 “Others went to Arlington, Virginia, to the Pentagon. Across the Potomac River, the United States Congress was back in session.” 旧版の p26 はずれ |
| K059 | c413・c414★ | 9:21 コマンドセンターがダレスの管制に一次レーダーの点を探してくれと頼んだ・9:32 ダレスの管制官が画面の設定を切り替えて探した・高速で東へ動く点がひとつ | 言いすぎ（軽い） | “At 9:21, it advised the Dulles terminal control facility, and Dulles urged its controllers to look for primary targets. At 9:32, they found one.” | p25（PDF p43）／第1章 注144 p460 | 「画面の設定を切り替えて」はダレスについて原文に無い。一次の点を探せと促したのはダレス側（コマンドセンターは advised）。★の “observed a primary radar target tracking eastbound at a high rate of speed” は一致 |
| K060 | c415 | 9:34 その点はホワイトハウスの方角へ・空港はすぐ大統領警護隊へ連絡 | 一致 | “At 9:34, Ronald Reagan Washington National Airport advised the Secret Service of an unknown aircraft heading in the direction of the White House.” | p9（PDF p27）／p25（PDF p43） | 空港＝レーガン・ナショナル（p25 はレーガン・ナショナルとダレスの両方の FAA 職員が警護隊へ）。直前の行がダレスなので「空港」がダレスと聞こえる＝§3-2 |
| K061 | c416 | 自動操縦は9:29に切られていた・高度約2,100m・ペンタゴンの西61km | 言いすぎ（軽い） | “At 9:29, the autopilot on American 77 was disengaged; the aircraft was at 7,000 feet and approximately 38 miles west of the Pentagon.” | p9（PDF p27） | 「約」が距離に掛かっていない（approximately 38 miles）。⚠️ NTSB（OCR）は “approximately 35 miles west”、9:08 ごろにも約3分の解除があったと書く＝§3-1 |
| K062 | c417・c418 | ペンタゴンの西南西8km（5マイル）・ほぼ一周して向き直った先がペンタゴン・最後の数分で高度が一気に下がった | 一致 | “American 77 was then 5 miles west-southwest of the Pentagon and began a 330-degree turn. At the end of the turn, it was descending through 2,200 feet, pointed toward the Pentagon and downtown Washington.” | p9（PDF p27）／NTSB 77便 PDF p2 | ⚠️ NTSB（OCR）は “about 3.5 miles west-southwest”、旋回の終わり “about 2000 feet altitude and 4 miles southwest”＝§3-1。高度の線は NTSB の図で人が確かめる（§4 #4） |
| K063 | c419・c420 | 軍の輸送機が管制に頼まれて点を追った・757と見分けた・9:37:46 ペンタゴンの西側に・数秒後に輸送機が伝えた | 一致 | “Reagan National controllers then vectored an unarmed National Guard C-130H cargo aircraft ... The C-130H pilot spotted it, identified it as a Boeing 757 ... and at 9:38, seconds after impact, reported to the control tower” | p25〜26（PDF p43〜44）／p10（PDF p28）／p314（PDF p332） | 西側＝p314 “the west wall of the Pentagon”。⚠️ 9:37:46 は注154 で “estimated time of impact”（FDR・管制・レーダー・標高と衝突地点から推定）。NTSB（OCR）9:37:45、第9章 p314 は「9:37」＝§3-1 |
| K064 | c421 | 64人・建物の中125人（軍人55・職員70） | 一致 | “All 64 people aboard the airliner were killed, as were 125 people inside the Pentagon (70 civilians and 55 military service members).” | p314（PDF p332） | 64人は乗っ取った5人を含む（注188 の 184 は nonterrorists＝125＋59） |
| K065 | c422★ | 防空司令部は77便が乗っ取られたとは聞かされていない・9:34に見失ったと聞いただけ・3機目は探されていた場所にいなかった | 一致 | “NEADS never received notice that American 77 was hijacked. It was notified at 9:34 that American 77 was lost.” | p34（PDF p52）／p27（PDF p45） | 旧版の「p26」は誤り（この2文は **p34**、9:34 の通話は p27）。9:34 の知らせは NEADS の側からかけた電話で偶然得た（p27 “it had come by chance”）。9:36 に正体不明機の知らせ（p27・p34） |
| K066 | c502・c503・c504 | ハーンドンのコマンドセンター・その日の責任者はベン・スライニー・9:25 全米の離陸を止めた・飛んでいる機にはまだ何も言っていない | 一致 | “While this was being discussed by executives at FAA headquarters, the Command Center ordered one at 9:25.” | p25（PDF p43）／p14・p16（PDF p32・p34）／p29（PDF p47） | 肩書きは原文 “the Command Center's national operations manager”（p29）。図表 p33 “9:25 Herndon Command Center orders nationwide ground stop” |
| K067 | c507 | 9:42 スライニーが次の命令・飛んでいる全部の機を最寄りの空港に降ろせ | 言いすぎ（軽い） | “At 9:42, the Command Center learned from news reports that a plane had struck the Pentagon. The Command Center's national operations manager, Ben Sliney, ordered all FAA facilities to instruct all aircraft to land at the nearest airport.” | p29（PDF p47） | 9:42 は「ペンタゴンの件を報道で**知った**時刻」。命令の時刻は書かれていない（9:42以後）。図表 p32〜33 にも無い |
| K068 | c509・c510★ | 手引きにこういう場合のやり方は無い・国ごと閉じたことは一度も無い・前例の無い命令 | 一致 | “This was an unprecedented order.” | p29（PDF p47）／p31（PDF p49） | 手引きに無い＝p31 “The defense of U.S. airspace on 9/11 was not conducted in accord with pre-existing training and protocols.” |
| K069 | c515・ep05 | 命令からほどなく民間機はほとんど全部が降りた・約4,500機（旅客機も小型機も）・その日の夕方、空を飛ぶ民間機はほとんど無かった | 言いすぎ（軽い） | “about 4,500 commercial and general aviation aircraft soon landed without incident.” | p29（PDF p47）／p327（PDF p345） | 「ほとんど全部」「夕方ほとんど無かった」は原文に無い（“evening” 9件・該当なし）。言えるのは「約4,500機がほどなく無事に降りた」「国の空域が再び開いたのは9月13日の朝」（p327） |
| K070 | c516・c517・c518 | 乗客は何日も動けない・待合室で寝泊まりした人も多い・民間機が普通に飛ぶのは数日後・降りる途中の事故は1件も無い | 見つからない | “On the morning of September 13, the national airspace reopened for use by airports that met newly improvised security standards.” | p327（PDF p345）／p29（PDF p47） | 🔴 足止め・寝泊まりの記述は無い（“stranded” 0件・第10章 p320〜335 に乗客の話なし）。「数日あと」＝p327（9月13日朝）。「事故1件も無い」＝p29 “without incident” |
| K071 | c519 | 報告書は管制の仕事ぶりを高く評価・手引きに無いことをその場で決めてやりきった | 一致 | “thought outside the box ... in deciding to land all aircraft and executing that unprecedented order flawlessly.” | p31（PDF p49）／p29（PDF p47） | p29 “handled it with great skill” |
| K072 | c520★ | 9:25に離陸を止め9:42に全機を降ろす命令・その日のうちに空はからになった | 言いすぎ（軽い） | “about 4,500 commercial and general aviation aircraft soon landed without incident.” | p25（PDF p43）／p29（PDF p47） | 9:42 は K067 と同じ（知った時刻）。「その日のうちに空はから」は原文に無い（“soon landed” のみ・再開は9月13日）＝★の言い切りは推論 |
| K073 | c602 | 93便は8:42に離陸・25分あまりの遅れがこの便を最後の1機にした | 言いすぎ | “When it left the ground at 8:42, the flight was running more than 25 minutes late.” | p10（PDF p28）／p11（PDF p29）／p12（PDF p30） | 🔴 因果を足した。原文が遅れと結びつけるのは「世界貿易センターの件がすでに起きていた」こと（p12 “given Flight 93's tardy departure from Newark”）。乗っ取りが離陸の46分後だったこと（p11）も「最後」に効いている |
| K074 | c603・c604 | 9:24 運航管理者が93便に文字の警告を送った・操縦室への侵入に気をつけろ・93便から確かめたいと返事・届いた約4分後に乗っ取り | ずれ（軽い） | “[the dispatcher's] warning message was not transmitted to Flight 93 until 9:23.” ／ “At 9:24, [the] warning to United 93 was received in the cockpit.” | p11（PDF p29）／第1章 注79 p456（PDF p474） | 本文では 9:24 は**受信**、送信は 9:23。注79 は “were sent to the aircraft ... at 9:24”＝本文と注で1分割れる→本文を採るなら「9:24、警告が操縦室に届いた」。返事＝p11 “responded with a note of puzzlement”（9:26）。警告の文＝“Beware any cockpit intrusion”。約4分＝9:24→9:28 |
| K075 | c605 | 9:28 無線に争う音・ここから出ろという叫び声 | 一致 | “could be heard declaring ‘Mayday’ amid the sounds of a physical struggle in the cockpit. ... ‘Hey get out of here—get out of here—get out of here.’” | p11（PDF p29）／p28（PDF p46）／第1章 注158・159 p461 | 1回目 9:28:17・2回目 9:28:54（注158・159）。図表 p33 “9:28 Likely takeover” |
| K076 | c606・c607 | クリーブランドの管制センターが受けた・同じ周波数のほかの便も聞いた・9:30 ほかの便に順に問い合わせ・何機かが聞こえたと答えた | 一致 | “At 9:30, the controller began to poll the other flights on his frequency to determine if they had heard the screaming; several said they had.” | p28（PDF p46）／注159 p461 | 注159 に他の便の返事（9:31:48） |
| K077 | c608 | 乗っ取りの瞬間、93便は210m（700ft）下がった | 一致 | “While traveling 35,000 feet above eastern Ohio, United 93 suddenly dropped 700 feet.” | p11（PDF p29）／p28（PDF p46） | p28 は “descended some 700 feet”。⚠️ NTSB（OCR）は “a brief descent of about 600 feet at 9:28”＝§3-1・§4 #5 |
| K078 | c609 | 9:32 無線に3度目の声・席に着いていろ、機内に爆弾がある・客室に向けた放送が無線に乗ってしまったもの | 言いすぎ（軽い） | “At 9:32, a third radio transmission came over the frequency: ‘Keep remaining sitting. We have a bomb on board.’” | p28（PDF p46）／p12（PDF p30）／第1章 注75 p456（PDF p474） | 声と時刻は一致。「乗ってしまった」（うっかり）は原文で限定つき：p12 “may have inadvertently broadcast the message”、注75 “apparently did not know how to operate the communication radios”。p12 は放送そのものも “made or attempted to make” |
| K079 | c610★ | そのすぐあと自動操縦に東へ戻れという指示・西へ向かっていた機が向きを変えた・4機目は来た道を引き返した | 一致 | “The flight data recorder (also recovered) indicates that [the hijacker pilot] then instructed the plane's autopilot to turn the aircraft around and head east.” | p12（PDF p30） | NTSB（OCR）は 9:34 から上昇し針路120°（南東）へ旋回、自動操縦は heading select（§3-1） |
| K080 | c612 | 9:41 93便のトランスポンダも切られた・4機のうち3機が名前の消えた点に | 一致 | “At 9:41, Cleveland Center lost United 93's transponder signal.” | p29（PDF p47）／p16（PDF p34）／第1章 注54 p454 | p16 “the terrorists turned off the transponders on three of the four hijacked aircraft”。本文は「信号を失った」、図表 p33 と注54 は “turned off” |
| K081 | c613 | 9:34 93便の乗っ取りの報せは FAA 本部に届いていた・このあと軍には回っていない | 一致 | “By 9:34, word of the hijacking had reached FAA headquarters.” ／ “Nor did any manager at FAA headquarters pass any of the information it had about United 93 to the military.” | p28（PDF p46）／p30（PDF p48） | 軍（NEADS）が知ったのは 10:07、クリーブランドの軍連絡官から（p30）＝墜落の後。「回っていない」は FAA 本部からの話と分かる形に（§3-2） |
| K082 | c614・c615・c616 | 機内から次々に電話（座席の電話と手持ちの電話）・WTC の件が地上から機内へ・少なくとも5本 | 一致 | “During at least five of the passengers' phone calls, information was shared about the attacks that had occurred earlier that morning at the World Trade Center.” | p12〜13（PDF p30〜31） | 電話の種類＝p12 “GTE airphones and cellular phones” |
| K083 | c617 | 9:46 コマンドセンターは首都まであと29分と伝えた | 一致 | “At 9:46 the Command Center updated FAA headquarters that United 93 was now ‘twenty-nine minutes out of Washington, D.C.’” | p29（PDF p47） | 伝えた先は FAA 本部 |
| K084 | c618★・c619 | 家族との電話を切って前へ向かった人たち・9:57 機内の反撃・CVR が記録・機体は左右に振られ上下に揺さぶられた | 一致 | “At 9:57, the passenger assault began. Several passengers had terminated phone calls with loved ones in order to join the revolt.” | p13〜14（PDF p31〜32） | 揺さぶり＝p13 “roll the airplane to the left and right”・“pitched the nose of the airplane up and down” |
| K085 | c620・c621 | 10:03:11 レーダーの画面から点が消えた・シャンクスビル近くの野原・44人全員が亡くなった（乗客37・乗員7）・地上の巻き込まれ無し | 言いすぎ（軽い） | “United 93 crashed in Pennsylvania at 10:03:11, 125 miles from Washington, D.C. The precise crash time has been the subject of some dispute.” | p30（PDF p48）／p14（PDF p32）／第1章 注168 p461〜462／第9章 注188 p552（PDF p570） | 10:03:11 は「墜落の時刻」で「点が消えた時刻」とは書いていない（管制はその前にピッツバーグ付近で見失った＝p30）。時刻は地震計の 10:06:05±5 を退けて決めた（注168）＝§3-1。44人＝乗客37（乗っ取った4人を含む）＋乗員7（p10）。注188 “Forty nonterrorists died in the crash”＝地上の死者の記述は無い（推論で可）。旧版の出典は NARA RG237 だけ |
| K086 | c622・c623★ | 首都まで飛行機であと20分ほど・およそ201km（125マイル） | 一致 | “about 20 minutes' flying time from Washington, D.C.” ／ “125 miles from Washington, D.C.” | p14（PDF p32）／p30（PDF p48） | 125mi＝201.2km（計算）。原文の 125 に「およそ」は無い（足すのは可） |
| K087 | c624 | 乗っ取りから墜落まで35分・最後の6分は機内の人が動いていた | 一致 | “The hijackers attacked at 9:28.” ／ “At 9:57, the passenger assault began.” | p11（PDF p29）／p13（PDF p31）／p30（PDF p48） | 計算（9:28→10:03:11＝35分11秒、9:57→10:03:11＝6分11秒） |
| K088 | c624 | 4機のうち狙った建物に届かなかったのはこの1機だけ | 一致 | “[The hijacker pilot]'s objective was to crash his airliner into symbols of the American Republic, the Capitol or the White House.” | p14（PDF p32）／第1章 注85 p457 | 注85＝9:55:11 に首都のレーガン・ナショナル空港の VOR の周波数を入れた |
| K089 | c705 | 発進を指示した将校の言葉が当直の録音に残る・どこへ向かわせるか分からない、方角がほしい | 一致 | “the officer directing the fighters pressed for more information: ‘I don't know where I'm scrambling these guys to. I need a direction, a destination.’” | p20（PDF p38）／第1章 注119 p459（PDF p477） | 録音＝注119 “NEADS audio file, Weapons Director Technician position, channel 14; 8:45:54” |
| K090 | c706★ | 防空司令部が11便を知ったのは8:37:52・衝突8:46:40・この9分がいちばん長い余裕 | 一致 | “That nine minutes' notice before impact was the most the military would receive of any of the four hijackings.” | p20（PDF p38）／p7（PDF p25）／p21（PDF p39） | 9分は原文の丸め（実差 8分48秒）。8:37:52 の割れは §3-1 |
| K091 | c707・c708 | 9:09 ラングレーの F-16 が機内で待機・まだ発進ではない・向かう先はニューヨーク・燃料の減った先発機との交代 | 一致 | “NEADS considered scrambling alert fighters from Langley Air Force Base in Virginia to New York, to provide backup. The Langley fighters were placed on battle stations at 9:09.” | p24（PDF p42）／第1章 注137 p460（PDF p478） | 交代＝注137 “they might be called on to relieve the Otis fighters over New York City if a refueling tanker was not located”。“battle stations” の中身（機内で待機）は報告書は定義していない |
| K092 | c709・c710 | 9:21 防空司令部に「11便がまだ飛んでワシントンへ」・11便は約34分前に衝突済み・出どころはいまも分からない | 言いすぎ（軽い） | “We have been unable to identify the source of this mistaken FAA information.” | p26（PDF p44）／第1章 注148 p461 | 「いまも」は2004年の報告書の範囲を越える＝「委員会は出どころを突き止められなかった」。ボストンセンターは FAA 本部から聞いた（p26）。34分は計算（34分20秒） |
| K093 | c711・c712 | 9:24 ラングレーに発進命令・理由はもう存在しない11便・9:30離陸の F-16 は東の海上へ・向き直って首都へ | 一致 | “That order was processed and transmitted to Langley Air Force Base at 9:24. Radar data show the Langley fighters airborne at 9:30.” | p27（PDF p45）／p26（PDF p44）／p34（PDF p52） | 命令を出したのは 9:23（p27）。東へ向かった理由3つ（p27） |
| K094 | c713 | 77便衝突時、F-16は約241km（150マイル）離れていた | 一致 | “The Pentagon had been struck by American 77 at 9:37:46. The Langley fighters were about 150 miles away.” | p27（PDF p45） | 150mi＝241km（計算） |
| K095 | c714★ | 10:10 首都上空の F-16 に「撃ってはならない」 | 一致 | “At 10:10, the pilots over Washington were emphatically told, ‘negative clearance to shoot.’” | p45（PDF p63）／p31（PDF p49）／第1章 注172 p462・注231 p465 | ⚠️ 報告書の中で割れる：p31 は “Shortly after 10:10”、言葉も “negative—negative clearance to shoot”。訳は §3-3 |
| K096 | c715・c716 | 副大統領が2度目に撃墜を許したのは10:12〜10:18ごろ・93便は墜落済み・許可が防空司令部に届いたのは10:31・最初の衝突から1時間44分 | 一致 | “The military aide returned a few minutes later, probably between 10:12 and 10:18 ... The Vice President again said yes.” ／ “Shootdown authority was first communicated to NEADS at 10:31.” | p41（PDF p59）／p45（PDF p63）／p42（PDF p60） | “probably” を「ごろ」で受けている（可）。1回目の許可も “some time between 10:10 and 10:15”（p41）＝墜落の後。1時間44分は計算（1時間44分20秒） |
| K097 | c717 | 命令は現場の操縦士まで降りていない・報告書は届いていなかったとはっきり書いている | 一致 | “the only orders actually conveyed to the pilots were to ‘ID type and tail.’” | p43（PDF p61）／p44（PDF p62） | p44 “the fighter pilots under NORAD direction who had scrambled out of Langley never received any type of engagement order”＝NORAD の指揮下の話。アンドルーズの機は別の交戦規定（weapons free）を受けていた（p44） |
| K098 | c718 | 事前に軍へ知らされたのは1機だけ・残る3機は墜ちるまで乗っ取りとして伝わらず | 一致 | “no advance notice on the second, no advance notice on the third, and no advance notice on the fourth.” | p31（PDF p49）／p34（PDF p52） | 93便＝p34 “By the time the military learned about the flight, it had crashed.” |
| K099 | c719 | 首都の別の基地からも戦闘機・軍の指揮系統の外から出た機 | 一致 | “fighters had been scrambled out of Andrews, at the request of the Secret Service and outside the military chain of command.” | p44（PDF p62） | 旧版の p42・p43 はずれ（**p44**）。基地はメリーランド州のアンドルーズ、最初の機の離陸は 10:38（p44） |
| K100 | c720★ | 委員会は迎撃が間に合ったとは書いていない・軍は93便の乗っ取りを墜ちるまで知らなかった・間に合う順番になっていなかった | 一致 | “NORAD did not even know the plane was hijacked until after it had crashed.” ／ “NORAD officials have maintained that they would have intercepted and shot down United 93. We are not so sure.” | p44〜45（PDF p62〜63） | 原文はもっとはっきり言う（“We are not so sure.”）＝§3-2 |
| K101 | c802 | ここが狙われたのは初めてではない・1993-02-26 地下駐車場で貨物車の爆薬・6人死亡、約1,000人負傷 | 一致 | “At 12:18 P.M. on February 26, 1993, a 1,500-pound bomb stashed in a rental van was detonated on a parking garage ramp beneath the Twin Towers. The explosion killed six people, injured about 1,000 more” | p280（PDF p298） | 旧版の「p279・p280」は **p280** だけ。車は “rental van”（p72 も “Ryder rental van”） |
| K102 | c803・c804 | 管制の無線はふだんからずっと録音・防空司令部の当直席も同じように録られていた・ほかにレーダーの記録と当直の書き込み | 一致 | “time codes automatically recorded in the ATC audiotapes for the FAA centers” ／ “taped conversations at NEADS ... contemporaneous logs compiled at NEADS, Continental Region headquarters, and NORAD” | 第1章 注168 p462（PDF p480）／p34（PDF p52）／注94 p457 | ⚠️ 一部の席は録音が無い：注120 p459（PDF p477）“Because of a technical issue, there are no NEADS recordings available of the NEADS senior weapons director and weapons director technician position responsible for controlling the Otis scramble.”＝§3-2 |
| K103 | c805・c806 | 記録装置が回収できたのは4機のうち2機・93便は2つとも、77便は飛行記録だけ・93便は野原、残る3機は建物の中 | 一致 | “The CVRs and FDRs from American 11 and United 175 were not found, and the CVR from American Flight 77 was badly burned and not recoverable.” | 第1章 注76 p456（PDF p474）／p12（PDF p30）／注154 p461 | 93便の FDR＝p12 “The flight data recorder (also recovered)”。77便の FDR＝注154（衝突時刻の推定に使用）。⚠️ 注76 の “This is the only recorder from the four hijacked airplanes to survive the impact and ensuing fire.” は93便の CVR の文＝単独で引くと「1つだけ」に読める（§3-2） |
| K104 | c807 | 委員会は19日間の公聴会・160人から話を聞いた・証言と録音と記録簿を突き合わせ | 一致 | “we held 19 days of hearings and took public testimony from 160 witnesses.” | p.xv（PDF p15）／p34（PDF p52） | 160人は「公開の証言」。ほかに “interviewed more than 1,200 individuals in ten countries”・“more than 2.5 million pages of documents”（p.xv） |
| K105 | c808★・c809 | 先に公表された時系列と録音が食い違い、委員会は録音を採った・食い違ったのはラングレー機の発進の理由・実際は存在しない便に向けて飛んだ | 言いすぎ（軽い） | “this response to a phantom aircraft was not recounted in a single public timeline or statement issued by the FAA or Department of Defense.” | p34（PDF p52） | 食い違いは3つ：9:16 に93便の乗っ取りを知った・9:24 に77便の乗っ取りを知った・ラングレー機は77便／93便に応じて発進（どれも誤り）。語りは1つだけのように言う。委員会が採ったのは録音と記録簿と “other records” |
| K106 | c811 | 1機目の衝突時刻は資料によって3つ・8:46:40／8:46:30／8:46:26 | 一致 | “At 8:46:40, American 11 crashed into the North Tower” ／ 表6-1 “First Aircraft Strike 8:46:30 a.m.” ／ 表6-1 “1 8:46:26 93-99 N 109-152” | 委員会 p7（PDF p25）／NIST NCSTAR 1 p84（PDF p134）／NCSTAR 1-6 p156（PDF p240） | ⚠️ NCSTAR 1-6 の中でも割れる：Finding 24（p.lxxv・PDF p79）は 8:46:30。NTSB 11便（OCR）は “approximately 8:?:40”（分が読めない）＝§4 |
| K107 | c813 | 建物を調べたのは別の役所・崩れ方を秒単位で見るために時刻の基準を作り直した | 一致 | “Images were timed to a single well-defined event ... the moment the second plane struck WTC 2, established from the time stamps in the September 11 telecasts.” | NIST NCSTAR 1 p83〜84（PDF p133〜134） | 写真3,032枚・映像2,673本を ±3秒以内で時刻づけ（p84） |
| K108 | c816・c817 | 9:21 の誤った連絡の出どころは分からないと書いた・それまでの説明を書き改めた | 一致 | “We have been unable to identify the source of this mistaken FAA information.” | p26（PDF p44）／p34（PDF p52）／p31（PDF p49） | 書き改め＝p31 の見出し “Clarifying the Record”・p34 |
| K109 | c901・c902 | 2001年11月に議会が法律・保安検査を国の仕事に・それまでは航空会社が業者に頼んでいた・国の職員が自分で行う | 一致 | “In November 2001, Congress passed and the President signed the Aviation and Transportation Security Act. This act created the Transportation Security Administration (TSA)” | p391（PDF p409）／p2〜4（PDF p20〜22） | 国の職員＝p391 “congressional mandates to federalize the security checkpoint screeners”。それまで＝航空会社が警備会社に委託（p2〜p4） |
| K110 | c903・c907 | 扉の造りが変わった・当時は緊急時にすぐ開けられることを求めた・いまはその逆／乗員は犯人と戦わないよう教えられていた・いまはそう教えられていない | 一次資料の外 | “Prior to 9/11, FAA regulations mandated that cockpit doors permit ready access into and out of the cockpit in the event of an emergency.” | p85（PDF p103） | 「当時」の2点は一致（p85。“Common Strategy of cooperation and nonconfrontation”）。「いま」の2点は委員会報告に無い（p383 は “new precautions to protect aircraft” とだけ）＝現行の規則など別の出典が要る |
| K111 | c905・c906★ | 管制と軍のつなぎ方もこの日のあとに作り直された・当時は本部を何段も上がってから軍へ・あの朝その順番は間に合わなかった | 一次資料の外 | “On the morning of 9/11, the existing protocol was unsuited in every respect for what was about to happen.” | p17〜18（PDF p35〜36）／p31（PDF p49） | 「当時」と「間に合わなかった」は一致。「作り直された」は報告書に記述なし（“Domestic Events Network” 0件・“since 9/11” 8件はどれも別の話） |
| K112 | c909 | 25年が経ってもその手順はまだ続いている | 一次資料の外 | — | — | 現在（2026年）の話。報告書（2004年）の範囲外 |
| K113 | ep04 | 1機目の衝突から4機目の墜落まで約1時間17分 | 一致 | “At 8:46:40, American 11 crashed into the North Tower” ／ “United 93 crashed in Pennsylvania at 10:03:11” | p7（PDF p25）／p30（PDF p48） | 計算＝1時間16分31秒（「およそ」で可）。NIST の 8:46:30 を使うと1時間16分41秒 |

---

## 2. ④で直す主なもの（言いすぎ・ずれ・見つからない）

### 2-A 語り（113行の中・重い順）

| 順 | ID | カット | 何が違うか（原文） |
|---:|---|---|---|
| 1 | K048 | c315・c316 | 「乗っ取られた便としては誰も見ていない」は**原文と逆**。ニューヨークセンターは 8:53「we may have a hijack」、8:55「175便も乗っ取られた」と判断し、9:01〜9:02 にコマンドセンターへ伝えた（p22・注66「9分後に知っていたか強く疑っていた」） |
| 2 | K025 | c121 | 「1986年からの15年、アメリカ機は1機も乗っ取られていない」は “no **terrorist** had hijacked ... since 1986”（p85）の限定落ち。注91＝国内の乗っ取りは1991年まで、p14・注90＝1993年にも米国の管制が関わる乗っ取り |
| 3 | K045 | c309・c310 | 175便からの電話の中身は「操縦士2人が殺された・乗っ取った側が操縦しているらしい」（p7〜8）で「動かない」ではない。「管制に回っていない」も、11便はアメリカン航空が 8:29 ごろボストンセンターへ連絡している（p5） |
| 4 | K023 | c119 | “loaded with up to 11,400 gallons”（p4）は**積んでいた量**。「積める量（容量）」「満載」は原文と違う |
| 5 | K053 | c321 | 「事故ではないと誰もが分かった」の原文の主語は「ホワイトハウスのほぼ全員」（p35） |
| 6 | K047 | c313 | 「街の人もテレビもまだ事故だと思っていた」は見つからない（事故と見ていたのはホワイトハウスの職員＝p35） |
| 7 | K031 | c204 | 「思い出せた人はいなかった」はボストンの監督者の話。ダレス・ニューアークは「変わった点を覚えていない」（p2〜4） |
| 8 | K057 | c407・c408 | 9:05「把握」は図表の字。本文は「9:10少し前・乗っ取りを疑い」（p9）。「西側の地上を探した」も、原文はレーダーで西・南西を見た（p25） |
| 9 | K073 | c602 | 「遅れがこの便を最後の1機にした」は因果の足し。原文は遅れ→WTC の件が先に起きていた（p12） |
| 10 | K070 | c516・c517 | 乗客の足止め・待合室での寝泊まりは一次資料に無い（言えるのは「空域の再開は9月13日の朝」＝p327） |
| 11 | K027 | c908 | 「冷戦のころの配置」は逆向き。7か所は冷戦期の26か所から減った残り（p16） |
| 12 | K074 | c603 | 9:24 は受信の時刻。送信は 9:23（p11）。注79 は 9:24 に送ったと書く＝本文と注で割れる |
| 13 | K067・K072 | c507・c520★ | 9:42 は「ペンタゴンの件を知った」時刻。命令の時刻は書かれていない。「その日のうちに空はから」も原文に無い（“soon landed”） |
| 14 | K105 | c808・c809 | 公表の食い違いは3つ（9:16 の93便・9:24 の77便・ラングレー機の理由）。1つだけのように言っている |
| 15 | K078 | c609 | 「無線に乗ってしまった」は原文 “may have inadvertently”・“apparently” の限定落ち |
| 16 | K050 | c317 | 「この瞬間」は原文 “at about the time” |
| 17 | K085 | c620 | 10:03:11 は墜落の時刻で「点が消えた時刻」ではない。原文は時刻に “some dispute” があったと書く |
| 18 | K092 | c710 | 「いまも分かっていない」→「委員会は突き止められなかった（2004年）」 |
| 19 | K061 | c416 | 「西61キロ」に「およそ」（approximately 38 miles）。NTSB は約35マイル |
| 20 | K035・K005・K006・K059・K069 | c218・pr05・pr06・c414・c515・ep05 | 原文に無いまとめ・推論（8時台は入りきっていない／主に爆弾と拳銃／管制も訓練された／画面の設定を切り替えて／夕方ほとんど無かった）。言い換えの元の文は §1 のメモ |

### 2-B 画面の札（`quote` 型の SPEC。113行の外だが画面に大きく出る）

`be3dc65:tools/cuts/c2〜c7.py` の `fig=("quote", …)` 13カットを原文に当てた。

| カット | 札の字（SPEC） | 原文 | 直し |
|---|---|---|---|
| c303 | who＝175便の操縦室 → **to＝ボストンセンター（管制）**・when＝**8時40分ごろ** | 報告の相手は**ニューヨークセンター**（p21 “shortly after entering New York Center's airspace ... ‘We figured we'd wait to go to your center.’”）。時刻は 8:41（注42）／約8:42（p21） | ずれ。to＝ニューヨークセンター、when＝8時41分ごろ。11便を探す依頼は 8:37・見つけたのは 8:38（注42） |
| c307 | **who＝ボストンセンターの管制官** | “the same **New York Center** controller was assigned to both American 11 and United 175”（p21）→8:53 “we may have a hijack”（p22） | ずれ。who＝ニューヨークセンターの管制官 |
| c419 | phrase＝「あれはボーイング757だ」（発言の形） | “identified it as a Boeing 757”（p26）＝**間接話法**。発言の字は報告書に無い | 言いすぎ。「757と見分けた」と地の文で出す |
| c414 | 「どうやって＝画面の設定を切り替えて一次レーダーを出した」 | “Dulles urged its controllers to look for primary targets”（p25） | 言いすぎ（K059 と同じ） |
| c609 | doc＝「管制の無線に乗ってしまったもの」 | “may have inadvertently broadcast”（p12）・“apparently”（注75） | 言いすぎ（K078 と同じ） |
| c705 | to＝「当直の部下」 | 相手は書かれていない（p20 “pressed for more information”） | 見つからない（軽い）。to を外す |
| c206・c211・c220・c319・c604・c709・c714 | — | 時刻・話し手・相手は原文と合う（c220 の話し手はボストンセンターの TMU） | 訳の注は §3-3（c211・c714） |

---

## 3. 一致でも直す方がよいもの（言い方・帰属）

### 3-1 時刻・数が資料で割れるもの（語りはどの値か）

| 出来事 | 委員会報告（本文） | ほかの値 | 語り |
|---|---|---|---|
| 11便の離陸 | 7:59（p4） | NTSB 約8:00（OCR・PDF p1〜2） | 委員会 |
| NEADS が11便を知った | 8:37:52（p20） | 図表 p32・注121 は「8:38」。注117 の戦闘配置の音声は 8:37:15（本文より前＝報告書は理由を書いていない） | 委員会本文 |
| **11便の北棟衝突** | **8:46:40**（p7。第9章 注30＝FAA のレーダーと管制ソフトの論理から） | NIST NCSTAR 1 表6-1 **8:46:30**（テレビの時刻表示が基準）／NCSTAR 1-6 表6-1 **8:46:26**（同じ巻の Finding 24 は 8:46:30）／NTSB 約8:?:40（OCR で分が欠ける）／第9章 p285 は「8:46」 | 委員会（c811 は3つを並べる） |
| **175便の南棟衝突** | **9:03:11**（p8。注130＝FAA のレーダーと管制ソフトの論理） | NIST **9:02:59**（NCSTAR 1 表6-1）／NTSB **約9:02:40**（OCR）／NORAD の証言 9:02（注130）／p22 は「9:03」 | 委員会 |
| 77便の針路逸脱 | 8:54（p9） | NTSB 約8:55（OCR） | 委員会 |
| 77便の自動操縦の解除 | 9:29・西へ約38マイル・7,000ft（p9） | NTSB 約9:29・西へ約35マイル・7,000ft 付近、ほかに 9:08 ごろ約3分の解除（OCR） | 委員会 |
| 77便の最後の旋回 | 9:34・西南西5マイル・330度・終わりに 2,200ft を降下中（p9） | NTSB 9:34・西南西約3.5マイル・330度・終わりに約2,000ft・南西4マイル（OCR） | 委員会 |
| **77便のペンタゴン衝突** | **9:37:46**（p10。注154 で「推定」） | NTSB **9:37:45**（OCR）／第9章 p314 は「9:37」 | 委員会 |
| 93便の 9:28 の降下 | 700ft（p11）・約700ft（p28） | NTSB 約600ft（OCR） | 委員会 |
| **93便の墜落** | **10:03:11**（p30。本文は “some dispute”、注168 で地震計の 10:06:05±5 を退け「1秒以内」） | NTSB 10:03:11（OCR）＝一致 | 委員会（＝NTSB） |
| 93便への警告 | 送信 9:23・受信 9:24（p11） | 注79 は「9:24 に送った」 | 注79 側（K074） |
| 「撃つな」の指示 | 10:10（p45）／“Shortly after 10:10”（p31） | 注172＝10:10、注231＝10:10〜11 | p45 |
| 北棟の高さ・1辺 | 約1,350ft・208ft（p278） | NIST 屋上 1,368ft（コンコース階から）＋アンテナ 360ft・1辺約210ft（NCSTAR 1 p5） | 両方（c216・c217） |
| 93便の速さ（語りには無い） | 580mph（p14） | NTSB 約490kt（563mph）（OCR） | — |

- **語りの時刻はすべて委員会報告の本文の値**（例外は K074 の 9:24＝注79 と同じ）。c812「どれかが嘘なのではない。測っている量が違うだけ」は原文の説明と違う：同じ「衝突の瞬間」を、委員会は FAA のレーダーと管制ソフトの論理で、NIST はテレビの時刻表示（衛星・原子時計で合わせた局の時計）で決めた（NCSTAR 1 p83）＝**測っている量は同じで、測り方（データと時計）が違う**。113行の外だが④で直す候補

### 3-2 言い方・帰属で直すとよいもの（一致の行）

- **K002**：出典を第1章 注1（p451）に付け替え。p245 は乗っ取った側の供述の又聞き（取り調べに基づく）＝そう分かる形で
- **K004・K098**：「0分」は “no advance notice” の言い換え。77便は 9:36 に「正体不明機がホワイトハウスの南西6マイル」と NEADS に伝わっている（p27・p34）
- **K010**：2,973 は「2004年7月9日時点」の数（注188）
- **K011**：東部「夏時間」（EDT）
- **K013**：報告書 p4 は93便を「going to Los Angeles」と書く（p10・p33 は San Francisco）＝画面で p4 を引かない
- **K019〜K021・K085**：乗客の数は乗っ取った側を含む（11便81人に5人・175便56人に5人・77便58人に5人・93便37人に4人）
- **K028**：主語 NORAD と「国内で」（within the United States）を落とさない
- **K032**：「長いあいだ」は「およそ25分」と原文どおり言える（旧版 §10-3 の訂正）
- **K037**：「屋上まで417m」はコンコース階から。527m は足し算
- **K042**：「乗っ取りはこの前後」→「その少し前（8:42〜8:46）」
- **K051**：ボストンセンターは自分の空域の便には警告を出した（実行されなかったのは全国への警告）
- **K054**：「最後の**定時の**交信」
- **K060**：「空港」＝レーガン・ナショナル（ダレスの職員も警護隊へ連絡）。直前の行がダレスなので主語を言う
- **K063**：9:37:46 は「推定」（注154）
- **K066**：肩書きは “national operations manager”（全米の運用の責任者）
- **K081**：「軍には回っていない」は FAA 本部からの話。軍は 10:07 にクリーブランドの軍連絡官から知った（墜落の後）
- **K096**：1回目の許可（10:10〜10:15）も墜落の後
- **K097**：届かなかったのは NORAD 指揮下（ラングレー）の操縦士。アンドルーズの機は別の規定
- **K100**：原文は “We are not so sure.”（委員会ははっきり疑っている）＝語りより強く言える
- **K102**：NEADS の一部の席は技術的な問題で録音が無い（注120）
- **K103**：注76 の “the only recorder ... to survive” は93便の CVR の話（93便の FDR と77便の FDR も回収されている）
- **K104**：160人は公開の証言。面接は1,200人超・文書250万頁超（p.xv）
- **K106**：NIST の中でも 8:46:30／8:46:26 が割れる（NCSTAR 1-6 の Finding 24 と表6-1）

### 3-3 訳（★と quote の原文と日本語）

| カット | 原文 | 旧版の訳 | 注 |
|---|---|---|---|
| c211★・c308 | “We have some planes.”（p19）／“Planes, as in plural.”（p23） | 「複数の飛行機がある」 | 原文は「**こっちは**何機か（押さえて）ある」＝主語 we が落ちて「ある」だけになっている。複数形という要点は合う。直すなら「こっちには何機もある」など |
| c714★ | “negative clearance to shoot”（p45）／“negative—negative clearance to shoot”（p31） | 「撃ってはならない」 | 直訳は「撃つ許可は出ていない」。禁止の命令形に強めている（意味の向きは同じ）。p31 は2回重ねて言っている |
| c604 | “confirm latest mssg plz”（p11） | 「いまの知らせをもう一度確かめたい」（語り）／「さっきの知らせを確かめたい」（札） | 合う。“a note of puzzlement”（戸惑い）を添えられる |
| c220 | “No, this is not an exercise, not a test.”（p20） | 「訓練ではない」 | 合う（“not a test” を省略） |
| c303 | “we heard a suspicious transmission on our departure out of Boston”（p21） | 「妙な無線を聞いた」 | 合う（相手と時刻は §2-B） |
| c307 | “we may have a hijack”（p22） | 「乗っ取られたかもしれない」 | 合う（話し手は §2-B） |
| c319 | “get messages to airborne aircraft to increase security for the cockpit”（p10） | 「操縦室の守りを固めろ」 | 依頼の中身を命令形にした言い換え。発言の字ではない |
| c414★ | “observed a primary radar target tracking eastbound at a high rate of speed”（p25） | 「高速で東へ動く点が、ひとつ」 | 合う（「ひとつ」は p25 “they found one”） |
| c610★ | “turn the aircraft around and head east”（p12） | 「来た道を引き返した」 | 合う |
| c510★ | “This was an unprecedented order.”（p29） | 「これは、前例の無い命令だった」 | 合う |

### 3-4 113行の外で目についたもの（全数は当てていない）

- **c322★「2機目は、最後まで追えていなかった」・c322「誰かが気づいたとしても、知らせを届ける先が無かった」**：p22 は管制が正体不明機（175便とみられる）を追い、ターミナルの管制が降下を見て「the radar data terminated over Lower Manhattan」と書く。9:01〜9:02 にコマンドセンター、9:03 に NEADS へ伝わっている（p22・p23）＝K048 と同じ向きの問題
- **c910「9月11日より前、国じゅうの空を閉じるという考えは無かった」**：原文は “This was an unprecedented order.”（p29）まで。「考えが無かった」は見つからない（“SCATANA” 0件）
- **c812「測っている量が違うだけ」**：§3-1 の下の注のとおり

---

## 4. 人が原寸で見る頁（この係は画像を開いていない）

| # | ファイル・PDF頁 | 何を確かめるか | 使う行 |
|---|---|---|---|
| 1 | `analytics/materials/ep7/ntsb_flight_path_study_AA11.pdf` PDF p1〜p2 | 離陸「approximately 8:00 AM」・8:13:29／26,000ft・8:21・**衝突時刻（OCR は「8 : : 40」で分が欠ける）** | K019・K029・K106 |
| 2 | `ntsb_flight_path_study_UA175.pdf` PDF p2 | **衝突「approximately 9:02:40」**（4つ目の値）・8:33・8:47 の符号変更2回 | K041・K042・K049 |
| 3 | `ntsb_flight_path_study_AA77.pdf` PDF p2 | 逸脱「approximately 8:55」・9:08ごろの解除・9:29／「approximately 35 miles」／7,000ft・9:34／「about 3.5 miles west-southwest」／330度・旋回の終わり「about 2000 feet」「4 miles southwest」・衝突「9:37:45」 | K055・K061・K062・K063 |
| 4 | `ntsb_flight_path_study_AA77.pdf` PDF p4〜p7 | 図（経路・高度の推移・最後の旋回）。c418「最後の数分で高度は一気に下がっている」が線に出るか（旧版 §12-3 #3 の点はまだ1つも拾っていない） | K062 |
| 5 | `ntsb_flight_path_study_UA93.pdf` PDF p2 | 9:28 の降下「about 600 feet」・9:34 上昇と針路120°・9:41・10:03:11 | K077・K079・K080・K085 |
| 6 | `nist/ncstar1.pdf` PDF p55（印字 p5） | 1,368ft・360ft・約210ft（OCR の層で1回しか出ない値） | K035・K037 |
| 7 | `nist/ncstar1.pdf` PDF p134（印字 p84） | 表6-1：8:46:30・9:02:59・9:58:59・10:28:22 | K049・K106 |
| 8 | `nist/ncstar1-6v1.pdf` PDF p240（印字 p156）／PDF p79（印字 p.lxxv） | 表6-1 の1行目「8:46:26」（OCR で1回だけ。表の一覧は p154 と書く）／Finding 24「8:46:30」 | K106 |
| 9 | `GPO-911REPORT.pdf` PDF p50〜p51（印字 p32〜33） | 図表の時刻と出来事の対応（文字の層では図の字の並びが崩れる）：9:05 “AA headquarters aware that Flight 77 is hijacked”・9:24・9:41・8:38 | K057・K074・K080 |
| 10 | `GPO-911REPORT.pdf` PDF p1〜p4 | 刊行年（2004）が表紙・扉に印刷されているか（文字の層に無い） | K007 |

- 合計 **10件・19頁**（機械で足した：#1＝2頁・#4＝4頁・#8＝2頁・#9＝2頁・#10＝4頁、ほかは1頁ずつ）
- 委員会報告の本文は生まれつきの文字の層（OCR ではない）なので、§1 の引用は人が見なくてよい。NIST と NTSB は OCR 並みの層＝**画面に出す値は図と表の字で確かめてから**

---

## 関連

- [old_script_inventory.md](old_script_inventory.md) §8（主張の表）・§3（★と quote）
- 生の照合の記録（git の外）＝`src/claims_raw/`（検索の道具・検索の出力・第1章と注の書き出し）
