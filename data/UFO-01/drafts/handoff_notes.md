# UFO-01 審稿交接備忘錄

> 日期：2026-08-07（更新）
> 狀態：topic_01 ~ topic_06 全部完成，待收尾流程（第五節）
> 回填：**全部審完後統一執行**（使用者明確指示，切勿中途回填）
> 注意：目前 main.yaml 的 translation 欄位是**校稿前的舊輸出**，最後由 drafts 回填覆寫取代，無需理會其內容

---

## 一、工作進度

| 檔案 | 段落範圍 | 狀態 | 修訂數 |
|------|---------|------|--------|
| topic_01.md | 1–66（開場、Mitchell、Hellyer） | ✅ 完成 | 12 處 |
| topic_02.md | 67–149（Dolan 證詞） | ✅ 完成 | 8 處＋terminology.yaml 1 條＋topics.json 1 條 |
| topic_03.md | 150–205（Cameron 證詞） | ✅ 完成 | 11 處＋topics.json 2 條 |
| topic_04.md | 206–334（Friedman 證詞） | ✅ 完成 | 19 處＋topics.json 1 條 |
| topic_05.md | 335–383（Howe 證詞） | ✅ 完成 | 8 處＋topics.json 4 條（見第六節） |
| topic_06.md | 384–746（Q&A，91KB 最大檔） | ✅ 完成 | 24 處＋topics.json 4 條（見第七節） |

完成的檔案均已用 Grep 驗證無殘留問題（僅餘刻意保留的原文註釋與 notes）。

---

## 二、已確立的翻譯原則（使用者逐項拍板，全 20 集適用）

### 1. 人名：全部統一中譯
- 依據 `data/UFO-01/terminology.yaml`（本集）與 `configs/terminology_master.yaml`（跨集主表，審稿最終基準）
- 主表未收錄的人名用台灣標準音譯（例：史蒂夫·巴塞特、霍華德·坎農、威爾·史密斯、傑登、泰德·菲利普斯、J·艾倫·海尼克、賽斯·蕭斯塔克、尼爾·德格拉斯·泰森）
- 同句重複出現時，第二次可簡稱姓（例：霍華德·坎農參議員…坎農）
- ✅ 原 `translation_guidelines.md` 的「專有名詞保留原文」條款已於 2026-08-07 修正為與此原則一致（template 與全 20 集副本同步更新）

### 2. 公司／機構名：知名縮寫保留原文、其餘中譯
- GE、GM、TRW、CIA、NSA、FBI、HBO 等知名縮寫 → 保留原文
- 其餘中譯：Westinghouse→西屋、McDonnell Douglas→麥克唐納-道格拉斯（依主表，注意有連字號）、Aerojet-General Nucleonics→航空噴射通用核子
- 軍事基地全中譯（專案慣例）：萊特-帕特森、柯特蘭、霍洛曼、愛德華茲空軍基地
- 媒體/節目名保留原文：Coast to Coast (AM)、earthfiles.com、《Astronomy Magazine》、《Bad Astronomy》、Diane Rehm Show

### 3. 原文事實疑義：保留數字＋notes 標記＋降 medium
不擅自修改原文資訊。已標記案例：
- topic_01 段 31：「47 年前登月」（應約 42 年）
- topic_01 段 62：「66 年前取得博士」（應約 61 年，講者應為 Bartlett，1952 年博士）
- topic_03 段 173：「1981 年」（應為 1982，E.T. 白宮放映會 1982/6/27，月日相符僅年份差）
- topic_04 段 294：「1523 年」（麥哲倫船隊 1522 年 9 月返抵西班牙）

### 4. 高信心 Whisper 轉錄錯誤：譯文以正確拼寫為準＋notes＋補 topics.json
- 譯文直接採用正確形式，notes 說明「原文 X 應為 Y」
- 同時在 `topics.json` 該 topic 的 `potential_errors` 補一筆（segment_id / error_text / suggested_correction / reasoning），供最後 `fix_transcription_errors.py` 修正 main.yaml 原文
- 已補：topic_02 段 116（Hillencutter→Hillenkoetter，並同步修正 terminology.yaml 條目：羅斯科·希倫科特）、topic_03 段 190（Jayden→Jaden）、段 193（conform→confirm）、topic_04 段 298（McDonald Douglas→McDonnell Douglas）
- ⚠️ 此機制僅用於高信心拼寫/同音錯誤；不確定是否為講者口誤者（如年份）只用原則 3 處理

