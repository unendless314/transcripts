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

### 譯名裁決紀錄

**Rendlesham Forest incident → 藍道申森林事件**（2026-08-10 人工裁決）：網路查證——百度百科條目標題、知乎／搜狐／Bilibili 大眾媒體普遍用「藍道申」，流通度壓倒性較高；維基繁中條目標題「倫德爾舍姆森林事件」較冷僻（藍道申為其重定向）。**本集 terminology.yaml 已回改**（5 處「倫德沙姆」→「藍道申」）。沿用 UFO-05 裁決。

**人名網路流通查證（2026-08-10）**：
- 吉姆·潘尼斯頓（Jim Penniston）、約翰·巴勒斯（John Burroughs）、查爾斯·哈爾特（Charles Halt）：星洲日報繁中報導流通譯名與 UFO-05 裁決一致，確認沿用
- 愛德華·泰勒（Edward Teller）：維基百科 zh-tw「愛德華·泰勒」流通，與本集詞彙表一致
- **費伏·森明頓（Fife Symington）**：維基百科 zh-tw「鳳凰城光點」條目與維基新聞流通譯名「費伏·森明頓」，且 UFO-08 譯文已用此形式。**2026-08-10 人工裁決採用**；本集 terminology.yaml 已回改（賽明頓州長→費伏·森明頓州長）。草稿 topic_06 殘留「賽明頓州長」3 處（seg 690/691 text+notes），審 topic_06 時改正
- 派翠克·弗雷斯科納（Pat Frascogna，**2026-08-10 人工裁決統一**：跟隨 UFO-05 定稿「派翠克·弗雷斯科納」；本集詞彙表已回改。草稿殘留「弗拉斯科納」審稿時全數改正，簡稱形式用「弗雷斯科納先生」）
- 查克·狄卡羅（Chuck DeCaro）：網路無中譯流通，從本集詞彙表

### 背景

本集為 **UFO-06：Rendlesham Forest Encounter Part 2**（藍道申森林事件 Part 2），seg 1–928，7 個 topic。證人：Jim Penniston、John Burroughs、律師 Pat Frascogna、前英國國防部官員 Nick Pope。內容為事件細節、OSI 掩蓋、硫噴妥鈉訊問、核武疑雲、醫療紀錄、Halt 備忘錄。

### 繼承 UFO-05 人工裁決（2026-08-09，直接沿用，不再重查）

- **Jim/James Penniston → 吉姆·潘尼斯頓／詹姆斯·潘尼斯頓**（非「佩尼斯頓」；主表已修正）
- **Charles Halt → 哈爾特上校**（全名：查爾斯·哈爾特；非「霍爾特」）
- **Bentwaters → 本特沃特斯**（RAF Bentwaters → 皇家空軍本特沃特斯基地；非「班特沃特斯」）
- **Rendlesham Forest incident → 藍道申森林事件**（廢棄譯名「倫德爾沙姆／倫德沙姆森林事件」；本集 terminology.yaml 已於 2026-08-10 回改完畢，見上方裁決紀錄）
- 其他定譯：尼克·波普（Nick Pope）、約翰·巴勒斯（John Burroughs）、蓋博上將（General Gabriel）、格拉維爾參議員（Senator Gravel）、希爾-諾頓勳爵（Lord Hill Norton，用連字號）、資訊自由法（FOIA）、最高機密、真相掩蓋／真相揭露、退伍軍人事務部（VA）、羅斯威爾
- 小組成員（UFO-05 已定譯）：胡利眾議員、基爾派翠克眾議員、羅斯科·巴特利特（Bartlett）、梅里爾·庫克（Cook）、琳恩·伍爾西（Woolsey；topics.json 誤轉為 Walsley）
- **括註風格**：保留全形括註「中譯（English）」，勿刪除

### 本集主表／詞彙表定譯（查主表確認者）

