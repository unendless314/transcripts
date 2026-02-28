# Gemini CLI Project Context: UFO Citizen Hearing 字幕翻譯專案

This project is a modular, LLM-powered translation pipeline designed to process and translate subtitles for the 20-episode **UFO Citizen Hearing** series. It transforms raw Whisper-generated transcripts into high-quality, context-aware Traditional Chinese (zh-TW) subtitles.

## 🚀 Project Overview

-   **Type:** Python-based Subtitle Processing Pipeline.
-   **Core Tech:** Python 3, LLM APIs (Gemini, OpenAI, Anthropic), `pysrt`, `PyYAML`.
-   **Main Goal:** Translate 20 episodes of UFO testimony with high consistency using thematic analysis, terminology mapping, and transcription error correction.
-   **Source Material:** Whisper-generated SRT files (medium model) with ~5-10% Word Error Rate (WER) and low speaker marker coverage.

## 📁 Directory Structure

-   `src/`: Core logic, including LLM clients (`clients/`) and data models (`models.py`).
-   `tools/`: CLI scripts for each step of the translation workflow.
-   `configs/`: YAML configurations (`default.yaml` and `UFO-XX.yaml` for each episode).
-   `data/UFO-XX/`: Working directory for each episode.
    -   `main.yaml`: The "Source of Truth" containing all segments, metadata, and translation status.
    -   `topics.json`: Thematic structure and segment-level summaries.
    -   `terminology.yaml`: Multi-sense term definitions for consistency.
    -   `drafts/`: Markdown work files (`topic_XX.md`) for manual or AI translation.
-   `input/UFO-XX/`: Input SRT files.
-   `output/UFO-XX/`: Final translated and processed SRT files.
-   `prompts/`: System prompts for LLM-based tasks (e.g., topic analysis).
-   `whisper-medium/`: Original Whisper-generated source SRT files.

## 🛠 Building and Running

### Prerequisites
1.  **Install Dependencies:** `pip install -r requirements.txt`
2.  **Setup Environment:** `cp .env.example .env` and add your API keys (Gemini, OpenAI, etc.).

### Standard Workflow (10 Steps)
Always run tools with `PYTHONPATH=.` and a specific config file.

1.  **Initialize Episode:** `mkdir -p input/UFO-01 data/UFO-01 ...`
2.  **Parse SRT:** `python3 tools/srt_to_main_yaml.py --config configs/UFO-01.yaml`
3.  **Export for Analysis:** `python3 tools/main_yaml_to_json.py --config configs/UFO-01.yaml`
4.  **Thematic Analysis:** `python3 tools/topics_analysis_driver.py --config configs/UFO-01.yaml`
5.  **Fix Transcription Errors:** `python3 tools/fix_transcription_errors.py --config configs/UFO-01.yaml`
6.  **Prepare Drafts:** `python3 tools/prepare_topic_drafts.py --config configs/UFO-01.yaml`
7.  **Translate:** Edit Markdown files in `data/UFO-01/drafts/`.
8.  **QA (Punctuation):** `python3 tools/fix_chinese_punctuation.py --config configs/UFO-01.yaml`
9.  **Backfill:** `python3 tools/backfill_translations.py --config configs/UFO-01.yaml`
10. **Export SRT:** `python3 tools/export_srt.py --config configs/UFO-01.yaml`
    -   *Optional:* Split long lines with `tools/split_srt.py`.

## 📏 Development Conventions

### Data Integrity
-   **`main.yaml` is the Source of Truth:** All tools should eventually sync their results back to this file.
-   **Status Tracking:** Segments use `translation.status` (`pending`, `completed`, `needs_review`, etc.) to support resuming interrupted jobs.
-   **Sentence Merging:** The pipeline prioritizes semantic completeness over raw SRT timing when merging segments.

### Coding Style
-   **CLI Tools:** Use `argparse` for configuration loading. Support `--verbose` and `--dry-run` where applicable.
-   **Error Handling:** Never fail silently. Log unparseable segments and mark them as `needs_review`.
-   **LLM Integration:** Abstract API calls through `src/clients/`. Use the models defined in `src/models.py`.

### Translation Guidelines
-   **Tone:** Formal, objective, and technical (matching the nature of the hearing).
-   **Punctuation:** Use Full-width Chinese punctuation (，、。？！) for the final output.
-   **Consistency:** Always refer to `terminology.yaml` and `topics.json` for context during translation.

## ⚠️ Known Characteristics
-   **Whisper Artifacts:** Transcripts often misspell proper nouns or technical terms. Use Step 5 (`fix_transcription_errors.py`) to correct these before translation.
-   **Low Speaker Markers:** Whisper markers (`>>`) are infrequent (0-5%). The pipeline handles this gracefully via `speaker_group` tracking.
