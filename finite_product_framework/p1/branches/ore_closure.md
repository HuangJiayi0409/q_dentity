# P1：q-Ore 算子闭包与消元

## 2026-10-14：独立核心第二阶段

在既有 `ore.py` 上补齐单变量算子代数，并通过 [ore_core.py](../ore_core.py) 接入 [solve_core.py](../../solve_core.py)。此接口自动构造算子与乘数、Bezout 或状态行向量见证。它接收精确数学输入，不读取 benchmark，不执行 Lean。下方 Rogers–Szegő 原生证明是此前版本的记录，不是本次新增覆盖。

系数域为 `QQ(q,Q,独立参数)`，`Q=q^n`，`E a(Q)=a(qQ) E`，系数数组按 `E` 次数升序排列。`q` 是不定元。系数使用第一阶段的整数、符号和 `add/mul/sub/div/neg/pow` 算术树；禁止浮点、代数字常量、代码字符串和目标证书字段。`X` 保留给求和变量，不能作本入口系数。

|operation|输入字段|自动构造与精确检查|
|---|---|---|
|`right_division`|`a`, `b`|右侧除数：`a=quotient*b+remainder`；余式阶数小于 `b`。|
|`left_division`|`a`, `b`|左侧除数：`a=b*quotient+remainder`；消去最高项时使用逆移位。|
|`gcrd`|`a`, `b`|扩展右欧几里得算法；首一最大公右因子 `G=U*a+V*b`，同时给出 `a=A*G,b=B*G`。|
|`lclm`|`a`, `b`|复用逐阶精确零空间算法，构造最低阶公左倍式 `L=U*a=V*b`；未知系数使用独立 Dummy，避免与参数同名。|
|`normalize`|`a`|清分母、去多项式公因子、规范化标量，输出缩放因子及最高阶多项式。|
|`closure`|`sequences`, `observable`|从多个递推的 companion 直和构造按次数分块的多项式状态空间，再以移位行向量相关性消元。|

零算子约定：`gcrd(0,0)=0`，任一输入为零时 `lclm=0`；零算子的阶数输出为 `null`。除数为零拒绝。闭包的输入递推必须是正阶齐次递推；非齐次递推与零阶序列描述暂未接入。零 observable 的湮灭算子为 `[1]`，不是零算子。

### 多对象闭包输入

```json
{
  "schema_version": 1,
  "solver": "q_ore",
  "input": {
    "operation": "closure",
    "sequences": {"f": [-2, 1], "g": [-3, 1]},
    "observable": ["add", 1, ["seq", "f", 0], ["pow", ["seq", "g", 0], 2]]
  }
}
```

这里的输入前提是 `f(n+1)=2f(n)`、`g(n+1)=3g(n)`；算法自动为 `h(n)=1+f(n)+g(n)^2` 算出 `[-18,29,-12,1]`，即 `h(n+3)-12h(n+2)+29h(n+1)-18h(n)=0`。输入没有提供此结果。任意初值均适用，但没有声称这些输入递推对应某个特定原题。

`["seq",名称,j]` 表示 `f(n+j)`。非负整数移位通过状态矩阵迭代计算；负移位需要该对象递推常数项非零，在有理函数域中用逆移位矩阵计算。observable 支持多对象和、积、非负整数幂、常数项和有理系数，允许不同总次数。序列变量出现在分母中时标 `unsupported_input`。代数参数可以与内部临时变量同名。

构造只为实际出现的齐次次数建立状态块；次数 `d`、基础维数 `r` 的块有 `binomial(r+d-1,d)` 个状态。输出含输入状态布局、输入/闭包转移矩阵、单项式指数、observable 行、逐次移位行及消元算子。首次线性相关给出该形式状态模块的最低阶关系；给定序列若还满足额外关系或特殊初值，实际最低阶可能更低。

### 域、预算与输出语义

- `result` 保留原始算子及其见证；顶层 `operator` 是清分母后的多项式算子，用 `scaling_factor` 与原始算子相连。不要把未缩放的乘数与顶层算子直接比较。
- `domain` 记录规范化输入和输出见证遇到的分母、输入及输出最高阶系数。该列表不是全部整数移位的特化条件，也不恢复输入约分前被消掉的因子；只主张一般有理函数域结果。
- 同一个统一入口提供硬进程时间预算。`--max-states` 默认 128，控制基础和多项式闭包维数；`--max-unknowns` 控制输入系数个数、公左倍式未知数个数和单次 observable 移位幅度。`--max-order` 仍用于 q-Zeilberger，不限制本阶段 Ore 消元。资源不足返回 `resource_exhausted`，不推断无解。
- closure 的输入递推是明确的前提，记录 `input_recurrences_are_assumptions=true`。第一阶段 q-Zeilberger 的局部求和项关系，必须另行处理有限和边界，才能作为真实齐次序列递推；当前接口没有跳过这一步自动串接。
- `constructed` 表示符号构造成功，始终 `original_identity_proved=false`。原序列递推的来源、初值、特化奇点和原题组装仍需后续层处理。未实现多变量 Ore Gröbner 基、一般 q-holonomic 创造性伸缩或序列商的闭包。

### 复现

在 `finite_product_framework/` 下运行：

```bash
python3 solve_core.py --input p1/examples/core_ore_gcrd.json --output generated/ore_core_20261014/gcrd.json
python3 solve_core.py --input p1/examples/core_ore_lclm.json --output generated/ore_core_20261014/lclm.json
python3 solve_core.py --input p1/examples/core_ore_closure.json --output generated/ore_core_20261014/closure.json
python3 solve_core.py --input p1/examples/core_ore_shift.json --output generated/ore_core_20261014/shift.json
python3 -m unittest discover -s p1 -p test_ore_core.py -v
```

