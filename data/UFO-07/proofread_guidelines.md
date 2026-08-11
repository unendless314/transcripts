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

本集為 **UFO-07：Nuclear Tampering Part 1**，seg 1–718，6 個 topic。證人：Robert Salas 上尉（Malmstrom，1967）、David Scindelli 上尉（Minot，1966）、David Scott 技術士官（Minot，1974）、Bruce Fenstermacher 上尉（F.E. Warren，1976）、研究者 Richard Dolan。主題：UFO 與核武設施的關聯、飛彈關閉事件、軍方掩蓋文化。

### 譯名裁決紀錄（2026-08-11）

- **辛德利（Scindelli）、芬斯特馬赫（Fenstermacher）**：網路無中譯流通，人工裁決採用台灣音譯。
- **薩拉斯（Salas）**：星島日報報導流通「薩拉斯」，與本集詞彙表一致。
- 多蘭（Richard Dolan）：主表定譯「理查德·多蘭」（UFO-09/17/18/20 一致），沿用。
- 海尼克（Dr. J. Allen Hynek）：主表定譯「J·艾倫·海尼克博士」，沿用。
- 康登委員會／康登調查／康登報告：主表定譯，沿用；Edward Condon → 愛德華·康登。
- **OSI → 空軍特別調查辦公室**：沿用 UFO-06 裁決（seg 234/235 已改）。
- Kathy → 凱西（聽證會工作人員，音譯；seg 185）。
- **括註格式裁決（2026-08-11 人工）**：本集草稿括註一律轉全形「中譯（English）」，省去日後補登任務。
- **導彈→飛彈**：全案統一用「飛彈」（與主表、詞彙表一致），topic_01 已全數改正。
- Kilpatrick → 基爾派翠克（沿用 UFO-06 定譯 基爾派翠克眾議員）。

### seg 52–110 音訊還原（2026-08-11 完成）

原 Whisper 轉錄於 seg 52–110（00:06:12,900–00:08:26,940）幻覺重複「I've never heard of it before.」。人工聽音訊還原後確認該區塊實為兩段 1996 年電話錄音＋Salas 說明：

- **第一段錄音（seg 52–76 區塊）**：Salas 與 **Walter Figel 上校**（Echo Flight 前副飛彈組指揮官）通話——Figel 描述 1967-03-16 當日兩個站點的安全／維修人員與兩支應變小組均目擊 UFO。
- **第二段錄音（seg 76–84 區塊）**：Salas 與 **Mywald**（原文拼寫 Maywald，全案統一作 Mywald）通話——兩名外出警衛目擊怪異後驚恐失聯、提前送回基地。
- **seg 84–93 間隔、seg 94–110**：Ms. Solis 提問、Salas 說明錄音來源（Figel 授權、1996 年電話錄音）。

處理方式：main.yaml seg 52–110 source_text 與譯文全數重寫（保留 seg 編號與時間戳，無內容間隔段 text 為 null）；topic_01.md 已同步；main_segments.json 已重產。人名依裁決規則保留（Colonel Walter Figel→沃爾特·菲格爾上校、Ms. Solis→索利斯女士，已新增本集詞彙表條目；譯名無網路流通，採台灣音譯）。

連帶發現並補錄：**seg 48/51 原文「Colonel Mywald」應為「Colonel Figel」**（第一段錄音歸屬，Whisper 誤聽）——譯文已逕改「菲格爾上校」，topics.json 補錄 2 筆，收尾 fix_transcription_errors.py 修原文。

### 已知 Whisper 轉錄錯誤（topics.json potential_errors）

- topic_01 原紀錄 7 筆：seg 1（assistance hearing）、8（Roger Salas）、14（Maldenstrom）、17（Mywold）、150（M91 missile）、172（Menott）經查 main.yaml 皆已預先修正，收尾自動跳過；seg 168 deputy accountant 經查錯誤文字實於 **seg 169**，已改掛 seg 169。
- 新補錄：seg 48/51 Colonel Mywald→Colonel Figel（音訊還原確認）；seg 165 Chase hinted→Chase and I had exchanged（康登報告引文）。
- （審稿中新發現的錯誤依三.1 流程補錄，並於此區追加紀錄）

### 進度與交接筆記

