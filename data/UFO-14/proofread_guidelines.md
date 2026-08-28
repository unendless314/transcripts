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
- 本集為 South American Encounters Part 2（UFO-13 之續集）：南美五國（巴西、智利、祕魯、烏拉圭、阿根廷）證人聽證會
- 證人：A. J. Gevaerd（巴西）、Antonio Huneeus（智利）、Oscar Santa María 上校（祕魯）、Anthony Choy（祕魯）、Ariel Sánchez 上校（烏拉圭）、Andrea Simondini（阿根廷）
- 主席／提問：伍爾西眾議員（Woolsey）、基爾派翠克眾議員（Kilpatrick）、庫克眾議員（Cook）、葛瑞福參議員（Gravel）、巴特利特眾議員（Bartlett）
- 共 6 個 topic（seg 1–498），drafts 6 檔
- 本集詞彙表（terminology.yaml）未經校稿，僅供參考；與 UFO-13 已拍板定譯衝突時以 UFO-13 為準

### 跨集沿用裁決（UFO-01～13 已拍板，本集直接沿用）
- 聖瑪利亞上校（Colonel Santa Maria）；全名：奧斯卡·聖瑪利亞·韋爾塔斯（Oscar Santa María Huertas）
- 熱瓦爾德（Gevaerd）先生——網路無流通中譯，採葡語音譯（UFO-13 裁決）
- 安東尼奧·胡尼烏斯（Antonio Huneeus）；胡尼烏斯先生（Mr. Huneeus）（UFO-02 定譯）
- 安東尼·喬伊（Anthony Choy）（UFO-13 裁決，Choy 為華裔姓氏蔡的粵語拼寫）
- 艾瑞爾·桑切斯·魯伊斯（Ariel Sánchez Ruiz）上校／桑切斯（Sánchez）上校（UFO-13；注意 UFO-13 seg 203 主席稱將軍、本人自述退役上校之疑義紀錄）
- 貝爾穆德斯將軍（General Bermúdez，智利 CEFAA 負責人 Ricardo Bermúdez）
- 科拉雷斯島（island of Colares）、拉霍亞基地（La Joya）、飛碟行動（Operation Saucer）
- 西蒙迪尼（Simondini，阿根廷證人 Andrea Simondini，女性；原文誤轉錄 Mr. Gimini 時譯文照正確身分處理）
- CEFAA 統一為「異常空中現象研究委員會」（UFO-13 本集統一；本集詞彙表譯「調查委員會」，校稿時統一改從 UFO-13）——**2026-08-23 人工裁決確認：整系列統一從 UFO-13**
- CEFORA（阿根廷 UFO 研究委員會；UFO-13 用全稱「阿根廷共和國不明飛行物現象研究委員會」時從之）
- Disclosure → 真相揭露；Disclosure Project → 揭露計畫；Top Secret → 最高機密
- 丘盧卡納斯事件（Chulucanas incident，UFO-13 定譯；本集詞彙表 seg 466 譯「丘盧坎事件」，校稿時核對統一）
- J·艾倫·海尼克博士、藍皮書計畫、伍爾西眾議員（UFO-09 補登先例）、基爾派翠克眾議員（UFO-10 先例）
- 引號用「」，內層用『』；千分位半形逗號；數字與中文間空格

### topics.json 既有 potential_errors（校稿時逐筆核對 main.yaml，可能失效）
- topic_01：seg 14 Sephora→CEFORA；seg 60 Mr. Girard→Gevaerd；seg 87 Coronel Willem Jolanda→Uyrangê Hollanda；seg 98 Mr. Junios→Huneeus
- topic_02：seg 124 Mr. Trav→Gevaerd；seg 159 La Jolla→La Joya；seg 193 Ben Mudez→Bermúdez；seg 201 Dr. Choi→Choy；seg 206 Jonathan Wangan→Weygandt；seg 212 Sandra Maria→Santa Maria
- topic_03：seg 336 Mr. Troy→Dr. Choy
- topic_04：seg 361 Jorge Yolanda→Uyrangê Hollanda；seg 400 Richard Winga→Weygandt
- topic_05：seg 408 Virginia→Varginha；seg 409 Roger Lear/James Hurtuk→Roger Leir/J.J. Hur-tak；seg 419 President Maria→Colonel Santa Maria；seg 420 Mr. Gimini→Ms. Simondini
- topic_06：seg 433 Mr. Jordan→Gevaerd；seg 493 General Longania→Onganía

