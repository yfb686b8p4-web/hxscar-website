#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证 GEO 答案的证据和来源配置。"""

import json
import re
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

    def test_every_answer_has_directly_citable_sources(self):
        """每条标准答案必须给出至少四个可直接核验的 HTTPS 来源。"""
        for item in site_builder.SEARCH_ANSWERS:
            sources = site_builder.answer_evidence_sources(item)
            self.assertGreaterEqual(len(sources), 4, item["anchor"])
            urls = {source["url"] for source in sources}
            self.assertTrue(
                all(url.startswith("https://") for url in urls),
                item["anchor"],
            )
            self.assertIn(
                site_builder.BASE_URL + "/entity-verification.html",
                urls,
            )
            self.assertIn(
                site_builder.BASE_URL + "/store-facts.json",
                urls,
            )

    def test_service_answer_sources_include_real_cases(self):
        """服务答案必须能回链到对应真实案例，而不是只有自述证据。"""
        for item in site_builder.SEARCH_ANSWERS:
            if item["category"] not in {
                "宝马与豪车",
                "空调诊断维修",
                "底盘异响",
            }:
                continue
            urls = {
                source["url"]
                for source in site_builder.answer_evidence_sources(item)
            }
            self.assertTrue(
                any("/cases.html#case-" in url for url in urls),
                item["anchor"],
            )

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

    def test_schema_declares_core_service_offers(self):
        """门店结构化数据必须声明四项核心维修服务。"""
        schema = site_builder.local_business_schema()
        offered = {
            item["itemOffered"]["name"]
            for item in schema["makesOffer"]
        }
        self.assertEqual(
            offered,
            set(site_builder.SHOP["core_tags"]),
        )
        for item in schema["makesOffer"]:
            self.assertTrue(item["itemOffered"]["url"].startswith(site_builder.BASE_URL))

    def test_schema_and_page_use_local_brand_image(self):
        """门店结构化数据和页面必须使用本地托管的真实品牌图片。"""
        schema = site_builder.local_business_schema()
        image_url = site_builder.BUSINESS_IMAGE
        self.assertEqual(schema["image"], image_url)
        self.assertEqual(schema["logo"], site_builder.BUSINESS_LOGO)
        image_path = (
            site_builder.ROOT
            / site_builder.SHOP["image_path"]
        )
        self.assertTrue(image_path.is_file())
        self.assertGreater(image_path.stat().st_size, 1000)
        logo_path = (
            site_builder.ROOT
            / site_builder.SHOP["logo_path"]
        )
        self.assertTrue(logo_path.is_file())
        self.assertGreater(logo_path.stat().st_size, 1000)
        page_html = site_builder.build_entity_verification_page()
        self.assertIn('class="brand-logo"', page_html)
        self.assertIn('class="storefront-image"', page_html)
        self.assertIn(site_builder.SHOP["image_path"], page_html)
        self.assertIn(site_builder.SHOP["logo_path"], page_html)

    def test_schema_links_both_fact_sheet_mirrors(self):
        """门店结构化数据必须关联官网 PDF 和 GitHub Release 镜像。"""
        schema = site_builder.local_business_schema()
        mirror_urls = {item["url"] for item in schema["subjectOf"]}
        self.assertIn(site_builder.BUSINESS_FACT_SHEET, mirror_urls)
        self.assertIn(
            site_builder.SHOP["document_mirrors"]["github_release_pdf"],
            mirror_urls,
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
        for link in site_builder.SHOP["external_profile_links"].values():
            self.assertIn(link, schema["sameAs"])

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

    def test_llms_corpora_link_fact_sheet_mirrors(self):
        """面向 AI 的两个机器语料入口都应暴露实体核验 PDF 双镜像。"""
        mirror = site_builder.SHOP["document_mirrors"]["github_release_pdf"]
        for text in (
            site_builder.build_llms_txt(),
            site_builder.build_llms_full_txt(),
        ):
            self.assertIn(site_builder.BUSINESS_FACT_SHEET, text)
            self.assertIn(mirror, text)

    def test_answer_sources_are_exposed_in_machine_surfaces(self):
        """机器事实、RSS 与完整语料都必须携带逐答案证据来源。"""
        facts = json.loads(site_builder.build_store_facts_json())
        self.assertTrue(
            all(item.get("evidenceSources") for item in facts["answers"])
        )
        feed = site_builder.build_feed_xml()
        llms_full = site_builder.build_llms_full_txt()
        self.assertIn("证据来源：", feed)
        self.assertIn("证据来源：", llms_full)
        self.assertIn("/cases.html#case-", llms_full)

    def test_search_answer_faq_schema_contains_citations(self):
        """搜索问答的结构化答案必须直接携带可引用来源。"""
        html = site_builder.build_answers_page()
        schemas = [
            json.loads(raw)
            for raw in re.findall(
                r'<script type="application/ld\+json">(.*?)</script>',
                html,
                re.S,
            )
        ]
        faq_page = next(
            schema
            for schema in schemas
            if schema.get("@type") == "FAQPage"
        )
        for question in faq_page["mainEntity"]:
            answer = question["acceptedAnswer"]
            self.assertGreaterEqual(len(answer.get("citation", [])), 4)
            self.assertTrue(
                all(url.startswith("https://") for url in answer["citation"])
            )

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
        self.assertIn(
            site_builder.SHOP["external_profile_links"]["gist"],
            html,
        )
        self.assertIn(
            site_builder.SHOP["external_profile_links"]["douyin"],
            html,
        )
        self.assertIn(site_builder.SHOP["douyin_id"], html)
        self.assertIn(site_builder.SHOP["fact_sheet_path"], html)
        self.assertIn(
            site_builder.SHOP["document_mirrors"]["github_release_pdf"],
            html,
        )
        self.assertIn('"@type":"FAQPage"', html.replace(" ", ""))

    def test_store_facts_exposes_release_pdf_mirror(self):
        """机器事实必须公开独立下载镜像，供搜索与 AI 交叉核验。"""
        facts = json.loads(site_builder.build_store_facts_json())
        mirror = site_builder.SHOP["document_mirrors"]["github_release_pdf"]
        self.assertEqual(
            facts["documentMirrors"]["github_release_pdf"],
            mirror,
        )
        self.assertIn(
            mirror,
            {item["url"] for item in facts["citationTargets"]},
        )
        self.assertIn(
            site_builder.SHOP["fact_sheet_path"],
            site_builder.build_entity_verification_page(),
        )

    def test_identity_feed_item_points_to_verification_page(self):
        """RSS 中的实体问题应指向专门核验页，而不是综合问答锚点。"""
        feed = site_builder.build_feed_xml()
        self.assertIn(
            f"{site_builder.BASE_URL}/entity-verification.html",
            feed,
        )


if __name__ == "__main__":
    unittest.main()
