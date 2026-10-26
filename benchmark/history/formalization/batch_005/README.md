# 第五批形式化：原目录第 401–446 条

最后一批共 46 条 statement，train 33 条、test 13 条。五批合计 446 条（train 346、test 100），沿用原目录顺序及冻结划分。

目标证明均保留一个 `by sorry`。本批新增 27 个具体定义和 37 个完整证明的辅助定理；累计 180 个辅助定理、329 个共享命名声明。共享模块没有 `sorry`、`admit` 或新增公理。statement 完成表示陈述已翻译并通过类型检查，不表示目标恒等式已经完成证明。

## 原书核对与形式化约定

采用冻结 Markdown 对应的 catalog 陈述及其已记录更正。`source_audit.json` 保存逐条来源；其中历史验证字段来自原目录，不代表本轮重复了所有旧计算。本轮查阅本地 Kac–Cheung《Quantum Calculus》相关章节，重点核对印刷页 9、99–104，并查看负指标定义及一般 Taylor 基底原页图像；Sills 的 Borwein 定义和 motivated proof 初值另核对印刷页 136、142 的扫描图像。文件指纹与核对点见 `review_notes.json`。

| 条目 | 处理 |
|---|---|
| 401–402 | 沿用第四批由有限和定义的 T₀、T₁、P。401 的整数指数保留负幂及 q≠0；402 的非负二次指数允许多项式边界取值。 |
| 403–409 | Borwein A、B、C 从真正的多项式乘积 ∏ᵢ(1−X³ⁱ⁺¹)(1−X³ⁱ⁺²) 的系数按模 3 分组提取。完整证明三部分重组为原乘积的关系和初值，不以待证 Gaussian 展开或耦合递推定义这些对象。406–408 保留 n≥1 及 n=0 的单独初值。 |
| 410 | Aᵢ 使用 {3,…,i−2} 的非相邻子集枚举，Bᵢ 使用原有限关系及 i=3 边界；核对原书 A₃=A₄=1、B₃=0。 |
| 411 | α 的三个剩余类及零指标独立定义，沿用 catalog 对两处原书指数的更正。完整证明各分支与 n=3r、3r±1 的写法一致。 |
| 412–414、435–437 | 使用真实的点值差分算子。乘法、商法则和伸缩和可对任意函数逐点陈述，因而包含原有多项式／有理函数情形。保留采样点和实际分母非零条件；414 的幂指标是非零整数。 |
| 415–420 | Pₙ 的指标完整保留为 ℤ；负指标使用原书 (3.7) 的移位倒积。分别记录源函数在 x、qx 的定义域及右侧实际分母，证明负分支及其逆确实相乘为 1。没有把负指标截为零。 |
| 421–424、431、433 | 高阶导数使用 Jackson 算子的实际函数迭代。多项式值使用 Polynomial.eval；q 阶乘是有限乘积。零点由已有导数延拓定义处理，422 保留 j>n 时为零的分支。431 约束所有被迭代访问的 qˢx 处的原始分母以及最后的乘积分母。 |
| 425–427、430 | X 和 M 是作用于实际多项式的乘法及代入函数。426 在一般含幺结合 K-代数中陈述，保持 YX=qXY，不错误要求算子交换。427 的加权子集指数用整数差，避免自然数减法隐式截断。Galois 数独立定义为 Gaussian 的有限和。 |
| 428–429 | 给定实际有限域 F，q=Fintype.card F。向量组按 LinearIndependent 筛选；矩阵按 Matrix.rank 筛选，直接计数有限对象。429 的等式写在 ℤ 中，保留计数的精确整数值及两段等号；没有把右侧乘积当作计数定义。证明有限域大小至少为 2。 |
| 432、434 | 倒底数与消去式中的指数用整数；保留所有实际商式分母及 M≥1。 |
| 438–442 | 对称 q 数、阶乘、Gaussian 和有限 q 幂均显式定义。对称差分在非零点是两点差商，在零点取导数延拓；完整证明 q≠0、q²≠1 保证 q−q⁻¹≠0。 |
| 443–445 | 量化原书的一般 Taylor 多项式族 T，明确给出初值、次数、边界 Tₖ(a)=0 和真正的多项式差分方程。sₙ 是 `(T n).roots.sum`，按重数求和；不是任意满足待证递推的序列。完整证明差分方程在普通点等于原差商，并用 Vieta 证明根和与次首项系数的关系。 |
| 446 | 沿用 catalog 已修正的有限三角递推，在 Polynomial 中递归构造 Tₙ；完整证明递归初值及定义解的唯一性。降阶关系和边界正是本条目标陈述的一部分，按用户约定留在目标的 `sorry` 中。 |

