# 第四批形式化：原目录第 301–400 条

本批 100 条 statement：train 75 条、test 25 条，沿用原目录顺序及既有划分。四批累计 400 条（train 313、test 87），其余 46 条尚未形式化。全部 446 条的划分仍为 train 346、test 100。

每个目标定理的证明保留一个 `by sorry`。本批增加 41 个具体定义和 40 个完整证明的辅助定理；累计 143 个辅助定理、265 个共享命名声明。共享模块不含 `sorry`、`admit` 或新增公理。类型检查、公理审计和数值抽样不等于目标恒等式的证明。

## 原书核对与形式化约定

采用冻结 Markdown 对应的 catalog 陈述及已记录修订。来源逐条保存在 `source_audit.json`，历史验证字段是原目录记录，不代表本轮重复了全部历史验证。本轮查阅本地 Andrews《q-Series》、Fine《Basic Hypergeometric Series and Applications》及 Sills《An Invitation to the Rogers–Ramanujan Identities》。Sills 是扫描本，另核对印刷页 44–46、123、134–135 的图像；AQ 的算子定义核对印刷页 103 图像。文件指纹和重点页码见 `review_notes.json`。

| 条目 | 处理 |
|---|---|
| 301–303 | 沿用平面分拆的转置数组表示；有序组成使用有限函数计数。303 的整数上指标高斯系数独立定义为有限乘积商，允许负上指标，保留任意端点 a₀、aₙ₊₁。 |
| 304–308 | Hermite 型对象使用有限 Laurent 和。三角逆 T 使用 (2.38) 递归定义，证明递归指标下降和解唯一性；没有用待证的乘积闭式定义 T。308 保留奇偶分支，闭式仅在 n≥1 时要求分母条件。 |
| 309–318 | 双边和用整数区间；Bailey 对显式展开。316 沿用 catalog 对原书 (3.42) 的更正。317 用 k+1 表示正参数对数，单调多重指标完整展开，证明相邻差没有自然数截断。 |
| 319–320 | aₙ 是原书 G₀(x)/(x;q³)∞ 的系数；G₀ 按 (6.14) 系数方程构造。没有将目标 (6.18) 或 (6.19) 作为 aₙ 的定义。 |
| 321–331 | F 是非相邻占据位置的有限枚举，σ=1 排除位置 1；G 是原书另一个递推多项式，二者不混用。AQ 的 Dₙ 是未移位的 `schurD q n`，区别于第三批 AP 的移位约定。327 用 v₀=m₁+R、其余 vᵢ=mᵢ₊₁ 转成非负有限单纯形，所有前缀和仍为整数。负长度 q-Pochhammer 保留倒积及其实际定义域。 |
| 332–335 | X 使用奇偶项成对递推及 −1 初值。335 的五元算子、J、G 按原页展开，陈述为任意序列 d 上的算子恒等式；代入原书 d 即得到原式。没有把 J 定义为零来消去待证关系。 |
| 336–340 | Euler 变换采用 ℚ 上形式幂级数，允许 aₘ 为有符号整数；取第 n 项时乘积截到 m=n。Rogers–Ramanujan 系数从函数方程递推构造，并证明对应形式函数方程。q-差分使用原书 (f(x)−f(qx))/x，在零点用导数延拓，证明它与已有 Jackson 算子的关系。 |
| 341 | Bₙ 根系乘积在真正的多变量 Laurent 代数中构造，常数项为 `.coeff 0`。 |
| 342–348 | Fine 的 C 是有限乘积商；H、G 由 L、M 递推，保留原下标 −1 的初值。A 是 Euler 因子与 C 系列乘积的实际系数，不用待证闭式定义。证明 H/G 递推唯一性及 A₀=1。 |
| 349–357 | Rogers–Szegő 多项式沿用有限定义；多变量 Q 用有限函数枚举，并证明每个总和为 n 的非负指标都在枚举内。单位根使用 `IsPrimitiveRoot`，分数幂改为相容根参数 sᵖ=q。357 的分拆固定长度、所有项正且最大项为 L。 |
| 358–366 | 有限双边和、Heine 和 Watson 函数显式展开；负指数保留 ℤ 类型。q-三项式 C 的越界项先置零，再计算非负指数，避免 q=0 时产生伪负幂。T、Heine f、Watson f 使用原书定义，递推仅为待证目标。 |
| 367–385 | 不同部分分拆用有限子集计数。统一 α^(d,e,k)(xᵉ,qᵉ) 的有限定义；e 决定 Bailey 基底，不能误加到 α 表达式中。证明整除支撑及 α₀=1，保留其商式定义域。半整数指数由 t²=q 表示。Schur 分拆保留间距条件及相邻 3 的倍数不能差 3 的限制。 |
| 386–400 | D、E、B、P、C、T₀、T₁ 均为具体有限和；初值、链式等式及全部递推系数照录。389 沿用 catalog 的 Eₙ₋₁ 修订，390–392 保留已更正的倒底数前因子。T₀/T₁ 定义另核对 Sills (1.191)–(1.192)，不以本批待证递推代替定义。 |

