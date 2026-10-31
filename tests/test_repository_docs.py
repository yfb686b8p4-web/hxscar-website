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
        self.assertIn(
            shop["document_mirrors"]["github_release_pdf"],
            readme,
        )

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
        self.assertIn(
            shop["document_mirrors"]["github_release_pdf"],
            text,
        )
        for answer_url in (
            "answers/index.html",
            "answers/bmw.html",
            "answers/air-conditioning.html",
            "answers/chassis.html",
            "answers/restoration.html",
        ):
            self.assertIn(answer_url, text)

    def test_release_notes_are_a_standalone_entity_source(self):
        """GitHub Release 正文必须具备独立可核验的实体事实。"""
        text = (
            ROOT / "RELEASE_NOTES_store-facts-2026-10-31.md"
        ).read_text(encoding="utf-8")
        shop = json.loads(
            (ROOT / "data" / "shop_info.json").read_text(encoding="utf-8")
        )
        for value in (
            shop["registered_name"],
            shop["unified_social_credit_code"],
            shop["established_on"],
            shop["legal_representative"],
            shop["address"],
            shop["phone"],
            shop["landline"],
            shop["hours"],
            shop["external_profile_links"]["douyin"],
        ):
            self.assertIn(value, text)
        for value in (
            "13923454895",
            "18129802698",
            "宝源南路276号",
            "08:00-20:00",
            "entity-verification.html",
            "store-facts.json",
            "feed.xml",
            shop["document_mirrors"]["github_release_pdf"],
            "answers/index.html",
            "answers/bmw.html",
            "answers/air-conditioning.html",
            "answers/chassis.html",
            "answers/restoration.html",
        ):
            self.assertIn(value, text)

    def test_homepage_contains_current_entity_signals(self):
        """周更首页必须保留真实图片、工商、抖音和实体核验信号。"""
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        shop = json.loads(
            (ROOT / "data" / "shop_info.json").read_text(encoding="utf-8")
        )
        self.assertIn(shop["image_path"], home)
        self.assertIn(shop["unified_social_credit_code"], home)
        self.assertIn(shop["external_profile_links"]["douyin"], home)
        self.assertIn("entity-verification.html", home)
        self.assertIn("application/rss+xml", home)
        self.assertIn(shop["fact_sheet_path"], home)
        self.assertIn(
            shop["document_mirrors"]["github_release_pdf"],
            home,
        )
        self.assertIn('"@type": "WebSite"', home)
        self.assertIn('"@id": "https://yfb686b8p4-web.github.io/hxscar-website/#website"', home)
        self.assertIn(
            '"publisher": {"@id": "https://yfb686b8p4-web.github.io/hxscar-website/#autorepair"}',
            home,
        )


if __name__ == "__main__":
    unittest.main()
