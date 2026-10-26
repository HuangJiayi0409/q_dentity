# Bressoud 有限 Rogers–Ramanujan

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 本次未匹配到旧算法 5 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

## FQI-SRC-SILLS-4.35 · Bressoud 多项式二阶递推

$$
B_{n+2}=(q^{2n+3}+q-q^{n+2}+1)B_{n+1}-q(1-q^{n+1})B_n,\quad B_0=1,\ B_1=1+q.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`SILLS-4.35`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：B_n=\sum_{k=0}^nq^{k^2}{n\brack k}_q\quad\text{(4.32)}.

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-4.35**（印刷页 128；4.35）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-4.37 · Bressoud 第一有限 Rogers–Ramanujan 恒等式

$$
\sum_{k=0}^nq^{k^2}\begin{bmatrix}n\\k\end{bmatrix}_q=\sum_{k=-n-1}^{n+1}(-1)^kq^{k(5k+1)/2}\begin{bmatrix}2n\\n+2k\end{bmatrix}_q.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`SILLS-4.37`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-4.37**（印刷页 128；4.37）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-4.38 · Bressoud 多项式的五阶递推

$$
\begin{aligned}0={}&B_{n+5}-(1+q+q^2+q^3+q^4+q^{2n+7}+q^{2n+8}+q^{2n+9})B_{n+4}\\&+q(q^{4n+12}+q^{2n+10}+q^{2n+6}+q^{2n+7}+2q^{2n+8}+2q^{2n+9}+q^{4n+13}+q^{4n+14}+q^6+q^5+2q^4+2q^3+2q^2+q+1)B_{n+3}\\&-q^3(q^{4n+12}+q^{2n+7}+q^{2n+8}+q^{2n+9}+q^{4n+11}+q^{6n+15}+q^6+q^5+2q^4+2q^3+2q^2+q+1)B_{n+2}\\&-q^6(q^{5n+10}+q^{2n+3}+q^{2n+4}+q^{2n+5}+q^{5n+8}-q^4-q^3-q^2-q-1)B_{n+1}\\&-q^{10}(q^{2n+1}-1)(q^{2n+2}-1)B_n.\end{aligned}
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`SILLS-4.38`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-4.38**（印刷页 129；4.38）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0；B_n见(4.32)/(4.37)。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-4.Sym · Bressoud 双边和的对称化

$$
B_n=\frac12\sum_{k=-n-1}^{n+1}(-1)^kq^{k(5k+1)/2}(1+q^{-k})\begin{bmatrix}2n\\n+2k\end{bmatrix}_q.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`SILLS-4.Sym`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-4.Sym**（印刷页 129；4.Sym）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-4.43 · Bressoud 第二有限 Rogers–Ramanujan 恒等式

$$
\sum_{k=0}^nq^{k(k+1)}\begin{bmatrix}n\\k\end{bmatrix}_q=\sum_{k=-n-2}^{n+2}(-1)^kq^{k(5k+3)/2}\begin{bmatrix}2n+1\\n+2k+1\end{bmatrix}_q.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`SILLS-4.43`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-4.43**（印刷页 133；4.43）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
