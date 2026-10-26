# q WZ 分支的 q Gosper 后端

当前第四阶段高阶 ΠΣ／数域核心见 [DIFFERENCE_GENERAL.md](DIFFERENCE_GENERAL.md)。原 q-Gosper／有理系统算法继续复用，本轮未改变第三阶段分母和次数界。

第四阶段最新实现、输入契约和仍缺少的通用算法见 [DIFFERENCE_COMPLETION.md](DIFFERENCE_COMPLETION.md)。新增耦合 `difference_system`；有理系统最终线性消元改用精确域，全部相关回归已重跑。

第四阶段后续已经新增一般有理 `difference_field` 及有限代数 `finite_difference_ring`，算法与仍未完成的范围见 [DIFFERENCE_FIELD.md](DIFFERENCE_FIELD.md)。本轮没有将第四阶段标成全部完成。

第四阶段已增加 `difference_ring` 参数化求和核心：复用本目录的 q 因子轨道和有理方程求解，支持经过常数域检查的 Laurent 乘积／多项式嵌套和塔。完整输入范围、自动次数界、冗余扩张和自由常数策略见 [DIFFERENCE_CORE.md](DIFFERENCE_CORE.md)，测试及样例见 [第四阶段报告](../generated/difference_core_20261014/validation.json)。下方第一至第三阶段记录保留。

## 2026-10-14：第三阶段完成——有限秩耦合 q 移位核心

第三阶段已从对角分量推进到**有限秩、两个可交换可逆移位、单个求和指标**的耦合系统。新增 [qrational_system.py](qrational_system.py) 和 [qholonomic.py](qholonomic.py)，沿用原精确有理输入、q 因子移位识别、递推规范化与进程预算。支持域为 `K(X)`，`K=QQ(q,Q,独立参数)`，q 为不定元，`X=q^k,Q=q^n`。

这里的“完成”指以下核心算法链已实现并接通；不表示所有有限 q 恒等式都可解，或所有 holonomic 表达式均已接入前端。对于**固定右端基/固定递推阶数**，现在有推导分母界、推导次数界、求完整有限线性系统的有理证书算法；外层按阶搜索仍受资源预算限制，不给任意输入的无条件终止或全阶不存在保证。

|第三阶段任务|当前实现与可审查产物|
|---|---|
|精确移位表示|列状态 `Y` 满足 `σ_n(Y)=U Y, σ_k(Y)=V Y`；支持一般有理矩阵，逐项检查 `σ_k(U)V=σ_n(V)U` 以及形式域内可逆性。|
|标量化消元|对耦合证书方程逐坐标构造移位行和强迫项行，首次线性相关得到不超过模块秩的标量高阶方程；输出消元行见证。|
|通用分母界|用首尾系数的非零不可约因子移位交集推导有限极点区间，构造含重数的分母倍式；不枚举猜测极点或分母。|
|Laurent 次数界|去除非零极点后，从零点与无穷处的首尾项指示多项式计算全部整数 q 幂共振，得到精确必要下/上界。|
|参数化矩阵求解|所有坐标共用右端系数，将各坐标有理 ansatz 代回原耦合方程，求精确零空间；独立入口可输出完整解空间基，包含齐次证书方向。|
|创造性伸缩|从零阶开始移位 observable，逐阶调用完整固定阶矩阵求解；构造非零递推与证书行，检查原矩阵关系残差。|
|规范化和预算|递推清分母后同步缩放全部证书分量；保留最高阶多项式，控制状态维数、总未知数、派生多项式次数和硬墙钟时间。|
|源表达式入口|从现有 q-超几何表达式 IR 自动构造对角移位模块，合并可精确识别的有理倍数，处理相关分量相消；一般耦合对象可以直接提供其数学移位矩阵。|
|验收与旧入口|统一 `solve_core.py` 接入两个入口；专项、旧求和/联合回归及六个 CLI 样例记录见本阶段报告。旧报告与 Train 基线不覆盖。|

### 输入、输出与使用

`parameterized_q_system` 求解

```text
σ_k(r) V - r = Σ_j c_j h_j，c_j∈K，r∈K(X)^(1×d)。
```

