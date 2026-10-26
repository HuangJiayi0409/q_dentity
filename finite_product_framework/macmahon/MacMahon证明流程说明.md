# MacMahon 分拆分析：矩形分拆恒等式的完整证明流程

本文说明当前已经实现并通过 Lean 验证的证明：从矩形分拆的有序链约束出发，构造形式生成函数，消去链约束，识别 Gaussian 系数，最后证明 benchmark Train 中的原始声明。

实现及验证状态对应 2026-10-13。核心代码见 [Rules.lean](lean/Rules.lean)，自动执行逻辑见 [pipeline.py](pipeline.py)。当前方法是**有序链的专用分拆分析流程**，尚不是任意线性约束的通用 MacMahon 消元器。

## 1. 要证明什么

Train 题目 `FQI-RECTANGLE-PARTITIONS` 要求证明

$$
\begin{bmatrix}n\\k\end{bmatrix}_q
=\sum_{n-k\geq\lambda_1\geq\cdots\geq\lambda_k\geq0}
q^{\lambda_1+\cdots+\lambda_k},\qquad k\leq n.
$$

右边枚举装在宽为 $n-k$、高为 $k$ 的矩形内的分拆，允许补零。原始 [Lean 声明](../../benchmark/lean/Benchmark/Statements/Train/Identity006.lean) 是：

```lean
variable {K : Type*} [Field K]
theorem statement (q : K) (n k : ℕ) (hk : k ≤ n) :
    gaussian q n k = rectangleWeight q (n-k) k := by
  macmahon_chain
  done
```

这里 $K$ 是任意域，$q$ 是任意元素。没有增加 $q\ne0$、$q\ne1$、非单位根或特征零假设。

特别要注意，[gaussian 的定义](../../benchmark/lean/Benchmark/Definitions.lean) 是递归定义的多项式：

$$
G_q(n,0)=1,\quad G_q(0,k+1)=0,
$$
$$
G_q(n+1,k+1)=G_q(n,k)+q^{k+1}G_q(n,k+1).
$$

因此不需要把 Gaussian 写成可能出现零分母的有限乘积商。

## 2. 整体路线与首版缺口

令

$$
R_q(a,b)=\sum_{a\geq\lambda_1\geq\cdots\geq\lambda_b\geq0}
q^{\lambda_1+\cdots+\lambda_b}.
$$

只需先证明 $R_q(a,b)=G_q(a+b,b)$，再代入 $a=n-k$、$b=k$。

完整路线是：

```text
矩形分拆加权和 R_q(a,b)
    ↕ 已证明的 Omega 约束编码
非负指数投影
    ↓ 分离最大部件，逐层消去有序链约束
F_b(t) = Σ_{a≥0} R_q(a,b)t^a
    ↓ 形式生成函数因子化
∏_{i=0}^b (1-q^i t)^(-1)
    ↑ 从 Gaussian 的局部关系独立验证
H_b(t) = Σ_{a≥0} G_q(a+b,b)t^a
    ↓ 比较 t^a 的系数
R_q(a,b) = G_q(a+b,b)
    ↓ 使用 k≤n 恢复原指标
Train 原始声明
```

首版只完成“分拆和等于某个 Omega 表达式”的桥接。这只是换了一种表示，尚未计算该表达式。此次补齐的是**链约束消元、生成函数因子化和 Gaussian 系数识别**，所以能回到原题结论。

## 3. 用 Omega 表示分拆约束

先允许每个部件独立取值 $0\leq\lambda_i\leq a$，暂时不施加大小顺序。对每对位置 $i\leq j$ 引入辅助变量，其指数取为

$$
e_\lambda(i,j)=\lambda_i-\lambda_j.
$$

实现中也保留 $i>j$ 的位置，其指数设为零。每个部件序列的系数仍为 $q^{\sum_i\lambda_i}$。

算子 $\Omega_{\geq0}$ 保留所有辅助指数均非负的项，再将辅助变量设为 $1$。非负条件恰好表达

$$
\lambda_1\geq\lambda_2\geq\cdots\geq\lambda_b.
$$

于是有已验证的桥接：

$$
\Omega_{\geq0}\bigl(\operatorname{rectangleEncoding}(q,a,b)\bigr)=R_q(a,b).
$$

代码对应 `rectangleEncoding`、`omegaAll` 和 `rectangle_omega`。这是有限 Laurent 编码，没有无穷展开顺序问题。

Omega 不能逐因子相乘：例如 $\Omega(\lambda^{-2}\lambda^3)=1$，但 $\Omega(\lambda^{-2})\Omega(\lambda^3)=0$。实现保持“先乘积卷积，后投影”的语义；单变量 `omegaGE` 只定义为加法同态。

