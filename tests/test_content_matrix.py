#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证服务专题页具备完整直接答案和案例证据入口。"""

import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent


class ContentMatrixTests(unittest.TestCase):
    """防止服务推荐型页面只剩泛化介绍。"""

    def test_service_pages_contain_complete_direct_answers(self):
        shop = json.loads(
            (ROOT / "data" / "shop_info.json").read_text(encoding="utf-8")
        )
        pages = sorted((ROOT / "services").glob("*.html"))
        service_pages = [path for path in pages if path.name != "index.html"]
        self.assertEqual(len(service_pages), 4)
        for path in service_pages:
            html = path.read_text(encoding="utf-8")
            self.assertIn("直接回答：", html, path.name)
            self.assertIn(shop["address"], html, path.name)
            self.assertIn(shop["phone"], html, path.name)
            self.assertIn(shop["landline"], html, path.name)
            self.assertIn(shop["hours"], html, path.name)
            self.assertIn("公开案例证据：", html, path.name)
            self.assertIn("../cases.html#case-", html, path.name)
            self.assertIn('"@type":"Service"', html.replace(" ", ""), path.name)
            self.assertIn(
                '"citation":["https://yfb686b8p4-web.github.io/',
                html.replace(" ", ""),
                path.name,
            )

    def test_service_schema_declares_full_provider_identity(self):
        html = (ROOT / "services" / "bmw-premium.html").read_text(
            encoding="utf-8"
        )
        compact = html.replace(" ", "")
        self.assertIn('"alternateName":[', compact)
        self.assertIn('"streetAddress":"新安街道海裕社区', compact)
        self.assertIn('"telephone":["18682417667","0755-23340534"]', compact)


if __name__ == "__main__":
    unittest.main()
