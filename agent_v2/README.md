# Agent v2 最小闭环

这是新的残差证书控制器。按用户后续要求，旧 Agent、旧 workflow、旧完整流程适配和历史验收代码全部不再使用。当前复用的是独立 `solve_core.py` 数学核心和项目固定的 Lean 工具链，没有改写数学算法。

本轮实现范围是状态管理、增量候选图、每轮一个动作、独立局部检查、严格受限的原题验收、失败恢复和留档。**尚未实现一般 Train 原题到局部 CAS 输入的形式化前端，也没有接通通用 LLM 自动证明。**

## 运行

在项目根目录运行：

```bash
python3 -m unittest discover -s agent_v2/tests -v
python3 -m agent_v2.cli --help

python3 -m agent_v2.cli core-demo \
  --input finite_product_framework/p1/examples/core_qgosper.json \
  --seconds 30 --output-root agent_v2/generated

python3 -m agent_v2.cli run \
  --identity FQI-SRC-AP-3.3.9 --method telescoping \
  --selector rule --max-steps 1 --seconds 30 \
  --output-root agent_v2/generated

python3 -m agent_v2.cli resume --run-dir agent_v2/generated/实际运行目录
```

每次新运行建立独立目录。CLI 的 `resume` 只接收固定 Train 清单绑定的正式状态，不能用于无原命题的 `core-demo`。断点恢复不自动追加预算。

| 退出码 | 含义 |
| --- | --- |
| 0 | 原命题经最终严格验收通过，或 `--help` 正常结束 |
| 2 | 数学证明尚未完成；参数语法错误也由 argparse 返回 2，诊断文本可区分 |
| 3 | 环境接口缺失或预算耗尽 |
| 4 | 数据契约、文件完整性或路径校验拒绝 |

任何非零退出码都不表示原命题为假。

## 两种演示的含义

`core-demo` 实际调用独立 q-Gosper 核心，保存完整返回和实际成本。输入没有原始 Lean 定理，所以它是**非形式化适配器探针**：没有伪造的 G、Gamma 或空 O。符号 `constructed` 只映射为 `symbolic_constructed`；C 不增加，原题证明状态为 false。

`run` 从固定 Train 清单读取所选原声明，核验原哈希并冻结快照，建立原目标义务和方法出口。按照放弃旧 Agent 的最新要求，已取消附件中的旧完整流程调用；新的方法边界在缺少形式化前端时明确返回 `formal_frontend_unavailable`。它不会偷偷恢复旧 `prove_*`、借用历史证明或换一道题。

## 状态和正确性

`ResidualState` 保存不可变 G/Gamma、当前表示 r、已验成果 C、开放义务 O 和剩余预算 b。所有契约使用版本化 JSON；拒绝未知字段、错误类型和枚举，并冻结嵌套对象。

`executor.validate_invariant` 从原目标重建证明依赖树。初始树就是原目标自身：若证明这个义务，即可得到原命题。每次替换义务，必须有实际通过 Lean 的连接定理，其类型精确为 `子义务₁ → … → 父义务`。依赖树的开放叶子必须恰好等于 O；不允许用诊断文字充当形式义务。

局部检查拒绝候选时，原义务保持开放。连接错误会回滚 r/O/连接变更，同时保留可独立验证的成果。O 为空后，还要从已验依赖组装证明并调用独立原题验收；拒绝或异常都会重开原目标，不能输出证明成功。

当前新的 `LeanChecker` 只支持闭合的 Init 命题和受限纯证明项，使用固定 Lean 执行实际类型与公理审计；默认不导入 Benchmark 或 Mathlib。原题接口仅接受精确的 Init 单定理模板，绑定原文件、快照、定理名、类型和原上下文。一般 Train 声明不在支持范围内，明确拒绝，绝不降格成局部命题验收。

## Graph 和选择

Graph 节点保存具体表示实例，转换边和方法出口保存契约、条件、来源及历史。它是候选搜索空间，不能充当证明证据。无新结构时保留原对象；`expand()` 当前没有自动数学变换生成器，无扩展时返回 false。

确定性过滤先检查表示、域、索引、源绑定、已验桥、预算、已尝试动作和禁用适配器。非 identity 转换仅接受已验证、语义匹配的闭合命题蕴含桥。规则选择器随后选择一个动作；执行结束后使用新状态重新选择。图保留原节点，因此失败后的下一次选择可以回到其他已认证节点，不存在固定的回退层数。

Jev 只有经校验的可注入协议，没有外部服务调用；无效 ID、低置信度或异常会回退到规则选择。LLM 默认禁用，Library 默认查询为空。测试中的替身位于 `tests/`，CLI 固定使用生产适配器和真实检查器。

## 存储与恢复

每轮保存 `state_before.json`、候选列表、动作、原始后端返回、标准化结果、验证结果和 `state_after.json`。CAS 和 Lean 使用独立子目录；`run.json` 给出终止原因，`graph.json` 保存图和失败历史。

断点以内容寻址文件加原子 manifest 作为提交记录；`checkpoint.json` 是展示副本。动作执行前记录在途状态并预留预算，崩溃后不会盲目重跑。恢复时核验源文件、依赖和产物哈希，并实际重验保存的局部证明；新证据替换旧收据。失败恢复和最终验收同样消耗真实墙钟预算。

路径守卫拒绝 Test 路径、越界产物及产物符号链接。本轮没有读取 Test、修改历史成绩、运行全 Train 或调用模型 API。进程清理机制负责超时和子进程回收，不是任意不可信代码的操作系统沙箱。

## 文件职责

| 文件 | 职责 |
| --- | --- |
| `models.py`、`storage.py` | 严格不可变契约、Train 快照、原子存储 |
| `graph.py`、`router.py` | 增量图、合法候选、规则与 Jev 边界 |
| `executor.py` | 单动作适配、C/O 更新、可重建不变量、证明组装 |
| `loop.py`、`recovery.py` | 循环、恢复、重复抑制、停止原因 |
| `cas_adapter.py`、`process.py` | 独立数学核心、超时及后代进程清理 |
| `lean_checker.py`、`lean/PartialCheck.lean` | 新局部验证和独立原题验收 |
| `llm_adapter.py` | 禁用的 LLM 和空 Library 边界 |
| `cli.py` | 固定生产入口、Train 绑定与退出码 |

下一阶段应先实现保留原域与上下文的形式化前端，以及至少一种 CAS 证书到 Lean 局部命题的真实桥接，再扩展 Graph 和生成式选择。当前测试不能解释为数学方法成功率提升。
