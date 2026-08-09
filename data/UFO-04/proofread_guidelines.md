# 校稿準則（Proofread Guidelines）— UFO-04

> 本檔案複製自 `configs/proofread_guidelines_template.md`，並在「八、本集專屬事項」補充 UFO-04 特有的術語、已知問題與交接筆記。
> 翻譯階段的風格規範請見 `data/UFO-04/translation_guidelines.md`（兩者職責分立；衝突時以本檔與術語表為準）。

---

## 一、參考資料與優先序

校稿時可參考的文件，衝突時依下列優先序裁決：

1. `configs/terminology_master.yaml` — 跨集術語主表（**最終基準**，人名譯名先查這裡）
2. `configs/terminology_master_rules.yaml` — 主表編輯規則（ deprecated 形式、情境例外）
3. `data/UFO-04/terminology.yaml` — 本集術語表
4. `data/UFO-04/topics.json` — 各 topic 摘要與 `potential_errors`（轉錄錯誤紀錄）
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
  - 歷史背景：`fix_chinese_punctuation.py` 舊版會把數字內半形逗號轉成全形（「4，000」），已於 2026-08-07 修正工具並清理全專案既有污染；校稿時仍可用 `\d，\d` 模式抽查確認
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

## 八、本集專屬事項

### 跨集譯名拍板（2026-08-08，人工裁決）
- **Dr. Steven Greer → 史蒂芬·格里爾博士**（簡稱格里爾博士）：主表已收錄（term key 統一為 "Dr. Steven Greer"），deprecated「史蒂芬·葛瑞爾博士／葛瑞爾博士／葛瑞爾」已列入 `terminology_master_rules.yaml`
  - 背景：UFO-03 校稿曾拍板「葛瑞爾」，經人工查證網路通用譯名為「格里爾」，改以格里爾為準；UFO-03 草稿 11 處「葛瑞爾」已同步改正，UFO-03 詞彙表已補收詞條
  - ⚠️ UFO-03 交接筆記（該集 proofread_guidelines.md 第八節）內的「葛瑞爾」定譯紀錄未回改，以本條與主表為準
- 主表 deprecated 提醒：凱倫·絲克伍案（非西爾克伍德）、五角大廈文件案（非五角大樓文件案）——本集 Daniel Sheehan 相關段落留意

### 本集草稿既有 Greer 譯名不一致（校稿時統一為格里爾博士）
- topic_01/02 有保留原文「Stephen Greer」；topic_04 有「Greer 博士」；topic_03/05 已用「格里爾博士」

### 已知轉錄錯誤（topics.json potential_errors，校稿時留意全數出現處）
- topic_01：Dick DiMatto→Dick D'Amato（seg 24）；Fence in High Places→Friends in High Places（seg 52，Hubbell 回憶錄《高層友人》）；afford to the book→a foreword to the book（seg 68，Richardson 寫序）
- topic_02：Ms. Howell→Ms. Howe（seg 81）；Project Pounds→Project Pounce（seg 91）
- topic_03：Dr. John at Princeton→Dr. Jahn at Princeton（seg 121，PEAR 實驗室 Robert Jahn）；Boutrous Golly→Boutros Boutros-Ghali（seg 131）；hornwim grasses→horn-rim glasses（seg 141）
- topic_04：Comita Report→COMETA Report（seg 206）；Jesse Helms→Richard Helms（seg 248，或為講者口誤）
- topic_05：Daniel Sheen→Daniel Sheehan（seg 361）；Congresswoman Houli→Hooley（seg 379）；~~palette（seg 389）~~ 人工覆聽確認原音確為 palette，乃證人姓名而非轉錄錯誤，已改音譯「帕萊特」，topics.json 佔位條目已移除

