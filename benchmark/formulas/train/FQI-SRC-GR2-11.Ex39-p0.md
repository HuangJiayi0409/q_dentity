# FQI-SRC-GR2-11.Ex39-p0 · D 型 Jackson 的有限单纯形变式（已注明修订）

家族：A · 超几何型有限求和；难度：高；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\sum_{\substack{k_1,\ldots,k_d\ge0\\|k|\le N}}\frac{\Delta(zq^k)}{\Delta(z)}\prod_{s=1}^d\frac{1-az_sq^{k_s+|k|}}{1-az_s}\prod_{r<s}\frac1{(z_rz_s;q)_{k_r+k_s}}\prod_{r,s=1}^d\frac{(z_sb_r,z_s/b_r;q)_{k_s}}{(qz_s/z_r;q)_{k_s}}\prod_{r=1}^d\frac{(az_r;q)_{|k|}(aq/z_r;q)_{|k|-k_r}}{(aqb_r,aq/b_r;q)_{|k|}}\frac{(q^{-N},c,a^2q^{N+1}/c;q)_{|k|}q^{|k|}}{\prod_{s=1}^d(aqz_s/c,cz_s/(aq^N),az_sq^{N+1};q)_{k_s}}=\prod_{s=1}^d\frac{(aqz_s,aq/z_s,aqb_s/c,aq/(b_sc);q)_N}{(aqz_s/c,aq/(z_sc),aqb_s,aq/b_s;q)_N}.
$$

代表来源：`GR2-11.Ex39-p0`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-11.Ex39-p0**（GR；Chapter 11, 11.Ex39-p0, 印刷p348）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。d≥1,N≥0，ab_scz_s非零。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
