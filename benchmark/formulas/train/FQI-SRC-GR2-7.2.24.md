# FQI-SRC-GR2-7.2.24 · 对偶 q-Hahn 有限正交

家族：A · 超几何型有限求和；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\sum_{x=0}^ND_m(x)D_n(x)\frac{(cq^{-N},bcq,q^{-N};q)_x(1-cq^{2x-N})}{(q,q^{-N}/b,cq;q)_x(1-cq^{-N})}q^{Nx-x(x-1)/2}(-bcq)^{-x}=\frac{(1/c;q)_N(q,bq;q)_n}{(bq;q)_N(bcq,q^{-N};q)_n}(cq^{-N})^n\delta_{mn}.
$$

代表来源：`GR2-7.2.24`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-7.2.24**（GR；Chapter 7, 7.2.24, 印刷p181）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。N≥0，0≤m,n≤N；D_n(x)=3φ2^[min(n,x)](q^{-n},q^{-x},cq^{x-N};q^{-N},bcq;q,q)，bc≠0。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
