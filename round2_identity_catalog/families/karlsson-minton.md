# q-Karlsson–Minton 消去与求值

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 本次未匹配到旧算法 4 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

## FQI-SRC-GR2-1.9.10 · 终止 q-Karlsson–Minton 求和

$$
{}_{r+2}\phi_{r+1}^{[n]}\!\left[\begin{matrix}q^{-n},b,b_1q^{m_1},\ldots,b_rq^{m_r}\\bq,b_1,\ldots,b_r\end{matrix};q,q\right]=\frac{b^n(q;q)_n}{(bq;q)_n}\prod_{i=1}^r\frac{(b_i/b;q)_{m_i}}{(b_i;q)_{m_i}}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-1.9.10`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-1.9.10**（Chapter 1, 1.9.10, 印刷p20）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。r≥0，m_i≥0，n≥M=Σm_i，b≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-1.9.11 · 终止 q-Karlsson–Minton 消去

$$
{}_{r+1}\phi_r^{[n]}\!\left[\begin{matrix}q^{-n},b_1q^{m_1},\ldots,b_rq^{m_r}\\b_1,\ldots,b_r\end{matrix};q,q\right]=0.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-1.9.11`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-1.9.11**（Chapter 1, 1.9.11, 印刷p20）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。r≥0，m_i≥0，n>M=Σm_i。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-1.9.12 · 单位自变量的终止 q-Karlsson–Minton

$$
{}_{r+1}\phi_r^{[n]}\!\left[\begin{matrix}q^{-n},b_1q^{m_1},\ldots,b_rq^{m_r}\\b_1,\ldots,b_r\end{matrix};q,1\right]=\frac{(-1)^n(q;q)_nq^{-n(n+1)/2}}{\prod_{i=1}^r(b_i;q)_{m_i}}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-1.9.12`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-1.9.12**（Chapter 1, 1.9.12, 印刷p20）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。r≥0，m_i≥0，n≥M=Σm_i。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-1.9.9-finite · 边界长度的 q-Karlsson–Minton 求值

$$
{}_{r+1}\phi_r^{[M]}\!\left[\begin{matrix}q^{-M},b_1q^{m_1},\ldots,b_rq^{m_r}\\b_1,\ldots,b_r\end{matrix};q,q\right]=(-1)^M(q;q)_M\prod_{i=1}^r\frac{b_i^{m_i}q^{m_i(m_i-1)/2}}{(b_i;q)_{m_i}}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-1.9.9-finite`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-1.9.9-finite**（Chapter 1, 1.9.9-finite, 印刷p20）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。r≥0，m_i≥0，M=Σm_i。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
