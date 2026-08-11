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

### 背景

本集為 **UFO-08：Nuclear Tampering Part 2**，seg 1–290，5 個 topic，為 UFO-07 的續集（聽證會閉幕場次）。證人：Robert Salas 上尉（Malmstrom，1967）、Bruce Fenstermacher 上尉（F.E. Warren，1976）、David Schindele 上尉（Minot）、研究者 Richard Dolan；評審小組：Roscoe Bartlett 眾議員（主席）、Mike Gravel 參議員、Darlene Hooley 眾議員、Lynn Woolsey 眾議員、Fife Symington 前州長等。主題：政府壓制 UFO 的動機、媒體角色、飛彈關閉事件的訊息解讀、保密協議、飛彈防禦與太空武器化、閉幕致詞。

### 沿用前集裁決與主表定譯（審稿前已確認）

- **薩拉斯（Salas）**、**芬斯特馬赫（Fenstermacher）**、多蘭（理查德·多蘭）、康登委員會／康登調查／康登報告（Condon）：沿用 UFO-07 裁決與主表。
- **費伏·森明頓（Fife Symington）**：沿用 UFO-06 裁決（本集詞彙表一致）。
- **格拉維爾參議員（Gravel）**：主表定譯；本集詞彙表 definition 中的舊寫「格拉韋爾」為 deprecated。
- **胡利眾議員（Hooley）**：主表定譯；「胡利女眾議員」已廢棄。
- **基爾派翠克（Kilpatrick，主持人）**：主表「基爾派翠克眾議員」（UFO-07 沿用 UFO-06 定譯）。
- **伍爾西（Woolsey）**：沿用 UFO-03/UFO-07 定譯「伍爾西」；本集 seg 115 出現者應為 Lynn Woolsey 眾議員。
- **巴特利特議員（Bartlett）**：主表「羅斯科·巴特利特」。
- **本特沃特斯（Bentwaters）**：沿用 UFO-06/07 定譯（主表：皇家空軍本特沃特斯基地）。
- **飛彈**（非導彈）、**互動網路**（非網絡）、**女議員→眾議員**：全案統一，沿用 UFO-07。
- **括註一律全形「中譯（English）」**：沿用 UFO-07 人工裁決，省去日後補登任務。
- **星魚主（Starfish Prime）**：本集詞彙表作「海星計畫」，經查證網路流通譯名為「星魚主」（維基百科條目名），本集採用「星魚主」；該詞僅見於本集，無跨集衝突。
- **約翰斯頓島（Johnston Island）**：原文 seg 103 作 "Johnson Island"，實為 Johnston Island（約翰斯頓島／強森島，太平洋核試驗場）之誤聽；網路流通「約翰斯頓島／約翰斯頓環礁」，本集詞彙表舊譯「約翰遜島」不合流通，改用「約翰斯頓島」並補錄 potential_errors。

### 已知 Whisper 轉錄錯誤（topics.json potential_errors，原紀錄）

- topic_01：seg 50 Mrs. Hollis→Mr. Salas、seg 62 Robert Salles→Robert Salas、seg 67 Mr. Vestermarker→Mr. Fenstermacher、seg 69 Mr. Darlan→Mr. Dolan
- topic_02：seg 115 Congresswoman Woesey→Congresswoman Woolsey
- topic_04：seg 165 Captain Fenstermarker→Fenstermacher、seg 171 Conant investigation→Condon investigation、seg 186 Captain Schindell and Captain Salson→Schindele and Salas、seg 199 Captain Solace, Captain Schindel→Salas, Schindele、seg 200 Captain Fenster talk about--Fencemaster→Fenstermacher
- topic_05：seg 285 bent waters→Bentwaters

（審稿中新發現的錯誤依三.1 流程補錄，並於此區追加紀錄）

### 進度與交接筆記

