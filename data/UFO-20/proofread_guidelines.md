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
4. **音近人名是 ASR 高風險群**（2026-08 UFO-17 案例歸納）：
   - ASR 聲音訊號模糊時傾向輸出「統計上更常見」的詞：名字被轉成另一個讀音相近的既有名字（例：Bartlett→Barrett、Thayer→Chair）時，先懷疑是誤轉錄而非新人物
   - 查證方法：與該集實際出席名單（小組成員、證人）比對——出現的名字對不上任何人即高度可疑，再以人物背景與上下文關聯性（委員會任職、提問內容、發言互動）定案
   - 實例：UFO-17 seg 714「Congressman Barrett」經查證 2013 聽證會小組名單無 Barrett，確認為 Roscoe Bartlett（科學委員會委員、問同類問題）；seg 652「Mr. Thayer」經人工觀看影片確認為「Mr. Chair」（講者交還發言權）
   - Whisper 輸出跨集一致，同一誤聽通常全專案只出現一處；可 grep 變體做跨集掃描確認（例：`grep -ri 'barrett' whisper-medium/ data/*/drafts/`）

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

### 本集背景

UFO-20「Citizen Hearing Closing Remarks」：2013 Citizen Hearing 閉幕集，7 個 topic、167 段：

- **topic_01**（seg 1–10）：開場宣誓、六位小組成員聯名要求 VA 釋出 Jim Penniston／Airman Burroughs 醫療紀錄
- **topic_02**（seg 11–40）：Paul Hellyer 證詞（外星種族、三姐妹影子政府、新美國世紀計畫）
- **topic_03**（seg 41–58）：Richard Dolan 揭露悖論
- **topic_04**（seg 59–73）：Daniel Sheehan 法律觀點（五角大廈文件案、伊朗門、MJ-12）
- **topic_05**（seg 74–95）：小組 Q&A（墜毀飛船數量、三姐妹、卡特總統簡報、憲法危機）
- **topic_06**（seg 96–108）：Hellyer 宣讀 Jim Sparks 外星訊息、赦免方案
- **topic_07**（seg 109–167）：閉幕陳述（格拉維爾、胡利、赫勒、馬賽爾二世）

### 高頻術語定譯（與主表及前集一致）

- 保羅·赫勒、理查德·多蘭、丹尼爾·希恩、吉姆·潘尼斯頓（主表裁決，非佩尼斯頓）、伯勞茲士官、布克曼博士（非醫師）
- 格拉維爾參議員（非格拉韋爾）、胡利眾議員、巴特利特眾議員、伍爾西眾議員、基爾派翠克眾議員（女性，與 UFO-19 一致）
- 真相揭露／真相掩蓋／真相封鎖、最高機密（非絕密）、軍工複合體（主表）、Majestic 12 小組（MJ-12）
- Being/beings → 存有（全檔統一）；George H.W. Bush 依語境雙譯：CIA 局長語境「喬治·H·W·布希」（主表）、總統語境「老布希總統」
- Honorable → 閣下；national security state → 國家安全體制（state 指體制非狀態）

### topics.json 既有 potential_errors 查對結果

既有 14 筆（topic_01 ×2、topic_02 ×3、topic_04 ×2、topic_05 ×4、topic_06 ×1、topic_07 ×2）之 main.yaml 原文**均已於轉錄修正階段套用**（與 UFO-19 同類 corrections_applied），草稿原文行反映正確拼寫，譯文均已對應。

### 校稿進度與決策紀錄（2026-08-24）

