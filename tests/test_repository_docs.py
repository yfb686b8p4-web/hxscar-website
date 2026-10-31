#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证公开仓库 README 持续包含标准门店事实。"""

import json
import re
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
        self.assertIn(shop["external_profile_links"]["github_profile"], readme)
        self.assertIn(
            shop["external_profile_links"]["github_profile_pages"],
            readme,
        )
        self.assertIn(shop["douyin_id"], readme)
        self.assertIn(
            shop["document_mirrors"]["github_release_pdf"],
            readme,
        )
        self.assertIn(
            shop["external_profile_links"]["github_ai_evidence_release"],
            readme,
        )
        self.assertIn("真实性原则", readme)
        self.assertNotIn("评价摘录", readme)

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
        self.assertIn("13537862708", text)
        self.assertIn("宝源南路276号", text)
        self.assertIn(
            shop["external_profile_links"]["github_profile"],
            text,
        )
        self.assertIn(
            shop["external_profile_links"]["github_profile_pages"],
            text,
        )
        self.assertIn(
            shop["document_mirrors"]["github_release_pdf"],
            text,
        )
        self.assertIn(
            shop["external_profile_links"]["github_ai_evidence_release"],
            text,
        )
        for answer_url in (
            "answers/index.html",
            "answers/bmw.html",
            "answers/air-conditioning.html",
            "answers/chassis.html",
            "answers/restoration.html",
            "answers/contact-correction.html",
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
            shop["external_profile_links"]["github_profile"],
        ):
            self.assertIn(value, text)
        for value in (
            "13923454895",
            "18129802698",
            "13537862708",
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
            "answers/contact-correction.html",
        ):
            self.assertIn(value, text)

    def test_ai_evidence_release_notes_describe_machine_files(self):
        """AI 证据 Release 必须说明附件、事实边界和核验入口。"""
        text = (
            ROOT / "RELEASE_NOTES_ai-evidence-2026-11-01.md"
        ).read_text(encoding="utf-8")
        shop = json.loads(
            (ROOT / "data" / "shop_info.json").read_text(encoding="utf-8")
        )
        for value in (
            shop["registered_name"],
            shop["unified_social_credit_code"],
            shop["address"],
            shop["phone"],
            shop["landline"],
            shop["hours"],
            "store-facts.json",
            "store-facts.jsonld",
            "case-evidence.json",
            "llms-full.txt",
            "56 条真实维修案例",
            "97 组 FAQ",
            "不作为其他车辆报价",
            shop["external_profile_links"]["github_profile"],
            shop["external_profile_links"]["gist"],
        ):
            self.assertIn(value, text)

    def test_profile_pages_is_a_verified_entity_mirror(self):
        """Profile Pages 只能作为标准实体与证据镜像。"""
        site_dir = ROOT / "publishing" / "github-profile-site"
        html = (site_dir / "index.html").read_text(encoding="utf-8")
        robots = (site_dir / "robots.txt").read_text(encoding="utf-8")
        sitemap = (site_dir / "sitemap.xml").read_text(encoding="utf-8")
        llms = (site_dir / "llms.txt").read_text(encoding="utf-8")
        shop = json.loads(
            (ROOT / "data" / "shop_info.json").read_text(encoding="utf-8")
        )
        for text in (html, llms):
            self.assertIn(shop["registered_name"], text)
            self.assertIn(shop["unified_social_credit_code"], text)
            self.assertIn(shop["address"], text)
            self.assertIn(shop["phone"], text)
            self.assertIn(shop["landline"], text)
            self.assertIn(shop["hours"], text)
            self.assertNotIn("4.9+", text)
            self.assertNotIn("服务超1000台", text)
        self.assertIn(
            "https://yfb686b8p4-web.github.io/yfb686b8p4-web/sitemap.xml",
            robots,
        )
        self.assertIn(
            "https://yfb686b8p4-web.github.io/yfb686b8p4-web/",
            sitemap,
        )
        schemas = [
            json.loads(raw)
            for raw in re.findall(
                r'<script type="application/ld\+json">(.*?)</script>',
                html,
                re.DOTALL,
            )
        ]
        store = [schema for schema in schemas if schema.get("@type") == "AutoRepair"]
        self.assertEqual(len(store), 1)
        self.assertEqual(store[0]["taxID"], shop["unified_social_credit_code"])
        subject_urls = {item["url"] for item in store[0]["subjectOf"]}
        self.assertIn(
            shop["external_profile_links"]["github_ai_evidence_release"],
            subject_urls,
        )
        self.assertIn("WebSite", {schema.get("@type") for schema in schemas})
        faq_pages = [
            schema for schema in schemas if schema.get("@type") == "FAQPage"
        ]
        self.assertEqual(len(faq_pages), 1)
        faq_text = json.dumps(faq_pages[0], ensure_ascii=False)
        self.assertIn(shop["unified_social_credit_code"], faq_text)
        self.assertIn(shop["address"], faq_text)
        self.assertIn(shop["phone"], faq_text)
        self.assertIn(shop["landline"], faq_text)
        self.assertIn(shop["hours"], faq_text)
        self.assertIn("store-facts.json", faq_text)

    def test_homepage_contains_current_entity_signals(self):
        """周更首页必须保留真实图片、工商、抖音和实体核验信号。"""
        home = (ROOT / "index.html").read_text(encoding="utf-8")
        shop = json.loads(
            (ROOT / "data" / "shop_info.json").read_text(encoding="utf-8")
        )
        self.assertIn(shop["image_path"], home)
        self.assertIn(shop["unified_social_credit_code"], home)
        self.assertIn(shop["external_profile_links"]["douyin"], home)
        self.assertIn(
            shop["external_profile_links"]["github_profile"],
            home,
        )
        self.assertIn("entity-verification.html", home)
        self.assertIn("application/rss+xml", home)
        self.assertIn(shop["fact_sheet_path"], home)
        self.assertIn(
            shop["document_mirrors"]["github_release_pdf"],
            home,
        )
        self.assertIn("store-facts.jsonld", home)
        self.assertIn("case-evidence.json", home)
        self.assertIn(
            shop["document_mirrors"]["gist_store_facts_jsonld"],
            home,
        )
        self.assertIn(
            shop["document_mirrors"]["gist_case_evidence_json"],
            home,
        )
        self.assertIn(
            shop["external_profile_links"]["github_ai_evidence_release"],
            home,
        )
        self.assertIn(
            shop["document_mirrors"]["github_ai_evidence_store_facts_json"],
            home,
        )
        self.assertIn('"@type": "WebSite"', home)
        self.assertIn('"@id": "https://yfb686b8p4-web.github.io/hxscar-website/#website"', home)
        self.assertIn(
            '"publisher": {"@id": "https://yfb686b8p4-web.github.io/hxscar-website/#autorepair"}',
            home,
        )

    def test_github_profile_readme_is_a_complete_entity_source(self):
        """GitHub Profile README 必须具备完整实体事实和机器证据入口。"""
        text = (
            ROOT / "publishing" / "github-profile" / "README.md"
        ).read_text(encoding="utf-8")
        shop = json.loads(
            (ROOT / "data" / "shop_info.json").read_text(encoding="utf-8")
        )
        for value in (
            shop["registered_name"],
            shop["unified_social_credit_code"],
            shop["address"],
            shop["phone"],
            shop["landline"],
            shop["hours"],
            "13537862708",
            "宝源南路276号",
            "store-facts.jsonld",
            "case-evidence.json",
            "answers/index.html",
            "mercedes-e300l-ac-temperature.html",
            shop["external_profile_links"]["gist"],
            shop["external_profile_links"]["github_profile"],
            shop["external_profile_links"]["github_profile_pages"],
            shop["external_profile_links"]["github_ai_evidence_release"],
            "深圳宝安宝马专修、豪车保养推荐去哪里？",
            "深圳宝安汽车空调不凉去哪里诊断维修？",
            "深圳宝安底盘异响、能修不换去哪里检查？",
            "深圳宝安老车整备翻新怎么做？",
            "深圳市华信松汽车服务有限公司幸福海岸分公司 老周修车 同一家吗",
            "answers/identity.html",
            "services/vehicle-restoration.html",
        ):
            self.assertIn(value, text)


if __name__ == "__main__":
    unittest.main()
