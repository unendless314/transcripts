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

### 本集概況（2026-08-21 啟動）
- 本集為 South American Encounters Part 1：南美五國（巴西、智利、烏拉圭、祕魯、阿根廷）UFO 研究聽證會
- 證人：威爾遜·皮克勒（Wilson Pickler，巴西前國會議員）、熱瓦爾德（A. J. Gevaerd，巴西）、安東尼奧·胡尼烏斯（Antonio Huneeus，智利）、Ariel Sánchez 上校（烏拉圭）、Anthony Choy（祕魯）、Oscar Santa María 上校（祕魯）、Alejandro Chionetti（阿根廷）
- 共 7 個 topic（seg 1–452），drafts 7 檔

### 跨集沿用裁決（UFO-01～12 已拍板，本集直接沿用）
- J·艾倫·海尼克博士（Dr. J. Allen Hynek，主表定譯；原文 Heineck 為轉錄錯誤）
- 安東尼奧·胡尼烏斯（Antonio Huneeus，UFO-02 定譯）；胡尼烏斯先生（Mr. Huneeus）
- Disclosure（揭露運動語境）→ 真相揭露；Being/Beings → 存有
- 聖瑪利亞上校（Colonel Santa Maria，UFO-14 詞彙表先例）、貝爾穆德斯將軍（General Bermudez，UFO-14 詞彙表先例；注意 UFO-14 詞彙表未經校稿，僅供參考）
- 科拉雷斯島（island of Colares，UFO-14 詞彙表先例）
- 引號用「」，內層用『』；千分位半形逗號

### 待裁決事項（校稿中先回報）
1. **主表 CEFORA 詞條矛盾（已解決，2026-08-21）**：確認為 commit 2cf0508 批次標準化誤抓（從無集數裁決、與首選譯名自相矛盾）；人工核准後已移除 `terminology_master_rules.yaml` 的 `cefora: ["CEFORA"]` 並以 build_terminology_master.py --force 重建主表（167 詞），CEFORA 詞條廢棄註記已消失
2. **CEFA vs CEFAA（已完成，2026-08-21）**：人工確認 CEFAA 為正確縮寫。已執行：UFO-13 詞彙表 CEFA→CEFAA、UFO-16 詞彙表 CEFA→CEFAA（含收尾補錄提示）、UFO-16 topic_02 seg 140 草稿預先更正、主表規則檔移除舊 cefa 廢棄項、build_terminology_master.py --force 重建（167 詞，CEFAA 收錄 UFO-13/14/16 三集；UFO-14 sense 譯名略異，該集校稿時留意）
3. **熱瓦爾德（Gevaerd）（已裁決）**：人工確認「熱瓦爾德」中譯採用
4. **Valdez → Valdés（已裁決，2026-08-21）**：seg 142 原文拼寫依網路流通慣例（Armando Valdés）更正，topics.json 已補錄，中譯「瓦爾德斯」不變
5. **Mohabt → Mohaupt（已裁決，2026-08-21）**：seg 411 正確拼寫為 Mariano Mohaupt（阿根廷空軍新聞發言人、CEFAE 首任主任，人工查證），topics.json 已補錄
6. **seg 203 軍銜（已裁決）**：人工裁決尊重講者自我表達，維持「將軍」照原文翻譯，notes 已更新
7. **seg 318 句構（已定案，2026-08-21）**：人工聽音確認原文發音確為 to（00:55:02,200–00:55:14,840）；本段為同步口譯，推測口譯者文法有誤。原文不修改，譯文依 seg 320 語境補足語意（呈報一份美國國防部的文件），notes 完整留痕，confidence 調回 high

