# FQI-SRC-GR2-8.Ex12 · Rogers 线性化的逆公式

家族：A · 超几何型有限求和；难度：高；集合：test。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
C_{m+n}(z;\beta)=\sum_{k=0}^{\min(m,n)}\frac{(q;q)_m(q;q)_n(\beta;q)_{m+n}}{(\beta;q)_m(\beta;q)_n(q;q)_{m+n}}\frac{(\beta^{-2}q^{-m-n},\beta^{-1};q)_k(1-\beta^{-2}q^{2k-m-n})}{(q,\beta^{-1}q^{1-m-n};q)_k(1-\beta^{-2}q^{-m-n})}(\beta^2/q)^kC_{m-k}(z;\beta)C_{n-k}(z;\beta).
$$

代表来源：`GR2-8.Ex12`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-8.Ex12**（GR；Chapter 8, 8.Ex12, 印刷p249）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。m,n≥0，βz≠0。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
