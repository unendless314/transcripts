# 校稿準則（Proofread Guidelines Template）

> 本檔案是全 20 集共用的校稿準則模板（由 UFO-01 實務經驗歸納）。
> 每集開始校稿前，複製本檔為 `data/<episode>/proofread_guidelines.md`，並在「本集專屬事項」補充該集特有的術語、已知問題與前任遺留事項。
> 翻譯階段的風格規範請見 `data/<episode>/translation_guidelines.md`（兩者職責分立；衝突時以本檔與術語表為準）。

---

## 一、參考資料與優先序

校稿時可參考的文件，衝突時依下列優先序裁決：

1. **網路流通慣用譯名** — 人名／地名／專有名詞先查網路流通譯名（維基百科 zh-tw、主流媒體等）；有流通者從流通譯法
2. `configs/terminology_master.yaml` — 跨集術語主表（預設參考；網路無流通資訊時以主表確保跨集一致性）
3. `configs/terminology_master_rules.yaml` — 主表編輯規則（ deprecated 形式、情境例外）
4. `data/<episode>/terminology.yaml` — 本集術語表
5. `data/<episode>/topics.json` — 各 topic 摘要與 `potential_errors`（轉錄錯誤紀錄）
6. 本檔與 `data/<episode>/proofread_guidelines.md`

⚠️ **主表並非絕對權威**：主表由各集詞彙表自動彙整生成，部分集數詞彙表未經校稿，詞條可能與網路流通慣用不合（實例：2026-08 UFO-05 校稿發現主表 Jim Penniston 譯「吉姆·佩尼斯頓」，網路流通實為「潘尼斯頓」，經人工裁決修正）。發現主表與網路流通衝突時，**不得盲從主表，也不得逕自改用其他譯名**，應暫停回報人工裁決；裁決後回寫 `terminology_master_rules.yaml` 與相關各集詞彙表，並以 `build_terminology_master.py --force` 重建主表。

## 二、術語與專有名詞原則

### 1. 人名：全部統一中譯
- 譯名先查網路流通慣用（見第一節優先序）；主表已收錄且與流通一致者從主表；網路無流通者用台灣標準音譯
- 同句重複出現時，第二次可簡稱姓氏
- 全名與簡稱形式（例：多蘭先生/多蘭）須跨 topic 保持一致
- 注意中譯同音歧義：如「喬治說」聽感近似「教智說」，必要時改用姓氏或調整句式

### 2. 公司／機構名
- 知名縮寫保留原文：GE、GM、TRW、CIA、NSA、FBI、DIA、NRO、HBO、MUFON 等
- 其餘中譯（依主表；主表未收錄者查維基百科標準譯名，音譯採用台灣慣用形式）
- 軍事基地全中譯（專案慣例）：萊特-帕特森、柯特蘭、霍洛曼、內利斯、愛德華茲空軍基地
- 媒體/節目名保留原文：Coast to Coast AM、earthfiles.com、《Bad Astronomy》、Diane Rehm Show
- 書籍/報告名：已有通行中譯者用中譯（《詭異收穫》），無者保留原文（《UFO Evidence》）

### 3. 關鍵術語定譯
- Top Secret → 最高機密（非「絕密」）
- Cover-up → 真相掩蓋；Disclosure → 真相揭露
- Being/Beings → 存有（「非人類存有」）；non-humans 統一
- Roswell → 羅斯威爾（地名與事件皆中譯，不保留原文）
- 核物理學家（非「核子物理學家」）、藍皮書計畫（非 Blue Book 計畫）

## 三、Whisper 轉錄錯誤處理

原文 WER 約 5–10%，**不可將轉錄視為絕對事實**。

1. **高信心拼寫／同音錯誤**（專有名詞、技術詞）：
   - 譯文直接採用正確拼寫
   - notes 註明「原文 X 應為 Y」
   - 同時在 `topics.json` 該 topic 的 `potential_errors` 補一筆（segment_id / error_text / suggested_correction / reasoning），供收尾時 `fix_transcription_errors.py` 修正 main.yaml 原文
   - ⚠️ 同一誤聽常在多段重複出現（例：Curlin→Kirtland 出現 4 次），務必全數補錄
2. **不確定或疑似講者口誤**（年份、數字等事實疑義）：
   - 不擅自修改原文資訊，保留原數字
   - notes 標記疑義與查證結果，confidence 降為 medium
3. 有疑慮可上網查證（人名拼寫、歷史日期、機構譯名）

## 四、格式與機械規則

