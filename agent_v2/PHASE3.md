# 第三阶段：递推整题闭环与逐方法扩展

当前实施依据为用户提供的《Codex_第三阶段_十二种CAS全方法真实接入提示词》。本文件随验收更新；不得将尚未验收的 C/D 目标解释为现有能力。

## A/B 当前状态

A/B 停止门已通过（`generated/phase3_20261112/ab_gate.json`）。固定真实 Train `FQI-GAUSS-ALTERNATING` 已完成五份候选和原题独立验收；正式 CLI 多阶段恢复、负例与全新完整回归均通过。

- theorem：`FiniteQBenchmark.Identity009.statement`。
- 原文件 SHA-256：`c49f5a4417e3d4d19df4463a377c4d3117cea07619d1867156eccb454ca8123c`。
- 参数域保留任意 Field，没有增加 `q ≠ 0` 等假设。
- 真实 q-Zeilberger 局部递推系数为 `[Q*q-1, 0, 1]`；局部证书 ID 从本次实际 witness 派生。
- 唯一性连接以已验证的局部递推为依赖，把原题换成右端递推、初值 0、初值 1 三个精确命题。
- 每动作至多一个待验候选，只有生产 LeanChecker 通过后才进入 C 或修改 O。

| 阶段 | C | O | ProofLink | 原题已证 |
| --- | ---: | --- | ---: | --- |
| 初始 | 0 | 原题 | 0 | 否 |
| 局部递推通过 | 1 | 原题 | 0 | 否 |
| 唯一性连接通过 | 2 | 右端递推、初值 0、初值 1 | 1 | 否 |
| 三个叶子分别通过 | 5 | 空 | 4 | 否 |
| 原 theorem 独立验收 | 5 | 空 | 4 | 是 |

右端证明保留自然数模／除法的奇偶语义，使用 Pochhammer 步进；唯一性使用强归纳并实际调用两个初值。连接尚未获批时，未验证的三个子义务不能替换原题。没有建立额外的证明成功出口。

## 公共核验与兼容

`proof_profiles.py` 只注册真实实现的配置。Source 多重适配会拒绝歧义，不按第一个匹配选取。partial、resume 和 original 共享候选重建与证据绑定；依赖只允许使用已按拓扑检查的前驱。

绑定项目包含证书 ID、profile/version、源 SHA、完整 proposition、受控证明、精确依赖、保留请求、Lean 源与编译产物、进程结果、实际 stdout 中的公理／导入审计和外部环境摘要。恢复实际重新编译候选，不能仅凭保存的 accepted 标志通过。

MacMahon 的原题实际只使用 `ℂ`，没有宇宙参数。为此新增固定 `MonomorphicCheck.lean`，同时要求候选及重建目标的宇宙参数为空；只有对应的完整 Source 配置可选择此驱动。旧两个多态驱动逐字节不变，旧 profile 默认仍要求 `u`；原题审计允许同数量的 Lean 自动命名，但数量必须为整数且名单无重复。实时与恢复收据共享固定配置的宇宙检查。这是受控单态扩展，不允许把原泛型域特化为 `Type 0`。

为保留既有独立局部检查接口，唯一旧别名 `telescoping_local` 仍可在精确源／类型／模板、无依赖的条件下使用；它不能代替完整望远镜连接所需的源派生证书 ID。未知或任意改名的 ID 不具有这一兼容例外。

独立审阅发现并修复了双驱动环境比较问题：旧实现分别登记局部与原题审计驱动，造成合法终验摘要不同。现在两类事务共同冻结两个驱动，保留逐文件哈希与严格比较。失败轮和修复后的新运行分别保留，没有合并或覆盖。

## 复现入口与证据

```bash
python3 -m unittest discover -s agent_v2/tests -v
python3 -m agent_v2.tests.recurrence_closure_smoke \
  --output-root agent_v2/generated/新的递推验收目录 --seconds 4000
python3 -m agent_v2.tests.closure_smoke \
  --output-root agent_v2/generated/新的望远镜验收目录 --seconds 2400
```

