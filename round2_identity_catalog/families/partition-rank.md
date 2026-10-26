# 分拆 rank、累计截面与同余

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 本次未匹配到旧算法 1 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

## FQI-SRC-FINE-25.shell · 固定最大部件与 rank 的有限生成多项式

$$
\sum_{\substack{\lambda_1=L\\\lambda_1-\ell(\lambda)=r}}q^{|\lambda|}=q^{2L-r-1}\begin{bmatrix}2L-r-2\\L-1\end{bmatrix}_q.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`FINE-25.shell`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[FINE_supplement.md](../../round1_source_collection/records/FINE_supplement.md)；[FINE.md](../../round1_source_collection/books/FINE.md)。

- **FINE-25.shell**（印刷页 52；(25.9) 前的 outside shell 论证及无编号 Gaussian 多项式）：q 为形式变量；数值代入要求所有实际分母非零，Gaussian 在奇点先作多项式延拓。空乘积为 1、空和为 0。L≥1，0≤r<L 为整数；λ 为非空分拆，ℓ(λ) 是部件数。左侧恰有 L−r 个正部件，且每个≤L。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
