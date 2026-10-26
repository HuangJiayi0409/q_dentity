# q-多项式与多重集合统计

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 本次未匹配到旧算法 9 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

**全家族框架已搭建（2026-09-24，9/9 条、12 个目标）**：[范式与条件域](../../finite_product_framework/docs/q_multinomial.md)。AP-3.5.MULTIPROD 与 AQ-B.12 的三个目标生成证明已闭合；GR2-1.Ex3ii 复用三变量卷积并对任意参数列表归纳，框架保留 5 个局部义务。Python 与 `qmultinomial_framework` tactic 共用算法，不调用 Maple。其余六条新增系数递推、根筛选和统计双射框架，八个目标共 33 个局部义务实例；[本轮报告](../../finite_product_framework/reports/q_multinomial/extension_20260924/check.json)。下方旧审计状态保留，不等同于当前框架搭建状态。

## FQI-SRC-GR2-1.Ex3ii · 有限 q 多项式定理

$$
(a_1\cdots a_{m+1};q)_n=\sum_{\substack{k_1,\ldots,k_m\ge0\\K=k_1+\cdots+k_m\le n}}\frac{(q;q)_n\prod_{j=1}^m(a_j;q)_{k_j}(a_{m+1};q)_{n-K}}{\prod_{j=1}^m(q;q)_{k_j}(q;q)_{n-K}}\prod_{j=2}^{m+1}a_j^{k_1+\cdots+k_{j-1}}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-1.Ex3ii`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-1.Ex3ii**（Chapter 1, 1.Ex3ii, 印刷p25）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。m≥1。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AP-3.4.2 · 逆序数的 q-多项系数生成式

$$
\sum_{s=0}^{S}\operatorname{inv}(m_1,\ldots,m_r;s)q^s=\frac{(q;q)_{m_1+\cdots+m_r}}{\prod_{i=1}^r(q;q)_{m_i}}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AP-3.4.2`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：inv/ind 分别数多重集合 {1^{m₁},…,r^{mᵣ}} 中逆序数/下降位置之和为 s 的不同排列。

定义文件：[ANDREWS_P_supplement.md](../../round1_source_collection/records/ANDREWS_P_supplement.md)；[ANDREWS_P.md](../../round1_source_collection/books/ANDREWS_P.md)。

- **AP-3.4.2**（p.41, Theorem 3.6, (3.4.2)）：r≥1；所有 m_i≥0 为整数；S=Σ_{i<j}m_i m_j。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AP-3.4.4 · major index（原书 greater index）的 q-多项系数生成式

