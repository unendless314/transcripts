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

### 本集概況（2026-08-23 啟動）
- 本集為 A Global Phenomenon Part 1（下集 UFO-16）：多國證人就本國官方／軍方 UFO 調查作證
- 證人：羅貝托·皮諾蒂博士（Dr. Roberto Pinotti，意大利）、孫式立博士（Sun Shili，中國）、格蘭特·卡麥隆（Grant Cameron，加拿大）、尼克·波普（Nick Pope，英國）、安東尼奧·胡尼烏斯（Antonio Huneeus，報告法國與俄國調查）
- 提問者（依 topic_07 摘要）：庫克眾議員（Cook）、基爾派翠克眾議員（Kilpatrick）、伍爾西眾議員（Woolsey）、巴特利特眾議員（Bartlett）；主席主持開幕與末段提問
- 共 7 個 topic（seg 1–723），drafts 7 檔；topic_07（seg 356–723，368 段）最大，須分批讀取審訂
- 本集詞彙表（terminology.yaml）未經校稿，僅供參考；與主表或已拍板定譯衝突時從主表／既有裁決

### 跨集沿用裁決（UFO-01～14 已拍板，本集直接沿用）
- 安東尼奧·胡尼烏斯（Antonio Huneeus）；胡尼烏斯先生（Mr. Huneeus）（UFO-02 定譯）
- 格蘭特·卡麥隆（Grant Cameron）、保羅·赫勒（Paul Hellyer）、威爾伯特·B·史密斯（Wilbert B. Smith）（主表）
- 萬尼瓦爾·布希博士（Dr. Vannevar Bush，UFO-10；布希非布什）
- J·艾倫·海尼克博士（Dr. J. Allen Hynek，主表）
- 藍皮書計畫（Project Blue Book）、羅斯威爾事件（Roswell）
- 藍道申森林事件（Rendlesham Forest incident，UFO-05/06 定譯）
- 萊特-帕特森空軍基地（Wright-Patterson AFB，主表）
- Top Secret → 最高機密；Cover-up → 真相掩蓋；Disclosure（揭露運動語境）→ 真相揭露
- Being/Beings → 存有；飛彈（非導彈）；網路（非網絡）；太空（非航天）
- 伍爾西眾議員（UFO-09 補登先例）、基爾派翠克眾議員（UFO-10 先例）、庫克眾議員、巴特利特眾議員（Roscoe Bartlett，主表全名羅斯科·巴特利特）
- 資訊自由法（FOIA，主表）；英國國防部（MOD／Ministry of Defence）
- 引號用「」，內層用『』；千分位半形逗號；數字與型號前後空格（年份除外）；括號用全形；縮寫標註「中文（縮寫）」格式

### topics.json 既有 potential_errors（校稿時逐筆核對草稿原文，可能已失效）
- topic_02：seg 25 `Centro Fologico Nazionale`→Centro Ufologico Nazionale；seg 31 `Italian Hermes Netto Third Myself Brigade`→Nike-Hercules 3rd Missile Brigade；seg 34 `Kuhn`→CUN；seg 39 `Japan`→GEPAN
- topic_03：seg 65 `Dr. Schille?`→Dr. Shili?；seg 105 `Mr. Chen Juesheng, Wang Gancha`→Qian Xuesen, Wang Ganchang（錢學森、王淦昌）
- topic_04：seg 171 `Royal Canadian Monopolis`→Royal Canadian Mounted Police；seg 188 `Dr. Robert Saubacher`→Sarbacher
- topic_05：seg 258 `Project Condyne`→Project Condign
- topic_06：seg 300 `Val-en-Salle`→Valensole；seg 318 `Trans-Improvance`→Trans-en-Provence
- topic_07：seg 443 `Mr. Pernati`→Pinotti；seg 476 `Mr. Hucsini`→Huneeus；seg 522 `Mr. Shelley`→Shili