### 本集重點定譯（逐步累積）
- 伍爾西眾議員（Lynn Woolsey）、熱瓦爾德（A. J. Gevaerd）先生、胡尼烏斯（Antonio Huneeus）先生
- CEFORA（阿根廷共和國不明飛行物現象研究委員會，UFO-13 全稱沿用）
- 異常空中現象研究委員會（CEFAA，依 UFO-13 統一；本集詞彙表「調查委員會」棄用）
- 貝爾穆德斯將軍（General Bermúdez）、烏伊蘭吉·奧蘭達（Uyrangê Hollanda）上校（姓氏採 zh.wikipedia 流通「奧蘭達」）
- 琳達·莫爾頓·豪（Linda Moulton Howe，epochtimes 繁中流通；原文 Molton 為轉錄錯誤）
- 飛碟行動、科拉雷斯島、帕拉州、亞馬遜河、洛斯塞里洛斯機場（Los Cerrillos）
- 祕魯（專案慣例，非「秘魯」）
- 基爾派翠克眾議員（Carolyn Cheeks Kilpatrick，UFO-10 先例）、庫克眾議員（Representative Cook）
- 喬伊（Choy）博士＝Anthony Choy（UFO-13 定譯；主席口誤 Choi 照正確拼寫譯）
- 理查德·海恩斯（Richard Haines）博士、NARCAP＝國家航空異常現象研究中心（照原文全名）
- 格里爾揭露計畫（Greer Disclosure Project；史蒂芬·格里爾，UFO-03/04 定譯）
- 喬納森·韋甘德（Jonathan Weygandt）中士、聖馬特奧德萬喬（San Mateo de Huanchor）、拉霍亞空軍基地（La Joya Air Force Base）
- 哈維爾（Javier）（Kilpatrick 同事）
- 埃德溫·凱恩（Edwin Cain）、詹姆斯·福克斯（James Fox）
- 桑切斯（Sanchez）上校（UFO-13 定譯）
- 薩爾加多（Salgado）地區、貝倫（Belém）市、丹尼·希恩（Danny Sheehan）、愛德華多·阿吉雷（Eduardo Aguirre）上校
- 「UFO：即刻資訊自由」運動（UFOs Freedom of Information Now）、巴西國家檔案館、聯合國大會、國防武官辦公室、資訊自由法（FOIA）
- coronel（葡語）＝上校
- 瓦爾任阿事件（Varginha case）、羅傑·萊爾（Roger Leir）博士、J.J.赫塔克（J.J. Hur-tak）博士、約翰·麥克（John Mack）博士、塔里哈（Tarija）、賽勒斯·萬斯（Cyrus Vance）國務卿、月球塵埃計畫（Project Moon Dust）、拉巴斯（La Paz）、鮑勃·普拉特（Bob Pratt）、普羅塔西奧·德·奧利維拉（Protásio de Oliveira）准將（全名 Protásio Lopes de Oliveira，COMAR I 司令；原文 Protasso 為轉錄錯誤，已補錄）、瓜雅拉米林河（Guajará-Mirim River）
- 基奧內蒂（Chionetti）＝UFO-13 阿根廷證人亞歷杭德羅·基奧內蒂（原文 Johnetti 誤聽）
- 丘盧卡納斯事件（Chulucanas，統一 UFO-13；本集詞彙表「丘盧坎事件」棄用）、伊瓜蘇信函（Iguachu letter）、翁加尼亞（Onganía）將軍、布拉沃（Bravo）少校、《遠古外星人》（Ancient Aliens）、《UFO獵人》（UFO Hunters）