- 派翠克·弗雷斯科納（Pat Frascogna，2026-08-10 裁決統一，見上方裁決紀錄；簡稱「弗雷斯科納先生」）
- **OSI → 空軍特別調查辦公室**（2026-08-10 裁決：與 UFO-05 定稿一致；本集詞彙表 notes 矛盾已修。草稿 topic_05/06 殘留「特別調查處」至少 6 處，審稿時全數改正）
- 費伏·森明頓州長（Fife Symington，2026-08-10 裁決，見上）、柯林頓總統、愛德華·泰勒（Edward Teller）、查克·狄卡羅（Chuck DeCaro）、阿爾弗雷德·金賽（Alfred Kinsey）
- 康拉德上校（Colonel Conrad）、威廉斯上校／少將（Colonel/Major General Williams）
- 皇家空軍伍德布里奇基地（RAF Woodbridge）、馬勒沙姆希斯（Marlesham Heath）、拉姆施泰因空軍基地（Ramstein）、蘭利空軍基地（Langley AFB）
- 眼鏡蛇迷霧計畫（Cobra Mist）、啄木鳥計畫（Woodpecker/Duga）、C3 設施、軍情六處（MI6）、國家安全局（NSA）、國務院、空軍特別調查辦公室（OSI）、美國駐歐空軍（USAFE）
- 硫噴妥鈉（sodium pentothal）、二進位代碼（binary code）、視網膜掃描器、心律調節器除顫器、洲際彈道飛彈（ICBM）、反彈道飛彈系統（ABM）、C-5 運輸機、A-10 反戰車攻擊機
- 真相封鎖（Truth Embargo）、小道消息（Scuttlebutt）、《世界新聞報》（News of the World）、《世界大戰》（War of the Worlds）、鳳凰城光點事件（Phoenix Light）
- ⚠️ 注意：本集詞彙表「Ministry of Defence → 國防部」與美國 DOD「國防部」同譯，語境上需能區分（英國國防部／美國國防部），必要時補「英國」限定

### 已知 Whisper 轉錄錯誤（topics.json potential_errors，校稿時留意全數出現處）

- topic_01：General Gabrielle→General Gabriel（seg 4）；Mr. Pendleton→Mr. Penniston（seg 13）
- topic_03：Sergeant Pennison→Sergeant Penniston（seg 177）；sodium penethol→sodium pentothal（seg 235）
- topic_04：Marvisham Heath→Marlesham Heath（seg 237）；it marrows from Heath→at Marlesham Heath（seg 249）；Bantwaters→Bentwaters（seg 289）；James book of known aircraft→Jane's book of known aircraft（seg 326）
- topic_05：Congresswoman Walsley→Congresswoman Woolsey（seg 367）；Chick-Sans→Chicksands（seg 413）；rocket sanctuary→rocket science（seg 489）；Mr. Frasconga→Mr. Frascogna（seg 535）
- topic_06：Governor Simonton→Governor Symington（seg 690）；Sergeant Paniston→Sergeant Penniston（seg 718）；Rheinstein, Germany→Ramstein, Germany（seg 732）；U-Safie area→USAFE area（seg 865）；General Basely→General Bazley（seg 868）
- （審稿中新發現的錯誤依三.1 流程補錄，並於此區追加紀錄）

### 本集核心事實備忘（供語意審查）

- 事件：1980 年 12 月 26 日起連續三夜，RAF Bentwaters／RAF Woodbridge 雙基地旁的藍道申森林，涉及 150+ 人員
- Penniston 近距離觸摸飛行器、筆記本記錄符號與二進位代碼；遭 OSI 脅迫以半頁刪減版聲明取代四頁詳細報告並背誦
- Burroughs 事後健康惡化，需植入心律調節器除顫器；兩人醫療紀錄遭拒
- 1994 年催眠中 Penniston 發現曾被二次訊問並施用硫噴妥鈉
- Halt 備忘錄：記錄現場壓痕與異常高輻射讀數，上報英國國防部；1983 年《世界新聞報》首次公開
- 核武疑雲：希爾-諾頓勳爵公開稱該基地為核武基地；掩蓋動機疑與駐英美軍核武政治敏感性有關
- 指揮鏈：蓋博上將（USAFE 總司令，駐 Ramstein）→威廉斯（聯隊指揮官）→康拉德（基地指揮官）→哈爾特（副基地指揮官）
- 結論假說：各國競相逆向工程與武器化先進技術，超越單純國安考量的權力動機