### 本集重點定譯（逐步累積）
- **義大利**（Italy）：全書統一，非「意大利」（台灣慣用國名；前 14 集無此國名先例，本集確立）
- **UFO 術語統一**：本集譯稿原大量使用「幽浮」（62 處，集中 topic_02），與 UFO-01～14 慣例（不明飛行物／UFO）不符，校稿時一律改為 UFO（幽浮學家→UFO 學家、國家幽浮研究中心→國家 UFO 研究中心等）
- 年份、數字與中文間加空格（從 UFO-13/14 校稿後實際慣例：「1978 年」「超過 12,000 起」；主表檔頭「年份除外」註記與實務不符，以校稿後各集為準）
- 掌聲標記：（掌聲），全形括號（UFO-01 先例；本集譯稿原用【掌聲】，遇則改）
- 羅貝托·皮諾蒂博士（Dr. Roberto Pinotti）、國家 UFO 研究中心（CUN，Centro Ufologico Nazionale）、義大利空軍（Aeronautica Militare）、安全部門（Reparto Generale Sicurezza）
- 朱利奧·安德烈奧蒂（Giulio Andreotti）、米開朗基羅·普里維特拉上校（Colonel Michelangelo Privitera）、阿爾多·奧利維羅將軍（General Aldo Oliveiro）、科拉多·巴爾杜奇蒙席（Monsignor Corrado Balducci）
- 古列爾莫·馬可尼（Guglielmo Marconi）、菲利普·科索（Philip Corso）、卡斯泰爾波爾齊亞諾（Castelporziano）
- 義大利太空總署（Italian Space Agency）、歐洲太空總署（European Space Agency）、國際太空聯合會（IAF）
- 星際外交（exodiplomacy）、上議院（House of Lords）
- 孫式立（Sun Shili，本名中譯逕用）、世界華人 UFO 聯合會、中國 UFO 研究會、龍的傳人、天人合一、神州
- 錢學森（Qian Xuesen）、王淦昌（Wang Ganchang）、陳景潤（Chen Jingrun）——原文 Chen Juesheng／Wang Gancha 為誤聽
- 鳳凰山事件（Fengshan Mountain，貴陽孟照國事件，網路流通）、北京曹公事件（北京校長曹公遭劫持案，網路有流通紀錄）；飛山事件、陸溪農場事件無流通資料，直譯
- 外星通訊者（alien communicators）、碟形載具（disc-shaped artifact）、知情權／發現權（right to know／right to discover）
- 信息→訊息（seg 125/126，台灣用語）；航天→航太（aerospace）
- 威爾伯特·B·史密斯（Wilbert B. Smith；原文 Wilbur 為誤聽，seg 182/195/201）
- 羅伯特·薩巴赫博士（Dr. Robert Sarbacher；原文 Saubacher 為誤拼，seg 189/194/196/199/200/201/204/205 共 8 處）
- 斯坦頓·弗里德曼（Stanton Friedman）、比爾·斯坦曼（Bill Steinman）、亞瑟·布里奇（Arthur Bridge）、布萊恩·沃克（Brian Walker）
- 艾瑞克·沃克博士（Dr. Eric Walker，主表）、賓州州立大學（Penn State University）、國防分析研究所（IDA）、國家科學基金會（NSF）、研究與發展委員會（Research and Development Board）、加拿大國防研究委員會（Defense Research Board）、國家研究委員會（National Research Council）
- 《星期六晚郵報》（Saturday Evening Post）、斯卡利（Frank Scully，《Behind the Flying Saucers》作者）、阿茲特克（Aztec, New Mexico，1948 年墜毀傳聞地點）、布雷姆納博士（Dr. Bremner，音譯）
- hardware 統一譯「硬體」；hyper-high/ultra-high frequency＝特高頻／超高頻
- 本集人名原則重申：譯稿原大量保留人名原文，校稿一律中譯＋首次括註原文（專案慣例：人名全部統一中譯）
- FBI 等知名縮寫逕用原文，不加中文註
- 尼克·波普（Nick Pope）；英國國防部（Ministry of Defence）；國防情報人員（Defence Intelligence Staff，從 UFO-05 先例）
- 藍道申森林事件（從 UFO-05/06 定譯；本集譯稿原「倫德爾沙姆」已改）、本特沃特斯事件（Bentwaters incident）
- 康代因計畫（Project Condign；原文 Condyne/Condine 誤聽 seg 263/267/272/283，seg 258 已正確）
- 潘尼斯頓中士（Penniston，從 UFO-05 人工裁決；本集譯稿原「彭尼斯頓」已改）、伯勞斯中士（Burroughs）
- 「不具國防意義」（no defense significance，UFO-05 同一用語先例）
- 定向能武器（directed energy weapons，非「定向能源武器」）；飛航安全（air safety）
- 民航局（Civil Aviation Authority）、聯邦航空總署（FAA）、英國國家檔案館（UK's National Archives）
- 音效標記一律全形括號：（掌聲）、（笑聲）
- 羅貝爾·加萊（Robert Galley，1974 年法國國防部長；原文 Galli 誤聽）、克勞德·波埃爾（Claude Poher）、雷納托·尼科萊（Renato Nicolai）、布尼亞斯教授（Professor Bounias；原文 Buñaz 誤聽）、讓-雅克·貝拉斯科（Jean-Jacques Velasco）、德尼·萊蒂（Denis Letty）、阿蘭·布迪埃（Alain Boudier）
- 法國機構：國家憲兵隊（National Gendarmerie）、國家國防高等研究院（IHEDN）、法國太空總署 CNES（原文 CNAS/CNS 皆誤聽）、不明航空現象研究組 GEPAN→GEIPAN、SEPRA（重返大氣層物體研究處）、COMETA 報告、西格瑪委員會（Sigma Commission）、3AF＝法國航空天文協會
- 普羅旺斯特朗（Trans-en-Provence；原文 Transan-Provence 誤聽、Valle 應為 Var 瓦爾省）、瓦朗索勒（Valensole）
- 彼得羅扎沃茨克（Petrozavodsk；原文 Petrosovodsk 誤聽）、卡累利阿、卡普斯京亞爾、阿斯特拉罕州、烏索沃（Usovo）
- 費利克斯·西格爾（Felix Siegel，俄羅斯 UFO 學之父）、弗拉基米爾·科瓦廖諾克（Vladimir Kovalyonok）、帕維爾·波波維奇（Pavel Popovich）、禮炮 6 號太空站
- 威廉·羅傑斯（William Rogers）、安德烈·葛羅米柯（Andrei Gromyko）；馬姆斯特羅姆空軍基地（Malmstrom AFB，從 UFO-07/08 定譯）
- 核武器→核武（專案慣例）；引號統一「」（本集譯稿原用『』處已改）
- 磁鐵計畫（Project Magnet，威爾伯特·史密斯的加拿大飛碟研究計畫；無先例，本集確立）
- UFO 光球（Foo Fighters，從本集詞彙表；譯稿原「幽靈戰鬥機」已改）
- 豪特中尉（Lieutenant Haut，Walter Haut，羅斯威爾事件基地新聞官；原文 Hoth 誤聽）
- 蓋博上將（General Gabriel；原文 Gabrielle 誤聽，主表 UFO-06 定譯）
- 丹尼斯·斯泰西（Dennis Stacey）、弗蘭克·斯卡利（Frank Scully）
- 議事稱謂定譯：庫克眾議員、基爾派翠克眾議員、巴特利特眾議員、主席女士（Madam Chair）
- 主席多次誤讀證人姓名（Pernati/Pananti/Penati/Panetti→Pinotti、Pananti、Paul→Pope、Shelley/Schille→Shili）：譯文一律照正確姓名翻譯，notes 標記

