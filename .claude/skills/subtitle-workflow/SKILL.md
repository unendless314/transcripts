---
name: subtitle-workflow
description: Manage SRT subtitle translation pipeline for UFO Citizen Hearing episodes. Automatically detect workflow stage (SRT parsing, topic analysis, translation, QA) and suggest next steps. Use when user asks about translation progress, next steps, or workflow status.
allowed-tools: Read, Glob, Bash, Grep, Edit, Write
---

# UFO Citizen Hearing 字幕翻譯工作流管理 Skill

這個 Skill 專門用於管理 UFO Citizen Hearing 系列 SRT 字幕翻譯的完整工作流程。

## 主要功能

### 1. 自動檢測當前工作流階段
根據專案檔案狀態，判斷當前處於哪個階段：
- ✅ **階段 1**：SRT 已轉換為 main.yaml
- ✅ **階段 2**：已產生 segments JSON
- ✅ **階段 3**：已完成 topic analysis（含錯誤檢測）
- ✅ **階段 3.5**：修正轉錄錯誤（Whisper 專用，建議執行）
- ✅ **階段 4**：術語候選生成
- ✅ **階段 5**：術語分類
- ✅ **階段 6**：準備翻譯草稿
- ✅ **階段 7**：翻譯進行中
- ✅ **階段 8**：回填翻譯結果
- ✅ **階段 9**：QA 檢查與匯出

### 2. 智慧建議下一步
基於當前狀態，提供具體的操作建議和命令。

### 3. 檢查檔案完整性
驗證必要檔案是否存在：
- `input/<episode>/*.srt` - Whisper 轉錄字幕檔
- `data/<episode>/main.yaml` - 主要資料檔
- `data/<episode>/main_segments.json` - 精簡段落 JSON
- `data/<episode>/topics.json` - 主題分析結果
- `data/<episode>/terminology_candidates.yaml` - 術語候選清單（可選）
- `data/<episode>/terminology.yaml` - 術語分類結果（可選）
- `data/<episode>/drafts/*.md` - 翻譯工作檔

## 工作流階段詳解

### 階段 1：SRT 轉 YAML
**檢查條件**：`input/<episode>/*.srt` 存在，但 `data/<episode>/main.yaml` 不存在

**建議操作**：
```bash
PYTHONPATH=. python3 tools/srt_to_main_yaml.py --config configs/<episode>.yaml --verbose
```

**說明**：將 Whisper SRT 字幕檔解析為 YAML 格式，進行智慧句子合併。

**注意事項**：Whisper SRT 的 speaker marker (`>>`) 覆蓋率較低（0-5%），這是正常現象，不影響工作流程。

---

### 階段 2：匯出 JSON 供 LLM 分析
**檢查條件**：`main.yaml` 存在，但 `data/<episode>/main_segments.json` 不存在

**建議操作**：
```bash
PYTHONPATH=. python3 tools/main_yaml_to_json.py --config configs/<episode>.yaml --pretty --verbose
```

**說明**：匯出精簡的 JSON 檔案（僅含 segment_id, speaker_group, source_text），供 LLM 進行主題分析。

---

### 階段 3：主題分析
**檢查條件**：`main_segments.json` 存在，但 `topics.json` 不存在

**建議操作**：
```bash
PYTHONPATH=. python3 tools/topics_analysis_driver.py --config configs/<episode>.yaml --verbose
```

**說明**：使用 LLM 進行主題劃分與摘要生成，產出 topics.json（含 global_summary、topic 範圍、摘要與關鍵詞）。

**提示**：需要配置 API key（GEMINI_API_KEY 或 OPENAI_API_KEY），見 `.env` 檔案。

---

### 階段 3.5：修正轉錄錯誤（Whisper 專用，強烈建議）
**檢查條件**：`topics.json` 存在且包含 `potential_errors` 欄位

**重要性**：⭐⭐⭐⭐⭐（5 星）
Whisper 轉錄稿有 5-10% 詞錯率（WER），在翻譯前修正錯誤可避免錯誤傳播。

