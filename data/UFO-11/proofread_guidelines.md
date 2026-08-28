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

### 本集概況
- 主題：羅斯威爾事件 Part 1（Roswell Part 1）；證人：唐·施密特（Don Schmidt，研究者）、史丹頓·弗里德曼（Stanton Friedman，核物理學家）、凱文·蘭德爾中校（Lt. Col. Kevin Randall，軍事情報退役軍官）、傑西·馬塞爾二世（Col. Jesse Marcel Jr., M.D.）、傑西·馬塞爾三世（Jesse Marcel III）、丹妮絲·馬塞爾（Denise Marcel）
- 草稿 5 檔：topic_01（77 → 行）、topic_02（111）、topic_03（114）、topic_04（167）、topic_05（**120KB、543 → 行，大檔，務必分段讀取審訂**）
- 本集為羅斯威爾事件核心集，人名、部隊番号、基地名密集，跨集一致性（尤其弗里德曼、羅斯威爾、萊特-帕特森）務必比對主表與前集定譯
- 注意：UFO-07～10 已裁決「導彈→飛彈」；本集 terminology.yaml 仍寫「白沙導彈靶場」，須查主表與網路流通定譯後裁決（White Sands Missile Range）

### topics.json 既有 potential_errors（校稿時須逐筆處理，注意可能有失效紀錄）
- topic_01：seg 29 `The tractors` → Detractors；seg 45 `Video writers` → Editorial writers；seg 71 `Cama Glocklin` → Kyle MacLachlan
- topic_02：seg 107 `Plains of Santa Augusta` → Plains of San Agustin；seg 111 `Don Belinner` → Don Berliner；seg 152 `Walter Holt, Hout` → Walter Haut
- topic_03：seg 202 `Frederick Pohl` → Frederik Pohl；seg 260 `Walter Hott` → Walter Haut；seg 261 `aid to camp` → aide-de-camp
- topic_04：seg 382 `a Lafayette Passion` → a lifelong passion；seg 388 `519th Composite` → 509th Composite；seg 393 `As the only NT` → As an ENT；seg 398 `head to home Louisiana` → head to Houma, Louisiana；seg 452 `weather or a blue night` → weather or a Mogul balloon
- topic_05：seg 507 `Lieutenant Colonel Hippler` → Quintanilla；seg 531 `Dick DiMatto` → Dick D'Amato；seg 552 `re-sanctions` → inner sanctums；seg 691 `Congresswoman Linda Wolfson` → Lynn Woolsey；seg 739 `Captain Sheridan Cavett` → Cavitt；seg 773 `Plane Close... Cabot` → Plainclothes... Cavitt；seg 876 `went to McNeil` → MacDill

### 本集重點定譯（依 terminology.yaml，校稿中如有增刪修訂回寫此節）
- 羅斯威爾事件／羅斯威爾陸軍航空基地；509 轟炸大隊／509 混合轟炸大隊
- 飛碟（1947 新聞稿用語）、氣象氣球、莫古爾計畫（Project Mogul）
- 傑西·馬塞爾（Jesse Marcel，情報官）；布蘭查德上校（Colonel Blanchard）；雷米將軍（General Roger Ramey）；托馬斯·（傑佛遜·）杜博斯上校（Colonel Thomas Jefferson Dubose）
- 史丹·弗里德曼／史丹頓·弗里德曼（Stanton Friedman，跨集統一「弗里德曼」，見 UFO-10 裁決）
- 康登委員會（Condon Committee）、藍皮書計畫、藍皮書特別報告 14 號、科羅拉多大學研究報告
- 史蒂芬·希夫眾議員（Stephen/Steven Schiff）；比爾·理查森（Bill Richardson，新墨西哥州前州長）
- J·艾倫·海尼克博士（Dr. J. Allen Hynek）；UFO 研究中心（CUFOS）；威斯康辛協和大學
- 三位一體核試驗場（Trinity site）；白沙導彈靶場（White Sands Missile Range，導彈/飛彈待裁決）；萊特機場（Wright Field）／萊特-帕特森空軍基地
- 《科羅納墜毀事件》（Crash at Corona）、《羅斯威爾 UFO 墜毀事件》（UFO Crash at Roswell）、《絕密計畫》（Majestic，書名）
- 憲兵司令（Provost Marshal）、反情報部隊（CIC）、薛瑞登·卡維特（Sheridan Cavitt）
- 沙格港事件（Shag Harbor）、聖奧古斯丁平原（Plains of San Agustin）、51 區

