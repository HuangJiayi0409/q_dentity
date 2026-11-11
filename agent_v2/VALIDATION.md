# Agent v2 本轮交付与验证

本轮交付独立的残差证书 MVP。用户后续指令“凡是涉及旧 Agent 的代码都遗弃”优先于附件中的旧流程复用建议：没有恢复、导入或调用旧 Agent/workflow/完整证明入口。旧 `finite_product_framework/agent/` 目录仍为空。

**最终新包测试：67/67 通过，退出码 0，28.398 秒。** 原始日志见 [final_tests.log](generated/validation/final_tests.log)，命令与退出码见 [commands.json](generated/validation/commands.json)。

## 实际命令与结果

以下命令均从项目根目录执行。最终含 Lean 的验证在宿主运行；首次沙箱中的超时结果保留在下文，不混入成功结果。

| 命令 | 退出码 | 实际结果 |
| --- | --- | --- |
| `python3 -m unittest discover -s agent_v2/tests -v` | 0 | 67 项通过，含行为测试、真实进程/CAS 和真实 Lean 正负例 |
| `python3 -m agent_v2.cli --help` | 0 | core-demo、run、resume 入口可用 |
| `python3 -m agent_v2.cli core-demo --input finite_product_framework/p1/examples/core_qgosper.json --seconds 30 --output-root agent_v2/generated` | 2 | `symbolic_constructed`，最终 `incomplete / translation_pending` |
| `python3 -m agent_v2.cli run --identity FQI-SRC-AP-3.3.9 --method telescoping --selector rule --max-steps 1 --seconds 30 --output-root agent_v2/generated` | 3 | `environment_blocked / formal_frontend_unavailable`；C=0，原义务开放 |
| `python3 -m agent_v2.tests.real_smoke` | 0 | 测试用合成题两动作闭环，实际 Lean 局部与原题检查通过 |

## 演示证据

### A：真实局部符号构造

[运行目录](generated/20261111T122204Z-bca43f3b82/)

固定 q-Gosper 输入仅运行一次，实际适配器成本 **0.777703 秒**。核心原始状态为 `constructed`，`benchmark_files_read=0`，`original_identity_proved=false`。全部 18 个核心源文件哈希又与当前源码核对一致。

由于输入不含原始 Lean 定理，本例明确记录为非形式化探针；没有伪造 G/Gamma、空 O 或已验证 C。符号证书原样留档，但没有把它升级成 Lean 证明。

### B：指定 Train 原题的一次新框架动作

[运行目录](generated/20261111T123343Z-61d918ffb4/)

原题固定为 `FQI-SRC-AP-3.3.9`，绑定 `FiniteQBenchmark.Identity272.statement`，原源码 SHA-256 为 `d9a88ffda89d1bbb38da774ac9f30bba41b11674e6057b698c11d0407dc26efa`。

执行一次新方法边界检查，成本 **0.041721 秒**，返回 `formal_frontend_unavailable`。未执行完整数学证明流程、未调用原题 Lean 验收；没有换题、借历史证明或恢复旧入口。C 为空，O 保留 `original`，源文件、快照、运行时代码哈希与条件不变量均已另行核对。

这里的阻塞是新形式化前端和证明桥尚未实现，不是 Lean 工具链缺失，也不是原命题为假。

### 补充：真实 Lean 的两动作合成闭环

[运行目录](generated/20261111T123400Z-c7048f15ab/)

这是**测试用人工候选提供器 + 真实 LeanChecker**，不是模型效果或 Train 成绩。原命题为 `Synthetic.statement : True`。

| 阶段 | 实际局部内容 | C | O |
| --- | --- | --- | --- |
| 初始 | 原目标 | 空 | original |
| 第 1 动作 | Lean 验证 `fun h => h : True → True`，建立连接 | bridge | leaf |
| 第 2 动作 | Lean 验证 `True.intro : True` | bridge、leaf_proof | 空 |
| 最终验收 | 组装两项证明，再按精确原声明检查 | 两项保留 | 空；原题验收通过 |

两轮成本分别为 5.203420 秒、5.183531 秒；最终验收另有实际记录。每次都是重新选路后执行一个动作。两个局部证书和最终定理的公理列表均为空。

独立产物复核通过：原声明/快照、两轮不变量、C 的证明项绑定、所有局部与最终产物哈希；两个局部检查各自记录的 5,213 项标准工具链依赖均重新核验。结果见 [evidence_audit.json](generated/validation/evidence_audit.json)。

## 测试边界

