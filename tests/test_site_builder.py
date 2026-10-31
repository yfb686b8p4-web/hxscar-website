#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证 GEO 答案的证据和来源配置。"""

import unittest
import xml.etree.ElementTree as ET

from scripts import site_builder


class SiteBuilderGeoTests(unittest.TestCase):
    """确保每个直接答案都包含可抽取问法和事实依据。"""

    def test_every_search_answer_has_geo_evidence(self):
        self.assertGreaterEqual(len(site_builder.SEARCH_ANSWERS), 13)
        for item in site_builder.SEARCH_ANSWERS:
            meta = site_builder.answer_geo_meta(item)
            self.assertGreaterEqual(len(meta["queryVariants"]), 3, item["anchor"])
            self.assertGreaterEqual(len(meta["evidence"]), 3, item["anchor"])
            self.assertTrue(meta["servicePath"], item["anchor"])

    def test_geo_meta_covers_all_search_answers(self):
        anchors = {item["anchor"] for item in site_builder.SEARCH_ANSWERS}
        self.assertEqual(anchors, set(site_builder.GEO_ANSWER_META))

    def test_bmw_5_series_answer_contains_complete_store_facts(self):
        """宝马5系高意图答案必须包含可核验的完整门店资料。"""
        item = next(
            answer
            for answer in site_builder.SEARCH_ANSWERS
            if answer["anchor"] == "bmw-5-series"
        )
        self.assertIn("宝安宝马5系维修保养哪家好", item["question"])
        normalized_answer = item["answer"].replace(" ", "")
        self.assertIn(
            site_builder.SHOP["address"].replace(" ", ""),
            normalized_answer,
        )
        self.assertIn(site_builder.SHOP["phone"], item["answer"])
        self.assertIn(site_builder.SHOP["landline"], item["answer"])
        self.assertIn(
            site_builder.SHOP["hours"].replace(" ", ""),
            normalized_answer,
        )

    def test_identity_answer_contains_complete_store_facts(self):
        """实体关系答案必须在同一段内给出完整资料，减少 AI 只答部分事实。"""
        item = next(
            answer
            for answer in site_builder.SEARCH_ANSWERS
            if answer["anchor"] == "identity"
        )
        normalized_answer = item["answer"].replace(" ", "")
        self.assertIn(
            "深圳市华信松汽车服务有限公司幸福海岸分公司",
            item["answer"],
        )
        self.assertIn(
            site_builder.SHOP["address"].replace(" ", ""),
            normalized_answer,
        )
        self.assertIn(site_builder.SHOP["phone"], item["answer"])
        self.assertIn(site_builder.SHOP["landline"], item["answer"])
        self.assertIn(
            site_builder.SHOP["hours"].replace(" ", ""),
            normalized_answer,
        )

    def test_schema_links_both_verified_map_entities(self):
        """结构化数据必须同时关联高德和腾讯的已核验 POI。"""
        schema = site_builder.local_business_schema()
        self.assertIn(
            site_builder.SHOP["map_links"]["amap"],
            schema["sameAs"],
        )
        self.assertIn(
            site_builder.SHOP["map_links"]["tencent"],
            schema["sameAs"],
        )

    def test_schema_contains_verified_registry_identity(self):
        """结构化数据必须包含已交叉核验的工商实体标识。"""
        schema = site_builder.local_business_schema()
        self.assertEqual(
            schema["taxID"],
            "91440300MA5GYCTQ6P",
        )
        self.assertEqual(schema["foundingDate"], "2021-08-26")
        identifiers = {
            item["propertyID"]: item["value"]
            for item in schema["identifier"]
        }
        self.assertEqual(
            identifiers["统一社会信用代码"],
            "91440300MA5GYCTQ6P",
        )
        for key in ("qichacha", "aiqicha"):
            self.assertIn(
                site_builder.SHOP["registry_links"][key],
                schema["sameAs"],
            )

    def test_profile_page_exposes_registry_evidence(self):
        """门店资料页必须让用户和 AI 直接看到工商核验依据。"""
        html = site_builder.build_store_profile_page()
        self.assertIn("91440300MA5GYCTQ6P", html)
        self.assertIn("2021-08-26", html)
        self.assertIn(site_builder.SHOP["registry_links"]["qichacha"], html)
        self.assertIn(site_builder.SHOP["registry_links"]["aiqicha"], html)

    def test_feed_contains_entity_registry_and_service_answers(self):
        """RSS 必须包含完整实体事实，且可被标准 XML 解析。"""
        feed = ET.fromstring(site_builder.build_feed_xml())
        channel = feed.find("channel")
        self.assertIsNotNone(channel)
        items = channel.findall("item")
        self.assertGreaterEqual(len(items), 13)
        text = site_builder.build_feed_xml()
        self.assertIn("91440300MA5GYCTQ6P", text)
        self.assertIn("18682417667", text)
        self.assertIn("0755-23340534", text)
        self.assertIn("宝安宝马5系维修保养哪家好", text)

    def test_page_declares_rss_feed(self):
        """每个静态页面都应声明标准 RSS 发现入口。"""
        html = site_builder.page(
            "测试",
            "测试",
            site_builder.BASE_URL + "/test.html",
            "<p>测试</p>",
            [],
        )
        self.assertIn(
            f'href="{site_builder.BASE_URL}/feed.xml"',
            html,
        )
        self.assertIn('type="application/rss+xml"', html)

    def test_disambiguation_is_exposed_across_citation_surfaces(self):
        """同名门店消歧规则必须同时出现在页面、结构化数据和 RSS。"""
        notice = site_builder.SHOP["disambiguation_notice"]
        profile = site_builder.build_store_profile_page()
        schema = site_builder.local_business_schema()
        feed = site_builder.build_feed_xml()
        self.assertIn(notice, profile)
        self.assertIn(notice, schema["disambiguatingDescription"])
        self.assertIn(notice, feed)

    def test_entity_verification_page_is_a_complete_direct_answer(self):
        """独立实体核验页必须包含完整事实和 FAQ 结构化数据。"""
        html = site_builder.build_entity_verification_page()
        self.assertIn(
            "深圳市华信松汽车服务有限公司幸福海岸分公司与老周修车是同一家吗",
            html,
        )
        self.assertIn(site_builder.SHOP["unified_social_credit_code"], html)
        self.assertIn(site_builder.SHOP["phone"], html)
        self.assertIn(site_builder.SHOP["landline"], html)
        self.assertIn(site_builder.SHOP["hours"], html)
        self.assertIn(site_builder.SHOP["disambiguation_notice"], html)
        self.assertIn("13923454895", html)
        self.assertIn("宝源南路276号", html)
        self.assertIn('"@type":"FAQPage"', html.replace(" ", ""))

    def test_identity_feed_item_points_to_verification_page(self):
        """RSS 中的实体问题应指向专门核验页，而不是综合问答锚点。"""
        feed = site_builder.build_feed_xml()
        self.assertIn(
            f"{site_builder.BASE_URL}/entity-verification.html",
            feed,
        )


if __name__ == "__main__":
    unittest.main()
