# 第二批形式化：原目录第 101–200 条

本批包含 **100 条 Lean statement：train 81 条、test 19 条**。沿用 `metadata/classification.json` 的原目录顺序与既有数据划分。两批累计 200 条，其中 train 162 条、test 38 条；整个 benchmark 仍为 train 346 条、test 100 条。

目标定理的证明按约定保留 `by sorry`。本批新增 **23 个完整证明的辅助定理**；共享对象的定义没有占位常量或未证明公理。全部 statement 逐条类型检查，共享声明另做公理依赖审计。类型检查通过不代表目标恒等式已经证明，数学翻译仍可接受独立复核。

## 原书核对与形式化约定

采用现有 Markdown 中的公式、参数域和修订版本。遇到省略对象定义、零系数项、分数幂和初值时，查阅本地 Gasper–Rahman《Basic Hypergeometric Series》第二版第 3、7、8、9 章。具体来源、版本、页码、历史修订记录逐条保存在 `source_audit.json`；其中历史审查字段来自原目录，不表示本轮重新执行了全部历史检查。

| 编号／主题 | 处理方式 |
|---|---|
| 101–112，多底数变换 | 使用第一批定义的 `bibasicPhi`、`phi` 和原始 very-well-poised 有限和。底数、相位、截断长度与各侧参数分别保留；λ 的约束以相等的有理式写出。 |
| 113–115，混合变换与反演 | 查 GR Ex.3.21、3.23（pp.106–107）。普通上升阶乘定义为有限乘积，K、T、R 按原式展开。第 113 条沿用 catalog 修正的 B+k−k/μ。第 115 条对任意有限前缀写出双向系数关系，复用实际定义的三角矩阵元素，不假设目标反演关系。 |
| 119–123，双边有限和 | 指标采用整数区间，特别保留 −n−1 下界；负长度 Pochhammer 用有限倒积，内部分母和外部分母分别列入条件。 |
| 125，常数项 | 在 `AddMonoidAlgebra K ℤ` 中定义 Laurent 单项式，提取零指数系数。 |
| 126–148，正交多项式 | q-Racah、q-Hahn、dual q-Hahn、Jacobi 等均按来源给出的有限超几何定义展开；正交关系中的两个公式分别保留。三项递推的负次数值为零，零领先系数不要求计算下一次数的未定义级数。 |
| 133、136–137、143 等平方根 | 显式给出相容根 s²=q、u²=β 等；半整数幂用该根的整数幂表示，不混用独立主值。 |
| 141–143，Askey–Wilson 算子 | 查 GR (7.7.1)–(7.7.6)，pp.196–197。采用 Laurent 坐标差商；完整证明坐标变化的分母为 (s−s⁻¹)(z−z⁻¹)/2。第 143 条保留 catalog 的已修正系数。 |
| 144、188–189，终止分支 | 对每侧分别使用“最早消失的上参数因子”条件 `terminatesAt`，不任意将不同级数截成同一长度。涵盖各侧实际最短终止长度的表述。 |
| 149、152，可去奇点 | 第 149 条同时保留有限和、非奇点处商式和复数穿孔邻域极限。第 152 条用有限 Laurent 和表示商式的延拓，并完整证明三种和分别等于原书的商式；四条公式均保留，第二条单独带 n≥1 条件。 |
| 153，不同连续 q-Jacobi 记号 | 𝒥 按 GR (7.5.25)／Ex.9.17(ii) 的定义，𝒦 按 Ex.7.32 的参数归一化分别展开，未把两个对象混为同一多项式。 |
| 154，有限差分式 | 查 GR Ex.7.37（p.208）。U、A、T 使用 catalog 的有限有理式，U 在 r 以上为零；n=r 的边界不会调用负截断长度。 |
| 160–169、181–185，乘积与双线性式 | F、H、A 等省略对象按实际有限和展开。来源要求跳过零系数项时，使用条件分支并将内部非零要求置于“外系数非零”条件下；有效 r、s 范围显式收紧到来源支持范围。 |
| 174，复数分数幂 | 所有非整数 q 幂采用同一个 L，假设 exp L=q；平方括号中的归一化指数沿用 catalog 修正版。 |
| 186–187，允许的终止分支 | 按 catalog 的 b=q⁻ⁿ 分支写出，c 分支通过参数互换实例化；不纳入原目录已隔离的 a 单独终止分支。 |
| 190，有限线性化 | 用原目录显式有限的 T 核，指标下界 max(k−m,k−n)，避免原印中的 0×∞；保留实参数 a,b>0。 |
| 191，修订后的长度 | 保留 catalog 修正的长度 k 和 m，以及对应原始来源／纠错记录。 |
| 193–195，相伴多项式 | 查 GR Ex.8.26–8.28（pp.254–255）。从初值 (前项,当前项)=(0,1) 和三项递推构造对象；完整证明递推方程、初值和解的唯一性。没有用待证 10W9／双重和／线性化公式定义对象。涉及递推除法的非零条件显式列出。第 195 条使用实际最短终止长度。 |
| 197，有限支撑权重 | 查 GR §9.5（pp.268–269）。权重在 N 以后为零，ν 的内和和两侧外和均显式有限。 |
| 198–200，有限生成函数 | 查 GR Ex.9.4–9.5（pp.272–273）。第 200 条采用 catalog 已辨明的习题参数定义，和第 130 条的同名 dual q-Hahn 对象区分。 |

