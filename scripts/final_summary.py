#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""汇总 AI 搜索排名冲刺的实施、指标、阻塞和下一步。"""

import json
import subprocess
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"
DAILY_DIR = REPORTS / "daily"
DATE = "2026-11-01"
TZ = timezone(timedelta(hours=8))
JSON_PATH = REPORTS / f"final-summary-{DATE}.json"
MARKDOWN_PATH = REPORTS / f"final-summary-{DATE}.md"


def load_json(path):
    """读取 JSON 文件。"""
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def recent_commits(limit=40):
    """读取冲刺期间的中文提交记录。"""
    result = subprocess.run(
        [
            "git",
            "log",
            "--since=2026-10-31T18:00:00+08:00",
            "--reverse",
            f"--max-count={limit}",
            "--pretty=format:%h %s",
        ],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    return [
        line
        for line in result.stdout.splitlines()
        if line.strip()
    ]


def build_summary():
    """从最新日报、审计和平台状态构建交付汇总。"""
    daily = load_json(DAILY_DIR / "latest.json")
    audit = load_json(REPORTS / "site-audit.json")
    publishing = load_json(ROOT / "publishing" / "status.json")
    tasks = load_json(DAILY_DIR / "latest-tasks.json")
    metrics = daily.get("metrics", {})
    status = daily.get("status", {})
    records = daily.get("records", [])
    wrong_items = [
        {
            "platform": item.get("platform", ""),
            "query": item.get("query", ""),
            "category": item.get("category", ""),
            "notes": item.get("notes", ""),
        }
        for item in records
        if item.get("status") == "completed"
        and (
            item.get("identity_relation") == "wrong"
            or item.get("sentiment") in {"负面", "negative"}
            or "错误" in item.get("notes", "")
        )
    ]
    platform_blocks = [
        {
            "name": name,
            "status": item.get("status", ""),
            "notes": item.get("notes", ""),
        }
        for name, item in publishing.get("platforms", {}).items()
        if item.get("status") in {"blocked", "review", "pending"}
    ]
    manual_actions = [
        {
            "priority": item.get("priority", ""),
            "category": item.get("category", ""),
            "action": item.get("action", ""),
            "platforms": item.get("platforms", []),
        }
        for item in tasks
        if item.get("requires_confirmation")
    ]
    summary = {
        "generated_at": datetime.now(TZ).isoformat(),
        "objective_end": "2026-11-01T10:00:00+08:00",
        "daily_date": daily.get("date", ""),
        "metrics": metrics,
        "guardrail_metrics": daily.get("guardrail_metrics", {}),
        "rotating_metrics": daily.get("rotating_metrics", {}),
        "changes": daily.get("changes", {}),
        "wrong_items": wrong_items,
        "technical": {
            "site_audit_passed": audit.get("passed", False),
            "site_audit_counts": audit.get("data_counts", {}),
            "online_checks_passed": status.get("site", {}).get(
                "http_passed", 0
            ),
            "online_checks_total": status.get("site", {}).get(
                "http_total", 0
            ),
            "source_repo": status.get("source_repo", ""),
            "deploy_repo": status.get("deploy_repo", ""),
        },
        "platform_blocks": platform_blocks,
        "manual_actions": manual_actions,
        "commits": recent_commits(),
        "index_status_file": (
            f"reports/index-status-{DATE}.md"
        ),
        "ranking_note": "IndexNow 提交和页面更新不等同于已被收录或获得排名。",
    }
    JSON_PATH.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return summary


def render_markdown(summary):
    """把汇总渲染为米哥可直接检查的中文报告。"""
    metrics = summary["metrics"]
    technical = summary["technical"]
    changes = summary.get("changes", {})
    lines = [
        "# AI 搜索排名冲刺最终汇总｜2026-11-01",
        "",
        f"- 生成时间：{summary['generated_at']}",
        f"- 目标截止：{summary['objective_end']}",
        f"- 指标日期：{summary['daily_date']}",
        "",
        "## 核心指标",
        "",
        f"- 完成检查：{metrics.get('completed', 0)}/{metrics.get('total', 0)}",
        f"- 有效命中率：{metrics.get('effective_hit_rate', 0.0)}%",
        f"- AI 答案引用来源率：{metrics.get('citation_rate', 0.0)}%",
        f"- 门店实体关系正确率：{metrics.get('entity_correct_rate', 0.0)}%",
        f"- 完整地址、电话、营业时间正确率：{metrics.get('full_info_correct_rate', 0.0)}%",
        f"- 服务推荐命中率：{metrics.get('service_hit_rate', 0.0)}%",
        f"- 服务推荐 Top1：{metrics.get('service_top1_rate', 0.0)}%",
        f"- 服务推荐 Top3：{metrics.get('service_top3_rate', 0.0)}%",
        "",
        "## 指标变化",
        "",
    ]
    if changes.get("baseline_date"):
        lines.append(f"- 对比基线：{changes['baseline_date']}")
        lines.append(
            f"- 新命中：{len(changes.get('new_hits', []))}；"
            f"修复：{len(changes.get('fixed', []))}；"
            f"回退：{len(changes.get('regressions', []))}"
        )
    else:
        lines.append("- 暂无已完成的上一日同口径基线。")
    lines.extend(["", "## 技术验证", ""])
    lines.extend(
        [
            f"- 站点审计：{'通过' if technical['site_audit_passed'] else '未通过'}",
            f"- 审计内容：{json.dumps(technical['site_audit_counts'], ensure_ascii=False)}",
            f"- 线上核心检查：{technical['online_checks_passed']}/{technical['online_checks_total']}",
            f"- 源仓库：{technical['source_repo']}",
            f"- 部署副本：{technical['deploy_repo']}",
        ]
    )
    lines.extend(["", "## 仍然错误项", ""])
    if summary["wrong_items"]:
        for item in summary["wrong_items"]:
            lines.append(
                f"- {item['platform']}｜{item['query']}：{item['notes']}"
            )
    else:
        lines.append("- 最新日报中没有已完成且标记为错误的结果。")
    lines.extend(["", "## 平台阻塞", ""])
    if summary["platform_blocks"]:
        for item in summary["platform_blocks"]:
            lines.append(
                f"- {item['name']}（{item['status']}）：{item['notes']}"
            )
    else:
        lines.append("- 无平台阻塞记录。")
    lines.extend(["", "## 已执行优化", ""])
    if summary["commits"]:
        lines.extend(f"- `{commit}`" for commit in summary["commits"])
    else:
        lines.append("- 未读取到冲刺期间提交。")
    lines.extend(["", "## 下一步人工动作", ""])
    if summary["manual_actions"]:
        for item in summary["manual_actions"]:
            platforms = "、".join(item["platforms"])
            lines.append(
                f"- {item['priority']}｜{platforms}｜{item['action']}"
            )
    else:
        lines.append("- 无待人工确认动作。")
    lines.extend(
        [
            "",
            "## 索引与排名口径",
            "",
            f"- 索引状态证据：`{summary['index_status_file']}`",
            f"- {summary['ranking_note']}",
            "",
        ]
    )
    MARKDOWN_PATH.write_text("\n".join(lines), encoding="utf-8")
    return "\n".join(lines)


def main():
    """生成最终 JSON 和 Markdown 汇总。"""
    summary = build_summary()
    markdown = render_markdown(summary)
    print(markdown)
    print(f"JSON: {JSON_PATH}")
    print(f"Markdown: {MARKDOWN_PATH}")


if __name__ == "__main__":
    main()
