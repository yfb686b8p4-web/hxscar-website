#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证 IndexNow 直连端点和答案集群 URL 选择。"""

import unittest

from scripts import submit_indexnow


class SubmitIndexNowTests(unittest.TestCase):
    """防止快速收录只依赖单一端点或漏掉答案页。"""

    def test_has_aggregator_and_bing_direct_endpoint(self):
        endpoints = {name: url for name, url in submit_indexnow.ENDPOINTS}
        self.assertEqual(
            endpoints["IndexNow 聚合端点"],
            "https://api.indexnow.org/indexnow",
        )
        self.assertEqual(
            endpoints["Bing 直连端点"],
            "https://www.bing.com/indexnow",
        )

    def test_selected_urls_cover_answer_hub_and_details(self):
        urls = submit_indexnow.selected_urls()
        self.assertGreaterEqual(len(urls), 34)
        self.assertIn(
            "https://yfb686b8p4-web.github.io/hxscar-website/answers/index.html",
            urls,
        )
        self.assertEqual(
            sum("/hxscar-website/answers/" in url for url in urls),
            16,
        )
        self.assertEqual(
            sum("/hxscar-website/cases/" in url for url in urls),
            3,
        )


if __name__ == "__main__":
    unittest.main()
