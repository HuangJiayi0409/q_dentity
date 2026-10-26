# Schur 有界分拆与模3递推

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 本次未匹配到旧算法 3 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

## FQI-SRC-AQ-6.18 · Schur 辅助系数递推

$$
a_0(q)=1,\quad a_n(q)=\frac{(1+q^{3n-1})(1+q^{3n-2})}{1-q^{3n}}a_{n-1}(q)\quad(n\ge1).
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`AQ-6.18`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_Q_supplement.md](../../round1_source_collection/records/ANDREWS_Q_supplement.md)；[ANDREWS_Q.md](../../round1_source_collection/books/ANDREWS_Q.md)。

- **AQ-6.18**（印刷页 55；式 (6.18)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 \(a_n=[x^n]G_0(x)/(x;q^3)_\infty\)，见 (6.15)–(6.17)。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AQ-6.19 · Schur 辅助系数的有限乘积

$$
a_n(q)=\frac{(-q,-q^2;q^3)_n}{(q^3;q^3)_n}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AQ-6.19`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_Q_supplement.md](../../round1_source_collection/records/ANDREWS_Q_supplement.md)；[ANDREWS_Q.md](../../round1_source_collection/books/ANDREWS_Q.md)。

- **AQ-6.19**（印刷页 56；式 (6.19)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 n≥0；a_n 由 (6.18) 的系数关系和 a₀=1 确定。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-2.76-78 · Schur 有界分拆的三项耦合递推

$$
\begin{aligned}S_{3n}&=S_{3n-1}+q^{3n}S_{3n-4},\\S_{3n-1}&=S_{3n-2}+x^{-1}q^{3n-1}S_{3n-4},\\S_{3n-2}&=S_{3n-3}+xq^{3n-2}S_{3n-5}.\end{aligned}
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`SILLS-2.76-78`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：S_N见(2.75)。

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-2.76-78**（印刷页 78；2.76-78）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥2；小指标由S_N的分拆定义给出。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
