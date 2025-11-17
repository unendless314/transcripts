#!/usr/bin/env python3
"""
合併 terminology.yaml 和 terminology_candidates.yaml
保留定義和譯法，使用 candidates 中的實際 segments
"""

import yaml
from pathlib import Path
from collections import defaultdict

def load_yaml(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def save_yaml(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, allow_unicode=True, sort_keys=False, width=1000)

def merge_terminology(terminology_path, candidates_path, output_path):
    """合併 terminology.yaml 和 candidates，使用實際的 segments"""

    terminology = load_yaml(terminology_path)
    candidates = load_yaml(candidates_path)

    # 建立 candidates 的 term -> segments 映射
    candidates_segments = {}
    for term_entry in candidates.get('terms', []):
        term = term_entry['term']
        segments = []
        for occurrence in term_entry.get('occurrences', []):
            segments.append(occurrence['segment_id'])
        candidates_segments[term] = sorted(set(segments))

    # 更新 terminology 中的 segments
    for term_entry in terminology.get('terms', []):
        term = term_entry['term']

        # 為每個 sense 更新 segments
        for sense in term_entry.get('senses', []):
            if term in candidates_segments:
                # 使用 candidates 中的實際 segments
                sense['segments'] = candidates_segments[term]
            else:
                # 如果 candidates 中沒有，清空 segments（可能是手動添加的術語）
                sense['segments'] = []

    # 儲存更新後的 terminology
    save_yaml(terminology, output_path)

    print(f"✅ 合併完成！")
    print(f"   輸入: {terminology_path}")
    print(f"   候選: {candidates_path}")
    print(f"   輸出: {output_path}")

    # 檢查是否有 candidates 中的術語在 terminology 中缺失
    terminology_terms = {entry['term'] for entry in terminology.get('terms', [])}
    missing_terms = set(candidates_segments.keys()) - terminology_terms

    if missing_terms:
        print(f"\n⚠️  在 candidates 中有但 terminology 中缺失的術語 ({len(missing_terms)} 個):")
        for term in sorted(missing_terms):
            print(f"  - {term}")

if __name__ == '__main__':
    episode_id = 'UFO-07'
    terminology_path = Path(f'data/{episode_id}/terminology.yaml')
    candidates_path = Path(f'data/{episode_id}/terminology_candidates.yaml')
    output_path = Path(f'data/{episode_id}/terminology_updated.yaml')

    merge_terminology(terminology_path, candidates_path, output_path)