### 進度與決策紀錄
- 2026-08-23：校稿啟動，建立本檔；依序處理 topic_01 → topic_07
- 2026-08-23：topic_01 審畢（seg 1–22）。修訂 1 筆：seg 2 移除原文所無的「完整」之意。無轉錄錯誤
- 2026-08-23：topic_02 審畢（seg 23–67）。修訂約 30 筆，重點：幽浮→UFO 全數統一、意大利→義大利、年份／數字空格、海尼克從 UFO-11 先例、掌聲改全形括號、seg 36 句構重整。topics.json：topic_02 既有 4 筆全數失效（seg 25/31/34/39 原文已正確），新補錄 2 筆（seg 35 darling-like→disc-like、seg 54 Castelga-Porziano→Castelporziano）；topic_03 seg 65 Schille 紀錄失效（原文已正確）；topic_07 新補錄 seg 626 Mr. Schille→Mr. Shili。另發現草稿 seg 57 原文行混入「Italian政府」，main.yaml 原文正確（Italian government），譯文不受影響
- 2026-08-23：topic_03 審畢（seg 68–142）。修訂約 25 筆，重點：幽浮→UFO、信息→訊息、資深學者、卡梅隆→卡麥隆（主表）、知情權／發現權統一、seg 110 陳覺生→錢學森（同 seg 105 誤聽）。topics.json：seg 105 紀錄失效（原文已正確），新補錄 seg 110 Chen Juesheng→Qian Xuesen。查證：鳳凰山＝孟照國事件、曹公事件皆有網路流通紀錄；飛山、陸溪農場事件無流通資料
- 2026-08-23：topic_04 審畢（seg 143–228）。修訂約 40 筆，重點：人名全數中譯（史密斯、布希、薩巴赫、赫勒、弗里德曼等）、hardware→硬體、簡體字「现在」修正、半形括號改半形標點、FBI 逕用。topics.json：seg 171/188 紀錄失效，新補錄 10 筆 Saubacher/Wilbur 誤拼（seg 182/189/194/195/196/199/200/201/204/205）
- 2026-08-23：topic_05 審畢（seg 229–286）。修訂約 25 筆，重點：倫德爾沙姆→藍道申（UFO-05/06 定譯）、彭尼斯頓→潘尼斯頓（UFO-05 裁決）、定向能武器、國防情報人員（UFO-05 先例）、不具國防意義（UFO-05 用語）、年份空格、音效標記全形化。topics.json：seg 258 紀錄失效，新補錄 4 筆 Condyne/Condine（seg 263/267/272/283）
- 2026-08-23：topic_06 審畢（seg 287–355）。修訂約 35 筆，重點：意大利→義大利、幽浮學→UFO 學、核武、『』→「」、人名全數中譯、透過。topics.json：seg 300/318 紀錄失效，新補錄 7 筆（seg 298 Galli→Galley、seg 304 CNAS→CNES、seg 307 Transan-Provence/Valle→Trans-en-Provence/Var、seg 312 Buñaz→Bounias、seg 320 CNS→CNES、seg 332 Petrosovodsk→Petrozavodsk）
- 2026-08-23：topic_07 審畢（seg 356–723，分四批）。修訂約 60 筆，重點：人名全數中譯（波普、卡麥隆、皮諾蒂、胡尼烏斯、孫式立、蓋博上將等）、議事稱謂定譯、主席誤讀姓名照正確譯名處理、『』→「」、音效標記全形化、義大利／核武／航太、磁鐵計畫、UFO 光球、豪特中尉。topics.json：seg 443/476/522 紀錄失效（誤聽實際段號有誤），新補錄 14 筆（seg 452/467/549/594 Pinotti 誤讀、seg 494 Paul→Pope、seg 503 Gabrielle→Gabriel、seg 562 antities→entities、seg 598 Hoth→Haut、seg 614/617 Netto→Nike、seg 658 medallurgist→metallurgist、seg 662 Wilbur→Wilbert、seg 673 Heineck→Hynek、seg 696 Shelley→Shili）；另 seg 597/670 草稿原文行混入中文，main.yaml 原文正確
- 2026-08-23：**全 7 個 topic 審畢（seg 1–723 共 723 段）**。全部 → 行 JSON 驗證通過、topics.json 合法、殘留掃描（幽浮／意大利／『／【／千分位／禁用詞）乾淨。累計新補錄轉錄錯誤 41 筆、失效 14 筆。⚠️ 依收尾流程人工確認門檻：暫停待人工裁決後始得執行 fix_transcription_errors / backfill / export
- 2026-08-23：seg 110 人工聽音裁決：Chen Juesheng 確認為錢學森（中文發音可辨），confidence 恢復 high，移除查證揣測註記——尊重會場發言，不做過多驗證
