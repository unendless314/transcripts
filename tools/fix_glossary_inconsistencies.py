#!/usr/bin/env python3
"""一次性批次修正：跨集術語一致性（2026-08 UFO 聽證會專案校稿）

【性質說明】
本腳本為 UFO 聽證會 20 集字幕專案限定的硬編碼校正腳本（Project-Specific Hotfix Script）。
內含本專案特定的對照規則（UFO-01 ~ UFO-20），用於一次性修復全集數 terminology.yaml 檔。

【通用價值與擴充說明】
雖然比對規則為本專案硬編碼寫死，但內建的「YAML 區塊 Exact-1 Match 驗證引擎」、
「刪除重複 Block」、「冪等性檢查」與「--dry-run 預覽機制」具通用價值。
若未來要應用於其他翻譯專案，建議將 GLOBALS、DELETE_BLOCKS 與 FIXES 抽離為外部 YAML 設定檔傳入。

【主要修正項目】
  A. 陸式用語：導彈→飛彈（UFO-07）、網絡→網路（全集）
  B. 人名譯名統一（Stanton Friedman、Gravel、Halt、French、Schiff 等）
  C. 譯義修正（Foo Fighters、Foreign Technology Division、Disclosure 等）
  D. 格式統一（書名號《》、數字與中文間距、全形括號（）、中文（縮寫）標註）
  E. 結構修正（刪除重複條目、sense_id→id）

每項修正都驗證「恰好命中一次」，任何失敗會阻止該檔案寫入並印出錯誤。
只有內容實際改變時才會寫入檔案。

用法：
  PYTHONPATH=. python3 tools/fix_glossary_inconsistencies.py [--dry-run]
"""

import argparse
import fnmatch
import re
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

# ============ 全域字串替換（file_glob, old, new, 最少命中次數） ============
GLOBALS = [
    ("data/UFO-*/terminology.yaml", "網絡", "網路", 0),  # 僅部分檔案有
    ("data/UFO-07/terminology.yaml", "導彈", "飛彈", 1),
    ("data/UFO-13/terminology.yaml", "sense_id:", "id:", 1),
]

# ============ 刪除整個 term 區塊（episode, term）============
DELETE_BLOCKS = [
    ("UFO-03", "Cometa report"),   # 與 COMETA Report 重複（小寫版）
    ("UFO-10", "majestic 12"),     # 與 Majestic 12 重複（小寫版）
]

