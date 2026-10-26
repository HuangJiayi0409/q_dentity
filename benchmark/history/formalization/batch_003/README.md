# 第三批形式化：原目录第 201–300 条

本批有 100 条 statement，train 76 条、test 24 条，沿用原目录顺序及既有分组划分。三批累计 300 条（train 238、test 62）；全部 446 条的划分仍为 train 346、test 100。

目标定理统一保留 `by sorry`。新增 34 个完整证明的辅助定理，以及 20 个具体数学定义；累计 103 个辅助定理、184 个共享命名声明。共享模块不含 `sorry`、未证明公理或占位对象。类型检查和公理审计不等于目标恒等式的证明，也不能替代数学翻译复核。

## 原书核对与形式化约定

采用冻结 Markdown 所对应的 catalog 陈述及修订。来源记录逐条保存在 `source_audit.json`，其中历史验证字段沿用 catalog，不代表本轮重做全部历史计算。本轮查阅本地 GR 第二版第 9 章、附录 III，Andrews《The Theory of Partitions》第 3、7、9、11、13 章；对于 PDF 文本提取不完整的公式，另核对原页图像（AP pp.117、147，GR p.362）。

| 条目 | 形式化处理 |
|---|---|
| 201 | 采用 Ex.9.5 的 dual q-Hahn 定义，与第 200 条一致：上参数 q⁻ⁿ、q⁻ˣ、bcqˣ⁺¹，下参数 q⁻ᴺ、bq；没有套用另一个归一化的同名对象。 |
| 202–205 | 相伴 ultraspherical 使用此前从初值构造的递推解，补齐递推中实际分母域。𝒥、r 和 Askey–Wilson 多项式使用各自的有限超几何定义。204 保留 catalog 已修订的总前因子。 |
| 206–209 | 双重和、逐项乘积和整数区间直接展开。负长度使用有限倒积；207 补充 U+V=1 的分母清除后代数关系。209 根据作者修订版 (3.26) 核对三重和；相同零因子在 j=n、k=0 或 s=q 时先约为 1，另证明非奇点处的商式、因子一致性和有限支撑外的项为零。 |
| 210–211、216–218 | 用有限函数表示多重指标，分别筛选总和等于 N、不超过 N 或各坐标不超过 m。完整证明有限坐标界及枚举完备性。Vandermonde 显式为 ∏ᵣ<ₛ(zᵣ−zₛ)。218 采用 catalog 已修订的平衡式和 λ。 |
| 212–215 | 原有平衡条件、参数分支、半长度与根的相容约束均保留。每侧实际分母分别记录。 |
| 219–240 | 整数指数显式使用 ℤ，长度使用受条件约束的 ℕ，避免负指数或长度中的自然数截断。239 指定原始 m 次单位根，保留链式等式的两段。 |
| 241–245 | 广义高斯系数独立定义：整数下指标负值为零，否则是有限乘积商。复数幂统一用 exp(Lα)，exp L=q；倒底数使用 −L。证明加法、整数幂一致性和倒底数相容性。 |
| 246–269 | φ、W 使用实际有限和。248 保留奇偶分支；249 保留 ceil(n/2) 和奇偶指数。264–265 分别约束两侧最早终止长度。266–268 的 V 展开为 q、q² 混合有限和；依据 GR p.362 合并成对根，并完整证明乘积合并性质。 |
| 270–280 | G 是矩形内分拆的枚举。inv、ind 是具有给定重数的有限词的逆序数／主指标计数。AP 的 Dₙ 等于此前辅助函数 `schurD q (n+1)`，不是 `schurD q n`；另定义并证明 D₋₁=1 的边界。 |
| 281 | AP pp.117–118 的严格间距由较小相邻项决定，使用独立的 `apGollnitzAllowed`，没有复用此前由较大项决定的定义。Λ 由原书生成函数导出的多项式系数递推构造，详见下文。 |
| 282–289、300 | 平面分拆采用原书矩阵的转置表示：首列变首行，体积和单调性保留；行列数参数没有交换含义。证明每个合法自然数数组都落在有限枚举内。行列式使用零越界高斯系数；三角／五边形指数的非负性另证。288 的 L 是作用于真实多项式环的线性映射，保留其全部基底值假设。 |
| 290–299 | 正／负振荡使用已有分拆枚举定义。F 和 f 按 AP p.147 及 catalog 的完整有限和定义；几何商用有限几何和延拓到比值为 1，证明其商式及边界。允许 −1 的参数 r 保持整数类型。 |

