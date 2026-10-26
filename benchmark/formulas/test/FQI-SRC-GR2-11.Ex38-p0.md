# FQI-SRC-GR2-11.Ex38-p0 · D 型多变量有限 Jackson 求和

家族：A · 超几何型有限求和；难度：高；集合：test。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\sum_{\substack{k_1,\ldots,k_d\ge0\\|k|=N}}\frac{\Delta(zq^k)}{\Delta(z)}\prod_{r<s}\frac1{(z_rz_s;q)_{k_r+k_s}}\prod_{s=1}^d\frac{z_s^{k_s}q^{\binom{k_s}2}\prod_{r=1}^{d-1}(z_sa_r,z_s/a_r;q)_{k_s}}{(bz_s,z_sq^{1-N}/b;q)_{k_s}\prod_{r=1}^d(qz_s/z_r;q)_{k_s}}=(-bq^{N-1})^N\frac{\prod_{s=1}^{d-1}(ba_s,b/a_s;q)_N}{(q;q)_N\prod_{s=1}^d(bz_s,b/z_s;q)_N}.
$$

代表来源：`GR2-11.Ex38-p0`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-11.Ex38-p0**（GR；Chapter 11, 11.Ex38-p0, 印刷p348）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。d≥1,N≥0；a_s,b,z_s非零，Δ同11.7.1。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