`specs/common.py` 是手工数学表达式的渲染工具，不是 LaTeX 解析器。它在构造除法、有限超几何式和有限和时收集实际分母条件，写入 statement 的 `h_domain`；求和内部条件保留对应指标范围，零系数分支内部条件是条件性的。目标陈述、平衡关系、正整数范围和原书非零条件逐条编写。整数幂显式使用 `ℤ`，避免自然数减法截断。

与第一批一致，一般代数式使用域 `K`；涉及极限和对数时使用 `ℂ`，第 190 条使用 `ℝ` 保留正性。安全非零参数域不是最大解析延拓域声明。

## 辅助证明与证据

新增共享模块：

- `Batch2Definitions.lean`：普通上升阶乘、Laurent 单项式、终止谓词、最短长度、Askey–Wilson 差商、递推解及两类相伴多项式。
- `Batch2Auxiliary.lean`：上升阶乘递推、递推解初值、基本递推方程。
- `Batch2Proofs.lean`：最短终止长度正确性、终止后的有限积／级数项为零、递推解唯一性、相伴多项式递推、坐标差商、零系数规则、三种 Laurent 和的商式桥接。
- `Batch2Audit.lean`：检查两批共享的 **130 个命名声明**，仅依赖 `propext`、`Classical.choice`、`Quot.sound`，不含 `sorryAx`。

目标文件只导入共享证明模块，不导入其他 train/test 目标。总入口包含带 `sorry` 的待证明目标，仅供开发编译；证明评测仍需明确允许的导入，不能将其他目标当作已证明事实。

`manifest.json` 记录 100 条对应关系与状态；`compilation.json` 和 `compile_logs/` 保存逐条编译结果及文件哈希；`auxiliary_audit.json` 保存共享模块哈希与公理检查结果。`source_conditions.txt` 保留来源条件的便于检索版本。

## 复现

从仓库根目录运行。编译脚本复用原 `project` 的匹配依赖缓存，输出写入 benchmark 的 `.lake`；不修改原项目。

```bash
python3 benchmark/scripts/generate_batch002.py
python3 benchmark/scripts/check_lean.py --log-batch batch_002 Benchmark/Batch2Definitions.lean Benchmark/Batch2Auxiliary.lean Benchmark/Batch2Proofs.lean Benchmark/Batch2Audit.lean
python3 benchmark/scripts/check_lean.py --batch002
python3 benchmark/scripts/check_lean.py --log-batch batch_002 Benchmark/Train.lean Benchmark/Test.lean Benchmark.lean
python3 benchmark/scripts/finalize_batch002.py
python3 benchmark/scripts/build_split.py
python3 benchmark/scripts/validate_split.py
```

从无 benchmark 编译缓存的环境开始时，先执行第一批 README 中的共享模块编译命令，再执行这里的命令。第一批目标也需编译才能构建包含两批的总入口。
