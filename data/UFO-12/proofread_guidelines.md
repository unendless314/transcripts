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

### 本集概況（2026-08-20 啟動）
- 本集為 Roswell Part 2：前半為理查德·弗倫奇中校（1960 年代末阿拉莫戈多 UFO 擊落事件目擊證詞），其後為弗里德曼／施密特／蘭德爾就 1947 羅斯威爾事件駁斥官方解釋（氣象氣球→莫古爾計畫）
- 共 8 個 topic（seg 1–471），drafts 8 檔（topic_07 約 30KB 為最大檔）

### 跨集沿用裁決（UFO-01～11 已拍板，本集直接沿用）
- 史丹頓·弗里德曼（Stanton Friedman）／史丹·弗里德曼（簡稱）；廢棄：佛烈德曼、史坦頓、斯坦頓
- 白沙飛彈靶場（White Sands Missile Range，導彈→飛彈，UFO-10 裁決）
- 萊特-帕特森空軍基地（Wright-Patterson AFB）；萊特機場（Wright Field）
- 羅斯威爾（Roswell，地名與事件皆中譯）；羅斯威爾陸軍航空基地
- 史蒂芬·希夫眾議員（Stephen Schiff）；廢棄：史蒂文
- 麥克·布拉澤爾（Mack Brazel）／比爾·布拉澤爾（Bill Brazel）／布拉澤爾（姓氏簡稱）
- 喬治·威爾考克斯警長（Sheriff George Wilcox）
- 理查德·弗倫奇中校（Richard French）；廢棄：法蘭奇（UFO-02 已統一）
- Colonel＝上校、Lieutenant Colonel＝中校（不可混淆，UFO-11 全面修正過）
- 克林頓→柯林頓（UFO-10 慣例）；飛碟（1947 新聞稿用語）；莫古爾計畫（Project Mogul）
- 薛瑞登·卡維特（Sheridan Cavitt，UFO-11 定譯；原文拼寫以 main.yaml 實際為準）
- 馬塞爾（Marcel，UFO-11 定譯，含一世／二世之別）；布蘭查德（Blanchard）；雷米將軍（General Roger Ramey）

### 待裁決／衝突事項（校稿中先回報，暫按建議處理）
1. **基爾派翠克 vs 柯派翠克（Carolyn Kilpatrick）**：本集 terminology.yaml 譯「卡蘿琳·柯派翠克」，但 UFO-01～10 全部校稿定譯與主表（Congresswoman Kilpatrick）均為「基爾派翠克」→ 校稿暫按主表改「基爾派翠克」，收尾回報人工確認
2. **Major Marcel 譯名**：本集 terminology.yaml 譯「馬瑟爾少校」，與 UFO-11 定譯「馬塞爾」衝突 → 暫按「馬塞爾少校」處理（同指 Jesse Marcel 一世）

### topics.json 既有 potential_errors（校稿時逐筆核對 main.yaml，可能失效）
- topic_01：seg 30 `Tongnyeongchon` → Tongyeong
- topic_02：seg 81 `Alan McGorgor` → Alamogordo；seg 86 `Kathleen Martin` → Kathleen Marden
- topic_03：seg 94 `Sidney Jack Wright` → Sidney "Stinky" Wright；seg 94 `Frankie Row` → Frankie Rowe
- topic_04：seg 100 `Colonel Watt-Randall` → Kevin Randle；seg 113 `Crash and Corona` → Crash at Corona；seg 114 `the Squam, Washington` → Sequim, Washington；seg 117 `Colonel Kev` → Colonel Cavett
- topic_05：seg 208 `Project Mobile` → Project Mogul
- topic_07：seg 266 `Sonoboy` → sonobuoy；seg 269 `notum` → NOTAM；seg 313 `Dr. Michael Swartz` → Dr. Michael D. Swords；seg 353 `General Raimi's` → General Ramey's；seg 375 `raywind radar target` → Rawin radar target
- topic_06/08：無

### 本集重點定譯（依 terminology.yaml，與主表衝突者見上方待裁決）
- 霍洛曼空軍基地（Holloman AFB）、英格蘭空軍基地（England AFB）、阿拉莫戈多（Alamogordo）
- 外國技術部門（Foreign Technology Division）、保羅·斯利珀上校（Colonel Paul Sleeper）
- 特別調查辦公室（OSI）、反情報部隊（CIC）、憲兵司令（provost marshal）
- 微風灣（Gulf Breeze, Florida，term 條目如此譯，注意網路流通可能為「格爾夫布里斯」，首見時查證）
- 貝蒂與巴尼·希爾（Betty and Barney Hill）、班傑明·賽門博士（Dr. Benjamin Simon）
- 克雷里博士的日記（Dr. Crary's diary）、查爾斯·摩爾（Charles Moore）
- 帕斯卡古拉（Pascagoula）、次軌道靈長類飛行、生物對稱性、真空管雷達
- 美國審計總署（GAO）、民航管理局（CAA）、聯邦航空總署（FAA）
- 丹·德懷爾（Dan Dwyer）、法蘭基·羅維（Frankie Rowe）、迪·普羅克特（Dee Proctor）、芳恩·弗里茨（Fawn Fritz）
- 艾德溫·伊斯利（Edwin Easley，UFO-11 同譯）、瑪莉安·史崔克蘭（Marion Strickland）
- 賈德·羅伯茨（Jud Roberts）、華特·惠特莫爾（Walt Whitmore）、KGFL 電台
- 格羅夫斯將軍（General Groves）、曼哈頓計畫、國家安全會議（NSC）

