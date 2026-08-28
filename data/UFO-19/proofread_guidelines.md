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

UFO-19「Science & Technology」：2013 Citizen Hearing 的科學與技術場次，四位科學／醫學背景證人作證：

- **Dr. Robert Wood**（羅伯特·伍德博士）— 前麥克唐納-道格拉斯工程主管（seg 18–85）
- **Dr. Steven Greer**（史蒂芬·格里爾博士）— 揭露計畫創始人（seg 86–149）
- **Dr. Thomas Vallone**（托馬斯·瓦隆博士）— 物理學家，零點能源／慣性屏蔽（seg 150–273）
- **Dr. Roger Leir**（羅傑·萊爾博士）— 足病醫學博士，植入物手術（seg 274–361）
- seg 362 起為國會小組 Q&A；seg 774 起閉幕（基爾派翠克眾議員、布克曼博士）

### 檔案注意事項

- `topic_06.md` 達 99KB（seg 362–773，412 段），必須分段讀取、分段審訂
- 開場 seg 9 原文曾混入中譯「這個問題」殘骸，人工已依影片原稿修正

### 高頻術語定譯（本集詞彙表）

- 零點能源、零點能源場、慣性屏蔽、慣性質量、等效原理、勞倫茲力、電重力學、電重力、同極發電機、瑟爾碟、純量波、超能系統
- 真相揭露（Disclosure）、真相掩蓋（Cover-up）、最高機密（Top Secret）、黑項目、偽旗行動、日落條款
- 揭露計畫（Disclosure Project）、藍皮書計畫、康登委員會、MUFON、幽浮光球（Foo Fighters）
- 羅斯威爾、51 區、夏延山、松峽基地、洛克希德臭鼬工廠、愛德華茲空軍基地、柯特蘭空軍基地、桑迪亞國家實驗室、洛斯阿拉莫斯國家實驗室、達格威試驗場、瓦丘卡堡、諾頓空軍基地
- 人名：尼古拉·特斯拉、湯森·布朗、萬尼瓦爾·布希、杜立德將軍、赫爾曼·奧伯特、奧本海默、詹姆斯·E·麥克唐納博士、史丹頓·弗里德曼、尼克·庫克、約翰·瑟爾、喬治·凡·塔瑟爾、布魯斯·德帕爾瑪、保羅·拉維奧萊特、馬克·麥坎德利什、卡羅爾·羅辛、約翰·波德斯達、史蒂芬·霍金、亞瑟·克拉克、菲利普·科索

### topics.json 既有 potential_errors（13 筆，校稿時核對是否已反映於譯文）

- topic_03：seg 99 Kołysko-Frost effect、seg 112 modus operandi、seg 144 ITT
- topic_04：seg 193 Godin and Roschin、seg 268 Paul LaViolette／Townsend Brown、seg 270 Electrogravitics 2
- topic_05：seg 274 Roger Leir
- topic_06：seg 372 Dr. Vallone、seg 402 Dr. Gehr→Vallone、seg 557 Strangelovian、seg 562 Carol Rosin、seg 586 Center for American Progress

### 前任譯者遺留

- UFO-19 資料夾無校稿紀錄；翻譯階段時間見各檔 mtime（2026-08-06/07）

### 校稿進度與決策紀錄

（校稿過程中陸續補充）

- **topic_01（2026-08-24 完成）**：
  - seg 4 原文 tested 應為 testified（轉錄錯誤），譯文已依正確語意，notes 補註；topics.json 補錄 1 筆 potential_errors
  - seg 13 括註（Representative Hooley）改（Hooley）（括註慣例只放人名，頭銜已由「眾議員」呈現）
  - 胡利眾議員與主表及 UFO-04/05/08/20 定譯一致；seg 9 原文已由人工修正（混入中譯殘骸）
- **topic_02（2026-08-24 完成）**：
  - 4 筆轉錄錯誤修正並補錄 topics.json：seg 52 Dean Bob John→Bob Jahn（Robert G. Jahn，普林斯頓工程學院院長、PEAR 意識研究）譯改「鮑勃·賈恩院長」；seg 54 Hal Putoff→Puthoff（詞彙表 term 拼寫同步修正、定義改史丹佛研究院）；seg 56 MacDonald Douglas／MacDonald→McDonnell Douglas／McDonnell（創辦人 James S. McDonnell）；seg 62 Pond's Fleischman→Pons and Fleischmann（冷核融合），譯改「龐斯與弗萊施曼」
  - seg 54「史丹佛研究所」改「史丹佛研究院」（詞彙表定譯）
  - seg 67 肖克利→蕭克利（維基百科 zh-tw「威廉·蕭克利」）
  - seg 69「醫生」改「博士」（主持人對伍德博士的稱呼）
  - seg 66 刪除重複「洛杉磯著名的洛杉磯空襲」；three crash recoveries 歸屬語意模糊，notes 說明、維持 medium
  - seg 36 語序調整（「在那裡放一張…照片」）
  - 全檔數字／英文與中文間空格修正（10 行）
