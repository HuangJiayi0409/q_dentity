# 生成函数的有限系数递推与反求

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 本次未匹配到旧算法 6 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

## FQI-SRC-GR2-1.2.26 · 有限超几何项的相邻项递推

$$
(1-q^{n+1})\prod_{j=1}^s(1-b_jq^n)v_{n+1}=z(-q^n)^{1+s-r}\prod_{i=1}^r(1-a_iq^n)v_n.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-1.2.26`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-1.2.26**（Chapter 1, 1.2.26, 印刷p5）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。r,s≥0；v_n的有限乘积定义见辅助说明。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-1.3.25 · 对称 q 指数的有限系数递推

$$
A_{n+1}=\frac{1-q}{1-q^{n+1}}q^{n/2}A_n,\quad A_0=1,\quad A_n=\frac{(1-q)^nq^{n(n-1)/4}}{(q;q)_n}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-1.3.25`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-1.3.25**（Chapter 1, 1.3.25, 印刷p11）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。分数幂相容。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AQ-10.30 · Euler 乘积系数的有限递推

$$
b_0=1,\quad D_j=\sum_{d\mid j}d\,a_d,\quad nb_n=\sum_{j=1}^nD_jb_{n-j}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`AQ-10.30`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_Q_supplement.md](../../round1_source_collection/records/ANDREWS_Q_supplement.md)；[ANDREWS_Q.md](../../round1_source_collection/books/ANDREWS_Q.md)。

- **AQ-10.30**（印刷页 104,105；式 (10.30)）：n≥1；\(b_n=[q^n]\prod_{m=1}^{n}(1-q^m)^{-a_m}\)，a_m 为整数。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AQ-10.32 · Euler 乘积指数的有限反求

$$
na_n=nb_n-\sum_{\substack{d\mid n\\d<n}}d\,a_d-\sum_{j=1}^{n-1}D_jb_{n-j},\qquad D_j=\sum_{d\mid j}d\,a_d.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`AQ-10.32`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_Q_supplement.md](../../round1_source_collection/records/ANDREWS_Q_supplement.md)；[ANDREWS_Q.md](../../round1_source_collection/books/ANDREWS_Q.md)。

- **AQ-10.32**（印刷页 105；式 (10.32)）：n≥1；a、b 与 (10.30) 相同。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AQ-10.7A · Rogers–Ramanujan 系数的递推与乘积

$$
a_0=1,\quad a_n=\frac{q^{2n-1}}{1-q^n}a_{n-1}=\frac{q^{n^2}}{(q;q)_n}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`AQ-10.7A`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_Q_supplement.md](../../round1_source_collection/records/ANDREWS_Q_supplement.md)；[ANDREWS_Q.md](../../round1_source_collection/books/ANDREWS_Q.md)。

- **AQ-10.7A**（印刷页 106；式 (10.7A)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 n≥1；a_n 是满足 f(z)=f(zq)+zqf(zq²)、f(0)=1 的形式幂级数的 z^n 系数。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-1.79 · q-二项式级数的有限系数递推

$$
(1-q^n)A_n=(1-aq^{n-1})A_{n-1},\quad A_n=\frac{(a;q)_n}{(q;q)_n},\quad A_0=1.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`SILLS-1.79`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-1.79**（印刷页 41；1.79）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥1。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
