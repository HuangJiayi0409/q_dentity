# FQI-SRC-GR2-11.Ex40-p0 · 多变量终止 Bailey 变换

家族：A · 超几何型有限求和；难度：高；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\mathcal S(a;b,c,d;e,f,g)=\left(\frac a\lambda\right)^{|m|}\frac{(\lambda q/f,\lambda q/g;q)_{|m|}}{(aq/f,aq/g;q)_{|m|}}\prod_{s=1}^{\ell}\frac{(aqz_s,\lambda qz_s/d;q)_{m_s}}{(\lambda qz_s,aqz_s/d;q)_{m_s}}\mathcal S(\lambda;\lambda b/a,\lambda c/a,d;\lambda e/a,f,g),\quad\lambda=a^2q/(bce),\quad a^3q^{2+|m|}=bcdefg,\quad\mathcal S(A;B,C,D;E,F,G)=\sum_{0\le k_s\le m_s}\frac{\Delta(zq^k)}{\Delta(z)}q^{|k|}\prod_{s=1}^{\ell}\frac{1-Az_sq^{k_s+|k|}}{1-Az_s}\frac{(B,C,D;q)_{|k|}}{(Aq/E,Aq/F,Aq/G;q)_{|k|}}\prod_{r=1}^{\ell}\frac{(Az_r;q)_{|k|}}{(Az_rq^{m_r+1};q)_{|k|}}\prod_{s=1}^{\ell}\frac{(Ez_s,Fz_s,Gz_s;q)_{k_s}}{(Aqz_s/B,Aqz_s/C,Aqz_s/D;q)_{k_s}}\prod_{r,s=1}^{\ell}\frac{(q^{-m_r}z_s/z_r;q)_{k_s}}{(qz_s/z_r;q)_{k_s}}.
$$

代表来源：`GR2-11.Ex40-p0`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-11.Ex40-p0**（GR；Chapter 11, 11.Ex40-p0, 印刷p349）：ℓ≥1，m_s≥0，z_s两两不同；a³q^{2+|m|}=bcdefg，λ=a²q/(bce)；所有实际分母非零；p=0。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