### 一般 Taylor 基底与根和

`quantumTaylorFamily q r h h' a T N` 要求 T₀=1，对 1≤k≤N 要求 deg(Tₖ)=k、Tₖ(a)=0，以及

`Tₖ(qX+h)−Tₖ(rX+h') = ((q−r)X+(h−h')) Tₖ₋₁(X)`。

这是原书定义的分母清除形式，没有加入任何待证根和关系。443–445 是对满足这些定义条件的任意多项式族的定理，并非另行声称本批已经形式证明所有参数上的一般基底存在性。443、445 保留所用量子数非零；444 使用 q=r≠0、h≠h' 的独立分支。

原书印刷页 104 的嵌套根乘积不能由根和递推推出，本批没有采用它。446 使用冻结 catalog 中已有推导的替代构造。一般根和对象采用复数域中的真实根；`quantumRootSum_coeff` 已完整证明其等于 −次首项系数／首项系数，不额外假设根嵌套或互异。

### 定义域和语义

一般有限代数式使用域 K；导数、三角基底与根使用 ℂ；有限域计数使用具体有限域 F。保留原 catalog 的 q≠0、1 或 q²≠1 条件，以及出现的有限分母非零条件。多项式型 Borwein 等式没有额外排除 q=0、1。这里不宣称给出了每条公式的最大可去奇点延拓域。

`specs/` 是逐条编写的数学表达式。生成器负责渲染和收集分母条件，不做 LaTeX 猜测转换。目标文件只导入共享模块，不互相导入 train/test 目标。含 `sorry` 的目标不能作为评测时默认允许使用的已证明定理。

## 文件与验证

- `manifest.json`：46 条公式、划分、路径和状态。
- `compilation.json`、`compile_logs/`：逐条编译、当前源文件哈希及总入口日志。
- `source_audit.json`、`review_notes.json`：逐条来源和本轮核对约定。
- `auxiliary_audit.json`、`compile_logs/Batch5Audit.log`：329 个共享声明的公理依赖；只允许 `propext`、`Classical.choice`、`Quot.sound`，没有 `sorryAx`。
- `semantic_checks.py`、`semantic_checks.json`：267 个独立精确检查，涵盖从原乘积提取的 Borwein 系数、正负指标的有限 q 幂、由一般差分算子构造的 Taylor 多项式、修正后的对称 Taylor 基底及有限域定秩矩阵穷举。根和样例通过 Vieta 系数值计算。这些检查不是 Lean 证明。

## 复现

在仓库根目录运行，先准备前四批共享模块及目标的编译缓存：

```bash
python3 benchmark/scripts/generate_batch005.py
python3 benchmark/scripts/check_lean.py --log-batch batch_005 Benchmark/Batch5Definitions.lean Benchmark/Batch5Proofs.lean Benchmark/Batch5Audit.lean
python3 benchmark/scripts/check_lean.py --batch005
python3 benchmark/scripts/check_lean.py --log-batch batch_005 Benchmark/Train.lean Benchmark/Test.lean Benchmark.lean
python3 benchmark/formalization/batch_005/semantic_checks.py
python3 benchmark/scripts/finalize_batch005.py
python3 benchmark/scripts/build_split.py
python3 benchmark/scripts/validate_split.py
```

工具链与锁文件逐字核对原 `project`，仅复用其依赖缓存，所有编译产物写入 benchmark 自身目录。重建保留所有已登记的 statement 及数据划分。
