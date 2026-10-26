# FQI-SRC-AP-3.4.2 · 逆序数的 q-多项系数生成式

家族：C · 递推与差分关系；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\sum_{s=0}^{S}\operatorname{inv}(m_1,\ldots,m_r;s)q^s=\frac{(q;q)_{m_1+\cdots+m_r}}{\prod_{i=1}^r(q;q)_{m_i}}.
$$

代表来源：`AP-3.4.2`。

局部定义：inv/ind 分别数多重集合 {1^{m₁},…,r^{mᵣ}} 中逆序数/下降位置之和为 s 的不同排列。

来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **AP-3.4.2**（ANDREWS-P；p.41, Theorem 3.6, (3.4.2)）：r≥1；所有 m_i≥0 为整数；S=Σ_{i<j}m_i m_j。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_P.md`
- `round1_source_collection/records/ANDREWS_P_supplement.md`
