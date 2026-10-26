# 第二轮统一记号与条件

## 共同记号

有限 q-Pochhammer 统一为

\[
(a;q)_n=\prod_{j=0}^{n-1}(1-aq^j),\quad
(a;q)_{-n}=\frac1{(aq^{-n};q)_n},\quad
(a_1,\ldots,a_r;q)_n=\prod_{i=1}^r(a_i;q)_n\quad(n\ge0).
\]

负长度表示有限有理式，不能设成零。空积为1，空和为0。底数 q、q²、q³、p、Q 分别保留，不能把不同底数的乘积机械替换成同一个底数。

普通 Gaussian 统一显示为

\[
\begin{bmatrix}n\\k\end{bmatrix}_q
=\frac{(q;q)_n}{(q;q)_k(q;q)_{n-k}}\quad(0\le k\le n),
\]

其中 n≥0、k 为整数，k<0 或 k>n 时为0；多项式解释下 q=1 等点由约去后的多项式求值。

**广义上指标必须区别处理：** GR 附录 I.43–47 与 AP-13.E7 使用

\[
\begin{bmatrix}\alpha\\k\end{bmatrix}_q
=\frac{\prod_{j=0}^{k-1}(1-tq^{-j})}{(q;q)_k},\quad t=q^\alpha,\ k\ge0.
\]

k<0 取0；α 为负整数时仍按乘积定义，不因上指标为负就置零。非整数 α 可将 t 看作独立变量，数值幂须固定相容分支。AP-13.E7 的每个整数上指标均按此定义。AQ-9.17 的 n=0 第二个 Gaussian 特例按 δ_(j,0) 解释。

终止基本超几何和统一解释为

\[
{}_r\phi_s^{[N]}(a_1,\ldots,a_r;b_1,\ldots,b_s;q,z)
=\sum_{k=0}^{N}\frac{(a_1,\ldots,a_r;q)_k}{(q,b_1,\ldots,b_s;q)_k}
\bigl((-1)^kq^{k(k-1)/2}\bigr)^{1+s-r}z^k.
\]

只有确定了实际终止长度或有限支持时才使用这个记号。不同侧可有不同上限；不计算终止点之后的0/0。Sills 含 φ 的主公式均已在第二轮补显式 [n]，不能把此操作推广到未收录的无限级数。

\[
W_{m+3}^{[N]}(A;b_1,\ldots,b_m;q,z)
=\sum_{k=0}^{N}\frac{1-Aq^{2k}}{1-A}
\frac{(A,b_1,\ldots,b_m;q)_k}{(q,Aq/b_1,\ldots,Aq/b_m;q)_k}z^k.
\]

本库 W_6、W_8、W_10、W_12 分别表示消去平方根对后的 6φ5、8φ7、10φ9、12φ11。它们与 GR 的 q-Racah 多项式 W_n 是不同记号，依 notation_context 区分。

\[
[n]_q=\frac{1-q^n}{1-q},\quad [n]_q!=\prod_{j=1}^n[j]_q,
\quad D_qf(x)=\frac{f(x)-f(qx)}{(1-q)x},
\]

\[
\langle n\rangle_q=\frac{q^n-q^{-n}}{q-q^{-1}},\quad
\widetilde D_qf(x)=\frac{f(qx)-f(q^{-1}x)}{(q-q^{-1})x}.
\]

Jackson 导数、对称导数、Askey–Wilson 算子分别保留。AQ 的 δ_x=(1−q)D_q 不可直接当作 D_q。

## 跨书对象对照

|对象|统一定义或对应|必须保留的区别|
|---|---|---|
|Rogers–Szegő|H_n(t;q)=Σ_k [n choose k]_q t^k；AP 的 H、Fine 的 f、KC 的 H、GR Ex7.40 的 h 对应此对象|AQ 的 A_n(x)=x^n H_n(x^−2;q) 为 Laurent 归一化，另记变换关系|
|Schur D|D_N(q)=Σ_j q^(j²)[N−j choose j]_q；AQ 的 F_N(0)、D_N 与 Sills 的 D_N 一致|AP 的 D_n=D_(n+1)，不可只改字母|
|Schur E|E_N(q)=Σ_j q^(j(j+1))[N−j choose j]_q，采用 Sills 指标|AQ 的 F_N(1)=E_(N−1)，N≥1|
|Göllnitz|AQ 的 d_N(t)=Sills 的 G_N(t,q)，严格差条件看较大部件，t 权按剩余类分配|AP-7.E11 的分拆约定另存，不按名称自动合并|
|Bailey 对|β_n=Σ_(r=0)^n α_r/((q;q)_(n−r)(aq;q)_(n+r))|Sills 参数 x 对应 a；n=0 单列 α₀=β₀|
|KC 有限 q 幂|P_n(x,a;q)=∏_(j=0)^(n−1)(x−aq^j)=x^n(a/x;q)_n，n≥0|后一表示在 x=0 先作多项式延拓；整数负阶沿用来源的倒数定义|
|局部多项式/序列|每条公式带 notation_context 与定义文件链接|同名 P、Q、D、H、F、G、W 不代表同一函数|

局部对象的参数和归一化保留在来源命名空间中；所有条目链接本书 supplement 和 books 说明，并保留本条 definitions。统一基础符号不等于对任意 LaTeX 作代数规范化。合并组中的 witness 给出来源到代表式的具体代换。

## 条件数据的含义

每条来源保留原 conditions 全文，并拆成带类别标签的 clauses：整数/范围、参数关系、非零/分母、根分支、函数与支持定义、边界约定、其他来源条件。标签仅供检索，约束正文仍为数学文本，**不是 CAS 可直接执行的完整条件 AST**。

合并条目的 domain_variants 是各来源条件在 witness 代换下的**析取**。每个分支使用自己的来源变量和定义；不能只保留代表来源的条件，也不能把不同分支的条件任意拼接成更大的域。相同公式在不同已核实域的记录可合并为“同式的多个条件分支”；严格特例和组合公式的单个等号另记有向关系。

适用于实际出现的对象的公共规则：

1. 有理式只在实际有限项的分母非零处直接求值；形式变量可在相应有理函数域解释。有限式本身不额外要求 |q|<1。
2. 多项式延拓只作用于已确认的多项式表达，不自动使所有有理式在奇点有定义。
3. q 的负幂、负长度乘积、倒底数要求 q≠0；涉及分数幂时使用同一个辅助根。原书安全域（如 GR 非单位根）保留，未擅自宣称最大域。
4. 有限域计数中的 q 是素数幂；不能把这个语义替换为形式变量。
5. 求和范围、零支撑、初值、配平关系、有限支持与特殊端点条件均是公式的一部分。
6. 某条的显式特例优先于来源模板：AQ-8.56 允许定义过的负长度；AP-13.E7 允许负上指标；Bailey 反演 n=0 先约去伪奇点。

## 前轮修订的保护

16项处置全部通过 target_record 关联到第二轮条目，见 correction_links.json。GR2-8.Ex15 只保留 b/c 终止分支，不恢复被否定的 a-only 分支；KC-26.23 保留“推导替代”身份；Sills Ex2.5a 只是修订后 Lem3.3 的别名。修订公式、conditions、transcription_changes、correction_basis、source_issues 与 source_corrections 均在 normalized_sources.json 的 source_record 中原样保留。