总证据根目录：`agent_v2/generated/phase3_20261112/`。包含原始源码 before、开发失败、修复前后冻结源码、真实候选／日志／状态、前置门及逐方法验收记录。公共 profile 子任务的开发日志另保留于项目根 `phase3_20261112/profile_tests/`，最终索引会明确引用。

新基线完整运行为 216 项通过，0 skip；这不是第三阶段最终测试数。修复后的预注册真实原题通过记录位于 `preregistration/runs/20261111T170918Z-defa1eb4ea/summary.json`，使用当时 `ab_fixed_source` 冻结源码。它证明数学出口真实存在，不代替后续正式 CLI、恢复和负例验收。

A/B 最终新进程回归为 258/258、0 skip、524.030 秒；递推分阶段检查包含 17 次真实证书重验、5 个实际 Lean 负例和原题独立检查。默认 CLI 兼容修复另经实际五动作及恢复验收。该计数属于 A/B 冻结版本，不是持续扩展后的第三阶段最终全套结果。

## C：六种方法已完成局部闭环，谱方法有明确缺口

系数法已在真实 Train `FQI-FINITE-Q-BINOMIAL`（`FiniteQBenchmark.Identity005.statement`，源 SHA-256 为 `4963bc05a9be240c2bcf2a3b74efad216ea9678eeb596f0067c3dd3b54f95108`）上通过 Source → 实际保留符号核心 → 独立整系数多项式核对 → 生产 LeanChecker → 恢复重验。

局部证书将原题右端 Pochhammer 表示为多项式的求值，证明乘入下一个仿射因子时零次系数和全部自然数后继指标的系数递推。Lean 中先证明有限 Cauchy 卷积的范围及仿射因子的零次、一次和高次零系数；实际 CAS 对提取后的两个环等式进行正规化。没有抽样指标，也没有增加非零或特征假设。Gaussian 系数公式和原恒等式仍未证明。

- 注册版本：`coefficient 2.0`，`capability_level=L3`、`local_lean=true`、`full_original=false`。
- 正式证书：`coefficient-local-77c50a6d3792f663bb99001e`。
- 残差状态：`C=1`、`O={original}`、`links=[]`、`original_identity_proved=false`。
- 正式验收包含一次局部 Lean 正例、一次全新恢复重验、一次实际错误 Lean 证明拒绝，以及真实 Train 不匹配和源绑定篡改检查。
- 最终相关兼容回归 54/54、0 skip；旧 30 个测试源文件哈希不变。此数与 A/B 套件有重叠，不相加作为独立测试总数。
- 无 Source 的 standalone/core-request 仍属于本次执行能力 L2，另外记录方法注册能力 L3，禁止导出正式 C/O。

验收卡与门记录：`generated/phase3_20261112/coefficient_review/acceptance_card.json`、`coefficient_gate.json`。正式运行及日志：`generated/phase3_20261112/coefficient/acceptance_final/`。验收后只增加 core-request 禁止 C/O 的两行保护，Source/Lean 路径不变；该差分和两个版本哈希单独保留。

插值法已在真实 Train `FQI-SRC-GR2-I-20`（`FiniteQBenchmark.Identity233.statement`，源 SHA-256 为 `92276ebe09255e6ae64ff0491b5fbe8a0bff7bee22a68fa56fb84fb478560a3c`）上完成同样的局部闭环。实际 `zero_certificate` 核心对参数多项式给出次数至多 1、节点 0 和 1 的证书；独立代码检查次数、变量、节点、残差和多项式绑定。Lean 真实使用次数界和两个互异零点推出多项式相等，再代入原参数并证明整数指数转自然数指数及幂次合并。

原题的 `regular q`、`k ≤ n`、`a ≠ 0`、分母非零假设和全部参数保持不变；局部命题覆盖所有 `j < n-k` 的尾段因子。只完成逐因子关系，乘积组装、商式连接和原恒等式仍开放。

