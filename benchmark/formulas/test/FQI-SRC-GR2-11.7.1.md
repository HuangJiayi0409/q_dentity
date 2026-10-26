# FQI-SRC-GR2-11.7.1 · Milne 的多变量有限 q 求和

家族：A · 超几何型有限求和；难度：高；集合：test。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\sum_{\substack{k_1,\ldots,k_d\ge0\\|k|=N}}\frac{\Delta(zq^k)}{\Delta(z)}\prod_{r,s=1}^d\frac{(a_rz_s/z_r;q)_{k_s}}{(qz_s/z_r;q)_{k_s}}=\frac{(a_1\cdots a_d;q)_N}{(q;q)_N},\quad\Delta(z)=\prod_{r<s}(z_r-z_s).
$$

代表来源：`GR2-11.7.1`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-11.7.1**（GR；Chapter 11, 11.7.1, 印刷p331）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。d≥1,N≥0，z_r非零且两两不同。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
