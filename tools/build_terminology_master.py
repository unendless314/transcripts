#!/usr/bin/env python3
"""產生 configs/terminology_master.yaml（跨集標準譯名表）

收錄標準：出現於 >= 2 集的術語（單集專屬術語留在各集 data/UFO-XX/terminology.yaml）。
此表是全系列「標準譯名」的唯一權威來源（single source of truth）：
  - 校稿時若字幕正文與此表不符，以此表為準修正
  - 各集 terminology.yaml 的新增/修改應與此表對齊

資料模型：以 term + sense 聚合（尊重各集 terminology.yaml 的 multi-sense 設計）。
同一術語的不同語義保留為不同 sense，不壓成單一譯名；
同一 sense 的合理語境差異記錄於該 sense 的 variants 欄位。

人工判斷（廢棄譯名、語境說明、待查證項目）集中於 configs/terminology_master_rules.yaml，
修改規則請編輯該檔後重新產生本表。

用法：
  PYTHONPATH=. python3 tools/build_terminology_master.py --force
"""

import argparse
import datetime
import glob
import os
import re
import sys
from collections import defaultdict

import yaml

sys.stdout.reconfigure(encoding="utf-8")
sys.stderr.reconfigure(encoding="utf-8")

DEFAULT_RULES = "configs/terminology_master_rules.yaml"
DEFAULT_OUTPUT = "configs/terminology_master.yaml"

HEADER = """# Terminology Master - UFO Citizen Hearing 全系列標準譯名表
#
# 收錄標準：出現於 >= 2 集的跨集術語（共 {n_cross} 個）。
# 單集專屬術語（僅出現 1 集，共 {n_single} 個）請見各集 data/UFO-XX/terminology.yaml。
#
# 此表是全系列「標準譯名」的唯一權威來源：
#   ✅ 校稿時字幕正文若與此表不符，以此表為準修正
#   ✅ 各集 terminology.yaml 的新增/修改應與此表對齊
#   ❌ 不要在此表加入 segments 欄位（段落對照請見各集檔案）
#
# 資料模型：以 term + sense 聚合，同一術語的不同語義保留為不同 sense；
# 同一 sense 的合理語境差異記錄於該 sense 的 variants 欄位。
# 人工判斷（廢棄譯名、語境說明、待查證項目）集中於 configs/terminology_master_rules.yaml。
#
# 全系列格式規範（2026-08 校稿確立）：
#   - 台灣用語：飛彈（非導彈）、網路（非網絡）、國家安全會議（非委員會）、布希（非布什）
#   - 作品名稱加書名號：《世界大戰》、《遠古外星人》（僅限指節目本身時）
#   - 數字與型號前後加空格：阿波羅 14 號、F-4 幽靈戰鬥機、行政命令 12958（年份除外：1947年）
#   - 括號用全形：（）而非 ()
#   - 縮寫標註格式：中文（縮寫），如 資訊自由法（FOIA）、國家安全局（NSA）；CIA 除外，直接用 CIA
#
# 產生方式：PYTHONPATH=. python3 tools/build_terminology_master.py --force
# 最後更新：{date}（依 20 集 terminology.yaml 校稿後版本自動產生）
"""


def norm_key(term):
    return re.sub(r"\s+", " ", term.strip().lower())


def load_rules(path):
    with open(path, encoding="utf-8") as f:
        doc = yaml.safe_load(f) or {}
    return (
        doc.get("deprecated", {}) or {},
        doc.get("contextual", {}) or {},
        doc.get("needs_verification", {}) or {},
    )