### 進度與交接筆記

- 2026-08-10：建立本檔；裁決紀錄完成（藍道申、費伏·森明頓、弗雷斯科納統一、OSI 統一）。
- topic_01（seg 1–48）：審畢，**8 行修訂**：人名英文形式全面中譯（波普先生、蓋博將軍、約翰和吉姆、潘尼斯頓先生，seg 3/4/11/13/45）；Ministry of Defence/Defense 補「英國」限定（seg 4/6）；seg 5 USAAF 逕採 USAFE 並註記（Ramstein 為駐歐空軍總部，USAAF 1947 年已不存在）；seg 30 prosperity→posterity 註記。
- topics.json 補錄 3 筆 potential_errors（topic_01）：seg 5 USAAF→USAFE、seg 11 Jim Peniston→Jim Penniston、seg 30 prosperity→posterity（main.yaml 皆有原文可匹配）；原紀錄 seg 4 Gabrielle、seg 13 Pendleton 經查 main.yaml 已預先修正，收尾時自動跳過。
- 定譯補充：人名一律中譯（跟隨 UFO-05 慣例），原文拼寫僅見於 notes。
- topic_02（seg 49–155）：審畢，**16 行修訂**：OSI 統一「空軍特別調查辦公室」×12 處（含 seg 80 notes）；人名中譯（約翰／吉姆 seg 57/73/117、潘尼斯頓先生 seg 63、威廉斯 seg 112–114、哈爾特／康拉德 seg 116）；seg 57 亂碼字「確鿿」改「確鑿」；seg 110「將軍的命令」改「一體適用的命令」（general orders 非指將軍）降 medium；seg 134「不是數學人」潤飾；seg 152 口誤 23→33 年註記降 medium。
- topics.json 補錄 1 筆（topic_02 範圍）：seg 63 Mr. Pendleton→Mr. Penniston（main.yaml 確認殘留於 seg 63；原紀錄 seg 13 已於翻譯前預先修正，已加註說明）。
- topic_03（seg 156–235）：審畢，**9 行修訂**：人名中譯（巴勒斯先生 seg 156、潘尼斯頓中士 seg 177、巴特利特眾議員 seg 197、蓋博將軍 seg 200〈原誤譯「加百列將軍」〉、查爾斯·哈爾特 seg 204）；OSI 統一 seg 233/235；seg 159 flights 改「分隊」並註解編制；seg 166 force→forest 註記。
- topics.json 補錄 3 筆（topic_03 範圍 seg 166 force→forest、seg 204 Charles Holt→Halt；topic_05 範圍 seg 368 Sergeant Pennison→Penniston）；原紀錄 seg 177/235 經查 main.yaml 已預先修正，已加註。
- topic_04（seg 236–366）：審畢，**4 行修訂**：約翰 seg 237/239；蓋博將軍 seg 289（原誤譯「加百列將軍」，notes 同修）；OSI 統一 seg 343。
- topic_04 四筆 potential_errors（Marvisham/marrows from Heath/Bantwaters/James book）經查 main.yaml source_text 均已預先修正（殘留僅在譯文 notes），收尾自動跳過。
- topic_05（seg 367–541）：審畢，**11 行修訂**：OSI 統一×7 處（seg 372/382/383/384/437/465）；潘尼斯頓中士 seg 368（原「佩尼斯頓」殘留）；弗雷斯科納先生 seg 535；尼克 seg 468/470；奇克桑茲（Chicksands）seg 413；英國國防部 seg 474；seg 409/479 誤轉註記降 medium；seg 412 DIS/DIA 註記。
- topics.json 補錄 4 筆（topic_05）：seg 409 copyright→the public、seg 422 top-seeker→top-secret、seg 466 Mr. Polk→Mr. Pope、seg 479 mono-amano→man to man（main.yaml 皆有殘留可匹配）；原紀錄 seg 367/413/489/535 經查已於翻譯前預先修正。
- topic_06（seg 542–888，76KB 分段審）：審畢，**48 處修訂**：OSI 統一×13；哈爾特上校×10（原文 Colonel Hall 反覆誤轉）；費伏·森明頓州長 seg 690/691（賽明頓改正）；藍道申森林事件 seg 652；蓋博將軍 seg 729/732/839/852/865（原「加百列」）；潘尼斯頓中士／先生 seg 708/718/741/754/820/823/847（佩尼斯頓殘留清除）；尼克·波普／波普先生／尼克 seg 720/731/810/812/831/847；約翰 seg 560/639；庫克眾議員 seg 713；傑瑞·哈里斯 seg 553；巴特利特眾議員 seg 888（原文 Carlson Bartlett 誤轉）；英國國防部限定 seg 729/747/810。
- topics.json 補錄 15 筆（topic_06）：Colonel Hall→Colonel Halt 共 10 段（seg 608/826/834/841/845/854/856/870/873/877）；General Basely→Bazley（seg 873，seg 868 紀錄加註）；seg 708 Pennington、seg 754 Peniston、seg 888 Carlson Bartlett→Congressman Bartlett、seg 652 DLD→DOD；原紀錄 seg 690/718/732/865 經查 main.yaml 已預先修正，已加註。
- topic_07（seg 889–928）：審畢，**2 行修訂**：seg 908 Councilwoman Wolsey 誤轉逕採「伍爾西眾議員」並移除誤拼括註；seg 902 句尾破碎降 medium。另 seg 344（topic_04）補戈登·威廉斯中譯並保留英文括註；seg 690 Larry King 改「賴瑞金（Larry King）」。
- topics.json 補錄 2 筆（topic_07）：seg 897 medical activity→sexual activity、seg 908 Councilwoman Wolsey→Congresswoman Woolsey（main.yaml 皆有殘留可匹配）。

