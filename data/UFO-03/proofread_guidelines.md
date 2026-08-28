# 校稿準則（Proofread Guidelines）— UFO-03

> 本檔案複製自 `configs/proofread_guidelines_template.md`，並在「八、本集專屬事項」補充 UFO-03 特有的術語、已知問題與交接筆記。
> 翻譯階段的風格規範請見 `data/UFO-03/translation_guidelines.md`（兩者職責分立；衝突時以本檔與術語表為準）。

---

## 一、參考資料與優先序

校稿時可參考的文件，衝突時依下列優先序裁決：

1. `configs/terminology_master.yaml` — 跨集術語主表（**最終基準**，人名譯名先查這裡）
2. `configs/terminology_master_rules.yaml` — 主表編輯規則（ deprecated 形式、情境例外）
3. `data/UFO-03/terminology.yaml` — 本集術語表
4. `data/UFO-03/topics.json` — 各 topic 摘要與 `potential_errors`（轉錄錯誤紀錄）
5. 本檔

## 二、術語與專有名詞原則

### 1. 人名：全部統一中譯
- 主表已收錄者從主表；未收錄者用台灣標準音譯
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
- 括號原文註釋用半形括號（既有格式，例：藍皮書計畫 (Project Blue Book)），保留不動
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

---

## 八、本集專屬事項

### 主表對齊決議（主表優先，覆蓋本集 terminology.yaml）
- GAO / Government Accountability Office：本集術語表作「美國政府問責署」→ 主表定譯 **美國審計總署（GAO）**（1995 年事件當時全名為 General Accounting Office；UFO-02 已拍板「美國審計總署」）
- Congresswoman Kilpatrick：→ **基爾派翠克眾議員**（主表；deprecated：基爾帕特里克議員）
- Senator Gravel：→ **格拉維爾參議員**（主表；deprecated：格拉韋爾參議員）
- Congressman Steven/Stephen Schiff：→ **史蒂芬·希夫眾議員**（主表；deprecated：史蒂文·希夫眾議員）
- National Reconnaissance Office：→ **國家偵察局（NRO）**（主表；deprecated：美國國家偵察局／國家偵察辦公室類舊寫法）
- need to know：→ **需知原則／需知權限**（主表 preferred：需知原則；deprecated：知密權）
- MUFON：→ **MUFON（UFO 互動網路）**（deprecated：互動網絡類寫法）
- Roscoe Bartlett：→ **巴特利特眾議員**（主表人名：羅斯科·巴特利特；UFO-02 沿用「巴特利特」）
- T. Townsend Brown → 湯森·布朗（deprecated：托馬斯·湯森·布朗）；Theodore Shackley → 西奧多·沙克利（deprecated：西奧多·謝克利）

### ⚠️ 跨集譯名差異（待人工裁決，本集一律從主表）
- Lawrence/Laurance Rockefeller：主表與本集術語表作 **勞倫斯·洛克菲勒**；UFO-02 校稿筆記作「勞倫斯·洛克斐勒」。本集從主表「洛克菲勒」。
- Steven Schiff：主表作 **史蒂芬·希夫**；UFO-02 校稿筆記作「史蒂文·席夫」。本集從主表。

### 新增人名／地名定譯（主表未收錄，供後續集數沿用）
- Dr. Steven Greer → **史蒂芬·葛瑞爾博士**（簡稱葛瑞爾博士）；本集主要證人
- Edgar Mitchell → **艾德加·米切爾**（沿用他集既有「米切爾」）；第六位登月太空人
- Asilomar → **阿西洛馬（Asilomar）**；加州蒙特雷會議中心
- Rumsfeld → **倫斯斐**（台灣慣用，沿用原譯）；Donald Rumsfeld → 唐納德·倫斯斐
- Dan Burton → **丹·伯頓眾議員**；眾議院政府監督委員會主席
- James Woolsey → **伍爾西**（本集術語表：CIA局長伍爾西）
- topic_01 新增：Richard D'Amato → **理查·達馬托**（原文 DeMato 為誤聽，已補錄 potential_errors）；John Peterson → 約翰·彼得森；Arlington Institute → 阿靈頓研究所；Brad Sorensen → 布萊德·索倫森；Admiral Harry Train → 哈利·特雷恩（沿用原譯）；Grumman → 格魯曼、Northrop → 諾斯羅普、Lockheed → 洛克希德（公司名中譯）
- topic_02 新增：Jim Goodale → **吉姆·古德爾**（原文 Goodell 為誤聽，NYT 五角大樓文件案法律顧問，已補錄 potential_errors）；Peter Stockton → 彼得·史塔克頓；John Dingell → 約翰·丁格爾；David Burnham → 大衛·伯納姆；Tip O'Neill → 提普·歐尼爾；Dr. John Mack → 約翰·麥克博士；F. Lee Bailey → F·李·貝利；McCord → 麥科德（沿用 UFO-02）；Judge Sirica → 西里卡法官；Holiday Inn → 假日飯店

### 待釐清／遺留
- 段落 64「Admiral Moran」：法國海軍上將兼醫學、物理雙博士、安培獎得主、薩科齊顧問——查證未果，音譯「莫蘭上將」保留，confidence 已降 medium
- 段落 115「platinum grade plutonium」：疑為 bomb-grade 口誤或誤聽，依規則保留原文「鉑級」、降 medium 並標註（不入 potential_errors）