### topics.json 既有 potential_errors（校稿時逐筆核對 main.yaml，可能失效）
- topic_01：seg 26 `Is it Givard?` → Gevaerd（⚠️ 經查 main.yaml 原文已是 Gevaerd，屬失效紀錄）
- topic_02：seg 79 `Mr. Javarn` → Gevaerd；seg 110 SICOANI；seg 112 `Coladis` → Colares
- topic_03：seg 128 `Antonio Junel` → Huneeus；seg 151 `DDIC` → DGAC；seg 191 `CFA and Kridovny` → CEFAA/CRIDOVNI
- topic_04：seg 212 square feet → square kilometers；seg 222 `LACRI OVNI` → CRIDOVNI
- topic_05：seg 268 `Ivan Issa Nanfardo` → Iván Ascanio Fajardo
- topic_06：seg 317 `I'm Mr. Huertas.`；seg 327 `La Jolla` → La Joya；seg 357 `Sukui 22` → Sukhoi Su-22
- topic_07：seg 361 `Chinoti` → Chionetti；seg 371 `Heineck` → Hynek；seg 389 `Parani` → Pagani；seg 405 `El Huitorco` → Uritorco；seg 410 `CEFA` → CEFAE；seg 418 `Sephora` → CEFORA

### 本集重點定譯（逐步累積）
- 威爾遜·皮克勒（Wilson Pickler）
- 熱瓦爾德（Gevaerd）先生（網路無流通中譯，採葡語音譯）
- 真相揭露（disclosure）、不明飛行物／UFO（依主表廢棄規則不加「（UFO）」括註）
- 珍妮佛（Jennifer）、塞爾索·阿莫里姆（Celso Amorim）大使
- 「不明飛行物調查系統」（SICOANI）、飛碟行動（Operation Saucer）
- 異常空中現象研究委員會（CEFAA，本集統一；原文 CEFA/CEFA-A/CFA 為轉錄變體）、智利民航局（DGAC）
- 貝爾穆德斯將軍（Ricardo Bermudez）、拉蒙·貝加（Ramon Vega）將軍、古斯塔沃·羅德里格斯（Gustavo Rodriguez）、瓦爾德斯（Valdez）下士、桑切斯（Sánchez）上校
- 《透明度法》（law 20285）、鵜鶘案（Pelican case）、埃爾博斯克基地（El Bosque）、方丹山（Fountain Hills）
- 艾瑞爾·桑切斯·魯伊斯（Ariel Sanchez Ruiz）上校、CRIDOVNI（烏拉圭空軍不明飛行物調查委員會，保留原文）
- 安東尼·喬伊（Anthony Choy）、丘盧卡納斯事件（Chulucanas incident）、祕魯空軍
- 胡里奧·查莫羅-弗洛雷斯（Julio Chamorro-Flores）指揮官、埃內斯托·阿蘭西維亞·利納雷斯（Ernesto Arancivia Linares）上尉、赫爾曼·施羅克·卡斯蒂略（Germán Shrock Castillo）上尉、何塞·拉蒂（José Ratti）上校
- 伊萬·阿斯卡尼奧·法哈多（Iván Ascanio Fajardo）、莫羅蓬（Moropon）、皮蘭山（Cerro Pilán）、庫斯科（Cusco）
- 奧斯卡·聖瑪利亞·韋爾塔斯（Oscar Santa María Huertas）上校、拉霍亞基地（La Joya）、蘇霍伊 Su-22 戰鬥機、氣球形飛行器（aerostatic globe）
- 亞歷杭德羅·基奧內蒂（Alejandro Chionetti）、COPEFO、不明潛水物（USO）
- CEFORA（阿根廷共和國不明飛行物現象研究委員會）、CEFAE（航太現象研究委員會）
- 奧馬爾·帕加尼（Omar Pagani）艦長、馬里亞諾·莫哈特（Mariano Mohabt）艦長（拼寫存疑）、吉列爾莫·阿洛伊（Guillermo Aloy）准將、胡里奧·戈塞納-阿瓜羅（Julio Goxena-Aguaro）
- 米奧蒂（Miotti）艦長、愛德華多·阿茲庫伊（Eduardo Azcuy）、欺騙島（Deception Island）、烏里托爾科山（Uritorco）、五月營（Campo de Mayo）、蒙特格蘭德（Monte Grande）、巴里洛切機場（Bariloche）、海岸巡防隊（Prefectura Naval Argentina）

