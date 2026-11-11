# 第一阶段验收：真实 Train 差分／望远镜局部闭环

本阶段完成附件允许的**结果 A：局部成功**。对唯一选定的真实 Train 题，生产 CLI 实际调用 q-Gosper，生成局部 Lean 候选，重新编译并审计后将一条证书加入 C；原题仍留在 O，最终状态为 `incomplete`。恢复重新编译该证书，错误证明实际交给 Lean 后被拒绝。**原命题未通过最终验收，不能计作整题成功或成功率提升。**

## 选题与原始声明

- ID：`FQI-SRC-AP-3.3.9`，Gaussian 加权 hockey-stick 求和。
- 原文件：`benchmark/lean/Benchmark/Statements/Train/Identity272.lean`。
- SHA-256：`d9a88ffda89d1bbb38da774ac9f30bba41b11674e6057b698c11d0407dc26efa`。
- 仅求解这一题。`FQI-FINITE-Q-BINOMIAL` 仅用于真实 Train 结构不匹配测试，没有求解。

原定理的完整声明和有效上下文如下。原文件中的占位 `sorry` 不会导入候选环境，也没有被当作证明使用。

```lean
import Benchmark.Batch3Proofs

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

namespace FiniteQBenchmark.Identity272
variable {K : Type*} [Field K]
attribute [local instance] Classical.propDecidable

theorem statement (q : K) (m n : ℕ)
 (h_domain : True) :
 (gaussian q (n+m+1) (m+1)) =
   (∑ j ∈ Finset.range (n+1), ((q^j) * (gaussian q (m+j) (m)))) := by
  sorry

end FiniteQBenchmark.Identity272
```

原域是任意 universe 的 `Field K`，`q : K`，`m,n : ℕ`，保留 `h_domain : True`。求和指标为自然数 `j`，范围为 `Finset.range (n+1)`。没有额外的 `q ≠ 0`、非单位根或正则性假设。

此题适合现有方法，因为求和项在通用符号域的移位比是有理函数：

```text
F(j) = q^j * gaussian q (m+j) m
X ↔ q^j，a ↔ q^(m+1)
F(j+1)/F(j) 的通用搜索表示 = q*(1-a*X)/(1-q*X)
```

正式运行中，真实 q-Gosper 返回 `constructed`，耗时约 0.348 秒，证书为 `(X-1)/(X*a-X)`。回译器安全解析实际回包，核对请求哈希、移位比和 `V(X)R(qX)-R(X)-1=0`，再在 Gaussian 邻接下标表示中得到无除法通量 `G(j)=gaussian q (m+j) (m+1)`。通用有理函数计算的分母不能直接特化至原域；原域有效性由下一步 Lean 独立证明。

## 实际通过 Lean 的精确局部命题

```lean
∀ {K : Type u} [Field K] (q : K) (m : ℕ) (n : ℕ)
    (h_domain : True) (j : ℕ),
  FiniteQBenchmark.gaussian q (m + (j + 1)) (m + 1) -
    FiniteQBenchmark.gaussian q (m + j) (m + 1) =
  q ^ j * FiniteQBenchmark.gaussian q (m + j) m
```

它证明 `G(j+1)-G(j)=F(j)`，使用现有 `FiniteQP1.gaussian_pascal`，在 Lean 中证明下标对齐、自然数减法消去，再做环正规化。原参数 `n` 和假设 `h_domain` 即使局部证明不使用，也完整保留。

每次验证重新编译 `Benchmark.Definitions`、`Benchmark.Auxiliary`、`Benchmark.Gaussian` 和含 Gaussian 基础规则的候选；候选不能指定 import。固定检查环境中没有原题 Statements 模块。正式验收的导入闭包为 2,879 个模块，固定外部依赖清单为 14,401 个文件；核对真实搜索路径的对象、分片、源码和前后哈希。公理审计仅出现 `propext`、`Classical.choice`、`Quot.sound`，保留 `universe u`。

固定工具链经 Mathlib 导入 `Std.Http.Test.Helpers`；它属于 Lean 标准库 HTTP 设施，不是 benchmark 留出 Test。仅对固定工具链中这一模块族作精确路径处理并显式记录，benchmark Test 与工具链外同名路径仍在读取前拒绝。

## 残差与 Graph 的实际变化

| 项目 | 动作前 | 动作后／恢复后 |
| --- | --- | --- |
| 当前表示 r | original | original |
| 联合动作 | — | `T=identity, M=CAS, method=telescoping` |
| C | 0 条 | 1 条真实 Lean 验证的局部差分证书 |
| O | 原题 original | 原题 original，保持开放 |
| 证明连接 | 空 | 空；没有未经验证的父子替换 |
| 最终状态 | running | incomplete |
| 原题验收 | 未执行 | 未执行，`original_identity_proved=false` |

Graph 只有原表示与方法出口，没有为展示添加转换边。来源检查与 identity 不移动表示的约束保持有效。每轮只执行一个动作。

还缺：把逐项差分提升为原有限范围求和的连接，零端点与末端点证明，以及原命题的组装和独立终验。这些是日志中的后续工作说明；尚无已验证连接，故不伪造额外形式子义务，O 仍为原题。C 非空不代表原题已接近完成。

## 实际执行与结果