---

## 三、術語與格式慣例（從已審檔案歸納，接手時請沿用）

- **數字千分位用半形逗號**：`4,000`、`10,000`、`12,000`、`3,200`、`5,000`、`15,000`、`1,000 萬`
  - ✅ 已查明：全形千分位污染（「4，000」）源自 `fix_chinese_punctuation.py` 的無條件逗號替換，非 LLM 翻譯錯誤。該工具已於 2026-08-07 修正（保留 `\d,\d` 千分位），全 20 集 drafts 的 99 處污染也已程式化清理。現在可安全執行此工具
- **台灣用語**：網路（非網絡）、透過（非通過，但「通過電話」是正確用法勿誤改）、品質（非質量）、太空（非航天，例：美國航空太空學會）、卡崔娜颶風
- **機密等級**：Top Secret → 最高機密（非絕密；guidelines 原寫「絕密」，已於 2026-08-07 全面修正為「最高機密」）
- **Cover-up**：真相掩蓋；避免「政府掩蓋」對立用詞，動詞用法「政府掩蓋真相」可接受
- **核物理學家**（非核子物理學家）、**藍皮書系統**（非 Blue Book 系統）
- **書名/報告名**：《詭異收穫》、《UFO Evidence》、《科學錯了》；引號用「」『』
- **UFO 前後空格**（檔案既有慣例）；「藍皮書計畫特別報告 14 號」數字前後空格
- **Being/Beings → 存有**（「非人類存有」）；**Roswell**：地名譯「羅斯威爾」、事件譯「羅斯威爾事件」，不保留原文
- 括號原文註釋用半形括號（既有格式，例：藍皮書計畫 (Project Blue Book)），保留不動

---

## 四、編輯操作注意事項

- 草稿格式：`N. 原文` 下一行 `→ {"text": "...", "confidence": "high/medium/low", "notes": "..."}`
- **只改 `→` 行**；JSON 必須保持**單行且合法**（斷行或語法錯誤會被 backfill 標為 needs_review 而不寫入）；notes 內不可出現未跳脫的雙引號
- 段落編號行、`## Speaker Group N` 標題不要動（parser 靠行首格式辨認）
- 每改完一份用 Grep 掃殘留，常用模式：`^→.*(，0|，000|原文人名|網絡|絕密)` 等
- 參考文件：`data/UFO-01/terminology.yaml`、`data/UFO-01/topics.json`（含各 topic 摘要與 potential_errors）、`data/UFO-01/translation_guidelines.md`、`configs/terminology_master.yaml`（跨集主表，人名譯名先查這裡）、`configs/proofread_guidelines_template.md`（校稿準則模板）
- 有疑慮可上網查證（本次已查證：Bartlett 博士年份、E.T. 放映日期、Hillenkoetter 拼寫與譯名）
- ⚠️ 本機 `python3` 是 Windows Store 的假 stub（執行會以 exit code 49 失敗），跑驗證腳本請用 `python`

---

## 五、全部審完後的收尾流程（依序）

⚠️ **執行 backfill 前，請先將本檔案（handoff_notes.md）移出 drafts/ 目錄**（backfill 會掃描目錄內所有 .md；本檔案雖不含可解析的翻譯行、理論上無害，但應避免任何誤判風險）

1. `PYTHONPATH=. python3 tools/fix_transcription_errors.py --config configs/UFO-01.yaml --verbose`（依 topics.json potential_errors 修 main.yaml 原文；累計已補齊 12 筆新記錄，執行前先 --dry-run 檢查）
2. `PYTHONPATH=. python3 tools/backfill_translations.py --config configs/UFO-01.yaml --dry-run`（驗證全部 JSON 可解析）
3. 正式回填：同上去掉 --dry-run（會覆寫 translation 欄位並將通過驗證的段落標為 completed）
4. `PYTHONPATH=. python3 tools/export_srt.py --config configs/UFO-01.yaml --verbose`（需要時）
5. 需要時再 `split_srt.py`

---

## 六、topic_05.md 審稿紀錄（2026-08-07 完成）

