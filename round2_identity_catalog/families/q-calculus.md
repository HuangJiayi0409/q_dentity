# Jackson q 差分、有限 Taylor 与伸缩

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 本次未匹配到旧算法 17 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

## FQI-DQ-MONOMIAL · 单项式的 Jackson q 导数

$$
D_qx^n=[n]_qx^{n-1}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`KAC-CHEUNG-1.10`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[KAC_CHEUNG_supplement.md](../../round1_source_collection/records/KAC_CHEUNG_supplement.md)；[KAC_CHEUNG.md](../../round1_source_collection/books/KAC_CHEUNG.md)。

- **KAC-CHEUNG-1.10**（印刷页 2；1.10）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。n≥0；n=0时右侧解释为0。
  对应：代表式；保留本条来源域。
- **SILLS-1.Dq**（印刷页 28；1.Dq）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥1；n=0时导数为0。
  对应：定义 [n]_q 相同；n=0 另按0解释，不求值 x^−1。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-1.Ex12iv · 高阶 q-Leibniz 公式

$$
D_q^n(fg)(z)=\sum_{k=0}^n\begin{bmatrix}n\\k\end{bmatrix}_q(D_q^{n-k}f)(zq^k)(D_q^kg)(z).
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-1.Ex12iv`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-1.Ex12iv**（Chapter 1, 1.Ex12iv, 印刷p27）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。f,g为多项式或有理函数；D_qf(z)=(f(z)−f(qz))/((1−q)z)。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-1.Ex31-monomial · q 差分算子的单项式作用

$$
\Delta_bx^n=(bq^n-1)x^n,\qquad\Delta_bf(x)=bf(qx)-f(x).
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-1.Ex31-monomial`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-1.Ex31-monomial**（Chapter 1, 1.Ex31-monomial, 印刷p32）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-1.Ex31-term · 有限超几何项的算子关系

