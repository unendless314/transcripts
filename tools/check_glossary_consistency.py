#!/usr/bin/env python3
"""跨集數術語一致性檢查工具

掃描所有 data/UFO-*/terminology.yaml，建立「術語 → 各集譯名」對照矩陣，
輸出：
  1. 跨集譯名不一致清單（同一術語在不同集有不同 preferred_translation）
  2. 寫法變體（含稱謂前綴的人名等）其譯名不一致
  3. 各集格式風格統計（半形/全形括號、書名號、保留英文、數字間距）
  4. 單集內重複條目（同一 normalized term 出現多筆）
  5. 高頻共用術語（≥5 集）一致性總覽
  6. 與 configs/terminology_master.yaml 的 drift 檢查（sense 感知；
     已記錄於 master variants 的語境差異不算 drift）

用法：
  PYTHONPATH=. python3 tools/check_glossary_consistency.py [--verbose]
"""

import argparse
import glob
import os
import re
import sys
from collections import defaultdict

import yaml

# Windows 終端中文輸出
sys.stdout.reconfigure(encoding="utf-8")

TITLE_PREFIXES = {
    "dr.", "dr", "mr.", "mr", "mrs.", "mrs", "ms.", "ms",
    "general", "gen.", "senator", "sen.", "president", "chairman",
    "colonel", "col.", "lieutenant", "lt.", "major", "maj.",
    "captain", "capt.", "sergeant", "sgt.", "airman", "officer",
    "congressman", "congresswoman", "secretary", "minister", "agent",
    "director", "admiral", "professor", "prof.", "sir", "lady",
    "governor", "gov.", "representative", "rep.", "judge", "former",
    "staff", "tech", "master", "chief", "private", "corporal",
    "commander", "cdr.", "first", "second", "lieutenant colonel",
}

CJK = r"一-鿿"


def norm_key(term: str) -> str:
    """正規化術語：小寫、去首尾空白、壓縮內部空白。"""
    return re.sub(r"\s+", " ", term.strip().lower())


def strip_titles(key: str) -> str:
    """移除人名前的稱謂前綴，用於偵測同一人物的寫法變體。"""
    tokens = key.split()
    while tokens and (tokens[0] in TITLE_PREFIXES or
                      re.fullmatch(r"(dr|mr|mrs|ms|lt|gen|sen|col|maj|capt|sgt|prof|rep|gov)\.", tokens[0])):
        tokens.pop(0)
    return " ".join(tokens)


