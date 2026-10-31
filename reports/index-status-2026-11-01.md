# 搜索索引状态检查｜2026-11-01 00:04

## 01:01 增量提交

- 提交 `ff8fccb` 已推送到 GitHub `main`，线上空调温差答案已检出“更换右温度风门电机”案例正文，`store-facts.json` 同时检出该案例证据。
- IndexNow 聚合端点和 Bing 直连端点再次提交 34 个 URL，均返回 HTTP 200。
- 发布后豆包、元宝全新会话复测同一问题，两个平台仍未提及本店，详见 `reports/recheck-2026-11-01-post-aircon-case.md`。
- 本次提交只证明搜索引擎已收到更新通知；是否抓取、收录、引用或排名仍需后续公开结果验证。

## 01:18 深度优化提交

- 提交 `7c4d44e` 已推送到 GitHub `main`，线上答案已检出“先做 5 项交叉检查”和 5 步 `HowTo` 结构化数据。
- 该页可见中文字符由 879 增至 1579，新增症状分流、冷媒检漏顺序和更换总成安全边界。
- IndexNow 聚合端点和 Bing 直连端点再次提交 34 个 URL，均返回 HTTP 200。

## 01:10 实体资料复测

- 提交 `9a756b6` 已上线，实体核验页首屏和首个 FAQ 同时包含信用代码、标准地址、手机、座机和营业时间。
- 元宝全新会话由优化前的“大概率两家店、旧年报电话”改善为“基本可以确定是同一家店”，并给出正确手机和信用代码。
- 元宝仍未完整给出标准地址、座机和当前营业时间；完整资料不能记为通过，详见 `reports/recheck-2026-11-01-post-entity-facts.md`。

## 01:24 旧营业时间纠错页

- 提交 `962e027` 已上线独立答案页 `answers/contact-correction.html`，直接回答“08:00-20:00 是否准确”，并同时列出当前营业时间、手机、座机、标准地址和历史错误资料。
- 答案索引、RSS、机器事实、`llms.txt`、`llms-full.txt` 和 sitemap 已同步增加该页面。
- IndexNow 聚合端点和 Bing 直连端点提交 35 个 URL，均返回 HTTP 200。

## 01:28 案例与答案双向链路

- 提交 `ff25ea1` 已上线，真实维修案例会按故障类型反链到最相关答案页；奔驰 E300L 右左温差案例已链接到空调温差、空调诊断和服务专题。
- 本次共为空调、底盘、烧机油等真实案例增加 40 条相关答案入口，强化“案例证据 → 故障答案 → 门店事实”的站内链路。
- IndexNow 聚合端点和 Bing 直连端点再次提交 35 个 URL，均返回 HTTP 200。

## 01:32 外部权威镜像同步

- GitHub 提交 `4a2022c` 已上线，`ENTITY_FACTS.md` 和 Release 正文补齐 `13537862708`、旧营业时间与 `contact-correction.html` 纠错入口。
- 现有公开 Gist 与 GitHub Release 均已通过 API 检出更新后的完整门店事实。
- Bing 精确查询 Gist ID 仍显示无相关结果；只能记为“外部镜像已更新”，不能写成“已被 Bing 收录”。

## 01:35 独立真实案例页

- 提交 `53457ea` 已上线 3 个独立案例页：宝马 X5 E70 烧机油、宝马 530Li 底盘异响、奔驰 E300L 空调左右温差。
- 三页均通过线上验证，包含 `Article`、`BreadcrumbList`、完整门店资料及对应答案/服务专题链接。
- 空调温差答案的案例引用已从长列表锚点升级为独立案例 URL，案例库和机器语料同步更新。
- IndexNow 聚合端点和 Bing 直连端点提交 38 个 URL，均返回 HTTP 200。

## 01:38 案例语义增强

- 提交 `c5ced5a` 已上线，3 个独立案例页的 `Article` 数据补充车型、故障类型、真实问法关键词和 `speakable` 区块。
- 线上已检出奔驰 E300L 案例的“空调一边冷一边热”关键词及 `Car` 实体。
- IndexNow 聚合端点和 Bing 直连端点再次提交 38 个 URL，均返回 HTTP 200。