### 草稿格式
- 格式：`N. 原文` 下一行 `→ {"text": "...", "confidence": "high/medium/low", "notes": "..."}`
- **只改 `→` 行**；JSON 必須保持**單行且合法**（斷行或語法錯誤會被 backfill 標為 needs_review）
- notes 內不可出現未跳脫的雙引號
- 段落編號行、`## Speaker Group N` 標題不可變動（parser 靠行首格式辨認）

### 標點與排版
- **數字千分位用半形逗號**：`4,000`、`10,000`、`1,000 萬`
- 中文譯文用中文標點（，。：「」）；引號用「」『』
- **保留全形括註「中譯（English）」**（2026-08-09 人工裁決）：草稿中人名／地名／專有名詞的原文括註**不得刪除**，校稿僅可修正括註內的錯字或標點；重要專有名詞首次出現若無括註可補上。括註內若為純英文內容，其標點用半形（例：（Ramstein, Germany））
- 既有半形括號的原文註釋（例：藍皮書計畫 (Project Blue Book)）保留原樣，無需強改全形
- 中英混排空格慣例：UFO 前後空格、數字與中文之間空格
- 討論外文發音的段落（如姓氏發音）可保留原文並括註中譯

## 五、台灣用語慣例

- 網路（非網絡）、品質（非質量）、太空（非航天）
- 透過（非通過）；但「通過電話」「通過法案」等動賓用法是正確的，勿誤改
- 資訊、資料、影片、連結等台灣慣用詞

## 六、語意審查要點

逐段檢查：
- **直譯成語誤用**：如 don't want any part of 不可譯「不想要任何…的部分」
- **前後矛盾**：如 bodies（含存活者）不可譯「屍體」後又說「活著的」
- **語境判斷**：韓戰語境的 Korea 指北韓；sharing an award 是分享共同榮譽非個人獲獎
- **原文句構破碎**（Whisper 常見）：譯文補足語意，notes 標記，confidence 視情況降 medium
- 講者口語重複、贅字可適度潤飾，但不可增減事實資訊

## 七、作業流程

1. 閱讀順序：本集 `proofread_guidelines.md` → `terminology.yaml` → `topics.json` → 前一個 topic 的定譯（保持一致）
2. 大檔（>50KB）分段讀取、分段審訂
   - 有疑慮時可比對 git 歷史：本專案全程以 git 追蹤，校稿前的草稿版本可用 `git log -p -- data/<episode>/drafts/<file>` 或 `git show <commit>:<path>` 查閱；需要還原被改動的內容（如括註、譯名）時，以 git 歷史為準，勿憑記憶補寫
3. 每修完一檔立即驗證：
   - 全部 `→` 行 JSON 合法（可用 python 逐行 `json.loads`）
   - Grep 掃殘留：`\d，\d`（千分位污染）、原文人名、`網絡|絕密|核子物理|通過`
4. 更新交接筆記（進度、修訂數、新發現、已拍板決策）：**一律寫入本檔「八、本集專屬事項」**，嚴禁在 drafts/ 放置任何筆記或說明檔（backfill_translations.py 會 glob 解析 drafts/ 內全部 `*.md`，非 topic 檔會被誤讀）
5. **回填統一在所有 topic 審完後執行**，切勿中途回填

### 收尾流程（依序）

> ⚠️ **人工確認門檻**：審完所有 topic 後必須**暫停**，向人工回報修訂摘要與待裁決事項，取得明確確認後才能進行以下任何步驟；收尾預設由人工執行，AI 校稿者不得擅自回填、修正原文或匯出。
> 歷史教訓：2026-08 千分位事件中，工具 bug 曾透過自動流程污染全專案譯稿，全自動化風險過高。

1. `fix_transcription_errors.py --dry-run` 檢查後正式執行（修 main.yaml 原文）
2. `backfill_translations.py --dry-run` 驗證 JSON 可解析
3. 正式回填
4. `export_srt.py`（需要時）
5. `split_srt.py`（需要時）
6. ⚠️ 本機 `python3` 是 Windows Store 假 stub（exit code 49），驗證腳本請用 `python`

## 八、本集專屬事項

