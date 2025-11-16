#!/usr/bin/env python3
"""
Fix Transcription Errors

根據 topics.json 中 LLM 檢測到的 potential_errors，修正 main.yaml 中的轉錄錯誤。

使用場景：
- Whisper 轉錄稿含有 5-10% WER（詞錯率）
- topics_analysis_driver.py 已生成包含 potential_errors 的 topics.json
- 需要在翻譯前修正原文錯誤，避免錯誤傳播

工作流程：
1. 讀取 topics.json 提取所有 potential_errors
2. 在 main.yaml 中找到對應的 segment
3. 將 error_text 替換為 suggested_correction
4. 保存修正後的 main.yaml

使用方法：
    PYTHONPATH=. python3 tools/fix_transcription_errors.py --config configs/UFO-01.yaml [--dry-run] [--verbose]
"""

import argparse
import json
import logging
import sys
from pathlib import Path
import yaml

from src.config_loader import load_config as load_project_config
from src.exceptions import ConfigError


def setup_logging(level: str = "INFO"):
    """設置日誌配置"""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s [%(levelname)s] %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )


def load_config(config_path: Path) -> dict:
    """載入配置檔"""
    config = load_project_config(config_path)
    required = ['episode_id', 'output', 'input']
    for field in required:
        if field not in config:
            raise ConfigError(f"Missing required field: {field}", str(config_path))
    return config


def extract_errors_from_topics(topics_path: Path) -> dict:
    """從 topics.json 提取所有 potential_errors

    Returns:
        dict: {segment_id: error_info, ...}
    """
    if not topics_path.exists():
        raise FileNotFoundError(f"topics.json not found: {topics_path}")

    with open(topics_path, 'r', encoding='utf-8') as f:
        topics = json.load(f)

    # Extract all errors
    all_errors = []
    for topic in topics['topics']:
        for error in topic.get('potential_errors', []):
            all_errors.append(error)

    # Create segment_id -> error mapping
    error_map = {err['segment_id']: err for err in all_errors}

    logging.info(f"Found {len(error_map)} potential errors in topics.json")
    return error_map


def apply_corrections(main_yaml_path: Path, error_map: dict, dry_run: bool = False) -> int:
    """應用修正到 main.yaml

    Args:
        main_yaml_path: main.yaml 路徑
        error_map: segment_id -> error_info 映射
        dry_run: 是否為試運行（不實際寫入）

    Returns:
        int: 修正的段落數量
    """
    if not main_yaml_path.exists():
        raise FileNotFoundError(f"main.yaml not found: {main_yaml_path}")

    # Load main.yaml
    with open(main_yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)

    fixed_count = 0

    # Apply corrections
    for segment in data['segments']:
        seg_id = segment['segment_id']

        if seg_id in error_map:
            error = error_map[seg_id]
            old_text = segment['source_text']

            # Perform replacement
            new_text = old_text.replace(error['error_text'], error['suggested_correction'])

            if new_text != old_text:
                segment['source_text'] = new_text
                fixed_count += 1

                logging.info(f"Segment {seg_id}: Fixed")
                logging.debug(f"  Error: \"{error['error_text']}\"")
                logging.debug(f"  Fixed: \"{error['suggested_correction']}\"")
                logging.debug(f"  Reason: {error['reasoning']}")
            else:
                logging.warning(f"Segment {seg_id}: Error text not found in source_text")
                logging.warning(f"  Looking for: \"{error['error_text']}\"")
                logging.warning(f"  In text: \"{old_text[:100]}...\"")

    # Save corrected main.yaml (unless dry-run)
    if not dry_run:
        with open(main_yaml_path, 'w', encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True, sort_keys=False, width=120)
        logging.info(f"Saved corrected main.yaml to {main_yaml_path}")
    else:
        logging.info("[DRY RUN] Would have saved corrections to main.yaml")

    return fixed_count


def main():
    parser = argparse.ArgumentParser(
        description="Fix transcription errors in main.yaml based on topics.json potential_errors",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Fix errors (normal mode)
  PYTHONPATH=. python3 tools/fix_transcription_errors.py --config configs/UFO-01.yaml --verbose

  # Preview changes without modifying files
  PYTHONPATH=. python3 tools/fix_transcription_errors.py --config configs/UFO-01.yaml --dry-run --verbose
        """
    )

    parser.add_argument(
        '--config',
        type=Path,
        required=True,
        help='Path to episode config file (e.g., configs/UFO-01.yaml)'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without modifying main.yaml'
    )

    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose logging (DEBUG level)'
    )

    args = parser.parse_args()

    # Setup logging
    setup_logging('DEBUG' if args.verbose else 'INFO')

    try:
        # Load config
        config = load_config(args.config)
        episode_id = config['episode_id']

        logging.info(f"Processing episode: {episode_id}")

        # Get file paths
        topics_path = Path(config['output']['topics_json'])
        main_yaml_path = Path(config['output']['main_yaml'])

        logging.info(f"Topics JSON: {topics_path}")
        logging.info(f"Main YAML: {main_yaml_path}")

        # Extract errors
        error_map = extract_errors_from_topics(topics_path)

        if not error_map:
            logging.info("No errors found in topics.json - nothing to fix")
            return 0

        # Apply corrections
        fixed_count = apply_corrections(main_yaml_path, error_map, dry_run=args.dry_run)

        # Summary
        logging.info("=" * 60)
        logging.info(f"Correction summary:")
        logging.info(f"  Total errors detected: {len(error_map)}")
        logging.info(f"  Successfully fixed: {fixed_count}")

        if fixed_count < len(error_map):
            logging.warning(f"  Failed to fix: {len(error_map) - fixed_count}")
            logging.warning("  (Error text not found in source_text)")

        logging.info("=" * 60)

        if not args.dry_run:
            logging.info("✓ Transcription errors fixed successfully!")
            logging.info("")
            logging.info("Next steps:")
            logging.info("  1. Regenerate main_segments.json:")
            logging.info(f"     PYTHONPATH=. python3 tools/main_yaml_to_json.py --config {args.config} --verbose")
            logging.info("  2. Regenerate translation drafts:")
            logging.info(f"     PYTHONPATH=. python3 tools/prepare_topic_drafts.py --config {args.config} --force --verbose")
        else:
            logging.info("[DRY RUN] No files were modified")

        return 0

    except Exception as e:
        logging.error(f"Error: {e}", exc_info=args.verbose)
        return 1


if __name__ == '__main__':
    sys.exit(main())
