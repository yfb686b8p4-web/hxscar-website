# 首页 Lighthouse 移动端优化记录｜2026-11-01

## 审计对象

- URL：https://yfb686b8p4-web.github.io/hxscar-website/
- 工具：Lighthouse CLI，移动端默认节流
- 审计分类：Performance、Accessibility、Best Practices、SEO

## 优化前

| 分类 | 分数 |
|---|---:|
| 性能 | 99 |
| 可访问性 | 95 |
| 最佳实践 | 100 |
| SEO | 100 |

- LCP：2.2 秒
- Speed Index：2.3 秒
- CLS：0
- 颜色对比度失败节点：121 个
- 首屏门头图为 150 KiB JPEG

## 已完成优化

- 为正文与按钮拆分两套强调色：深色背景使用 `#ff8ca0`，白字按钮使用 `#b42318`。
- 普通卡片链接使用浅蓝色 `#8ab4ff`，增加键盘 `focus-visible` 轮廓。
- 用 FFmpeg 从真实门头原图生成 WebP：
  - `store-banner-960.webp`：92 KiB，960x540
  - `store-banner.webp`：167 KiB，1291x726
- 首页通过 `<picture>` 和 preload 优先加载 WebP，同时保留 JPEG 回退。
- WebP 已加入 sitemap、图片 sitemap、IndexNow 和每日线上检查。

## 优化后

| 分类 | 分数 |
|---|---:|
| 性能 | 100 |
| 可访问性 | 100 |
| 最佳实践 | 100 |
| SEO | 100 |

- LCP：1.6 秒
- Speed Index：2.2 秒
- Total Blocking Time：30 毫秒
- CLS：0
- 颜色对比度失败节点：0
- IndexNow：57 个 URL，聚合端点和 Bing 直连端点均返回 HTTP 200

## 说明

Lighthouse 分数会随网络和运行环境轻微波动；本次结论对应 2026-11-01 05:24（Asia/Shanghai）对线上首页的实际审计。IndexNow HTTP 200 只代表通知被接收，不代表收录、引用或排名。