- **原文行中譯殘骸還原 3 段**（翻譯階段污染，依 main.yaml 還原）：seg 24（intellectual 精英…整段）、seg 55（power 精英）、seg 84（from 各位。）
- **校稿補錄 topics.json potential_errors 6 筆**：seg 14 Linda Bolton Howe→Linda Moulton Howe；seg 54 Investors→Investigators；seg 57 searchers→researchers；seg 83 Paul Heller→Hellyer；seg 97 Minister Heller→Hellyer；seg 112 Dr. Buckman→Bookman。加計既有 14 筆共 20 筆
- **譯文錯置修復**：seg 24/25 譯文互相重複錯置，重寫；seg 62/63、seg 70/71（聯合國大會斷裂重複）、seg 104/105 越界內容修正；seg 69/72 誤置開引號清除
- **術語修正**：seg 9 佩尼斯頓→潘尼斯頓；布克曼醫師→博士（seg 9/74/88/112）；seg 119 絕密→最高機密；seg 118 軍事工業複合體→軍工複合體；seg 120/147/149 格拉韋爾→格拉維爾；seg 145 基爾帕特里克→基爾派翠克（並改「她」，Carolyn Kilpatrick 為女性）；seg 61 Bush 改 CIA 局長語境定譯「喬治·H·W·布希」；seg 132 《世界大戰》書名號；seg 65 MJ-12 改主表格式 Majestic 12 小組（MJ-12）
- **語意修正**：seg 20/21 本世紀末→這個十年（decade，seg 20 降 medium 加註）；seg 23 all three 補回；seg 47 agenda 贅語；seg 50 Never mind the fact→更何況；seg 58 ethics 漏譯補回；seg 92 extra constitutional≠違憲；seg 129 so darn many「該死的」→多得驚人；seg 134 質量→品質；seg 163 一萬億分之一→兆分之一；seg 102 妳們→你們
- **格式**：全檔數字／英文與中文間空格（約 30 行）；簡體字修正 4 處（seg 38 学、seg 92/95 确、seg 130 们）；透過／通過釐清（seg 18/38/136 改透過，seg 115/148 合法動賓保留）
- **降 medium 1 段**：seg 20（We have it best until the end of this decade 語意含糊；seg 91 經看片確認後已回升 high）

### 人工看片確認紀錄（2026-08-24）

校稿者提出 4 段建議人工確認，人工比對影片後裁決如下：

- **seg 20（00:09:36–00:10:45）**：無轉錄錯誤，語意含糊屬講者原話特性，譯文維持、註記已更新
- **seg 54（00:31:38–00:31:57）**：音檔實為 **Citizens**（非校稿者推測的 Investigators，亦非原文 Investors；人工判斷不似單純音近誤轉錄）。topics.json 修正建議已更新，譯文改「公民」
- **seg 91（00:53:48–00:54:10）**：講者實際說完 "We have a democratic process" 後群眾即鼓掌，**無富蘭克林引語**；結尾 "But we are a republic, Benjamin Franklin asked." 為 Whisper 於掌聲段產出的幻覺文字。topics.json 補錄 2 筆（刪除幻覺句、We are→We have），譯文刪句並回升 high
- **seg 157（01:37:52–01:38:49）**：**Carol Rosin**（卡羅爾·羅辛，UFO-19 定譯）、**Bob Salas**（鮑勃·薩拉斯，即 UFO-07 證人羅伯特·薩拉斯上尉）。topics.json 補錄 2 筆，詞彙表兩條「待確認」詞條已改正確，segments 並修正 159→157

校稿補錄 potential_errors 共 **10 筆**（看片前 6 筆：seg 14、54、57、83、97、112；看片後新增 4 筆：seg 91 ×2、seg 157 ×2；其中 seg 54 之建議修正經看片更新為 Citizens），加計既有 14 筆，topics.json 現共 **24 筆**。

### 全部 7 個 topics 審訂完畢（2026-08-24）

- 167 個 `→` 行 JSON 全數合法；段落編號 1–167 連續無缺漏
- 殘留掃描：無千分位污染、無「妳／網絡／絕密／核子物理／信息」殘留；「質量」僅 seg 163 物理質量合法保留；「通過」僅 seg 115/148 合法動賓用法；無簡體字殘留；音效標記全形統一
- **待人工裁決事項**：無。校稿者提出之 4 段看片確認（seg 20、54、91、157）均已結案，見上方「人工看片確認紀錄」
- 依收尾流程，**暫停等待人工確認**後才執行 fix_transcription_errors / backfill / export