### 進度與決策紀錄
- 2026-08-12：校稿啟動，依序處理 topic_01 → topic_05
- [x] topic_01（11 處修訂）：seg 22/36 Roswell 保留原文改中譯羅斯威爾；seg 40 notes 改寫裁決；seg 41 希夫補括註（Stephen Schiff）；seg 43 墜落假人→碰撞測試假人；seg 44 傑·雷諾補括註（Jay Leno）；seg 47 get away with 譯文潤飾；seg 50 德傑諾瓦補括註（Joseph DeGenova）；seg 62 賀拉修→霍拉旭（朱生豪譯本通行）；seg 67 句構改寫並補括註（Dr. J. Allen Hynek／Center for UFO Studies）；seg 71 麥克拉克蘭→麥克拉克倫（zh 維基流通）、尤肯→尤卡姆（流通不一，暫採尤卡姆，待人工裁決）、書名補括註。**新發現轉錄錯誤 seg 67 Heineck→Hynek，已補錄 topics.json**
- ⚠️ 本集 topics.json 原有 3 筆 topic_01 potential_errors（seg 29/45/71）經查 main.yaml 原文皆已正確，屬失效紀錄
- [x] topic_02（24 處修訂）：seg 78 佛烈德曼→弗里德曼（UFO-10 裁決）；seg 90 take wax→take a whack 轉錄錯誤補錄、大放厥詞→大肆批評、降 medium；seg 101/102 核武器→核武；**裁決：白沙飛彈靶場（White Sands Missile Range），導彈→飛彈沿用 UFO-10 裁決、zh 維基 zh-tw 同採飛彈（seg 102/103），並補括註 Trinity site**；seg 107 Corona→科羅納補括註、Roswell 陸軍機場→羅斯威爾陸軍航空基地；seg 108 亞瑟·坎貝爾補括註；seg 109 阿茲特克補括註；seg 111 唐·伯林納補括註（UFO-10 定譯）、書名補括註；seg 120 傑西·馬塞爾補括註；seg 123/124 Houma→霍馬；seg 129 gray basket notes 裁決改寫；seg 138 貝米吉補括註；seg 139/145 比爾·摩爾補括註；seg 141 休伊·格林補括註；seg 151 Editor & Publisher 補括註；seg 152/156 華特·豪特補括註；seg 160/164 布拉澤爾、卡里索索補括註；seg 169 補括註＋原文 Raimi→Ramey 補錄；seg 173 Don→唐；seg 180 中校→上校（Colonel 誤譯）。**新發現轉錄錯誤補錄 topics.json：seg 90 wax→whack、seg 169 Raimi→Ramey，共 2 筆**
- ⚠️ topic_02 原有 3 筆 potential_errors（seg 107/111/152）經查 main.yaml 原文皆已正確，屬失效紀錄
- [x] topic_03（30 處修訂）：seg 196 凱文·蘭德爾補括註；seg 202 弗雷德里克·波爾／喬治·R·R·馬丁補括註；seg 203 唐·施密特補括註；seg 207 SAC 補括註；seg 209 法蘭克·喬伊斯補括註；seg 212 克里夫·史東補括註；seg 216 卡里索索中譯（與 topic_02 一致，原文 Carrizoza 拼錯已補錄）；seg 217/229/240/241/243/245 布拉澤爾中譯；seg 218/220 麥克／比爾中譯；seg 231/233/246/247 艾德溫·伊斯利補括註；seg 245 馬里昂·斯特里克蘭補括註；seg 252 傑西·馬塞爾補「一世」區別二世並補括註；seg 256/268 派屈克·桑德斯補括註；seg 257 署名帕特（Pat）；seg 259/274 桑德斯／哈里斯中譯；seg 260/261/262/275/279 豪特中譯（原文 Hott／Haught 拼寫錯誤補錄）；seg 267 理查·哈里斯補括註；seg 282 克雷里補括註；seg 290 Moore→摩爾、疑指莫古爾工程師 Charles Moore 查證待人工確認、降 medium。**新發現轉錄錯誤補錄 topics.json：seg 261/262 Hott→Haut、seg 275 Haught→Haut、seg 279 Walter Haught→Walter Haut（2 處）、seg 216 Carrizoza→Carrizozo，共 5 筆**
- ⚠️ topic_03 原有 3 筆 potential_errors（seg 202/260/261 aide-de-camp）經查 main.yaml 原文皆已正確，屬失效紀錄（seg 261 另有真實錯誤 Hott 已補錄）
- [x] topic_04（33 處修訂）：**Colonel 誤譯中校全面修正→上校（seg 306/310/321/420）**；seg 304/306/312/369/371-373/375/460 馬塞爾中譯（seg 372 姓氏討論段保留原文括註）；seg 307/419 丹妮絲補括註；seg 313 中隊→大隊；seg 317/411 LSU→路易斯安那州立大學；seg 318 倫維爾號補括註；seg 324 福斯特牧場補括註；seg 325/328 查維斯郡補括註；seg 329 薛瑞登·卡維特補括註（main.yaml 原文已是正確拼寫 Cavitt）；seg 354 Fort Worth→沃斯堡；seg 364 史丹·佛烈德曼→史丹·弗里德曼（deprecated）；seg 375/420/421 一世／二世補齊（seg 420/421 跨段句重構）；seg 392/426 克蘭西補括註；seg 393 ENT 主語修正為其父、降 medium；seg 398 Houma→霍馬；seg 399 薇歐（Vio）補括註；seg 431 海倫娜天文協會補括註；seg 439 肯特·傑弗里斯補括註；seg 458/463 史丹頓·弗里德曼補括註。**新發現轉錄錯誤補錄 topics.json：seg 413 rousal→Roswell、seg 447/449 eye beam→I-beam，共 3 筆**
- ⚠️ topic_04 原有 5 筆 potential_errors（seg 382/388/393/398/452）經查 main.yaml 原文皆已正確，屬失效紀錄
- [x] topic_05（120KB 大檔、543 → 行，分 4 段讀取審訂；64 處修訂＋topics.json 補錄 9 筆）：seg 470 理查·歐康納補括註；seg 474 梅里爾·庫克補括註；seg 477/571 唐納德·施密特；seg 483/501/618 凱文·蘭德爾（中校稱謂統一，seg 578/618 原「上校」改中校）；seg 490/492 原文 Brazzo→Brazel 補錄、雪莉中譯；seg 502 A-Tech 疑指 ATIC 加註；seg 503/654/664/712/811 破碎句構 notes 裁決改寫；seg 507 金塔尼拉補括註（紀錄失效）；seg 510/507 notes 清理；seg 520 Jenny 口誤裁決；seg 522/523 丹妮絲／傑西·馬塞爾二世；seg 531 迪克·達馬托補括註（紀錄失效）；seg 543 Majestic 書名補括註；seg 544 惠特利·史崔伯補括註；seg 573 萊斯·阿斯平補括註；seg 574/584 巴里·戈德華特補括註；**seg 575 克林頓→柯林頓（UFO-10 慣例）**；seg 578 理查·韋弗補括註；seg 580 唐；seg 594 安全幕幕語病；seg 600 托馬斯·杜博斯准將補括註（DeBose 異拼註記）；seg 606/611 等馬塞爾中譯；seg 625 肯尼斯·阿諾德補括註＋signing→sighting 補錄；seg 671 store systems→solar systems 補錄；seg 691 琳恩·伍爾西（紀錄失效，未改譯）；seg 708/711 Haught→Haut 補錄、湯姆·凱里補括註；seg 712 理查·哈里斯／豪特中譯；seg 727/856 right field→Wright Field 補錄；seg 728/731 亞瑟·艾克森補括註、外國技術部門補括註；seg 739/773 薛瑞登·卡維特中譯（2 筆紀錄失效）；seg 758 Smith→Schmidt 主席口誤註記；seg 765/768/769/782 查維斯郡／馬塞爾／威廉·布蘭查德；seg 771 白沙飛彈靶場；seg 776 briefing→debris 補錄；seg 798 雪莉；seg 811 傑西·馬塞爾一世；seg 814/823/831 馬塞爾先生；seg 819 伊斯利；seg 832 麥克·布拉澤爾；seg 876 麥克迪爾補括註（紀錄失效）；seg 884/887 凱文／馬塞爾；seg 890/893/894/897/910 卡維特、路易斯·里基特補括註；seg 969/970 卡蘿琳；seg 1005 雷米將軍子句語序修正。**新發現轉錄錯誤補錄 topics.json：seg 490/492 Brazzo→Brazel、seg 625 signing→sighting、seg 671 store systems→solar systems、seg 708/711 Haught→Haut、seg 727/856 right field→Wright Field、seg 776 briefing→debris，共 9 筆**
- ⚠️ topic_05 原有 7 筆 potential_errors（seg 507/531/552/691/739/773/876）經查 main.yaml 原文皆已正確，屬失效紀錄

