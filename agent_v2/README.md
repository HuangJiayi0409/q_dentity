# Agent v2 最小闭环

这是新的残差证书控制器。按用户后续要求，旧 Agent、旧 workflow 控制层、旧完整流程适配和历史验收代码不再使用。当前复用独立数学核心和项目固定 Lean 工具链。矩阵方法显式共享仍保留的 `finite_product_framework/workflow/matrix_symbolic.py` 纯计算辅助模块；它只有标量/矩阵序列化和残差核对，不运行旧框架控制流程。

第一阶段完整收尾见 [TELESCOPING_CLOSURE.md](TELESCOPING_CLOSURE.md)。原始真实 Train 差分局部闭环见 [TELESCOPING_PHASE1.md](TELESCOPING_PHASE1.md)。此前四项修复记录见 [REVIEW_FIXES.md](REVIEW_FIXES.md)，原始 MVP 验证记录保留在 `VALIDATION.md`。

望远镜方法支持一种窄结构的真实 Train 前端：任意 Field 上、范围为 `range(n+1)` 的 `q^j * gaussian q (m+j) m` 求和。它调用真实 q-Gosper 核心，将受支持的符号候选回译为无除法局部差分命题，经真实 Lean 检查后加入 C。显式 `--scope full` 会再执行有限求和连接及两个端点任务，并独立验收原题。默认 `--scope local` 仍只产生局部证书。一般 Train 前端与通用 LLM 自动证明尚未实现。

递推方法支持交替权重 Gaussian 有限和。它使用本次 q-Zeilberger 二阶证书，独立检查有理残差，再用现有纯数学生成器和固定 Lean 环境验证闭合有限和递推。通过后 C 增加、原题 O 保留；目标右端递推、两个初值及唯一性连接尚未接通。其余方法的真实等级和结构限制由 `methods` 命令列出。

## 运行

在项目根目录运行：

```bash
python3 -m unittest discover -s agent_v2/tests -v
python3 -m agent_v2.cli --help
python3 -m agent_v2.cli methods

python3 -m agent_v2.cli core-demo \
  --input finite_product_framework/p1/examples/core_qgosper.json \
  --seconds 30 --output-root agent_v2/generated

python3 -m agent_v2.cli run \
  --identity FQI-SRC-AP-3.3.9 --method telescoping \
  --selector rule --max-steps 1 --seconds 600 \
  --output-root agent_v2/generated

python3 -m agent_v2.cli resume --run-dir agent_v2/generated/实际运行目录

# 独立验收：真实 Train CLI、恢复重验和错误证明负例
python3 -m agent_v2.tests.telescoping_smoke
python3 -m agent_v2.tests.closure_smoke
python3 -m agent_v2.tests.recurrence_smoke
```

每次新运行建立独立目录。`--output-root` 可指定默认目录之外的位置，恢复时将该次运行目录传给 `resume --run-dir` 即可；路径仍拒绝 Test、符号链接和父路径穿越。CLI 的 `resume` 只接收固定 Train 清单绑定的正式状态，不能用于无原命题的 `core-demo`。断点恢复不自动追加预算。

| 退出码 | 含义 |
| --- | --- |
| 0 | 原命题经最终严格验收通过，或 `--help` 正常结束 |
| 2 | 数学证明尚未完成；参数语法错误也由 argparse 返回 2，诊断文本可区分 |
| 3 | 环境接口缺失或预算耗尽 |
| 4 | 数据契约、文件完整性或路径校验拒绝 |

任何非零退出码都不表示原命题为假。

## 两种演示的含义

`core-demo` 实际调用独立 q-Gosper 核心，保存完整返回和实际成本。输入没有原始 Lean 定理，所以它是**非形式化适配器探针**：没有伪造的 G、Gamma 或空 O。符号 `constructed` 只映射为 `symbolic_constructed`；C 不增加，原题证明状态为 false。

`run` 从固定 Train 清单读取所选原声明，核验哈希并冻结快照。前端完整匹配受支持语法、类型、binder 和有限范围，保存原 Lean 对象与 CAS 对象的映射；不匹配的数学结构返回 `not_applicable`。形式化输入缺失或 Init-only 输入保留 `formal_frontend_unavailable` 边界。`constructed` 只是符号候选；无法回译时记录 `translation_pending` 且 C 不增加。局部模式通过真实 Lean 后报告 `partial_lean_verified`，原题仍开放；完整模式逐轮建立连接、关闭端点，再重新编译原 theorem。

## 状态和正确性

`ResidualState` 保存不可变 G/Gamma、当前表示 r、已验成果 C、开放义务 O 和剩余预算 b。所有契约使用版本化 JSON；拒绝未知字段、错误类型和枚举，并冻结嵌套对象。

`executor.validate_invariant` 从原目标重建证明依赖树。初始树就是原目标自身：若证明这个义务，即可得到原命题。每次替换义务，必须有实际通过 Lean 的连接定理，其类型精确为 `子义务₁ → … → 父义务`。依赖树的开放叶子必须恰好等于 O；不允许用诊断文字充当形式义务。