### 進度與決策紀錄
- 2026-08-20：校稿啟動，依序處理 topic_01 → topic_08
- [x] topic_01（11 處修訂）：seg 14/18/19 弗倫奇中譯＋括註（Colonel French／Lieutenant Colonel Richard French，沿用 UFO-02/17 定譯）；seg 21 英格蘭空軍基地補括註、第 614 補空格；seg 22/23 阿拉莫戈多中譯補括註、White Sands→白沙靶場；seg 25 數字空格；seg 27 類人生命體→類人生物（跨集慣用，原 notes 誤引詞彙表）；seg 28 霍洛曼空軍基地補括註、base operations 譯基地指揮中心加註；seg 30 萊特-帕特森空軍基地、保羅·斯利珀上校補括註、特別調查處→特別調查辦公室（OSI，沿用 UFO-02）、Tongyeong→統營補括註；seg 32 微風灣（沿用 UFO-02 定譯）、OSI 統一
- ⚠️ topic_01 原有 1 筆 potential_errors（seg 30 Tongnyeongchon→Tongyeong）經查 main.yaml 原文已是 Tongyeong，屬失效紀錄（Whisper 原始 SRT 確為 Tongnyeongchon，推測轉錄建檔時已逕修）
- [x] topic_02（16 處修訂）：seg 39/81 弗倫奇中譯；seg 40/41 年代與數字空格、阿拉莫戈多中譯；seg 43 同；seg 52/60/68/81/83 類人生命體→類人生物（全檔統一，共 7 處）；seg 70 基地作業中心→基地指揮中心（與 seg 28 統一）；seg 75 萊特-帕特森空軍基地；seg 76/77 保羅·斯利珀、喬治·克里斯托夫博士補括註；seg 81 史丹頓·弗里德曼補括註；seg 84 班傑明·賽門博士補括註、3,000 千分位；seg 85 弗里德曼先生（原文 Freeman 誤稱）；seg 86 凱薩琳·馬登補括註（網路無流通中譯，採台灣音譯）。**新發現轉錄錯誤 seg 85 Freeman→Friedman 已補錄 topics.json**
- ⚠️ topic_02 原有 2 筆 potential_errors（seg 81 Alan McGorgor、seg 86 Kathleen Martin）經查 main.yaml 原文皆已正確，屬失效紀錄
- [x] topic_03（10 段中 8 處修訂）：seg 88 麥克·布拉澤爾補括註；seg 89/90/95 1947 年空格；seg 90 威爾考克斯警長、威廉·W·布拉澤爾、法蘭克·喬伊斯補括註、Joyce→喬伊斯；seg 91/93 喬伊斯中譯；seg 94 布拉澤爾中譯（原文 Brazl×3 轉錄錯誤已補錄）、芳恩·弗里茨／迪·普羅克特／西德尼·傑克·萊特／法蘭基·羅維補括註；seg 96 馬塞爾少校（Major Marcel）中譯＋一世／二世註記（沿用 UFO-11 定譯，本集詞彙表「馬瑟爾」不採用）；seg 97 法蘭基·羅維、丹·德懷爾補括註。**新發現轉錄錯誤補錄 topics.json：seg 90 fine→find、seg 94 Brazl→Brazel（3 處），共 2 筆**
- ⚠️ topic_03 原有 2 筆 potential_errors：seg 94 Frankie Row→Frankie Rowe 屬失效紀錄（原文已是 Rowe）；seg 94 Sidney Jack Wright→Sidney "Stinky" Wright 非明確拼寫錯誤而是稱謂疑義，照字面翻譯保留，**待人工查證裁決**（網路查證工具當下受限）
- [x] topic_04（18 處修訂）：seg 98 馬塞爾上校中譯（指二世）；seg 100 凱文·蘭德爾補括註（紀錄 Watt-Randall 失效，原文已正確）；seg 101 Project Mogul→莫古爾計畫（全集統一改中譯，首見補括註）、查爾斯·摩爾／克雷里博士補括註；seg 102 唐／史丹中譯加註、白沙飛彈試驗場→白沙飛彈靶場（沿用 UFO-10/11 裁決）；seg 103 terrestrial terms→以地球上的事物來解釋；seg 104 弗里德曼先生；seg 107 卡維特中譯（首見，加註原文拼寫不一）；seg 109/111/121 傑西·馬塞爾／馬塞爾中譯；seg 113 史丹頓·佛烈德曼→弗里德曼（廢棄譯名）、《羅斯威爾報告》《科羅納墜毀事件》（沿用 UFO-11）書名補括註、Cosimo 出版社；seg 114 凱文／瑪麗／塞奎姆／塞拉維斯塔補括註（紀錄 the Squam 失效）；seg 115 通過電話→透過電話；seg 117 瑪麗、理查德·韋弗上校補括註、莫古爾計畫報告（紀錄 Colonel Kev 失效）；seg 118 馬瑟爾少校→馬塞爾少校、莫古爾計畫；seg 120 Kavett 拼寫註記
- ⚠️ topic_04 原有 4 筆 potential_errors（seg 100 Watt-Randall、seg 113 Crash and Corona、seg 114 the Squam、seg 117 Colonel Kev）經查 main.yaml 原文皆已正確，屬失效紀錄
- ⚠️ **新發現待裁決**：本集 main.yaml 原文 Cavett×17、Kavett×6，與 UFO-11 定案拼寫 Cavitt 不一致（該集已統一為 Cavitt）。收尾時是否全數修正為 Cavitt（23 處）待人工裁決；譯文不受影響
- [x] topic_05（15 處修訂）：seg 123 卡蘿琳·基爾派翠克（依主表與 UFO-01～10 定譯；本集詞彙表「柯派翠克」不採用，原文 Kirkpatrick 拼寫加註）；seg 124 施密特先生；seg 125 史蒂芬·希夫眾議員補括註（詞彙表「史蒂文」為廢棄譯名）；seg 127 希夫眾議員、木製墜落假人加註（沿用 UFO-11）；seg 129 日期空格；seg 130 Marcellus→馬塞爾先生（轉錄錯誤已補錄）；seg 154/155 總審計辦公室→美國審計總署（GAO，UFO-11 定譯）；seg 179 史丹；seg 196 went into service 疑轉錄錯誤加註；seg 216 Lynn→琳恩（所指委員待人工確認，降 medium）；另清理多處詞彙表引用式冗餘 notes
- ⚠️ topic_05 原有 1 筆 potential_errors（seg 208 Project Mobile）經查 main.yaml 原文已是 Project Mogul，屬失效紀錄。**新發現補錄：seg 130 Marcellus→Marcel**
- [x] topic_06（8 處修訂）：seg 218/223 馬瑟爾→馬塞爾；seg 233 日期空格、引號改「」；seg 234 瑪莉安·史崔克蘭補括註；seg 235 艾德溫·伊斯利補括註；seg 242/251/253 引號『』→「」
- ⚠️ topic_06 無既有 potential_errors，亦無新發現
- [x] topic_07（156 → 行大檔，分 2 段讀取；17 處修訂）：seg 259/260/263/269/272/280/353/359/370/388/397/398/405 年代數字空格；seg 269 CAA/NOTAM 補括註；seg 272 聯邦航空管理局→聯邦航空總署（FAA）補括註（UFO-11 定譯）、White Sand 錯誤加註；seg 273 白沙飛彈試驗場→白沙飛彈靶場；seg 281 傑西·馬瑟爾→馬塞爾；seg 313 麥可·索茲博士補括註＋講者校名有誤註記（實為西密西根大學）；seg 330 史蒂夫·希夫加註；seg 355/356 Wright Field→萊特機場（UFO-11 定譯）、Raimi 錯誤加註；seg 375 雷文雷達標靶補括註與縮寫說明
- ⚠️ topic_07 原有 5 筆 potential_errors：seg 266 Sonoboy、seg 313 Swartz、seg 375 raywind 三筆原文已正確（失效）；seg 269 notum 與 seg 353 Raimi 兩筆紀錄指向錯誤段位，實際殘留錯誤在 seg 271（notums/notum）與 seg 355（Raimi），已於 topics.json 補錄新紀錄並註記原紀錄失效。**新發現補錄：seg 272 White Sand→White Sands、seg 273 White Sand's missile range→White Sands Missile Range，共 4 筆新紀錄**
- [x] topic_08（11 處修訂）：seg 420 White Sands→白沙靶場；seg 427/428 New Mexico→新墨西哥州；seg 433 1948 年改阿拉伯數字；seg 439 國家安全委員會→國家安全會議（主表定譯）、1950 年代／18 個月數字化；seg 446 清理註記；seg 463/464/465 清理詞彙表引用式註記、大會首見補全「聯合國大會」
- ⚠️ topic_08 無既有 potential_errors，亦無新發現

