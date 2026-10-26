# 硬六角 G 多项式

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 本次未匹配到旧算法 6 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

## FQI-SRC-AQ-8.44 · G_N(0) 的 Schur 型有限展开

$$
G_N(0;q)=\sum_{\lambda=-N-2}^{N+2}(-1)^\lambda q^{\lambda(5\lambda+1)}\begin{bmatrix}N\\\lfloor(N-5\lambda)/2\rfloor+0\end{bmatrix}_q.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AQ-8.44`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_Q_supplement.md](../../round1_source_collection/records/ANDREWS_Q_supplement.md)；[ANDREWS_Q.md](../../round1_source_collection/books/ANDREWS_Q.md)。

- **AQ-8.44**（印刷页 80；式 (8.44)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 N≥1；G 的递推与初值见 (8.46)–(8.49)；G 的式在 N=0 也成立。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AQ-8.45 · G_N(1) 的 Schur 型有限展开

$$
G_N(1;q)=\sum_{\lambda=-N-2}^{N+2}(-1)^\lambda q^{\lambda(5\lambda-3)}\begin{bmatrix}N\\\lfloor(N-5\lambda)/2\rfloor+1\end{bmatrix}_q.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AQ-8.45`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_Q_supplement.md](../../round1_source_collection/records/ANDREWS_Q_supplement.md)；[ANDREWS_Q.md](../../round1_source_collection/books/ANDREWS_Q.md)。

- **AQ-8.45**（印刷页 80；式 (8.45)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 N≥1；G 的递推与初值见 (8.46)–(8.49)；G 的式在 N=0 也成立。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AQ-8.46 · 硬六角 G 多项式三阶递推

$$
G_N(\sigma)=G_{N-1}(\sigma)+qG_{N-2}(\sigma)-(q-q^{N-1})G_{N-3}(\sigma),\quad G_0(0)=1,\ G_0(1)=0,\ G_1(\sigma)=1,\ G_2(0)=1+q,\ G_2(1)=1.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`AQ-8.46`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_Q_supplement.md](../../round1_source_collection/records/ANDREWS_Q_supplement.md)；[ANDREWS_Q.md](../../round1_source_collection/books/ANDREWS_Q.md)。

- **AQ-8.46**（印刷页 81；式 (8.46)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 N≥3，σ∈{0,1}。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AQ-8.50 · G 偶指标倒数多项式

$$
q^{N^2}G_{2N}(0;q^{-1})=\sum_{k=-N-2}^{N+2}q^{5k^2-2k}\left(\begin{bmatrix}2N\\N-5k\end{bmatrix}_q-\begin{bmatrix}2N\\N-5k+2\end{bmatrix}_q\right).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AQ-8.50`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_Q_supplement.md](../../round1_source_collection/records/ANDREWS_Q_supplement.md)；[ANDREWS_Q.md](../../round1_source_collection/books/ANDREWS_Q.md)。

- **AQ-8.50**（印刷页 81；式 (8.50)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 N≥0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AQ-8.52 · G 倒数多项式的两组差分展开

$$
\begin{aligned}q^{N^2}G_{2N}(0;q^{-1})={}&\sum_{k=-N-2}^{N+2}q^{5k^2-2k}\left(\begin{bmatrix}2N-1\\N-5k\end{bmatrix}_q-\begin{bmatrix}2N-1\\N-5k+1\end{bmatrix}_q\right)\\&+q^N\sum_{k=-N-2}^{N+2}q^{5k^2+3k}\left(\begin{bmatrix}2N-1\\N-5k-1\end{bmatrix}_q-\begin{bmatrix}2N-1\\N-5k-3\end{bmatrix}_q\right).\end{aligned}
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`AQ-8.52`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_Q_supplement.md](../../round1_source_collection/records/ANDREWS_Q_supplement.md)；[ANDREWS_Q.md](../../round1_source_collection/books/ANDREWS_Q.md)。

- **AQ-8.52**（印刷页 81；式 (8.52)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 N≥1。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AQ-9.17 · G 多项式的有限系数展开（显式修订移位）

$$
G_N(0;q)=\sum_{\substack{n,j\ge0\\3n+2j\le N+1}}q^{n(3n-1)/2+j}\begin{bmatrix}n+N+1-3n-2j\\n\end{bmatrix}_q\begin{bmatrix}n+j-1\\j\end{bmatrix}_{q^2}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AQ-9.17`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_Q_supplement.md](../../round1_source_collection/records/ANDREWS_Q_supplement.md)；[ANDREWS_Q.md](../../round1_source_collection/books/ANDREWS_Q.md)。

- **AQ-9.17**（印刷页 90；式 (9.17)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 N≥0；n=0 时第二 Gaussian 按 δ_{j,0} 解释。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