- 2026-08-11：建立本檔（自模板複製）；完成背景調查與沿用裁決盤點；查證星魚主／約翰斯頓島譯名（來源：維基百科 zh 條目、Reddit 中文討論流通用法）。
- topic_01（seg 1–84）：審畢，**12 行修訂**：
  - 人名中譯：斯科特先生（seg 39）、薩拉斯／多蘭先生（seg 50）、羅伯特·薩拉斯（Robert Salas）（seg 62）、芬斯特馬赫先生（seg 67）、多蘭先生（seg 69）
  - 括註補登：萊特機場（Wright Field）（seg 74）、溫特沃斯上校（Colonel Wentworth）（seg 75）、聯邦航空總署（FAA）（seg 79）
  - seg 64 原文殘缺譯文潤飾並補 notes；seg 66「在 2010 年前」→「到 2010 年時」（by the time in 2010）；seg 76「僅從…聯繫」病句潤飾
  - seg 50 原文 Mr. Dole 應為 Mr. Dolan，notes 標註，topics.json 補錄（原紀錄 Mrs. Hollis 經查 main.yaml 已預先修正，紀錄改掛殘留錯誤）
- topics.json 異動：seg 50 紀錄更新為 Mr. Dole→Mr. Dolan；原紀錄 seg 62（Robert Salles）、67（Mr. Vestermarker）、69（Mr. Darlan）經查 main.yaml 皆已預先修正，收尾 fix_transcription_errors.py 自動跳過。
- 全部 `→` 行 JSON 驗證通過；千分位／網絡／絕密／核子物理殘留掃描通過。
- topic_02（seg 85–121）：審畢，**13 行修訂**：
  - 人名中譯＋括註：薩拉斯上尉（seg 88）、基爾派翠克女士（Ms. Gilpatrick）／彼得·詹寧斯（Peter Jennings）（seg 89）、斯科特先生／中士（seg 91，註實際軍銜為技術士官）、福克斯·穆德（Fox Mulder）／丹娜·史考莉（Dana Scully）（seg 95）、比爾·格雷厄姆（Bill Graham）／強尼·福斯特（Johnny Foster）（seg 103）、瓊·伍達德（Joan Woodard）／洛厄爾·伍德（Lowell Wood）／湯姆·克蘭西（Tom Clancy）／約翰·凱爾（John Kyle）（seg 104）、伍爾西眾議員（seg 115，女眾議員 deprecated 改眾議員）
  - **星魚主（Starfish Prime）**：seg 103 海星計畫→星魚主（網路流通查證，詞彙表待回改）；**約翰斯頓島（Johnston Island）**：原文 Johnson Island 誤聽，約翰遜島→約翰斯頓島，topics.json 補錄
  - seg 95 原文 Sculley 應為 Scully，notes 標註＋topics.json 補錄
  - seg 106 藍皮書數字 notes 補述（原文 12,800 – 618 口語＝官方 12,618 起／701 起未解）；seg 102 互聯網→網際網路；seg 96「被激勵暫停懷疑」潤飾；seg 116「擺脫人類」→「消滅人類」升 high；seg 86/100 潤飾；seg 103/104 EMP 委員會人名依人工裁決定稿（約翰·福斯特／勞威爾·伍德／瓊·凱爾／瓊·伍達德照字面）
- JSON 驗證與殘留掃描通過。
- topic_03（seg 122–163）：審畢，**14 行修訂**：
  - 人名中譯：彼得·詹寧斯（seg 124）、斯科特中士（seg 149）、眾議員（seg 150，女眾議員 deprecated 改正）、鮑勃（seg 151，Bob Salas）、大衛（seg 153，David Schindele）、薩拉斯上尉（seg 156）
  - **胡利女眾議員→胡利眾議員**（seg 144，主表廢棄譯名改正）
  - **flight 統一「飛行分隊」**（seg 156×2 處，沿用 UFO-06/07 裁決）
  - extraterrestrial 名詞用法譯「外星生命」（seg 130，沿用 UFO-07）；seg 131「UFO 知識彙編」→「不明飛行物知識彙編」
  - 邁諾特→邁諾特空軍基地統一（seg 145/146）；數據→資料（seg 161×2）；（掌聲。）→（掌聲）（seg 132）
