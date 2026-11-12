# 自主 CLI／恢复／调用计数交叉复审

复审读取当前 `autonomous.py`、`autonomous_adapter.py`、`autonomous_cli.py`、`loop.py`、图去重逻辑、Source 验证及模型客户端。没有读取真实凭据，没有发起新的 live 请求。期间主任务已把主循环更新为绝对截止时间，本报告不把旧的 verify/persist 漏扣作为现存问题。

本轮证实并按主任务授权修复的事项：

1. 数学库来源未完整加入 Source.dependencies。原先只冻结所选方法依赖及两份元数据 JSON，product 独有运行缺少 Auxiliary、Gaussian、GaussianRules，determinant/coefficient 独有运行缺少 GaussianRules。已补共同四份基础文件、project manifest/toolchain/lakefile、每条库声明的来源文件与哈希以及实际 Lean binary。读取返回记录时先比较当前哈希；恢复时 Source 验证会拒绝后续来源漂移。严格 Lean 检查此前仍会拦截错误证明；此项解决的是初始依赖冻结与可复现性缺口。
2. `_unsupported(..., reason=setup_budget_exhausted)` 原来统一返回 incomplete，查库耗尽总预算也返回 environment_blocked。现按实际共享剩余预算区分 budget_exhausted 与环境阻塞，未把缺依赖改报成数学失败。
3. 模型实际调用计数原来在 remaining<=0 检查前递增。纯离线探针观察到 transport=0、model_calls=1；现把递增放到截止时间检查后、紧邻传输。新增回归证实相同本地超时场景 transport=0、model_calls=0、calls_used=0。此前的 `task2_review_counter_probe.json` 保留为修复前证据。
4. 符号入口适用不保证 LocalLeanChecker 有可验证的原题 Source profile。现初始化先调用固定 checker._bound；对于明确不支持的原题形式环境，返回 incomplete/formal_source_translation_unavailable，先于查库和模型客户端构造。其他完整性异常仍拒绝，不被掩盖成不适用。

恢复检查结果：配置、能力与库元数据哈希都绑定在原 Source 中；任务需逐个通过 LocalTask 内容哈希及 Source 完整相等检查；模型/Jev/扩展/修复计数都有边界；completed_methods 中证书必须属于当前 C。随后旧 loop.resume 重新验证 Source、证书及链接。保守调用预留通过 snapshot 的 max(actual,reserved) 提交；恢复把保存值装入客户端 calls_used，预留字段归零，不释放已经占用的额度。

另用完全离线的初始化夹具写入 inflight 模型动作，再经过实际 autonomous_cli.resume_run 和 loop.resume，观察到 model_calls 恢复为 1、动作预算只扣一次、预留归零、原中断动作因相同 fingerprint 被排除；见 `task2_review_inflight_probe.json`。该探针没有真实模型结果和 Lean 成功声明。对于尚未提交的模型响应或局部验收产物，恢复采用保守去重，不会把未提交材料自动写入 C；本轮未宣称恢复了这些未提交证明。

最终相关回归命令：

```text
python3 -m unittest agent_v2.tests.test_model_client agent_v2.tests.test_jev_client agent_v2.tests.test_autonomous_cli -v
```

40 项通过，0.684 秒。数学库真实 Lean 类型检查已有前序独立记录；本轮最小改动未改变库类型查询实现。完整仓库回归及冻结后真实 Train 验收由主任务统一执行，不能从本报告外推自主解题率。
