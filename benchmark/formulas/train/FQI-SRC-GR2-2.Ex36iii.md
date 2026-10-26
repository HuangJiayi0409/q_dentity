# FQI-SRC-GR2-2.Ex36iii · 任意阶终止级数的 Gasper 展开

家族：A · 超几何型有限求和；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
{}_{r+2}\phi_{s+1}^{[n]}(q^{-n},\nu,\boldsymbol a;\gamma,\boldsymbol b;q,z)=\frac{(\lambda,\nu;q)_n}{(\gamma,\mu;q)_n}\sum_{k=0}^n\frac{(q^{-n},\gamma\mu/(\lambda\nu);q)_{n-k}}{(q,q^{1-n}/\lambda;q)_{n-k}}q^{n-k}{}_3\phi_2^{[n-k]}(\mu/\nu,\gamma/\nu,q^{k-n};\gamma\mu/(\lambda\nu),q^{1-n}/\nu;q,q^{1-k}/\lambda){}_{r+2}\phi_{s+1}^{[k]}(q^{-k},\mu,\boldsymbol a;\lambda,\boldsymbol b;q,z).
$$

代表来源：`GR2-2.Ex36iii`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-2.Ex36iii**（GR；Chapter 2, 2.Ex36iii, 印刷p67）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。r,s≥0，a长r、b长s；λν≠0。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
