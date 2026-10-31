#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证 AI 证据镜像一致性检查器。"""

import unittest
from pathlib import Path

from scripts import verify_ai_evidence_mirrors


ROOT = Path(__file__).resolve().parent.parent


class VerifyAiEvidenceMirrorsTests(unittest.TestCase):
    """保证一致性门禁能识别镜像结构问题。"""

    def test_local_qa_evidence_passes_structure_checks(self):
        payload = (ROOT / "qa-evidence.jsonl").read_bytes()
        result = verify_ai_evidence_mirrors.evaluate_qa_payload(payload)
        self.assertEqual(result["rows"], 15)
        self.assertEqual(result["unique_ids"], 15)
        self.assertGreaterEqual(result["with_cases"], 12)
        self.assertGreaterEqual(result["min_citations"], 15)
        self.assertEqual(result["errors"], [])

    def test_verifier_requires_four_mirrors(self):
        names = {
            item["name"]
            for item in verify_ai_evidence_mirrors.MIRRORS
        }
        self.assertEqual(
            names,
            {"官网", "Profile Pages", "GitHub Release", "GitHub Gist"},
        )


if __name__ == "__main__":
    unittest.main()