输入只有 `k_matrix` 和 `rhs_basis`（右端行列表）。输出 `solution_basis` 是 `(c,r)` 的完整 K 线性解空间基；可包含 `c=0` 的齐次方向。`constructed` 要求存在非零 c；如果仅有齐次方向，标 `no_relation_in_declared_basis` 并保留这些方向，不能误当非零伸缩算子。

`q_holonomic` 接收 `n_matrix`、`k_matrix`、`observable`，或单独的 `summands` 表达式列表。对 `H=hY`，计算

```text
Σ_j c_j(Q) σ_n^j(hY) = Δ_k(rY)。
```

一般耦合输入示例：

```json
{
  "schema_version": 1,
  "solver": "q_holonomic",
  "input": {
    "n_matrix": [[0,1],[["add",1,["mul","Q","X"]],0]],
    "k_matrix": [[0,1],[["add",1,["mul","Q","X"]],0]],
    "observable": [1,0]
  }
}
```

该例自动得到 `L=E_n-1`、证书行 `[1,0]`。另一个耦合样例 `core_holonomic_order2.json` 的两个移位矩阵不同，算法得到二阶算子 `[6,-5,1]` 和两个非零证书分量；不是只核验用户提供的关系。

所有矩阵元素沿用精确算术树，不接受可执行字符串、目标答案、证书或猜测的分母/次数。输出含规范化输入、移位相容性残差、逐阶右端行、各坐标消元与界的推导、线性系统规模、首一及多项式化关系。`result.certificate_row` 对应首一关系；`primitive_relation.certificate_row` 对应顶层多项式 `operator`。

在 `finite_product_framework/` 目录运行：

```bash
python3 solve_core.py --input p1/examples/core_holonomic_coupled.json --output generated/holonomic_core_20261014/holonomic_coupled.json --max-order 3 --seconds 60
python3 solve_core.py --input p1/examples/core_holonomic_gauge.json --output generated/holonomic_core_20261014/holonomic_gauge.json --max-order 3 --seconds 60
python3 solve_core.py --input p1/examples/core_holonomic_order2.json --output generated/holonomic_core_20261014/holonomic_order2.json --max-order 3 --seconds 60
python3 solve_core.py --input p1/examples/core_holonomic_cancellation.json --output generated/holonomic_core_20261014/holonomic_cancellation.json --max-order 3 --seconds 60
python3 solve_core.py --input p1/examples/core_holonomic_source.json --output generated/holonomic_core_20261014/holonomic_source.json --max-order 3 --seconds 60
python3 solve_core.py --input p1/examples/core_rational_system.json --output generated/holonomic_core_20261014/rational_system.json --max-order 3 --seconds 60
python3 -m unittest discover -s p1 -p test_holonomic_core.py -v
```

### 分母界为何覆盖所有有理证书

这部分说明实现所用的保守界，便于代码审查；不是 Lean 形式化证明。消元后将系数及**每个**参数化右端列一起清分母，得到

```text
Σ_(i=0)^m a_i(X) y(q^i X) = Σ_j c_j b_j(X)，a_0 a_m ≠ 0，a_i,b_j∈K[X]。
```

设 `σ(p)(X)=p(qX)`，去掉首尾系数的 X 因子。任何非零不可约因子 p 的 q 移位轨道上，y 的极点指标范围有限，记最小、最大指标为 l、u。

1. 在轨道最左端 l，只有 `a_0 y` 可能有未被抵消的极点，故 `σ^l(p)` 必须整除 `a_0`；在最右端 `u+m`，只有 `a_m σ^m(y)`，故 `σ^(u+m)(p)` 必须整除 `a_m`。
2. 因而 `u-l ≤ N`，其中 `N=max{j≥0:gcd(a_m,σ^j(a_0))≠1}-m`。集合通过现有精确 q 移位因子识别计算。集合为空或 N<0 时没有非零有限极点。
3. 设 y 在位置 t 的极点重数为 e_t。由原方程在该处的赋值比较，`e_t ≤ val_t(a_0)+max(0,e_(t-1),…,e_(t-m))`。从 l 归纳可得它不超过从 l 到 t 的 `a_0` 因子重数之和。
4. 因而 `D=∏_(j=0)^N σ^j(a_0 / X^val_X(a_0))` 同时覆盖这些极点及重数。D 可以偏大，但不遗漏合法证书；它不是声称最低次数的分母。零点 X=0 的特殊轨道单独处理。