- **topic_03（2026-08-24 完成）**：
  - seg 101 原文行混入中譯「物理學」殘骸，main.yaml seg 101 原文完整，已依 main.yaml 還原（與 seg 9 同類型翻譯階段污染）
  - seg 134 Pahoot Mesa→Pahute Mesa（格魯姆湖旁真實台地），topics.json 補錄 1 筆 potential_errors
  - seg 112 句構錯誤修正（「但有一個由高級團隊領導，由…領導」重組為「一個由萬尼瓦爾·布希博士領導的高層團隊」）
  - seg 131「二十一點」改保留 Blackjack（疑為設施代號，原文破碎無從查證）；seg 132 降 medium 並加註（Hellendale 疑為 Palmdale 誤轉錄）
  - seg 95 長句重組（FBI 沒收文件句）；seg 111 威爾伯·史密斯文件句序調整；seg 140「追踪」改「追蹤」
  - 全檔數字／英文與中文間空格修正（12 行）
  - 既有 3 筆 potential_errors（seg 99、112、144）查對：main.yaml 原文已於 2026-02-27 修正（corrections_applied），譯文均已反映正確拼寫
- **topic_04（2026-08-24 完成）**：
  - 5 筆轉錄錯誤補錄 topics.json：seg 172/173 serial disk→Searle disk；seg 239 Hayes, Schwetter→Haisch, Rueda；seg 262 Dr. Villon→Vallone；seg 271 Putoff→Puthoff（同 seg 54）
  - seg 159 Bob Beck 依人名全中譯規則改「鮑勃·貝克博士（Dr. Bob Beck）」
  - seg 170 Ed Mitchell 改「艾德加·米切爾博士」（與 UFO-18 seg 141 查證定譯一致）；seg 172 譯文 Ed 同步改艾德加
  - seg 271 hovercraft 改「懸停飛行器」（UFO 語境非氣墊船）並加註
  - seg 270 notes 修正（原誤稱引自 topics.json）：1908 年疑為轉錄錯誤（諾頓基地 1942 年方成立），依規則保留原數字、維持 medium
  - seg 157 原文破碎（holding the instamatic photo），譯文重組、降 medium
  - seg 239、250 英文括註內全形逗號改半形
  - 全檔數字／英文與中文間空格修正（8 行）
  - 既有 potential_errors 查對：seg 193、268 main.yaml 已修正；seg 270 Electrogravitics 2 譯文已反映
- **topic_05（2026-08-24 完成）**：
  - 2 筆轉錄錯誤補錄 topics.json：seg 275 Major Podiatric Medicine→Doctor of Podiatric Medicine；seg 355 Kirkpatrick→Kilpatrick（Carolyn Kilpatrick），譯改「基爾派翠克眾議員」
  - seg 283/306 Dow Corning 依公司名中譯規則改「道康寧公司（Dow Corning）」
  - seg 295 艾森豪→艾森豪威爾（與 UFO-18 定譯及本集 seg 376 一致）
  - seg 307 secret metal 疑為 sheet metal 誤轉錄，依原文直譯並降 medium 加註（待人工看片確認）
  - seg 274「[掌聲]」改全形「［掌聲］」（與 topic_01 一致）；seg 326/327 通過→透過
  - 全檔數字／英文與中文間空格修正（10 行）
  - seg 274 既有 potential_error（Roger Lier）譯文已反映正確拼寫；seg 278 主席 Mr. Cook 無從查證，保留
- **topic_06（2026-08-24 完成，99KB 大檔分 5 段審訂）**：
  - 3 段原文行混入中譯殘骸，依 main.yaml 還原：seg 394（到另一端）、seg 444（大段）、seg 445（更好更強大）
  - 18 筆轉錄錯誤補錄 topics.json：seg 371/580/726/759 Dr. Lear→Leir；seg 403 meditational→gravitational mass；seg 436 Wilsey→Woolsey（Lynn Woolsey，UFO-01 先例）；seg 462 Paul Violette→LaViolette；seg 464/576 Moulton-Hull／Moulton-Hal→Moulton Howe（主表琳達·莫爾頓·豪）；seg 482 Dr. Lark→Vallone；seg 491 Barton→Bartlett（Roscoe Bartlett）；seg 538 Bernie Hayes→Bernard Haisch；seg 562 Werner→Wernher von Braun；seg 617 Berkman→Bookman；seg 618/632 Grevelle→Gravel（Mike Gravel）；seg 620 Valone→Vallone；seg 717 serious→《Sirius》（2013 紀錄片）；seg 748 air phone→earphone
  - seg 709 Representative Patrick 無從對應小組名單，降 medium 待人工看片（見待裁決 3）；seg 425 David Frohnig 人名無從查證，降 medium 加註
  - 全檔幻燈片→投影片（11 處，與 topic_04 同講者一致）、信息→資訊（17 處）；納米→奈米（seg 746/747/749）；通過→透過（seg 462/517/562/586/739）；在線→線上（seg 769）；人工智能→人工智慧（seg 430/431）；數字資訊→數位訊息（seg 763）；阿雷西博資訊→訊息（seg 761/766）
  - seg 397 範式研究小組→範式研究組織（主表定譯）；seg 444 斯坦·弗里德曼→史丹頓·弗里德曼；seg 486 majestic 12→Majestic 12 小組（MJ-12）；seg 594 majestic 委員會補 MJ-12 括註
  - 全檔數字／英文與中文間空格修正（43 行）；412 個 → 行 JSON 全數合法
  - 既有 5 筆 potential_errors（seg 372、402、557、562、586）查對：main.yaml 原文均已於 2026-02-27 修正，譯文反映正確拼寫