### 總檢查（2026-08-12）
- [x] 全部 1,012 個 → 行 JSON 合法（77+111+114+167+543）；topics.json 合法
- [x] git diff 無非 → 行異動（5 檔皆然）
- [x] 殘留掃描零命中：`\d，\d`、佛烈德曼、克林頓、導彈（正文）、網絡／絕密／核子物理／通過；譯文（括註外）無英文人名殘留（僅存 UFO／DVD／B-29／V-2／SAC／CIC／FAA／LSU／KGFL／CBS 等允許縮寫）
- [x] 弗里德曼全 4 處統一（topic_02 seg 78、topic_04 seg 364/458/463）

### potential_errors 總結（收尾用）
- **有效紀錄共 21 筆**（校稿中補錄，fix_transcription_errors 收尾時執行）：
  - topic_01：seg 67 Heineck→Hynek
  - topic_02：seg 90 take wax→take a whack、seg 169 Raimi→Ramey
  - topic_03：seg 216 Carrizoza→Carrizozo、seg 261/262 Hott→Haut、seg 275 Haught→Haut、seg 279 Walter Haught→Walter Haut（2 處）
  - topic_04：seg 413 rousal→Roswell、seg 447/449 eye beam→I-beam
  - topic_05：seg 490/492 Brazzo→Brazel、seg 502 A-Tech→ATIC（人工聽音確認）、seg 625 signing→sighting、seg 671 store systems→solar systems、seg 708/711 Haught→Haut、seg 727/856 right field→Wright Field、seg 776 briefing→debris
