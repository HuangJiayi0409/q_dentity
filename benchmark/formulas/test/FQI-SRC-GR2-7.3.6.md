# FQI-SRC-GR2-7.3.6 · 小 q-Jacobi 三项递推

家族：C · 递推与差分关系；难度：中；集合：test。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
x\ell_n(x)=A_n(\ell_{n+1}(x)-\ell_n(x))-C_n(\ell_n(x)-\ell_{n-1}(x)),\quad A_n=-\frac{q^n(1-abq^{n+1})(1-aq^{n+1})}{(1-abq^{2n+1})(1-abq^{2n+2})},\quad C_n=-\frac{aq^n(1-q^n)(1-bq^n)}{(1-abq^{2n})(1-abq^{2n+1})}.
$$

代表来源：`GR2-7.3.6`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-7.3.6**（GR；Chapter 7, 7.3.6, 印刷p182）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。ℓ_n(x)=2φ1^[n](q^{-n},abq^{n+1};aq;q,qx)，ℓ_{−1}=0。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
