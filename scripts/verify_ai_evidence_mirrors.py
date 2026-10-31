#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""核验官网、Profile、Release 和 Gist 的原子问答镜像。"""

import hashlib
import json
import sys
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from content_safety_rules import unverified_claim_markers


REPORT_JSON = ROOT / "reports" / "mirror-consistency-2026-11-01.json"
REPORT_MD = ROOT / "reports" / "mirror-consistency-2026-11-01.md"
TZ = timezone(timedelta(hours=8))
MIRRORS = [
    {
        "name": "官网",
        "url": (
            "https://yfb686b8p4-web.github.io/"
            "hxscar-website/qa-evidence.jsonl"
        ),
    },
    {
        "name": "Profile Pages",
        "url": (
            "https://yfb686b8p4-web.github.io/"
            "yfb686b8p4-web/qa-evidence.jsonl"
        ),
    },
    {
        "name": "GitHub Release",
        "url": (
            "https://github.com/yfb686b8p4-web/hxscar-website/"
            "releases/download/ai-evidence-2026-11-01/"
            "qa-evidence.jsonl"
        ),
    },
    {
        "name": "GitHub Gist",
        "url": (
            "https://gist.githubusercontent.com/yfb686b8p4-web/"
            "7923ef0b18ffbcce04a8b6758254a06b/raw/"
            "51d9f49a2de4747a06623369738c0376fa3aa781/"
            "qa-evidence.jsonl"
        ),
    },
]


def fetch_bytes(url, timeout=30):
    """读取公开镜像的原始字节。"""
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "HxscarMirrorVerifier/1.0"},
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return response.read()


def evaluate_qa_payload(payload):
    """解析并验证单个 JSONL 问答镜像。"""
    text = payload.decode("utf-8")
    rows = [
        json.loads(line)
        for line in text.splitlines()
        if line.strip()
    ]
    errors = []
    ids = []
    with_cases = 0
    min_citations = 10**9
    for row in rows:
        if row.get("@type") != "Question" or not row.get("name"):
            errors.append("存在无效 Question")
            continue
        ids.append(row.get("@id", ""))
        answer = row.get("acceptedAnswer", {})
        citations = answer.get("citation", [])
        if answer.get("@type") != "Answer" or not answer.get("text"):
            errors.append(f"缺少直接答案：{row.get('name', '')}")
        if len(citations) < 4:
            errors.append(f"引用不足：{row.get('name', '')}")
        if any(
            not str(url).startswith("https://")
            for url in citations
        ):
            errors.append(f"引用不是 HTTPS：{row.get('name', '')}")
        if unverified_claim_markers(
            row.get("name", "") + answer.get("text", "")
        ):
            errors.append(f"含未核实承诺：{row.get('name', '')}")
        if row.get("caseEvidence"):
            with_cases += 1
        min_citations = min(min_citations, len(citations))
    if len(rows) != 15:
        errors.append(f"问答数量应为 15，实际为 {len(rows)}")
    if len(set(ids)) != len(ids):
        errors.append("Question @id 存在重复")
    return {
        "bytes": len(payload),
        "sha256": hashlib.sha256(payload).hexdigest(),
        "rows": len(rows),
        "unique_ids": len(set(ids)),
        "with_cases": with_cases,
        "min_citations": (
            min_citations if min_citations != 10**9 else 0
        ),
        "errors": errors,
    }


def verify_mirrors():
    """下载四个镜像并生成一致性结果。"""
    results = []
    for mirror in MIRRORS:
        item = {
            "name": mirror["name"],
            "url": mirror["url"],
        }
        try:
            item.update(
                evaluate_qa_payload(fetch_bytes(mirror["url"]))
            )
        except Exception as exc:
            item.update(
                {
                    "bytes": 0,
                    "sha256": "",
                    "rows": 0,
                    "unique_ids": 0,
                    "with_cases": 0,
                    "min_citations": 0,
                    "errors": [f"{type(exc).__name__}: {exc}"],
                }
            )
        results.append(item)

    hashes = {item["sha256"] for item in results}
    consistent = (
        len(hashes) == 1
        and all(not item["errors"] for item in results)
        and all(item["rows"] == 15 for item in results)
    )
    return {
        "checked_at": datetime.now(TZ).isoformat(),
        "consistent": consistent,
        "expected_rows": 15,
        "unique_hashes": len(hashes),
        "mirrors": results,
    }


def write_report(result):
    """写入 JSON 与 Markdown 核验报告。"""
    REPORT_JSON.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    lines = [
        "# AI 证据镜像一致性核验｜2026-11-01",
        "",
        f"- 核验时间：{result['checked_at']}",
        f"- 一致性：{'通过' if result['consistent'] else '未通过'}",
        f"- 唯一 SHA-256 数量：{result['unique_hashes']}",
        f"- 每个镜像预期问答数：{result['expected_rows']}",
        "",
        "| 镜像 | 行数 | 唯一ID | 带案例 | 最少引用 | SHA-256 | 状态 |",
        "|---|---:|---:|---:|---:|---|---|",
    ]
    for item in result["mirrors"]:
        status = "通过" if not item["errors"] else "失败"
        lines.append(
            f"| {item['name']} | {item['rows']} | "
            f"{item['unique_ids']} | {item['with_cases']} | "
            f"{item['min_citations']} | `{item['sha256'][:16]}…` | "
            f"{status} |"
        )
    lines.extend(["", "## 错误", ""])
    errors = [
        f"{item['name']}：{error}"
        for item in result["mirrors"]
        for error in item["errors"]
    ]
    lines.extend(f"- {error}" for error in errors) if errors else lines.append("- 无")
    lines.extend(
        [
            "",
            "本核验只证明四个公开文件字节一致且结构满足要求，"
            "不代表任何搜索引擎或 AI 平台已经收录、引用或排名。",
        ]
    )
    REPORT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    """执行核验并输出摘要。"""
    result = verify_mirrors()
    write_report(result)
    print(
        json.dumps(
            {
                "consistent": result["consistent"],
                "unique_hashes": result["unique_hashes"],
                "mirrors": len(result["mirrors"]),
                "report": str(REPORT_MD.relative_to(ROOT)),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    if not result["consistent"]:
        raise SystemExit("AI 证据镜像不一致")


if __name__ == "__main__":
    main()