### 進度
- [x] topic_01（段落 1–80）已審完，26 處修訂；JSON 驗證通過（80/80，0 錯誤）
  - 主要修訂：人名統一中譯 24 處（卡麥隆先生、喬治·奈普、迪克·達馬托、阿爾弗雷德·歐唐納、史蒂芬·格里爾/格里爾、班·里奇、瑪格麗特·柴契爾、比爾·柯林頓/柯林頓、約翰·波德斯達/波德斯達、保羅·大衛斯、韋伯斯特·哈貝爾/哈貝爾、比爾·理查森/理查森）；seg 31 act of God 直譯「上帝的行為」改譯「奇蹟」並補 deep black 說明；seg 49 半形冒號改全形
  - 查證：seg 47 柯林頓 2005 年香港公開談 UFO 屬實（中國財經論壇，Open Minds 報導）
  - seg 52：main.yaml 原文已是 Friends in High Places，topics.json 該筆 potential_errors 為無害殘留（fix_transcription_errors 套用時會找不到文字而跳過）
- [x] topic_02（段落 81–116）已審完，14 處修訂；JSON 驗證通過（36/36，0 錯誤）
  - 主要修訂：豪女士（seg 81）、史蒂芬·格里爾（82）、約翰·麥克博士統一（83/85/87/89/104/111，主表「博士」優先於本集術語表「醫師」）、琳達（108/111/113）、seg 87「電視製作」潤飾、seg 91 補 Project Pounce 註記、seg 94 bodies 改遺體避屍體/存活矛盾、seg 106/107 呎吋統一英尺英寸、seg 111 破碎收尾句重組
- [x] topic_03（段落 117–151）已審完，8 處修訂；JSON 驗證通過（35/35，0 錯誤）；topics.json 補錄 5 筆 potential_errors（seg 123/124 Wolsey→Woolsey、seg 131/138/141 Dr. Grier→Dr. Greer）
  - 主要修訂：湯瑪斯·傑佛遜/麻薩諸塞州（119）、千分位 1,000 億（120）、琳達/雅恩博士（121，Dr. John→Dr. Jahn 查證為 Robert G. Jahn，中文通行譯名雅恩）、麥克唐納-道格拉斯（125）、裴爾助學金句誤譯修正（136）、法國國防部備忘錄句重組（145）、【掌聲】格式（151）、seg 123/125 補註記
  - ⚠️ 工具 bug 已修：`fix_transcription_errors.py` 原以 segment_id 做 dict key，同段多筆 potential_errors 會互相覆蓋（seg 141 即有 2 筆）；已改為 segment_id → 錯誤列表逐筆套用，並修正 summary 計數
  - seg 141 main.yaml 原文已是 horn-rim glasses，該筆 potential_errors 為無害殘留
- [x] topic_04（段落 152–252）已審完，18 處修訂；JSON 驗證通過（101/101，0 錯誤）
  - 主要修訂：巴特利特先生（152/225，主表 Roscoe Bartlett）、老布希總統（172）、鮑伯·史瓦茲（176）、《60 分鐘》數字空格（178/185）、湯瑪斯·傑佛遜（180）、格里爾博士（191/193）、艾拉（192）、COMETA 報告/普羅旺斯/本特沃特斯/英國國防部（206，情境規則英國語境）、喬治·法勒（219，查證未果音譯保留）、Steve→格里爾（222，truth embargo 創用語）、【掌聲】（224）、比爾·柯林頓（235）、蔡斯·布蘭登（244/247）、格拉維爾參議員（252）
  - seg 245/246/248 main.yaml 原文已是 Richard Helms，topics.json seg 248 Jesse Helms 該筆為無害殘留
- [x] topic_05（段落 253–421）已審完，16 處修訂；JSON 驗證通過（169/169，0 錯誤）
  - 主要修訂：傑佛遜統一（258，原譯傑斐遜）、【掌聲】格式（285/353/378/413/421）、透過（291）、訊息/資訊（298/301/375）、想像（343）、UA→UFO 聽證會暫譯降 medium（362）、可據以行動的情報統一 UFO-03 定譯（370/372）、專案（386）、需知權限（403，主表）

### 本集新增人名定譯（主表未收錄，供後續集數沿用）
- Bob Schwartz → **鮑伯·史瓦茲**（Time Life 董事）
- George Filer → **喬治·法勒**（空軍少校；查證未果，音譯保留）
- Chase Brandon → **蔡斯·布蘭登**（CIA 42 年資歷，著有羅斯威爾虛構小說）
- Dr. Robert G. Jahn → **雅恩博士**（普林斯頓 PEAR 實驗室；查證中文通行譯名「雅恩」）
- Thomas Jefferson → **湯瑪斯·傑佛遜**、Massachusetts → **麻薩諸塞州**
- palette → **帕萊特**（seg 389 證人姓名；人工覆聽確認原音如此，身分待查證）

