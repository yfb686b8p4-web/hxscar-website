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
