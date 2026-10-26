# Schur、q-Fibonacci 与有限 Rogers–Ramanujan

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 已有自动证明流程（旧条件域） 1 条；已有 Lean 证明实现（旧条件域） 3 条；已有可复用部件，待组装 3 条；本次未匹配到旧算法 11 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

## FQI-SCHUR-RR-BUNDLE · Schur 两支有限 Rogers–Ramanujan

$$
\sum_{j=0}^{\lfloor(n+1-a)/2\rfloor}q^{j^2+aj}\begin{bmatrix}n+1-a-j\\j\end{bmatrix}_{q}=\sum_{h=-n-2}^{n+2}(-1)^hq^{h(5h+1)/2-2ah}\begin{bmatrix}n+1\\\lfloor(n+1-5h)/2\rfloor+a\end{bmatrix}_{q}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AP-3.E10`。

**证明算法状态：已有可复用部件，待组装**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SCHUR-RR-BUNDLE)

方法：两支已证 Schur 定理的合并。

覆盖边界：目录把 a∈{0,1} 合成一条，旧项目未提供该统一签名；另有范数限制。

定义文件：[ANDREWS_P_supplement.md](../../round1_source_collection/records/ANDREWS_P_supplement.md)；[ANDREWS_P.md](../../round1_source_collection/books/ANDREWS_P.md)。

- **AP-3.E10**（p.50, Example 10）：n≥0 为整数；a∈{0,1}；Gaussian 下指标越界为零。
  对应：代表式；保留本条来源域。
- **AP-9.E4a**（p.157, Example 4，第一式）：n≥0 为整数；a∈{0,1}；Gaussian 下指标越界为零。
  对应：公式、定义与条件逐字相同；仅书内定位不同。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SCHUR-RR-FIRST · Schur 第一有限 Rogers–Ramanujan

$$
\sum_{j=0}^{\lfloor n/2\rfloor}q^{j^2}\begin{bmatrix}n-j\\j\end{bmatrix}_q=\sum_{j=-n-1}^{n+1}(-1)^jq^{j(5j+1)/2}\begin{bmatrix}n\\\lfloor(n+5j+1)/2\rfloor\end{bmatrix}_q.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`SILLS-4.14`。

**证明算法状态：已有自动证明流程（旧条件域）**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SCHUR-RR-FIRST)

方法：共同 q-Fibonacci 二阶递推与两个初值。

覆盖边界：旧证明在 Complete NormedField、0<‖q‖<1（以 q≠0 与 ‖q‖<1 表述）下；目录为形式多项式／一般安全域。

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-4.14**（印刷页 123；4.14）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0。
  对应：代表式；保留本条来源域。
- **AQ-8.36**（印刷页 79；式 (8.36)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 N≥1；F 的递推与初值见 (8.32)–(8.35)。
  对应：F_N(0)=D_N=Σ_j q^(j²)[N−j choose j]_q；n=N，Gaussian 对称将 floor((n−5j)/2) 换成 floor((n+5j+1)/2)。两边多余尾项均为0。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SCHUR-RR-SECOND · Schur 第二有限 Rogers–Ramanujan

$$
E_n=\sum_{j=0}^{\lfloor n/2\rfloor}q^{j(j+1)}\begin{bmatrix}n-j\\j\end{bmatrix}_q=\sum_{j=-n-2}^{n+2}(-1)^jq^{j(5j+3)/2}\begin{bmatrix}n+1\\\lfloor(n+5j+3)/2\rfloor\end{bmatrix}_q.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`SILLS-4.16`。

**证明算法状态：已有 Lean 证明实现（旧条件域）**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SCHUR-RR-SECOND)

方法：第二支共同二阶递推（已作为旧库定理）。

覆盖边界：旧定理有范数域条件；第二支有限定理存在于库中，独立 #q_finite_rr_prove 仅接受第一支标准输入。

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-4.16**（印刷页 123；4.16）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0。
  对应：代表式；保留本条来源域。
- **AQ-8.37**（印刷页 79；式 (8.37)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 N≥1；F 的递推与初值见 (8.32)–(8.35)。
  对应：F_N(1)=E_(N−1)；n=N−1，λ=−j；floor((N+5j)/2)+1=floor((n+5j+3)/2)。零支撑调整求和界。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SCHUR-EVEN-RECIPROCAL · Schur D 偶指标倒数的两种展开

$$
q^{m^2}D_{2m}(q^{-1})=\sum_{j=0}^mq^{j^2}\begin{bmatrix}m+j\\2j\end{bmatrix}_q=\sum_{k=-m-2}^{m+2}\left(q^{15k^2-k}\begin{bmatrix}2m\\m+5k\end{bmatrix}_q-q^{15k^2-11k+2}\begin{bmatrix}2m\\m+5k-2\end{bmatrix}_q\right).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`SILLS-4.23`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-4.23**（印刷页 125；4.23）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。m≥0。
  对应：代表式；保留本条来源域。
- **AQ-REF-8.42**（印刷页 80；式 (8.42)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 N≥0；F₀(0)=1 为与原递推相容的延拓。
  对应：N→m；F_(2N)(0)=D_(2N)；双边和 k→−k，再用 Gaussian 对称，得到两项指数 15k²−k、15k²−11k+2。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-2.7.5 · Rogers–Ramanujan 证明中的有限变换

$$
\sum_{k=0}^n\frac{(a;q)_k(1-aq^{2k})(q^{-n};q)_k}{(q;q)_k(1-a)(aq^{n+1};q)_k}q^{2k^2}(a^2q^n)^k=(aq;q)_n\sum_{k=0}^n\frac{(q^{-n};q)_k}{(q;q)_k}(-aq^{n+1})^kq^{k(k-1)/2}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-2.7.5`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-2.7.5**（Chapter 2, 2.7.5, 印刷p44）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。a≠1。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AP-3.E12a · Schur 多项式倍指标恒等式

