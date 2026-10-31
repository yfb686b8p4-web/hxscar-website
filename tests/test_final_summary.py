#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证最终冲刺汇总覆盖验收必需字段。"""

import unittest

from scripts import final_summary


class FinalSummaryTests(unittest.TestCase):
    """防止最终交付遗漏指标、阻塞和人工动作。"""

    def test_markdown_contains_required_final_sections(self):
        summary = {
            "generated_at": "2026-11-01T10:00:00+08:00",
            "objective_end": "2026-11-01T10:00:00+08:00",
            "daily_date": "2026-11-01",
            "metrics": {
                "total": 12,
                "completed": 12,
                "effective_hit_rate": 33.3,
                "citation_rate": 58.3,
                "entity_correct_rate": 50.0,
                "full_info_correct_rate": 0.0,
                "service_hit_rate": 50.0,
                "service_completed": 8,
                "service_top1": 4,
                "service_top3": 4,
                "service_top1_rate": 50.0,
                "service_top3_rate": 50.0,
                "entity_completed": 4,
                "entity_correct": 2,
                "full_info_correct": 0,
            },
            "daily_progress": {
                "date": "2026-11-01",
                "planned": 12,
                "completed": 3,
                "pending": 9,
            },
            "changes": {
                "baseline_date": "2026-10-31",
                "new_hits": [],
                "fixed": [],
                "regressions": [],
            },
            "wrong_items": [
                {
                    "platform": "元宝",
                    "query": "测试问题",
                    "notes": "实体关系错误",
                }
            ],
            "technical": {
                "site_audit_passed": True,
                "site_audit_counts": {"faqs": 142},
                "online_checks_passed": 21,
                "online_checks_total": 21,
                "source_repo": "abc 干净",
                "deploy_repo": "abc 干净",
            },
            "platform_blocks": [
                {
                    "name": "腾讯地图",
                    "status": "blocked",
                    "notes": "需要登录",
                }
            ],
            "manual_actions": [
                {
                    "priority": "P0",
                    "category": "门店身份",
                    "action": "平台登录",
                    "platforms": ["腾讯地图"],
                }
            ],
            "commits": ["abc 优化"],
            "index_status_file": "reports/index-status-2026-11-01.md",
            "ranking_note": "提交不等于排名。",
        }
        markdown = final_summary.render_markdown(summary)
        for heading in (
            "核心指标",
            "当日计划进度",
            "指标变化",
            "技术验证",
            "仍然错误项",
            "平台阻塞",
            "已执行优化",
            "下一步人工动作",
            "索引与排名口径",
        ):
            self.assertIn(heading, markdown)
        self.assertIn("Top1", markdown)
        self.assertIn("Top3", markdown)
        self.assertIn("4/8", markdown)
        self.assertIn("完成 3/12", markdown)
        self.assertIn("50.0%", markdown)
        self.assertIn("提交不等于排名", markdown)


if __name__ == "__main__":
    unittest.main()
