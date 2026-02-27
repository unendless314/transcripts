# UFO-17 翻譯過程發現問題紀錄

**日期**: 2026-02-28
**翻譯範圍**: topic_01 至 topic_09（共 930 個段落）

---

## 一、轉錄錯誤（Potential Errors）

根據 topics.json 中標記的 `potential_errors` 及翻譯過程中發現的問題：

| Segment | 原文錯誤 | 正確內容 | 說明 |
|---------|----------|----------|------|
| 95 | Admiral Ingen | Admiral Engen | FAA 局長 Donald D. Engen 的轉錄錯誤 |
| 96 | Admiral Ingen | Admiral Engen | 同上，重複出現 |
| 129 | South Bomber | Stealth Bomber | 隱形轟炸機，語境為軍事機密飛機 |
| 143 | RAF Scalthorpe | RAF Sculthorpe | 英國空軍基地名稱拼寫錯誤 |
| 172 | the Earl Monboton | the Earl Mountbatten | 蒙巴頓伯爵，菲利普親王的叔叔 |
| 180 | call them curses | call them cursus | 考古學術語 cursus（巨石陣平行溝渠） |
| 181 | Stonehenge curses | Stonehenge cursus | 同上 |
| 195 | Ernie aircraft | Aurigny aircraft | 英國海峽群島航空公司名稱 |
| 195 | Blue Island pilot | Blue Islands pilot | 航空公司名稱應為複數 |
| 205 | Mr. Jim Grant | Mr. Jim Courant | 證人 Jim Courant 的姓名錯誤 |
| 289 | Kiliwale | Kīlauea | 夏威夷基拉韋厄火山 |
| 415 | up at Lang City | up at Atlantic City | FAA 技術中心位於大西洋城 |
| 485 | Mr. Kallen | Mr. Callahan | 約翰·卡拉漢的姓名錯誤 |
| 516 | 07-47 | 747 | 波音 747 客機 |
| 545 | Dr. Schreifer | Major Filer | 說話者應為費勒少校 |
| 598 | Representative Pooley | Representative Kilpatrick | 國會議員 Carolyn Cheeks Kilpatrick |
| 636 | Michi Kuka | Michio Kaku | 物理學家加來道雄 |
| 719 | Representative Patrick | Representative Kilpatrick | 同上 |
| 827 | Mr. Fryler | Major Filer | 費勒少校的另一個轉錄錯誤 |

---

## 二、術語表調整

翻譯過程中對 `terminology.yaml` 進行的微調：

| 術語 | 原翻譯 | 調整後 | 理由 |
|------|--------|--------|------|
| Sighting | 目擊 | 目擊事件 | 更完整表達，與 "sighting report" 對應 |
| transponder | 應答機 | 航空應答機 | 更精確的航空術語 |
| Mount Blanc | 白朗峰 | 法國白朗峰 | 增加地區標示，避免混淆 |
| Kīlauea | 基拉韋厄火山 | 夏威夷基拉韋厄火山 | 增加地區標示 |
| Major Carl Lewis | 卡爾·劉易斯 | 卡爾·路易斯 | 統一譯名（Lewis 譯為路易斯） |
| TR-3B | TR-3B | TR-3B 三角飛行器 | 補充說明，讓讀者了解其形狀 |

---

## 三、翻譯注意事項

### 1. 特殊術語處理
- **cursus**: 考古學專有名詞，指巨石陣附近的平行溝渠遺跡，保留原文並加註解
- **cargo cult**: 貨物崇拜，指南太平洋島民模仿外來科技的文化現象
- **mothership / mother ship**: 統一譯為「母艦」

### 2. 口語化表達
- "scared the pants off him" → 「把他嚇壞了」（俚語，非字面意思）
- "They're drooling" → 「他們都流口水了」（形容極度渴望）
- "you can see it the next Tuesday" → 「你下個星期二都還能看見它」（誇張說法，形容視野極佳）

### 3. 信心度標記為 medium 的段落

主要為以下幾類：
1. **轉錄錯誤處**：原文可能有誤，需根據語境判斷
2. **口語化長句**：需要較多語序調整以符合中文習慣
3. **複雜科學概念**：涉及物理學或工程學術語
4. **說話者身份不明確**：如 segment 545 "Dr. Schreifer" 應為 Major Filer

---

## 四、後續建議

1. **執行標點符號修正**（建議在回填前執行）：
   ```bash
   PYTHONPATH=. python3 tools/fix_chinese_punctuation.py --config configs/UFO-17.yaml --verbose
   ```

2. **回填翻譯到 main.yaml**：
   ```bash
   PYTHONPATH=. python3 tools/backfill_translations.py --config configs/UFO-17.yaml --verbose
   ```

3. **匯出 SRT 字幕**：
   ```bash
   PYTHONPATH=. python3 tools/export_srt.py --config configs/UFO-17.yaml --verbose
   ```

4. **審校建議**：
   - topic_08 中涉及較多科學理論（相對論、蟲洞、自由能源等），建議由具物理背景的審校者檢查
   - topic_09 中 John Callahan 的雷達技術說明較專業，建議由航空背景人員確認

---

## 五、Git 提交紀錄

**Commit**: 7d3598e
**訊息**: UFO-17: 完成全部 9 個 topics 翻譯 (topic_01-09)
**推送狀態**: 已推送至 origin/master