## 4. 真正的消元：分离最大部件

考虑高度为 $b+1$ 的分拆，记其最大部件为 $r=\lambda_1$。剩下的 $b$ 个部件满足

$$
r\geq\lambda_2\geq\cdots\geq\lambda_{b+1}\geq0.
$$

也就是说，剩余部分是宽为 $r$、高为 $b$ 的矩形分拆。反过来，将 $r$ 放在任何这样的分拆前面，就得到原来的分拆。由此构造双射

$$
\operatorname{Rect}(a,b+1)
\simeq\coprod_{r=0}^{a}\operatorname{Rect}(r,b).
$$

Lean 中 `splitHead` 和 `joinHead` 实现两个方向，`headEquiv` 证明它们互逆，同时验证取值边界和单调性。权重满足

$$
q^{\lambda_1+\cdots+\lambda_{b+1}}
=q^r q^{\lambda_2+\cdots+\lambda_{b+1}}.
$$

因此得到消元规则 `rectangle_head_elimination`：

$$
\boxed{R_q(a,b+1)=\sum_{r=0}^{a}q^r R_q(r,b).}
$$

初始情形是 $R_q(a,0)=1$。这里证明的是任意符号参数 $a,b$ 的规则，而不是枚举若干固定矩形。

## 5. 生成函数把累加变成几何因子

引入独立的形式变量 $t$，定义

$$
F_b(t)=\sum_{a\geq0}R_q(a,b)t^a,\qquad
E_c(t)=\sum_{m\geq0}c^m t^m.
$$

它们属于形式幂级数环 $K[[t]]$。不要求 $|q|<1$ 或数值收敛；每个指定次数的系数运算只涉及有限项。

代入上一节的消元规则：

$$
\begin{aligned}
F_{b+1}(t)
&=\sum_{a\geq0}\sum_{r=0}^{a}q^rR_q(r,b)t^a\\
&=\left(\sum_{r\geq0}q^rR_q(r,b)t^r\right)
  \left(\sum_{s\geq0}t^s\right)\\
&=F_b(qt)E_1(t).
\end{aligned}
$$

Lean 的 `rectangle_series_step` 逐系数验证这个等式；代换 $t\mapsto qt$ 使用 `PowerSeries.rescale`。

初值 $F_0(t)=E_1(t)$，并且 $E_c(qt)=E_{qc}(t)$。对 $b$ 归纳便得到 `rectangle_series_factorization`：

$$
\boxed{F_b(t)=\prod_{i=0}^{b}E_{q^i}(t)
=\prod_{i=0}^{b}(1-q^i t)^{-1}.}
$$

这里有 $b+1$ 个因子，因为宽度也由 $t$ 记录，其中包括宽度的剩余空间；例如 $b=0$ 时，所有宽度的空分拆都贡献 $1$，所以生成函数仍是 $(1-t)^{-1}$。

实现首先用系数定义 $E_c$，再由 `geometric_denominator` 证明

$$
E_c(t)(1-ct)=1.
$$

`cone_denominator` 进一步验证整个乘积与分母乘积相乘等于 $1$。每个形式分母的常数项都是 $1$，因此不需要假设标量 $1-q^i$ 非零。原题证明直接比较共同的几何级数乘积，分母证书是另外验证的精确有理表示。

## 6. 为什么乘积系数就是 Gaussian

还需要独立证明 $G_q(a+b,b)$ 是上述乘积的系数，不能把待证矩形分拆恒等式作为已知事实调用。

实现使用共享的 [Gaussian 局部规则](../p1/lean/GaussianRules.lean)，其中包含从 Gaussian 定义证明的另一种 Pascal 关系：

$$
G_q(n+1,k+1)=G_q(n,k+1)+q^{n-k}G_q(n,k),\qquad k\leq n.
$$

结合对角值 $G_q(b,b)=1$，对 $a$ 归纳，得到 `gaussian_geometric_coefficient`：

$$
\sum_{r=0}^{a}q^rG_q(r+b,b)=G_q(a+b+1,b+1).
$$

定义

$$
H_b(t)=\sum_{a\geq0}G_q(a+b,b)t^a.
$$

上面的有限和公式说明

$$
H_{b+1}(t)=H_b(qt)E_1(t),\qquad H_0(t)=E_1(t).
$$

于是 `gaussian_series_factorization` 在本方法内部归纳证明

$$
H_b(t)=\prod_{i=0}^{b}E_{q^i}(t)=F_b(t).
$$

这一步确实使用局部递推关系与归纳；它没有调用已有的递推 pipeline，也没有导入原题证明。独立方法可以共享已验证的基础引理。

## 7. 提取系数并返回原题

对 $F_b(t)=H_b(t)$ 取 $t^a$ 的系数，得到

