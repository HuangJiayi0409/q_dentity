# FQI-SRC-GR2-8.9.8 · 双连续 q-超球平方展开（修订）

家族：A · 超几何型有限求和；难度：高；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
{}_7\phi_6^{[n]}(q^{-n},q^{n+\alpha+2},q^{(\alpha+1)/2},q^{(\alpha+1)/2}z^2,q^{(\alpha+1)/2}/z^2,q^{(\alpha+2)/2}w^2,q^{(\alpha+2)/2}/w^2;q^{\alpha+1},q^{(\alpha+3)/2},-q^{(\alpha+3)/2},-q^{(\alpha+2)/2},-q^{(\alpha+2)/2},-q^{(\alpha+1)/2};q,q)=\sum_{j=0}^n\frac{(q^{-n},q^{n+\alpha+2},q^{(\alpha+2)/2},q^{(\alpha+2)/2}w^2,q^{(\alpha+2)/2}/w^2;q)_j(-1)^jq^{j+\binom j2}}{(q,q^{(\alpha+3)/2},-q^{(\alpha+3)/2},-q^{(\alpha+2)/2},q^{j+\alpha+1};q)_j}\left[\frac{(q;q)_j(q;q)_{n-j}q^{[n(\alpha+2)+2j(n-j)-j]/4}}{(q^{\alpha+1};q)_j(q^{2j+\alpha+2};q)_{n-j}}C_j(z;q^{(\alpha+1)/2})C_{n-j}(w;q^{j+(\alpha+2)/2})\right]^2.
$$

代表来源：`GR2-8.9.8`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-8.9.8**（GR；Chapter 8, 8.9.8, 印刷p238）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。zw≠0；所有幂取相容分支。所有实际分母非零；见修订报告。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