- 2026-08-11：建立本檔（自模板複製）；裁決紀錄完成（辛德利／芬斯特馬赫音譯、括註轉全形、導彈→飛彈）。
- topic_01（seg 1–184）：審畢，**約 45 行修訂**：
  - 導彈→飛彈全數統一（約 20 處）；敏感資訊網絡→敏感資訊網路（seg 129）
  - 半形括註轉全形（seg 8/14/15/17/20/25/44/140/158/163/164/168/172，共 13 段）
  - 人名中譯：基爾派翠克先生（seg 13）、邁沃爾德中尉／上校（seg 42/46/48/51/118/120）、辛德利先生／斯科特先生（seg 184）；seg 10 「Salas 是正確的」為發音確認語境，依四.排版規則保留原文
  - seg 158 team leader→主持人（Condon 為研究主持人）
  - seg 165 原文 hinted 應為 and I，譯文改「蔡斯上校與我……寒暄之後」降 medium，topics.json 補錄
  - seg 168/169 deputy accountant notes 統一「原文 deputy accountant 應為 project coordinator（Whisper 誤轉）」
  - seg 173 notes 補述 right-pat 疑為亂碼轉錄
  - seg 52–110 幻覺重複區塊保留，待人工聽音訊裁決（見上節）
- topic_02（seg 185–262）：審畢，**24 行修訂**：
  - 導彈→飛彈統一（seg 191/195/196/220/222/225/227/229/230/242/247）；半形括註轉全形（seg 186/187/191/193/251/252/256）
  - OSI 定譯「空軍特別調查辦公室」（seg 234/235，沿用 UFO-06 裁決）
  - 凱西（seg 185）、地面人員（seg 241 topside airmen）；seg 252 「of Blue Book fame」改「因藍皮書計畫而聞名」
  - seg 231 原文 Hopside 應為 topside，notes 補記；seg 253 原文 Heineck 應為 Hynek，notes 補記
- topics.json 補錄 3 筆（topic_02）：seg 194 west of Mole Hall→Mohall（seg 193 原紀錄該處已預先修正，此處為殘留）、seg 231 Hopside→topside、seg 253 Heineck→Hynek；原紀錄 seg 193/195/251/252 經查 main.yaml 已預先修正，收尾自動跳過。
- topic_03（seg 263–300）：審畢，**約 20 行修訂**：
  - 導彈→飛彈統一（seg 266/274/278/284/296 等）；人名中譯：斯科特士官（seg 263/300）、格雷（Gray×7 處）、希克斯士官（Hicks×5 處）
  - seg 265 第 91 飛彈安全中隊補空格；Alpha Flight 譯「Alpha 飛行分隊」並註解 flight＝分隊編制（沿用 UFO-06 慣例）
  - seg 293 括註內「Winnipeg， Canada」半形逗號修正為「Winnipeg, Canada」
  - seg 300 末句「Captain」指主持人基爾派翠克（陸軍上校），譯「上校」並註記，非上尉
- topic_04（seg 301–386）：審畢，**約 15 行修訂**：
  - 芬斯特馬赫（seg 301/302 證人自報姓氏，保留原文括註）；大衛·辛德利（seg 312）、大衛·斯科特（seg 315）、勃·薩拉斯（seg 377）、薩拉斯先生（seg 380）
  - flight 統一「飛行分隊」：Papa/Quebec/Romeo/Sierra/Tango（seg 339）、Quebec 飛行分隊（seg 340/344/377）、Quebec 分隊指揮官（seg 369）、Quebec 分隊安全警戒小組（seg 364）
  - seg 350 導彈→飛彈；seg 351 原文 LFE Warren 應為 F.E. Warren，notes 補記，topics.json 補錄
  - seg 374 notes 維持「1960 應為 1976 的口誤」（講者口誤，不擅改原文）
- topics.json 補錄 1 筆（topic_04）：seg 351 LFE Warren→F.E. Warren；原紀錄 seg 312（Schindley）、337（SAT command post）、379（亂碼句）經查 main.yaml 皆已預先修正，收尾自動跳過。
- topic_05（seg 387–503）：審畢，**約 20 行修訂**：
  - 人名中譯：多蘭先生（seg 387）、拜倫·D·瓦爾納（Byron D. Varner，seg 395）、羅蘭·鮑威爾／鮑威爾（Roland Powell，seg 398/409/418）、沃爾特·安德魯斯先生（Walter Andrus，seg 399）
  - 互動網絡→互動網路（seg 399/400）；OSI 定譯 seg 430；半形括註轉全形（seg 391/401/406/425/443/444/480）；seg 443 括註內半形逗號修正
  - seg 396 書名《Living on the Edge…》無通行中譯，依二.2 準則改回原文，中譯移入 notes
  - seg 481 原文 plan 應為 plant，notes 補記，topics.json 補錄
