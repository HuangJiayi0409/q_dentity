# 自主流程验证（2026-11-12）

本轮为预选小样本集成验证，不是全 Train 成功率实验。原题、原假设与 Lean 最终验收标准不变；未读取 benchmark Test、未导入历史解题证明、未恢复旧 Agent。

## 已完成的真实运行

| Train 题目 | 实际路径 | 生成模型请求 | 结果 |
|---|---|---:|---|
| FQI-SRC-AP-3.3.9 | CAS 局部差分 → 暂停 → 恢复重验 → 模型连接证明 → 原题终验 | 2 | 完整通过 |
| FQI-GAUSS-ALTERNATING | CAS 局部递推 → 模型局部证明及反馈修订 → 原题终验 | 3 | 完整通过 |
| FQI-FINITE-Q-BINOMIAL | 多方法候选 → Jev/规则选择 → CAS → 模型分解 → Graph 子目标导航 | 8 | 留下两个开放子目标 |

首题第一份模型返回缺少协议字段，随后一次受控修复成功。生成证明由现场 HTTP 模型响应提供，主控未补写证明项。该题另经独立 `accept_original` 重新编译通过；独立审计确认 81 个冻结运行时文件前后无漂移，旧证据文件没有被修改。

第三题实际调用 Jev 4 次，其中两次按置信度采用、两次低置信度回退。已验证的分解桥引入两个子目标，随后实际执行 `decomposition` 和 `focus_obligation` 边；桥通过不等于整题通过。冻结版第一轮把“模型调用额度已耗尽且路线同时重复”的停止原因记作 `incomplete/repeated_actions_exhausted`。最终版已修正为 `budget_exhausted/model_call_limit`，新增回归先复现失败再通过；旧日志保持原样。

另一个受控现场检查成功完成了相反方向：模型现场生成 `局部差分命题 → 原题` 的连接，Lean 通过后加入子节点，正常规则路由沿真实 `decomposition` 边执行望远镜 CAS，闭合子目标，再验收原题。共 1 次模型请求、2 个动作；主控没有提供证明项。首个 LLM 动作和目标结构由测试指定，所以这验证 Graph→CAS 接线，不计作自主策略效果。

## 证据位置

统一目录：`agent_v2/generated/autonomous_20261112/`。

- 预选题单：`train_preregistration.json`。
- 运行时冻结：`final_revision_01/source_manifest.json`，共 81 个 Python/Lean 文件。
- 首题：`final_revision_01/live_hockey/20261112T055221Z-05ffaad720/`。
- 递推题：`final_revision_01/live_recurrence/20261112T055819Z-d489a737b9/`。
- Jev 多方法题：`final_revision_01/live_multi_method/20261112T055459Z-062bba8130/`。
- 最终版受控 Graph→CAS：`final_revision_02/live_controlled_expansion/20261112T060938Z-aeac5e776a/controlled_expansion_report.json`。
- 首题独立验收：首题目录的 `independent_audit/` 与 `math_probe/live_hockey_audit.*`。

每个运行目录的 `run.json` 是总结果；`rounds/*/model/` 保存请求响应，`rounds/*/verification.json` 保存实际 Lean 验收，`graph.json` 与内容寻址 checkpoint 保存实际状态。此前配置预检的网络拒绝、HTTP 403/401 与凭据更新后的成功检查均保留，不计作 Train 模型解题。

有一次启动工具报告“派发前中止”，但进程实际已经启动；后来启动的重复运行 `20261112T055756Z-1e4da7f531` 已显式中断，退出 130，并写入 `excluded_duplicate.json`。其额外请求与局部证据保留，未混入上表。

## 边界与独立审阅

控制流程测试中的模拟模型与检查器只验证契约和状态更新，不计数学证明或模型效果。真实 Lean 反例覆盖：改变目标、添加原题假设、注入命令、调用未批准公理、篡改证书与依赖、恢复重验失败。

独立审阅发现的共同墙钟漏扣、执行前预算耗尽分类、标准数学 AST 节点缺失、Library 依赖冻结与实际 HTTP 次数计数问题，均先复现再修正。审阅记录见 `math_probe/runtime_review.md`、`math_probe/local_security_review.md`、`task2_independent_review.md`。

## 回归与版本对应

- 第一份冻结运行时完成整套 **553 项测试**，全部通过，958.963 秒；日志 `final_revision_01/unittest.log`。包含最终 Lean 驱动的混合 CAS/生成证明 Train 验收。
- 最终版与该冻结版仅 `autonomous.py` 一处停止分类条件不同。修正后 **66 项定向测试**全部通过，1.876 秒；日志 `final_revision_02/targeted_unittest.log`。两组测试有重叠，不相加为独立测试总数。
- 最终版冻结 81 个运行时文件，并完成上述真实 Graph→CAS→原题验收。第一版证明仍归属其原冻结版本，没有冒称经过新源码重跑。
- 完整修改清单、前后源码和补丁分别保存在 `changed_files.json`、`before/`、`after/`、`changes.diff`；汇总见 `final_validation.json`。

复现方式见 `agent_v2/AUTONOMOUS.md`。现有数学结构范围、有限声明库和纯 tactic 白名单仍是明确限制；上述结果不代表一般 Train 题都能证明。
