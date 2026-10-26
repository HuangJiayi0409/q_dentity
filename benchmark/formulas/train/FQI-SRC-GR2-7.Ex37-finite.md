# FQI-SRC-GR2-7.Ex37-finite · 加权有限多项式的 q 差分关系

家族：C · 递推与差分关系；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\mathcal D_q\left[\frac{U_n(z)}{(\rho qz,\rho q/z;q)_n}\right]=-\frac{1-\rho^2q^n}{1-q^{n+1}}\frac{T_n(z)U_{n+1}(sz)-T_n(z^{-1})U_{n+1}(z/s)}{(s-s^{-1})(z-z^{-1})/2},\quad T_n(z)=\frac{1-q^{-n}/(\rho sz)}{(\rho qs z;q)_n(\rho s/z;q)_{n+1}},\quad U_n(z)=A_{n,r}(\rho qz,\rho q/z;q)_n{}_6\phi_5^{[r-n]}(q^{n-r},\rho^2\lambda^2q^{n+r+1},\rho sq^n,\rho^2q^n,\rho q^{n+1}z,\rho q^{n+1}/z;\rho^2q^{2n+1},\rho\lambda q^{n+1},\rho^2q^{n+1},-\rho\lambda q^{n+1},-\rho sq^n;q,q),\quad A_{n,r}=\frac{(q;q)_n(\rho^2\lambda^2q;q)_{n+r}s^{3n^2+n-2nr}\rho^{2n}}{(q;q)_{r-n}(\rho q,\rho^2q,\rho\lambda q,-\rho q,-\rho s,-\rho s,-\rho\lambda q;q)_n},\quad s^2=q.
$$

代表来源：`GR2-7.Ex37-finite`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-7.Ex37-finite**（GR；Chapter 7, 7.Ex37-finite, 印刷p208）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。1≤n≤r；U_{r+1}=0，ρ=q^ν,λ=q^λ_original非零，D_q见7.7.6。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
