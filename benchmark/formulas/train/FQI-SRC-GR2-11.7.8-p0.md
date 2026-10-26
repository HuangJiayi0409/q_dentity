# FQI-SRC-GR2-11.7.8-p0 · Milne 的 A 型多变量 Jackson 求和

家族：A · 超几何型有限求和；难度：高；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\sum_{\substack{k_1,\ldots,k_d\ge0\\|k|=N}}\frac{\Delta(zq^k)}{\Delta(z)}\prod_{r=1}^d\frac{\prod_{s=1}^{d+1}(a_sz_r;q)_{k_r}}{(bz_r;q)_{k_r}\prod_{s=1}^d(qz_r/z_s;q)_{k_r}}=\frac{(b/a_1,\ldots,b/a_{d+1};q)_N}{(q,bz_1,\ldots,bz_d;q)_N},\quad b=\prod_{s=1}^{d+1}a_s\prod_{r=1}^dz_r.
$$

代表来源：`GR2-11.7.8-p0`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-11.7.8-p0**（GR；Chapter 11, 11.7.8-p0, 印刷p332）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。d≥1,N≥0，a_s,z_r非零，Δ同11.7.1。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