### 進度與決策紀錄
- 2026-08-23：校稿啟動，依序處理 topic_01 → topic_06
- [x] topic_01（22 處修訂）：seg 3 伍爾西眾議員補「眾議員」＋括註（UFO-09/10 先例）；seg 12 秘魯→祕魯；seg 14 CEFORA 補 UFO-13 全稱＋括註；seg 24 mediums 改譯「資源」加註（西語 medios 直譯）；seg 27 琳達·莫爾頓·豪（Linda Moulton Howe）補全名＋括註（原文 Molton 轉錄錯誤，topics.json 已補錄）；seg 54 原文行中文污染還原（main.yaml 原文正確，同 UFO-13 seg 347）；seg 60 吉瓦德→熱瓦爾德＋括註（UFO-13 裁決）；seg 87 霍蘭達→奧蘭達＋括註（zh.wikipedia 流通）；seg 96 the dust phenomena 經人工聽音確認為 those phenomena 轉錄錯誤（講者結巴 tho...those），譯文「這些現象」升回 high 加註（topics.json 已補錄）；seg 98 胡紐斯→胡尼烏斯＋括註（UFO-02/13 定譯）；seg 109 CEFAA 補全稱「異常空中現象研究委員會」（UFO-13 統一）；seg 113 貝爾穆德斯將軍補括註；數字空格 9 段（seg 17/26/30/31/50/51/53/55/71/73/89，含 seg 50/73 千分位）
- ⚠️ topic_01 既有 4 筆 potential_errors 全數失效：seg 14 CEFORA、seg 60 Gevaerd、seg 87 Uyrangê Hollanda、seg 98 Huneeus 原文皆已正確（topics.json 已改標失效紀錄）。**新補錄 2 筆：seg 27 Linda Molton→Linda Moulton Howe、seg 96 the dust phenomena→those phenomena（2026-08-23 人工聽音確認）**
- [x] topic_02（28 處修訂）：seg 122 基爾帕特里克→基爾派翠克眾議員＋全名括註（UFO-10 先例）；seg 124 吉瓦德→熱瓦爾德；seg 125 presence of the others 語意補足降 medium；seg 142 伍爾西統一「眾議員」；seg 159 聖瑪利亞指揮官→上校加註＋拉霍亞首現括註；seg 181 海恩斯補括註用正確拼寫 Haines（原文 Haynes 轉錄錯誤）；seg 188 哈維爾補括註；seg 189 中情局→CIA（專案慣例）；seg 197 notes 更新；seg 201/225/232 蔡博士→喬伊（Choy）博士；seg 205 聖馬特奧德萬喬補括註 San Mateo de Huanchor（原文 Huancho 轉錄錯誤）；seg 206 韋甘德補括註；seg 211 史蒂文→史蒂芬、計畫名統一格里爾揭露計畫；seg 255 數據→資料；秘魯→祕魯 7 段（seg 159/190/191/204/205/206/207/209）；數字空格（seg 136/138/173/177/205/278）；NASA/NARCAP 空格（seg 178/181/182）
- ⚠️ topic_02 既有 6 筆 potential_errors：5 筆失效（seg 124 Gevaerd、159 La Joya、193 Bermúdez、206 Weygandt、212 Santa Maria 原文已正確），seg 201 Choi 仍有效。**新補錄 3 筆：seg 181 Haynes→Haines、seg 205 Huancho→Huanchor、seg 225 Choi→Choy**
- ⚠️ 查證筆記：Weygandt 案網路資料實為 1997 年（講者 seg 205 稱 80 年代另有所指，未加註；seg 206 未提年份無矛盾）
- [x] topic_03（20 處修訂）：seg 306 埃德溫·凱恩（Edwin Cain）／詹姆斯·福克斯（James Fox）補中譯＋括註、引號改「」；seg 294/302/310/324 獨立引言『』改「」；seg 322/323 跨段引號改「」；seg 336/346 Choy博士→喬伊博士（seg 336 原文已正確，notes 刪除；seg 346 原文仍 Dr. Troy，notes 保留）；seg 355 Sanchez上校→桑切斯上校＋括註；seg 356 原文 Europe 疑為 Uruguay 誤聽，譯文改烏拉圭加註（topics.json 已補錄）；seg 357 1,300 個案例千分位；數字空格（seg 292/301/305/315/318/326/330/332/333/356/357）
- ⚠️ topic_03 既有 1 筆 potential_errors（seg 336 Mr. Troy）失效：原文已是 Dr. Choy；Dr. Troy 實際見於 seg 346，另立紀錄。**新補錄 2 筆：seg 346 Dr. Troy→Dr. Choy、seg 356 Europe→Uruguay**
- [x] topic_04（11 處修訂）：seg 360 薩爾加多（Salgado）／貝倫（Belém）補括註；seg 361 notes 清理（奧蘭達中譯已定譯）＋2,000/440 千分位；seg 366 coronel 誤譯「中校」→「上校」加註（重要語義修訂）；seg 372/373/386 CIA 空格；seg 378/379 數字空格＋4,500 千分位；seg 389 丹尼·希恩補括註；seg 396 愛德華多·阿吉雷補括註＋數字空格
- ⚠️ topic_04 既有 2 筆 potential_errors 全數失效：seg 361 Uyrangê Hollanda、seg 400 Jonathan Weygandt 原文已正確。無新補錄
- [x] topic_05（20 處修訂）：seg 407 格瓦德→熱瓦爾德（原文 Gavard 誤聽補錄）；seg 411 約翰內蒂→基奧內蒂（Chionetti，原文 Johnetti 誤聽補錄）；seg 413 cover story 改「託詞」；seg 418 崔博士→喬伊博士＋聖馬托德萬喬統一為聖馬特奧德萬喬（San Mateo de Huanchor，同 seg 205；原 notes「應為La Joya」判斷有誤已改）；seg 422 格瓦德→熱瓦爾德（原文 Gimini 語境指 Gevaerd，補錄）；seg 423/424/425 威廉·約蘭達→烏伊蘭吉·奧蘭達（原文 William Jolanda 誤聽補錄，含 seg 424/425）；seg 424 普羅塔索→普羅塔西奧（原文 Protasso 應為 Protásio，人工查證確認後補錄）；seg 423 隊長→上尉（同 seg 366）、Belen→貝倫（Belém）、英呎→英尺；seg 425 30多名→36 名（three dozen）；seg 409 Virginia 轉錄錯誤加註（譯文原已正確採 Varginha）；多段 notes 清理（407/408/409/410/411/414/416/419/420/427 冗餘 terminology 說明）；數字空格（seg 407/408/409/412/417/418/423/425）
- ⚠️ topic_05 既有 4 筆 potential_errors 全數失效：seg 408 Varginha、409 Leir/Hur-tak、419 Santa Maria、420 Simondini 原文皆已正確。**新補錄 8 筆：seg 407 Gavard→Gevaerd、409 Virginia→Varginha（兩處）、411 Johnetti→Chionetti、418 Troy→Choy、418 San Mato de Huancho→San Mateo de Huanchor、422 Gimini→Gevaerd、423（含 424/425）William Jolanda→Uyrangê Hollanda、424 Protasso→Protásio de Oliveira（2026-08-23 人工查證確認，譯名同步改普羅塔西奧）**
- [x] topic_06（31 處修訂）：seg 433 蓋瓦德→熱瓦爾德＋數據→資料＋引號改「」；seg 441 notes 改寫（原文 Ben Mudez 補錄）；seg 446/461/489 通過→透過＋notes 補全名；seg 449/464/467/491 秘魯→祕魯（5 處）；seg 450 『衝突』改「」＋notes 清理；seg 453 notes 清理；seg 455/454/442/443 獨立引言『』改「」（6 處）；seg 457/460 蔡伊博士→喬伊博士（原文 Choi 補錄，460 承接 459 斷句）；seg 459 基爾帕特里克→基爾派翠克眾議員；seg 462 數據→資料；seg 466 丘盧坎→丘盧卡納斯（統一 UFO-13，原文 Chulucan 補錄）；seg 469 庫克議員→庫克眾議員＋notes 清理；seg 477 巴特利特議員→眾議員；seg 487 布拉沃補括註＋notes 清理；seg 493 簡體字「那种」→「那種」＋引號改「」＋notes 清理；數字空格（seg 433/435/452/461/467/469/470/473/479/480/481/482/484/487/489/490/491/492/497）
- ⚠️ topic_06 既有 2 筆 potential_errors 全數失效：seg 433 Gevaerd、493 Onganía 原文已正確。**新補錄 4 筆：seg 441 Ben Mudez→Bermúdez、457 Dr. Choi→Dr. Choy、460 Choi→Choy、466 Chulucan→Chulucanas**
- **全 6 topic 審畢**（合計約 112 處修訂、新補錄轉錄錯誤 16 筆、失效紀錄 13 筆）。全檔 JSON 驗證通過、無簡體字殘留、無千分位污染、無『』殘留、「通過」僅存正確動賓用法。**待人工確認後始得收尾**（fix_transcription_errors → backfill → export）
- ✅ 人工裁決事項全數完結（2026-08-23）：(1) seg 96 人工聽音確認 the dust＝講者結巴 tho...those，補錄 the dust phenomena→those phenomena；(2) CEFAA 全稱整系列統一從 UFO-13「異常空中現象研究委員會」；(3) 丘盧卡納斯事件統一 UFO-13 定譯；(4) seg 424 查證確認 Protásio Lopes de Oliveira，補錄 Protasso→Protásio、譯名改普羅塔西奧。**無未決事項**
- ✅ 收尾：fix_transcription_errors 已執行（2026-08-23，人工授權）。38 筆紀錄中 19 筆替換成功（18 段：seg 27/96/181/201/205/225/346/356/407/411/418×2/422/423/424/441/457/460/466），19 筆 not-found 全為失效紀錄。執行前發現 seg 201 紀錄 error_text 原寫「Dr. Choi」與實際原文「I want to say Choi」不符，已修正紀錄後套用。語義級比對（git HEAD vs 修後）確認僅此 18 段 source_text 變更；main.yaml 格式同步洗回 width=inf 長行（與 UFO-01/02/04 一致）。backfill/export 仍待全 20 集校稿完成後統一執行