写 `y=f/D` 后，f 只能是 Laurent 多项式。再次清分母所得系数记作 `A_i`。令 `v=min_i val_X(A_i)`，`d=max_i deg_X(A_i)`，构造

```text
I_0(T)=Σ_i [X^v]A_i * T^i，I_∞(T)=Σ_i [X^d]A_i * T^i。
```

如果 f 的最低/最高次数超过由右端列次数给出的普通界，对应首尾项必须抵消，即 `I_0(q^l)=0` 或 `I_∞(q^u)=0`。实现对指示多项式在 K 上精确因式分解：`q^e∈K`，因此每个可能的整数幂根都出现在一次因子中，再用精确 q 幂识别取得全部整数 e，不设猜测半径。将这些共振与所有右端列的普通界合并；零右端只保留共振允许的区间。

矩阵标量化只提供必要界，最终解仍由**原耦合方程**决定：设 `A=(V^T)^(-1)`，`G=A[h_0^T,…]`，则 `σ(y)=Ay+Gc`。每个坐标递推记录状态行与强迫项行；解空间中的任意真实有理 y 必在所导出的有限 ansatz 中。把 ansatz 代回原方程后求完整零空间，既没有漏掉域内有理解，也不会把只满足标量必要条件的伪解接收。

算法背景参考 [Abramov–Bronstein–Petkovšek–Schneider：参数化差分方程的有理解、分母界与次数界](https://arxiv.org/abs/2005.04944)，以及 [HolonomicFunctions 的耦合差分系统与创造性伸缩说明](https://risc.jku.at/sw/holonomicfunctions/)。上述移位乘积界和具体实现由本项目自行推导、实现；没有声称调用这些软件或实现整个差分域理论。

### 源表达式归并、边界和验收语义

`summands` 模式从已有表达式 IR 导出每个基分量的 U、V。若 `F_i/F_j` 经现有精确有理化可表示为 `K(X)`，且反代回原商后的符号残差为零，就把它们合并为同一个状态的有理权重。输入 `2^n,-2^n` 因而得到零 observable 和零阶关系；源映射及倍数写入 `source_frontend`。未合并的分量不被宣称线性无关，也不宣称发现任意特殊函数之间的全部关系。

直接输入矩阵时，其与具体对象的对应关系仍是输入前提，标 `input_module_equations_are_premises=true`；从源 IR 导出时明确记录来源。有限和边界、初值、特化奇点和原声明 Lean 组装属于此前排除的后续层，本阶段不计原题成功。

`--max-states` 控制模块秩，`--max-unknowns` 控制所有坐标 Laurent 未知数加共享右端系数的总数，`--max-normal-form-degree` 控制派生分母及清分母后的多项式次数。分母移位乘积展开前先检查预测次数。外层 `--max-order` 默认为无固定上限，统一 `core.solve`/CLI 提供硬进程时间预算；直接低层函数没有独立墙钟保护。

`no_relation_in_declared_basis` 是完成固定基有理系统后的结论；`search_exhausted` 只表示所设递推阶数内失败；`resource_exhausted` 是资源中止。三者都不能解读为原题不可证明。一般奇异移位矩阵、单位根/数值 q、多求和指标、从任意 Ore 理想自动生成有限基的 Gröbner 前端，以及不属于现有表达式 IR 的任意对象定义，不在这套核心输入契约内。

本阶段核验记录见 [validation.json](../generated/holonomic_core_20261014/validation.json)：25项新专项、38项旧核心/联合回归、6个CLI样例全部通过。专项覆盖极点方向/重数/非线性不可约因子、正负共振、高阶标量化、二维与三维耦合、完整齐次解方向、原矩阵残差、等价有理基变换、源相消、预算与篡改拒绝。六个结果文件另行检查输入/源码哈希、首一与规范化证书残差及源分量归并。测试支持实现的正确性判断，不替代算法的形式化证明。

## 2026-10-14：第三阶段第一步——多分量联合创造性伸缩

以下保存第一步完成时的实现记录；其中“尚未实现耦合系统”的状态已由上方本阶段完成记录更新。

统一入口新增 `q_zeilberger_joint`，实现见 [qjoint.py](qjoint.py)。这是已有 q-Zeilberger 路线的算法增强，支持有限个 q-超几何分量的共同伸缩关系；仍只有一个求和指标 k，未实现耦合矩阵系统或一般多重求和。

设分量 `F_i(n,k)` 的移位比为 `U_i=F_i(n+1,k)/F_i(n,k)`、`V_i=F_i(n,k+1)/F_i(n,k)`。逐阶自动寻找一组共享的 `c_j(Q)` 和每个分量的有理函数 `R_i(Q,X)`，使

```text
Σ_j c_j(Q) F_i(n+j,k) = Δ_k(R_i(Q,X) F_i(n,k))  （每个 i）
因此 L(Σ_i F_i) = Δ_k(Σ_i R_i F_i)。
```

这一步从输入的求和分量构造系数与证书，无须提供对象递推或候选证书。它与第二阶段 Ore 闭包所需的“已知序列递推”输入不同；有限求和后的边界与初值仍不在本阶段处理。

### 算法构建

1. 对每个分量检查两个方向移位相容，即 `U_i V_i(qQ,X)=V_i U_i(Q,qX)`，并计算各阶 n 移位比。
2. 将 [qparameterized.py](qparameterized.py) 中原有的单分量 Laurent 方程构造抽成公共块构造器。每个块自动计算公共分母、Gosper 正规形及 Laurent 次数界；不输入猜测分母或猜测次数。
3. 所有块共用同一组 `c_j`，各自保留独立的 Laurent 未知数。合并全部方程后求精确零空间，排除共享系数全零的解，要求最高阶系数非零。不能先从每个块选一组证书再比较，否则可能丢掉可共同满足的解。
4. 同步规范化递推和全部证书，逐分量检查首一关系及多项式化关系残差。公共缩放因子作用于每个 `R_i`。

旧 `parameterized_q_gosper` 和 `q_zeilberger` 通过单块适配继续使用同一构造器；旧证书及 Laurent 解字段保留。联合模块没有以逐分量独立求递推再求公左倍式代替联合系数求解。

### 输入和复现

```json
{
  "schema_version": 1,
  "solver": "q_zeilberger_joint",
  "input": {"components": [
    {"summand": ["pow", "a", "n"]},
    {"summand": ["pow", "b", "n"]}
  ]}
}
```

该例自动得到共同算子 `[a*b,-a-b,1]`，对应两个几何分量的二阶关系。每个 component 也可以只提供 `n_shift` 和 `k_shift` 算术树；这两种格式可以混用。只接收 `components`，拒绝目标答案、候选证书或额外提示字段。零 summand 分量会被保留在输出索引中，证书为零；全零输入直接返回零阶算子 `[1]`。

在 `finite_product_framework/` 目录运行：

```bash
python3 solve_core.py --input p1/examples/core_joint_geometric.json --output generated/joint_core_20261014/geometric.json --max-order 3 --seconds 60
python3 solve_core.py --input p1/examples/core_joint_binomial.json --output generated/joint_core_20261014/binomial.json --max-order 3 --seconds 60
python3 solve_core.py --input p1/examples/core_joint_order_zero.json --output generated/joint_core_20261014/order_zero.json --max-order 3 --seconds 60
python3 solve_core.py --input p1/examples/core_joint_three_components.json --output generated/joint_core_20261014/three_components.json --max-order 3 --seconds 60
python3 -m unittest discover -s p1 -p test_joint_core.py -v
```

Gaussian 样例的两个分量分别为 `Gaussian(n,k) * 2^k * q^(k(k-1)/2)` 和将 `2^k` 换成 `3^k` 的分量。联合搜索得到两个非零有理证书，共同算子为

```text
[6*Q^2*q + 5*Q*q + q, -5*Q*q - q - 1, 1]。
```

这是局部伸缩关系；本次没有执行有限和端点求值。该 CLI 样例本次约 16.6 秒，其余三个约 0.4–0.6 秒，时间只代表这些具体输入与环境，不代表 Train 性能。

### 输出与边界

- `coefficients/certificates` 保存首一关系，`primitive_relation` 保存共同多项式化系数和同步缩放后的证书列表；顶层 `operator` 使用后者。
- `active_component_indices` 绑定非零分量与原始输入位置，顶层证书列表恢复为完整输入顺序。`attempts` 保存逐阶的各块正规形、次数界和总线性系统规模。给了 summand 时还输出对应的 `operator_certificate_term_expressions`；仅给移位比的分量在该字段为 `null`。
- 复用统一入口的硬进程超时；`--max-states` 限制对角分量数，`--max-unknowns` 对共享系数加所有块的 Laurent 未知数总数计数，`--max-normal-form-degree` 限制各块正规形。超过限制只报 `resource_exhausted`。
- 未找到共同关系时按阶数继续搜索；达到指定阶数只报 `search_exhausted`。当前分量独立处理，不发现分量之间的有理等价、线性相关或相消。例如 `2^n + (-2^n)` 的和为零，本算法仍会逐分量寻求 `E-2`；零阶搜索失败不表示这个和不存在零阶关系。因此不能把当前求出的阶数宣称为总和的最低阶。
- 尚未实现非对角耦合矩阵差分方程的分母/次数界、跨分量约化、完整 q-holonomic 创造性伸缩。有限和边界、初值、原参数域特化和 Lean 组装继续留给后续层。

18 项联合专项及 55 项旧算法回归通过，4 个 CLI 样例通过；[验证记录](../generated/joint_core_20261014/validation.json)。本轮不重跑 Train、不读取 Test、不执行 Lean；`constructed` 始终不代表原题 `proved`。第一、二阶段报告保留为各自版本的历史记录。

## 2026-10-14：独立核心求解器

本阶段只建设单基 q 求和核心算法，不扩展 Lean 前端或验证器，不批测 Train、不读取 Test。复用已有 q-Gosper 正规形、精确移位集合和 Laurent 次数界；不是重新实现已有算法，也不是把十二类流程宣称为全部完成。

### 输入与输出契约

入口 `../solve_core.py` 调用 [core.py](core.py)，接收 JSON 数学输入。根字段只允许 `schema_version: 1`、`solver`、`input`；不接收目标答案、证书、候选分母或猜测次数。下列三种 solver 属于同一条 q 求和主线。后续第二阶段还接入了 `q_ore`，其输入和边界另见 [Ore 核心契约](branches/ore_closure.md)：

|solver|input|核心输出|
|---|---|---|
|`q_gosper`|`summand`，或向前移位比 `k_shift`|R，使 V(X)R(qX)-R(X)=1；即 G=RF 的局部反差分|
|`parameterized_q_gosper`|`k_shift` 和非空 `rhs_basis`|不全为零的 c_i 及 R，使 V(X)R(qX)-R(X)=Σc_i b_i(X)，c_i 不依赖 X|
|`q_zeilberger`|`summand`，或 `n_shift` 与 `k_shift`|阶数、递推系数及证书；首一表示与多项式化表示同时保留|

移位坐标为 X=q^k、Q=q^n。比例输入使用精确整数、符号及 `add/mul/sub/div/neg/pow` 算术树；`pow` 指数须是整数字面量，不执行 Python 表达式字符串。`summand` 复用原有 `expressions.py` 数学语法，支持其已有 Pochhammer/Gaussian/幂及乘积表示，不表示已接入任意 Lean 定义。

系数域为 QQ(q,Q,其他独立参数)(X)，q 是不定元、特征为零。原始表达式中约消前的奇点及参数特化不由此接口处理；输出的 `normalized_input_denominators` 是正规化后输入的分母，不能当作原声明的全部定义域。即使证书在该形式域中成立，也不声称 q=0、单位根或任意特征下的原题已被证明。

### 算法流程

q-Gosper 沿用下文已有正规形和算法次数界；补上非有限值/浮点输入拒绝，以及在展开长移位乘积之前对推导出的正规形次数进行资源检查。该限制只产生 `resource_exhausted`。

新增 [qparameterized.py](qparameterized.py) 统一处理参数化问题：从所有 b_i 自动计算关于 X 的公共分母 D，对 H=F/D 应用原 Gosper 正规形，逐项推导右端 P D b_i 的 Laurent 界，再精确求解 c_i 和 Laurent 系数的联合系统。零右端显式处理；c 全为零的齐次解不能当作递推证书。结果代回完整有理关系检查残差。

[zeilberger.py](zeilberger.py) 复用这个共享内核。先检查 U(Q,X)V(qQ,X)=V(Q,X)U(Q,qX)，再按阶数构造所有 n 移位比并求非零最高递推系数。核心入口从零阶开始，`max_order=null` 时按阶数推进至成功或资源耗尽；旧证明入口保留原来的默认最低阶数和首一结果字段，避免改变现有重建接口。

递推系数清分母、除公共多项式因子时，证书按相同比例缩放，并再次检查符号关系。`operator` 使用这个多项式化关系；`leading_coefficient` 的零点明确保留，不静默添加它非零的假设。`certificate_term_expression` 对应首一关系，`operator_certificate_term_expression` 对应多项式化关系，两者均不进行有限求和端点求值。

独立核心入口用子进程强制执行时间预算，覆盖因式分解、正规化和线性求解。不要把直接调用低层 `compute/search` 当作有进程超时保护的公共 API；公共 API 是 `core.solve` 或 CLI。未知数上限和正规形次数上限是资源限制，均不产生不可解结论。

### 运行示例

在 `finite_product_framework` 目录运行：

```bash
python3 solve_core.py --input p1/examples/core_qgosper.json --output generated/core_solver_20261014/qgosper.json
python3 solve_core.py --input p1/examples/core_qzeilberger.json --output generated/core_solver_20261014/qzeilberger.json
python3 solve_core.py --input p1/examples/core_qzeilberger_order5.json --output generated/core_solver_20261014/order5.json
python3 solve_core.py --input p1/examples/core_parameterized.json --output generated/core_solver_20261014/parameterized.json
python3 p1/test_core_solver.py
```

默认时间 30 秒、未知数 10000、正规形次数 10000，递推阶数默认不设固定上限；可以显式指定 `--max-order`。进程启动也计入时间预算。输出保存输入哈希、核心源码哈希、预算和版本。

### 状态与完成边界

- `constructed`：已计算并通过精确代回的局部符号证书；不是原恒等式 `proved`。
- `no_solution_in_class`：q-Gosper 在声明的形式域与解类中完成算法判定；不排除特殊参数或其他解类。
- `no_relation_in_declared_basis`：所给右端基的联合系统没有所需非零系数关系。
- `search_exhausted`：达到指定递推阶数，没有找到关系；不表示所有阶数均不存在。
- `resource_exhausted`：时间、未知数或正规形资源限制。
- `unsupported_domain/unsupported_input/invalid_input`：系数域、数学语法或输入契约不支持；`implementation_error/worker_failed` 单列实现故障。

新专项测试覆盖参数化右端、负 Laurent 次数、零/一/二/三/五阶关系、奇异首项系数保留、错误移位比、输入提示拒绝、精确无解和进程超时回收；见 [tests.json](../generated/core_solver_20261014/tests.json)。旧 17 项 q-Gosper 回归同时通过。

本阶段未完成：有限求和边界及初值闭合、参数特化、任意符号序列前端、完整 q-holonomic／差分环／有理 Omega 算法。高阶、多参数精确线性系统仍可能很慢；完成算法主线不等于性能完备或全输入保证终止。下一阶段需根据明确规格分别补强这些能力，不用固定尺寸枚举替代符号 n。

## 此前 q-WZ 接入记录

首分支按原方案实现：目标引导的 q WZ 证明路线调用 q Gosper 构造原差分，再处理边界、初值和 Lean 证明。原有界有理式搜索已退出主流程，保存在 archive/bounded_search；不作为失败后的回退。

## 算法来源与实现范围

[qgosper.py](qgosper.py)用 SymPy 精确代数实现 q Gosper 的正规化、移位消去、Laurent 次数界和线性方程求解。算法步骤参照 REDUCE QSUM 的 qgosper_qupdate、qgosper_qdegreebound、qgosper_qfindf；[官方说明](https://reduce-algebra.sourceforge.io/manual/manualse172.html)描述其 q 超几何原差分构造用途。已保存[源码快照](references/qsum.red)、[来源及哈希](references/source.json)和[许可证](QSUM_LICENSE.txt)。本次执行的是 Python 实现，没有运行 REDUCE 或 Mathematica。

支持系数域为 Q(q, parameters)，q 和其他参数视为独立不定元，求和移位变量为 x=q^k。输入须为精确有理函数；数值底数、代数扩张、超越函数系数不在本版范围。拒绝这些输入不表示原差分不存在。

此处完成的是该域上的符号构造算法实现及测试，不是算法正确性的 Lean 形式化，后端单独运行不构成有限求和恒等式的完整形式证明。原生 Lean 入口另以原定义验证所有局部关系，首例已覆盖原参数域（含 q=0 和单位根），不依赖形式分母的非零假设。

## q WZ 调用

从输入表达式计算 U=F(n+1,k)/F(n,k)、V=F(n,k+1)/F(n,k) 和 c=T(n+1)/T(n)，令 W=U−c，D=WF。

如果 W=0，局部差分为零，返回零证书。否则自动得到 D 的向下移位比：

    r(x) = D(n,k)/D(n,k−1) = V(x/q) W(x)/W(x/q).

将 r 交给 q Gosper；它返回 S=G/D 后，自动取 R=SW，并独立复核 V(x)R(qx)−R(x)=W(x)。不预填 R、G、分母、递推或局部证明。

## 正规化与移位消去

计算 r 的分子分母在系数域上的不可约因子。对同次数且常数项非零的一对因子 f、g，若 f(x) 与 g(q^j x) 成比例，其首尾系数比必须为 q^(j deg f)。精确识别这个 q 幂，再验证多项式等式，得到所有非负移位 j。x 因子作为 Laurent 单位处理，不需要枚举移位半径。

对每个移位使用 gcd 消去，构造

    r(x) = P(x)/P(x/q) * A(x)/B(x),

使 A(x) 与 B(q^j x) 无非平凡公共因子。实现会重新检查表示等式和消去后的移位集合。

## Laurent 方程与次数界

求解

    A(qx) f(x) − B(x) f(x/q) = P(x).

f 是 Laurent 多项式，允许负次数。上下界由 P、A、B 的最高/最低次数计算；当 A、B 对应次数相同，还检查首尾系数抵消所对应的整数 q 幂。由此得到有限区间 [L,H]，建立全部未知系数的线性方程，一次求解。

次数界来自算法，不再提供 max_degree、shift_radius 或题目分母接口。通用时间和未知数数量限制只控制资源；超过时报告 timeout/resource_exhausted，不能报告无解。

求出 f 后构造 S(x)=B(x)f(x/q)/P(x)，并验证 r(qx)S(qx)−S(x)=1，再返回 q WZ 层。若精确次数区间为空或完整系数方程不相容，则在所支持的形式域与 q 超几何原差分类内报告 no_q_hypergeometric_antidifference；它不表示原有限恒等式不可证明，也不排除特殊参数下另有解。

## 验证与剩余工作

17项测试覆盖：输入变化、拒绝证明提示、不按题目ID选证明、移位13、超出旧次数上限、负Laurent解、独立构造的有理差分、QSUM示例、无原差分判定、资源限制和不支持的域。每个成功结果均独立检查有理恒等式。

首例结构化公式已通过新版构造，详见[运行报告](generated/symbolic_run.json)。原生入口现已从 Lean Expr 提取输入并完成首例的局部、边界、初值和目标递推证明，该目标引导分支的自动训练证明数为1；见[原目标报告](generated/runs/FQI-FINITE-Q-BINOMIAL/report.json)。覆盖限于 README 中的受限语法与改写规则，其他目标的原域桥接仍可能失败。

## 直接求和调用

新增 direct.py 直接以 F(k)/F(k−1) 调用同一 q-Gosper 后端，计算 G/F；Gaussian 邻接表示仅用于搜索结果的 Lean 回译，不参与算法次数界或分母计算。Gaussian 加权 hockey-stick 的 Laurent 次数界由算法得到 −1，局部差分和真实端点由 Lean 验证。见 [分支报告](generated/runs/FQI-SRC-AP-3.3.9/report.json)。首例 q-WZ 路线继续保留，两者共用原目标与公理审计。