def load_all():
    """回傳 {episode: [(term, sense_id, translation), ...]}"""
    data = {}
    for path in sorted(glob.glob("data/UFO-*/terminology.yaml")):
        ep = re.search(r"(UFO-\d+)", path).group(1)
        with open(path, encoding="utf-8") as f:
            doc = yaml.safe_load(f)
        rows = []
        for t in (doc or {}).get("terms", []) or []:
            term = str(t.get("term", "")).strip()
            for s in t.get("senses", []) or []:
                tr = s.get("preferred_translation")
                if tr is None:
                    continue
                rows.append((term, str(s.get("id", "")), str(tr).strip()))
        data[ep] = rows
    return data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    data = load_all()

    # ---- 建立矩陣：norm_key -> {ep: set(translations)}，以及 surface forms ----
    matrix = defaultdict(lambda: defaultdict(set))
    surfaces = defaultdict(set)  # norm_key -> 原始寫法集合
    for ep, rows in data.items():
        for term, _sid, tr in rows:
            k = norm_key(term)
            matrix[k][ep].add(tr)
            surfaces[k].add(term)

    # ---- 1. 跨集譯名不一致 ----
    conflicts = []
    for k, eps in matrix.items():
        all_tr = set()
        for trs in eps.values():
            all_tr |= trs
        if len(eps) >= 2 and len(all_tr) >= 2:
            conflicts.append((k, eps, all_tr))
    conflicts.sort(key=lambda x: (-len(x[1]), x[0]))

    print("=" * 70)
    print(f"【1】跨集譯名不一致：{len(conflicts)} 個術語")
    print("=" * 70)
    for k, eps, all_tr in conflicts:
        ep_list = sorted(eps)
        print(f"\n◆ {sorted(surfaces[k])} （出現於 {len(eps)} 集）")
        for ep in ep_list:
            print(f"    {ep}: {' / '.join(sorted(eps[ep]))}")

    # ---- 2. 稱謂前綴變體：strip_titles 後相同但原 key 不同 ----
    by_stripped = defaultdict(set)
    for k in matrix:
        by_stripped[strip_titles(k)].add(k)
    print("\n" + "=" * 70)
    print("【2】同一人物/事物的不同寫法（稱謂前綴變體）")
    print("=" * 70)
    n2 = 0
    for sk, keys in sorted(by_stripped.items()):
        if len(keys) < 2 or not sk:
            continue
        # 這些變體各自的譯名
        variant_info = []
        all_tr = set()
        for k in sorted(keys):
            trs = set()
            for ep_trs in matrix[k].values():
                trs |= ep_trs
            all_tr |= trs
            variant_info.append((k, sorted(matrix[k]), sorted(trs)))
        n2 += 1
        flag = " ⚠️ 譯名不一致" if len(all_tr) >= 2 else ""
        print(f"\n◇ 基底「{sk}」{flag}")
        for k, eps, trs in variant_info:
            print(f"    {sorted(surfaces[k])} {eps} → {' / '.join(trs)}")
    if n2 == 0:
        print("（無）")

    # ---- 3. 各集格式風格統計 ----
    print("\n" + "=" * 70)
    print("【3】各集格式風格統計（譯名欄位）")
    print("=" * 70)
    header = f"{'集數':<8}{'總數':>5}{'半形()':>7}{'全形（）':>8}{'書名號':>7}{'含英文':>7}{'數字前有空格':>10}{'數字貼字':>8}"
    print(header)
    print("-" * 70)
    for ep in sorted(data):
        rows = data[ep]
        n = len(rows)
        half = sum(1 for _, _, tr in rows if re.search(r"[()]", tr))
        full = sum(1 for _, _, tr in rows if re.search(r"[（）]", tr))
        book = sum(1 for _, _, tr in rows if "《" in tr)
        eng = sum(1 for _, _, tr in rows if re.search(r"[A-Za-z]", tr))
        num_sp = sum(1 for _, _, tr in rows if re.search(rf"[{CJK}] \d|\d [{CJK}]", tr))
        num_nosp = sum(1 for _, _, tr in rows if re.search(rf"[{CJK}]\d|\d[{CJK}]", tr))
        print(f"{ep:<8}{n:>5}{half:>7}{full:>8}{book:>7}{eng:>7}{num_sp:>10}{num_nosp:>8}")

    # 半形括號與數字貼字的明細（不一致來源）
    print("\n--- 半形括號明細 ---")
    for ep in sorted(data):
        items = [(t, tr) for t, _, tr in data[ep] if re.search(r"[()]", tr)]
        for t, tr in items:
            print(f"  {ep}: {t} → {tr}")
    print("\n--- 數字貼字（未加空格）明細 ---")
    for ep in sorted(data):
        items = [(t, tr) for t, _, tr in data[ep]
                 if re.search(rf"[{CJK}]\d|\d[{CJK}]", tr) and not re.search(rf"[{CJK}] \d|\d [{CJK}]", tr)]
        for t, tr in items:
            print(f"  {ep}: {t} → {tr}")

    # ---- 4. 單集內重複條目 ----
    print("\n" + "=" * 70)
    print("【4】單集內重複術語條目（同一 normalized term 多筆）")
    print("=" * 70)
    n4 = 0
    for ep in sorted(data):
        seen = defaultdict(list)
        for term, sid, tr in data[ep]:
            seen[norm_key(term)].append((term, tr))
        for k, items in seen.items():
            if len(items) > 1:
                n4 += 1
                trs = {tr for _, tr in items}
                flag = " ⚠️ 譯名不同" if len(trs) > 1 else ""
                print(f"  {ep}: {sorted(surfaces[k])} x{len(items)}{flag} → {' / '.join(sorted(trs))}")
    if n4 == 0:
        print("（無）")

    # ---- 5. 高頻共用術語（出現 >= 5 集）的一致性總覽 ----
    print("\n" + "=" * 70)
    print("【5】高頻共用術語（≥5 集）一致性總覽")
    print("=" * 70)
    common = [(k, eps) for k, eps in matrix.items() if len(eps) >= 5]
    common.sort(key=lambda x: (-len(x[1]), x[0]))
    for k, eps in common:
        all_tr = set()
        for trs in eps.values():
            all_tr |= trs
        status = "⚠️ 不一致" if len(all_tr) >= 2 else "✓ 一致"
        print(f"  [{len(eps):>2}集] {status}  {sorted(surfaces[k])[0]} → {' / '.join(sorted(all_tr))}")

    # ---- 6. 與 master 的 drift 檢查（sense 感知） ----
    print("\n" + "=" * 70)
    print("【6】各集詞彙表與 configs/terminology_master.yaml 的 drift 檢查")
    print("=" * 70)
    master_path = "configs/terminology_master.yaml"
    if not os.path.exists(master_path):
        print(f"（找不到 {master_path}，跳過）")
    else:
        with open(master_path, encoding="utf-8") as f:
            mdoc = yaml.safe_load(f)
        # (term_key, sense_id) -> 允許譯名集合（標準譯名 + variants）
        master_senses = {}
        term_allowed = defaultdict(set)  # term_key -> 所有 sense 譯名的聯集
        for t in (mdoc or {}).get("terms", []) or []:
            k = norm_key(str(t.get("term", "")))
            for s in t.get("senses", []) or []:
                allowed = set()
                pt = s.get("preferred_translation")
                if pt:
                    allowed.add(str(pt).strip())
                for v in s.get("variants", []) or []:
                    vt = v.get("translation")
                    if vt:
                        allowed.add(str(vt).strip())
                master_senses[(k, str(s.get("id", "")))] = allowed
                term_allowed[k] |= allowed

        drift = []          # 與 master 收錄譯名不符
        sid_mismatch = []   # 譯名相符但 sense id 未對齊
        for ep in sorted(data):
            for term, sid, tr in data[ep]:
                k = norm_key(term)
                if k not in term_allowed:
                    continue  # 單集術語本就不收錄於 master
                allowed = master_senses.get((k, sid))
                if allowed is not None:
                    if tr not in allowed:
                        drift.append((ep, term, sid, tr,
                                      " / ".join(sorted(allowed))))
                elif tr in term_allowed[k]:
                    sid_mismatch.append((ep, term, sid, tr))
                else:
                    drift.append((ep, term, sid, tr,
                                  " / ".join(sorted(term_allowed[k]))))
        if drift:
            print(f"\n⚠️ 譯名與 master 不符：{len(drift)} 筆")
            for ep, term, sid, tr, expected in drift:
                print(f"  {ep}: {term} [{sid}] → 實際「{tr}」，master 收錄「{expected}」")
        else:
            print("\n譯名與 master 一致 ✓")
        if sid_mismatch:
            print(f"\n◇ sense id 未對齊（譯名本身相符）：{len(sid_mismatch)} 筆")
            for ep, term, sid, tr in sid_mismatch:
                print(f"  {ep}: {term} [{sid}] → {tr}")

    print("\n" + "=" * 70)
    total = sum(len(v) for v in data.values())
    print(f"統計：{len(data)} 集、共 {total} 筆 sense 條目、{len(matrix)} 個唯一術語")
    print(f"不一致衝突 {len(conflicts)} 項（詳見【1】）")


if __name__ == "__main__":
    main()
