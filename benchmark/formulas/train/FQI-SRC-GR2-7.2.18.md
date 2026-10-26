# FQI-SRC-GR2-7.2.18 · q-Racah 有限正交及对偶正交

家族：A · 超几何型有限求和；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\sum_{x=0}^N\rho_x W_m(x)W_n(x)=\delta_{mn}/h_n,\qquad\sum_{n=0}^Nh_nW_n(x)W_n(y)=\delta_{xy}/\rho_x,\quad\rho_x=\frac{(cq^{-N},aq,bcq,q^{-N};q)_x(1-cq^{2x-N})}{(q,cq^{-N}/a,q^{-N}/b,cq;q)_x(1-cq^{-N})}(abq)^{-x},\quad h_n=\frac{(bq,aq/c;q)_N}{(abq^2,1/c;q)_N}\frac{(abq,aq,bcq,q^{-N};q)_n(1-abq^{2n+1})q^{Nn}c^{-n}}{(q,bq,aq/c,abq^{N+2};q)_n(1-abq)}.
$$

代表来源：`GR2-7.2.18`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-7.2.18**（GR；Chapter 7, 7.2.18, 印刷p180）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。N≥0，0≤m,n,x,y≤N；W_n(x)=4φ3^[min(n,x)](q^{-n},abq^{n+1},q^{-x},cq^{x-N};aq,q^{-N},bcq;q,q)，abc≠0。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