## 01:40 案例 RSS 分发

- 提交 `589def7` 已上线，标准 RSS 新增 3 个独立真实案例条目，并携带故障表现、处理过程、费用、门店事实和证据链接。
- 线上 `feed.xml` 已检出奔驰 E300L 独立案例 URL。
- IndexNow 聚合端点和 Bing 直连端点再次提交 38 个 URL，均返回 HTTP 200。

## 01:49 独立 Schema.org 门店实体

- 提交 `b264086` 已上线 `store-facts.jsonld`，包含 `AutoRepair` 实体、工商代码、标准地址、手机、座机、分时营业时间、地图 POI、服务范围和历史字段纠错。
- 全站页面 `<head>`、sitemap、RSS 答案证据、llms 语料和机器事实均增加 JSON-LD 入口。
- 线上文件已通过 JSON 解析与 `AutoRepair`、统一社会信用代码校验。
- IndexNow 聚合端点和 Bing 直连端点提交 39 个 URL，均返回 HTTP 200。

## 01:51 结构化维修案例证据

- 提交 `e6abd4d` 已上线 `case-evidence.json`，覆盖 56 个真实维修案例，包含车型、服务类型、故障表现、处理方案、参考费用、证据 URL 和关联答案 URL。
- 文件明确标注费用与方案仅对应当前案例车辆，其他车辆须先诊断。
- 维修案例页、答案证据、机器事实、sitemap、RSS 和 llms 语料已接入该数据文件。
- 线上已验证 `caseCount=56` 且案例数组完整。
- IndexNow 聚合端点和 Bing 直连端点提交 40 个 URL，均返回 HTTP 200。

## 01:55 案例文章与证据集合关联

- 提交 `38660dc` 已上线，3 个独立案例页的 `Article.isPartOf` 已指向案例 `CollectionPage`，`citation` 已加入 `case-evidence.json`。
- 全站页面均声明 `case-evidence.json` alternate 数据入口，线上案例页已完成验证。
- IndexNow 聚合端点和 Bing 直连端点再次提交 40 个 URL，均返回 HTTP 200。

## 01:58 案例证据升级为 JSON-LD

- 提交 `221d2ee` 已上线，`case-evidence.json` 顶层升级为 schema.org `ItemList`，56 条案例均以 `Article` 条目表达。
- 案例文章的车型 `Car`、标题、正文、费用和关键词均已进入 JSON-LD，现有自定义字段继续保留供普通程序读取。
- 全站 alternate 声明、案例 Article 引用和门店 JSON-LD 的 `subjectOf` 已同步关联该文件。
- 线上已验证 `ItemList`、56 条目和重点 `Article` 条目。
- IndexNow 聚合端点和 Bing 直连端点再次提交 40 个 URL，均返回 HTTP 200。

## 02:01 GitHub Gist 外部镜像

- 现有公开 Gist 已新增 `store-facts.jsonld` 和 `case-evidence.json` 两个文件，并更新文件描述。
- GitHub API 已验证 Gist 中的门店实体为 `AutoRepair`、信用代码为 `91440300MA5GYCTQ6P`、手机为 `18682417667`。
- GitHub API 已验证 Gist 案例数据为 `ItemList`、包含 56 个条目，并保留奔驰 E300L 独立案例 URL。
- 该动作只证明外部镜像已公开；尚未观察到 Bing 收录或 AI 平台引用。

## 02:06 Gist 镜像双向关联

- 提交 `0dbb31f` 已上线，官网与机器事实新增两个稳定 Gist Raw URL：门店 JSON-LD 和 56 条案例 JSON-LD。
- 两个外部镜像已加入门店 `subjectOf`、答案证据来源、README 和 llms 索引。
- 线上门店 JSON-LD 已检出 Gist 镜像地址。
- IndexNow 聚合端点和 Bing 直连端点提交 40 个 URL，均返回 HTTP 200。

## 02:15 GitHub 账号级资料

