# 一般 q-Zeilberger：联合递推与证书 pipeline

实现日期：2026-10-12。构造器已实现，受限表示的端到端出口已接通。首个新增原始 train 目标为 **FQI-GAUSS-ALTERNATING**；不宣称覆盖全部 120 条候选或任意 q-超几何输入。

## 运行与产物

在 `finite_product_framework/p1` 执行：

```bash
python3 run.py --identity FQI-GAUSS-ALTERNATING
python3 run.py --identity FQI-GAUSS-ALTERNATING --branch general_q_zeilberger --max-order 4 --seconds 30
python3 test_zeilberger.py
python3 check.py
```

自动路由按表达式选择；也可显式指定一般递推分支，比较相同输入在不同构造器中的表现。原 q-WZ 与直接 q-Gosper 路由保持优先。前端无法被旧分支表示时，尝试一般递推分支；旧分支搜索失败暂不自动重试新分支，可用 `--branch` 明确选择。

证明：[Proof.lean](../generated/runs/FQI-GAUSS-ALTERNATING/Proof.lean)；逐次构造、阶数尝试及审计：[report.json](../generated/runs/FQI-GAUSS-ALTERNATING/report.json)；回归：[zeilberger_tests.json](../generated/zeilberger_tests.json)。

## 构造算法

[zeilberger.py](../zeilberger.py) 只接收求和项及来源元数据，**不接收右端目标、预写递推或证书**。从原项 F 推导 U=F(n,k+1)/F(n,k)、V=F(n+1,k)/F(n,k)，逐阶构造 V_j=F(n+j,k)/F(n,k)。

在每个阶数 r，取 V_j 关于 X=q^k 的分母最小公倍式 D，令 H=F/D。对 H 的后向项比使用已有 q-Gosper 正规形：

\[
\frac{H(X)}{H(X/q)}=\frac{P(X)}{P(X/q)}\frac{A(X)}{B(X)}.
\]

联合求未知递推系数 c_j(Q) 和 Laurent 多项式 f：

\[
A(qX)f(X)-B(X)f(X/q)=\sum_{j=0}^r c_j(Q)P(X)D(X)V_j(X).
\]

右端每个基多项式使用已有精确 Laurent 次数界，再取覆盖区间；不是预填证书分母或猜定次数。通过线性系统的零空间寻找 c_r≠0 的解，归一化 c_r=1，恢复

\[
R(X)=\frac{B(X)f(X/q)}{D(X)P(X)}.
\]

最后独立复核 U(X)R(qX)-R(X)=Σ c_j V_j。构造方式遵循参数化 q-Gosper/q-Zeilberger 的局部证书机制；具体公共分母组织和验证接口为本项目实现。[Paule–Riese 原始论文，第4节](https://www.risc.jku.at/publications/download/risc_117/Paule_Riese.pdf)

阶数上限是资源限制，默认 4，可配置；超时由独立进程强制执行。`search_exhausted` 仅表示搜索至指定阶数未找到，不声明不存在递推。超过线性系统未知数限制返回 `resource_exhausted`。系数域是形式有理函数域，搜索域与原 Lean 参数域分开。

## 原题证明如何闭合

[zeilberger_pipeline.py](../zeilberger_pipeline.py) 从 Lean Expr 解析求和项，保留原目标供最后验证。对于 Gauss 交错式，实际搜索结果为：

\[
c_0=qQ-1,\quad c_1=0,\quad c_2=1.
\]

对应 S(n+2)=(1-q^(n+1))S(n)。这是运行产物，不是构造器中的常量。

证书经项比转换为 G(n,0)=0，G(n,k+1)=q^(n+1-k)F(n+1,k)，在有效区间内只使用非负次幂。转换系数从搜索结果计算，通用 Gaussian 相邻关系的组合乘数也由局部代数计算。Lean 直接验证原 Gaussian 多项式上的局部关系，保留任意 Field 中的 q，包括 q=0 和单位根。

[Shared.lean](../lean/Shared.lean) 新增三个通用引理：

- `sum_zero_extend`：有已证零支撑时，将各移位项放到共同有限区间。
- `telescoper_sum`：对一般阶局部关系求和，显式保留真实端点差；未假设所有输入边界为零。
- `higher_order_unique`：任意正阶、最高系数为 1 的非齐次递推唯一性，允许低阶系数为零及稀疏移位。

首例在最大区间 range(n+3) 上验证所有项，包括上边界，再证明端点差为零。从原目标计算并验证 n=0、1；目标递推由余数分类、自然数除法与 Pochhammer 后继规则证明。余数分类是二阶证明生成的通用算术步骤，没有输入奇支答案。最后恢复原声明并审核证明公理，不含 `sorryAx`。

## 已实现范围与剩余义务

|层次|能力与限制|
|---|---|
|符号构造|支持受限表达式 IR 可导出的单基有理项比；阶数可配置。回归包含一阶、二阶和三阶局部证书。|
|一阶 Lean 出口|复用既有证书回译与求和验证；系数由联合搜索产生，不读取目标相邻比。|
|二阶 Lean 出口|单个 Gaussian 因子、与 n 无关的几何权重；证书可转为多项式乘 F(n+1,k) 的后移通量；局部残差可由公共相邻关系组合验证。|
|目标验证|现有算术、Pochhammer 与二余数分段表达式；真实目标必须在 Lean 中满足递推和初值，无法闭合返回失败。|
|尚未接通|三阶以上自动局部回译；非单项/多重和；非 monic 原域处理；任意分段、显式分母域及非零边界的自动生成；双侧独立递推比较。|

“一般”指联合搜索未知递推和证书，并非任意输入都能完成原域证明。构造成功但不满足回译条件时返回 `representation_gap` / `domain_unresolved`；Lean 义务未闭合返回 `lean_failed`，不增加训练覆盖。

## 验收内容

原 Gauss 声明与公理审计；改名、常数倍权重的完整证明；改变偶支初值、改变奇支目标均被 Lean 拒绝；篡改证书或递推被局部验证拒绝；篡改通量下端点被 Lean 拒绝。另检验阶数预算和未知数预算的失败语义，以及一阶分支复用。合成变体和三阶局部证书均不算新增训练证明。

本分支的 CAS 接入点是 Python/SymPy 参数化线性系统，复用本项目 q-Gosper 正规形，没有安装或调用外部 qZeil。算法本身未在 Lean 中形式化；每次结果由 Lean 验证原定理。
