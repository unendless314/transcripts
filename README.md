# UFO Citizen Hearing 字幕翻譯專案

這是一個基於 Whisper 轉錄字幕的模組化翻譯管道，用於處理 UFO Citizen Hearing 系列影片的字幕翻譯。

## 專案結構

```
.
├── whisper-medium/         # Whisper 轉錄的原始 SRT 檔案（來源）
├── src/                    # 共用模組
│   ├── clients/           # LLM API 客戶端
│   ├── models.py          # 資料模型
│   └── exceptions.py      # 自訂例外
├── tools/                 # CLI 工具腳本
├── prompts/               # LLM prompt 模板
├── configs/               # 配置檔案
│   ├── default.yaml       # 預設配置
│   └── UFO-XX.yaml        # Episode 配置
├── input/                 # 輸入 SRT 檔案
│   └── UFO-XX/
├── data/                  # 工作檔案
│   └── UFO-XX/
│       ├── main.yaml      # 主資料檔案
│       ├── topics.json    # 主題分析結果
│       ├── terminology.yaml
│       ├── guidelines.md  # 翻譯風格指南
│       └── drafts/        # 翻譯草稿檔案
├── output/                # 輸出結果
│   └── UFO-XX/
└── logs/                  # 日誌檔案
```

## Episode 列表

共 20 集，按照 YouTube 官方順序：

| Episode ID | 標題 |
|------------|------|
| UFO-01 | UFOs - History & Background Part 1 |
| UFO-02 | UFOs - History & Background Part 2 |
| UFO-03 | UFOs - Truth, Lies & The Coverup Part 1 |
| UFO-04 | UFOs - Truth, Lies & The Coverup / Part 2 |
| UFO-05 | UFOs - Rendlesham Forest Encounter Part 1 |
| UFO-06 | UFOs - Rendlesham Forest Encounter Part 2 |
| UFO-07 | UFOs - Nuclear Tampering Part 1 |
| UFO-08 | UFOs - Nuclear Tampering Part 2 |
| UFO-09 | UFOs - Associated Phenomena |
| UFO-10 | UFOs - Documents & Proof |
| UFO-11 | UFOs - Roswell Part 1 |
| UFO-12 | UFOs - Roswell Part 2 |
| UFO-13 | UFOs - South American Encounters Part 1 |
| UFO-14 | UFOs - South American Encounters Part 2 |
| UFO-15 | UFOs - A Global Phenomenon Part 1 |
| UFO-16 | UFOs - A Global Phenomenon Part 2 |
| UFO-17 | UFOs - Pilots & Aviation Experts |
| UFO-18 | UFOs - The Truth Embargo |
| UFO-19 | UFOS - Science & Technology |
| UFO-20 | UFOs - Citizen Hearing Closing Remarks |

## 翻譯工作流程

### 步驟 1：設置 Episode

為每個 episode 建立目錄結構和配置檔案：

```bash
# 建立目錄
mkdir -p input/UFO-01 data/UFO-01 output/UFO-01 logs/UFO-01

# 複製 SRT 檔案到 input 目錄（保留原始檔名）
cp "whisper-medium/UFOs - History & Background Part 1.wav.srt" input/UFO-01/

# 建立配置檔案
cat > configs/UFO-01.yaml << EOF
episode_id: UFO-01
EOF
```

### 步驟 2：SRT → main.yaml

解析 SRT 並生成主資料檔案：

```bash
PYTHONPATH=. python3 tools/srt_to_main_yaml.py --config configs/UFO-01.yaml --verbose
```

### 步驟 3：匯出 JSON 供 LLM 分析

```bash
PYTHONPATH=. python3 tools/main_yaml_to_json.py --config configs/UFO-01.yaml --verbose
```

### 步驟 4：主題分析

使用 LLM 分析字幕並生成主題結構（需要 API key）：

```bash
PYTHONPATH=. python3 tools/topics_analysis_driver.py --config configs/UFO-01.yaml --verbose
```

### 步驟 5：準備翻譯草稿

生成按主題分組的翻譯工作檔案：

```bash
PYTHONPATH=. python3 tools/prepare_topic_drafts.py --config configs/UFO-01.yaml --verbose
```

### 步驟 6：翻譯

編輯 `data/UFO-01/drafts/topic_XX.md` 檔案，填入翻譯內容。

參考資料：
- `data/UFO-01/guidelines.md` - 翻譯風格指南
- `data/UFO-01/terminology.yaml` - 術語對照表
- `data/UFO-01/topics.json` - 主題摘要

### 步驟 7：QA - 修正中文標點

```bash
PYTHONPATH=. python3 tools/fix_chinese_punctuation.py --config configs/UFO-01.yaml --verbose
```

### 步驟 8：回填翻譯到 main.yaml

```bash
PYTHONPATH=. python3 tools/backfill_translations.py --config configs/UFO-01.yaml --verbose
```

### 步驟 9：匯出翻譯後的 SRT

```bash
PYTHONPATH=. python3 tools/export_srt.py --config configs/UFO-01.yaml --verbose
```

### 步驟 10：分割長字幕（可選）

```bash
PYTHONPATH=. python3 tools/split_srt.py \
  -i output/UFO-01/UFO-01.zh-TW.srt \
  -o output/UFO-01/UFO-01.zh-TW.split.srt \
  --max-chars 35 \
  --verbose
```

## 環境設置

### 安裝依賴

```bash
pip install -r requirements.txt
```

### 配置 API Keys

```bash
cp .env.example .env
# 編輯 .env 並加入你的 API keys
```

## Whisper SRT 特性

這個專案使用 Whisper 生成的 SRT 檔案，與一般 SRT 有些差異：

1. **說話者標記較少**：Whisper 轉錄的 SRT 只有部分說話者標記（`>>` 前綴），覆蓋率約 1.2%
2. **自動斷句**：Whisper 會自動在適當位置斷句，但可能不完全符合語義完整性
3. **長度適中**：平均每個 episode 約 1,000+ 個段落

現有的工具已經可以處理這些特性，無需額外調整。

## 注意事項

- LLM 翻譯常見問題：中文翻譯中混用英文標點符號（例如 `,` 而非 `，`）
- 建議在翻譯後執行 `fix_chinese_punctuation.py` 進行修正
- 長字幕建議執行 `split_srt.py` 2-3 次以達到理想長度

---

© 2025 UFO Citizen Hearing 字幕翻譯專案
