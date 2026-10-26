# FQI-SRC-GR2-1.Ex4ii · 任意阶终止基本超几何和反向求和

家族：A · 超几何型有限求和；难度：低；集合：test。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
{}_{r+1}\phi_s^{[n]}\!\left[\begin{matrix}a_1,\ldots,a_r,q^{-n}\\b_1,\ldots,b_s\end{matrix};q,z\right]=\frac{\prod_i(a_i;q)_n}{\prod_j(b_j;q)_n}(z/q)^n\left((-1)^nq^{n(n-1)/2}\right)^{s-r-1}\sum_{k=0}^n\frac{(q^{-n};q)_k\prod_j(q^{1-n}/b_j;q)_k}{(q;q)_k\prod_i(q^{1-n}/a_i;q)_k}\left(\frac{\prod_jb_j}{\prod_ia_i}\frac{q^{n+1}}z\right)^k.
$$

代表来源：`GR2-1.Ex4ii`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-1.Ex4ii**（GR；Chapter 1, 1.Ex4ii, 印刷p25）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。r,s≥0；a_i,b_j,z非零。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