### 全集聚合（校稿完畢，2026-08-10）

- 7 個 topic 全數審畢：topic_01（8）／topic_02（16）／topic_03（9）／topic_04（6）／topic_05（11）／topic_06（49）／topic_07（2），合計約 **101 處修訂**。
- topics.json 累計新補錄 **27 筆** potential_errors（topic_01×3、topic_02×1、topic_03×2、topic_05×5 含 seg 368、topic_06×14、topic_07×2），全部已確認 main.yaml 有原文可匹配；另有多筆原紀錄經查已於翻譯階段前預先修正（seg 4/13/177/235/237/249/289/326/367/413/489/535/690/718/732/865），收尾時 fix_transcription_errors.py 會自動跳過。
- 全檔機械驗證通過：7 檔 `→` 行 JSON 全合法、topics.json 合法、無千分位污染、無禁用詞殘留（網絡／絕密／核子物理）、無舊譯名殘留（特別調查處／賽明頓／倫德沙姆／加百列／佩尼斯頓／弗拉斯科納／班特沃特斯／霍爾特）。
- 跨集一致性：OSI／弗雷斯科納／蓋博／哈爾特／本特沃特斯／藍道申／潘尼斯頓／費伏·森明頓 均與 UFO-05/08 定稿一致。

### 待人工裁決／收尾事項

1. 本日裁決均已執行完畢（藍道申、費伏·森明頓、弗雷斯科納統一、OSI 統一），本集 terminology.yaml 已同步回改。
2. **收尾流程尚未執行**（依人工確認門檻，AI 校稿者不執行）：fix_transcription_errors → backfill → export/split；執行前請先 dry-run 驗證。
3. 提醒：fix_transcription_errors 依 segment_id 匹配，本次補錄之 27 筆皆已逐一確認段落編號；執行 dry-run 時如出現「Error text not found」警告，多屬已預先修正之歷史紀錄，可跳過。