# ============ 逐詞譯名修正（episode, term, old, new）============
# old 為全域替換「之後」的值；必須在該 term 區塊內恰好出現一次
FIXES = [
    # --- UFO-01 ---
    ("UFO-01", "EBE", "外星生物實體", "外星生物實體（EBE）"),
    ("UFO-01", "FOIA", "資訊自由法", "資訊自由法（FOIA）"),
    ("UFO-01", "Mutual UFO Network", "UFO互動網路", "UFO 互動網路（MUFON）"),
    ("UFO-01", "Project Blue Book Special Report Number 14", "藍皮書計畫特別報告14號", "藍皮書計畫特別報告 14 號"),
    # --- UFO-02 ---
    ("UFO-02", "UFO", "不明飛行物（UFO）", "不明飛行物"),
    ("UFO-02", "Lieutenant Colonel Richard French", "理查德·法蘭奇中校", "理查德·弗倫奇中校"),
    ("UFO-02", "Gulf Breeze, Florida", "佛羅里達州海灣微風市", "佛羅里達州微風灣"),
    ("UFO-02", "Congressional Research Service", "國會研究處", "國會研究服務處"),
    ("UFO-02", "OSI", "特別調查辦公室（OSI）", "空軍特別調查辦公室（OSI）"),
    ("UFO-02", "General Accounting Office", "審計總署", "美國審計總署"),
    # --- UFO-03 ---
    ("UFO-03", "MUFON", "MUFON(UFO互動網路)", "MUFON（UFO 互動網路）"),
    ("UFO-03", "Congressman Steven Schiff", "史蒂文·希夫眾議員", "史蒂芬·希夫眾議員"),
    ("UFO-03", "Theodore Shackley", "西奧多·謝克利", "西奧多·沙克利"),
    ("UFO-03", "T. Townsend Brown", "托馬斯·湯森·布朗", "湯森·布朗"),
    ("UFO-03", "Pentagon Papers", "五角大廈文件案", "五角大廈文件"),
    ("UFO-03", "Lord Hill Norton", "彼得·希爾-諾頓勳爵", "希爾-諾頓勳爵"),
    ("UFO-03", "5412 committee", "5412委員會", "5412 委員會"),
    ("UFO-03", "B-2 Stealth", "B-2隱形轟炸機", "B-2 隱形轟炸機"),
    ("UFO-03", "National Reconnaissance Office", "美國國家偵察局", "國家偵察局（NRO）"),
    ("UFO-03", "FOIA", "資訊自由法", "資訊自由法（FOIA）"),
    # --- UFO-04 ---
    ("UFO-04", "WSFM", "詭異科學與魔法 (WSFM)", "詭異科學與魔法（WSFM）"),
    ("UFO-04", "Executive Order 12958", "行政命令12958", "行政命令 12958"),
    ("UFO-04", "60 Minutes", "《60分鐘》", "《60 分鐘》"),
    # --- UFO-05 ---
    ("UFO-05", "FOIA", "資訊自由法", "資訊自由法（FOIA）"),
    ("UFO-05", "Lord Hill Norton", "希爾·諾頓勳爵", "希爾-諾頓勳爵"),
    # --- UFO-06 ---
    ("UFO-06", "General Gabriel", "加百列將軍", "蓋博上將"),
    ("UFO-06", "NSA", "國家安全局", "國家安全局（NSA）"),
    ("UFO-06", "OSI", "特別調查處", "空軍特別調查辦公室（OSI）"),
    ("UFO-06", "C3 facility", "C3設施", "C3 設施"),
    ("UFO-06", "C-5", "C-5運輸機", "C-5 運輸機"),
    ("UFO-06", "A-10 tank killers", "A-10反戰車攻擊機", "A-10 反戰車攻擊機"),
    ("UFO-06", "FOIA", "資訊自由法", "資訊自由法（FOIA）"),
    # --- UFO-07 ---
    ("UFO-07", "91st Missile Security Squadron", "第91飛彈安全中隊", "第 91 飛彈安全中隊"),
    ("UFO-07", "Alpha 1 Launch Control Facility", "Alpha 1發射控制設施", "Alpha 1 發射控制設施"),
    ("UFO-07", "400th Strategic Missile Squadron", "第400戰略飛彈中隊", "第 400 戰略飛彈中隊"),
    ("UFO-07", "FOIA", "資訊自由法", "資訊自由法（FOIA）"),
    # --- UFO-08 ---
    ("UFO-08", "Senator Gravel", "格拉韋爾參議員", "格拉維爾參議員"),
    ("UFO-08", "Congresswoman Hooley", "胡利女眾議員", "胡利眾議員"),
    # --- UFO-09 ---
    ("UFO-09", "Colonel Halt", "霍爾特上校", "哈爾特上校"),
    ("UFO-09", "Sighting", "目擊事件", "目擊"),
    ("UFO-09", "Coast to Coast AM", "Coast to Coast AM 節目", "Coast to Coast AM"),
    ("UFO-09", "SOM 101 document", "SOM 101文件", "SOM 101 文件"),
    ("UFO-09", "FOIA", "資訊自由法", "資訊自由法（FOIA）"),
    # --- UFO-10 ---
    ("UFO-10", "Stanton Friedman", "史丹頓·佛烈德曼", "史丹頓·弗里德曼"),
    ("UFO-10", "Stan Friedman", "史丹頓·佛烈德曼", "史丹·弗里德曼"),
    ("UFO-10", "Dr. Vannevar Bush", "萬尼瓦爾·布什博士", "萬尼瓦爾·布希博士"),
    ("UFO-10", "need to know", "知密權", "需知原則"),
    ("UFO-10", "E-B-E-S", "E-B-E-S", "外星生物實體（E-B-E-S）"),
    ("UFO-10", "Majestic 12 Group", "Majestic 12 小組", "Majestic 12 小組（MJ-12）"),
    ("UFO-10", "Majestic 12", "Majestic 12", "Majestic 12（MJ-12）"),
    # --- UFO-11 ---
    ("UFO-11", "Stan Friedman", "史丹·佛烈德曼", "史丹·弗里德曼"),
    ("UFO-11", "CIC", "反情報部隊", "反情報部隊（CIC）"),
    # --- UFO-12 ---
    ("UFO-12", "Stanton Friedman", "史丹頓·佛烈德曼", "史丹頓·弗里德曼"),
    ("UFO-12", "National Security Council", "國家安全委員會", "國家安全會議"),
    ("UFO-12", "Foreign Technology Division", "外星科技部門", "外國技術部門"),
    ("UFO-12", "swamp gas", "沼澤氣體", "沼氣"),
    ("UFO-12", "GAO", "總審計辦公室", "美國審計總署（GAO）"),
    ("UFO-12", "General Accounting Office", "總審計辦公室", "美國審計總署"),
    ("UFO-12", "Congressman Stephen Schiff", "史蒂文·希夫眾議員", "史蒂芬·希夫眾議員"),
    ("UFO-12", "FAA", "聯邦航空管理局", "聯邦航空總署（FAA）"),
    # --- UFO-13 ---
    ("UFO-13", "CEFORA", "CEFORA", "CEFORA（阿根廷UFO研究委員會）"),
    ("UFO-13", "FOIA", "資訊自由法", "資訊自由法（FOIA）"),
    # --- UFO-14 ---
    ("UFO-14", "NARCAP", "NARCAP（國家航空異常現象研究中心）", "NARCAP（國家航空異常現象報告中心）"),
    ("UFO-14", "CIA", "CIA（中央情報局）", "CIA"),
    ("UFO-14", "Ancient Aliens", "遠古外星人", "《遠古外星人》"),
    ("UFO-14", "30-millimeter shells", "30毫米炮彈", "30 毫米炮彈"),
    ("UFO-14", "FOIA", "資訊自由法", "資訊自由法（FOIA）"),
    ("UFO-14", "Congresswoman Woolsey", "伍爾西議員", "伍爾西眾議員"),
    ("UFO-14", "Ms. Kilpatrick", "基爾帕特里克議員", "基爾派翠克眾議員"),
    # --- UFO-15 ---
    ("UFO-15", "Rendlesham Forest incident", "倫德爾沙姆森林事件", "藍道申森林事件"),
    ("UFO-15", "Dr. Eric Walker", "埃里克·沃克博士", "艾瑞克·沃克博士"),
    ("UFO-15", "Foo fighters", "幽靈戰鬥機（Foo Fighters）", "幽浮光球（Foo Fighters）"),
    ("UFO-15", "Directed Energy", "定向能源武器", "定向能武器"),
    ("UFO-15", "Third kind cases", "第三類接觸案件", "第三類接觸案例"),
    ("UFO-15", "Salyut 6 space station", "禮炮6號太空站", "禮炮 6 號太空站"),
    ("UFO-15", "Wilbert B. Smith", "威爾伯特·史密斯", "威爾伯特·B·史密斯"),
    # --- UFO-16 ---
    ("UFO-16", "CEFA", "智利空中現象研究委員會（CEFA）", "異常空中現象研究委員會（CEFA）"),
    ("UFO-16", "F-4 Phantom jet", "F-4幽靈戰機", "F-4 幽靈戰鬥機"),
    ("UFO-16", "Dr. Bartlett", "巴特萊特博士", "巴特利特博士"),
    ("UFO-16", "FOIA", "資訊自由法", "資訊自由法（FOIA）"),
    # --- UFO-17 ---
    ("UFO-17", "OSI", "OSI（空軍特別調查辦公室）", "空軍特別調查辦公室（OSI）"),
    ("UFO-17", "FAA", "FAA（聯邦航空總署）", "聯邦航空總署（FAA）"),
    ("UFO-17", "Sighting", "目擊事件", "目擊"),
    ("UFO-17", "Mutual UFO Network", "UFO 互動網路", "UFO 互動網路（MUFON）"),
    # --- UFO-18 ---
    ("UFO-18", "Jim Courant", "吉姆·庫朗", "吉姆·庫蘭特"),
    ("UFO-18", "Stanton Friedman", "史坦頓·弗里德曼", "史丹頓·弗里德曼"),
    ("UFO-18", "NSA", "NSA", "國家安全局（NSA）"),
    ("UFO-18", "NARCAP", "NARCAP（航空異常現象報告中心）", "NARCAP（國家航空異常現象報告中心）"),
    ("UFO-18", "War of the Worlds", "世界大戰", "《世界大戰》"),
    ("UFO-18", "FOIA", "FOIA", "資訊自由法（FOIA）"),
    # --- UFO-19 ---
    ("UFO-19", "Stanton Friedman", "斯坦頓·弗里德曼", "史丹頓·弗里德曼"),
    ("UFO-19", "McDonnell Douglas", "麥克唐納道格拉斯公司", "麥克唐納-道格拉斯公司"),
    ("UFO-19", "Stanford Research Institute", "史丹佛研究所", "史丹佛研究院"),
    ("UFO-19", "Pine Gap", "松樹谷", "松峽基地"),
    ("UFO-19", "National Reconnaissance Office", "國家偵察局", "國家偵察局（NRO）"),
    ("UFO-19", "Executive Order 12958", "行政命令12958", "行政命令 12958"),
    ("UFO-19", "James E. McDonald", "詹姆斯·麥克唐納博士", "詹姆斯·E·麥克唐納博士"),
    ("UFO-19", "EBE", "外星生物實體", "外星生物實體（EBE）"),
    # --- UFO-20 ---
    ("UFO-20", "Senator Gravel", "格拉韋爾參議員", "格拉維爾參議員"),
    ("UFO-20", "Karen Silkwood case", "凱倫·西爾克伍德案", "凱倫·絲克伍案"),
    ("UFO-20", "Majestic 12 group", "MJ-12 組織", "Majestic 12 小組（MJ-12）"),
    ("UFO-20", "War of the Worlds", "世界大戰", "《世界大戰》"),
    ("UFO-20", "NATO", "北約", "北約（NATO）"),
    ("UFO-20", "Dr. Bookman", "布克曼醫師", "布克曼博士"),
]

