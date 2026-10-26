# FQI-SRC-GR2-1.Ex33 · 小 q-Jacobi 多项式的有限连接公式

家族：A · 超几何型有限求和；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
p_n(x;c,d;q)=\sum_{k=0}^n A_{k,n}p_k(x;a,b;q),\quad A_{k,n}=\frac{(-1)^kq^{k(k+1)/2}(q^{-n},aq,cdq^{n+1};q)_k}{(q,cq,abq^{k+1};q)_k}{}_3\phi_2^{[n-k]}\!\left[\begin{matrix}q^{k-n},cdq^{n+k+1},aq^{k+1}\\cq^{k+1},abq^{2k+2}\end{matrix};q,q\right].
$$

代表来源：`GR2-1.Ex33`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-1.Ex33**（GR；Chapter 1, 1.Ex33, 印刷p33）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。p_n(x;a,b;q)={}_2φ₁^{[n]}(q^{-n},abq^{n+1};aq;q,qx)。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
