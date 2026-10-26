# Fine 基本级数的有限系数变换

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 本次未匹配到旧算法 6 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

## FQI-SRC-FINE-2.3 · 基本级数有限系数比递推

$$
(1-bq^{n+1})c_{n+1}=(1-aq^{n+1})c_n.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`FINE-2.3`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[FINE_supplement.md](../../round1_source_collection/records/FINE_supplement.md)；[FINE.md](../../round1_source_collection/books/FINE.md)。

- **FINE-2.3**（印刷页 2；式 (2.3)）：q 为形式变量；数值代入要求所有实际分母非零，Gaussian 在奇点先作多项式延拓。空乘积为 1、空和为 0。n≥0；c_n=(aq;q)_n/(bq;q)_n；与§15的A_n不同。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-FINE-4.coeff · 基本级数有限系数差分

$$
c_n-c_{n-1}=\frac{(b-a)q^n}{1-aq^n}c_n.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`FINE-4.coeff`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[FINE_supplement.md](../../round1_source_collection/records/FINE_supplement.md)；[FINE.md](../../round1_source_collection/books/FINE.md)。

- **FINE-4.coeff**（印刷页2；(4.2) 后、页末的无编号系数差分）：q 为形式变量；数值代入要求所有实际分母非零，Gaussian 在奇点先作多项式延拓。空乘积为 1、空和为 0。n≥1；c_n=(aq;q)_n/(bq;q)_n；1−aq^n≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-FINE-7.GH · q-移位迭代的有限累积系数

$$
H_n=\frac{(b/a;q)_{n+1}}{(bq;q)_{n+1}(b/(at);q)_{n+1}},\qquad G_n=-\frac{b/(at)}{1-b/(at)}\sum_{j=0}^n\frac{(b/a;q)_j q^j}{(bq;q)_j(bq/(at);q)_j}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`FINE-7.GH`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[FINE_supplement.md](../../round1_source_collection/records/FINE_supplement.md)；[FINE.md](../../round1_source_collection/books/FINE.md)。

- **FINE-7.GH**（印刷页5；§7 开头、(7.1) 前的无编号 H_n、G_n）：q 为形式变量；数值代入要求所有实际分母非零，Gaussian 在奇点先作多项式延拓。空乘积为 1、空和为 0。n≥0，at≠0；L_j=bq^j/(bq^j−at)，M_j=(bq^j−a)t/((1−bq^{j+1})(bq^j−at))；H_{−1}=1,G_{−1}=0；H_n=M_nH_{n−1},G_n=G_{n−1}+L_nH_{n−1}。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-FINE-15.2 · Fine 系数的有限卷积

$$
A_N=\sum_{k=0}^N\frac{(-1)^k(aq;q)_{N-k}q^{k(k-1)/2}}{(bq;q)_{N-k}(q;q)_k}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`FINE-15.2`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[FINE_supplement.md](../../round1_source_collection/records/FINE_supplement.md)；[FINE.md](../../round1_source_collection/books/FINE.md)。

- **FINE-15.2**（印刷页 16；式 (15.2)；§15 A special development）：q 为形式变量；数值代入要求所有实际分母非零，Gaussian 在奇点先作多项式延拓。空乘积为 1、空和为 0。N≥0；A_N=[t^N](t;q)_\infty F(a,b;t)，F(a,b;t)=\sum_{j≥0}(aq;q)_jt^j/(bq;q)_j。A_0=1。这里只收录固定 N 的有限系数表达。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-FINE-15.31 · Fine 系数的一阶递推

$$
(1-bq^n)A_n=-aq^n A_{n-1}+\frac{(-1)^n(1-b)q^{n(n+1)/2}}{(q;q)_n}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`FINE-15.31`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[FINE_supplement.md](../../round1_source_collection/records/FINE_supplement.md)；[FINE.md](../../round1_source_collection/books/FINE.md)。

- **FINE-15.31**（印刷页 17；式 (15.31)）：q 为形式变量；数值代入要求所有实际分母非零，Gaussian 在奇点先作多项式延拓。空乘积为 1、空和为 0。n≥1，A_0=1；A_n 同 (15.2)。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-FINE-15.41 · Fine 系数的第二有限展开

$$
A_N=\frac{(-a)^Nq^{N(N+1)/2}}{(bq;q)_N}\sum_{j=0}^N\frac{(b;q)_j a^{-j}}{(q;q)_j}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`FINE-15.41`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[FINE_supplement.md](../../round1_source_collection/records/FINE_supplement.md)；[FINE.md](../../round1_source_collection/books/FINE.md)。

- **FINE-15.41**（印刷页 17；式 (15.41)）：q 为形式变量；数值代入要求所有实际分母非零，Gaussian 在奇点先作多项式延拓。空乘积为 1、空和为 0。N≥0，a≠0；A_N 同 (15.2)。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
