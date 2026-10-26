# FQI-SRC-GR2-2.Ex36ii · 平衡终止 4φ3 的双级数展开

家族：A · 超几何型有限求和；难度：高；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
{}_4\phi_3^{[n]}(\alpha,\beta,\nu q^n,q^{-n};\gamma,\delta,\rho;q,q)=\frac{(\gamma/\lambda,\nu q/\gamma;q)_n}{(\gamma,\lambda\nu q/\gamma;q)_n}\lambda^n\sum_{k=0}^n\frac{(\lambda\nu/\gamma,\lambda,\rho/\alpha,\delta/\sigma,\nu q^n,q^{-n};q)_k(\lambda\nu q/\gamma;q)_{2k}}{(q,\nu q/\gamma,\delta,\rho\sigma/\alpha,\lambda q^{1-n}/\gamma,\nu\lambda q^{n+1}/\gamma;q)_k(\lambda\nu/\gamma;q)_{2k}}(\sigma q/\gamma)^k{}_4\phi_3^{[k]}(\alpha/\sigma,\beta,\lambda\nu q^k/\gamma,q^{-k};\lambda,\delta/\sigma,\rho;q,q){}_4\phi_3^{[n-k]}(\sigma,\beta/\lambda,\nu q^{n+k},q^{k-n};\gamma/\lambda,\delta q^k,\sigma\rho q^k/\alpha;q,q).
$$

代表来源：`GR2-2.Ex36ii`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-2.Ex36ii**（GR；Chapter 2, 2.Ex36ii, 印刷p67）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。αβνq=δγρ；αλγσν≠0。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