- 注册版本：`interpolation 2.0`，`capability_level=L3`、`local_lean=true`、`full_original=false`。
- 正式证书：`interpolation-local-e04cfa302db775ecaeef8012`。
- 状态仍为 `C=1`、`O={original}`、`links=[]`、`original_identity_proved=false`。
- 正式局部正例、全新恢复重验、实际错误 Lean 证明各一次，另有绑定篡改和真实 Train 不匹配拒绝；正式 smoke 核对 99 个产物哈希。
- 独立定向审阅测试 55/55、0 skip，旧 30 个测试文件不变；不与其他有重叠的套件累加。
- 验收卡与门记录：`generated/phase3_20261112/interpolation/acceptance_card.json`、`gate.json`；最终运行在同目录的 `acceptance_final/`。

行列式法已在真实 Train `FQI-SRC-AP-11.2.4`（`FiniteQBenchmark.Identity284.statement`，源 SHA-256 为 `86d3a48107e99eeb5321582fddd12cf698e4b820445c8d38ad9cfe8c77589bb1`）上完成局部闭环。原维数 `k`、全部参数及 `Fin k` 索引保留，局部命题对任意两行、两列的选择量化，证明实际源矩阵的二阶子式展开。整数强制转换、整数除法、`.toNat` 和 `gaussianInt` 指标按原式保留。

实际保留核心返回 LU 分解与无除法 Berkowitz 构造；只有无除法结果进入翻译，并由独立的两项 Leibniz 展开核对。Lean 以 `Matrix.det_fin_two` 验证原矩阵所选子式，不增加主元非零、行列互异或特征条件，也不把原维数设为 2。共享的有界多项式解析器只是检查基础设施，没有调用系数法求解核心。任意维数整行列式及 `planePi` 原题仍开放。

- 注册版本：`determinant 2.0`，`capability_level=L3`、`local_lean=true`、`full_original=false`。
- 正式证书：`determinant-local-18cb4a91ea2b4215a60cb6cf`。
- 状态为 `C=1`、`O={original}`、`links=[]`、`original_identity_proved=false`。
- 正式局部正例、全新恢复重验、实际错误 Lean 证明各一次；另有绑定篡改和真实 Train 不匹配拒绝，84 个产物哈希核对通过。
- 独立定向审阅测试 61/61、登记后相关回归 36/36，均 0 skip；旧 30 个测试文件哈希不变。套件存在重叠，不累加为独立总数。
- 验收卡与门记录：`generated/phase3_20261112/determinant/acceptance_card.json`、`gate.json`；最终运行在同目录的 `acceptance_final/`。

核变换已在真实 Train `FQI-SRC-AQ-3.23`（`FiniteQBenchmark.Identity313.statement`，源 SHA-256 为 `62ecabe282447bdcb7b6b5bbdeb51172f92d640cbf5498cb4f87436a84586ac5`）上完成局部闭环。完整 Source/Gamma 保留任意 `N : ℕ`、任意 `CommRing R` 和四个序列；没有固定规模抽样或增添非零条件。原命名空间中的 `K/Field K` 仍保留于源快照，实际 Lean 类型审计确认这些未使用变量没有被泛化进 theorem 的有效参数。

实际纯核心搜索两坐标置换，构造双向有限域蕴含、有限上下界以及序列指标非负性的整数仿射见证。独立检查器逐条检查 24 个见证，并验证置换逆和带重数的序列权重。特别是 `u (r-n)` 仍使用自然数减法，其指标与支持域绑定。Lean 使用保留的有限三角求和换序引理，只证明原左端等于转置后的嵌套和；从转置和中提取 `delta` 并连接原右端仍是未完成工作。

