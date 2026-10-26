# Lusztig–Macdonald–Wall 多项式

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 本次未匹配到旧算法 2 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

## FQI-SRC-AQ-10.1 · Lusztig–Macdonald–Wall 多项式递推

$$
X_{-1}(a,b,q)=a,\quad X_0(a,b,q)=b,\quad X_{2n+1}=X_{2n}+q^{2n+1}X_{2n-1},\quad X_{2n+2}=X_{2n+1}+q^{n+1}(1+q^{n+1})(X_{2n}+X_{2n-1}).
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`AQ-10.1`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_Q_supplement.md](../../round1_source_collection/records/ANDREWS_Q_supplement.md)；[ANDREWS_Q.md](../../round1_source_collection/books/ANDREWS_Q.md)。

- **AQ-10.1**（印刷页 95；式 (10.1)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 n≥0；a,b 为自由参数。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AQ-10.5 · LMW 的 Gaussian 展开（显式修订下标）

$$
X_{2n-1}(1,1,q)=\begin{bmatrix}2n\\n\end{bmatrix}_q+2\sum_{j=1}^{\lfloor n/2\rfloor}q^{j^2}\begin{bmatrix}2n\\n-2j\end{bmatrix}_q.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AQ-10.5`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_Q_supplement.md](../../round1_source_collection/records/ANDREWS_Q_supplement.md)；[ANDREWS_Q.md](../../round1_source_collection/books/ANDREWS_Q.md)。

- **AQ-10.5**（印刷页 98；式 (10.5)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 n≥0；X 由 (10.1)–(10.2) 定义。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