1. **段 336**：父親 Chet Moulton → 切特·莫爾頓 ✅
2. **段 344**：改為「分享該台因科學與醫療節目卓越表現而獲得的皮博迪獎」，notes 註明 sharing 為分享電視台共同榮譽 ✅
3. **段 352**：警長 Tex Graves → 泰克斯·格雷夫斯 ✅
4. **段 356**：譯文重組為「…把動物引誘到牧場上，之後發現牠們已經死亡，身上都有同樣的無血切割」；rounder 疑為 round 誤聽 → notes 標記＋已補 topics.json ✅
5. **段 358**：全形千分位改半形（2,000、1,800）；句子重組消除重複累贅 ✅
6. **段 364、369**：譯文已是柯特蘭，已補 topics.json potential_errors 兩筆（Curlin→Kirtland），供 fix_transcription_errors 修原文 ✅
7. **段 378**：「廣播網絡」→「廣播網路」；「所謂國家安全利益為由」→「所謂的國家安全理由」；原文 intelligent 疑為 intelligence 誤聽 → notes 標記＋已補 topics.json ✅
8. 段 360 Home Box Office / HBO 保留原文（符合公司原則，不動）；段 375 herpetologist 譯「爬蟲學家」描述 OK（爬行動物含蛇類，不動）

**清單外新發現（同次修訂）**：
- **段 374**：「小型類人屍體，既有死亡的也有活著的」自相矛盾（原文 bodies 含存活者）→ 改「類人身軀」
- **段 382**：non-humans 依段 376 與術語表 Being→存有慣例，統一為「非人類存有」

**驗證**：49 條 JSON 全部合法；無 `\d，\d` 千分位污染；殘留拉丁字僅為刻意保留的縮寫/媒體名（UFO、HBO、CIA、NSA、DIA、NRO、KNBC、WCVB、KMGH-TV、UAC、UAV、EBE、earthfiles.com、Coast to Coast AM）。

## 七、topic_06.md 審稿紀錄（2026-08-07 完成）

**人名統一中譯**（24 處修訂的主要類別）：
- George Knapp → 喬治·奈普（段 417、421、426、430、432、433、435、667；段 435 使用者拍板用「喬治」而非姓氏「奈普」）
- Kilpatrick → 基爾派翠克女士（441）、Cook → 庫克議員（578、710）、Woolsey → 伍爾西議員（443）、Friedman → 弗里德曼先生（443、611）、Howe → 豪女士（611）、Pat Robertson → 派特·羅伯森（447）
- Nellis 空軍基地 → 內利斯空軍基地（422，維基百科標準譯名）
- Martin Marietta → 馬丁·瑪麗埃塔（481，維基百科標準譯名）

**其他修訂**：
- 段 443：「核子物理學家」→「核物理學家」（術語表）；notes 補記原文 Congressman Woolsey 應為 Congresswoman（琳恩·伍爾西為女性）
- 段 476：原文 urgent Congress 疑為 US Congress，notes 標記
- 段 500/501：Gravel 發音討論段，保留原文並括註（格拉維爾）
- 段 518：Terrans → 地球人（Terrans）
- 段 521：don't want any part of 直譯誤譯 → 「不想…有任何瓜葛」
- 段 523：補足語意（公元前 4004 年創世說 vs 40 億年）
- 段 528：韓戰語境 Korea → 北韓
- 段 540：radical technology → 顛覆性技術；段 555：primordial → 最初的
- 段 566：OSI 辦公室 → 空軍特別調查辦公室（與 topic_05 段 363/369 統一）
- 段 622：通過 → 透過；段 634：notes 改為「Dark bombs 疑為 atom bombs 之轉錄錯誤」
- 段 646：使用者建議改「把兩個角對接在一起」
- 段 656：Prairie State 括註（伊利諾州）
- 段 663：UFO 互動網絡 → 互動網路（術語表）；段 670：分發網絡 → 網路
- 段 672：全形千分位「10，000」×2 → 半形
- 段 711：lighter than aircraft 疑為 lighter-than-air aircraft，譯文修正＋notes
- 段 489 書名（Alien Harvest 等）保留原文，比照《UFO Evidence》先例

**topics.json 補錄 4 筆**：443（Freeman→Friedman）、476（urgent→US Congress）、634（Dark→atom bombs）、711（lighter-than-air）

**驗證**：363 條 JSON 全部合法；無 `\d，\d`；無「網絡/絕密/核子物理/通過」殘留；保留拉丁字僅為刻意項目（earthfiles.com、書名、Gravel 發音段、Terrans 括註、Google、YouTube、Coast to Coast AM 等）。
