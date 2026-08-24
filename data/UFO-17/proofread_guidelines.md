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
  - 歷史背景：`fix_chinese_punctuation.py` 舊版會把數字內半形逗號轉成全形（「4，000」），已於 2026-08-07 修正工具並清理全專案既有污染；校稿時仍可用 `\d，\d` 模式抽查確認
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

（每集自行補充：該集高頻術語與定譯、前任校稿者遺留問題、已查證的事實、特殊格式決定等）

### UFO-17：飛行員與航空專家（Pilots & Aviation Experts）

**核心證人與事件**：
- John Callahan（約翰·卡拉漢，FAA 事故調查部主管）— 1986 JAL 1628 阿拉斯加事件（topic_01、06、07、09）
- Major Filer（費勒少校）— 1962 英國巨石陣 RAF 攔截事件（topic_02、06、07、08）
- Jim Courant（吉姆·庫蘭特，航線機長）— 1995 新墨西哥州目擊（topic_03、06、08、09）
- Lt. Col. Richard French（理查德·弗倫奇中校）— 水下與火山 UFO、鳳凰城光點（topic_04、07）
- Steve Allen（史蒂夫·艾倫，私人飛行員）— 2008 德州斯蒂芬維爾事件（topic_05、07、09）

**前任譯者遺留（TRANSLATION_ISSUES.md，僅供參考）**：
- 已記錄 19 筆轉錄錯誤（含 topics.json 未收錄者：seg 96 Ingen、181 curses、485 Mr. Kallen→Callahan、516 07-47→747、545 Dr. Schreifer→Major Filer），校稿時須核實並補錄至 topics.json 的 `potential_errors`
- 術語調整紀錄：Sighting→目擊事件、transponder→航空應答機、Mount Blanc→法國白朗峰、Kīlauea→夏威夷基拉韋厄火山、Carl Lewis→卡爾·路易斯、TR-3B→TR-3B 三角飛行器
- 特殊處理：cursus（考古學術語，保留原文加註）、cargo cult（貨物崇拜）、mothership→母艦

**校稿進度與決策紀錄**：
（校稿過程中陸續補充）

- **topic_01（2026-08-24 完成）**：
  - 修正 seg 107–139 系統性多餘引號（含 104–106、109–112、114–115、117–118、123–125 改依原文跨段引號結構）
  - seg 122：「Well done」→「接著」（Well then）、「測高設備的對數」→「演算法」（logarithm→algorithm）
  - seg 125：「你們要沒收」→「我們會沒收」（You're→We're，CIA 沒收資料）
  - seg 74 重複語句潤飾；seg 119「現在」→「當時」
  - 全檔機械修正數字/英文與中文間空格（33 行）
  - topics.json 補錄 3 筆 potential_errors（seg 122×2、125）
- **topic_02（2026-08-24 完成）**：
  - seg 166–167 引號改依原文跨段結構
  - seg 173 原文破碎降 medium；seg 191 補譯 twice 並改直譯、降 medium
  - 全檔空格修正（15 行）
  - topics.json 補錄 4 筆 potential_errors（seg 96 Ingen、153 Forth Bridge、181 cursus、187 cargo cult）
- **topic_03（2026-08-24 完成）**：
  - seg 217–220、248–249 引號改依原文跨段結構
  - seg 222 astronauts/cosmonauts 區分譯為美國／蘇聯太空人
  - seg 250「通過那個情況」→「經過那次經歷」並補 notes
  - seg 254 簡體「约」→「約」
  - seg 211 書名補原文括註（Flying Saucers Top Secret）
  - seg 214 補 notes；全檔空格修正（13 行）
  - topics.json 補錄 2 筆 potential_errors（seg 219 Narita、256 Howe）
- **topic_04（2026-08-24 完成）**：
  - 譯文品質良好；seg 287 語序潤飾、seg 293 補 notes
  - 全檔空格修正（8 行）；無新轉錄錯誤
- **topic_05（2026-08-24 完成）**：
  - seg 310、322、381 括註內純英文改用半形逗號
  - 全檔空格修正（7 行）
  - topics.json 補錄 1 筆 potential_errors（seg 378 AWACS 全稱）
- **topic_06（2026-08-24 完成）**：
  - seg 446–447 引號『』改「」；ART CAS 統一「航空防撞系統」
  - seg 458 in so many words 誤譯修正；back-engineered 統一「反向工程」（另 seg 465；topic_08/09 待查）
  - seg 437 時間語序重組降 medium；seg 438 原文殘句標 medium；seg 463、466 潤飾
  - seg 475 查證 LeRoy Gover 為二戰王牌（鷹中隊、5 架擊落），「Triple H」記為轉錄錯誤
  - topics.json 補錄 2 筆 potential_errors（seg 451 Feiler、475 Triple H）
  - 本檔空格已符合慣例，無需修正
- **topic_07（2026-08-24 完成）**：
  - seg 591「30 miles down」改譯為沿航向前方 30 英里（非高度）並加註
  - 全檔空格修正（16 行）
  - topics.json 補錄 3 筆 potential_errors（seg 485 Kallen、516 07-47、545 Schreifer，均核實前人紀錄）
- **topic_08（2026-08-24 完成）**：
  - seg 598 Kilpatrick→基爾派翠克、654 Gravel→格拉維爾（依主表）；664 Danny Sheehan→丹尼爾·希恩
  - seg 671 電影《機長》（Flight）補丹佐·華盛頓；705 John→約翰（應指 Callahan）
  - seg 652 Thayer→經人工確認為 Mr. Chair，改譯「主席先生？」；seg 714 Barrett→經查證小組名單確認為 Bartlett，改譯「巴特利特」
  - seg 604、615、675 補 notes；628 贅字修正
  - topics.json 補錄 3 筆 potential_errors（seg 625 Piler、652 Mr. Chair、714 Barrett）；本檔空格已符合慣例
- **topic_09（2026-08-24 完成）**：
  - seg 719 Kilpatrick→基爾派翠克；761 Coran→庫蘭特；786 Gordon→戈登；832 Rob Simone→羅布·西蒙尼（音譯）
  - seg 765「外星智慧生物」→「外星生命」；seg 751、755 講者重複贅述適度潤飾；seg 814 破碎口語潤飾
  - seg 600、698（topic_08）Jim→吉姆
  - topics.json 補錄 1 筆 potential_errors（seg 828 terror→air traffic control）；本檔空格已符合慣例

### 全部 9 個 topics 審訂完畢（2026-08-24）

- 9 檔 `→` 行 JSON 全數合法；無千分位污染；無簡體字殘留（全檔掃描僅 seg 254 一例已修）
- topics.json 共補錄 **18 筆** potential_errors（含前人紀錄核實與新發現）
- **待人工裁決事項**（全部解決）：
  1. ~~seg 652「Mr. Thayer」~~ → 2026-08-24 人工觀看影片確認為「Mr. Chair」（基爾派翠克保留時間後交還主席），已改譯「主席先生？」，seg 654 同步改為主席請格拉維爾發言的語氣
  2. ~~seg 714「Congressman Barrett」~~ → 2026-08-24 人工確認發言者為 Gravel；查證聽證會小組名單（無 Barrett 成員）確認為 Bartlett，已改譯「巴特利特眾議員」
  3. ~~seg 211 書名~~ → 2026-08-24 人工裁決照字面翻譯，維持《飛碟最高機密》（Flying Saucers Top Secret）
- 依收尾流程，**暫停等待人工確認**後才執行 fix_transcription_errors / backfill / export