$$
(\Delta_1\Delta_{b_1/q}\cdots\Delta_{b_s/q})v_n(z)=z(\Delta_{a_1}\cdots\Delta_{a_r})v_{n-1}(zq^{1+s-r}).
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-1.Ex31-term`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-1.Ex31-term**（Chapter 1, 1.Ex31-term, 印刷p32）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。n≥1；v_n的有限乘积定义同(1.2.26)。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-KAC-CHEUNG-1.11-12 · q 导数乘法规则

$$
D_q(fg)(x)=f(qx)D_qg(x)+g(x)D_qf(x)=f(x)D_qg(x)+g(qx)D_qf(x).
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`KAC-CHEUNG-1.11-12`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[KAC_CHEUNG_supplement.md](../../round1_source_collection/records/KAC_CHEUNG_supplement.md)；[KAC_CHEUNG.md](../../round1_source_collection/books/KAC_CHEUNG.md)。

- **KAC-CHEUNG-1.11-12**（印刷页 3；1.11-12）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。f,g为多项式或有理函数，所需点处有定义；x≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-KAC-CHEUNG-1.13-14 · q 导数商法则

$$
D_q(f/g)(x)=\frac{g(x)D_qf(x)-f(x)D_qg(x)}{g(x)g(qx)}=\frac{g(qx)D_qf(x)-f(qx)D_qg(x)}{g(x)g(qx)}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`KAC-CHEUNG-1.13-14`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[KAC_CHEUNG_supplement.md](../../round1_source_collection/records/KAC_CHEUNG_supplement.md)；[KAC_CHEUNG.md](../../round1_source_collection/books/KAC_CHEUNG.md)。

- **KAC-CHEUNG-1.13-14**（印刷页 3；1.13-14）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。f,g为多项式或有理函数；xg(x)g(qx)≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-KAC-CHEUNG-1.15 · 幂代换的 q 链式规则

$$
D_q(f\circ u)(x)=(D_{q^\beta}f)(u(x))D_qu(x),\qquad u(x)=\alpha x^\beta.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`KAC-CHEUNG-1.15`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[KAC_CHEUNG_supplement.md](../../round1_source_collection/records/KAC_CHEUNG_supplement.md)；[KAC_CHEUNG.md](../../round1_source_collection/books/KAC_CHEUNG.md)。

- **KAC-CHEUNG-1.15**（印刷页 4；1.15）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。β为非零整数，αx≠0，q^β≠1；f为有理函数。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-KAC-CHEUNG-3.5 · 有限 q 幂的降阶导数

$$
D_qP_n(x,a;q)=[n]_qP_{n-1}(x,a;q).
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`KAC-CHEUNG-3.5`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[KAC_CHEUNG_supplement.md](../../round1_source_collection/records/KAC_CHEUNG_supplement.md)；[KAC_CHEUNG.md](../../round1_source_collection/books/KAC_CHEUNG.md)。

- **KAC-CHEUNG-3.5**（印刷页 8；3.5）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。n∈Z；n=0右侧为0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-KAC-CHEUNG-3.10 · 有限 q 幂倒数的导数

$$
D_q\frac1{P_n(x,a;q)}=[-n]_qP_{-n-1}(x,q^na;q).
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`KAC-CHEUNG-3.10`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[KAC_CHEUNG_supplement.md](../../round1_source_collection/records/KAC_CHEUNG_supplement.md)；[KAC_CHEUNG.md](../../round1_source_collection/books/KAC_CHEUNG.md)。

- **KAC-CHEUNG-3.10**（印刷页 11；3.10）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。n∈Z。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-KAC-CHEUNG-3.11 · 第二变量的有限 q 幂导数

$$
D_{q,x}P_n(a,x;q)=-[n]_qP_{n-1}(a,qx;q).
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`KAC-CHEUNG-3.11`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[KAC_CHEUNG_supplement.md](../../round1_source_collection/records/KAC_CHEUNG_supplement.md)；[KAC_CHEUNG.md](../../round1_source_collection/books/KAC_CHEUNG.md)。

- **KAC-CHEUNG-3.11**（印刷页 11；3.11）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。n∈Z。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-KAC-CHEUNG-3.12 · 第二变量的有限 q 幂倒数导数

$$
D_{q,x}\frac1{P_n(a,x;q)}=\frac{[n]_q}{P_{n+1}(a,x;q)}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`KAC-CHEUNG-3.12`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[KAC_CHEUNG_supplement.md](../../round1_source_collection/records/KAC_CHEUNG_supplement.md)；[KAC_CHEUNG.md](../../round1_source_collection/books/KAC_CHEUNG.md)。

- **KAC-CHEUNG-3.12**（印刷页 11；3.12）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。n∈Z。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-KAC-CHEUNG-4.1 · 多项式的有限 q-Taylor 展开

$$
f(x)=\sum_{j=0}^N\frac{(D_q^jf)(c)}{[j]_q!}P_j(x,c;q).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`KAC-CHEUNG-4.1`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[KAC_CHEUNG_supplement.md](../../round1_source_collection/records/KAC_CHEUNG_supplement.md)；[KAC_CHEUNG.md](../../round1_source_collection/books/KAC_CHEUNG.md)。

- **KAC-CHEUNG-4.1**（印刷页 12；4.1）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。deg f≤N，N≥0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-KAC-CHEUNG-4.3 · 单项式的高阶 q 导数

$$
D_q^jx^n=\begin{cases}\dfrac{[n]_q!}{[n-j]_q!}x^{n-j},&0\le j\le n,\\0,&j>n.\end{cases}
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`KAC-CHEUNG-4.3`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[KAC_CHEUNG_supplement.md](../../round1_source_collection/records/KAC_CHEUNG_supplement.md)；[KAC_CHEUNG.md](../../round1_source_collection/books/KAC_CHEUNG.md)。

- **KAC-CHEUNG-4.3**（印刷页 12；4.3）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。n,j≥0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-KAC-CHEUNG-5.1 · 有限 q 幂的高阶导数

$$
D_q^jP_n(x,-a;q)=\frac{[n]_q!}{[n-j]_q!}P_{n-j}(x,-a;q).
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`KAC-CHEUNG-5.1`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[KAC_CHEUNG_supplement.md](../../round1_source_collection/records/KAC_CHEUNG_supplement.md)；[KAC_CHEUNG.md](../../round1_source_collection/books/KAC_CHEUNG.md)。

- **KAC-CHEUNG-5.1**（印刷页 14；5.1）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。0≤j≤n。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-KAC-CHEUNG-8.reciprocal · 有限倒数乘积的高阶 q 导数

$$
D_q^j\frac1{P_n(1,x;q)}=\frac{\prod_{r=0}^{j-1}[n+r]_q}{P_{n+j}(1,x;q)}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`KAC-CHEUNG-8.reciprocal`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[KAC_CHEUNG_supplement.md](../../round1_source_collection/records/KAC_CHEUNG_supplement.md)；[KAC_CHEUNG.md](../../round1_source_collection/books/KAC_CHEUNG.md)。

- **KAC-CHEUNG-8.reciprocal**（印刷页 28；8.reciprocal）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。n≥1，j≥0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-KAC-CHEUNG-14.higher · 第二变量有限 q 幂的高阶导数

$$
D_q^jP_n(1,-x;q)=q^{j(j-1)/2}\frac{[n]_q!}{[n-j]_q!}P_{n-j}(1,-q^jx;q).
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`KAC-CHEUNG-14.higher`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[KAC_CHEUNG_supplement.md](../../round1_source_collection/records/KAC_CHEUNG_supplement.md)；[KAC_CHEUNG.md](../../round1_source_collection/books/KAC_CHEUNG.md)。

- **KAC-CHEUNG-14.higher**（印刷页 48；14.higher）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。0≤j≤n。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-KAC-CHEUNG-19.telescoping · Jackson 证明中的有限伸缩和

$$
(1-q)x\sum_{j=0}^Nq^j(D_qF)(q^jx)=F(x)-F(q^{N+1}x).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`KAC-CHEUNG-19.telescoping`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[KAC_CHEUNG_supplement.md](../../round1_source_collection/records/KAC_CHEUNG_supplement.md)；[KAC_CHEUNG.md](../../round1_source_collection/books/KAC_CHEUNG.md)。

- **KAC-CHEUNG-19.telescoping**（印刷页 69；19.telescoping）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。N≥0，x≠0；F为多项式或有理函数，在所需点有定义。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
