#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""根据 AI 搜索实测结果生成差距分析和跨平台发布策略。"""

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
LATEST_PATH = ROOT / "reports" / "rank-history" / "latest.json"
SNAPSHOT_DIR = ROOT / "reports" / "rank-history"
DAILY_PATH = ROOT / "reports" / "daily" / "latest.json"
REPORT_PATH = ROOT / "reports" / "visibility-insights.md"
JSON_PATH = ROOT / "reports" / "visibility-insights.json"
PLAN_PATH = ROOT / "publishing" / "CROSS_PLATFORM_PLAN.md"
TZ = timezone(timedelta(hours=8))


def load_json(path):
    """读取 JSON 文件。"""
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def write_json(path, data):
    """写入格式化 JSON。"""
    path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def latest_snapshot():
    """读取汇总对应的原始快照。"""
    summary = load_json(LATEST_PATH)
    snapshot_path = Path(summary["snapshot"])
    return summary, load_json(snapshot_path)


def negative_mentions(snapshot):
    """找出负面或错误提及。"""
    results = []
    for keyword_id, item in snapshot["results"].items():
        for platform, result in item["platforms"].items():
            if result.get("status") != "completed":
                continue
            notes = result.get("notes", "")
            if result.get("sentiment") == "negative" or "错误" in notes:
                results.append(
                    {
                        "keyword_id": keyword_id,
                        "query": item["query"],
                        "platform": platform,
                        "notes": notes,
                    }
                )
    return results


def percentage(part, total):
    """计算一位小数百分比。"""
    return round(part * 100 / total, 1) if total else 0.0


def parse_position(value):
    """把推荐位置转换为正整数。"""
    try:
        position = int(value)
    except (TypeError, ValueError):
        return None
    return position if position > 0 else None


def aggregate_records(records):
    """把每日检测记录汇总为平台和分类指标。"""
    completed_records = [
        item for item in records if item.get("status") == "completed"
    ]
    platform_values = {}
    category_values = {}
    for item in completed_records:
        mentioned = bool(item.get("mentioned"))
        position = parse_position(item.get("position"))
        for values, key in (
            (platform_values, item.get("platform", "")),
            (category_values, item.get("category", "")),
        ):
            if not key:
                continue
            bucket = values.setdefault(
                key,
                {
                    "total": 0,
                    "completed": 0,
                    "mentioned": 0,
                    "positions": [],
                },
            )
            bucket["total"] += 1
            bucket["completed"] += 1
            bucket["mentioned"] += int(mentioned)
            if position:
                bucket["positions"].append(position)
    for values in (platform_values, category_values):
        for bucket in values.values():
            bucket["mention_rate"] = percentage(
                bucket["mentioned"], bucket["completed"]
            )
            bucket["average_position"] = (
                round(sum(bucket["positions"]) / len(bucket["positions"]), 1)
                if bucket["positions"]
                else None
            )

    mentioned = sum(
        int(bool(item.get("mentioned"))) for item in completed_records
    )
    effective_hits = sum(
        int(bool(item.get("effective_hit"))) for item in completed_records
    )
    overall = {
        "total": len(records),
        "completed": len(completed_records),
        "pending": len(records) - len(completed_records),
        "mentioned": mentioned,
        "mention_rate": percentage(mentioned, len(completed_records)),
        "effective_hits": effective_hits,
        "effective_hit_rate": percentage(
            effective_hits, len(completed_records)
        ),
    }
    return {
        "overall": overall,
        "by_platform": platform_values,
        "by_category": category_values,
    }


def daily_negative_mentions(records):
    """从每日记录找出错误或负面提及。"""
    results = []
    for item in records:
        if item.get("status") != "completed":
            continue
        notes = item.get("notes", "")
        sentiment = item.get("sentiment", "")
        if (
            item.get("identity_relation") == "wrong"
            or sentiment in {"负面", "negative"}
            or "错误" in notes
        ):
            results.append(
                {
                    "keyword_id": item.get("check_id", ""),
                    "query": item.get("query", ""),
                    "platform": item.get("platform", ""),
                    "notes": notes or item.get("answer_summary", ""),
                }
            )
    return results


def select_summary():
    """优先使用已有完成结果的最新日报，否则回退到排名快照。"""
    daily = load_json(DAILY_PATH) if DAILY_PATH.exists() else {}
    daily_completed = int(daily.get("metrics", {}).get("completed", 0))
    if daily_completed > 0:
        return {
            "source": "reports/daily/latest.json",
            "source_generated_at": daily.get("generated_at", ""),
            "summary": aggregate_records(daily.get("records", [])),
            "negatives": daily_negative_mentions(daily.get("records", [])),
        }
    summary, snapshot = latest_snapshot()
    return {
        "source": "reports/rank-history/latest.json",
        "source_generated_at": summary.get("updated_at", ""),
        "summary": summary,
        "negatives": negative_mentions(snapshot),
    }