- 注册版本：`kernel_transform 2.0`，`capability_level=L3`、`local_lean=true`、`full_original=false`。
- 正式证书：`kernel-transform-local-d9603cb74629f83d3bbf4bff`。
- 状态为 `C=1`、`O={original}`、`links=[]`、`original_identity_proved=false`。
- 正式局部正例、全新恢复重验、实际错误 Lean 证明各一次；另有四类绑定篡改、真实 Train 不匹配和真实核心错误域／指标／搜索预算负例。正式 smoke 核对 84 个产物哈希；独立审阅另核对 77 个唯一生产产物路径，两种计数口径不相加。
- 登记后组件回归 32/32、0 skip；独立审阅未发现 Critical/Important，旧 30 个测试源文件哈希不变。本次未重新运行整个第三阶段套件。
- 验收卡与门记录：`generated/phase3_20261112/kernel_transform/acceptance_card.json`、`gate.json`；独立审阅在 `kernel_transform_review/review.json`，最终运行在 `kernel_transform/acceptance_final/`。

差分环已在真实 Train `FQI-SRC-FINE-2.1`（`FiniteQBenchmark.Identity342.statement`，源 SHA-256 为 `c3eda83aab248ff5a577f8b43b5f82c995346ec43c769253770b5967fdcd356e`）上完成局部闭环。完整保留任意 `Field K`、参数 `a/q`、自然数 `n`、`1 ≤ n` 与原 `h_domain : True`，没有增加 `q ≠ 0` 或特征零条件。

源映射使用 `aq=a*q`、`x=q^(n-1)`、`p=pochList [a*q] q (n-1)`、`pnext=pochList [a*q] q n`。实际差分环核心以原关系乘子 1 给出 `pnext-p = -(aq*x*p)`；独立整数多项式检查器重新计算目标、关系和乘子恒等式，并拒绝有理分母。关系 `pnext=p*(1-aq*x)` 没有加入原假设：固定 Lean 规则先由 `poch_succ` 和原 `hn` 证明它，再用 `linear_combination` 重放乘子。共享系数模块中的有界整数解析器仅用于检查，没有调用系数法求解核心。

该局部证书证明末端增量关系，原题要求的首项抽取／尾段参数移位仍开放。组件探针中的负号结合形式与真实候选一度不同，受控 `simpa only [neg_mul]` 已统一它们；最终预注册和生产 CLI 都使用真实 Source 重建的候选，组件通过不替代正式验收。

- 注册版本：`difference_ring 2.0`，`capability_level=L3`、`local_lean=true`、`full_original=false`。
- 正式证书：`difference-ring-local-7b633cc3585ceacacf380513`。
- 状态为 `C=1`、`O={original}`、`links=[]`、`original_identity_proved=false`。
- 正式局部正例、全新恢复重验、实际错误 Lean 证明各一次；另有四类绑定拒绝、真实 Train 不匹配、实际核心缺关系／关系变号／次数预算负例。smoke 核对 84 个产物哈希，独立审阅核对 77 个唯一生产产物路径，口径不累加。
- 登记后相关回归 34/34、0 skip；独立审阅未发现 Critical/Important，61 个冻结源码与原运行依赖绑定一致，旧 30 个测试源文件不变。
- 验收卡与门记录：`generated/phase3_20261112/difference_ring/acceptance_card.json`、`gate.json`；最终审阅在 `difference_ring_review/review.json`，实际运行在 `difference_ring/acceptance_final/`。

MacMahon 已在真实 Train `FQI-SRC-GR2-7.Ex14`（`FiniteQBenchmark.Identity149.statement`，源 SHA-256 为 `d955fd8fb345c0110619eb923c2b21eccdbd6e913aaf0fcaba92e77816342580`）上完成局部闭环。完整解析并保留原来的三个合取目标及 `z/q : ℂ`、`n : ℕ`、`regular q`、`z ≠ 0`；原命名空间中未使用的泛型 Field 仅保留在 Source/Gamma，不人为加入实际命题的宇宙参数。

实际有理 Ω 核心接收两因子分母，其展开项为 `C0^n Grade^k W0^(n-2k) L0^(n-k)`。非负辅助指数投影精确选择 `0 ≤ k ≤ n`；令 `u=n-k、v=k` 后，得到 `1/((1-C0*W0)*(1-C0*Grade/W0))`。独立检查器用有界整数多项式交叉相乘核对两块分式分解，并检查正块与严格负块的展开方向。负块从 `L0^-1` 开始，不能把它的常数项误收进 Ω 结果。

