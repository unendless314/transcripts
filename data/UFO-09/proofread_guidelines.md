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

### 本集概要
UFO-09「Associated Phenomena」：四位證人證詞＋委員會 Q&A。證人：Peter B. Davenport（國家UFO報告中心）、Peter Robbins（UFO嘲諷現象／蘭德沙姆森林）、Gary Heseltine（英國退休警探，PRUFOS資料庫）、Linda Moulton Howe（動物肢解現象）。

### Topic 分段
- topic_01（seg 1–161）：Davenport 證詞
- topic_02（seg 162–215）：Robbins 證詞
- topic_03（seg 216–292）：Heseltine 證詞
- topic_04（seg 293–385）：Howe 證詞
- topic_05（seg 386–833）：委員會 Q&A（108K 大檔，分批處理）

### 高頻術語定譯（本集詞彙表）
- 鳳凰城光點事件（Phoenix Lights）
- 歐海爾機場事件（O'Hare Airport case）
- 蘭德沙姆森林事件（Rendlesham Forest）
- UFO嘲諷現象（UFO ridicule factor）
- 真相掩蓋（cover-up）／真相揭露（disclosure）／真相封鎖（truth embargo）
- PRUFOS資料庫、英國運輸警察、加拿大皇家騎警（RCMP）
- 《詭異收穫》（A Strange Harvest）、熟化血紅素（cooked hemoglobin）、凝固性壞死（coagulative necrosis）、基因收穫（genetic harvest）

### 已知 Whisper 轉錄錯誤（topics.json potential_errors，收尾補錄）
| seg | 誤 | 正 |
|-----|----|----|
| 75 | Cartourette, New Jersey | Carteret, New Jersey |
| 250 | Arief North Alton Middlesex | RAF Northolt, Middlesex |
| 292 | Ms Hall | Ms Howe |
| 367 | Lynn Lauber | Len Lauber |
| 371 | Sheriff Tech's graves | Sheriff Tex Graves |
| 387 | Mr. Hickerton | Mr. Heseltine |
| 468 | Congresswoman Wilsey | Congresswoman Woolsey |
| 661 | Mr. Hilton | Mr. Heseltine |
| 676 | Mr. Haysclan | Mr. Heseltine |
另：Heseltine 全集多次誤拼 "Hazeltine"；Colonel Halt 曾誤拼 "Charles Holt"；PRUFOS 誤拼 "Proof Force Police Database"。

### 校稿進度
- [x] topic_01（7 處修訂：seg 50 標點、seg 59 elk→加拿大馬鹿、seg 79 沃爾多夫／安德魯斯基地關係、seg 110 潤飾、seg 138 flag officers 口誤處理、seg 80/94 型號空格）
- [x] topic_02（5 處修訂：seg 182/210 破碎句構補足、seg 190 FOIA 用詞、seg 200 潤飾、seg 207 Hill-Norton 重寫——上議院貴族非 MP，降 medium）
- [x] topic_03（4 處修訂＋topics.json 補錄 seg 228 Charles Holt→Halt、seg 234 Proof Force→PRUFOS；seg 246/250 補括註）
- [x] topic_04（7 處修訂＋topics.json 補錄 seg 368 Lynn→Len Lauber；seg 300 括註半形標點、seg 309 半形逗號、seg 355 四季豆、seg 367/368 勞伯統一、seg 376 they're、seg 379 數據→資料）
- [x] topic_05（約 20 處修訂＋topics.json 補錄 seg 455/581/619/621/811/813；重點：seg 417 十億、seg 455/468 伍爾西、seg 556-567 implication→意涵、seg 581 海絲汀、seg 621 潘尼斯頓、seg 710 賴希、seg 721/722/736 The Times→紐約時報、seg 809 太空人、seg 811 薩拉斯＋洲際彈道飛彈、seg 813 Dugway、seg 831 真相封鎖、多處補括註）
- [x] 總檢查：全部 `→` 行 JSON 合法；`\d，\d`、網絡／絕密／核子物理、導彈／宇航員／酒店殘留皆為零

### 已拍板決策與新發現
- Gary Heseltine 譯「蓋瑞·海絲汀」：網路查無流通中譯，採台灣標準音譯維持原譯（2026-08-11 人工裁決確認）
- 伍爾西（Lynn Woolsey）：網路流通譯名（大紀元等作「伍尔西」），原譯「沃爾西」修正
- 威廉·賴希（Wilhelm Reich）：流通譯名「賴希」，原譯「萊希」修正
- Len Lauber 統一譯「連恩·勞伯」（原譯「蘭·勞伯」，seg 367/368）
- Jim Penniston 依主表改「潘尼斯頓」（UFO-05 人工裁決案）；Captain Solace 考訂為 Salas，依 UFO-07/08 定譯「薩拉斯」
- elk（北美 wapiti）定譯「加拿大馬鹿」；string beans 譯「四季豆」；cosmonauts 譯「俄國太空人」
- ⚠️ 失效 potential_errors（main.yaml 原文早已改正，收尾 fix_transcription_errors 不會匹配）：seg 292（Ms Hall）、367（Lynn Lauber）、371（Tech's graves）、387（Hickerton）、468（Wilsey）、661（Hilton）、676（Haysclan）
- ⚠️ 有效 potential_errors（main.yaml 原文仍存在）：75、228、234、250、368、455、581、619、621、811、813
- 「通過」殘留 4 處（topic_04 seg 328/340、topic_05 seg 464/623）經審為動賓手段用法（類「通過電話」），依準則保留
- 「統計數據」2 處（topic_03 seg 243、topic_05 seg 387）為台灣通用複合詞，保留
- seg 207/210/182 等 Whisper 破碎長句採「依史實／脈絡補足＋confidence 降 medium」處理
- 英呎／英尺：本集統一用「英呎」（全專案 英呎 57 vs 英尺 18），維持現狀

### 狀態
全部 5 topic 審畢，**已達人工確認門檻**——待人工核可後始得執行收尾流程（fix_transcription_errors → backfill → export）。
