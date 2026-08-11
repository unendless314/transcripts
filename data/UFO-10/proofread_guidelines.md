# 校稿準則（UFO-10：Documents & Proof）

> 本檔案由 `configs/proofread_guidelines_template.md` 複製而來，第八節為本集專屬事項。
> 翻譯階段的風格規範請見 `data/UFO-10/translation_guidelines.md`（兩者職責分立；衝突時以本檔與術語表為準）。

---

## 一、參考資料與優先序

校稿時可參考的文件，衝突時依下列優先序裁決：

1. **網路流通慣用譯名** — 人名／地名／專有名詞先查網路流通譯名（維基百科 zh-tw、主流媒體等）；有流通者從流通譯法
2. `configs/terminology_master.yaml` — 跨集術語主表（預設參考；網路無流通資訊時以主表確保跨集一致性）
3. `configs/terminology_master_rules.yaml` — 主表編輯規則（ deprecated 形式、情境例外）
4. `data/UFO-10/terminology.yaml` — 本集術語表
5. `data/UFO-10/topics.json` — 各 topic 摘要與 `potential_errors`（轉錄錯誤紀錄）
6. 本檔

⚠️ **主表並非絕對權威**：主表由各集詞彙表自動彙整生成，部分集數詞彙表未經校稿，詞條可能與網路流通慣用不合（實例：2026-08 UFO-05 校稿發現主表 Jim Penniston 譯「吉姆·佩尼斯頓」，網路流通實為「潘尼斯頓」，經人工裁決修正）。發現主表與網路流通衝突時，**不得盲從主表，也不得逕自改用其他譯名**，應暫停回報人工裁決；裁決後回寫 `terminology_master_rules.yaml` 與相關各集詞彙表，並以 `build_terminology_master.py --force` 重建主表。

## 二、術語與專有名詞原則

### 1. 人名：全部統一中譯
- 譯名先查網路流通慣用（見第一節優先序）；主表已收錄且與流通一致者從主表；網路無流通者用台灣標準音譯
- 同句重複出現時，第二次可簡稱姓氏
- 全名與簡稱形式（例：弗里德曼／史丹頓·弗里德曼）須跨 topic 保持一致
- 注意中譯同音歧義：必要時改用姓氏或調整句式

### 2. 公司／機構名
- 知名縮寫保留原文：CIA、NSA、FBI、DIA、NRO、HBO、MUFON、RCMP 等
- 其餘中譯（依主表；主表未收錄者查維基百科標準譯名，音譯採用台灣慣用形式）
- 軍事基地全中譯（專案慣例）：萊特-帕特森、柯特蘭、霍洛曼、內利斯、愛德華茲空軍基地
- 媒體/節目名保留原文：Coast to Coast AM、earthfiles.com、majesticdocuments.com 等
- 書籍/報告名：已有通行中譯者用中譯，無者保留原文

### 3. 關鍵術語定譯
- Top Secret → 最高機密（非「絕密」）；Secret → 機密；Confidential → 密
- Cover-up → 真相掩蓋；Disclosure → 真相揭露
- Being/Beings → 存有（「非人類存有」）；non-humans 統一
- Roswell → 羅斯威爾（地名與事件皆中譯，不保留原文）
- 核物理學家（非「核子物理學家」）、藍皮書計畫（非 Blue Book 計畫）
- need to know → 需知原則

## 三、Whisper 轉錄錯誤處理

原文 WER 約 5–10%，**不可將轉錄視為絕對事實**。

1. **高信心拼寫／同音錯誤**（專有名詞、技術詞）：
   - 譯文直接採用正確拼寫
   - notes 註明「原文 X 應為 Y」
   - 同時在 `topics.json` 該 topic 的 `potential_errors` 補一筆（segment_id / error_text / suggested_correction / reasoning），供收尾時 `fix_transcription_errors.py` 修正 main.yaml 原文
   - ⚠️ 同一誤聽常在多段重複出現，務必全數補錄
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
- **數字千分位用半形逗號**：`4,000`、`10,000`、`1,000 萬`（可用 `\d，\d` 模式抽查）
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
- **直譯成語誤用**：不可逐字直譯英文慣用語
- **前後矛盾**：注意同一主題前後段落譯法一致
- **語境判斷**：文件／機密等級語境的用詞須精確
- **原文句構破碎**（Whisper 常見）：譯文補足語意，notes 標記，confidence 視情況降 medium
- 講者口語重複、贅字可適度潤飾，但不可增減事實資訊

