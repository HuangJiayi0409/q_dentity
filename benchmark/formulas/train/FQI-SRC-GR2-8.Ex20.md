# FQI-SRC-GR2-8.Ex20 · 特殊 Askey–Wilson 的有限线性化

家族：A · 超几何型有限求和；难度：高；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
P_m(z;a,q/a,-b,-q/b)P_n(z;a,q/a,-b,-q/b)=\sum_{k=0}^{2\min(m,n)}L_kP_{m+n-k}(z;a,q/a,-b,-q/b),\quad L_k=\frac{(q;q)_{2m}(q;q)_{2n}(q;q)_{m+n}}{(q;q)_m(q;q)_n(q;q)_{2m+2n}}b^{-k}q^{(3m+3n+1)k-3\binom k2}\frac{1-q^{2m+2n+1-2k}}{1-q^{2m+2n+1-k}}\frac{(q^{-2m-2n},-bq^{-m-n}/a,-abq^{-m-n-1};q)_k}{(q,q^{-2m},q^{-2n},q^{-m-n};q)_k}T_k(-bq^{m+n+1-k}/a,-bq^{-m-n}/a)T_k(-abq^{m+n-k},-abq^{-m-n-1}),\quad T_k(U,V)=\sum_{j=\max(0,k-m,k-n)}^{\min(k,m,n)}\frac{(q^{-k},q^{-m},q^{-n},U;q)_j(q^{-m},q^{-n};q)_{k-j}}{(q,V;q)_j}q^{(2k-m-n)j-j^2}.
$$

代表来源：`GR2-8.Ex20`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-8.Ex20**（GR；Chapter 8, 8.Ex20, 印刷p252）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。m,n≥0；a,b>0，P见7.5.3。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