- topics.json 無新增（本 topic 原紀錄即為空）。JSON 驗證與殘留掃描通過。
- topic_04（seg 164–212）：審畢，**12 行修訂**：
  - 人名中譯：庫克眾議員（seg 164，查證＝梅里爾·庫克 Merrill Cook，沿用 UFO-03 定譯；女眾議員 deprecated 改眾議員）、斯科特中士（seg 167）、菲格爾／邁沃爾德／卡爾森先生（seg 171，Carlson 音譯待查證）、馬卡姆教授（Professor Markham）（seg 185，身分待查證）、辛德利上尉（seg 186/199）、巴特利特先生（seg 187）、鮑勃·薩拉斯（seg 202）
  - flight 統一「飛行分隊」（seg 203 回音（Echo）飛行分隊站點、seg 207 回音與奧斯卡飛行分隊、seg 210）
  - UFO→不明飛行物（seg 171/190/202/203）；seg 194 yield 改議事用語「讓出發言權」
- topics.json 異動：seg 171 紀錄更新為 Conant investigator→Condon investigator（改掛 main.yaml 殘留文字）；原紀錄 seg 165（Fenstermarker）、186（Schindell/Salson）、199（Solace/Schindel）、200（Fenster/Fencemaster）經查 main.yaml 皆已預先修正，收尾自動跳過。
- JSON 驗證與殘留掃描通過。
- topic_05（seg 213–290）：審畢，**5 行修訂**：
  - 格拉韋爾→格拉維爾參議員（seg 216，主表 deprecated 改正）；朝鮮→北韓（seg 259，與 seg 224 統一）
  - seg 247 原文 Centres 應為 Senator，notes 標註＋topics.json 補錄
  - seg 266 查證註記：中國反衛星試驗（2007-01）實早於美國擊落 USA-193（2008-02），講者時序顛倒，依規則不擅改原文
  - seg 267「至高無上的愚蠢」→「極大的愚蠢」潤飾
- topics.json 補錄 1 筆（topic_05）：seg 247 Centres→Senator；原紀錄 seg 285（bent waters）經查 main.yaml 已預先修正為 Bentwaters，收尾自動跳過。

### 全集聚合（審稿完畢，2026-08-11）

- 5 個 topic 全數審畢，合計 **56 行修訂**（topic_01 12、topic_02 13、topic_03 14、topic_04 12、topic_05 5）。
- topics.json 累計新補錄 **4 筆**（seg 95 Sculley→Scully、seg 103 Johnson Island→Johnston Island、seg 171 紀錄改掛殘留文字 Conant investigator→Condon investigator、seg 247 Centres→Senator），另有 seg 50 紀錄改掛殘留錯誤 Mr. Dole→Mr. Dolan；原紀錄多筆經查 main.yaml 已預先修正（seg 50 Mrs. Hollis、62 Salles、67 Vestermarker、69 Darlan、115 Woesey、165 Fenstermarker、186 Schindell/Salson、199 Solace/Schindel、200 Fenster/Fencemaster、285 bent waters），收尾自動跳過。topics.json 現共 14 筆 potential_errors。
- 本集 terminology.yaml 回改 2 條目：Starfish Prime（海星計畫→星魚主）、Johnson Island→Johnston Island（約翰遜島→約翰斯頓島），皆經網路流通查證。
- 全部 290 行 `→` JSON 驗證通過（0 錯誤）；千分位／網絡／絕密／核子物理／互聯網／deprecated 譯名殘留掃描通過。
- **待人工事項**：
  1. ~~EMP 委員會人名拼寫查證~~ **已裁決（2026-08-11 人工）**：John Kyle→**瓊·凱爾（Jon Kyl）**（轉錄錯誤，topics.json 補錄 seg 104）；Johnny Foster 實為 **John S. Foster Jr.（約翰·福斯特博士）**；Lowell Wood 實為 **Lowell L. Wood Jr.（勞威爾·伍德博士）**；**Joan Woodard 查無其人**，疑為福斯特／伍德連讀混音之轉錄亂碼，edge case 照字面保留（瓊·伍達德＋註記）
  2. **Markham 教授**（seg 185）與 **Carlson**（seg 171）身分待查證，全案僅各一次出現，已音譯（馬卡姆／卡爾森）
  3. seg 266 講者時序顛倒（中國反衛星試驗早於美國擊落衛星），譯文保留原文僅註記，是否需其他處理請裁示
- ⚠️ 收尾流程（fix_transcription_errors／backfill／export）依模板第七節**暫停等待人工確認**，不得逕行。