### 本集概況（2026-08-23 啟動）
- 本集為 A Global Phenomenon Part 2（上集 UFO-15 已校稿完結）：國際專家小組 Q&A，主題涵蓋美國檔案公開、ESP 與航空安全、加拿大／中國案例、先進推進理論、聯合國行動提案
- 證人（依 UFO-15 先例與本集 topics.json）：格蘭特·卡麥隆、尼克·波普、孫式立博士（Sun Shili，原文誤聽 Sheila/Shelley/Schille）、安東尼奧·胡尼烏斯、羅貝托·皮諾蒂博士等
- 提問者：伍爾西眾議員（女）、巴特利特眾議員、庫克眾議員、基爾派翠克眾議員、葛拉維爾參議員（Senator Gravel，末段提出聯合國決議案）、高華德參議員（seg 620 提及）
- 共 6 個 topic（seg 1–662），drafts 6 檔（18–36KB 皆可整檔讀取）；main.yaml 328KB 須分批或以 grep 查段
- 本集詞彙表（terminology.yaml）部分經 UFO-13/15 校稿回寫（如 CEFAA、孫式立），其餘僅供參考；與主表或既有裁決衝突時從主表／既有裁決
- seg 56 "Will." 語境不明（疑為 Well 之轉錄或稱呼），無音頻可查，照字面譯「威爾」降 medium，未補錄 potential_errors（無把握）

### 跨集沿用裁決（UFO-01～15 已拍板，本集直接沿用）
- 秘魯（Peru，UFO-02/09/10/13 慣例；UFO-13 topic_05 曾用「祕魯」為孤例，不從）
- 資訊自由法（FOIA），首次出現括註縮寫（UFO-01/02 先例），不括英文全名
- 羅伯森調查小組（Robertson Panel，主表）、反 UFO 保密公民組織（CAUS）、FBI 文件庫（The Vault）、國防情報局（DIA）
- 安東尼奧·胡尼烏斯（Antonio Huneeus）、格蘭特·卡麥隆、威爾伯特·B·史密斯、尼克·波普、孫式立（Sun Shili）、羅貝托·皮諾蒂博士
- 伍爾西眾議員（女，稱「伍爾西女士」）、巴特利特眾議員、庫克眾議員、基爾派翠克眾議員、主席女士（Madam Chair）
- 羅伯特·薩巴赫博士（Dr. Robert Sarbacher；原文 Saubacher 為誤拼，UFO-15 定譯）
- 康代因計畫（Project Condign；原文 Condyne/Condine 誤聽，UFO-15 定譯）
- 普羅旺斯特朗（Trans-en-Provence，UFO-15 定譯）、磁鐵計畫（Project Magnet）、定向能武器（非「定向能源武器」）
- 鳳凰山事件（貴陽孟照國事件，網路流通，UFO-15 定譯）
- Top Secret → 最高機密；Cover-up → 真相掩蓋；Disclosure → 真相揭露；Being/Beings → 存有；飛彈（非導彈）；網路；太空；硬體（hardware）
- 報名用《》（《紐約時報》、《華盛頓郵報》，UFO-01/02/03 先例）
- UFO／CIA／FBI 等英文前後空格、年份／數字與中文間空格、千分位半形逗號、括號全形、引號「」

### topics.json 既有 potential_errors（校稿時逐筆核對草稿原文，可能已失效）
- topic_01：seg 57 `releasing siting files`→sighting files【已失效：main.yaml seg 57 原文已正確】
- topic_02：seg 132 Trans Improvance→Trans-en-Provence；seg 149 O'Hara→O'Hare；seg 183 absorb→deflect bullets（裁示語氣存疑，審到再議）
- topic_03：seg 246 Saubacher→Sarbacher；seg 275 Dr. Sheila→Sun Shili；seg 307 Beijing Zoukong→Zuoanmen（待查證）
- topic_04：seg 363 Project Condine→Condign；seg 383 Conventional→Unconventional Flying Objects；seg 390 Penemunde→Peenemünde
- topic_05：seg 398 Mr. Juneyus→Huneeus；seg 484 Dr. Shelley→Sun Shili；seg 493 cursor→Corso；seg 496 Patagon→Pentagon
- topic_06：seg 594 Prime Minister Gary→Gairy；seg 647 Carbocult→cargo cult
- 另：main.yaml seg 415 `grants at the siting files`（topic_05）同 seg 57 誤聽，審 topic_05 時補錄