### 進度（2026-08-08 盤點：以 git diff 核實，非前任自述）
- [x] topic_01（段落 1–84）已審完，19 處修訂；JSON 驗證通過；topics.json 補錄 1 筆 potential_errors（seg 46 DeMato→D'Amato）— **已核實**：diff 修訂數與記載一致
- [x] topic_02（段落 85–144）已審完，16 處修訂；JSON 驗證通過；topics.json 補錄 2 筆（seg 87、89 Jim Goodell→Jim Goodale）— **已核實**
- [x] topic_03（段落 145–198）已審完，8 處修訂；JSON 驗證通過；無新增 potential_errors（FOIAA 等 4 處原譯已標註）；GAO 統一為美國審計總署、Schiff 從主表史蒂芬·希夫、alien bodies 統一「外星存有遺體」（避開屍體/存活矛盾）— **已核實**
- [x] topic_04（段落 199–272）已審完，11 處修訂；JSON 驗證通過；topics.json 補錄 4 筆（seg 221 STP→OSTP、seg 258 close→closed、seg 261 Hess-Dowling→Hessdalen、seg 266 forward→foreword）；MUFON 互動網絡→互動網路；Trans-en-Provence 音譯改特朗斯昂普羅旺斯 — **已核實**
- [x] **topic_05（段落 273–544）已全部審完（2026-08-08 續審）**：前任完成 seg 273–353（18 處修訂）並複查無誤；續審 seg 354–544 共 **64 處修訂**（354–400：14；401–450：14；451–500：16；501–544：20）；全部 `→` 行 JSON 驗證通過（0 錯誤）
  - 續審定譯/決策：the bomb→核彈（seg 341 伊朗核武語境）、cleared→已獲安全許可（391，舊譯「被清除」為誤譯）、actionable intelligence→可據以行動的情報（428/523/541 統一）、need to know→需知權限（520 主表）、denied access→被拒絕訪問（429/510/515 維持既有）、compartmented operations→機密分隔行動（420）、disruptive→顛覆性（484）、dog-and-pony show→表面秀（541）、cosmonauts→宇宙飛行員（533，與太空人區分）、terminated→被除掉（535 指人）、B-2 隱形轟炸機（連字號，510）、參謀長聯席會議情報主管（510）、阿西洛馬（Asilomar）（528）、SEC 主席（522）、Asilomar 檔案 deprecated 寫法「不明飛行物（UFO）」改「不明飛行物」（449）、Sheehan 統一「希恩」（387）、Dr. Greer 統一「葛瑞爾博士」（448、486）
  - seg 508/509 依原文斷句重劃（as well as C.I. / Director Woolsey → 以及 CIA／局長伍爾西），兩段譯文互相承接
  - 降 medium：seg 398（原文 exercise 語境不明，暫譯「演習」，無法確定原詞，不入 potential_errors）

### ⚠️ 交接待辦（2026-08-08 續審後更新）
1. ~~topics.json 漏補 2 筆 potential_errors~~ **已處理**：seg 297（Koloski-Frost→Kowsky-Frost）、seg 303（a special skiff→a special SCIF）已補登入 topics.json；本次續審另新增 2 筆（seg 463 USABs→USAPs、seg 508 C.I.→CIA）
2. **所有校稿異動尚未 commit**：topic_01–05 草稿與 topics.json 皆為工作區未提交修改；本檔為 untracked。建議人工確認後再 commit
3. **收尾流程一律未執行**（且依第七節須人工確認門檻）：`fix_transcription_errors.py`（topics.json 累計 **13 筆**校稿新增 potential_errors 待套用）、`backfill_translations.py`、`export_srt.py` 皆未跑；`output/UFO-03/UFO-03.zh-TW.srt` 仍為**校稿前**舊版，勿直接使用
4. 全部 5 個草稿 `→` 行 JSON 已驗證合法（84/60/54/74/272 段，0 錯誤）
5. **待人工裁決**：seg 398 原文「exercise」（threatened, near-death, exercise, eliminated 列舉）語境不明，暫譯「演習」並降 medium，無法確定原詞；seg 377「an active longitude」疑為轉錄錯誤（對照 seg 386 active suppression），依語境意譯但未入 potential_errors（原詞不明）

### 已知轉錄錯誤（topics.json potential_errors，校稿時留意全數出現處）
- topic_01：CI Director→CIA Director（seg 10）；Admiral Kramer 或為 Wilson 誤聽（seg 18→保留克拉默並註記）；Isilomar→Asilomar（seg 22）；North of Grumman→Northrop Grumman（seg 75）；DeMato→D'Amato（seg 46，校稿新增）
- topic_02：Nugent Hand→Nugan Hand（95）；Kermage→Kerr-McGee（106）；Judge Tice→Frank G. Theis（113）；Stan Turner→Stansfield Turner（117）；Ron Contra→Iran-Contra（132）
- topic_03：FOIAA→FOIA（149，另見 152、155、178）；Bruce McAbee→Bruce Maccabee（167）；G.O.A.→GAO（178）
- topic_04：forays in topology→ufology（227）；Marie Goldbreath→Marie Galbraith（242 等多處）；CNS→CNES（250）；J-PAN→GEIPAN（250）；Transant Provence→Trans-en-Provence（251）；Denis Letti→Denis Letty（253）；Taritone→Tarrytown（258）
- topic_05：pointy vector→Poynting vector（294）；Wolsey→Woolsey（315）；Danny Sheen→Daniel Sheehan（327）；Dr. Crere→Dr. Greer（486）；Sylmar→Asilomar（528）；USABs→USAPs（463，續審新增）；C.I./Director→CIA Director（508/509，續審新增）；另 seg 297 Koloski-Frost→Kowsky-Frost、seg 303 a special skiff→a special SCIF 為前任補登