局部检查拒绝候选时，原义务保持开放。连接错误会回滚 r/O/连接变更，同时保留可独立验证的成果。O 为空后，还要从已验依赖组装证明并调用独立原题验收；拒绝或异常都会重开原目标，不能输出证明成功。

`LeanChecker` 保留原有 Init 检查路径，并新增受控望远镜检查配置。该配置从冻结源独立重算预期局部命题，保留任意 universe 的 Field 参数及全部原假设，只加载固定基础数学依赖，重新编译基础模块和候选，核对实际导入闭包、源码、编译产物和公理。候选不能指定 import 或任意 tactic；不导入原题 Statements 模块。终验除 Init 模板外，还支持该 Gaussian 结构族的完整原声明。它从实际证明树重建自包含项，保留原始参数、宇宙及等式方向，再独立编译和审计。

## Graph 和选择

Graph 节点保存具体表示实例，转换边和方法出口保存契约、条件、来源及历史。它是候选搜索空间，不能充当证明证据。无新结构时保留原对象；`expand()` 当前没有自动数学变换生成器，无扩展时返回 false。

确定性过滤先检查表示、域、索引、源绑定、已验桥、预算、已尝试动作和禁用适配器。所有动作从当前 `r` 出发：identity 必须满足 `source == target == r`；非恒等动作只能走当前节点的直接出边，并使用已验证、语义匹配的闭合命题蕴含桥。规则选择器随后选择一个动作；执行结束后使用新状态重新选择。图保留其他节点，但返回这些节点需要真实转换路径；当前没有独立的“切换工作节点”操作。

Jev 只有经校验的可注入协议，没有外部服务调用；无效 ID、低置信度或异常会回退到规则选择。LLM 默认禁用，Library 默认查询为空。测试中的替身位于 `tests/`，CLI 固定使用生产适配器和真实检查器。

## 存储与恢复

每轮保存 `state_before.json`、候选列表、动作、原始后端返回、标准化结果、验证结果和 `state_after.json`。CAS 和 Lean 使用独立子目录；`run.json` 给出终止原因，`graph.json` 保存图和失败历史。

断点以内容寻址文件加原子 manifest 作为提交记录；`checkpoint.json` 是展示副本。动作执行前记录在途状态并预留预算，崩溃后不会盲目重跑。恢复时核验源文件、依赖和产物哈希，并实际重验保存的局部证明；新证据替换旧收据。失败恢复和最终验收同样消耗真实墙钟预算。代码更新后，绑定旧运行时哈希的断点会拒绝恢复，需新建运行。

无合法路线时统一区分不可承担的预算、重复尝试、输入契约不匹配、Graph 能力缺口和环境不可用。最终验收保留 `integrity_error`、`budget_exhausted`、`environment_blocked` 类别及具体原因，并在失败时重开原义务；哈希或证据绑定错误不会降级成普通 `incomplete`。

路径守卫拒绝 Test 路径、越界产物及产物符号链接。本轮没有读取 Test、修改历史成绩、运行全 Train 或调用模型 API。进程清理机制负责超时和子进程回收，不是任意不可信代码的操作系统沙箱。

## 文件职责

| 文件 | 职责 |
| --- | --- |
| `models.py`、`storage.py` | 严格不可变契约、Train 快照、原子存储 |
| `graph.py`、`router.py` | 增量图、合法候选、规则与 Jev 边界 |
| `executor.py` | 单动作适配、C/O 更新、可重建不变量、证明组装 |
| `loop.py`、`recovery.py` | 循环、恢复、重复抑制、停止原因 |
| `cas_adapter.py`、`process.py` | 独立数学核心、超时及后代进程清理 |
| `formal_frontend.py`、`telescoping_translation.py` | 窄结构类型化前端、CAS 映射、无除法局部证书回译 |
| `lean_checker.py`、`lean/PartialCheck.lean` | 新局部验证和独立原题验收 |
| `math_lean_profile.py`、`lean/TelescopingCheck.lean` | 真实 Train 局部命题的固定依赖编译与多态公理审计 |
| `llm_adapter.py` | 禁用的 LLM 和空 Library 边界 |
| `cli.py` | 固定生产入口、Train 绑定与退出码 |

方法声明与实际能力由 `method_registry.py` 管理，CLI `methods` 显示版本、契约、能力等级和限制；注册本身不授权证明。完整求和闭环的单题成功不表示全 Train 成功率改善。自动扩图和网络模型调用仍未启用。

## 显式符号请求

`method-demo --method <方法> --input <请求.json>` 运行注册方法的独立符号核心，输入契约为 `{"schema_version":1,"method":"方法ID","input":{...}}`。各方法有各自的严格类型与资源限额。结果只表示本次符号构造，不创建虚假的形式状态、证明树或可恢复原题断点；C 始终为空。L0 方法明确报告 `capability_unavailable`。

L2 方法只接受显式导出的 `core_request`，没有自动 Train 源码导出器。正式 `run --identity` 会在不适配时拒绝建立出口；调用者已经明确提供的 core_request 可经 Graph/Executor 执行，但其数学含义尚不能替换原题义务。方法注册、候选规则列表和 CAS 的 `constructed` 都不能充当证明。