`Grade=1` 只在每个原次数的 `k` 已有有限范围后代入。CAS 的外部有理函数系数域不被当成原定理的附加假设：Lean 在原 `ℂ` 域中证明所得两因子分母有形式幂级数逆，并证明任意原 `n` 的有限 Cauchy 系数恰等于源 Laurent 和；整数幂桥仅使用原 `z ≠ 0`。这是所得形式幂级数的局部实现验证，不是通用 Lean Ω 算子的形式化，也不涉及解析收敛。原 ultraspherical 比较、商式和极限三个目标仍开放。

- 注册版本：`macmahon 2.0`，`capability_level=L3`、`local_lean=true`、`full_original=false`。
- 正式证书：`macmahon-local-0086445c194540adb19a9da5`。
- 状态为 `C=1`、`O={original}`、`links=[]`、`original_identity_proved=false`；实际 Lean 审计宇宙参数为空。
- 正式局部正例、全新恢复重验、实际错误 Lean 证明各一次，另有绑定篡改与真实 Train 不匹配拒绝。smoke 核对 99 个产物哈希；独立审阅核对 92 个唯一生产产物路径，两者不累加。
- 登记后相关回归 34/34、0 skip；公共单态驱动和既有 profile 的相关实际检查另有 21 项通过，套件有重叠。独立审阅未发现 Critical/Important，74 个冻结源码绑定一致，旧 30 个测试源不变。
- 验收卡与门记录：`generated/phase3_20261112/macmahon/acceptance_card.json`、`gate.json`；最终审阅在 `macmahon_review/review.json`，实际运行在 `macmahon/acceptance_final/`。`common_validation.json` 和静态审阅中的 pending 字段是较早阶段记录，不用于描述最终门状态。

谱方法已完成一次真实接入尝试并记录明确缺口，分支停止，仍为 `spectral 1.0 / L2`。预选真实 Train 是 `FQI-SRC-GR2-7.2.24`（`FiniteQBenchmark.Identity130.statement`，源 SHA-256 为 `b8f35c5da4ec0e64366b20a87595c2ea6ca257d0f7b75b33a1aef29767a0b955`）。生产 CLI 在 Source 入口返回 `not_applicable`；恢复后的停止分类为 `graph_capability_missing`。原 Source/Gamma、`C=0`、`O={original}`、`links=[]` 保持不变，没有局部 Lean 候选或 Lean 重验。

缺口首先是现有请求仅支持大小 1–4 的显式矩阵，原题则有任意 `N+1` 个指标。其次，原 `phi` 序列的移位／特征关系与边界、分母尚未桥接；原题允许 `m=n`，此时两个向量相同，且按定义在 `x=0` 的值为 1，现有固定 `Af=0`、`Ag=g` 的 0/1 特征值分离器无法处理该分支。对角范数还需要独立证明。保留的谱 Lean 规则另引用当前缺失的 `Benchmark.StructuralAtoms`，尚无干净的固定基础导入路径。

一次真实核心进程对单个对角分量诊断返回 `search_exhausted`，它只复现现有分离器的不兼容，不是原题反例或原题特化后的成功样例。符号维数请求和极小预算分别被正确拒绝；19 项既有共享契约回归通过。谱方法的门记录为 `status=branch_stopped`、`passed=false`，仅证据核对通过；见 `generated/phase3_20261112/spectral/gate.json`、`acceptance_card.json` 及 `spectral_independent/review.json`。

## D：三种方法均已达到真实 Source L2

有限乘积已在真实 Train `FQI-POCHHAMMER-RESIDUES`（`FiniteQBenchmark.Identity023.statement`，源 SHA-256 为 `17f555760f965b55530908a84f8447b0590cecb3f8bcf50a3d9d75d1b06edf19`）上完成 Source 导出和实际符号构造。完整保留原任意 `Field K`、`a/q`、自然数 `m/n` 与 `0<m`，不固定长度，不增加 `q≠0`。

