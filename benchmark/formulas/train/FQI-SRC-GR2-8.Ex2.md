# FQI-SRC-GR2-8.Ex2 · 大 q-Jacobi 的有限乘积公式

家族：A · 超几何型有限求和；难度：高；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
J_n(x)J_n(y)=(-aq)^nq^{\binom n2}\frac{(bq;q)_n}{(aq;q)_n}\sum_{m=0}^n\frac{(q^{-n},abq^{n+1},cq/x,cq/y;q)_m}{(q,bq,cq,cq;q)_m}(xy/a)^m{}_4\phi_3^{[m]}(q^{-m},b^{-1}q^{-m},x,y;aq,xq^{-m}/c,yq^{-m}/c;q,abq/c^2).
$$

代表来源：`GR2-8.Ex2`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-8.Ex2**（GR；Chapter 8, 8.Ex2, 印刷p245）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。J=J_n(·;a,b,c)，abcxy≠0。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
