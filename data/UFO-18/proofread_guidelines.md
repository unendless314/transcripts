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

（每集自行補充：該集高頻術語與定譯、前任校稿者遺留問題、已查證的事實、特殊格式決定等）

### UFO-18：真相封鎖（The Truth Embargo）

**核心證人與事件**：
- 匿名證人（前美國陸軍密碼學家、CIA 幹員）— 1958 年藍皮書計畫與艾森豪威爾派遣的 51 區／S-4 任務（topic_01，預錄訪談）
- Linda Moulton Howe（琳達·莫爾頓·豪，調查記者）— 證實匿名證人證詞、1947 年杜魯門政府確立的「真相封鎖」政策、動物肢解案件與 FOIA 訴訟（topic_02、05）
- Richard Dolan（理查德·多蘭，歷史學家）— 「脫離文明」理論、黑預算與軍工複合體分析（topic_03、05）
- Jeffrey Torres（傑佛瑞·托雷斯）— 代父作證：父親米爾頓·約翰·托雷斯少校 1957 年英國 RAF Manston F-86D 攔截事件、遭 NSA 封口 50 餘年（topic_04、05）

**topics.json 既有 potential_errors（13 筆，翻譯階段已產出）**：
- topic_01：seg 25 Fort Belleville→Fort Belvoir；seg 50 river's/recurse gravity→reversing gravity；seg 83 Linda Motenhouse→Linda Moulton Howe
- topic_02：seg 92 Linda Motenhouse；seg 100 pro words→code words
- topic_03：seg 108 Jim Carant→Jim Courant；seg 110 dum-dum media→dumbed-down media
- topic_04：seg 127 Florida National University→Florida International University
- topic_05：seg 156 RAF Manson→RAF Manston；seg 200 Paul Hales→Paul Hill；seg 204 Stan and Friedman→Stanton Friedman、Paul LeVoillet→Paul LaViolette、lecture gravatics→electrogravitics；seg 205 cloak of frequency→cloak of secrecy；seg 208 ideology→etiology

⚠️ 注意：topic_01 的 seg 50 有兩筆同段錯誤，收尾跑 `fix_transcription_errors.py` 前需確認工具能處理同段多筆。另 seg 25 與 seg 83/92 的錯誤可能同時存在於 main.yaml 原文與譯文括註，校稿時譯文應直接採用正確拼寫並核對括註。

**本集詞彙表重點定譯**（詳見 `terminology.yaml`）：
- Truth Embargo → 真相封鎖（與 cover-up「真相掩蓋」區分）
- Area 51 → 51 區、S-4 設施、Papoose Mountain → 帕普斯山
- Breakaway civilization → 脫離文明；MJ-12 保留原文
- 灰人／金髮族／爬蟲人（三種外星種族）
- electrogravitics → 電重力學、field propulsion → 場推進、reversing gravity → 反轉重力
- Miguel Alcubierre → 米格爾·阿庫別瑞；Stanton Friedman → 史丹頓·弗里德曼；Paul LaViolette → 保羅·拉維奧萊特；Paul Hill → 保羅·希爾
- Jim Courant → 吉姆·庫蘭特（UFO-17 亦出現，跨集一致）
- Nick Pope → 尼克·波普；Daniel Inouye → 丹尼爾·井上；Harrison Schmitt → 哈里森·施密特（Schmitt 非 Schmidt）
- 艾森豪威爾總統、杜魯門總統、尼克森副總統、J·埃德加·胡佛
- 貝爾沃堡基地（Fort Belvoir）、曼斯頓皇家空軍基地（RAF Manston）、柯特蘭空軍基地

**前任譯者遺留**：
- UFO-18 資料夾無 TRANSLATION_ISSUES.md，無前任校稿紀錄

**校稿進度與決策紀錄**：
（校稿過程中陸續補充）

- **topic_01（2026-08-24 完成）**：
  - 匿名證人經查證為男性（後續研究指認為 Oscar Wayne Wolff，2013 聽證會前預錄），全檔 33 處誤用「妳」全改「你」（全專案慣例亦統一用「你」）
  - seg 54 原文行遭翻譯階段截斷並混入譯文 JSON 殘骸（main.yaml seg 54 原文完整、backfill 時被標 pending），已依 main.yaml 還原原文行並補足譯文
  - seg 22 上司自我介紹改間接敘述；seg 43「這週，下週」改「在接下來這一週內」；seg 46 車庫門開口潤飾；seg 71「飛回通勤飛機」改「搭乘通勤飛機返回」；seg 74 OSS 首次出現補中譯「戰略情報局（OSS）」
  - seg 48 原文破碎（疑 walk 誤轉錄為 rock），重組譯文並降 medium
  - 全檔數字／英文與中文間空格修正（seg 13、18、35、36、42、44、46、48、50、67、81）
  - topics.json 補錄 2 筆 potential_errors（seg 42 in→with Nixon、seg 48 rock→walk）
- **topic_02（2026-08-24 完成）**：
  - seg 99、103 原文行遭翻譯階段截斷並混入譯文 JSON 殘骸（backfill 標 pending），已依 main.yaml 還原完整原文行並從殘骸重組譯文
  - 《奇異的收穫》依主表與 UFO-01 定譯改《詭異收穫》（seg 100、102）
  - Harrison Schmidt→Schmitt 拼寫修正（seg 100×2、101，參議員正確拼寫）
  - seg 97 補譯 after you left、引號內「妳」改「你」（威脅者對男性證人）；seg 92、101「妳」改「你」（全專案慣例）
  - seg 95 軍事掩護句重組；seg 100 語序重組；seg 104「互相勾結」改「相互連結」（interlinked）；seg 105 括註改半形逗號（Suitland, Maryland）；seg 103「ground saucer watch」括註改正確大小寫（Ground Saucer Watch）
  - 全檔數字／英文與中文間空格修正
  - topics.json 補錄 2 筆 potential_errors（seg 100 Harrison Schmidt、seg 101 Senator Schmidt）
