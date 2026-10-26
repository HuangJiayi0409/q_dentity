# FQI-SRC-GR2-8.Ex28 · 相伴连续 q-超球线性化公式

家族：A · 超几何型有限求和；难度：高；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
C_m^\alpha(z;\beta)C_n^\alpha(z;\beta)=\sum_{k=0}^{\min(m,n)}L_kC_{m+n-2k}^\alpha(z;\beta),\quad L_k=\frac{(q;q)_m(q;q)_n(\alpha q;q)_{m+n-2k}(\alpha\beta;q)_{m-k}(\alpha\beta;q)_{n-k}(\alpha\beta;q)_k}{(\alpha q;q)_m(\alpha q;q)_n(\alpha\beta^2;q)_{m+n-2k}(q;q)_{m-k}(q;q)_{n-k}(q;q)_k}\frac{(\alpha\beta^2;q)_{m+n-k}(q^{k-m-n}/\alpha;q)_k\alpha^k(1-\alpha\beta q^{m+n-2k})}{(\alpha\beta q;q)_{m+n-k}(q^{k-m-n};q)_k(1-\alpha\beta)}W_{10}^{[k]}(q^{k-m-n-1};q^{k-m-n}/(\alpha\beta),q^{k-m-n}/(\alpha\beta),\alpha,\alpha\beta^2/q,q^{k-m},q^{k-n},q^{-k};q,q).
$$

代表来源：`GR2-8.Ex28`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-8.Ex28**（GR；Chapter 8, 8.Ex28, 印刷p255）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。C_{−1}^α=0,C_0^α=1；(z+z^{-1})C_n^α=(1−αq^{n+1})/(1−αβq^n) C_{n+1}^α+(1−αβ²q^{n−1})/(1−αβq^n) C_{n−1}^α；αβz≠0；当W提前终止按最小长度计算。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
