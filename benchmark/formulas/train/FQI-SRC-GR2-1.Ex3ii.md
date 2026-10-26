# FQI-SRC-GR2-1.Ex3ii · 有限 q 多项式定理

家族：A · 超几何型有限求和；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
(a_1\cdots a_{m+1};q)_n=\sum_{\substack{k_1,\ldots,k_m\ge0\\K=k_1+\cdots+k_m\le n}}\frac{(q;q)_n\prod_{j=1}^m(a_j;q)_{k_j}(a_{m+1};q)_{n-K}}{\prod_{j=1}^m(q;q)_{k_j}(q;q)_{n-K}}\prod_{j=2}^{m+1}a_j^{k_1+\cdots+k_{j-1}}.
$$

代表来源：`GR2-1.Ex3ii`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-1.Ex3ii**（GR；Chapter 1, 1.Ex3ii, 印刷p25）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。m≥1。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