**建議操作**：
```bash
# 1. 先檢查 topics.json 中檢測到的錯誤（手動或用腳本）
python3 -c "
import json
with open('data/UFO-01/topics.json') as f:
    data = json.load(f)
for topic in data['topics']:
    errors = topic.get('potential_errors', [])
    if errors:
        print(f\"{topic['topic_id']}: {len(errors)} errors\")
"

# 2. 自動修正 main.yaml 中的轉錄錯誤
PYTHONPATH=. python3 tools/fix_transcription_errors.py --config configs/UFO-01.yaml --verbose

# 3. 重新生成 main_segments.json（反映修正後的原文）
PYTHONPATH=. python3 tools/main_yaml_to_json.py --config configs/UFO-01.yaml --verbose
```

**說明**：
- `topics_analysis_driver.py` 在階段 3 會自動檢測轉錄錯誤，存入 `topics.json` 的 `potential_errors` 欄位
- 每個錯誤包含：`segment_id`、`error_text`、`suggested_correction`、`reasoning`
- `fix_transcription_errors.py` 會自動將錯誤修正應用到 `main.yaml`
- 修正後需重新生成 `main_segments.json`，翻譯草稿（階段 6）會使用修正後的文本

**常見錯誤類型**：
- 專有名詞拼寫錯誤（人名、地名、組織名）
- 技術術語誤聽（scientific terms、military jargon）
- 上下文語意錯誤（"proof of the moon" → "flew to the moon"）
- 同音異義詞錯誤（their/there, to/too）

**範例輸出**：
```
✓ Segment 3: Fixed
  Error: "Darlene Houley"
  Fixed: "Darlene Hooley"

✓ Segment 16: Fixed
  Error: "proof of the moon on Apollo 14"
  Fixed: "flew to the moon on Apollo 14"

Correction summary:
  Total errors detected: 15
  Successfully fixed: 15
```

---

### 階段 4：術語候選生成
**檢查條件**：`topics.json` 存在，但 `data/<episode>/terminology_candidates.yaml` 不存在

**建議操作**：
```bash
PYTHONPATH=. python3 tools/terminology_mapper.py --config configs/<episode>.yaml --verbose
```

**說明**：掃描 `main.yaml` 找出所有術語（來自 `configs/terminology_template.yaml` 與 `topics.json` 關鍵詞）的出現位置，為每個術語記錄所有匹配的段落（segment_id、sources、source_text），產出 `terminology_candidates.yaml`。

**輸出檔案結構**：
- 每個術語有 `occurrences` 陣列（尚未分類到不同語意）
- 包含 `segment_id`、`sources`（template/topic）、`source_text`

**注意**：這是術語分類的**輸入檔案**，下一階段會根據上下文將出現位置分類到不同語意（senses）。

---

### 階段 5：術語分類
**檢查條件**：`terminology_candidates.yaml` 存在，但 `data/<episode>/terminology.yaml` 不存在或不完整

**建議操作**（手動或使用 Claude Code 協助）：

**方法一：手動分類**
1. 開啟 `data/<episode>/terminology_candidates.yaml`
2. 檢視 `configs/terminology_template.yaml` 中定義的多語意術語
3. 對照每個 occurrence 的 `source_text` 上下文
4. 將 `segment_id` 分配到對應的 sense（語意）中
5. 產出 `terminology.yaml`，結構為每個 sense 有 `segments` 陣列

**方法二：使用 Claude Code 協助**
- 載入 `terminology_candidates.yaml` 與 `terminology_template.yaml`
- 請 Claude 根據上下文進行語意消歧（multi-sense disambiguation）
- 審核並修正 Claude 的分類結果
- 產出最終的 `terminology.yaml`

**術語分類範例**：
```yaml
terms:
  - term: UFO
    senses:
      - sense_id: 1
        translation: 不明飛行物
        definition: "泛指無法辨識的空中現象"
        segments: [1, 5, 12, 23]  # 從 candidates 的 occurrences 分類而來
      - sense_id: 2
        translation: 飛碟
        definition: "明確指稱具有碟形外觀的飛行器"
        segments: [45, 67, 89]
```

**說明**：根據上下文將術語出現位置分類到不同語意，確保翻譯時使用正確的術語對應。這是翻譯品質控制的關鍵步驟。

---