- **失效紀錄共 21 筆**（原有紀錄，main.yaml 原文早已正確，收尾時標記、不執行修正）：
  - topic_01：seg 29/45/71（3 筆）
  - topic_02：seg 107/111/152（3 筆）
  - topic_03：seg 202/260/261 aide-de-camp（3 筆；seg 261 另有真實錯誤 Hott 已另行補錄）
  - topic_04：seg 382/388/393/398/452（5 筆）
  - topic_05：seg 507/531/552/691/739/773/876（7 筆）

### 人工裁決紀錄（2026-08-12）
1. ✅ seg 71 Dwight Yoakam 中譯：人工確認採校稿提案「德懷特·尤卡姆」
2. ✅ seg 290「Moore」：人工確認照校稿處理（譯「摩爾」降 medium，疑指莫古爾工程師 Charles Moore 之註記保留）
3. ✅ seg 502「A-Tech」：**人工聽音確認確為 ATIC**——譯文已改「空軍技術情報中心（ATIC）」，topics.json 已補錄；main.yaml 原文已由人工逕行修正（A-Tech→ATIC），故收尾時此筆紀錄視同失效、不重複執行
4. ✅ 本集 terminology.yaml「白沙導彈靶場」已回寫「白沙飛彈靶場」；主表回寫留待收尾時一併評估