新纯数学核心 `product/index_construct.py` 搜索两种轴顺序：缺少 `n>0` 时拒绝以 n 为基数的候选，再用原 `m>0` 得到 `k=j+m*i`，逆映射为 `j=k % m、i=k / m`。独立检查器核对六条商余数／范围／逆映射规则，重新计算原两侧因子的自然指数多项式；保留 `n=0` 空积、单项积和 `q=0`。它实际构造索引证书，不以候选计划代替数学执行。

这条路线没有 Lean 桥或 proof profile。定义展开、有限乘积重排及原题组装尚未形式化，符号证书不能进入 C。公共 `source_symbolic_only` 作用域拒绝正式候选及新义务导出；成功停为 `incomplete / symbolic_translation_pending`，`C=0`、`O={original}`、`links=[]`、`original_identity_proved=false`。

- 新 Source 注册：`product 2.0 / L2`，`local_lean=false`、`full_original=false`；旧通用 standalone 入口实际仍为 L0，正式 `method-demo` 正确报告 `capability_unavailable`。
- 正式 CLI 一次真实动作耗时约 0.385 秒、扣一次动作预算；恢复不重复 CAS，Lean 调用始终为 0。17 个正式产物哈希通过；独立审阅连同真实核心探针共核对 70 个唯一产物路径。
- 六个真实核心探针分别覆盖成功、错误因子、缺少正基数、错误基数总量、候选预算耗尽和实际 worker 超时，超时无遗留子进程；另保存真实 Train 不匹配、极小预算和源哈希篡改拒绝。
- 登记后相关回归 41/41；共享作用域／既有运行时 50 项、产品组件 17 项通过。套件有重叠，不累加为总数。旧 30 个测试源文件哈希不变。
- 正式证据在 `generated/phase3_20261112/product/acceptance_final/`，验收卡／门为同方法目录下的 `acceptance_card.json`、`gate.json`；独立最终审阅见 `product_review/review.json`。
- 预注册 01/02/03 的证据脚本错误及 finalize01 的证据路径错误原样保留，不改写为成功；预注册正式采用第 04 轮，最终能力以 `acceptance_final` 及正式门为准。

非交换已在真实 Train `FQI-SRC-KAC-CHEUNG-5.7`（`FiniteQBenchmark.Identity425.statement`，SHA-256 为 `fa7bfbfae1de6d6fdeaefd41e14a56f2cd236cd0158676f2ceb79418f84bb22c`）上达到 `noncommutative 2.0 / L2`。完整保留任意 `Field K`、任意 `Polynomial K`、原 `q≠0` 和 `q≠1`。原 Source 的 `Batch5Proofs` 导入仅原样保存为输入文本，没有执行 Lean 或调用其中历史证明；符号来源绑定 `Batch5Definitions` 中的乘 x 与代入 q*x 两个定义。

实际核心从右向左计算每个有序算子词对任意 `c*x^d` 的作用。每个 M 贡献当前次数对应的 q 幂；独立检查另数原词中 M 在 X 之前的有序配对，验证额外 q 幂。原两侧 `MX` 与 `qXM` 都得到 `c*q^(d+1)*x^(d+1)`，没有预先把目标交换关系作为规则，也没有把两个算子当作可交换量。

由原两个定义的 K 线性可扩张到有限多项式，但当前只记录此符号规则，明确 `symbolic_rule_recorded=true / lean_verified=false`。没有 proof profile、Lean 候选或形式义务导出；`C=0`、`O={original}`、`links=[]`，原题未证明。旧通用非交换 standalone 请求仍为 L0。