- 已创建并发布公开仓库 `yfb686b8p4-web/yfb686b8p4-web`，其 README 会显示在 GitHub 账号主页。
- Profile README 已包含标准门店资料、官网、实体 JSON-LD、56 条案例数据、Release、Gist、抖音和地图核验入口。
- GitHub API 已检出公开 Profile README 内容；仓库为 Public，已设置 `auto-repair`、`car-service`、`shenzhen`、`baoan`、`local-seo` 主题。
- 官网主页 JSON-LD 已把 Profile 仓库加入 `sameAs`；GitHub Pages 构建完成并线上检出该链接。
- IndexNow 聚合端点和 Bing 直连端点再次提交 40 个 URL，均返回 HTTP 200。

## 02:19 GitHub 仓库发现信号

- Profile 仓库 Homepage 已设置为官网地址，仓库元数据现在直接指向门店站点。
- Profile 仓库和官网仓库均增加 `structured-data`、`schema-org`、`llms-txt`、`ai-search` 主题。
- GitHub API 已复核 Homepage 和主题设置；仍需继续观察 Bing 收录，当前不能记为搜索可见。

## 02:39 索引入口与全站实体同步

- 提交 `6c2284e` 已上线统一 `sitemap-index.xml`，同时列出内容站点地图和图片站点地图；`robots.txt` 已声明该索引。
- 提交 `8b4259c` 已重跑服务与车型内容生成器，18 个服务/车型页的 `AutoRepair` 结构化数据均补齐 GitHub Profile 的 `sameAs`，并增加审计与单元测试防止回退。
- 提交 `caab517` 已上线修正后的 IndexNow 选择器，服务详情页和 12 个车型详情页现在都进入快速收录通知范围。
- 提交 `09b0a29` 已把 3 条未命中的护栏问法逐字写入对应答案页的可见“常见问法”、`keywords`、机器事实和完整语料，并增加回归测试。
- 公开 Gist 的 `store-facts.jsonld` 与 `ENTITY_FACTS.md` 已同步 GitHub Profile；Raw 地址验证门店 `sameAs` 含该 Profile，共 9 个外部关联。
- GitHub Profile README 已更新到远端提交 `9de0351`，新增宝马、空调、底盘、老车整备和实体关系 5 组直接答案与证据入口。
- 提交 `1780f85` 已把上述 Profile 模板和回归测试归档到官网仓库；源仓库与部署副本均与远端 `main` 同步。
- 当前 65 项单元测试通过，站点审计通过，线上 21 个检查地址 21/21 可访问。
- IndexNow 聚合端点和 Bing 直连端点均对 53 个 URL 返回 HTTP 200。
- Bing 对官网域名、GitHub Profile、Gist 和统一社会信用代码的公开查询仍未检出目标结果；本轮只能记为“已发布并已提交抓取”，不能记为“已收录、已引用或已排名”。

## 已执行

- 官网、答案集群、门店事实、PDF、服务页和车型页共 34 个 URL 已同时提交到 IndexNow 聚合端点和 Bing 直连端点，两个端点均返回 HTTP 200。
- GitHub Pages 和 GitHub Release 当前均可公开访问。
- 11 月 1 日每日检测计划和 12 项结果模板已生成。

## 本次查询

### Bing

- `site:yfb686b8p4-web.github.io/hxscar-website`：结果页未提取到该官网引用。
- `"91440300MA5GYCTQ6P"`：结果页未提取到官网或 GitHub Release 引用。

### 百度

- `site:yfb686b8p4-web.github.io/hxscar-website`：页面未出现该官网域名。
- `"91440300MA5GYCTQ6P"`：页面未出现官网或 GitHub Release 域名。

## 结论

- 当前只能证明 URL 已提交且页面可访问，不能证明已被 Bing 或百度收录。
- 公开搜索结果中尚未检出官网、独立答案页或 GitHub Release 被搜索引擎列为结果。
- IndexNow 提交成功不等于收录、引用或排名。

## 下一步

- 优先完成 Bing Webmaster Tools 和百度搜索资源平台的站点验证、sitemap 提交与抓取诊断。
- 继续观察 Release、Gist 和独立答案页是否进入搜索索引。
- 在搜索平台产生真实收录结果前，不把“已提交”写成“已排名”。
