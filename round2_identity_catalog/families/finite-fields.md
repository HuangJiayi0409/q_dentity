# 有限域子空间、向量组与矩阵计数

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 本次未匹配到旧算法 3 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

## FQI-SUBSPACE-COUNT · 有限域子空间计数

$$
\begin{bmatrix}n\\k\end{bmatrix}_q=\#\{U\le\mathbb F_q^n:\dim U=k\}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-1.NoteEx2-subspace`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-1.NoteEx2-subspace**（Chapter 1, 1.NoteEx2-subspace, 印刷p35）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。q为素数幂，0≤k≤n。
  对应：代表式；保留本条来源域。
- **AP-13.T1**（p.212, Theorem 13.1；乘积证明 p.213）：q 为素数幂；0≤m≤n 为整数。
  对应：m→k；附带乘积是 Gaussian 定义，不另计命题。
- **SILLS-1.Rem1.54**（印刷页 34；1.Rem1.54）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0，0≤k≤n；q为素数幂。
  对应：逐项相同。
- **KAC-CHEUNG-7.1**（印刷页 21；7.1）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。q为素数幂；0≤j≤n。
  对应：j→k。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-KAC-CHEUNG-7.2 · 有序线性无关向量组计数

$$
\#\{(v_1,\ldots,v_j)\in(\mathbb F_q^n)^j:\operatorname{rank}(v_1,\ldots,v_j)=j\}=\prod_{i=0}^{j-1}(q^n-q^i).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`KAC-CHEUNG-7.2`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[KAC_CHEUNG_supplement.md](../../round1_source_collection/records/KAC_CHEUNG_supplement.md)；[KAC_CHEUNG.md](../../round1_source_collection/books/KAC_CHEUNG.md)。

- **KAC-CHEUNG-7.2**（印刷页 22；7.2）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。q为素数幂；0≤j≤n。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-KAC-CHEUNG-7.rank · 有限域定秩矩阵计数

$$
\#\{A\in\mathbb F_q^{m\times n}:\operatorname{rank}A=j\}=\begin{bmatrix}n\\j\end{bmatrix}_q\begin{bmatrix}m\\j\end{bmatrix}_q\prod_{i=0}^{j-1}(q^j-q^i)=\begin{bmatrix}n\\j\end{bmatrix}_q\prod_{i=0}^{j-1}(q^m-q^i).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`KAC-CHEUNG-7.rank`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[KAC_CHEUNG_supplement.md](../../round1_source_collection/records/KAC_CHEUNG_supplement.md)；[KAC_CHEUNG.md](../../round1_source_collection/books/KAC_CHEUNG.md)。

- **KAC-CHEUNG-7.rank**（印刷页 25；7.rank）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。q为素数幂；0≤j≤min(m,n)。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
