# FQI-SRC-GR2-7.Ex41 · 小 q-Jacobi 的有限加法公式

家族：A · 超几何型有限求和；难度：高；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\ell_n(q^z;1,1)\ell_y(q^z;q^x,0)=\ell_n(q^{x+y};1,1)\ell_n(q^y;1,1)\ell_y(q^z;q^x,0)+\sum_{k=1}^n\frac{(q;q)_{x+y+k}(q;q)_{n+k}q^{k(k+y-n)}}{(q;q)_{x+y}(q;q)_{n-k}(q;q)_k^2}\ell_{n-k}(q^{x+y};q^k,q^k)\ell_{n-k}(q^y;q^k,q^k)\ell_{y+k}(q^z;q^x,0)+\sum_{k=1}^{\min(n,y)}\frac{(q;q)_y(q;q)_{n+k}q^{k(x+y-n+1)}}{(q;q)_{y-k}(q;q)_{n-k}(q;q)_k^2}\ell_{n-k}(q^{x+y-k};q^k,q^k)\ell_{n-k}(q^{y-k};q^k,q^k)\ell_{y-k}(q^z;q^x,0).
$$

代表来源：`GR2-7.Ex41`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-7.Ex41**（GR；Chapter 7, 7.Ex41, 印刷p210）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。x,y,z,n非负整数；ℓ_n(t;a,b)=2φ1^[n](q^{-n},abq^{n+1};aq;q,qt)。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