def build_insights():
    """构建差距与行动建议。"""
    selected = select_summary()
    summary = selected["summary"]
    categories = summary["by_category"]
    completed_categories = {
        name: values
        for name, values in categories.items()
        if values["completed"] > 0
    }
    zero_categories = [
        name
        for name, values in completed_categories.items()
        if values["mentioned"] == 0
    ]
    strong_categories = [
        name
        for name, values in completed_categories.items()
        if values["mention_rate"] >= 50
    ]
    negatives = selected["negatives"]

    actions = []
    if any("同一家" in item["query"] for item in negatives):
        actions.append(
            "优先统一门店实体：在所有平台固定写明“老周修车、驰加米其林幸福海岸店、华信松汽车、宝源南路店为同一家门店”。"
        )
    for category in zero_categories:
        actions.append(
            f"为“{category}”发布真实检测、施工过程、配件选择和费用范围内容，增加可被 AI 引用的第三方证据。"
        )
    if strong_categories:
        actions.append(
            "保留已命中的门店身份和空调维修内容结构，持续更新真实案例，避免只重复关键词。"
        )
    actions.append(
        "各平台名称、地址、电话、营业时间和主营项目必须一致，发布后回填真实链接。"
    )

    insights = {
        "generated_at": datetime.now(TZ).date().isoformat(),
        "source": selected["source"],
        "source_generated_at": selected["source_generated_at"],
        "overall": summary["overall"],
        "platforms": summary["by_platform"],
        "categories": categories,
        "zero_hit_categories": zero_categories,
        "strong_categories": strong_categories,
        "negative_mentions": negatives,
        "recommended_actions": actions,
    }
    write_json(JSON_PATH, insights)

    lines = [
        "# AI 搜索可见性洞察",
        "",
        f"- 生成时间：{insights['generated_at']}",
        f"- 数据来源：`{insights['source']}`",
        f"- 来源更新时间：{insights['source_generated_at']}",
        f"- 已完成检查：{summary['overall']['completed']}/{summary['overall']['total']}",
        f"- 提及次数：{summary['overall']['mentioned']}",
        f"- 已检查命中率：{summary['overall']['mention_rate']}%",
        f"- 有效命中率：{summary['overall'].get('effective_hit_rate', 0.0)}%",
        "",
        "## 分类结果",
        "",
        "| 分类 | 已完成 | 提及 | 命中率 |",
        "|---|---:|---:|---:|",
    ]
    for name, values in categories.items():
        lines.append(
            f"| {name} | {values['completed']}/{values['total']} | "
            f"{values['mentioned']} | {values['mention_rate']}% |"
        )
    lines.extend(["", "## 主要发现", ""])
    lines.append(
        f"- 零命中分类：{'、'.join(zero_categories) if zero_categories else '无'}"
    )
    lines.append(
        f"- 高命中分类：{'、'.join(strong_categories) if strong_categories else '暂无'}"
    )
    if negatives:
        for item in negatives:
            lines.append(
                f"- 错误提及：{item['platform']}「{item['query']}」：{item['notes']}"
            )
    else:
        lines.append("- 未发现错误或负面提及")
    lines.extend(["", "## 行动建议", ""])
    lines.extend(f"- {action}" for action in actions)
    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")

    plan = f"""# 跨平台发布策略

生成时间：{datetime.now(TZ).date().isoformat()}

## 第一优先级：纠正门店实体

所有平台必须统一使用：

- 华信松汽车服务有限公司（幸福海岸分公司）
- 老周修车
- 驰加米其林幸福海岸店
- 米其林驰加汽车服务中心（宝源南路店）
- 宝源南路店

明确写出这些名称对应同一地址、同一电话、同一门店。

## 第二优先级：补零命中服务

当前零命中分类：{'、'.join(zero_categories) if zero_categories else '无'}

每个 P0 平台发布内容时，优先安排：

1. 宝马专修与豪车保养：真实车型、故障、检测数据、维修过程。
2. 底盘异响诊断维修：路试、升车检查、胶套或球头处理过程。
3. 老车整备翻新：整备清单、能修不换、品牌件/原厂件/拆车件选择。
4. 空调不凉诊断维修：继续保持真实检漏、压力数据和维修前后结果。

## 平台顺序

### 地图平台

先完成高德、百度、腾讯地图的认领和资料统一。地图是 AI 搜索判断门店真实性的基础来源。

### 大众点评、美团

更新门店介绍、服务项目、真实照片、施工案例和评价回复，名称统一覆盖全部别名。

### 抖音

先发布门店身份统一文章，再发布宝马、底盘和老车整备的真实案例。视频内容优先使用维修前后画面对比。

### 小红书

重点发布车型维修故事、故障判断、配件选择和整备清单，避免纯广告文案。

### 58 同城

补充本地商家资料、服务范围、配件选择和营业时间。

## 发布验收

- 每个平台发布后回填真实链接。
- 每周重新查询豆包及其他 AI 平台。
- 比较门店实体错误是否消失、零命中分类是否开始命中。
- 不以发布数量代替效果，以提及率、推荐位置和引用来源判断效果。
"""
    PLAN_PATH.write_text(plan, encoding="utf-8")
    print(f"已生成洞察: {REPORT_PATH}")
    print(f"已生成跨平台策略: {PLAN_PATH}")
    return insights


if __name__ == "__main__":
    build_insights()
