#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证可见性洞察使用最新已完成检测记录。"""

import unittest

from scripts import visibility_insights


class VisibilityInsightsTests(unittest.TestCase):
    """防止最终洞察继续使用过期或全待测快照。"""

    def test_aggregate_records_ignores_pending_and_calculates_rates(self):
        records = [
            {
                "status": "completed",
                "platform": "豆包",
                "category": "宝马与豪车",
                "mentioned": True,
                "effective_hit": True,
                "position": "1",
            },
            {
                "status": "completed",
                "platform": "元宝",
                "category": "宝马与豪车",
                "mentioned": False,
                "effective_hit": False,
                "position": "",
            },
            {
                "status": "pending",
                "platform": "豆包",
                "category": "空调诊断维修",
                "mentioned": False,
            },
        ]
        summary = visibility_insights.aggregate_records(records)
        self.assertEqual(summary["overall"]["completed"], 2)
        self.assertEqual(summary["overall"]["pending"], 1)
        self.assertEqual(summary["overall"]["mention_rate"], 50.0)
        self.assertEqual(summary["overall"]["effective_hit_rate"], 50.0)
        self.assertEqual(
            summary["by_platform"]["豆包"]["average_position"],
            1.0,
        )
        self.assertEqual(
            summary["by_category"]["宝马与豪车"]["completed"],
            2,
        )
        self.assertNotIn("空调诊断维修", summary["by_category"])

    def test_daily_negative_mentions_detects_wrong_identity(self):
        records = [
            {
                "status": "completed",
                "platform": "元宝",
                "query": "华信松与老周修车是同一家吗",
                "identity_relation": "wrong",
                "notes": "实体关系错误",
            },
            {
                "status": "pending",
                "platform": "豆包",
                "query": "测试待办",
                "identity_relation": "wrong",
            },
        ]
        negatives = visibility_insights.daily_negative_mentions(records)
        self.assertEqual(len(negatives), 1)
        self.assertEqual(negatives[0]["platform"], "元宝")


if __name__ == "__main__":
    unittest.main()