### 進度與決策紀錄
- 2026-08-21：校稿啟動，依序處理 topic_01 → topic_07
- [x] topic_01（5 處修訂）：seg 28 Gevaerd 補中譯音譯＋括註（紀錄 seg 26 Givard 屬失效紀錄，原文已正確）；seg 38 威爾遜·皮克勒補中譯＋括註；seg 57 沙皇炸彈查證註記、confidence 降 medium（保留講者原數字 3,333 倍）；seg 62/63 「小男孩」/「胖子」引號改「」並補原文括註。其餘段落（宣誓、開場、核武論述）品質佳未修訂
- [x] topic_02（6 處修訂）：seg 79 熱瓦爾德先生（統一中譯）；seg 82 威爾遜·皮克勒教授（統一中譯）；seg 94 珍妮佛（Jennifer）補中譯＋括註；seg 95/98 簡體字「张」→「張」；seg 98 塞爾索·阿莫里姆（Celso Amorim）補中譯＋括註；seg 112 刪冗餘音譯註記（括註已含原文）
- ⚠️ topic_02 原有 3 筆 potential_errors 全數失效：seg 79 原文已是 Gevaerd、seg 110 原文已是正確 SICOANI 全稱、seg 112 原文已是 Colares（推測建檔時已逕修）
- [x] topic_03（26 處修訂）：CEFA/CEFA-A/CFA 全數統一為 CEFAA（seg 139/147/148/150/151/155/156/163/164/185/186，共 11 段；原文變體已補錄 topics.json）；貝爾穆德斯將軍（Ricardo Bermudez）全檔統一中譯（沿用 UFO-14 詞彙表先例）；拉蒙·貝加（Ramon Vega）、古斯塔沃·羅德里格斯（Gustavo Rodriguez）、瓦爾德斯（Valdez）下士、桑切斯（Sanchez）上校、方丹山（Fountain Hills）補中譯＋括註；seg 147 洛克菲勒名採 Laurance（依 UFO-03/04 裁決）；跨段引文引號全面改「」（含 seg 198/199 多餘閉引號移除）；seg 165 鵜鶘案引號；seg 191 數據→資料
- ⚠️ topic_03 原有 3 筆 potential_errors：seg 128 Junel 原文已正確（失效）；seg 151 DDIC 待核對（原文實為 DGAC，失效）；seg 191 CFA/Kridovny 原文已正確（失效，CFA 實際見於 seg 185/186 已另立紀錄）。新補錄 5 筆：seg 139 CEFA→CEFAA、seg 147 Lawrence→Laurance＋CEFA-A、seg 148 CEFA-A（含 150/151/155/156/163/164）、seg 185 CFA（含 186）
- ⚠️ **新發現待裁決**：seg 142 Valdez 下士，網路流通該案當事人多作 Valdés（Armando Valdés），拼寫待人工裁決；譯名「瓦爾德斯」兩者通用
- [x] topic_04（10 處修訂）：seg 203/206 艾瑞爾·桑切斯（Ariel Sánchez）／艾瑞爾·桑切斯·魯伊斯補中譯＋括註（seg 203 主席稱將軍、seg 207 自述退役上校，加註疑義）；seg 208/211/212/213/216/221 數字與中文間補空格（7 段）；seg 212 notes 更新（square feet 紀錄失效）；seg 221 recopilación 加註；seg 225 notes 更新（LACRI OVNI 轉錄錯誤確認）
- ⚠️ topic_04 原有 2 筆 potential_errors：seg 212 square feet 原文已正確（失效）；LACRI OVNI 實際出現於 seg 225（原紀錄 segment_id 誤載 222，topics.json 已更正）
- [x] topic_05（22 段修訂）：seg 243/246 安東尼·喬伊（Anthony Choy）補中譯＋括註（網路查無流通中譯，採音譯；Choy 為華裔姓氏蔡的粵語拼寫）；seg 249 補回漏譯 Space for Peru（降 medium）；seg 250 機構成立年份疑義加註（實際 2001 年，講者稱 1971 年，保留原數字，降 medium）；seg 268 伊萬·阿斯卡尼奧·法哈多（Iván Ascanio Fajardo）補中譯＋括註（原紀錄失效）；seg 269 胡里奧·查莫羅-弗洛雷斯；seg 277/278/279/281 埃內斯托·阿蘭西維亞·利納雷斯／阿蘭西維亞上尉；seg 283 赫爾曼·施羅克·卡斯蒂略、莫羅蓬（Moropon）；seg 287 何塞·拉蒂（José Ratti）；多段數字空格（seg 250/251/252/257/260/266/277/283/285/286/296/299/308）
- ⚠️ topic_05 原有 1 筆 potential_errors（seg 268 Ivan Issa Nanfardo）經查原文已正確，屬失效紀錄
- ⚠️ **新發現待裁決**：seg 250 祕魯官方 UFO 研究機構成立年份，講者稱 1971 年，查證實際為 2001 年（DIFAA），疑講者口誤；依規範保留原數字並加註、降 medium
- [x] topic_06（7 處修訂）：seg 313/317 奧斯卡·聖瑪利亞（Oscar Santa María）／奧斯卡·聖瑪利亞·韋爾塔斯補中譯＋括註（沿用 UFO-14 聖瑪利亞先例）；seg 318 句構疑義改譯「呈報一份美國國防部的文件」（降 medium 加註）；seg 321/357 notes 更新（紀錄失效）；seg 333 notes 更新＋topics.json 補錄（1,500 kilometers→meters，新發現）；seg 347 原文行「cream色的」污染還原為 cream-colored（main.yaml 原文正確，僅草稿污染）
- ⚠️ topic_06 原有 3 筆 potential_errors 全數失效：seg 317 全名、seg 327 La Joya、seg 357 Sukhoi Su-22 原文皆已正確。**新補錄 1 筆：seg 333 1,500 kilometers→meters**
- [x] topic_07（28 段修訂）：seg 361 亞歷杭德羅·基奧內蒂（Alejandro Chionetti）補中譯＋括註；seg 371/372/436 海尼克博士（主表定譯 J·艾倫·海尼克博士）、藍皮書計畫（Project Blue Book）括註依前集慣例；seg 376 米奧蒂（Miotti）艦長；seg 383 愛德華多·阿茲庫伊（Eduardo Azcuy）；seg 389 奧馬爾·帕加尼（Omar Pagani）艦長；seg 407 胡里奧·戈塞納-阿瓜羅；seg 411 馬里亞諾·莫哈特（Mariano Mohabt，拼寫存疑降 medium）；seg 412 弗格森／烏爾丘克／西蒙迪尼三人補中譯；seg 413 吉列爾莫·阿洛伊（Guillermo Aloy）准將；seg 429 prefecture 誤譯「地方行政長官公署」→海岸巡防隊（Prefectura Naval Argentina）；seg 435 海梅（Jaime）；seg 419 括註內半形逗號；年代／年份／時間空格（seg 371/375/384/392/395/396/397/398/399/405/407/408/414/426/438/440/442/450）；冗餘 notes 清理多處
- ⚠️ topic_07 原有 6 筆 potential_errors：seg 361/371/389/405 原文已正確（失效）；seg 410 原文實為 CEFAEE（紀錄更正，譯文已用 CEFAE）；seg 418 Sephora 紀錄更正（實際見於 seg 424/428/430，譯文已逕採 CEFORA）
- **全 7 topic 審畢**。全檔 JSON 驗證通過、無簡體字、無千分位污染、無『』殘留、「通過」僅存正確動賓用法。**待人工確認後始得收尾**（fix_transcription_errors → backfill → export）
