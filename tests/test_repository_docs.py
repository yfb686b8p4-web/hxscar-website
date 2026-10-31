#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证公开仓库 README 持续包含标准门店事实。"""

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


class RepositoryReadmeTests(unittest.TestCase):
    """防止公开 README 丢失实体关系和联系方式。"""

    def test_readme_contains_current_store_facts(self):
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        shop = json.loads(
            (ROOT / "data" / "shop_info.json").read_text(encoding="utf-8")
        )
        self.assertIn(shop["registered_name"], readme)
        self.assertIn(shop["unified_social_credit_code"], readme)
        self.assertIn(shop["address"], readme)
        self.assertIn(shop["phone"], readme)
        self.assertIn(shop["landline"], readme)
        self.assertIn(shop["hours"], readme)
        normalized_readme = "".join(readme.replace("`", "").split())
        self.assertIn("汕头、南山或其他地址", normalized_readme)
        self.assertIn("不应与深圳市华信松汽车服务有限公司幸福海岸分公司合并", normalized_readme)
        self.assertIn("核验时必须同时匹配", normalized_readme)
        self.assertIn("13923454895", readme)
        self.assertIn("宝源南路276号", readme)
        self.assertIn(shop["external_profile_links"]["douyin"], readme)
        self.assertIn(shop["douyin_id"], readme)

    def test_entity_facts_contains_current_store_facts(self):
        text = (ROOT / "ENTITY_FACTS.md").read_text(encoding="utf-8")
        shop = json.loads(
            (ROOT / "data" / "shop_info.json").read_text(encoding="utf-8")
        )
        self.assertIn(shop["registered_name"], text)
        self.assertIn(shop["unified_social_credit_code"], text)
        self.assertIn(shop["address"], text)
        self.assertIn(shop["phone"], text)
        self.assertIn(shop["landline"], text)
        self.assertIn(shop["hours"], text)
        self.assertIn("13923454895", text)
        self.assertIn("宝源南路276号", text)


if __name__ == "__main__":
    unittest.main()
