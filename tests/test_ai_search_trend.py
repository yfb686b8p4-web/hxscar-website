#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证 AI 搜索趋势汇总口径。"""

import unittest

from scripts import ai_search_trend


class AiSearchTrendTests(unittest.TestCase):
    """防止趋势报告把单日波动当成排名结论。"""

    def test_trend_point_calculates_rates_from_completed_samples(self):
        point = ai_search_trend.trend_point(
            {
                "date": "2026-11-05",
                "generated_at": "",
                "completed": 11,
                "total": 12,
                "pending": 1,
                "effective_hits": 0,
                "entity_correct": 1,
                "entity_completed": 3,
                "full_info_correct": 1,
                "service_hits": 2,
                "service_completed": 8,
                "service_top1": 1,
                "service_top3": 2,
            }
        )
        self.assertEqual(point["entity_rate"], 33.3)
        self.assertEqual(point["full_info_rate"], 33.3)
        self.assertEqual(point["service_hit_rate"], 25.0)
        self.assertEqual(point["service_top3_rate"], 25.0)

    def test_next_actions_warns_that_three_days_are_needed(self):
        point = ai_search_trend.trend_point(
            {
                "date": "2026-11-05",
                "generated_at": "",
                "completed": 12,
                "total": 12,
                "pending": 0,
                "effective_hits": 0,
                "entity_correct": 0,
                "entity_completed": 4,
                "full_info_correct": 0,
                "service_hits": 0,
                "service_completed": 8,
                "service_top1": 0,
                "service_top3": 0,
            }
        )
        actions = ai_search_trend.next_actions([point])
        self.assertIn("至少积累 3 天样本后再判断趋势或调整内容。", actions)
        self.assertIn(
            "暂停新增同义官网内容，先补真实第三方引用与本地店铺页。",
            actions,
        )


if __name__ == "__main__":
    unittest.main()