- 正式 CLI 一次动作约 0.400 秒；恢复无重复 CAS、无 Lean。正式 17 个产物哈希通过；独立审阅含核心探针共核对 71 个唯一产物路径。
- 六个真实核心探针覆盖原关系成功、较长有序词成功、错误标量、错误顺序、步骤预算和实际 worker 超时；另有真实 Train 不匹配、源哈希拒绝和旧 standalone L0 检查。
- 登记后相关回归 31/31、0 skip。首次测试命令误拼模块名及提前 finalize 的日志原样保留；它们是证据执行错误，不改写为生产错误或成功轮。
- 验收卡、门和最终运行位于 `generated/phase3_20261112/noncommutative/`；独立审阅为 `noncommutative_review/review.json`。74 个冻结文件均核对，旧 30 个测试源不变。

组合已在真实 Train `FQI-FINITE-Q-BINOMIAL`（`FiniteQBenchmark.Identity005.statement`，源 SHA-256 为 `4963bc05a9be240c2bcf2a3b74efad216ea9678eeb596f0067c3dd3b54f95108`）达到 `combinatorial 2.0 / L2`。完整 Source 包括原 Gaussian 有限和、自然数三角指数与 Pochhammer 右端；实际符号构造只从右端定义提取 `1-z*q^i`，不把左端 Gaussian 与固定秩子集权重的对应关系当作已证事实。

核心搜索补集与成员两种布尔编码，对任意 `i<n` 的两种成员状态分别核对双向逆映射和局部权重。补集不保持原秩，成员编码成功；它在任意 n 上定义特征函数／过滤逆映射，没有枚举一个固定长度。六条有限基数规则核对固定秩子集与普通子集的 tag/forget 映射，权重保留 `(-1)^k*z^k*q^(∑ i∈s,i)`。末坐标的限制／追加映射与整数多项式分配律核对有限乘积展开的归纳步；空集、单点以及 q=0、z=0 不要求除法。

这是权重保持双射，未使用符号反转对合或不动点消去。Gaussian 固定秩权重桥在前端、证书和检查结果中均明确为 `pending`；有限集合规则与权重运输也尚未经过 Lean。正式状态仍为 `C=0`、`O={original}`、`links=[]`，没有形式候选、proof profile 或原题成功；旧通用 standalone 仍 L0。

- 正式一次动作约 0.388 秒，17 个正式产物哈希通过；恢复没有重复 CAS 或 Lean。独立审阅含真实核心探针共核对 70 个唯一产物路径。
- 六个真实探针覆盖成功、错误选择权重、遗漏秩符号、错误秩范围、候选预算及实际 worker 超时；另有不匹配 Train、源哈希拒绝、极小预算及旧 standalone 边界。
- 组件 20 项及登记后 31 项通过、0 skip；套件存在重叠，不累加。独立审阅无 Critical/Important，旧 30 个测试源不变。
- 卡、门及正式运行在 `generated/phase3_20261112/combinatorial/`，独立审阅为 `combinatorial_review/review.json`；78 个冻结文件均核对。

目前注册矩阵为 **8 个 L3、4 个 L2**，其中 11 种方法有真实 Train Source 路线，谱方法只有旧显式核心 L2。最终统一源码已完成全新 475 项回归，失败、错误和跳过均为 0；望远镜、递推与 Init 原题复验，以及六种局部 L3、三种 Source L2 和谱方法拒绝边界均按预期通过。A/B、D 已完成，C 为六项完成、一项停止；谱方法缺口仍在，所以第三阶段结论为部分完成。十二方法当前矩阵见 [METHOD_CAPABILITIES.md](METHOD_CAPABILITIES.md)，最终逐项结果见 [PHASE3_VALIDATION.md](PHASE3_VALIDATION.md)。

## 已完成部分的证据包