- **topic_03（2026-08-24 完成）**：
  - seg 108 吉姆·庫朗→吉姆·庫朗特（本集詞彙表與 UFO-17 定譯）
  - seg 115「掩蓋行動」→「真相掩蓋」（cover-up 定譯）、「其他生命體」→「其他存有」（beings 定譯）
  - seg 120「非人類智慧生命」→「非人類智慧體」（與 UFO-09 intelligences 定譯一致）
  - seg 122「他說對了」→「他確實察覺到了什麼」（He was on to something）
  - seg 110 金·卡戴珊經查證為維基百科條目名（網路流通譯名），保留並補 notes
  - 全檔數字／英文與中文間空格修正（seg 108–113、121、122）
  - 無新轉錄錯誤（seg 108 Jim Carant、110 dum-dum media 前人已補錄）
- **topic_04（2026-08-24 完成）**：
  - seg 125 aerospace engineering 改「航太工程」；air medals 改「航空勳章」（Air Medal）並補 notes
  - seg 128／129 譯文重複修正（尼克·波普將此事解密只留 seg 128，seg 129 改譯「波普，來自英國」）；seg 129 補 notes：講者稱 Nick Pope 為國防部長與事實（英國國防部 UFO 事務官員）不符，依原文直譯
  - seg 138 原文 'an ordinary aircraft could do' 依語境應為 couldn't do（譯文已正確），補 notes；topics.json 補錄 1 筆 potential_errors
  - seg 141 艾德嘉·米切爾→艾德加·米切爾（維基百科條目名）；seg 141／142 斷句還原（「有很多人，包括我的家人…」移回 seg 142）
  - 全檔數字／英文與中文間空格修正（seg 124、125、128、129、131、135、138、139、141）
- **topic_05（2026-08-24 完成）**：
  - seg 143「Senator Grovel」經查證 2013 聽證會小組名單（Mike Gravel 在列）改「格拉維爾參議員」（與 UFO-17 定譯一致）
  - seg 204「Representative Fire」初判為 Representative Bartlett，經人工觀看影片推翻：實為交叉對話（Cook 交棒、對方接話 All right），「Fire」為疊音誤轉錄，最終譯文以刪節號呈現交棒語句
  - seg 204「Thomas Vallone」→托馬斯·瓦隆（Thomas Valone，電重力學研究者）
  - seg 186 語意反轉修正（keep…from the press＝對媒體隱瞞）；seg 189「he came to me as a reporter」改「找到了身為記者的我」；seg 214「We would have leaked…」改「若是蘇聯的，我們早就大肆宣揚了」
  - seg 180、187 non-humans 統一「非人類存有」；seg 151 intelligences 改「智慧體」（UFO-09 定譯）；seg 195 aerospace engineering 改「航太工程」（與 seg 125 一致）
  - seg 164 tinfoil hat 與 seg 110「錫箔帽陰謀論」看齊；seg 167 社交媒體→社群媒體；seg 202《星際迷航》→《星際爭霸戰》（台譯）
  - seg 207 公司名改「羅斯科·巴特利特聯合公司（Roscoe Bartlett and Associates）」、captive Navy contractor 改「海軍的專屬承包商」
  - 全檔數字／英文與中文間空格修正（seg 144、189、195、200、202、204、206、207、213、218）
  - topics.json 補錄 5 筆 potential_errors（seg 143 Grovel、200 piles、204 Representative Fire、204 Vallone、217 ideology）；seg 197 white-lane brain 無高信心修正，僅記草稿 notes

### 全部 5 個 topics 審訂完畢（2026-08-24）

- 5 檔 221 個 `→` 行 JSON 全數合法；段落編號 1–221 連續無缺漏；無千分位污染、無簡體字殘留、無「妳／網絡／社交媒體／星際迷航」等殘留（「通過」僅兩處合法動賓用法）
- 翻譯階段損毀的 3 段（seg 54、99、103 原文行混入譯文 JSON 殘骸、backfill 被標 pending）已全部依 main.yaml 還原，重新回填後應可補齊
- topics.json 校稿共補錄 **10 筆** potential_errors（topic_01 ×2、topic_02 ×2、topic_04 ×1、topic_05 ×5），加計既有 13 筆共 23 筆
- **待人工裁決事項**（全部解決）：
  1. ~~seg 204「Representative Fire」~~ → 2026-08-24 人工觀看影片確認為**交叉對話**：Cook 時間用畢欲移交發言權，說完「Representative…」後對方立即接話「All right」，「Fire」為 Whisper 疊音誤轉錄而非人名；譯文移除先前補入的「巴特利特」，改以刪節號呈現未說完的交棒；topics.json 修正建議同步更新
  2. ~~seg 213「majestic documents」~~ → 2026-08-24 人工裁決遵循模板規則譯「最高機密文件」（詞彙表原定譯「絕密文件」為早期產物、與其他集未同步，已更新 `terminology.yaml`）；主表未收錄此詞，無需重建
  3. ~~seg 48（topic_01）「We could rock next to it」~~ → 2026-08-24 人工觀看影片確認為「walk next to it」，譯文已依正確原文處理，confidence 調回 high
  4. ~~seg 197（topic_05）「white-lane brain」~~ → 2026-08-24 人工確認此處轉錄不一致（Whisper 作 white-lane brain、YouTube 字幕作 right length brain），聆聽後語意為「純以理性邏輯思考之人」，譯文依語境處理並加註；無高信心原文修正，不記 topics.json
- 依收尾流程，**暫停等待人工確認**後才執行 fix_transcription_errors / backfill / export
