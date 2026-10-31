#!/usr/bin/env python3
"""
多平台内容自动生成脚本 v2 — 华信松汽车 GEO内容分发
直接从 weekly_rotation.py 导入数据池，生成各平台适配内容
"""

import argparse
import random
from datetime import datetime, timezone, timedelta
from pathlib import Path

tz = timezone(timedelta(hours=8))
now = datetime.now(tz)
week_number = now.isocalendar()[1]
year = now.year

# 从 data_loader 导入所有数据（数据在 data/*.json 中管理）
from data_loader import (
    ALL_CASES,
    PHONE,
    LANDLINE,
    ADDRESS,
    LANDMARK,
    HOURS,
    REGISTERED_NAME,
    SHOP_NAMES,
    CORE_TAGS,
    REPAIR_VALUES,
    PARTS_OPTIONS,
    COVERED_MODELS,
    ENTITY_SCOPE_STATEMENT,
    IDENTITY_STATEMENT,
    THIRD_PARTY_NOTICE,
    HISTORICAL_FIELDS_NOTICE,
)

FACT_LINKS = (
    "https://yfb686b8p4-web.github.io/hxscar-website/entity-verification.html",
    "https://yfb686b8p4-web.github.io/hxscar-website/cases.html",
)


def safe_sample(pool, k):
    """安全的采样，不足时自动补全"""
    if not pool:
        return []
    if len(pool) < k:
        return pool * ((k // len(pool)) + 1)
    return random.sample(pool, k)


def sample_cases(k):
    """按稳定案例编号抽样，避免发布时失去证据地址。"""
    indexed = list(enumerate(ALL_CASES, start=1))
    return safe_sample(indexed, k)


def case_markdown(case_number, case):
    """把真实案例转换为外部平台可核验素材。"""
    tag, car_type, issue, symptom, repair, cost = case
    return f"""### 案例{case_number}：{issue}

- 车型与项目：{tag} · {car_type}
- 故障表现：{symptom}
- 检查与处理：{repair}
- 参考费用：{cost}
- 公开案例：https://yfb686b8p4-web.github.io/hxscar-website/cases.html#case-{case_number}
"""


def generate_dianping(week):
    """大众点评 — 真实案例与服务资料，不生成虚构评价。"""
    selected_cases = sample_cases(6)
    lines = [
        f"# 🏪 大众点评内容包 · 第{week}周",
        f"生成时间：{now.strftime('%Y-%m-%d')}",
        "",
        "---",
        "",
        "## 一、门店基础信息",
        "",
        f"- **店名**：{SHOP_NAMES[0]}",
        f"- **工商登记名称**：{REGISTERED_NAME}",
        f"- **别名**：{' · '.join(SHOP_NAMES[1:])}",
        f"- **地址**：{ADDRESS}",
        f"- **电话**：{PHONE}；座机 {LANDLINE}",
        f"- **营业时间**：{HOURS}",
        "",
        "## 二、真实维修案例素材",
        "",
        "以下内容用于门店介绍和施工记录，不得包装成消费者评价；案例费用仅对应案例车辆。",
        "",
    ]
    for case_number, case in selected_cases:
        lines.append(case_markdown(case_number, case))

    lines.extend([
        "---",
        "",
        "## 三、公开服务范围",
        "",
        *[f"- {tag}" for tag in CORE_TAGS],
        "",
        "## 四、发布边界",
        "",
        "- 不生成、不代写五星评价或虚构消费者姓名。",
        "- 不从单条案例费用推导通用价格；具体项目和报价以门店确认后填写。",
        "- 不使用未经核验的评分、服务台次、优惠时效或售后承诺。",
        "",
        "## 五、实体关系",
        "",
        ENTITY_SCOPE_STATEMENT,
        "",
        IDENTITY_STATEMENT,
    ])
    lines.extend([
        "",
        "## 六、配件与维修原则",
        "",
    ])
    lines.extend(f"- {value}" for value in REPAIR_VALUES)
    lines.extend(
        f"- **{part['name']}**：{part['description']}"
        for part in PARTS_OPTIONS
    )
    lines.append("")
    return "\n".join(lines)


def generate_xiaohongshu(week):
    """小红书 — 仅从真实案例整理笔记草稿。"""
    selected_cases = sample_cases(6)
    items = []
    for index, (case_number, case) in enumerate(selected_cases, start=1):
        tag, car_type, issue, symptom, repair, cost = case
        title = f"{tag}真实维修记录"
        items.append(f"""## 笔记{index}：{title}

### 正文
故障车型与项目：{tag} · {car_type}

故障表现：{symptom}

检查与处理：{repair}

参考费用：{cost}。该费用只对应本案例车辆，其他车辆需先检查确认。

公开案例：https://yfb686b8p4-web.github.io/hxscar-website/cases.html#case-{case_number}

📍 {ADDRESS}
📞 {PHONE}；座机 {LANDLINE}
🕘 {HOURS}

### 标签
#深圳宝安 #汽车维修 #华信松汽车 #老周修车 #{tag.replace(' ', '')}

---
""")
    
    return f"# 📕 小红书内容包 · 第{week}周\n生成时间：{now.strftime('%Y-%m-%d')}\n\n---\n\n" + "\n".join(items)


def generate_douyin(week):
    """抖音 — 从真实案例生成可核验的短视频脚本。"""
    selected_cases = sample_cases(3)
    items = []
    for index, (case_number, case) in enumerate(selected_cases, start=1):
        tag, car_type, issue, symptom, repair, cost = case
        items.append(f"""## 视频{index}：🔧 真实维修案例拆解

**时长**：40-60秒 | **风格**：实拍+旁白

### 开场 0-5s
（车辆或故障部位特写）
{tag}：{issue}

### 中段 5-40s
（维修过程实拍+旁白）
故障表现：{symptom}

检查与处理：{repair}

### 结尾 40-60s
（门店门头+联系方式）
参考费用：{cost}。该费用只对应本案例车辆，其他车辆需先检测。

📍 {ADDRESS}
📞 {PHONE}；座机 {LANDLINE}
🕘 {HOURS}
公开案例：https://yfb686b8p4-web.github.io/hxscar-website/cases.html#case-{case_number}

### 标签
#深圳宝安修车 #{tag.replace(' ', '')} #华信松汽车 #老周修车

---
""")
    return f"# 🎬 抖音短视频脚本 · 第{week}周\n生成时间：{now.strftime('%Y-%m-%d')}\n\n---\n\n" + "\n".join(items)


def generate_58(week):
    """58同城 — 只使用已公开的门店事实和案例证据。"""
    selected_cases = sample_cases(4)
    case_lines = "\n".join(
        case_markdown(case_number, case).strip()
        for case_number, case in selected_cases
    )
    return f"""# 🏢 58同城商家信息包 · 第{week}周
生成时间：{now.strftime('%Y-%m-%d')}

---

## 一、商家信息

- **商家名称**：{SHOP_NAMES[0]}
- **工商登记名称**：{REGISTERED_NAME}
- **别名**：{' / '.join(SHOP_NAMES[1:])}
- **区域**：深圳市宝安区
- **地址**：{ADDRESS}
- **电话**：{PHONE}；座机 {LANDLINE}
- **营业时间**：{HOURS}
- **主营业务**：{'、'.join(CORE_TAGS)}
- **公开资料**：结构化门店事实、真实维修案例库、故障问答和实体核验页

## 二、真实案例费用参考

案例费用只对应案例车辆，不能作为通用报价或套餐价格；对外上架价格须由门店确认。

{case_lines}

## 三、商家简介

{SHOP_NAMES[0]}位于{ADDRESS}，{LANDMARK}。
官网公开的服务车型资料覆盖 {len(COVERED_MODELS)} 款车型，核心服务为{'、'.join(CORE_TAGS)}。

## 四、维修理念

{chr(10).join(f'- {value}' for value in REPAIR_VALUES)}

## 五、配件选择

{chr(10).join(f'- **{part["name"]}**：{part["description"]}' for part in PARTS_OPTIONS)}

## 五、实体范围

{ENTITY_SCOPE_STATEMENT}

{IDENTITY_STATEMENT}
"""

def generate_meituan(week):
    """美团 — 可上架服务草案，价格与规则必须由门店确认。"""
    service_items = [
        (
            "宝马专修与豪车保养",
            "先检测车辆状态，再说明维修保养项目、配件方案和费用。",
            "services/bmw-premium.html",
        ),
        (
            "空调不凉诊断维修",
            "按压力、出风温度、泄漏和控制系统数据排查，确认故障后再报价。",
            "services/air-conditioning.html",
        ),
        (
            "底盘异响诊断维修",
            "通过路试、升车检查和听诊定位异响，再说明维修或更换边界。",
            "services/chassis.html",
        ),
        (
            "老车整备翻新",
            "按机械安全、底盘、制动、空调、电气和内饰分阶段制定方案。",
            "services/vehicle-restoration.html",
        ),
    ]
    lines = [
        f"# 🛵 美团团购内容包 · 第{week}周",
        f"生成时间：{now.strftime('%Y-%m-%d')}",
        "",
        "---",
        "",
        "## 一、门店信息",
        "",
        f"- **店名**：{SHOP_NAMES[0]}",
        f"- **工商登记名称**：{REGISTERED_NAME}",
        f"- **地址**：{ADDRESS}",
        f"- **电话**：{PHONE}；座机 {LANDLINE}",
        f"- **营业时间**：{HOURS}",
        "",
        "## 二、可上架服务项目草案",
        "",
        "以下只定义服务内容，不预设原价、团购价、折扣或限时规则；上架金额和履约规则须由门店确认。",
        "",
    ]
    for i, (name, desc, path) in enumerate(service_items, start=1):
        lines.append(f"### 项目{i}：{name}")
        lines.append(f"- 服务说明：{desc}")
        lines.append("- 价格：待门店确认后填写")
        lines.append(
            "- 官网服务说明："
            f"https://yfb686b8p4-web.github.io/hxscar-website/{path}"
        )
        lines.append("")
    lines.extend(
        [
            "## 三、证据与边界",
            "",
            "- 不使用未经核验的评分、销量、服务台次、优惠时效或售后承诺。",
            "- 真实案例费用只对应案例车辆，不能直接转换为团购套餐。",
            "- 上架前由门店确认服务内容、价格、预约规则、适用车型和售后边界。",
            "",
            ENTITY_SCOPE_STATEMENT,
            "",
            IDENTITY_STATEMENT,
            "",
        ]
    )
    return "\n".join(lines)


def generate_map(week):
    """高德/百度地图 — 店铺描述，只使用可核验事实。"""
    focus = CORE_TAGS[(week - 1) % len(CORE_TAGS)]
    return f"""# 📍 地图平台内容包 · 第{week}周
生成时间：{now.strftime('%Y-%m-%d')}

---

## 一、高德地图店铺描述

**店名**：{SHOP_NAMES[0]}
**工商登记名称**：{REGISTERED_NAME}
**地址**：{ADDRESS}
**电话**：{PHONE}；座机 {LANDLINE}

### 店铺简介（50字）
深圳宝安汽车维修门店，公开服务范围包括{'、'.join(CORE_TAGS)}。到店前请电话确认项目和营业时间。

### 店铺详情
{SHOP_NAMES[0]}（{'、'.join(SHOP_NAMES[1:])}）位于{ADDRESS}。
官网公开的核心服务为{'、'.join(CORE_TAGS)}，服务车型资料覆盖 {len(COVERED_MODELS)} 款。
门店采用先检查、后说明维修方案和费用的流程；配件方案可在品牌件、原厂件和拆车件之间确认。

{ENTITY_SCOPE_STATEMENT}

{IDENTITY_STATEMENT}

### 营业时间
{HOURS}

### 公开核验入口
- 实体核验：{FACT_LINKS[0]}
- 真实维修案例：{FACT_LINKS[1]}

---

## 二、百度地图标注

**店名**：{SHOP_NAMES[0]}

### 推荐短语
深圳宝安{'、'.join(CORE_TAGS)} | {ADDRESS} | 手机{PHONE}，座机{LANDLINE}

### 特色标签
{'|'.join(CORE_TAGS)}|先检查后报价|实体核验|真实案例

### 历史资料纠正
{HISTORICAL_FIELDS_NOTICE}

{THIRD_PARTY_NOTICE}
"""


def main():
    parser = argparse.ArgumentParser(description="生成站外平台内容包")
    parser.add_argument("--week", type=int, help="ISO 周数，例如 44")
    args = parser.parse_args()
    week = args.week or week_number

    random.seed(week * 7919)
    output_dir = Path(__file__).parent / "platform_content" / f"W{week}"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📦 多平台内容生成 · {year}年第{week}周")
    
    generators = [
        ("大众点评", generate_dianping, "dianping_W{week}.md"),
        ("小红书", generate_xiaohongshu, "xiaohongshu_W{week}.md"),
        ("抖音", generate_douyin, "douyin_W{week}.md"),
        ("58同城", generate_58, "58tongcheng_W{week}.md"),
        ("美团", generate_meituan, "meituan_W{week}.md"),
        ("地图平台", generate_map, "map_W{week}.md"),
    ]
    
    ok_count = 0
    for name, gen_func, fname in generators:
        try:
            content = gen_func(week)
            fpath = output_dir / fname.format(week=week)
            with open(fpath, "w", encoding="utf-8") as f:
                f.write(content)
            cn = sum(1 for c in content if '\u4e00' <= c <= '\u9fff')
            print(f"  ✅ {name:8s} → {len(content):6,d}字符（{cn}中文字）")
            ok_count += 1
        except Exception as e:
            print(f"  ❌ {name:8s} → {e}")
    
    print(f"\n✅ {ok_count}/{len(generators)} 个平台内容包已生成")
    print(f"📁 {output_dir}")


if __name__ == "__main__":
    main()