`output/agent_v2_phase3_evidence_20261112/pack_index.json` 索引 A/B 分阶段运行、默认 CLI 兼容版本、系数、插值、行列式、核变换、差分环、MacMahon 正式运行及三个 D 方法的 Source L2 运行及各自补充审阅材料。各包逐字节保留源、候选、日志、检查点和 `Candidate.olean`，分别映射到当次冻结运行时；`runtime_diffs/` 记录版本间的精确差分，不把旧运行重新标为当前源码的结果。插值组件开发探针早于最终固定 `BatchDefinitions` 导入，只有最终源码快照和生产收据用于该方法正式验收。行列式包映射 42 个冻结运行时文件和 11 个数学／配置源，保存与插值验收版本之间的六路径差分；核变换包映射 47 个冻结运行时文件和 13 个数学／配置源，保存与行列式验收版本之间的九路径运行时差分及纯核心差分。核变换增量包核对 320 个复制文件和 14 个明确省略的编译缓存，旧包清单哈希不变；这些快照不被描述为后续持续修改的当前工作区。

包中的原始收据保留绝对路径，清单提供原路径到包内路径的映射。Lean 工具链、Mathlib 与 CAS 外部环境只保留依赖清单；重复的基础编译缓存不随包分发。因此该包用于审阅和核对证据，不是一套独立运行环境。打包检查不会替代 Lean 验证，也不改变历史验收结果。

另增 `spectral_stopped` 包，逐字节核对 110 个文件，保存失败入口、实际核心诊断、独立审阅和停止卡，不加入已完成能力。冻结的 47 个运行时文件与核变换验收版本相同；另有 3 个诊断核心依赖和 2 个仅审阅的数学源。后二者没有被原题执行或 Lean 验收，来源映射明确区分这些角色。谱分支的恢复只保持原停止状态，不存在可重新检查的证明证书。

差分环包另核对 310 个复制文件、14 个明确省略的编译缓存，映射 52 个冻结运行时文件和 9 个数学／配置源，并保存相较核变换验收版本的七路径运行时差分。后续方法若修改公共驱动，也不得把此包的证明收据改写成后续版本的验收。

MacMahon 包核对 354 个复制文件、20 个明确省略的编译缓存，映射 58 个冻结运行时文件和 16 个数学／配置源。与差分环验收版本的九路径差分包含单态公共核验扩展；旧多态驱动没有变化。各组件开发失败、早期 pending 记录、最终正式门与审阅分别保留，最终状态以实际 `gate.json` 和生产收据为准。

有限乘积包核对 251 个复制文件，无省略项；冻结视图共 71 文件，其中 62 个运行时文件、3 个其他 Source 依赖、原声明与5个测试／辅助文件。所有 65 个实际 Source 依赖均有精确映射，与 MacMahon 验收版本存在六路径运行时差分，新增指标构造核心另留差分。此包没有 Lean 候选或证明收据；符号证书、错误返回、超时记录及历史脚本失败均保持原字节。

非交换增量包核对 242 个复制文件，无省略项；冻结视图 74 文件包括 66 个运行时文件、3 个其他 Source 依赖、原声明及4个测试／辅助文件。相对有限乘积验收版本只有五路径运行时差分：registry 与四个非交换适配文件，共享 loop 不变；新增算子核心另留精确差分。任意次数的符号作用和线性扩张记录没有被打包过程升级为 Lean 证明。

组合增量包核对 248 个复制文件，无省略项；78 个冻结文件为 70 个运行时文件、3 个其他 Source 依赖、原声明及4个测试／辅助文件。与非交换验收版本有五路径运行时差分，新增选择构造核心另有差分。至此 22 个分阶段包共 4138 个复制文件已核对，先前包不改写；最终统一源码的新回归证据单独归档，包含 262 个冻结源码／测试／配置文件、额外 1 个 Train 清单及每次运行的原声明快照；新旧版本不合并验收。

本阶段至今未读取 benchmark Test、未调用模型 API、未恢复旧 Agent/workflow 控制器、未运行全 Train，也未上传至 GitHub。

详细的 19 项验收报告见 [PHASE3_VALIDATION.md](PHASE3_VALIDATION.md)；最终统一回归及所有正式复验已完成；[十二张最终卡](generated/phase3_20261112/final_validation_01/report_metadata/method_cards_index.json)与阶段卡分别保留。