## 七、作業流程

1. 閱讀順序：本檔 → `terminology.yaml` → `topics.json` → 前一個 topic 的定譯（保持一致）
2. 大檔（>50KB）分段讀取、分段審訂
   - 有疑慮時可比對 git 歷史：`git log -p -- data/UFO-10/drafts/<file>` 或 `git show <commit>:<path>`；需要還原被改動的內容時以 git 歷史為準，勿憑記憶補寫
3. 每修完一檔立即驗證：
   - 全部 `→` 行 JSON 合法（python 逐行 `json.loads`；本機 `python3` 是假 stub，用 `python`）
   - Grep 掃殘留：`\d，\d`（千分位污染）、原文人名、`網絡|絕密|核子物理|通過`
4. 更新交接筆記（進度、修訂數、新發現、已拍板決策）：**一律寫入本檔「八、本集專屬事項」**，嚴禁在 drafts/ 放置任何筆記或說明檔（backfill_translations.py 會 glob 解析 drafts/ 內全部 `*.md`）
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

### 本集概況
- 主題：洩密政府文件與 MJ-12（Documents & Proof）；證人：鮑勃·伍德博士（Dr. Bob Wood）、史丹頓·弗里德曼（Stanton Friedman）、加拿大研究者（推定 Grant Cameron）、麥可·格雷維爾參議員（Senator Mike Gravel）等
- 草稿 5 檔：topic_01（63 個 → 行）、topic_02（36）、topic_03（50）、topic_04（93）、topic_05（**91KB、470 個 → 行，大檔，務必分段讀取審訂**）
- 本集大量「文件名稱」與「機密等級」用語，譯法須前後一致

### topics.json 既有 potential_errors（校稿時須處理）
- topic_01：seg 55 `polygraph device` → Autopen device；seg 63 `Dr. Wilkins` → Dr. Wood（主席口誤）
- topic_02：seg 82 `Homo sapien` → Homo sapiens
- topic_04：seg 166 `Senator Graval's` → Gravel's；seg 197 `Stanton Freeman` → Stanton Friedman
- topic_05：seg 321 `Staten Friedman` → Stanton Friedman（⚠️ 此筆紀錄掛在 topic_04 條目下但 seg 321 屬 topic_05 範圍，處理時注意）；seg 454 `Congresswoman Kayle Patrick` → Carolyn Cheeks Kilpatrick；seg 542 `Eric Gehry` → Eric Gairy；seg 686 `Congressman Hoolie` → Congresswoman Darlene Hooley

### 本集重點定譯（依 terminology.yaml，校稿中如有增刪修訂回寫此節）
- SOM 1-01 手冊（Majestic 12 技術行動手冊）；口語 SOM 101 亦照此處理
- Majestic 12 / MJ-12 / Magic 12 代號保留原文
- 《外星實體、科技回收與處置》（Extraterrestrial Entities in Technology, Recovery and Disposal）
- 最高機密 Magic Eyes Only
- 不明飛行物體（UFOBs）、外星生物實體（EBE）／（E-B-E-S）
- 需知原則（need to know）
- 磁鐵計劃（Project Magnet，加拿大）、威爾伯特·B·史密斯（Wilbert B. Smith）、最高機密備忘錄（Top Secret Memo）
- 洛克菲勒倡議（Rockefeller Initiative）、柯林頓總統圖書館
- 羅斯威爾事件、洛杉磯之戰（Battle of LA）、巴西瓦爾吉尼亞（Varginha）
- 聯合國大會／聯合國安理會（Senator Gravel 倡議國際會議）