- topics.json 補錄 1 筆（topic_05）：seg 481 plan→plant；原紀錄 seg 387（Mr. Doley）、432（Media rights）經查 main.yaml 已預先修正，收尾自動跳過。
- **flight 譯法跨檔統一（2026-08-11）**：飛彈聯隊編制中 flight＝分隊（沿用 UFO-06 慣例）。topic_01×11 行、topic_02×4 行、topic_06×2 行「飛行中隊」→「飛行分隊」（Echo／Oscar／November 皆同）；本集 terminology.yaml 已回改（Echo flight incident、November Flight 兩條目）。中隊（squadron，如第 91 飛彈安全中隊）不受影響。
- topic_06（seg 504–718）：審畢，**約 50 行修訂**：
  - 導彈→飛彈全數統一（約 10 處）；半形括註轉全形（seg 504/507/525/540/555/585/587/592/594/632/641/664/666/670/684/686/688/694/699/701/710/712 等）
  - 人名中譯：羅伯特（seg 524）、理查德（seg 568）、胡利眾議員（seg 585）、詹姆斯·克洛茨（seg 597）、弗雷德·邁沃爾德（seg 603）、勃·薩拉斯（seg 556/635）、瓦爾·史密斯（seg 671）、羅伯特·洛（seg 689）、伍爾西眾議員（seg 701）、維克多·維吉亞尼／彼得·金（seg 710）、提摩西·古德（seg 592）
  - 女議員→眾議員統一（seg 585/631/701，沿用 UFO-06）；數據→資料（seg 543/704）
  - seg 537 Bentwaters 改「本特沃特斯場次」（沿用 UFO-06 定譯）並註記
  - seg 544 主持人稱 Scott「上尉」實為士官，譯文照原文保留「斯科特上尉」並維持 medium＋notes（講者口誤類，不擅改）
  - seg 567 extraterrestrial 改「外星生命」，原文 "not by other countries" 疑誤轉註記
  - seg 573 Kasputin Yar→卡普斯京亞爾（Kapustin Yar）並註記
  - seg 592 《Above Top Secret》無通行中譯，依準則保留原文（原譯《絕密之上》亦觸犯 Top Secret≠絕密定譯）；Timothy Goode→Timothy Good 註記
  - seg 633 委員口誤稱 Fenstermacher 為 Congressman，notes 已記，譯文照譯「芬斯特馬赫上尉」
  - notes 統一格式：seg 593（Malsom）、603（Mywall）、647（ear→year）、664（Conant→Condon）
- topics.json 補錄 7 筆（topic_06）：seg 507 Mr. Dole→Dolan、seg 573 Kasputin Yar→Kapustin Yar、seg 592 Timothy Goode→Good、seg 593 Malsom→Malmstrom、seg 603 Mywall→Mywald、seg 647 ear→year、seg 664 Conant→Condon（main.yaml 皆有殘留可匹配）；原紀錄 seg 556（Salwas）、635（Salazar）、666（Schindl）、710（Bigliani/Zeeland）經查 main.yaml 已預先修正，收尾自動跳過。

### 全集聚合（審稿完畢，2026-08-11）

- 6 個 topic 全數審畢，合計約 **170 行修訂**（topic_01 約 45、topic_02 24、topic_03 約 20、topic_04 約 15、topic_05 約 20、topic_06 約 50，含 flight 統一 17 行跨檔改動）。
- topics.json 累計新補錄 **15 筆** potential_errors（topic_01×3、topic_02×3、topic_04×1、topic_05×1、topic_06×7），全部已確認 main.yaml 有原文可匹配（seg 48/51 為音訊還原後補錄）；原紀錄多筆經查已於翻譯階段前預先修正（seg 1/8/14/17/150/172/193/195/251/252/312/337/379/387/432/556/635/666/710），收尾時 fix_transcription_errors.py 會自動跳過。
- 本集 terminology.yaml 回改 2 條目（Echo flight incident、November Flight：飛行中隊→飛行分隊）；新增 2 條目（Colonel Walter Figel、Ms. Solis，音訊還原產出）。
- seg 52–110 幻覺區塊已依人工還原音訊重寫（main.yaml＋topic_01.md＋main_segments.json 同步完畢）。
- **待人工事項**：
  1. ~~seg 52–110 幻覺重複~~ **已解決（2026-08-11）**：人工還原音訊，內容已回填
  2. ~~seg 544「斯科特上尉」~~ **已裁決（2026-08-11 人工）**：逕改「斯科特士官」，notes 註明原文 Captain Scott 為主持人口誤——已執行
- ⚠️ 收尾流程（回填、修原文、匯出）依模板第七節**暫停等待人工確認**，不得逕行。
