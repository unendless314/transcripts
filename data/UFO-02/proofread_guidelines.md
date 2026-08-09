# 校稿準則（Proofread Guidelines Template）

> 本檔案是全 20 集共用的校稿準則模板（由 UFO-01 實務經驗歸納）。
> 每集開始校稿前，複製本檔為 `data/<episode>/proofread_guidelines.md`，並在「本集專屬事項」補充該集特有的術語、已知問題與前任遺留事項。
> 翻譯階段的風格規範請見 `data/<episode>/translation_guidelines.md`（兩者職責分立；衝突時以本檔與術語表為準）。

---

## 一、參考資料與優先序

校稿時可參考的文件，衝突時依下列優先序裁決：

1. `configs/terminology_master.yaml` — 跨集術語主表（**最終基準**，人名譯名先查這裡）
2. `configs/terminology_master_rules.yaml` — 主表編輯規則（ deprecated 形式、情境例外）
3. `data/<episode>/terminology.yaml` — 本集術語表
4. `data/<episode>/topics.json` — 各 topic 摘要與 `potential_errors`（轉錄錯誤紀錄）
5. 本檔與 `data/<episode>/proofread_guidelines.md`

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
  - 歷史背景：`fix_chinese_punctuation.py` 舊版會把數字內半形逗號轉成全形（「4，000」），已於 2026-08-07 修正工具並清理全專案既有污染；校稿時仍可用 `\d，\d` 模式抽查確認
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

### 進度
- [x] topic_01（段落 1–208）已審完，約 30 處修訂；JSON 驗證通過；topics.json 已補錄 4 筆新 potential_errors（seg 181、206、208×2）
- [x] topic_02（段落 209–510）已審完，約 15 處修訂；JSON 驗證通過；topics.json 再補錄 4 筆（seg 213、214、326、448）

### 新增人名／地名定譯（主表未收錄，供後續集數沿用）
- topic_01：Gordon Cooper → 戈登·庫珀；Jacques Vallee → 雅克·瓦萊；Lawrence Coyne → 勞倫斯·科恩；Maurice Bishop → 莫里斯·畢夏普；Lawrence Rockefeller → 勞倫斯·洛克斐勒；Father Bill Davis → 比爾·戴維斯神父；Peter Rodino → 彼得·羅迪諾；Scott Armstrong → 史考特·阿姆斯壯；Alexander Butterfield → 亞歷山大·巴特菲爾德；Poindexter → 波因德克斯特；Brigadier General Carroll → 卡羅爾准將（查證為 Joseph F. Carroll，OSI 首任指揮官 1948–1955）；John Drahos → 約翰·德拉霍斯
- topic_02：Steven Schiff → 史蒂文·席夫；Oliver North → 奧利弗·諾斯；Donald Menzel → 唐納德·門澤爾；Carl Bernstein → 卡爾·伯恩斯坦；Edward Condon → 愛德華·康登；Gerald Ford → 傑拉爾德·福特；Teilhard de Chardin → 德日進；Carroll Bolender → 卡羅爾·博倫德；Pat Robertson → 帕特·羅伯遜
- 地名：Los Alamos → 洛斯阿拉莫斯；Oak Ridge → 橡樹嶺；Jefferson Building → 傑弗遜大樓；DuPont Circle → 杜邦圓環；1717 Mass Ave → 麻薩諸塞大道 1717 號；McCord → 麥科德（McChord）；Gulf Breeze → 微風灣（從本集術語表）；Alamogordo → 阿拉莫戈多；White Sands → 白沙

### 待釐清／遺留
- **收尾待人工執行**（2026-08-08 裁決）：topics.json 已含全部 potential_errors，人工依收尾流程跑 fix_transcription_errors → backfill → export 即可
- 段落 4「Mr. Gillin」：查無此人，暫音譯「吉林先生」，confidence 已降 medium，待有影帶或官方名單再定
- 段落 89 格瑞納達獨立年份：原文 1978，查證實際為 1974-02-07；保留原數字、已標註（不入 potential_errors，不改原文）
- 段落 485「96 名參議員」：實際應為 100 名；保留原數字、降 medium 並標註
- off-the-shelf enterprise（段落 201–202）按 off-the-books（帳外行動）處理並註記

### 已拍板決定
- Dolan 沿用 UFO-01 定譯「多蘭」；Bartlett 沿用「巴特利特」；Friedman 從主表「史丹頓·弗里德曼」；Hooley 沿用「胡利眾議員」
- GAO 統一「美國審計總署」；Uniting for Peace Resolution → 聯合一致促進和平決議
- Whisper 斷句造成的跨段語意（如段落 67/68 的 for the past 37 years）：以字幕流暢為優先併入前段，notes 標註
- 講者自述的 Whisper 誤聽採正確義直接入譯並註記：artful lawyer→liar、were observed→absurd、pie ball→pibal、osteopithecus→australopithecus、drugged→dragged、magic→Majic、McCord→McChord、Marsha→Marcia

### 交接待辦：補上原文括註（2026-08-09 人工登記，由後續校稿者處理）
- **背景**：2026-08-09 人工裁決**譯文應保留「中譯（English）」全形括註**，`configs/proofread_guidelines_template.md` 已明訂此規則；格式可參考 UFO-05 定稿
- **git 查證結果**：經比對校稿前版本（`git show 7ccea6b:data/UFO-02/drafts/`），本集草稿於翻譯階段括註極少（全 2 檔僅 3 處），故本任務為**新增**而非還原；若對個別段落有疑慮，可用 `git log -p -- data/UFO-02/drafts/<file>` 追查該行歷史
- **任務**：於 `data/UFO-02/drafts/` 各檔的定譯中，為重要人名／地名／專有名詞補上原文括註（例：多蘭（Richard Dolan））。僅補重要專有名詞的**首次出現**，無需重複
- **格式**：全形括號；括註內純英文內容用半形標點；只改 `→` 行，JSON 保持單行且合法；編號行與 Speaker Group 標題不動
- **驗證與收尾**：完成後以 `python` 逐行 `json.loads` 驗證並回報人工；若本集尚未回填，括註隨正常收尾流程生效；若已回填／匯出，是否重跑 backfill/export 由人工決定
