# UFO-05 校稿準則（Proofread Guidelines）

> 本檔案複製自 `configs/proofread_guidelines_template.md`，並在「八、本集專屬事項」補充 UFO-05 特有的術語、已知問題與交接筆記。
> 翻譯階段的風格規範請見 `data/UFO-05/translation_guidelines.md`（兩者職責分立；衝突時以本檔與術語表為準）。

---

## 一、參考資料與優先序

校稿時可參考的文件，衝突時依下列優先序裁決：

1. `configs/terminology_master.yaml` — 跨集術語主表（**最終基準**，人名譯名先查這裡）
2. `configs/terminology_master_rules.yaml` — 主表編輯規則（ deprecated 形式、情境例外）
3. `data/UFO-05/terminology.yaml` — 本集術語表
4. `data/UFO-05/topics.json` — 各 topic 摘要與 `potential_errors`（轉錄錯誤紀錄）
5. 本檔與 `data/UFO-05/proofread_guidelines.md`

## 二、術語與專有名詞原則

### 1. 人名：全部統一中譯
- 主表已收錄者從主表；未收錄者用台灣標準音譯
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
- 括號原文註釋用半形括號（既有格式，例：藍皮書計畫 (Project Blue Book)），保留不動
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

### 譯名裁決（2026-08-09，人工裁決）

**裁決原則**（人工指示）：譯名優先採用**網路上流通的用語**；僅當網路資訊缺乏時才自定義，並以主表確保一致性。

- **James/Jim Penniston → 潘尼斯頓**（詹姆斯·潘尼斯頓／吉姆·潘尼斯頓）：網路流通查證——維基百科 zh-tw「吉姆·潘尼斯頓」、繁中譯文（jgospel）「潘尼斯頓」；主表現行「吉姆·佩尼斯頓」罕見。**草稿維持潘尼斯頓不改**；主表 Jim Penniston 詞條待收尾時修正 preferred_translation 並標註佩尼斯頓為 deprecated
- **Charles Halt → 哈爾特上校**：維基百科 zh-tw「查爾斯·哈爾特」流通，與主表一致；「賀特」僅見單一來源；本集草稿現用「霍爾特」15 處**需改為哈爾特**（全名形式：查爾斯·哈爾特）
- **Bentwaters → 本特沃特斯**：維基百科 zh-tw「本特沃特斯皇家空軍基地」，與主表一致；本集草稿現用「班特沃特斯」9 處**需改為本特沃特斯**（事件名：本特沃特斯事件）
- **Senator McCain → 約翰·麥凱恩參議員**：本集詞彙表誤收「馬侃」，維基百科與 BBC 皆用「麥凱恩」，校稿時修正
- 其餘人名主表已有定譯者從主表：尼克·波普（Nick Pope）、約翰·巴勒斯（John Burroughs）、藍道申森林事件（Rendlesham Forest incident，廢棄譯名「倫德爾沙姆森林事件」）、蓋博上將（General Gabriel）、格拉維爾參議員、胡利眾議員（廢棄「胡利女眾議員」）、基爾派翠克眾議員、羅斯科·巴特利特、梅里爾·庫克、丹·希恩、布克曼博士、資訊自由法（FOIA）、藍皮書計畫、最高機密、真相掩蓋／真相揭露、創傷後壓力症候群（PTSD）、退伍軍人事務部（VA）
- 主表未收錄、暫依本集詞彙表：派翠克·弗雷斯科納（Frescona）、希爾-諾頓勳爵（Lord Hill Norton）、艾德·卡班希克（Kabancik）、巴德·史蒂芬斯（Steffens）、凱爾參議員（Kyl）、詹姆斯·埃克森參議員（Exon）、琳恩·伍爾西（Woolsey）
- **括註風格**（2026-08-09 人工裁決）：**保留**全形括註「中譯（English）」。人工偏好保留以便對照原名；抽樣未校稿集數（UFO-06/07/09/13–20）多數保留括註。另經 git 查證，UFO-01/02/04 於翻譯階段本就幾乎無括註（非校稿時刪除），補註待辦已登記於該三集準則檔。後續各集校稿請保留既有括註，勿刪除
- seg 5「Mike Ravel」轉錄錯誤：main.yaml 已於翻譯階段前修正為 Mike Gravel，topics.json potential_errors 該筆為歷史紀錄，收尾 fix_transcription_errors.py 會自動跳過（無匹配）

### 已知 Whisper 轉錄錯誤（topics.json potential_errors，校稿時留意全數出現處）