修改前基线：100 项通过，29.690 秒。最终完整套件：**144 项，144 通过，0 失败，0 跳过，115.037 秒，退出码 0**；新增 44 项。没有删除、跳过或放宽旧测试。完整套件覆盖前端、回译、状态、旧身份／预算／完整性／恢复检查及真实 Lean 集成；故障注入测试明确标记，不算真实 Lean 成功。

```bash
python3 -m unittest discover -s agent_v2/tests -v
python3 -m agent_v2.tests.telescoping_smoke
```

第二条验收脚本实际执行了以下生产命令：

```bash
/usr/bin/python3 -m agent_v2.cli run \
  --identity FQI-SRC-AP-3.3.9 --method telescoping \
  --selector rule --max-steps 1 --seconds 600.0 \
  --output-root /home/hjy/Project/finite_q_identity_catalog/agent_v2/generated/telescoping_phase1_20261111/acceptance/runs

/usr/bin/python3 -m agent_v2.cli resume \
  --run-dir /home/hjy/Project/finite_q_identity_catalog/agent_v2/generated/telescoping_phase1_20261111/acceptance/runs/20261111T140718Z-09ef07d547
```

两条 CLI 均返回 2，即预期的 `incomplete`，不是进程异常；分别约 44.612 秒和 43.339 秒。单动作记录的成本约 44.357 秒，动作预算扣除 1。恢复比对旧外部环境摘要后仍重新编译，生成了新的候选文件、审计 nonce 和收据，没有重跑 CAS。CLI 准备与进程启动开销不等于单动作成本，因此同时保留命令墙钟和动作成本。

验收脚本随后把同一个局部命题的证明改成 `by rfl`，调用生产 `LeanChecker.check_partial`；它确实到达 Lean 并以非零编译退出码、`incomplete / lean_check_failed` 被拒绝。该独立负例不修改正式运行状态。脚本整体退出码 0，另核对三次检查的 77 项本地产物哈希；这些脚本步骤不重复计入 144 项测试总数。

## 修改文件及职责

| 文件 | 职责 |
| --- | --- |
| `formal_frontend.py` | 完整消费的窄语法、类型与结构匹配；完整上下文、范围、AST、哈希和语义映射 |
| `telescoping_translation.py` | 安全解析实际 CAS 有理式，检查残差，选择无除法通量，生成独立局部候选 |
| `cas_adapter.py` | 生产 MethodAdapter 接通前端、真实 CoreAdapter、回译及逐层留档 |
| `lean_checker.py` | 保留 Init 路径，按冻结 Source 选择受控数学配置 |
| `math_lean_profile.py`、`lean/TelescopingCheck.lean` | 固定依赖重编译、独立预期类型、多态／公理审计、实际导入路径与环境摘要 |
| `executor.py` | 验证时提供完整原 Source，沿用事务性 C/O 与连接不变量 |
| `loop.py` | 局部能力范围完成时诚实停止；恢复重验、错误分类与完整失败收据 |
| `cli.py` | 固定数学源与配置依赖、真实 Train 前端绑定、恢复退出类别 |
| 新增五个 `test_*.py` 与 `tests/telescoping_smoke.py` | 前端、回译、真实 Lean、控制器／方法回归和生产 CLI 验收 |
| `README.md`、`PROGRESS.md`、本说明与实施计划 | 当前用法、边界、变更和验收记录 |

独立审阅的两项 Important 均已复现修复：恢复错误分类丢失，以及高优先级目录中的同名 Lean 对象绕过冻结清单。最终审阅无未解决 Critical／Important。32 个源码、测试与驱动文件在最终验证前后哈希一致。

## 支持范围与尚未完成部分

前端支持当前完整声明布局下，任意 Field、一个基变量、两个自然数参数和一个 True 假设的 Gaussian 加权前缀和结构；允许受检查的变量改名及等式方向。识别不依赖题目 ID，所有源码 token 都必须被支持语法消费。

不支持任意 Lean 语法、额外假设、其他参数域、一般范围、类型转换或其他求和权重。未知结构返回 `not_applicable`，损坏绑定返回完整性错误；符号构造有结果但不满足当前回译范围时为 `translation_pending`，C 不增加。

本阶段没有完整有限求和连接、端点出口、一般 Train 原题终验、自动扩图、其他十一种 CAS、LLM、Jev 或网络调用。附件列举的 `finite_product_framework/prove_telescoping.py` 当前不存在；未恢复旧入口或旧 Agent/workflow，复用现存 `solve_core.py` 数学核心和基础引理。

## 证据位置与复现

本地证据根目录：`agent_v2/generated/telescoping_phase1_20261111/`。

- `validation.json`、`final_tests.log`、`final_smoke.log`、`final_source_hashes.json`：最终摘要、完整测试及源码冻结。
- `acceptance/acceptance.json`、`cli_run.json`、`cli_resume.json`：真实验收和准确命令。
- `acceptance/runs/20261111T140718Z-09ef07d547/`：原题快照、Graph、候选动作、前端／映射／CAS 请求与回包、Lean 源与日志、检查结果、前后状态、恢复结果、负例与成本。
- `before/`、各 `*_red.log`／`*_green.log`、`review_final.diff`：修改前副本、开发失败和审阅修复证据。

这些普通运行产物保留在本地 generated，不批量提交；本说明是筛选后的验收记录。重新执行验收脚本须用新的 `--output-root`，避免覆盖证据。断点绑定当前运行时、数学源码、配置及外部环境；更新代码或依赖后不应强行恢复旧断点。