$$
D_{2n}(q)=\sum_{j=0}^n q^{jn}\begin{bmatrix}n+1\\j\end{bmatrix}_{q}D_{n-1-j}(q).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AP-3.E12a`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：\(D_n(q)=\sum_{j=0}^{\lfloor(n+1)/2\rfloor}q^{j^2}\begin{bmatrix}n+1-j\\j\end{bmatrix}_q\)（n≥0）；为解释原习题端点，补充 D_{-1}=1。

定义文件：[ANDREWS_P_supplement.md](../../round1_source_collection/records/ANDREWS_P_supplement.md)；[ANDREWS_P.md](../../round1_source_collection/books/ANDREWS_P.md)。

- **AP-3.E12a**（p.50, Example 12，第一式）：n≥0 为整数；D_{−1}=1。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AP-3.E12b · Schur 多项式累加恒等式

$$
D_n(q)=1+\sum_{j=1}^n q^jD_{j-2}(q).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AP-3.E12b`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：\(D_n(q)=\sum_{j=0}^{\lfloor(n+1)/2\rfloor}q^{j^2}\begin{bmatrix}n+1-j\\j\end{bmatrix}_q\)（n≥0）；为解释原习题端点，补充 D_{-1}=1。

定义文件：[ANDREWS_P_supplement.md](../../round1_source_collection/records/ANDREWS_P_supplement.md)；[ANDREWS_P.md](../../round1_source_collection/books/ANDREWS_P.md)。

- **AP-3.E12b**（p.50, Example 12，第二式）：n≥0 为整数；D_{−1}=1。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AP-9.E4b · 有限 Euler 五边形型恒等式

$$
\sum_{h=-n-2}^{n+2}(-1)^h q^{h(3h+1)/2}\begin{bmatrix}n+1\\\lfloor(n+1-3h)/2\rfloor\end{bmatrix}_{q}=1.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AP-9.E4b`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_P_supplement.md](../../round1_source_collection/records/ANDREWS_P_supplement.md)；[ANDREWS_P.md](../../round1_source_collection/books/ANDREWS_P.md)。

- **AP-9.E4b**（p.157, Example 4，第二式）：n≥0 为整数；Gaussian 下指标越界为零。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AQ-8.32 · 硬六角 F 多项式递推

$$
F_N(\sigma;q)=F_{N-1}(\sigma;q)+q^{N-1}F_{N-2}(\sigma;q),\quad F_1(\sigma)=1,\quad F_2(0)=1+q,\ F_2(1)=1.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`AQ-8.32`。

**证明算法状态：已有可复用部件，待组装**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SRC-AQ-8.32)

方法：两支 Schur 的递推组合。

覆盖边界：目录 F_N(σ) 的统一 σ 定义及初值没有同签名自动证明。

定义文件：[ANDREWS_Q_supplement.md](../../round1_source_collection/records/ANDREWS_Q_supplement.md)；[ANDREWS_Q.md](../../round1_source_collection/books/ANDREWS_Q.md)。

- **AQ-8.32**（印刷页 79；式 (8.32)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 N≥3，σ∈{0,1}；F 是 (8.31) 非相邻占据序列的权重和。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AQ-9.5 · D 多项式的正项 Gaussian 展开

$$
D_N(q)=F_N(0;q)=\sum_{n=0}^{\lfloor N/2\rfloor}q^{n^2}\begin{bmatrix}N-n\\n\end{bmatrix}_q.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AQ-9.5`。

**证明算法状态：已有可复用部件，待组装**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SRC-AQ-9.5)

方法：Schur 多项式定义及递推唯一性。

覆盖边界：仅存在相同和的定义不等于已证明目录 D=F=单和。

定义文件：[ANDREWS_Q_supplement.md](../../round1_source_collection/records/ANDREWS_Q_supplement.md)；[ANDREWS_Q.md](../../round1_source_collection/books/ANDREWS_Q.md)。

- **AQ-9.5**（印刷页 89；式 (9.5)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 N≥0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AQ-9.26 · D 奇指标倒数恒等式