### 本集重點定譯（逐步累積）
- 巴特利特博士（Dr. Bartlett，主表；本集詞彙表 definition 曾寫「巴特萊特」不從）
- 普羅旺斯特朗（Trans-en-Provence，從 UFO-15；譯稿原「特朗桑普羅旺斯」已改）
- 把 ET 帶回家的技術、act of God＝奇蹟、deep black＝極深層的黑預算（從 UFO-03/04 定譯）
- 智利異常空中現象研究委員會（CEFAA，從 UFO-13 裁決；原文 CEFA 為誤拼）
- 歐海爾機場（O'Hare Airport）、聯邦航空總署（FAA）、《芝加哥論壇報》
- 貝穆德斯將軍（General Bermudez，智利 CEFAA 負責人）
- 電磁效應（electromagnetic effect）、電磁推進（electromagnetic propulsion）、近距離接觸（close encounter）
- 刪節號一律 ……（譯稿原用 ⋯⋯ 已改）
- 威爾伯特（Wilbert Smith 簡稱一律威爾伯特，原文 Wilbur 為誤聽；主表／UFO-15 先例）
- 羅伯特·薩巴赫博士（Dr. Robert Sarbacher，原文 Saubacher 誤拼 seg 256/259/263 補錄；seg 246 原文已正確）
- 《Crash Saucer》書名保留原文（UFO-15 先例；譯稿原《墜毀飛碟》已改）
- 斯坦頓·弗里德曼（Stanton Friedman，從 UFO-02 定譯；譯稿原「史坦頓」已改）
- 加拿大交通部／加拿大交通部副部長（Department of Transport 補「加拿大」限定，UFO-15 先例）
- bodies 譯遺體（無存活語境時）／外星存有遺體（alien bodies，存有原則）
- 中國五案定譯（2026-08-23 人工裁決）：seg 281 沿用 UFO-15 定譯——鳳凰山事件、飛山事件（Faxiang trapeze）、北京曹公事件（Beijing Sokong）、陸溪農場事件（River Forest）；Mayang alien research station 於 UFO-15 無對應，暫保留音譯「馬陽外星研究站事件」待考。seg 307 原文 Beijing Zuoanmen event 依同裁決譯「北京曹公事件」（講者兩集稱呼不一致，main.yaml 原文不改、不補錄）
- 康代因計畫（Project Condign，從 UFO-15；譯稿原「康丁計畫」已改）
- 安東尼奧·胡尼烏斯（原文 Antonio Neus 為 Huneeus 誤聽 seg 353，已補錄）
- 伍德博士（Dr. Judy Wood，9/11 定向能理論；原文僅稱 Dr. Wood，註記身分）
- 赫爾曼·奧伯特教授（Professor Hermann Oberth）、《火箭進入星際空間》（1922）、齊奧爾科夫斯基（Tsiolkovsky）、羅伯特·戈達德（Robert Goddard）
- 保羅·希爾（Paul Hill）、《非常規飛行物體》（Unconventional Flying Objects）
- 羅斯·西格瑪（Rho Sigma，筆名；原文 Ross Sigma）、《以太技術》（Ether Technologies）、佩訥明德（Peenemünde，zh 維基繁中同字）、戈登·庫伯（Gordon Cooper）
- 不明潛水物體（USO）、射頻武器（RF weapons）、迴紋針行動（Operation Paperclip）
- 康登報告（Condon Report）、約翰·亞歷山大上校（Colonel John Alexander）、艾布拉姆森將軍（James Abrahamson，SDI 主任；原文 Abramson 少一字母不改）
- 中國 UFO 研究聯合會／中國 UFO 研究會／世界華人 UFO 聯合會（後者從 UFO-15 定譯）
- 柯索上校（Colonel Corso＝菲利普·科索 Philip Corso，UFO-15 定譯；《The Day After Roswell》作者，書名無通行中譯保留原文）
- 機槍攝影機（gun camera，戰機槍械攝影機；譯稿原「槍砲攝影機」已改）
- 迪克·迪馬托（Dick DiMatto）、伯德參議員（Senator Byrd）、阿爾弗雷德·奧唐納（Alfred O'Donnell）、極光（Aurora，傳聞祕密偵察機代號）
- 格瑞那達決議（Grenada resolution）、蓋瑞總理（Eric Gairy）、聖馬利諾（San Marino）、聯合國外太空事務辦公室、英國皇家學會
- 高華德參議員（Senator Goldwater）、格拉維爾參議員（Senator Gravel，Mike Gravel）
- 聯合國大會（General Assembly）、聯合國安理會（Security Council，譯稿原「安全理事會」已統一）
- 孫式立博士（主席誤讀 Dr. Shelley 照正確姓名譯，UFO-15 先例；main.yaml 舊 notes「孫世力」為筆誤，本集一律孫式立）