### 總檢查（2026-08-20）
- [x] 全部 471 個 → 行 JSON 合法（33+54+10+25+95+40+156+58）；topics.json 合法
- [x] git diff 無非 → 行異動（+114/-114，8 檔皆然）
- [x] 殘留掃描零命中：`\d，\d`、佛烈德曼、馬瑟爾、史蒂文、法蘭奇、網絡、絕密、核子物理、總審計辦公室；「通過」僅 1 處且為合法動賓用法（決議通過）
- [x] 譯文（括註外）無英文人名殘留（僅存 UFO／FBI／GAO／FAA／CAA／CIC／OSI／KGFL／PTSD／NOTAM／B-29／Mogul／Rawin／Cosimo 等允許縮寫與書名原文）

### potential_errors 總結（收尾用）
- **有效紀錄共 17 筆**（fix_transcription_errors 收尾時執行）：
  - topic_02：seg 85 Mr. Freeman→Mr. Friedman（補錄）
  - topic_03：seg 90 reported the fine→reported the find（補錄）；seg 94 Brazl→Brazel 3 處（補錄）
  - topic_04：seg 107/109/111/114/117 Cavett→Cavitt、seg 120/121 Kavett→Cavitt（人工裁決統一為 UFO-11 定案拼寫，seg 114 含 Sheridan-Cavett、seg 120 為 Kavett×3，共 7 筆補錄）
  - topic_05：seg 130 Marcellus→Marcel（補錄）
  - topic_06：seg 223 Cavett→Cavitt（補錄）
  - topic_07：seg 271 notum→NOTAM、seg 272 White Sand.→White Sands.、seg 273 White Sand's missile range→White Sands Missile Range、seg 282 Cavett→Cavitt、seg 355 Raimi→Ramey（補錄）
