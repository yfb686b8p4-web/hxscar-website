# AI 搜索每日效果简报｜2026-11-09

- 生成时间：2026-11-09T09:42:19.516696+08:00
- 今日结论：已完成 5 项搜索检查，有效命中 0 项。
- 完成检查：5/12，待补测 7，已排除 0
- 护栏有效命中率：0.0%
- AI答案引用来源率：100.0%
- 门店实体关系正确率：0.0%
- 地址、电话、营业时间完整正确率：0.0%
- 服务推荐命中率：0.0%
- 服务推荐 Top1 率：0.0%
- 服务推荐 Top3 率：0.0%
- 轮换探测：1/4 完成，提及 0 项

## 与上一份日报相比

- 对比日期：2026-11-08
- 有效命中率变化：+0.0 个百分点
- 实体关系正确率变化：+0.0 个百分点
- 完整资料正确率变化：+0.0 个百分点
- AI引用来源率变化：+0.0 个百分点

## 今天确认改善

- 无

## 新增或仍然错误

- 元宝｜深圳市华信松汽车服务有限公司幸福海岸分公司 老周修车 同一家吗：实体=partial，电话=错误，营业时间=错误｜完整证据见 reports/ai-probes/2026-11-09-yuanbao.json
- 元宝｜深圳宝安 宝马专修 豪车保养 推荐：未提及｜完整证据见 reports/ai-probes/2026-11-09-yuanbao.json
- 元宝｜深圳宝安 汽车空调不凉 诊断维修：未提及｜完整证据见 reports/ai-probes/2026-11-09-yuanbao.json
- 元宝｜深圳宝安 底盘异响 老车整备 能修不换：未提及｜完整证据见 reports/ai-probes/2026-11-09-yuanbao.json
- 元宝｜老车底盘整备 品牌件 原厂件 拆车件：未提及｜完整证据见 reports/ai-probes/2026-11-09-yuanbao.json

## 运行状态

- 线上页面：47/49 通过
- 最近站点审计：通过
- 自动部署：已加载，最近退出码 1
- 源仓库：f39cf71	记录11月9日复测与额度状态，干净
- 部署副本：305e519	同步线上主线与部署安全修复，干净

## 待执行任务

- 持续待办：17 项，详见 `reports/daily/latest-tasks.json`
已延后关闭：service-底盘异响诊断（对应检查尚未完成）

## 运行异常

- Release问答证据镜像：失败 直连 curl: curl: (28) Connection timed out after 30006 milliseconds；直连 Python: <urlopen error EOF occurred in violation of protocol (_ssl.c:1108)>；本机代理 curl: curl: (35) LibreSSL SSL_connect: SSL_ERROR_SYSCALL in connection to github.com:443；本机代理 Python: <urlopen error EOF occurred in violation of protocol (_ssl.c:1108)>
- Release门店历史资料纠正：失败 直连 curl: curl: (28) Connection timed out after 30005 milliseconds；直连 Python: <urlopen error EOF occurred in violation of protocol (_ssl.c:1108)>；本机代理 curl: curl: (35) LibreSSL SSL_connect: SSL_ERROR_SYSCALL in connection to github.com:443；本机代理 Python: <urlopen error EOF occurred in violation of protocol (_ssl.c:1108)>