### 進度與決策紀錄
- 2026-08-23：校稿啟動，建立本檔；依序處理 topic_01 → topic_06
- 2026-08-23：topic_01 審畢（seg 1–78）。修訂約 20 筆，重點：UFO／CIA／FBI 前後空格全面補齊、年份／數字空格（12 分鐘、1,000 頁、1977/1953 年）、祕魯→秘魯、FOIA 括註改縮寫先例、《紐約時報》《華盛頓郵報》加《》、seg 31 句序重組、seg 56 Will 降 medium、seg 73 uncover 補註、seg 74 破碎句重組。topics.json：seg 57 紀錄失效（main.yaml 原文已正確），新補錄 1 筆（seg 58 Everybody's releasing file files→Nobody's releasing the real files）
- 2026-08-23：topic_02 審畢（seg 79–219）。修訂約 15 筆，重點：巴特萊特→巴特利特（主表）、特朗桑普羅旺斯→普羅旺斯特朗（UFO-15 定譯）、seg 103/104 對齊 UFO-03/04 定譯（把 ET 帶回家、奇蹟、極深層黑預算）、operations→計畫、seg 195 破碎句改寫、seg 205 suggestions→說法、刪節號 ⋯⋯→……。topics.json：seg 132/149/183 紀錄失效（main.yaml 原文已正確），新補錄 2 筆（seg 136 Trans Improvance→Trans-en-Provence、seg 140 CEFA→CEFAA）
- 2026-08-23：topic_03 審畢（seg 220–320）。修訂約 18 筆，重點：威爾伯→威爾伯特統一、交通部補「加拿大」、《墜毀飛碟》→《Crash Saucer》、史坦頓→斯坦頓、bodies→遺體／外星存有遺體、seg 253 補註官方聲明脈絡、seg 299 破碎句降 medium。topics.json：seg 246/275/307 紀錄失效（main.yaml 原文已正確），新補錄 5 筆（seg 248/259 Wilbur→Wilbert、seg 256/259/263 Saubacher→Sarbacher、seg 269 siding→sighting）。查證：鳳凰山事件（孟照國案）發生於黑龍江省五常市鳳凰山（東北），講者 seg 288 稱 northeastern 正確；UFO-15 交接筆記誤記「貴陽」，宜於 UFO-15 檔補正
- 2026-08-23：topic_04 審畢（seg 321–396）。修訂約 14 筆，重點：康丁→康代因計畫（UFO-15 定譯）、國防部補「英國」、胡內斯→胡尼烏斯（seg 353 原文 Antonio Neus 誤聽補錄）、幽浮學→UFO 學、beings→存有（seg 380）、書名《火箭進入星際空間》《非常規飛行物體》、年份／數字空格、seg 335 combat 疑為 contact 降 medium 存疑、seg 345 補 Judy Wood 身分註。topics.json：seg 363/383/390 紀錄失效（main.yaml 原文已正確），新補錄 1 筆（seg 353 Antonio Neus→Antonio Huneeus）
- 2026-08-23：topic_05 審畢（seg 397–577）。修訂約 25 筆，重點：烏內烏斯→胡尼烏斯全面統一（UFO-02 定譯；seg 398/403/439）、seg 407 FBI 被起訴語意修正（原文 file a suit 疑口誤）降 medium、seg 415 grants at the siting files 標記、seg 427 Abramson 補註、seg 459 United States Library 存疑降 medium、gun camera→機槍攝影機（seg 550/556）、MOD 補英國、祕魯→秘魯（seg 553）、UFO／CIA／FBI／FOIA／DNA 空格、年份／數字空格。topics.json：seg 484/493/496 紀錄失效（main.yaml 原文已正確），新補錄 3 筆（seg 409 sitting files→sighting files、seg 415 grants at the siting files、seg 439 Mr. Honest→Mr. Huneeus）
- 2026-08-23：topic_06 審畢（seg 578–662）。修訂約 8 筆，重點：安全理事會→聯合國安理會（seg 655/661）、皮諾提→皮諾蒂（UFO-15 定譯）、孫博士→孫式立博士（seg 616 照正確姓名）、seg 604 移除冗餘括註。topics.json：seg 594/647 紀錄失效（main.yaml 原文已正確），新補錄 3 筆（seg 583 member state of the United States→United Nations、seg 616 Dr. Shelley→Dr. Sun Shili、seg 640 Don't remember→Don't forget）
- 2026-08-23：**全 6 個 topic 審畢（seg 1–662 共 662 段）**。全部 → 行 JSON 驗證通過（662 行 0 錯）、topics.json 合法、殘留掃描（幽浮／意大利／『／【／⋯／千分位／祕魯／烏內烏斯／康丁／巴特萊特／特朗桑／皮諾提／史坦頓／禁用詞）乾淨。累計新補錄轉錄錯誤 15 筆（seg 58/136/140/248/256/259/263/269/353/409/415/439/583/616/640）、既有紀錄失效 15 筆（seg 57/132/149/183/246/275/307/363/383/390/484/493/496/594/647）。人工裁決 1 項：seg 281/307 中國五案名稱沿用 UFO-15 定譯。⚠️ 依收尾流程人工確認門檻：暫停待人工裁決後始得執行 fix_transcription_errors / backfill / export