- topic_01：Mike Ravel→Mike Gravel（seg 5）
- topic_02：Charles Holt→Charles Halt（seg 11，反覆出現）；Project Bluebird→Project Blue Book（seg 17）
- topic_04：Aria Bentwaters→RAF Bentwaters（seg 44）；Wurundjerum Forest→Rendlesham Forest（seg 47）；Kibansack→Kabancik（seg 48）
- topic_05：transgressional hypnosis→regressional hypnosis（seg 73）；Reynolds Forest→Rendlesham Forest（seg 86）；heart fracture rate→ejection fraction rate（seg 89）；Mr. Polk→Mr. Pope（seg 94）；rendition case→Rendlesham case（seg 113）
- topic_07：Reynolds and Forrest incident→Rendlesham Forest incident（seg 209）；Mr. Franscona→Mr. Frescona（seg 219）；Glomar Challenger→Glomar Explorer（seg 253）
- 本集詞彙表另記：Warsaw Pack→Warsaw Pact（seg 50）

### 本集核心事實備忘（供語意審查）

- 事件：1980 年 12 月 26 日起連續三夜，RAF Bentwaters／RAF Woodbridge 雙基地（美軍第 81 戰術戰鬥機聯隊駐紮）旁的藍道申森林
- 主要證人：詹姆斯·潘尼斯頓（Jim Penniston，技術軍士）、約翰·巴勒斯（John Burroughs）；律師派翠克·弗雷斯科納
- 第三夜：哈爾特上校率隊調查，有著名 17 分鐘現場錄音（Halt tape）與 Halt 備忘錄
- 輻射讀數：英國國防情報人員評估「顯著高於背景值」；解密文件稱達正常值 7 倍
- 麥克斯威爾空軍基地檔案館缺少第 81 聯隊 1980 年 12 月的官方歷史記錄
- Glomar response：源自 CIA 對 Hughes Glomar Explorer 打撈案的「不確認也不否認」回覆

### 進度與交接筆記

