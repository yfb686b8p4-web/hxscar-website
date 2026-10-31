#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""识别未提供可核验依据的价格、优惠、时效、资历和售后承诺。"""

import re


UNVERIFIED_FAQ_MARKERS = (
    "免费",
    "当天",
    "立等可取",
    "排名第一",
    "口碑推荐率高",
    "300位",
    "数百位",
    "1000台",
    "10年",
    "4S",
    "原厂诊断",
    "原厂设备",
    "原厂电路图",
    "原厂专用",
    "专用工具",
    "专业设备",
    "ISTA",
    "PIWIS",
    "SDD",
    "DAS",
    "4.9",
    "省一半",
    "不限里程",
    "技术有保障",
    "精准诊断",
    "精准定位",
    "快速诊断",
    "快速查漏",
    "彻底解决",
    "一步到位",
    "不损伤",
    "无损复原",
    "绝不",
    "不花冤枉钱",
    "不误判",
    "成功案例",
    "德国进口",
    "经验丰富",
    "资深技师",
    "所有维修记录",
    "存档可查",
    "亲自跟车",
    "换轮胎",
    "轮胎库存",
    "隐形车衣",
    "贴膜",
    "改装",
    "救援",
    "休息区",
    "不影响安全",
    "全系",
    "保证",
    "确保",
)

UNVERIFIED_FAQ_PATTERNS = (
    r"质保\s*(?:[0-9一二两三四五六七八九十]+\s*(?:年|个月|月)|无忧|完善|不限里程)",
    r"(?:提供|含|包含|享受|承诺)[^。；]{0,12}质保",
    r"不影响质保",
    r"比\s*4S\s*(?:便宜|省)",
)


def unverified_claim_markers(text):
    """返回文本中的字面风险词和具体未核实承诺模式。"""
    matches = [
        marker for marker in UNVERIFIED_FAQ_MARKERS if marker in text
    ]
    for pattern in UNVERIFIED_FAQ_PATTERNS:
        match = re.search(pattern, text)
        if match:
            matches.append(match.group(0))
    return matches


def unverified_faq_markers(item):
    """返回一条 FAQ 中命中的未核验承诺标记。"""
    if isinstance(item, dict):
        text = item["question"] + item["answer"]
    else:
        text = item[0] + item[1]
    return unverified_claim_markers(text)


def partition_faqs(items):
    """将 FAQ 分为可进入机器语料和待核验两组。"""
    safe = []
    blocked = []
    for item in items:
        matches = unverified_faq_markers(item)
        if matches:
            blocked.append({"item": item, "markers": matches})
        else:
            safe.append(item)
    return safe, blocked
