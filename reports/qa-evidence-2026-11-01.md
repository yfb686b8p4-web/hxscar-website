# 原子问答证据数据｜2026-11-01

## 产物

- 文件：`qa-evidence.jsonl`
- 线上地址：https://yfb686b8p4-web.github.io/hxscar-website/qa-evidence.jsonl
- Gist 镜像：https://gist.githubusercontent.com/yfb686b8p4-web/7923ef0b18ffbcce04a8b6758254a06b/raw/51d9f49a2de4747a06623369738c0376fa3aa781/qa-evidence.jsonl
- 格式：UTF-8 JSONL，每行一条 schema.org `Question`
- 记录数：15 条唯一标准问答
- 带真实案例记录：12 条
- 每答案最少引用：15 个 HTTPS 来源

## 每条记录包含

- 标准问题、同一问题的常见问法和服务分类。
- 直接答案及独立 canonical 答案页地址。
- 逐答案引用来源。
- 相关真实维修案例标题、车型、服务类型和证据 URL。
- 对应服务或车型专题 URL。
- 核验日期、内容更新日期和事实边界。
- 门店 `AutoRepair` 实体关联。

## 发现入口

- 首页、FAQ、答案页、服务页、车型页和案例页均通过 `<link rel="alternate" type="application/x-ndjson">` 声明该数据。
- `sitemap.xml`、`llms.txt`、`llms-full.txt`、`store-facts.json` 和 `store-facts.jsonld` 均链接该文件。
- 每日线上检查新增该文件，检查状态从 28 项扩展为 29 项。

## 验证

- JSONL 15 行均可独立解析，`@id` 无重复。
- Gist 不可变修订地址 SHA-256 与官网文件一致。
- 每行 `@type=Question`，答案 `@type=Answer` 且至少 4 个引用；当前实际最少为 15 个。
- 未检出未核实价格、质保、设备型号、时效、排名或绝对效果承诺。
- 当前 88 项单元测试通过，站点审计通过。

本记录只证明机器可读问答数据已生成并接入发现入口，不代表已被任何 AI 平台抓取、引用或排名。