$$
\sum_{s=0}^{S}\operatorname{ind}(m_1,\ldots,m_r;s)q^s=\frac{(q;q)_{m_1+\cdots+m_r}}{\prod_{i=1}^r(q;q)_{m_i}}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AP-3.4.4`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：inv/ind 分别数多重集合 {1^{m₁},…,r^{mᵣ}} 中逆序数/下降位置之和为 s 的不同排列。

定义文件：[ANDREWS_P_supplement.md](../../round1_source_collection/records/ANDREWS_P_supplement.md)；[ANDREWS_P.md](../../round1_source_collection/books/ANDREWS_P.md)。

- **AP-3.4.4**（p.42, Theorem 3.7, (3.4.4)）：r≥1；所有 m_i≥0 为整数；S=Σ_{i<j}m_i m_j。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AP-3.5.MULTIPROD · q-多项系数的 Gaussian 乘积分解

$$
\frac{(q;q)_{m_1+\cdots+m_r}}{\prod_{i=1}^r(q;q)_{m_i}}=\prod_{j=2}^r\begin{bmatrix}m_1+\cdots+m_j\\m_1+\cdots+m_{j-1}\end{bmatrix}_{q}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`AP-3.5.MULTIPROD`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_P_supplement.md](../../round1_source_collection/records/ANDREWS_P_supplement.md)；[ANDREWS_P.md](../../round1_source_collection/books/ANDREWS_P.md)。

- **AP-3.5.MULTIPROD**（p.48, Theorem 3.11 证明末尾）：r≥1，m_i≥0 均为整数。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AQ-B.9 · Rogers 对称齐次多项式的 q-差分

$$
\delta_\lambda H_n=\delta_\mu H_n=\delta_\nu H_n=H_{n-1},\quad \delta_x f=\frac{f(x)-f(qx)}x.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`AQ-B.9`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_Q_supplement.md](../../round1_source_collection/records/ANDREWS_Q_supplement.md)；[ANDREWS_Q.md](../../round1_source_collection/books/ANDREWS_Q.md)。

- **AQ-B.9**（印刷页 112,113；式 (B.9)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 n≥1；\(H_n=\sum_{r+s+t=n}\lambda^r\mu^s\nu^t/((q;q)_r(q;q)_s(q;q)_t)\)；x=0 以多项式延拓解释。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AQ-B.12 · Rogers 齐次展开系数递推

$$
(1-q^{r+1})a_{r+1,s,t}=(1-q^{s+1})a_{r,s+1,t}=(1-q^{t+1})a_{r,s,t+1},\quad a_{r,s,t}=\frac1{(q;q)_r(q;q)_s(q;q)_t}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`AQ-B.12`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_Q_supplement.md](../../round1_source_collection/records/ANDREWS_Q_supplement.md)；[ANDREWS_Q.md](../../round1_source_collection/books/ANDREWS_Q.md)。

- **AQ-B.12**（印刷页 112,113；式 (B.12)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 r,s,t≥0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-FINE-21.2 · basic multinomial 的根单位筛选

$$
Q_n(1,\zeta,\ldots,\zeta^{k-1})=\begin{cases}0,&n\not\equiv0\pmod k,\\\dfrac{(q;q)_n}{(q^k;q^k)_{n/k}},&n\equiv0\pmod k,\end{cases}\quad \zeta=e^{2\pi i/k}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`FINE-21.2`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：Q_n(u_1,…,u_k)=\sum_{r_1+…+r_k=n,\,r_i≥0}(q;q)_n\prod_{i=1}^k u_i^{r_i}/(q;q)_{r_i}。

定义文件：[FINE_supplement.md](../../round1_source_collection/records/FINE_supplement.md)；[FINE.md](../../round1_source_collection/books/FINE.md)。

- **FINE-21.2**（印刷页 30；式 (21.2)；The basic multinomial）：q 为形式变量；数值代入要求所有实际分母非零，Gaussian 在奇点先作多项式延拓。空乘积为 1、空和为 0。k≥1；s=0,1,…,k−1；n≥0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-FINE-21.21 · basic multinomial 的分数幂特化

$$
Q_n(1,q^{1/p},q^{2/p},\ldots,q^{(p-1)/p})=\frac{(q;q)_n}{(q^{1/p};q^{1/p})_n}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`FINE-21.21`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：Q_n(u_1,…,u_k)=\sum_{r_1+…+r_k=n,\,r_i≥0}(q;q)_n\prod_{i=1}^k u_i^{r_i}/(q;q)_{r_i}。

定义文件：[FINE_supplement.md](../../round1_source_collection/records/FINE_supplement.md)；[FINE.md](../../round1_source_collection/books/FINE.md)。

- **FINE-21.21**（印刷页 30；式 (21.21)；The basic multinomial）：q 为形式变量；数值代入要求所有实际分母非零，Gaussian 在奇点先作多项式延拓。空乘积为 1、空和为 0。p≥1，n≥0 为整数；选择 q^{1/p}。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-FINE-21.23 · basic multinomial 的整除筛选

$$
Q_m=0\ (m\not\equiv0\pmod k),\qquad Q_{nk}=\frac{(q;q)_{nk}}{(q^{k/p};q^{k/p})_n}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`FINE-21.23`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：Q_n(u_1,…,u_k)=\sum_{r_1+…+r_k=n,\,r_i≥0}(q;q)_n\prod_{i=1}^k u_i^{r_i}/(q;q)_{r_i}。

定义文件：[FINE_supplement.md](../../round1_source_collection/records/FINE_supplement.md)；[FINE.md](../../round1_source_collection/books/FINE.md)。

- **FINE-21.23**（印刷页 30；式 (21.23)；The basic multinomial）：q 为形式变量；数值代入要求所有实际分母非零，Gaussian 在奇点先作多项式延拓。空乘积为 1、空和为 0。k,p≥1；n,m≥0；选定 s=q^{1/p}，并解释 q^{k/p}=s^k。Q_m 的 kp 个参数为 u_{r,j}=s^{r-1}exp(2πij/k)，1≤r≤p、0≤j<k（原式 21.22）。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
