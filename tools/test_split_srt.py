#!/usr/bin/env python3
"""
Regression tests for tools/split_srt.py bracket-aware splitting.

Run: python -m unittest tools.test_split_srt
  or python tools/test_split_srt.py
"""

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from split_srt import find_split_point, _compute_depths  # noqa: E402

MIN_CHARS = 10


def split_text(text, **kwargs):
    result = find_split_point(text, MIN_CHARS, **kwargs)
    if result is None:
        return None, None
    split_pos, punct, _ = result
    return text[:split_pos], text[split_pos:]


class HardProtectionTests(unittest.TestCase):
    """Hard brackets （）()《》【】[] must never be split inside."""

    def test_parenthesized_english_name_not_split(self):
        # Only candidate in the window is the space inside （...）; no other
        # punctuation exists anywhere -> must refuse to split
        text = "我們歡迎來自美國的貴賓參議員（Carolyn Cheeks Kilpatrick）蒞臨今天的現場"
        self.assertIsNone(find_split_point(text, MIN_CHARS))

    def test_falls_back_to_comma_outside_parentheses(self):
        text = ("今天國會聽證會上邀請到卡蘿琳基爾派翠克眾議員"
                "（Carolyn Cheeks Kilpatrick）針對國防預算發表演說，"
                "內容涵蓋多項未來政策方向與預算配置細節")
        part1, part2 = split_text(text)
        self.assertIsNotNone(part1)
        self.assertIn("（Carolyn Cheeks Kilpatrick）", part1)
        self.assertTrue(part1.endswith("，"))
        self.assertGreaterEqual(len(part2), MIN_CHARS)

    def test_book_title_mark_protected(self):
        text = "最近正在閱讀一本非常有意思的書籍叫做《The Day After Roswell》讀後感觸很深久久不能自己"
        self.assertIsNone(find_split_point(text, MIN_CHARS))

    def test_half_width_parens_protected(self):
        text = "國防部宣布與加拿大武裝部隊(Canadian Defence Force)展開聯合演訓，雙方將進行為期數週的協調"
        part1, part2 = split_text(text)
        self.assertIsNotNone(part1)
        self.assertIn("(Canadian Defence Force)", part1)
        self.assertTrue(part1.endswith("，"))

    def test_unmatched_hard_opener_protects_to_end(self):
        text = "根據未經證實的消息來源（某位不願具名的官員透露國防部正在評估一項新計畫，但目前還沒有具體結論"
        self.assertIsNone(find_split_point(text, MIN_CHARS))

    def test_unmatched_hard_closer_does_not_block(self):
        text = "這項傳聞後來被證實為假消息）相關單位出面澄清，強調一切都只是誤會並沒有任何隱瞞或不實的情況"
        part1, part2 = split_text(text)
        self.assertIsNotNone(part1)
        self.assertTrue(part1.endswith("，"))


class SoftQuoteFallbackTests(unittest.TestCase):
    """Quotes 「」『』 are only split inside as a last resort."""

    def test_comma_inside_quotes_used_only_as_fallback(self):
        # The only punctuation in the whole segment is inside 「...」
        text = "他當時只說了一句話「我們今天必須完成這項任務，否則一切都來不及了」隨後便離開了現場沒有多做任何解釋說明"
        part1, part2 = split_text(text)
        self.assertIsNotNone(part1)
        self.assertTrue(part1.endswith("，"))
        self.assertGreaterEqual(len(part2), MIN_CHARS)

    def test_punctuation_outside_quotes_preferred(self):
        text = "會議開始前主席先宣布了議程，隨後提到「今天的討論重點是預算」然後進入正式討論階段大家開始發言"
        part1, part2 = split_text(text)
        self.assertEqual(part1, "會議開始前主席先宣布了議程，")

    def test_nested_quotes_fallback(self):
        text = "報導指出「發言人表示『我們對結果感到滿意，未來會繼續努力』現場響起掌聲」這段談話隨即引發熱議"
        part1, part2 = split_text(text)
        self.assertIsNotNone(part1)
        self.assertTrue(part1.endswith("，"))

    def test_unmatched_quote_opener_no_crash_and_soft_fallback(self):
        text = "他忽然大喊一聲「大家快點離開這裡非常危險，不要再繼續停留了快點撤退"
        part1, part2 = split_text(text)
        self.assertIsNotNone(part1)
        self.assertTrue(part1.endswith("，"))

    def test_unmatched_quote_closer_does_not_block(self):
        text = "現場情況十分混亂」警方隨後宣布封鎖周邊區域，並要求所有民眾配合疏散保持冷靜"
        part1, part2 = split_text(text)
        self.assertIsNotNone(part1)
        self.assertTrue(part1.endswith("，"))


class EmDashTests(unittest.TestCase):
    def test_em_dash_two_chars_outside_protection(self):
        text = "這個計畫的最終結果出乎所有人意料——負責單位在最後一刻才宣布了決定，讓許多等待的民眾感到相當錯愕"
        part1, part2 = split_text(text)
        self.assertIsNotNone(part1)
        self.assertTrue(part1.endswith("——"))


class SpaceSplitTests(unittest.TestCase):
    EN = ("This is a fairly long English sentence without any punctuation marks "
          "at all so the only way to split it is on a space")

    def test_space_not_used_by_default(self):
        self.assertIsNone(find_split_point(self.EN, MIN_CHARS))

    def test_space_used_when_opted_in(self):
        result = find_split_point(self.EN, MIN_CHARS, allow_space_splits=True)
        self.assertIsNotNone(result)
        split_pos, punct, _ = result
        self.assertEqual(punct, ' ')
        self.assertEqual(self.EN[split_pos - 1], ' ')

    def test_space_inside_parens_still_protected_when_opted_in(self):
        text = "我們歡迎來自美國的貴賓參議員（Carolyn Cheeks Kilpatrick）蒞臨今天的現場"
        self.assertIsNone(find_split_point(text, MIN_CHARS, allow_space_splits=True))


class DepthComputationTests(unittest.TestCase):
    def test_nested_hard_and_quote_depths(self):
        text = "外（內「深」外）尾"
        hard, quote = _compute_depths(text)
        # indices: 0外 1（ 2內 3「 4深 5」 6外 7） 8尾
        self.assertEqual(hard[0], 0)   # 外
        self.assertEqual(hard[2], 1)   # 內 inside （
        self.assertEqual(hard[6], 1)   # 外 inside （, after 」
        self.assertEqual(hard[8], 0)   # 尾 after ）
        self.assertEqual(quote[3], 1)  # 「 opener
        self.assertEqual(quote[4], 1)  # 深
        self.assertEqual(quote[6], 0)  # after 」


if __name__ == '__main__':
    unittest.main()
