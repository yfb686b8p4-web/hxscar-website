#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证站外发布内容不会生成虚构评价或未经核验的承诺。"""

import random
import unittest

import multi_platform_publisher as publisher
from data_loader import ADDRESS, PHONE
from scripts import authority_queue


class ContentSafetyTests(unittest.TestCase):
    """把未核验营销话术挡在发布队列之前。"""

    def test_platform_drafts_use_real_facts_without_unverified_claims(self):
        random.seed(44 * 7919)
        generators = (
            publisher.generate_dianping,
            publisher.generate_xiaohongshu,
            publisher.generate_douyin,
            publisher.generate_58,
            publisher.generate_meituan,
            publisher.generate_map,
        )
        banned = (
            "4.9+",
            "服务超1000台",
            "⭐⭐⭐⭐⭐",
            "评分：",
            "推荐评价文案",
            "团队10年以上",
            "免费检测",
            "质保无忧",
            "当天可取",
            "省一半",
            "原价：¥",
            "团购价：",
        )
        for generator in generators:
            content = generator(44)
            self.assertIn(ADDRESS, content, generator.__name__)
            self.assertIn(PHONE, content, generator.__name__)
            for marker in banned:
                self.assertNotIn(marker, content, generator.__name__)

    def test_publish_queue_blocks_unverified_claims(self):
        matches = authority_queue.unverified_claim_matches(
            "推荐评价文案：评分：⭐⭐⭐⭐⭐，4.9+，服务超1000台。"
        )
        self.assertEqual(
            set(matches),
            {"推荐评价文案", "评分：", "⭐⭐⭐⭐⭐", "4.9+", "服务超1000台"},
        )
        self.assertEqual(authority_queue.unverified_claim_matches("真实案例"), [])


if __name__ == "__main__":
    unittest.main()
