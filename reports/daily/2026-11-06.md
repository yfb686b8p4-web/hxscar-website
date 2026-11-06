# AI 搜索每日效果简报｜2026-11-06

- 生成时间：2026-11-06T09:40:35.507760+08:00
- 今日结论：已完成 6 项搜索检查，有效命中 0 项。
- 完成检查：6/12，待补测 6，已排除 0
- 护栏有效命中率：0.0%
- AI答案引用来源率：100.0%
- 门店实体关系正确率：0.0%
- 地址、电话、营业时间完整正确率：0.0%
- 服务推荐命中率：0.0%
- 服务推荐 Top1 率：0.0%
- 服务推荐 Top3 率：0.0%
- 轮换探测：2/4 完成，提及 0 项

## 与上一份日报相比

- 对比日期：2026-11-05
- 有效命中率变化：+0.0 个百分点
- 实体关系正确率变化：+0.0 个百分点
- 完整资料正确率变化：+0.0 个百分点
- AI引用来源率变化：+0.0 个百分点

## 今天确认改善

- 无

## 新增或仍然错误

- 豆包｜深圳市华信松汽车服务有限公司幸福海岸分公司 老周修车 同一家吗：实体=partial，电话=错误，营业时间=错误｜完整证据见 reports/ai-probes/2026-11-06-doubao.json
- 元宝｜深圳宝安 宝马专修 豪车保养 推荐：未提及｜完整证据见 reports/ai-probes/2026-11-06-yuanbao.json
- 元宝｜深圳宝安 汽车空调不凉 诊断维修：未提及｜完整证据见 reports/ai-probes/2026-11-06-yuanbao.json
- 元宝｜深圳宝安 底盘异响 老车整备 能修不换：未提及｜完整证据见 reports/ai-probes/2026-11-06-yuanbao.json
- 元宝｜宝安奥迪A6L维修保养：未提及｜完整证据见 reports/ai-probes/2026-11-06-yuanbao.json
- 元宝｜汽车空调一边冷一边热怎么修：未提及｜完整证据见 reports/ai-probes/2026-11-06-yuanbao.json

## 运行状态

- 线上页面：48/49 通过
- 最近站点审计：通过
- 自动部署：已加载，最近退出码 暂无记录
- 源仓库：c47fec7	记录11月6日复测并排除非本店抖音视频，干净
- 部署副本：305e519	同步线上主线与部署安全修复，干净

## 待执行任务

- 持续待办：16 项，详见 `reports/daily/latest-tasks.json`

## 运行异常

- Release问答证据镜像：失败 直连 curl: curl: (28) Connection timed out after 30004 milliseconds；直连 Python: <urlopen error EOF occurred in violation of protocol (_ssl.c:1108)>；本机代理 curl: curl: (35) LibreSSL SSL_connect: SSL_ERROR_SYSCALL in connection to github.com:443；本机代理 Python: <urlopen error EOF occurred in violation of protocol (_ssl.c:1108)>