- **失效紀錄共 12 筆**（main.yaml 原文早已正確，收尾時標記、不執行修正）：
  - topic_01：seg 30 Tongnyeongchon（1 筆）
  - topic_02：seg 81 Alan McGorgor、seg 86 Kathleen Martin（2 筆）
  - topic_03：seg 94 Frankie Row（1 筆）
  - topic_04：seg 100 Watt-Randall、seg 113 Crash and Corona、seg 114 the Squam、seg 117 Colonel Kev（4 筆）
  - topic_05：seg 208 Project Mobile（1 筆）
  - topic_07：seg 266 Sonoboy、seg 313 Swartz、seg 375 raywind（3 筆；另 seg 269 notum 與 seg 353 Raimi 兩筆原紀錄指向錯誤段位，實際錯誤已另立 seg 271/355 新紀錄）

### 待人工裁決事項
1. ✅ **基爾派翠克 vs 柯派翠克**：人工裁決採「基爾派翠克」，已回寫本集 terminology.yaml（2026-08-21）
2. ✅ **Cavett/Kavett→Cavitt**：人工裁決全數修正，已補錄 9 筆紀錄（topic_04 seg 107/109/111/114/117/120/121、topic_06 seg 223、topic_07 seg 282，共 12 處原文），收尾時執行（2026-08-21）
3. ✅ **Sidney Jack Wright**（seg 94）：人工裁決查無流通資料，照字面音譯「西德尼·傑克·萊特」保留；topics.json 原紀錄已刪除以免收尾誤執行（2026-08-21）
4. ✅ **Lynn**（seg 216）：人工確認指林恩·伍爾西（Lynn Woolsey），譯文已更新並改 high；譯名用字從 UFO-09 定譯「林恩」（人工訊息原寫「琳恩」，如欲改用琳恩請示下，並需一併評估 UFO-09）
5. ✅ **terminology.yaml 跨集定譯比對完成**（2026-08-21）：實際衝突共 3 處，均已回寫——柯派翠克→基爾派翠克、馬瑟爾少校→馬塞爾少校（UFO-11 定譯）、理查德·韋弗→理查·韋弗（UFO-11 seg 328 定譯，seg 117 譯文同步修正）；其餘詞條（GAO／FAA／軍事委員會／陸軍航空隊／憲兵司令／曼哈頓計畫／阿拉莫戈多／喬伊斯／布拉澤爾家族等）與 UFO-02/03/10/11 及主表一致，Kristof／Sleeper／Pascagoula／Groves／Hill 案相關為本集首見無衝突
6. ✅ **UFO-02 seg 235「史蒂文·席夫」**：人工裁決一併修正，已改為「史蒂芬·希夫（Stephen Schiff）」（括註內 Steven 亦改正為原文實際拼寫 Stephen），該集尚未回填，隨收尾統一處理（2026-08-21）