- 2026-08-09：建立本檔；譯名裁決完成（見上）。
- topic_01（seg 1–10）：審畢，**0 處修訂**。JSON 驗證通過、無千分位污染與禁用詞殘留。
- topic_02（seg 11–23）：審畢，**9 處修訂**（霍爾特→哈爾特×1、班特沃特斯→本特沃特斯×3、Jim Penniston 改譯吉姆·潘尼斯頓×1、希爾·諾頓→希爾-諾頓勳爵×2、括註內英文逗號改半形×2）。seg 17 原文 Project Bluebird 已於 main.yaml 修正為 Blue Book，譯文未受影響。
- 定譯補充：Jim Penniston → 吉姆·潘尼斯頓、James Penniston → 詹姆斯·潘尼斯頓（視原文形式選用）；希爾-諾頓勳爵用連字號。
- topic_03（seg 24–43）：審畢，**9 行約 20 處修訂**：Bentwaters/Woodbridge 中譯為本特沃特斯／伍德布里奇（seg 26/27/33/34 共 6 處）；霍爾特→哈爾特（seg 38/39）；「詹姆·潘尼斯頓」統一為「吉姆·潘尼斯頓」（原文 Jim，seg 38/40/41/43 共 6 處）；DARPA 改「國防高等研究計畫署」；seg 41 原文 default requests 亂碼改譯並降 medium；seg 43 Mr. Pennington 譯文逕採潘尼斯頓。
- topics.json 補錄 2 筆 potential_errors（topic_03）：seg 34 Kubancik→Kabancik、seg 43 Mr. Pennington→Mr. Penniston（main.yaml 各有原文可匹配）。
- 一致性待查：「classified records section」各 topic 譯法不一（seg 42 機密記錄系統），審至 topic_05/07 時統一。
- topic_04（seg 44–65）：審畢，**3 輪共 8 處修訂**：seg 44 RAF Bentwaters 改「皇家空軍本特沃特斯基地（RAF Bentwaters）」；班特沃特斯→本特沃特斯×4；霍爾特中校→哈爾特中校×3。
- topics.json 的 topic_04 三筆 potential_errors（Aria Bentwaters、Wurundjerum Forest、Kibansack）經查 main.yaml 均已修正，收尾時自動跳過。
- topic_05（seg 66–117）：審畢，**9 行約 12 處修訂**：seg 75 成語直譯「嘴巴掉到桌子底下」改「驚訝得下巴都快掉下來」；seg 77 班特沃特斯→本特沃特斯；seg 91 補 Mr. Frisco 誤轉註記；麥侃→麥凱恩（seg 92/93/94，維基/BBC 標準譯名）；seg 94 通過→透過；seg 96 潘尼斯→潘尼斯頓並擴充 notes；seg 102 大不列顛→英國；seg 106 潤飾語序並降 medium。
- topics.json 補錄 4 筆 potential_errors（topic_05）：seg 91 Mr. Frisco→Mr. Frescona、seg 94 Senator Kyle→Senator Kyl、seg 96 Mr. Penness→Mr. Penniston、seg 100 those boroughs→that Burroughs（皆存在於 main.yaml）。topic_05 原有 5 筆錯誤紀錄經查 main.yaml 均已預先修正。
- 「classified records section」本集暫見兩種譯法：seg 42「機密記錄系統」、seg 91/92「機密檔案區」，審 topic_07 後統一。
- topic_06（seg 118–192）：審畢，**6 行 7 處修訂**：seg 119 補 Mr. Friscona 誤轉註記；seg 128 代詞修正；seg 129 「入伍空軍的地方」語病修正；seg 145 Nassau→NASA 並註記；seg 171 霍爾特中校→哈爾特中校（原文 Charles Holt 殘留，見下）；seg 179 班特沃特斯→本特沃特斯。
- topics.json 補錄 3 筆 potential_errors（topic_06）：seg 119 Mr. Friscona→Mr. Frescona、seg 145 Nassau→NASA、seg 171 Charles Holt→Charles Halt（main.yaml 確認有原文可匹配）。
- topic_07（seg 193–325）：審畢，**12 行 13 處修訂**（含回改 topic_03 seg 42）：機密記錄系統／機密記錄部門統一為「機密檔案區」（seg 231/233/236/237 + topic_03 seg 42）；霍爾特→哈爾特（seg 243/280/312/315 共 5 處）；seg 245 威爾福德醫院→威爾福德廳（與 seg 86 統一）；seg 267 馬侃→麥凱恩。另回改 topic_04 seg 50 介詞「通過」→「透過」（「通過體檢」等動賓用法保留）。
- topics.json 補錄 8 筆 potential_errors（topic_07）：seg 219 siding→sighting、Stephens→Steffens（8 處反覆出現）、seg 220 in the force→in the forest、seg 234 Senator Cowell→Senator Kyl（2 處）、seg 237 identified→unidentified flying object、seg 243 Colonel Hall→Colonel Halt（4 處）、seg 280 Colonel Holt→Colonel Halt（4 處）。topic_07 原有 3 筆（Reynolds and Forrest、Mr. Franscona、Glomar Challenger）經查 main.yaml 均已預先修正。

### 全集聚合（校稿完畢，2026-08-09）

- 7 個 topic 全數審畢：topic_01（0）／topic_02（9）／topic_03（約 20）／topic_04（9）／topic_05（約 12）／topic_06（7）／topic_07（13），合計約 **70 處修訂**，涉及 40+ 個段落行。
- topics.json 累計新補錄 **17 筆** potential_errors（topic_03×2、topic_05×4、topic_06×3、topic_07×8），全部已確認 main.yaml 有原文可匹配；原紀錄中另有 14 筆經查已於翻譯階段前預先修正，收尾時 fix_transcription_errors.py 會自動跳過。
- 全檔機械驗證通過：7 檔 `→` 行 JSON 全合法、topics.json 合法、無千分位污染（`\d，\d`）、無禁用詞殘留（網絡／絕密／核子物理）、無舊譯名殘留（霍爾特／班特沃特斯／馬侃／詹姆[^斯]／潘寧頓／希爾·諾頓）。

### 待人工裁決／收尾事項

1. ~~**主表修正建議**~~：已完成（2026-08-09 人工核准）。`terminology_master_rules.yaml` 新增 jim penniston deprecated 條目；UFO-06/20 詞彙表同步改「吉姆·潘尼斯頓」；主表已重新生成並驗證
2. ~~**本集 terminology.yaml 未回改**~~：已完成（2026-08-09 人工核准）。霍爾特→哈爾特、班特沃特斯→本特沃特斯、馬侃→麥凱恩均已回改，James Penniston 詞條補註 Jim 形式譯法
3. **收尾流程尚未執行**（依人工確認門檻，AI 校稿者不執行）：fix_transcription_errors → backfill → export/split；執行前請先 dry-run 驗證