### 階段 6：準備翻譯草稿
**檢查條件**：`topics.json` 存在（`terminology.yaml` 為可選），但 `data/<episode>/drafts/` 目錄不存在或為空

**建議操作**：
```bash
PYTHONPATH=. python3 tools/prepare_topic_drafts.py --config configs/<episode>.yaml --verbose
```

**說明**：根據 topics.json 與 main_segments.json，為每個 topic 生成 Markdown 工作檔（`drafts/topic_01.md` 等），包含原文與空白翻譯框架。自動插入 Speaker Group 標題標記話輪切換。

**常用參數**：
- `--force` - 覆寫已存在檔案
- `--topic topic_01` - 只生成特定 topic

**注意**：若已完成階段 5（terminology.yaml 存在），翻譯時可參考該檔案確保術語一致性。

---

### 階段 7：執行翻譯
**檢查條件**：drafts 目錄存在且有檔案

#### 🎯 建議工作流程（最佳實踐）

**第一步：AI 翻譯前 2-3 個 topics（建立基準）**

- ✅ **掌握語調脈絡** - 理解證詞的語氣風格與情緒表達
- ✅ **發現細節問題** - 實際翻譯會暴露 guidelines 需要補充的地方
- ✅ **測試術語表** - 確認 terminology.yaml 是否涵蓋所有需要的術語
- ✅ **建立翻譯範例** - 完成的 topics 可作為後續 agent 的參考樣本
- ✅ **優化指令品質** - 有了實際經驗後，給 agent 的指令會更精準

**推薦範圍**：
- **最少**：topic_01 ~ topic_02（掌握基本語調）
- **建議**：topic_01 ~ topic_03（涵蓋更多語境變化）

**操作方式**：
1. 載入 Context：
   - `topics.json` - 全域摘要與當前 topic 的 summary、keywords
   - `data/<episode>/terminology.yaml` - 術語翻譯標準（若已完成階段 5）
   - `configs/guidelines_template.md` - 翻譯風格指引
2. 直接在 `drafts/topic_0X.md` 中填寫翻譯（修改箭頭右側的 JSON 欄位）
3. 填寫欄位：
   - `text` - 翻譯內容（必填，非空）
   - `confidence` - high/medium/low（必填）
   - `notes` - 備註（可選）

**完成後檢視**：
- 檢查翻譯品質是否符合 guidelines
- 記錄翻譯過程中發現的注意事項
- 如有需要，調整 guidelines 或 terminology

---

**第二步：使用 Task Tool 委派剩餘 topics（提升效率）**

**何時開始委派**：
- 已完成前 2-3 個 topics 的翻譯
- 確認翻譯品質符合預期
- guidelines 與 terminology 已調整完善

**委派策略**：

⚠️ **不建議**：同時並行處理多個 topics
✅ **建議**：一次委派一個 topic，確認品質後再繼續

**原因**：
- 避免批次出錯導致大量重翻
- 可在過程中調整指令
- 保持對翻譯品質的掌控
- 降低風險，提升整體效率

**委派方式**：
1. 使用 Task Tool 啟動 general-purpose agent
2. 提供詳細的翻譯指令，建議結構：
   ```
   請翻譯 data/<episode>/drafts/topic_0X.md

   **必讀參考文檔**（請先閱讀以下檔案）：
   1. configs/guidelines_template.md - 翻譯風格與規範
   2. data/<episode>/terminology.yaml - 術語翻譯標準（若已完成階段 5）
   3. data/<episode>/topics.json - 全集摘要與當前 topic 的語境

   **額外注意事項**（文檔未涵蓋但重要的補充）：
   - 本 topic 的特殊語境或主題特色（例如：軍事證詞 vs. 科學分析）
   - 特定表達方式的處理建議
   - 其他在翻譯過程中發現的注意事項

   **成功標準**：
   - 所有 JSON 欄位填寫完整（text, confidence, notes）
   - 術語嚴格依照 terminology.yaml（如適用）
   - 語氣與風格符合 guidelines 要求（正式、客觀、嚴謹）
   - 格式正確無誤
   - 中文標點符號使用正確（，。？！）
   ```

3. Agent 完成後檢查品質
4. 確認無誤後再委派下一個 topic

