# FQI-SRC-GR2-8.Ex1i · 小 q-Jacobi 乘积的有限双和（一）

家族：A · 超几何型有限求和；难度：高；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\ell_n(x)\ell_n(y)=(-aq)^nq^{\binom n2}\frac{(bq;q)_n}{(aq;q)_n}\sum_{m=0}^n\frac{(q^{-n},abq^{n+1},x^{-1},y^{-1};q)_m}{(q,bq;q)_m}\left(\frac{xyq^{1-m}}a\right)^m\sum_{k=0}^m\frac{(q^{-m},b^{-1}q^{-m};q)_k(abxy)^kq^{k^2+2k}}{(q,aq,xq^{1-m},yq^{1-m};q)_k}.
$$

代表来源：`GR2-8.Ex1i`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-8.Ex1i**（GR；Chapter 8, 8.Ex1i, 印刷p245）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。ℓ=ℓ_n(·;a,b)，abxy≠0。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
