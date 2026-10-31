# AI 证据 Release 发布记录｜2026-11-01

## 公开入口

- Release：https://github.com/yfb686b8p4-web/hxscar-website/releases/tag/ai-evidence-2026-11-01
- GitHub Profile：https://github.com/yfb686b8p4-web/yfb686b8p4-web
- Profile 实体镜像页：https://yfb686b8p4-web.github.io/yfb686b8p4-web/
- GitHub Gist：https://gist.github.com/yfb686b8p4-web/7923ef0b18ffbcce04a8b6758254a06b

## 附件

| 附件 | 状态 | 用途 |
|---|---|---|
| `store-facts.json` | HTTP 200 | 字段级门店事实与历史资料纠错 |
| `store-facts.jsonld` | HTTP 200 | Schema.org `AutoRepair` 实体 |
| `case-evidence.json` | HTTP 200 | 56 条真实维修案例 `ItemList` |
| `llms.txt` | HTTP 200 | AI 资料索引 |
| `llms-full.txt` | HTTP 200 | 证据边界内机器语料 |

## 双向关联

- 官网首页、答案页、服务页、车型页、`store-facts.json` 和 `store-facts.jsonld` 均已加入 Release 入口或附件镜像。
- Gist 的 `store-facts.jsonld` 已加入 Release 页面地址，并通过 `subjectOf` 关联 3 个 Release 数据附件。
- Gist 的 `ENTITY_FACTS.md` 已加入 Release 入口。
- GitHub Profile README 已加入 Release 入口，远端提交为 `e46099b`。
- 结构化实体已拆分身份与文档关系：`sameAs` 只保留官网仓库、GitHub Profile、抖音、地图和工商页；Gist、Release 页面与附件改放到 `subjectOf`。

## 验证结果

- Release 的 5 个附件均通过独立下载地址验证为 HTTP 200。
- 官网 4 个服务页均包含 `Service` 与 5 步 `HowTo`。
- FAQ 人工问题库为 142 条，机器 FAQ 结构化数据为 97 条。
- 当前 73 项单元测试通过，站点审计通过。

## 事实边界

本记录只证明证据包已公开发布、附件可下载并已写入官网机器事实；不证明 Bing、百度、豆包、元宝或其他平台已经收录、引用或排名。