### 進度與決策紀錄
- 2026-08-12：校稿啟動，依序處理 topic_01 → topic_05
- [x] topic_01（17 處修訂）：弗里德曼譯名統一「史丹·弗里德曼」（原「史丹頓·佛烈德曼」，主表與 UFO-01/02/09 皆「弗里德曼」）；導彈→飛彈（seg 12/49，UFO-07/09 裁決）；英文人名補中譯＋括註：豪女士（Linda Moulton Howe）、胡利眾議員（Darlene Hooley）、伍爾西眾議員（Lynn Woolsey）、麥卡特先生（McCarter）、提姆·庫珀（Tim Cooper）、萊恩（Ryan）、琳達·豪、斯特林菲爾德補括註、唐·伯林納補括註；**人工裁決：question documents → 「質疑文件」**（seg 15/49/54/56/57）；seg 39 Whisper 破碎句構重寫降 medium；seg 48 補註句構破碎；seg 55/63 notes 改寫（topics.json 紀錄失效，main.yaml 原文早已正確）
- ⚠️ 本集 topics.json 原有 9 筆 potential_errors 經查 main.yaml 原文皆已是正確拼寫，屬失效紀錄（同 UFO-09 收尾案例），收尾時標記、不執行 fix_transcription_errors
- [x] topic_02（6 處修訂）：Gravel→格拉維爾參議員（Mike Gravel）補括註；布什→布希博士並補括註（Dr. Vannevar Bush）；福萊斯特補括註（James V. Forrestal）；千分位 2,000／7,000；seg 82 notes 改寫（Homo sapiens 紀錄失效）
- [x] topic_03（11 處修訂）：佛烈德曼→弗里德曼（seg 100/101/143）並補括註（Stanton Friedman）；布什→布希（seg 111/118）；知密權→需知權限（seg 118/119/147，知密權為 deprecated 形式 UFO-03 已標記）；磁氣動力學→磁空氣動力學（magneto aerodynamics）；《天空與望遠鏡》補括註；里科弗上將補括註；**新發現轉錄錯誤 seg 126 Truman-Forestall→Truman-Forrestal，已補錄 topics.json**
- [x] topic_04（13 處修訂＋topics.json 補錄 8 筆）：Gravel→格拉維爾（seg 166/172，seg 166 紀錄失效）；洛克菲勒倡議／柯林頓總統圖書館／最高機密備忘錄補括註；佛烈德曼→弗里德曼（seg 197 紀錄失效、seg 206 真實錯誤）；布什→布希（seg 218）；Bartlett→巴特利特先生補括註；威爾伯→威爾伯特·史密斯（seg 227/229，原文 Wilbur 誤拼）；Wright→賴特補括註。**新發現轉錄錯誤補錄 topics.json：seg 172 Mr. Graval、seg 206 Stanton Freeman、seg 227/229 Wilbur Smith、seg 181/182/183/185 siting→sighting files，共 8 筆**
- [x] topic_05（91KB 大檔、470 → 行，分 4 段讀取審訂；16 處修訂＋topics.json 補錄 4 筆）：佛烈德曼→弗里德曼（seg 245/321）；Kilpatrick→基爾派翠克眾議員補括註（seg 454）；Hooley→胡利眾議員（seg 686）；知密權→需知權限（seg 354）；B 計劃→B 計畫（seg 577）；seg 261「evidence of 36」語意不明降 medium；seg 363 bodies dead and alive 矛盾修正（遺體→死亡或仍存活的實體）、seg 382 bodies→實體；洛杉磯之戰／跨行星現象研究小組／巴西瓦爾吉尼亞／華倫·克里斯多福補括註；威爾伯→威爾伯特（seg 373/385）；弗里曼→弗里德曼（seg 499）。**新發現轉錄錯誤補錄 topics.json：seg 373/385 Wilbur Smith、seg 499 Dr. Freeman、seg 614 siting files，共 4 筆**；seg 454/542/686 notes 改寫（topics.json 紀錄失效）

### 總檢查（2026-08-12）
- [x] 全部 712 個 → 行 JSON 合法；topics.json 合法
- [x] git diff 無非 → 行異動（5 檔皆然）
- [x] 殘留掃描零命中：`\d，\d`、佛烈德曼、布什、導彈、威爾伯·、網絡／絕密／核子物理；「知密權」僅 1 處為 topic_03 seg 118 notes 內說明 deprecated 之引用，屬刻意保留
- [x] 譯文（括註外）無英文人名殘留

### potential_errors 總結（收尾用）
- **失效紀錄 9 筆**（原有紀錄全數；main.yaml 原文早已正確，fix_transcription_errors 不會匹配）：topic_01 seg 55/63、topic_02 seg 82、topic_04 seg 166/197/321（其中 seg 321 屬 topic_05 範圍，紀錄掛錯條目）、topic_05 seg 454/542/686
- **真實待修 13 筆**（校稿中補錄）：seg 126 Truman-Forestall；seg 172 Mr. Graval、206 Stanton Freeman、227/229 Wilbur Smith、181/182/183/185 siting files；seg 373/385 Wilbur Smith、499 Dr. Freeman、614 siting files

### 收尾狀態
⚠️ 全 5 topic 審畢，**暫停待人工確認**。確認後始得執行 fix_transcription_errors.py（先 --dry-run）→ backfill → export 等收尾流程。