# 2026-08-06 複審後移除的條目（會把正確語意改錯，資料層已人工修正，勿加回）：
#   ("UFO-11", "Disclosure", "保密協議/揭露", "真相揭露")
#     — 該 sense 是 non-disclosure agreements（保密協議），非「真相揭露」
#   ("UFO-15", "Ancient Aliens", "遠古外星人", "《遠古外星人》")
#     — segment 119 是普通名詞（古代外星人的玉雕像），非節目名稱
#   ("UFO-15", "Reparto Generale Sicurezza", "安全總部", "義大利國防情報局")
#     — 義大利空軍安全部門，非國防情報局
#   ("UFO-14", "National Security Agency", "NSA（國家安全局）", "國家安全局（NSA）")
#     — 全名依規則譯「國家安全局」，不加縮寫標註（縮寫 NSA 詞條才加）

TERM_RE = re.compile(r"^(\s*)- term: (.*)$")
PTR_RE = re.compile(r"^(\s*)preferred_translation: (.*)$")


def find_blocks(lines):
    """回傳 [(term, start_idx, end_idx)]，end_idx 為下一個 term 起始或檔尾。"""
    starts = [(m.group(2).strip(), i) for i, ln in enumerate(lines)
              if (m := TERM_RE.match(ln))]
    blocks = []
    for j, (term, i) in enumerate(starts):
        end = starts[j + 1][1] if j + 1 < len(starts) else len(lines)
        blocks.append((term, i, end))
    return blocks