$$
R_q(a,b)=G_q(a+b,b).
$$

在 Lean 中，`omega_rectangle_evaluation` 组合两侧因子化，并使用

```lean
congrArg (PowerSeries.coeff a) h
```

提取等式两边的系数；再结合 `rectangle_omega` 得到完整 Omega 求值定理。

最后代入 $a=n-k$、$b=k$。由于原题给出 $k\leq n$，自然数减法满足 $(n-k)+k=n$，所以

$$
R_q(n-k,k)=G_q(n,k).
$$

调整等式方向即得到原始目标。`macmahon_chain` 完成相关规则的实例化和指标整理。末尾用于自然数指标的 Lean `omega` tactic 是整数算术工具，与 MacMahon 的 Omega 投影算子是不同概念。

## 8. 自动 pipeline 如何运行

入口是 [prove_macmahon.py](../prove_macmahon.py)。流程如下：

1. 读取选定 Train 题目的冻结声明，依据实际表达式判断受支持的计划，不按题号直接分发证明。
2. 构造独立 Lean 编译环境，包含冻结定义、矩形对象定义、Gaussian 基础引理、共享局部规则及本方法的规则库。
3. 对支持的链式目标生成 `macmahon_chain` 证明候选；本次成功计划为 `chain_geometric_elimination`，后端为 `finite_omega_elimination`。
4. 将候选填回原始声明，交由 Lean 检查完整证明。不会以单独通过一个中间引理代替原题成功。
5. 审计目标的公理依赖，记录源文件、依赖、证明及证书哈希，保存报告。

符号推导通过已证明的通用模板实例化完成，没有接入外部 CAS，没有自动调用其他方法作为回退，也没有实现任意约束消元规则的自动发现。

## 9. 运行与已有验证结果

从项目的框架目录运行：

```bash
cd /home/hjy/Project/finite_q_identity_catalog/finite_product_framework
python3 prove_macmahon.py --identity FQI-RECTANGLE-PARTITIONS
python3 macmahon/check.py
python3 check.py --audit-existing
```

第一条 Python 命令证明原题，第二条验证本方法专项案例，第三条审计已有方法产物。生成的 `Proof.lean` 依赖 pipeline 准备的编译环境，单独复制该文件并不包含所有依赖。

| 检查对象 | 已记录结果 | 证据 |
| --- | --- | --- |
| Train 原题 | `proved`，本次新增 1 条 Train 原题成功 | [report.json](../generated/macmahon/12f36842274642ddb30f09af60f908cd/report.json) |
| 原声明完整证明 | `macmahon_chain` 后目标全部闭合 | [Proof.lean](../generated/macmahon/12f36842274642ddb30f09af60f908cd/attempts/00_finite_omega_elimination/Proof.lean) |
| 原题证明证书 | 保存依赖及证明审计信息 | [certificate.json](../generated/macmahon/12f36842274642ddb30f09af60f908cd/attempts/00_finite_omega_elimination/certificate.json) |
| 专项检查 | 15 个模块证明通过，6 个错误目标拒绝；另验证证书篡改拒绝 | [macmahon_validation.json](../generated/macmahon_validation.json) |
| 统一已有产物审计 | 12 个方法入口审计通过 | [method_pipelines_validation.json](../generated/method_pipelines_validation.json) |
| 冻结源审计 | 346 条 Train 的 692 个源文件匹配；未读取 Test 文件 | [macmahon_source_audit.json](../generated/macmahon_source_audit.json) |

原题公理审计只包含 `propext`、`Classical.choice`、`Quot.sound`，没有 `sorryAx`。专项的 15 个模块成功不等于证明了 15 道 Train 题；已有产物审计也不等于重跑全部 Train。

全目录构建和验证另有既存缺失项：`pending16_resolutions.json` 与 Python 模块 `validate_sills`，记录见 [项目检查报告](../generated/macmahon_chain_project_checks.json)。因此这里的成功结论限定为上述 Lean 证明与专项审计，不声称整个目录构建已通过。本说明整理已有验证结果，不代表重新执行了这些检查。

## 10. 当前方法的适用边界

当前完成的是矩形分拆中任意宽高的有序链消元，以及规则库支持的有限 Omega 投影。证明同时覆盖 $q=0$、$q=1$ 和单位根等取值，因为使用多项式 Gaussian 与形式幂级数。

尚未实现一般 Elliott/CTEuclid 有理 Omega、任意线性 Diophantine 约束系统、任意多面锥分解或任意组合对象自动编码。推广到新的 Train 恒等式时，仍需证明新对象的编码、相应约束消元规则，以及消元结果与原题另一侧之间的联系；仅写出 Omega 表示还不构成完整证明。
