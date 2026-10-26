# q-Chu–Vandermonde 与 Gaussian 卷积

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 已有自动证明流程（旧条件域） 3 条；本次未匹配到旧算法 2 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

## FQI-GAUSSIAN-VANDERMONDE · Gaussian q-Vandermonde 卷积

$$
\sum_{k=\max(0,h-m)}^{\min(h,n)} \begin{bmatrix}n\\k\end{bmatrix}_{q}\begin{bmatrix}m\\h-k\end{bmatrix}_{q}q^{(n-k)(h-k)}=\begin{bmatrix}m+n\\h\end{bmatrix}_{q}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AP-3.3.10`。

**证明算法状态：已有自动证明流程（旧条件域）**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-GAUSSIAN-VANDERMONDE)

方法：固定上界 q-WZ 与对角初值。

覆盖边界：旧 main_identity 额外要求 r≤m 且 r≤n；当前目录允许更大的 h，只覆盖其中一部分参数域。

定义文件：[ANDREWS_P_supplement.md](../../round1_source_collection/records/ANDREWS_P_supplement.md)；[ANDREWS_P.md](../../round1_source_collection/books/ANDREWS_P.md)。

- **AP-3.3.10**（p.37, Theorem 3.4, (3.3.10)）：m,n≥0，0≤h≤m+n，均为整数。
  对应：代表式；保留本条来源域。
- **KAC-CHEUNG-7.6**（印刷页 23；7.6）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。m,n≥0，0≤k≤m+n；Gaussian越界为0。
  对应：原 (m,n,k,j)→(n,m,h,k)，零支撑将 j=0..h 缩至有效区间。
- **AP-13.E6**（p.225, Example 6）：m,n≥0，0≤h≤m+n，均为整数。
  对应：在代表式中换 (n,m,k)→(m,n,h−k)；指数成为 k(m−h+k)，因子交换。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-CHU-VANDERMONDE-Q · q-Chu–Vandermonde：自变量 q

$$
{}_2\phi_1^{[n]}\!\left[\begin{matrix}a,q^{-n}\\c\end{matrix};q,q\right]=a^n\frac{(c/a;q)_n}{(c;q)_n}
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-II-06`。

**证明算法状态：已有自动证明流程（旧条件域）**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-CHU-VANDERMONDE-Q)

方法：终止超几何一阶 q-WZ。

覆盖边界：旧定理使用 Generic 和对所有递推层成立的非零条件；比目录仅要求当前有限式分母非零更强。尚未证明目录全部条件能推出这些假设。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-II-06**（Appendix II, (II.6), 印刷p354）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。n 为非负整数；q 为非零且非单位根的复数；所有显示的分母非零。 a≠0。
  对应：代表式；保留本条来源域。
- **AQ-2.41**（印刷页 16；式 (2.41)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 n≥0，q,a≠0。
  对应：展开有限 2φ1，求和指标 j 不变。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-CHU-VANDERMONDE-BALANCED · q-Chu–Vandermonde：自变量 cq^n/a

$$
{}_2\phi_1^{[n]}\!\left[\begin{matrix}a,q^{-n}\\c\end{matrix};q,cq^n/a\right]=\frac{(c/a;q)_n}{(c;q)_n}
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-II-07`。

**证明算法状态：已有自动证明流程（旧条件域）**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-CHU-VANDERMONDE-BALANCED)

方法：终止超几何一阶 q-WZ。

覆盖边界：旧定理使用 Generic 和对所有递推层成立的非零条件；比目录仅要求当前有限式分母非零更强。尚未证明目录全部条件能推出这些假设。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-II-07**（Appendix II, (II.7), 印刷p354）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。n 为非负整数；q 为非零且非单位根的复数；所有显示的分母非零。 a≠0。
  对应：代表式；保留本条来源域。
- **SILLS-1.Thm1.46**（印刷页 31；1.Thm1.46）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0，a≠0。
  对应：补上显式截断上限 n；参数及乘积完全一致。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-1.Ex3i · 乘积参数的两种有限 q 卷积

$$
(ab;q)_n=\sum_{k=0}^n\begin{bmatrix}n\\k\end{bmatrix}_qb^k(a;q)_k(b;q)_{n-k}=\sum_{k=0}^n\begin{bmatrix}n\\k\end{bmatrix}_qa^{n-k}(a;q)_k(b;q)_{n-k}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-1.Ex3i`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-1.Ex3i**（Chapter 1, 1.Ex3i, 印刷p25）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AP-13.E7 · Bender广义q-Vandermonde卷积（修订）

$$
\begin{bmatrix}N\\n\end{bmatrix}_q=\sum_{k=0}^n q^{(n-k)(a_{k+1}-k)}\begin{bmatrix}a_k\\k\end{bmatrix}_q\begin{bmatrix}N-a_{k+1}\\n-k\end{bmatrix}_q.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AP-13.E7`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：一般整数上指标 {v\brack k}_q=\prod_{i=0}^{k-1}(1-q^{v-i})/(q;q)_k；{v\brack0}_q=1，k<0时为0。

定义文件：[ANDREWS_P_supplement.md](../../round1_source_collection/records/ANDREWS_P_supplement.md)；[ANDREWS_P.md](../../round1_source_collection/books/ANDREWS_P.md)。

- **AP-13.E7**（pp.225–226, Chapter13 Example7）：n≥0，N与a_i为整数，a_{i+1}−a_i∈{0,1} (1≤i<n)。a₀、a_{n+1}任意；q≠0，(q;q)_n≠0；n=0两边为1。允许负上指标，不能沿用仅非负Gaussian越界为零的规则。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
