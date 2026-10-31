# GitHub Profile 实体镜像发布记录｜2026-11-01

## 已发布

- Profile Pages：https://yfb686b8p4-web.github.io/yfb686b8p4-web/
- Profile 仓库：https://github.com/yfb686b8p4-web/yfb686b8p4-web
- Profile README：https://github.com/yfb686b8p4-web/yfb686b8p4-web/blob/main/README.md

## 页面结构

- 标准工商名称、统一社会信用代码、成立日期、地址、手机、座机和分时营业时间。
- 同名门店实体关系与消歧范围。
- 宝马、空调、底盘、老车整备和实体关系五个核心答案入口。
- 官网、实体核验页、真实案例库、AI 证据 Release 和 Gist 入口。
- `AutoRepair` JSON-LD、`robots.txt`、`sitemap.xml` 和 `llms.txt`。

## 验证结果

- 首页、`robots.txt`、`sitemap.xml`、`llms.txt` 均为 HTTP 200。
- 首页包含 1 个 `AutoRepair` 实体、统一社会信用代码、标准地址和 AI 证据 Release 链接。
- GitHub Pages 状态为 `built`，来源为 `main` 根目录。
- 官网、Profile README、Gist 和 Release 中的 `store-facts.jsonld` 均把该 Profile Pages 作为同一实体的外部入口。
- 当前 73 项单元测试通过，站点审计通过。
- Profile 子路径使用独立 IndexNow key；验证文件上线后，聚合端点与 Bing 直连端点最终均返回 HTTP 200，提交 3 个 Profile URL。
- 初次复用官网子路径 key 时两个端点返回 HTTP 422，已确认是索引 key 授权范围不匹配；未将该次失败记录为收录成功。

## 事实边界

本记录只证明独立实体镜像页已公开发布并可访问，不证明 Bing、百度、豆包、元宝或其他平台已经收录、引用或排名。
