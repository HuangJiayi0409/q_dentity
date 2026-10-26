# FQI-SRC-GR2-8.Ex21 · Askey–Wilson 有限卷积恒等式

家族：A · 超几何型有限求和；难度：高；集合：test。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\sum_{k=0}^{m+n}b^{m-k}\begin{bmatrix}m+n\\k\end{bmatrix}_q\frac{(b^2;q)_n(a^2b^2c^2q^{m+n-1};q)_k(c^2;q)_m}{(c^2,b^2c^2q^{k-1};q)_k(b^2c^2q^{2k};q)_{m+n-k}}{}_4\phi_3^{[\min(k,n)]}(q^{-k},b^2c^2q^{k-1},q^{-n},a^2b^2q^{n-1};b^2,a^2b^2c^2q^{m+n-1},q^{-m-n};q,q)P_k(w_2;bw_1,b/w_1,cs,c/s)P_{m+n-k}(w_1;at,a/t,bcsq^k,bcq^k/s)=P_n(w_1;at,a/t,bw_2,b/w_2)P_m(w_2;abtq^n,abq^n/t,cs,c/s).
$$

代表来源：`GR2-8.Ex21`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-8.Ex21**（GR；Chapter 8, 8.Ex21, 印刷p252）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。m,n≥0；abcstw1w2≠0；P见7.5.3。所有实际分母非零；见修订报告。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
