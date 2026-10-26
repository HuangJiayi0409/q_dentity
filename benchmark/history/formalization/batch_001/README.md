# 第一批形式化：原目录第 1–100 条

本批包含 **100 条 Lean statement：train 81 条、test 19 条**，按 `metadata/classification.json` 的原目录顺序选取，保留既有 train/test 划分。整个 benchmark 仍为 train 346 条、test 100 条；本批数量不是重新分配的测试名额。

每条目标定理的证明为 `by sorry`，这是本批约定的待证明任务。共享对象均有实际定义，所需辅助性质有完整证明。类型检查成功不等于目标恒等式已获证明，也不能代替对翻译数学语义的独立复核。

## 文件与验收证据

- `manifest.json`：100 条 ID、原目录编号、split、Markdown / Lean 路径及编译状态。
- `compilation.json`、`compile_logs/IdentityNNN.log`：逐条编译结果与文件 SHA-256。目标定理的 `sorry` 警告符合约定。
- `source_audit.json`：逐条原公式与 Markdown 哈希、来源记录、书名版本、页码／定位及原目录保留的修订依据。来源记录中的历史审查字段沿用原目录，不表示本次重新进行过其中每项历史检查。
- `auxiliary_audit.json`、`compile_logs/AuxiliaryAudit.log`：全部 96 个共享命名声明的公理依赖检查，其中有 46 个完整证明的辅助定理；只允许 `propext`、`Classical.choice`、`Quot.sound`，没有 `sorryAx` 或新增数学公理。
- `specs/`：逐条手工编写的 Lean statement 规格，生成脚本仅负责渲染文件，不自动猜测 LaTeX 的含义。
- `../../metadata/lean_statements.json`：已登记 statement 的持久索引，重建 train/test JSONL 时读取并验证。

## 原书核对与形式化约定

本轮对缺省记号和对象定义查阅了本地原书 PDF：Gasper–Rahman 第二版第 1–3 章（GR）、Andrews《The Theory of Partitions》第 9 章（AP）、Andrews 的 q-Series 专著（AQ），以及 Sills 的相应条目。逐条出处保存在 `source_audit.json`；下面列出对实现有实际影响的解释。