**逐一委派範例流程**：
```
✅ 自行翻譯：topic_01, topic_02, topic_03（建立基準）
→ 委派 topic_04 → 檢查品質 ✓
→ 委派 topic_05 → 檢查品質 ✓
→ 委派 topic_06 → 檢查品質 ✓
→ 委派 topic_07 → 檢查品質 ✓
```

---

### 階段 8：回填翻譯到 main.yaml
**檢查條件**：drafts 中的檔案已完成翻譯

**建議操作**：
```bash
PYTHONPATH=. python3 tools/backfill_translations.py --config configs/<episode>.yaml --verbose
```

**說明**：解析填妥的 Markdown 檔案，驗證翻譯欄位，並寫回 `main.yaml` 的 `translation.*` 與 `metadata.topic_id` 欄位。驗證通過設為 `completed`，失敗設為 `needs_review`。

**可選參數**：
- `--dry-run` - 驗證但不寫入
- `--topic topic_01` - 只處理特定 topic

**QA 檢查**：
在回填之前，建議先執行標點符號修正：
```bash
PYTHONPATH=. python3 tools/fix_chinese_punctuation.py --config configs/<episode>.yaml --verbose
```

---

### 階段 9：QA 檢查與匯出
**檢查條件**：`main.yaml` 中的 `translation.status` 大部分為 `completed`

**建議操作**：

1. **匯出 SRT 字幕**：
   ```bash
   PYTHONPATH=. python3 tools/export_srt.py --config configs/<episode>.yaml --verbose
   ```

   **說明**：將 `main.yaml` 中的翻譯結果轉換回 SRT 格式，輸出到 `output/<episode>/<episode>.zh-TW.srt`

   **參數說明**：
   - `--no-speaker-hints` - 不加入說話者提示標記（預設會在話輪切換時加入 `>>` 標記）
   - `--fail-on-missing` - 遇到未完成翻譯時報錯並中止（預設會使用原文繼續）
   - `--verbose` - 顯示詳細的處理進度與統計資訊

2. **分割過長字幕（可選後處理）**：
   ```bash
   PYTHONPATH=. python3 tools/split_srt.py \
     -i output/<episode>/<episode>.zh-TW.srt \
     -o output/<episode>/<episode>.zh-TW.split.srt \
     --max-chars 35 --verbose
   ```

   **說明**：智慧分割過長字幕段落，基於標點符號優先級重新分配時間碼

   **注意**：工具每次只分割一次，超長段落可能需要執行 2-3 次

---

## 檢測邏輯

當用戶詢問「接下來要做什麼」或「目前進度如何」時，自動執行：

1. 檢查 `configs/` 目錄，找出當前工作的 episode
2. 掃描對應的 `input/<episode>/` 和 `data/<episode>/` 目錄
3. 根據檔案存在狀態判斷階段
4. 提供具體的下一步指令

## 使用範例

**用戶問**：「UFO-01 目前進度如何？」

**Skill 自動執行**：
1. 檢查 `configs/UFO-01.yaml` 是否存在
2. 掃描 `data/UFO-01/` 檔案
3. 判斷：`main.yaml` ✅, `topics.json` ✅, `terminology.yaml` ✅, `drafts/` ✅（但內容未完成）
4. 回應：「目前在階段 7（翻譯進行中），建議繼續編輯 drafts 中的 Markdown 檔案，或使用 Claude Code 協助翻譯。」

---

## UFO 專案特殊注意事項

1. **Whisper SRT 特性**：
   - Speaker marker (`>>`) 覆蓋率低（0-5%）是正常現象
   - 不影響翻譯工作流程
   - speaker_group 欄位仍會被正確填充

2. **翻譯風格**：
   - 正式且嚴謹（國會聽證會記錄）
   - 客觀中立（不添加評論或情緒）
   - 專業術語保持一致性

3. **術語處理**：
   - 專有名詞保留原文（人名、地名、軍事單位、專案代號）
   - 技術術語參考 `configs/terminology_template.yaml`
   - 軍銜與職稱翻譯為中文，必要時附註原文

---

**建立時間**：2025-11-16
**適用專案**：UFO Citizen Hearing 字幕翻譯管線
**來源專案**：基於 translations 專案改編