$$
q^{N(N+1)}D_{2N+1}(q^{-1})=\sum_{n=0}^Nq^{n(n+1)}\begin{bmatrix}N+n+1\\2n+1\end{bmatrix}_q.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AQ-9.26`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_Q_supplement.md](../../round1_source_collection/records/ANDREWS_Q_supplement.md)；[ANDREWS_Q.md](../../round1_source_collection/books/ANDREWS_Q.md)。

- **AQ-9.26**（印刷页 92；式 (9.26)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 N≥0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AQ-9.27 · D 偶指标倒数恒等式

$$
q^{N^2}D_{2N}(q^{-1})=\sum_{n=0}^Nq^{n^2}\begin{bmatrix}N+n\\2n\end{bmatrix}_q.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AQ-9.27`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_Q_supplement.md](../../round1_source_collection/records/ANDREWS_Q_supplement.md)；[ANDREWS_Q.md](../../round1_source_collection/books/ANDREWS_Q.md)。

- **AQ-9.27**（印刷页 92；式 (9.27)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 N≥0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-4.6 · 第一 q-Fibonacci 多项式递推

$$
D_n=D_{n-1}+q^{n-1}D_{n-2},\quad D_0=D_1=1.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`SILLS-4.6`。

**证明算法状态：已有 Lean 证明实现（旧条件域）**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SRC-SILLS-4.6)

方法：Schur 证明内部的 q-Fibonacci 递推。

覆盖边界：旧库有范数域条件；目录用 D/E 局部名字及独立初值，仍需定义桥接。

局部定义：D_n=\sum_{j=0}^{\lfloor n/2\rfloor}q^{j^2}{n-j\brack j}_q.

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-4.6**（印刷页 118；4.6）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥2。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-4.17 · 第二 q-Fibonacci 多项式递推

$$
E_n=E_{n-1}+q^nE_{n-2},\quad E_0=E_1=1.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`SILLS-4.17`。

**证明算法状态：已有 Lean 证明实现（旧条件域）**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SRC-SILLS-4.17)

方法：Schur 证明内部的 q-Fibonacci 递推。

覆盖边界：旧库有范数域条件；目录用 D/E 局部名字及独立初值，仍需定义桥接。

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-4.17**（印刷页 123；4.17）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥2；E_n见(4.16)。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-4.25 · 奇数 D 多项式的倒数对偶

$$
q^{m(m+1)}D_{2m+1}(q^{-1})=\sum_{j=0}^mq^{j(j+1)}\begin{bmatrix}m+j+1\\2j+1\end{bmatrix}_q=\sum_{k=-m-2}^{m+2}\left(q^{15k^2+4k}\begin{bmatrix}2m+1\\m+5k+1\end{bmatrix}_q-q^{15k^2+14k+3}\begin{bmatrix}2m+1\\m+5k+3\end{bmatrix}_q\right).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`SILLS-4.25`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-4.25**（印刷页 126；4.25）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。m≥0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-4.26-corrected · 偶数 E 多项式的倒数对偶

$$
q^{m(m+1)}E_{2m}(q^{-1})=\sum_{j=0}^mq^{j(j+1)}\begin{bmatrix}m+j\\2j\end{bmatrix}_q=\sum_{k=-m-2}^{m+2}\left(q^{15k^2+2k}\begin{bmatrix}2m+1\\m+5k+1\end{bmatrix}_q-q^{15k^2+8k+1}\begin{bmatrix}2m+1\\m+5k+2\end{bmatrix}_q\right).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`SILLS-4.26-corrected`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-4.26-corrected**（印刷页 126；4.26-corrected）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。m≥0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-4.27-corrected · 奇数 E 多项式的倒数对偶

$$
q^{m(m+2)}E_{2m+1}(q^{-1})=\sum_{j=0}^mq^{j(j+2)}\begin{bmatrix}m+j+1\\2j+1\end{bmatrix}_q=\sum_{k=-m-2}^{m+2}\left(q^{15k^2+7k}\begin{bmatrix}2m+2\\m+5k+2\end{bmatrix}_q-q^{15k^2+13k+2}\begin{bmatrix}2m+2\\m+5k+3\end{bmatrix}_q\right).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`SILLS-4.27-corrected`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-4.27-corrected**（印刷页 126；4.27-corrected）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。m≥0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-5.6-8 · Motivated proof 中的有限系数多项式递推

$$
A_{i+1}=A_i+B_i,\quad B_{i+1}=q^iA_i,\quad A_3=1,\ B_3=0;\qquad A_{i+1}=A_i+q^{i-1}A_{i-1}\ (i\ge4).
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`SILLS-5.6-8`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：等价地A_i为从{3,…,i−2}选取互不相邻整数的q权之和，B_i=q^{i−1}A_{i−1}（i≥4）；这个有限集合解释用于独立核验。

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-5.6-8**（印刷页 142；5.6-8）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。耦合递推i≥3；A₄=1。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
