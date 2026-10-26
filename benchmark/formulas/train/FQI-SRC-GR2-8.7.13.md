# FQI-SRC-GR2-8.7.13 · 有限 q-Racah Poisson 核展开

家族：A · 超几何型有限求和；难度：高；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\sum_{n=0}^Nt^nh_nW_n(x;a,b,c,N)W_n(y;\alpha,ab/\alpha,\gamma,M)=h_0\sum_{r=0}^x\sum_{s=0}^{N-x}\frac{(abq^2;q)_{2r+2s}}{(abq^{N+2};q)_{r+s}}H_{r,s}A_{r,s}C_{r,s}(-t)^{r+s}q^{(r+s)(2N-r-s+1)/2},\quad C_{r,s}=\sum_{j=0}^{N-r-s}\frac{1-\lambda q^{2j}}{1-\lambda}\frac{(\lambda,q^{r+s-N};q)_j}{(q,abq^{N+r+s+2};q)_j}(tq^{N-r-s})^j,\quad\lambda=abq^{2r+2s+1}.
$$

代表来源：`GR2-8.7.13`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-8.7.13**（GR；Chapter 8, 8.7.13, 印刷p231）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。0≤x≤N≤M，0≤y≤M；h,H,A和零系数约定见7.2.18及8.Ex8。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
