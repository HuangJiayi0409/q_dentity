# 2026-11-11 代码审查修复

已修复四项实际问题，并先复现失败再验证修复。旧 Agent 仍不使用；本轮没有读取 Test、调用模型 API、修改数学算法或回填历史成绩。

| 问题 | 修复 |
| --- | --- |
| identity 可跳到其他根可达节点 | 只允许 `source == target == state.r`；非恒等动作只取当前节点直接出边。Executor 和状态更新入口也检查来源，不能跳过中间转换；返回旧节点需要真实回边。 |
| 无可承担动作归为普通未完成 | 主循环使用 `recovery.classify_stop` 的统一分类；预算、重复尝试、输入契约、图能力、环境分别给出终态或停止原因。保留 `stop_reason` 的兼容状态接口，二者共用同一分类逻辑。 |
| 终验完整性错误被降级 | 保留 `integrity_error`、`budget_exhausted`、`environment_blocked` 及失败代码；对应异常也正确分类。证据错绑、源变化、损坏返回都不能记录为普通未完成，失败仍重开原义务并扣成本。 |
| 自定义输出目录无法恢复 | `run --output-root` 和 `resume --run-dir` 均支持默认树外的显式目录；保留路径、Train 身份、原声明、快照、依赖和断点校验。 |

交叉审查还补齐了相关边界：重复动作关联实际匹配的历史尝试而非全局最后失败；不可序列化的终验回包能保存完整性错误终态；恢复前先守卫 Train 清单路径再读取；终验迟到的成功结果记录为墙钟预算耗尽。

## 验证

```bash
python3 -m unittest discover -s agent_v2/tests -v
python3 -m agent_v2.tests.real_smoke
```

- 完整套件 **100/100 通过**，退出码 0，29.462 秒；相对原版 67 项新增 33 项回归。
- 真实 Lean 合成闭环退出码 0，完成两次单动作和独立原题终验。候选提供器是明确标注的人工测试夹具，不计作模型效果或 Train 成绩。
- 自定义目录测试使用临时合成 Train 仓库，实际经过 CLI、RunStore、循环和恢复校验；符号链接负例在读取 Test 路径字节前被阻止，没有读取真实 Test。
- 独立复查覆盖当前来源、回边、混合过滤原因、异常分类、终态保存和自定义目录安全边界。

[完整测试日志](generated/review_fixes_20261111/final_tests.log)、[验证摘要](generated/review_fixes_20261111/validation.json)、[当前源码哈希](generated/review_fixes_20261111/source_hashes.json)随补丁保留。

修复前副本、差异及新合成运行的完整证据留在开发环境 `agent_v2/generated/review_fixes_20261111/` 和 `agent_v2/generated/20261111T132031Z-bbb7b62156/`；本次发布保留上述摘要和测试日志。旧运行绑定旧代码哈希，更新代码后应新建运行，不能绕过完整性检查强行续跑。

原有限制仍然有效：一般 Train 形式化前端未实现，LLM 默认禁用，Graph 不自动生成新数学变换；本轮没有新增“切换当前工作节点”操作。
