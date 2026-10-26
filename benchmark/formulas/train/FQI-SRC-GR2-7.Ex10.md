# FQI-SRC-GR2-7.Ex10 · 大 q-Jacobi 三项递推

家族：C · 递推与差分关系；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
(x-1)J_n(x)=A_n(J_{n+1}(x)-J_n(x))+C_n(J_n(x)-J_{n-1}(x)),\quad A_n=\frac{(1-aq^{n+1})(1-cq^{n+1})(1-abq^{n+1})}{(1-abq^{2n+1})(1-abq^{2n+2})},\quad C_n=\frac{acq^{n+1}(1-q^n)(1-bq^n)(1-abq^n/c)}{(1-abq^{2n})(1-abq^{2n+1})}.
$$

代表来源：`GR2-7.Ex10`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-7.Ex10**（GR；Chapter 7, 7.Ex10, 印刷p202）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。J_n(x)=3φ2^[n](q^{-n},abq^{n+1},x;aq,cq;q,q)，c≠0，J_{−1}=0。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