209 的原始更正来源：[Gasper–Schlosser, *Summation, transformation, and expansion formulas for multibasic theta hypergeometric series*, p.16, (3.26)](https://www.mat.univie.ac.at/~schlosse/pdf/GSpaper.pdf)。该式明确更正 GR (11.6.21)。本批沿用 catalog 的有限支撑版本。

### Λ 的系数定义

原书定义 F(x)=∑ Λₙxⁿ/(q⁶;q⁶)ₙ，由三个分子无限乘积和一个分母无限乘积给出。抽取各乘积首因子得到

`(1-x) F(x) = (1+xq²)(1+xq⁴)(1+xq⁵) F(q⁶x)`。

记 Q=q⁶，e₁=q²+q⁴+q⁵，e₂=q⁶+q⁷+q⁹，e₃=q¹¹。固定次数系数满足

`Λₙ₊₁ = (1+e₁Qⁿ)Λₙ + e₂Qⁿ⁻¹(1−Qⁿ)Λₙ₋₁ + e₃Qⁿ⁻²(1−Qⁿ)(1−Qⁿ⁻¹)Λₙ₋₂`，

其中 Λ₀=1，越过零下标的项为零。这是 `apLambda` 的定义，保留 q 为形式变量时的多项式意义，也不对数值 q 引入额外除法。Lean 中证明初值、一般递推、归一化后系数方程以及递推解唯一性。未将第 281 条目标恒等式用作 Λ 的定义，也未把无限乘积收敛性作为新的目标或假设。

### 表达与假设

一般代数式使用域 K，复数对数使用 ℂ。多项式恒等式不额外要求底数非单位根；存在实际商式时列出相应非零域。与此前两批一致，这不是最大解析延拓域声明。

`specs/` 是逐条手写表达式，不是 LaTeX 猜测转换器。除法、φ、W 的实际分母条件由渲染工具收集；内和中的条件只在该内和范围内要求，奇偶／可去值分支保留条件性约束。

## 文件与验证

- `Batch3Definitions.lean`：20 个具体定义。
- `Batch3Proofs.lean`：34 个辅助定理，完整证明。
- `Batch3Audit.lean`：共享 184 个声明的公理依赖检查，允许 `propext`、`Classical.choice`、`Quot.sound`。
- `manifest.json`：100 条公式、划分、路径和状态。
- `compilation.json`、`compile_logs/`：逐条编译结果与当前文件哈希。
- `source_audit.json`、`auxiliary_audit.json`：来源和辅助模块证据。
- `review_notes.json`：本轮实际核对的原书文件哈希、页码和翻译修订点。
- `semantic_checks.py`、`semantic_checks.json`：92 个独立精确有理数样例，比较分拆枚举、首列固定平面分拆、行列式、Λ 的 Euler 系数卷积和第 201 条的多项式归一化；均通过。这些抽样不是 Lean 证明。

目标文件仅导入共享模块，不相互导入 train/test 目标。总入口用于开发编译，含 `sorry` 的目标不能作为评测时默认允许调用的已证明定理。

## 复现

在仓库根目录运行。先准备前两批共享模块及目标的编译缓存，再运行：

```bash
python3 benchmark/scripts/generate_batch003.py
python3 benchmark/scripts/check_lean.py --log-batch batch_003 Benchmark/Batch3Definitions.lean Benchmark/Batch3Proofs.lean Benchmark/Batch3Audit.lean
python3 benchmark/scripts/check_lean.py --batch003
python3 benchmark/scripts/check_lean.py --log-batch batch_003 Benchmark/Train.lean Benchmark/Test.lean Benchmark.lean
python3 benchmark/scripts/finalize_batch003.py
python3 benchmark/scripts/build_split.py
python3 benchmark/scripts/validate_split.py
```

工具链与锁文件逐字核对原 `project`，只复用其依赖缓存；编译产物写入 benchmark 自身目录。重建不会重新分配公式，也不会修改原项目或已登记的 Lean 文件。
