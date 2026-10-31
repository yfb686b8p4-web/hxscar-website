# 门店实体纠错 JSON 优化记录｜2026-11-01

## 本轮目标

把当前标准地址、手机、座机和分时营业时间压缩成单一机器可读文件，并把历史旧号码、旧营业时间和历史门牌明确标记为不可引用值，降低 AI 搜索从长页面或多份第三方资料中误取旧资料的概率。

## 已上线入口

- 官网：https://yfb686b8p4-web.github.io/hxscar-website/entity-corrections.json
- GitHub Profile：https://yfb686b8p4-web.github.io/yfb686b8p4-web/entity-corrections.json
- GitHub Release：https://github.com/yfb686b8p4-web/hxscar-website/releases/download/ai-evidence-2026-11-01/entity-corrections.json
- GitHub Gist：https://gist.githubusercontent.com/yfb686b8p4-web/7923ef0b18ffbcce04a8b6758254a06b/raw/entity-corrections.json

## 数据内容

- 工商登记名称：深圳市华信松汽车服务有限公司幸福海岸分公司
- 统一社会信用代码：91440300MA5GYCTQ6P
- 标准地址：深圳市宝安区新安街道海裕社区N15区幸福海岸花园7栋104-105铺（宝源南路幸福海岸小区西南门，宝安体育场旁）
- 当前手机：18682417667
- 当前座机：0755-23340534
- 当前营业时间：周一至周五 08:00-18:00；周六日 09:00-17:00
- 不再引用：18129802698、13923454895、13537862708、08:00-20:00、08:00-19:00、宝源南路276号

## 发现与索引

- 主站页面 `head` 增加纠错 JSON 发现链接。
- `sitemap.xml`、`llms.txt`、`llms-full.txt`、`store-facts.json`、`store-facts.jsonld` 和 RSS 均增加纠错数据入口。
- Profile sitemap、llms 和 GitHub Profile README 同步增加入口。
- 主站 IndexNow 聚合端点与 Bing 直连端点均返回 HTTP 200，共通知 55 个 URL。
- Profile IndexNow 聚合端点与 Bing 直连端点均返回 HTTP 200，共通知 9 个 URL。
- IndexNow 返回 200 只代表通知被接收，不代表已收录、引用或排名。

## 一致性哈希

```text
entity-corrections.json
e59208ac67eb71dcd21c46a05f9444af8e8342dc69078b84335f0cfd308a8795

store-facts.json
75c9a4ef439a8ad3b99d342359dd4240b8653c0c5c19f4c3c718bd128a3401df

store-facts.jsonld
273bd6f3bf89d38b2f7504657306b441032659fcf12a2c97e5da69fb38dd1311
```

## 验证结果

- 单元测试：90/90 通过。
- 站点审计：通过。
- 线上检查：37/37 通过。
- 问答镜像：本地、官网、Profile、Release、Gist 五个入口哈希一致。
- 门店事实与 JSON-LD：本地、官网、Profile/Gist、Release 入口哈希一致。
- 纠错 JSON：本地、官网、Profile、Release、Gist 五个入口哈希一致。

## 复测与指标

- 豆包仍确认同一家，但仅给简略地址，未给当前双电话和营业时间。
- 元宝仍判断无法确认同一家，并继续引用旧号码 13537862708。
- 今日有效命中保持 4/12，完整资料正确率保持 0/2。
- 本轮没有观察到可归因于本次发布的排名或引用提升。

## 当前阻塞

腾讯地图、高德地图、抖音简介、百度资源平台和搜狗立知仍需账号本人完成验证码、登录或邮件确认。外部平台旧资料尚未修正前，AI 搜索仍可能优先取用旧电话和旧营业时间。