| 原目录编号／对象 | 原书依据与实现 |
|---|---|
| 1–9，Gaussian | 使用递推定义的 Gaussian 多项式，保留零底数和单位根处的多项式取值。`gaussian_eq_quotient` 完整证明它与非零分母域上的有限乘积商一致；`gaussian_polynomial_eval` 证明多项式求值兼容性。整数下标越界为零。GR 第 1 章 Notes on Ex. 1.2 的矩形分拆解释和有限域子空间解释分别对应显式有限枚举、`Submodule` 的计数。 |
| 12–20、39 等有限超几何式 | GR (1.2.22)、(1.2.26)，印刷 pp.5–6。显式定义每项的有限 Pochhammer 因子、基本超几何相位幂及截断求和。`phiDefined` 对实际求和项要求分母非零，截断后的尾项不参与计算。 |
| 15、16，very-well-poised | 证明消去可去因子后的 `wellPoised` 与 `wellPoisedRaw` 在 a≠1 时一致。第 15 条采用来源允许的 a=1 消因子解释；第 16 条保留原始表达式及 a≠1。 |
| 21，Dyson 常数项 | GR Notes on Ex. 2.31，印刷 p.68。使用指数为整数向量的群代数实现 Laurent 多项式，读取零向量系数，无未定义的“常数项”占位符。 |
| 24，根单位分解 | GR 第 1 章与 Sills 的根单位分解条目。用 `IsPrimitiveRoot` 表示原根；辅助定理证明原书的复指数选择确实是原根。 |
| 25，Jackson 导数 | KC (1.10)，p.2。非零点使用差商，零点使用导数延拓，避免把 0/0 当成原式的导数值。 |
| 26–29，Göllnitz 多项式 | AQ pp.102–103，(10.16)、(10.18)、(10.21)–(10.24)，并参照 Sills 2.82–2.83（p.85）。按分拆部分的实际限制定义有限集合：不含 1、3，相邻部分差至少 6，较大部分模 6 为 0、1、3 时严格大于 6；t 权重按余数类别计数。完全证明 N=0,…,6 的初值及约定 N=−1、−7 的取值。 |
| 30、36–38，Schur 多项式 | 有限 q-binomial 和定义 D、E，目标是其另一种有限和表示；双边和使用整数指标，Gaussian 越界为零，整数除以 2 对应原式的 floor。 |
| 31，Cayley | AP p.81。以有界重数向量枚举分拆，完整证明加权总和等于 n 的重数均不超过 n，因此没有漏掉合法重数向量。 |
| 32–35，oscillation | AP §9.3，pp.143–149，特别是 (9.3.9) 及后续公式。分拆以矩形内弱降序序列定义；successive ranks 使用共轭列高，oscillation 是 Durfee 范围内的严格递增指标序列，正／负起始阈值按原书。计数“至少 μ”由存在长度 μ 的序列表示，并证明长序列可截成短序列。 |
| 40、41，复数分数幂 | GR (1.2.47)、(1.2.55)，pp.7–8。显式给出共同对数分支 L，要求 exp L=q；所有相关分数幂均由同一 L 的指数表示。 |
| 42，对称 q-exponential 系数 | GR (1.3.23)–(1.3.26)，pp.11–12。用幂级数及原书定义函数的差分初值方程刻画 A，目标保留系数递推和显式系数公式。没有用待证系数公式定义 A。 |
| 43–47，ultraspherical／算子／little q-Jacobi | GR Ex.1.29、1.31–1.33，pp.31–33。定义相应有限 Laurent 和、算子迭代及有限超几何多项式。 |
| 相关 q-Racah、Askey–Wilson 条目 | GR Ex.2.10–2.11，p.59。t 表示 q-Racah 的 q^x 坐标及 Askey–Wilson 的谱坐标；x=(t+t⁻¹)/2，辅助性质证明 t→−t 对应 x→−x。 |
| 77、83、86 | 按 catalog 的已修正版公式形式化；保留来源记录中的纠错与来源信息，不回退为书中原误式。 |
| 90–96，负长度 Pochhammer／双底数局部式 | GR §3.6，pp.80–83。负长度使用倒数有限积，另列内部分母定义域；T 的 −1 初值显式定义为零并证明。不能仅检查最外层分母。 |
| 97–100，multibase／矩阵 | GR §3.9，pp.94–95；§3.10，pp.97–98。按原书 Φ 的底数和相位约定定义有限项，主底数阶乘只出现一次；逆矩阵元素使用整数长度 Pochhammer 和显式定义域。 |

一般代数恒等式使用域参数 `K`，来源要求复数、对数分支或有限域时则使用相应对象。自然数与整数指数分开编码，所有分母和底数条件写在 statement 中。来源给出的安全参数域不宣称是最大解析延拓域。必要的原式假设保留为假设；从对象定义推导出的辅助性质则在共享模块中证明。

共享模块分层为 `Definitions → Auxiliary → Gaussian → BatchDefinitions → BatchAuxiliary → InitialValues → Representation`。目标 statement 只导入共享模块，train/test 的目标互不导入。`Benchmark.Train`、`Benchmark.Test` 分别汇总，`Benchmark.lean` 为开发编译入口。进行证明评测时必须明确允许的导入，不能将含 `sorry` 的其他目标定理当作已证明事实使用。

## 复现

从仓库根目录运行，复用现有 `project/.lake` 依赖缓存；脚本先核对两个项目的 toolchain 和依赖锁文件相同，不修改原项目。

```bash
python3 benchmark/scripts/generate_batch001.py
python3 benchmark/scripts/check_lean.py Benchmark/Definitions.lean Benchmark/Auxiliary.lean Benchmark/Gaussian.lean Benchmark/BatchDefinitions.lean Benchmark/BatchAuxiliary.lean Benchmark/InitialValues.lean Benchmark/Representation.lean Benchmark/AuxiliaryAudit.lean
python3 benchmark/scripts/check_lean.py --batch001
python3 benchmark/scripts/check_lean.py Benchmark/Train.lean Benchmark/Test.lean Benchmark.lean
python3 benchmark/scripts/finalize_batch001.py
python3 benchmark/scripts/build_split.py
python3 benchmark/scripts/validate_split.py
```

生成会将批次状态重置为待验证，只有当前文件哈希与全部成功编译记录一致，且共享声明公理审计通过，才可重新登记。重建脚本检查已形式化条目的 split、Markdown 和 Lean 哈希；修改这些内容后需重新验证，不能静默沿用旧状态。