67 项中有 50 项状态、存储、图、路由、执行、恢复、CLI 和适配器测试，以及 17 项 LeanChecker 测试。行为测试会在验证或数学构造边界注入替身；进程清理、指定的独立 CAS 小输入，以及 Lean 正负例使用真实程序。

伪造进程输出、篡改依赖、越界符号链接等故障注入只用于证明拒绝逻辑有效，不能解释为真实 Lean 曾接受伪证。生产 CLI 没有假检查器或测试候选提供器开关。补充合成闭环代码单独位于 `tests/real_smoke.py`。

覆盖附件要求的 13 类行为，包括 G/Gamma 固定、候选不自动进 C、CAS 构造不等于证明、原题终验、图保留和局部增加、过滤先于选择、单动作重新选路、C/O 同时存在、不变量回滚、去重/预算、终验重开、Test 路径拒绝、假证据/错误定理/禁用公理/哈希/路径拒绝。

## 关键实现位置

- `executor.validate_invariant`：以真实已验连接和开放叶子重建条件证明关系，拒绝循环、缺依赖、错连接和伪造空 O。
- `executor.verify_and_update`：候选逐个检查后进入 C；只有匹配连接才能改 O；无效状态更新回滚，保留独立已验成果。
- `executor.assemble_term` 与 `loop._final`：按证书依赖组装，独立验收原题；异常或拒绝重开原目标。
- `loop.run`：每轮只调用一次 executor；失败后重新筛选和选择。
- `models.action_fingerprint`、`state_fingerprint`：以数学状态和动作参数去重；扣预算、改动作展示 ID、更新重验收据都不能解锁盲重试。
- `storage.RunStore` 与 `loop.resume`：内容寻址的原子提交、源/依赖/产物复核、实际 Lean 重验、新收据替换、失败仍扣成本。
- `lean_checker.py`、`lean/PartialCheck.lean`：新受限纯证明语言、精确定理与类型、公理白名单、真实加载模块和工具链/运行库路径的前后校验。

## 本轮新增文件

生产模块共 13 个：`__init__.py`、`models.py`、`storage.py`、`graph.py`、`router.py`、`executor.py`、`cas_adapter.py`、`process.py`、`llm_adapter.py`、`lean_checker.py`、`recovery.py`、`loop.py`、`cli.py`；另有 `lean/PartialCheck.lean`。

测试文件：`test_models_storage.py`、`test_graph_router.py`、`test_executor.py`、`test_loop.py`、`test_adapters.py`、`test_cli.py`、`test_lean_checker.py`、`real_smoke.py`，均在 `agent_v2/tests/`。

文档：本文件、`README.md`、`PROGRESS.md`，以及根目录下的 `docs/superpowers/plans/2026-11-11-agent-v2-mvp.md`。运行产物均在 `agent_v2/generated/`。

没有可用 Git 元数据，因此未建立分支或提交。基线记录中的现有文件哈希保持不变，独立核心 18 个源文件哈希亦复核通过；没有编辑旧数学算法。[基线核对](generated/baseline/current_check.json)和[新模块导入审计](generated/baseline/new_imports.json)已保存。

## 开发失败与修复记录

首次完整开发测试运行了 55 项，退出 1：五个真实 Lean 断言因 20 秒超时失败，涉及四个测试方法，其中一个有两个子例。它不是最终验证。诊断与迁移说明保留在 `generated/lean_diagnostics/`；改为固定单线程、缩小可信标准导入并准确冻结实际依赖后，最终 67 项通过。

独立审查发现的断点提交中断、恢复失败不扣预算、终验异常遗漏重开、后续检查异常丢失独立成果、工具链依赖漂移、产物符号链接越界等问题均先复现再修复，并纳入回归。恢复收据更新造成重复动作重新开放的问题也已修复。

## 当前限制与停止点

- 新形式化前端、一般 Train 证明桥和完整原题求解出口尚未实现，B 如实阻塞。
- 原题检查只支持规范 Init 单定理模板；局部检查限闭合命题、受限证明语法和自包含证明项，不接受任意外部引理依赖。
- Graph 提供增量存储与过滤；没有自动生成数学变换的扩图器。只执行已经验证的、语义匹配的闭合蕴含转换。
- 默认规则选择器；Jev 仅协议，LLM 禁用，Library 为空。未接模型 API、未跑批测、未读取 Test、未改历史成绩。
- 进程及工具链完整性检查针对当前 Linux 固定工具链，不提供执行任意不可信代码的通用沙箱。

本轮到此停止。下一阶段的必要工作是原题上下文/原域保持的形式化前端和一种真实 CAS→Lean 局部证书桥接；不应把当前骨架验证视为解题率提升。