### ⚠️ 交接待辦（全部 topic 審完後更新，2026-08-08）
1. topics.json 校稿補錄 **5 筆** potential_errors（seg 123/124 Wolsey→Woolsey、seg 131/138/141 Dr. Grier→Dr. Greer）；topics.json 現共 17 筆（seg 389 palette 經人工覆聽確認非轉錄錯誤，佔位條目已移除）
2. 無害殘留（main.yaml 原文已正確，fix_transcription_errors 套用時會找不到文字而跳過）：seg 52 Fence in High Places、seg 141 hornwim grasses、seg 248 Jesse Helms
3. ⚠️ **工具 bug 已修**：`tools/fix_transcription_errors.py` 原以 segment_id 做 dict key，同段多筆 potential_errors 互相覆蓋；已改為一對多逐筆套用（建議 UFO-03 收尾時重跑 dry-run 核對其 13 筆待套用紀錄）
4. **收尾流程一律未執行**（依第七節人工確認門檻）：`fix_transcription_errors.py`、`backfill_translations.py`、`export_srt.py` 皆未跑
5. 全部 5 個草稿 `→` 行 JSON 已驗證合法（80/36/35/101/169 = 421 段，0 錯誤）；禁詞掃描（千分位污染、網絡/絕密/核子物理、通過、半形掌聲、「信息」）全數通過
6. **待人工裁決**：
   - seg 300 原文「who that public private doctor for」語法破碎（疑轉錄錯誤），暫譯「公私合作夥伴關係究竟是什麼」並降 medium；原詞不明，不入 potential_errors
   - seg 362 原文「UA hearings」疑為 UFO 誤聽，暫譯「UFO 聽證會」並降 medium；原詞不明，不入 potential_errors
   - seg 222「as Steve calls it」依語境譯為格里爾（truth embargo 為其創用語），已加註記
   - ~~seg 389「palette」~~ **已決（2026-08-08）**：人工覆聽並比對 YouTube 字幕，確認原音確為 palette，乃證人姓名；譯文改音譯「帕萊特」，confidence 維持 medium（身分待查證），topics.json 佔位條目已移除
7. **本次校稿異動尚未 commit**：5 個草稿、topics.json、本檔、UFO-04 terminology.yaml（Greer 主表對齊）、configs/terminology_master.yaml＋rules（Greer 收錄 167 詞）、tools/fix_transcription_errors.py（bug 修復）、UFO-03/17 詞彙表與 UFO-03 草稿（葛瑞爾→格里爾 11 處）皆為未提交修改
8. **交接待辦：補上原文括註**（2026-08-09 人工登記，由後續校稿者處理）：
   - 背景：2026-08-09 人工裁決**譯文應保留「中譯（English）」全形括註**，`configs/proofread_guidelines_template.md` 已明訂此規則；格式可參考 UFO-05 定稿
   - git 查證結果：經比對校稿前版本（`git show 7ccea6b:data/UFO-04/drafts/`），本集草稿於翻譯階段本無括註（全 5 檔皆 0），故本任務為**新增**而非還原；若對個別段落有疑慮，可用 `git log -p -- data/UFO-04/drafts/<file>` 追查該行歷史
   - 任務：於 `data/UFO-04/drafts/` 各檔的定譯中，為重要人名／地名／專有名詞補上原文括註（例：史蒂芬·格里爾博士（Dr. Steven Greer））。僅補重要專有名詞的**首次出現**，無需重複
   - 格式：全形括號；括註內純英文內容用半形標點；只改 `→` 行，JSON 保持單行且合法；編號行與 Speaker Group 標題不動
   - 驗證與收尾：完成後以 `python` 逐行 `json.loads` 驗證並回報人工；本集收尾尚未執行，括註可隨正常收尾流程生效；若屆時已回填／匯出，是否重跑 backfill/export 由人工決定
