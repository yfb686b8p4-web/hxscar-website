#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""识别未提供可核验依据的价格、优惠、时效、资历和售后承诺。"""


UNVERIFIED_FAQ_MARKERS = (
    "免费检测",
    "质保",
    "当天",
    "10年",
    "4S",
    "数百位",
    "原厂诊断",
    "ISTA",
    "PIWIS",
    "SDD",
    "DAS",
    "4.9",
    "1000台",
    "省一半",
    "不限里程",
)


def unverified_faq_markers(item):
    """返回一条 FAQ 中命中的未核验承诺标记。"""
    if isinstance(item, dict):
        text = item["question"] + item["answer"]
    else:
        text = item[0] + item[1]
    return [marker for marker in UNVERIFIED_FAQ_MARKERS if marker in text]


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
