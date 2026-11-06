#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""汇总最近若干天的 AI 搜索复测趋势。"""

import argparse
import json
from datetime import date, timedelta
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DAILY_DIR = ROOT / "reports" / "daily"
STATUS_PATH = ROOT / "publishing" / "status.json"
OUTPUT_JSON = ROOT / "reports" / "ai-search-trend.json"
OUTPUT_MD = ROOT / "reports" / "ai-search-trend.md"


def load_json(path):
    """读取 JSON 文件。"""
    return json.loads(path.read_text(encoding="utf-8"))


def load_days(days):
    """读取最近若干天的日报。"""
    start = date.today() - timedelta(days=max(days - 1, 0))
    records = []
    for path in sorted(DAILY_DIR.glob("20??-??-??.json")):
        try:
            current = date.fromisoformat(path.stem)
        except ValueError:
            continue
        if current < start:
            continue
        data = load_json(path)
        metrics = data.get("metrics", {})
        identity_records = [
            item
            for item in data.get("records", [])
            if "门店身份" in item.get("category", "")
            and item.get("status") == "completed"
        ]
        records.append(
            {
                "date": path.stem,
                "generated_at": data.get("generated_at", ""),
                "completed": metrics.get("completed", 0),
                "total": metrics.get("total", 0),
                "pending": metrics.get("pending", 0),
                "effective_hits": metrics.get("effective_hits", 0),
                "entity_correct": sum(
                    1
                    for item in identity_records
                    if item.get("identity_relation") == "correct"
                ),
                "entity_completed": len(identity_records),
                "full_info_correct": sum(
                    1
                    for item in identity_records
                    if item.get("address_ok") is True
                    and item.get("phone_ok") is True
                    and item.get("hours_ok") is True
                ),
                "service_hits": metrics.get("service_hits", 0),
                "service_completed": metrics.get("service_completed", 0),
                "service_top1": metrics.get("service_top1", 0),
                "service_top3": metrics.get("service_top3", 0),
            }
        )
    return records


def rate(part, total):
    """计算百分比。"""
    return round(part / total * 100, 1) if total else 0.0


def trend_point(item):
    """补充可直接展示的百分比。"""
    return {
        **item,
        "entity_rate": rate(item["entity_correct"], item["entity_completed"]),
        "full_info_rate": rate(
            item["full_info_correct"], item["entity_completed"]
        ),
        "service_hit_rate": rate(
            item["service_hits"], item["service_completed"]
        ),
        "service_top3_rate": rate(
            item["service_top3"], item["service_completed"]
        ),
    }


def platform_blockers():
    """读取仍需人工处理的平台。"""
    status = load_json(STATUS_PATH).get("platforms", {})
    return [
        {
            "id": platform_id,
            "status": item.get("status", ""),
            "updated_at": item.get("updated_at", ""),
        }
        for platform_id, item in status.items()
        if item.get("status") != "published"
    ]


def next_actions(points):
    """根据趋势给出下一步，不把波动误判为排名。"""
    if not points:
        return ["还没有可汇总的日报。"]
    latest = points[-1]
    actions = []
    if latest["entity_rate"] < 100:
        actions.append("优先统一地图、工商聚合页和公众号中的实体关系。")
    if latest["full_info_rate"] < 100:
        actions.append("优先补齐标准地址、双电话和分时营业时间。")
    if latest["service_hits"] == 0:
        actions.append("暂停新增同义官网内容，先补真实第三方引用与本地店铺页。")
    if any(
        item["id"] == "tencent-map" and item["status"] != "published"
        for item in platform_blockers()
    ):
        actions.append("继续跟踪腾讯地图标准 POI 公开索引。")
    if len(points) < 3:
        actions.append("至少积累 3 天样本后再判断趋势或调整内容。")
    return actions


def build_report(days):
    """生成结构化趋势与 Markdown 报告。"""
    points = [trend_point(item) for item in load_days(days)]
    blockers = platform_blockers()
    return {
        "generated_at": date.today().isoformat(),
        "window_days": days,
        "samples": len(points),
        "points": points,
        "blockers": blockers,
        "next_actions": next_actions(points),
    }


def render_markdown(report):
    """输出便于人工阅读的趋势报告。"""
    lines = [
        "# AI 搜索 7 日趋势",
        "",
        f"- 生成日期：{report['generated_at']}",
        f"- 有效样本天数：{report['samples']}",
        "",
        "| 日期 | 完成 | 有效命中 | 实体正确 | 完整资料 | 服务命中 | Top3 | 待补测 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for item in report["points"]:
        lines.append(
            "| {date} | {completed}/{total} | {effective_hits} | "
            "{entity_correct}/{entity_completed} | "
            "{full_info_correct}/{entity_completed} | "
            "{service_hits}/{service_completed} | "
            "{service_top3}/{service_completed} | {pending} |".format(
                **item
            )
        )
    lines.extend(["", "## 关键判断", ""])
    lines.extend(f"- {item}" for item in report["next_actions"])
    lines.extend(["", "## 仍需人工处理", ""])
    if report["blockers"]:
        lines.extend(
            f"- `{item['id']}`：{item['status']}（{item['updated_at']}）"
            for item in report["blockers"]
        )
    else:
        lines.append("- 无")
    lines.extend(
        [
            "",
            "## 使用边界",
            "",
            "- 单日波动不作为排名结论。",
            "- 至少 3 个独立新对话后再判断稳定性。",
            "- 页面已发布、提交索引或账号审核通过，不等于已收录或已排名。",
            "",
        ]
    )
    return "\n".join(lines)


def main():
    """命令行入口。"""
    parser = argparse.ArgumentParser(description="汇总 AI 搜索复测趋势")
    parser.add_argument("--days", type=int, default=7)
    parser.add_argument("--output-json", type=Path, default=OUTPUT_JSON)
    parser.add_argument("--output-md", type=Path, default=OUTPUT_MD)
    args = parser.parse_args()
    report = build_report(max(args.days, 1))
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    args.output_md.write_text(render_markdown(report), encoding="utf-8")
    print(render_markdown(report))
    print(f"JSON：{args.output_json.relative_to(ROOT)}")
    print(f"Markdown：{args.output_md.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