- **topic_07（2026-08-24 完成）**：
  - 全檔「妳」改「你」（seg 800、802、803、805、806、807、809，全專案慣例）
  - seg 790「醫生們」改「博士們」（對 PhD 證人的稱呼）；seg 808 約翰·葛倫→約翰·格倫（維基百科 zh-tw，與 seg 753 一致）
  - seg 800 括註（Congresswoman Kilpatrick）改（Kilpatrick）；seg 799/812 音效標記改全形［掌聲］／［靜默］；seg 806 引號『』改「」

### 全部 7 個 topics 審訂完畢（2026-08-24）

- 7 檔 812 個 `→` 行 JSON 全數合法；段落編號 1–812 連續無缺漏
- 殘留掃描：無千分位污染（`\d，\d`）、無「妳／網絡／絕密／核子物理」殘留；「通過」僅 seg 601 合法動賓用法（通過立法）；無簡體字殘留；音效標記全形統一
- 翻譯階段原文行混入中譯殘骸共 4 段（seg 101、394、444、445），均已依 main.yaml 完整原文還原（seg 9 由人工先行修正）
- topics.json 校稿共補錄 **32 筆** potential_errors（topic_01 ×1、topic_02 ×4、topic_03 ×1、topic_04 ×5、topic_05 ×2、topic_06 ×19），加計既有 13 筆共 45 筆
- 詞彙表修正 1 處：Dr. Hal Putoff→Puthoff（term 拼寫與定義）
- **待人工裁決事項**：Dr. Wood、Pine Gap、seg 709 Patrick 均已裁決（詳見下方）；seg 278 Mr. Cook、seg 307 secret metal 經看片確認屬實；seg 425 David Frohnig 仍無從查證（維持 medium）
- 依收尾流程，**暫停等待人工確認**後才執行 fix_transcription_errors / backfill / export
- **待人工裁決事項**：
  1. ~~Dr. Wood 譯名跨集不一致~~ → 2026-08-24 人工看片確認 UFO-10 與 UFO-19 的 Dr. Wood 為**同一人**（長相、聲音一致，皆為 Robert Wood；證人自報 Bob 為暱稱）。已回寫：UFO-10 詞彙表 term 改「Dr. Robert Wood」／羅伯特·伍德博士並加註裁決；`terminology_master_rules.yaml` deprecated 增列「鮑勃·伍德博士」；主表已以 `build_terminology_master.py --force` 重建（新增 Dr. Robert Wood 詞條，UFO-10/19 兩集）。UFO-10 草稿譯文「鮑勃·伍德博士」留待該集校稿時統一
  2. ~~Pine Gap 譯名主表與網路流通衝突~~ → 2026-08-24 人工裁決從主表用**松峽基地**（網路流通雖以松樹谷為主，人工偏好松峽基地）；seg 141 已改，括註與 notes 已清理
  3. ~~seg 709「Representative Patrick」~~ → 2026-08-24 人工看片確認發言者為**基爾派翠克眾議員（Kilpatrick）**，ASR 把 Kilpatrick 截成 Patrick。譯文已改「基爾派翠克眾議員（Kilpatrick）」調回 high；topics.json 補錄 potential_error（原文修正為 Representative Kilpatrick）

### 人工看片查證結果（2026-08-24）

依 AI 提供的時間軸人工看片，4 處待查證事項結果：
- **seg 278（00:34:38–00:34:58）Mr. Cook**：現場座位名牌確為 Mr. Cook，譯文「庫克先生」屬實，維持 high 不動
- **seg 307（00:39:55–00:40:14）secret metal**：發音確為 secret metal，YouTube 字幕同；人工裁決尊重發言人原話，不採 sheet metal 猜想，已調回 high 並更新註記
- **seg 425（00:54:40–00:54:43）David Frohnig**：發言者為 Thomas Valone；其提及的人名人工亦不確定，YouTube 字幕顯示 david frowny，仍無從查證，維持音譯 medium 並更新註記
- **seg 709（01:23:31–01:23:34）Representative Patrick**：確認發言人為 Kilpatrick，ASR 誤轉錄，已修正譯文並補登 topics.json（見待裁決 3）