18 项 Ore 专项、20 项第一阶段核心回归、17 项旧求和回归通过；4 个新 CLI 样例均构造成功。测试以独立算子作用、Bezout/整除等式、状态多项式变换和递推残差核验结果，另含参数名冲突、奇点、零算子、不支持输入与预算情形。完整记录见 [validation.json](../../generated/ore_core_20261014/validation.json)。本轮没有 Train 重跑、Test 读取或 Lean 编译。

## 此前原生证明分支

这是 P1 内的新构造分支，与 q-WZ、直接 q-Gosper、一般 q-Zeilberger、双基 Gosper 共享原声明导出、有限求和组装及公理审计。首个完整目标为 `FQI-SRC-GR2-7.Ex40`，Rogers–Szegő 有限 Turán 恒等式。旧表中的 R14/T53 是候选分布，不是本分支覆盖数量。

## 构造内核

[ore.py](../ore.py) 实现有理函数系数上的单变量 q-Ore 运算，σ(Q)=qQ，E·a(Q)=a(qQ)·E。未知数与阶数的预算是资源限制，不能解释为数学不可证。

- 非交换算子加法、乘法，以及带乘数见证的公共左倍数 L=U·A=V·B。公共倍数通过逐阶精确线性系统构造。
- 从递推系数计算 companion 状态矩阵；直和与张量积组织和、不同对象的乘积。
- 枚举固定总次数的单项式状态，构造齐次多项式闭包矩阵。枚举量按组合数检查预算，不枚举整个指数立方体。
- 对指定多项式对象生成移位行向量，通过线性相关消去状态，输出标量递推及行向量见证；也可保留指定强迫项，搜索非齐次关系。

这些运算采用 [holonomic/Ore 闭包与消元方法](https://www1.risc.jku.at/sw/holonomicfunctions/)；本项目使用 Python/SymPy 独立实现，没有安装或调用 HolonomicFunctions。构造算法本身未在 Lean 中形式化，使用的结果必须另经验证。

## 原生输入与首例

[ore_pipeline.py](../ore_pipeline.py) 识别原目标中的定义对象和有限和。当前对象原子为冻结定义中的 `rogersSzego`：另行展开其实际 Lean 定义并导出 Gaussian 求和项，再调用现有一般 q-Zeilberger。定义递推不是预写的对象规则，也不导入原题证明。目标左端仅用于确定要进行闭包的多项式对象；右端权重不参与定义递推或 Ore 强迫关系的搜索。

首例的实际运行生成二阶对象递推、三维二次状态系统、两个三阶消元算子，以及用于最终有限求和的一阶非齐次关系。它们均写入[原题报告](../generated/runs/FQI-SRC-GR2-7.Ex40/report.json)。生成器重新检查底层 q-Zeilberger 证书、状态矩阵、消元算子和非齐次关系的精确残差。

完整 Lean 证明使用计算出的对象递推与非齐次关系；三阶算子作为已作 CAS 残差检查的消元产物保存，不宣称已生成独立的通用 Lean 算子语义证明。公共左倍数已有内核和回归，双侧求和比较的原生出口尚未接通。

## 原声明如何闭合

1. 复用 q-Zeilberger 的局部 Gaussian 证书验证和真实有限支撑求和，仅输出对象递推，无须先给求和值。
2. 将自动计算的乘积关系回译，Lean 从已证对象递推直接验证局部多项式等式。
3. 从实际右端提取外因子和三角区间权重，验证权重移位与新增尾项。公共 `triangular_recurrence` 组装右端递推。
4. 在原定义上证明初值，再归纳比较；公共 `sum_Icc_reverse` 完成原 Icc 区间重编号，整数幂仅在已证非负的实际区间转换。
5. 编译完整原声明并审核公理，成功且无剩余义务才计入 train 证明。

没有新增 x≠0 假设；权重保留自然数次幂，不把 x^(m+1−j) 转成需要除以 x 的商。非零 Pochhammer 条件由原声明已有的 regular q 推出，原 statement 与 benchmark 文件不变。

## 运行、验证和边界

```bash
# 在 finite_product_framework/p1 中运行
python3 run.py --identity FQI-SRC-GR2-7.Ex40
python3 run.py --identity FQI-SRC-GR2-7.Ex40 --branch ore_closure
python3 test_ore.py
python3 check.py
```

[生成证明](../generated/runs/FQI-SRC-GR2-7.Ex40/Proof.lean)、[分支回归](../generated/ore_tests.json)、[统一验收](../validation.json)。回归涵盖 Ore 非交换乘法、公共左倍数见证、二/三次闭包和消元、直和/张量积、资源及精确系数域、改名、三倍对象及权重、错误右端、缺失底数条件，以及底层证书/强迫关系/消元算子篡改。合成检查不计训练覆盖。

当前原生出口限：可由现有几何 Gaussian 二阶出口验证定义递推的对象；二次多项式观察量，最小对象指标 n−1；Icc 1 n 上的同对象平方加权和；能够闭合的一阶强迫关系和现有 Pochhammer 权重。原子登记、结构判断及通用规则允许复用，禁止按题目 ID 选择递推、矩阵、证书或最终证明。

任意定义对象、多对象原生闭包、高阶强迫关系、公共算子的奇点处理及两侧非齐次项比较仍待实现。构造失败、资源耗尽、表示缺口及 Lean 未闭合分别报告；不把 R14/T53 候选全部标为已证明。
