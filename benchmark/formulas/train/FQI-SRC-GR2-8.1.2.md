# FQI-SRC-GR2-8.1.2 · 成对有限积的线性化

家族：A · 超几何型有限求和；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
(t,a/t;q)_j(t,a/t;q)_k=(q;q)_j(q;q)_k(a;q)_{j+k}\sum_{m=\max(j,k)}^{j+k}\frac{(t,a/t;q)_m(-1)^{j+k+m}q^{\binom j2+\binom k2+\binom{m+1}2-m(j+k)}}{(a;q)_m(q;q)_{m-j}(q;q)_{m-k}(q;q)_{j+k-m}}.
$$

代表来源：`GR2-8.1.2`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-8.1.2**（GR；Chapter 8, 8.1.2, 印刷p217）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。j,k≥0，t≠0。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