def main():
    ap = argparse.ArgumentParser(
        description="產生 configs/terminology_master.yaml（跨集標準譯名表）")
    ap.add_argument("--rules", default=DEFAULT_RULES,
                    help=f"人工判斷規則檔（預設 {DEFAULT_RULES}）")
    ap.add_argument("--output", default=DEFAULT_OUTPUT,
                    help=f"輸出路徑（預設 {DEFAULT_OUTPUT}）")
    ap.add_argument("--force", action="store_true",
                    help="覆寫已存在的輸出檔案（未加此旗標時拒絕覆寫）")
    args = ap.parse_args()

    if os.path.exists(args.output) and not args.force:
        print(f"❌ 輸出檔已存在：{args.output}（確認要覆寫請加 --force）",
              file=sys.stderr)
        sys.exit(1)

    deprecated, contextual, needs_verification = load_rules(args.rules)

    # term_key -> {surfaces, eps, senses: {sense_id: {definition, eps, trs:{tr: set(eps)}}}}
    terms = {}
    for path in sorted(glob.glob("data/UFO-*/terminology.yaml")):
        ep = re.search(r"(UFO-\d+)", path).group(1)
        with open(path, encoding="utf-8") as f:
            doc = yaml.safe_load(f)
        for t in doc.get("terms", []) or []:
            term = str(t.get("term", "")).strip()
            k = norm_key(term)
            td = terms.setdefault(k, {"surfaces": set(), "eps": set(), "senses": {}})
            td["surfaces"].add(term)
            td["eps"].add(ep)
            for s in t.get("senses", []) or []:
                sid = str(s.get("id", "")).strip() or re.sub(r"\W+", "_", k).strip("_")
                sd = td["senses"].setdefault(sid, {
                    "definition": None, "eps": set(), "trs": defaultdict(set),
                })
                sd["eps"].add(ep)
                tr = s.get("preferred_translation")
                if tr:
                    sd["trs"][str(tr).strip()].add(ep)
                if sd["definition"] is None and s.get("definition"):
                    sd["definition"] = str(s["definition"]).strip()

    # 只收跨集術語，按字母排序
    cross = [(k, v) for k, v in terms.items() if len(v["eps"]) >= 2]
    cross.sort(key=lambda x: x[0])
    n_single = len(terms) - len(cross)

    out_terms = []
    for k, v in cross:
        surfaces = sorted(v["surfaces"])

        senses_out = []
        for sid, sd in sorted(v["senses"].items()):
            trs = sd["trs"]
            # 標準譯名：出現集數最多者；同票時取較短（無標註）形式
            canonical = max(trs, key=lambda tr: (len(trs[tr]), -len(tr))) if trs else ""
            sense_doc = {
                "id": sid,
                "definition": sd["definition"] or "",
                "preferred_translation": canonical,
                "episodes": sorted(sd["eps"]),
            }
            variants = sorted(tr for tr in trs if tr != canonical)
            if variants:
                sense_doc["variants"] = [
                    {"translation": tr, "episodes": sorted(trs[tr])}
                    for tr in variants
                ]
            senses_out.append(sense_doc)

        notes_parts = []
        if len(surfaces) > 1:
            notes_parts.append("亦寫作：" + "、".join(surfaces[1:]))
        if k in deprecated:
            notes_parts.append("廢棄譯名（校稿時發現請改正）：" + "、".join(deprecated[k]))
        if k in contextual:
            notes_parts.append(contextual[k])
        if k in needs_verification:
            notes_parts.append("⚠️ 需查證：" + needs_verification[k])

        term_doc = {
            "term": surfaces[0],
            "senses": senses_out,
            "episodes": sorted(v["eps"]),
        }
        if notes_parts:
            term_doc["notes"] = "；".join(notes_parts)
        if len(surfaces) > 1:
            term_doc["also_written_as"] = surfaces[1:]
        out_terms.append(term_doc)

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(HEADER.format(
            n_cross=len(out_terms),
            n_single=n_single,
            date=datetime.date.today().isoformat(),
        ))
        yaml.dump({"terms": out_terms}, f, allow_unicode=True,
                  sort_keys=False, width=1000)

    print(f"已產生 {args.output}，收錄 {len(out_terms)} 個跨集術語"
          f"（另有 {n_single} 個單集術語未收錄）")


if __name__ == "__main__":
    main()