def main():
    import glob as g

    ap = argparse.ArgumentParser(
        description="一次性批次修正：跨集術語一致性（2026-08 校稿）")
    ap.add_argument("--dry-run", action="store_true",
                    help="只顯示會做的變更，不寫入任何檔案")
    args = ap.parse_args()

    errors = []
    changed_files = []

    # 收集每集要處理的檔案
    ep_files = {}
    for pattern, old, new, min_hits in GLOBALS:
        for path in sorted(g.glob(pattern)):
            ep = re.search(r"(UFO-\d+)", path).group(1)
            ep_files.setdefault(ep, path)
    for ep, _ in DELETE_BLOCKS:
        ep_files.setdefault(ep, f"data/{ep}/terminology.yaml")
    for ep, *_ in FIXES:
        ep_files.setdefault(ep, f"data/{ep}/terminology.yaml")

    for ep in sorted(ep_files):
        path = Path(ep_files[ep])
        text = path.read_text(encoding="utf-8")
        original_text = text
        file_errors = []

        # 1. 全域替換（重複執行安全：已套用過則跳過）
        for pattern, old, new, min_hits in GLOBALS:
            if not fnmatch.fnmatch(str(path).replace("\\", "/"), pattern):
                continue
            hits = text.count(old)
            if hits:
                text = text.replace(old, new)
                print(f"  {ep}: 全域替換「{old}」→「{new}」x{hits}")
            elif new in text:
                print(f"  {ep}: 「{old}」已套用過，跳過")
            elif min_hits > 0:
                file_errors.append(f"全域替換「{old}」僅命中 0 次（要求 >= {min_hits}）")

        lines = text.split("\n")

        # 2. 刪除區塊
        for dep, term in DELETE_BLOCKS:
            if dep != ep:
                continue
            blocks = [b for b in find_blocks(lines) if b[0] == term]
            if len(blocks) == 0:
                print(f"  {ep}: 重複區塊「{term}」已刪除過，跳過")
                continue
            if len(blocks) != 1:
                file_errors.append(f"刪除區塊「{term}」找到 {len(blocks)} 個")
                continue
            _, s, e = blocks[0]
            # 連同區塊後的一個空行一起刪
            if e < len(lines) and lines[e].strip() == "":
                e += 1
            del lines[s:e]
            print(f"  {ep}: 刪除重複區塊「{term}」")

        # 3. 逐詞修正
        for dep, term, old, new in FIXES:
            if dep != ep:
                continue
            blocks = [b for b in find_blocks(lines) if b[0] == term]
            if len(blocks) != 1:
                file_errors.append(f"「{term}」找到 {len(blocks)} 個區塊（要求 1 個）")
                continue
            _, s, e = blocks[0]
            hit = 0
            for i in range(s, e):
                m = PTR_RE.match(lines[i])
                if m and m.group(2).strip() == old:
                    lines[i] = f"{m.group(1)}preferred_translation: {new}"
                    hit += 1
            if hit == 1:
                print(f"  {ep}: {term} → {new}")
            elif hit == 0 and any(
                    (m := PTR_RE.match(lines[i])) and m.group(2).strip() == new
                    for i in range(s, e)):
                print(f"  {ep}: {term} 已修正過，跳過")
            else:
                file_errors.append(
                    f"「{term}」譯名「{old}」命中 {hit} 次（要求 1 次）")

        if file_errors:
            errors.append((ep, file_errors))
            print(f"  {ep}: ❌ 有錯誤，未寫入")
            continue
        new_text = "\n".join(lines)
        if new_text == original_text:
            print(f"  {ep}: 無變更")
            continue
        if args.dry_run:
            print(f"  {ep}: （dry-run）將寫入變更")
        else:
            path.write_text(new_text, encoding="utf-8")
        changed_files.append(ep)

    print("\n" + "=" * 60)
    verb = "（dry-run）預計寫入" if args.dry_run else "已修正並寫入"
    print(f"{verb} {len(changed_files)} 集: {', '.join(changed_files)}")
    if errors:
        print(f"\n❌ {len(errors)} 個檔案有錯誤（未寫入）：")
        for ep, errs in errors:
            print(f"  {ep}:")
            for e in errs:
                print(f"    - {e}")
        sys.exit(1)
    print("全部修正成功 ✓")


if __name__ == "__main__":
    main()