### 形式生成函数

`eulerReciprocalSeries q` 和 `eulerProductSeries q` 分别由系数 1/(q;q)ₙ 及 (−1)ⁿqⁿ⁽ⁿ⁻¹⁾ᐟ²/(q;q)ₙ 构造。Lean 中完整证明初始系数与系数递推，并证明 F(X)=F(qX)+XF(X) 和 E(X)=E(qX)−XE(qX)。这些是正规化 Euler 因子的形式函数方程，不声称已经证明任意数值参数上的无限乘积解析收敛。

AQ 的 G₀ 由 (6.14) 导出的系数递推构造，再与 `eulerReciprocalSeries (q^3)` 做真正的幂级数乘法得到 aₙ。Fine 的 Aₙ 同样采用幂级数系数定义。Euler 变换使用 (1−Xᵐ) 的真实形式逆，另证明正 m 时逆存在并具有常数项 1。

### 定义域

多项式恒等式保留 q=0、1 及单位根处有意义的取值。出现商式时收集实际分母非零条件，涉及负幂时保留非零底数。一般代数式用域 K，三角函数、单位根及导数用 ℂ；Euler 变换用 ℚ。这里不宣称给出了每式的最大解析延拓域。

`specs/` 是逐条编写的表达式。生成脚本只渲染这些表达式和收集分母条件，不做 LaTeX 猜测转换。目标文件仅导入共享模块，不互相导入 train/test 目标。

## 验证记录

- `manifest.json`：100 条来源、划分、路径及状态。
- `compilation.json`、`compile_logs/`：逐条编译及当前源文件哈希。
- `source_audit.json`、`review_notes.json`：来源记录及本轮翻译约定。
- `auxiliary_audit.json`、`Batch4Audit.log`：265 个共享声明的公理依赖；只允许 `propext`、`Classical.choice`、`Quot.sound`，没有 `sorryAx`。
- `semantic_checks.py`、`semantic_checks.json`：350 个精确有理数检查，涵盖三角逆闭式、G₀ 系数卷积、Bailey 对、Schur 分拆、Fine H/G/A、P 和 T₀/T₁ 递推，以及算子恒等式的独立基向量输入；包含适用多项式的 q=0、1 边界。这些抽样不代替证明。

目标定理仍含 `sorry`，不能当作已证明定理默认开放给评测中的求证程序。

## 复现

在仓库根目录运行，先准备前三批共享模块及目标编译缓存：

```bash
python3 benchmark/scripts/generate_batch004.py
python3 benchmark/scripts/check_lean.py --log-batch batch_004 Benchmark/Batch4Definitions.lean Benchmark/Batch4Proofs.lean Benchmark/Batch4Audit.lean
python3 benchmark/scripts/check_lean.py --batch004
python3 benchmark/scripts/check_lean.py --log-batch batch_004 Benchmark/Train.lean Benchmark/Test.lean Benchmark.lean
python3 benchmark/formalization/batch_004/semantic_checks.py
python3 benchmark/scripts/finalize_batch004.py
python3 benchmark/scripts/build_split.py
python3 benchmark/scripts/validate_split.py
```

工具链和锁文件逐字核对原 `project`；只复用原依赖缓存，编译产物写入 benchmark。重建保留已登记的 statement 和原有数据划分。
