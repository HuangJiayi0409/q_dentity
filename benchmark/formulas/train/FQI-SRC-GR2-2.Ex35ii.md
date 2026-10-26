# FQI-SRC-GR2-2.Ex35ii · Gasper 离散分式积分的有限展开（二）

家族：A · 超几何型有限求和；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
{}_3\phi_2^{[n]}(\alpha,\beta,q^{-n};\gamma,\delta;q,q)=\sum_{k=0}^n\begin{bmatrix}n\\k\end{bmatrix}_q\frac{(\lambda,\delta/\sigma;q)_k(\gamma/\lambda;q)_{n-k}}{(\gamma;q)_n(\delta;q)_k}\lambda^n(\sigma/\lambda)^k{}_3\phi_2^{[k]}(\alpha/\sigma,\beta,q^{-k};\lambda,\delta/\sigma;q,q){}_3\phi_2^{[n-k]}(\sigma,\beta/\lambda,q^{k-n};\gamma/\lambda,\delta q^k;q,q).
$$

代表来源：`GR2-2.Ex35ii`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-2.Ex35ii**（GR；Chapter 2, 2.Ex35ii, 印刷p66）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。λσ≠0。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
