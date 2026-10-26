# FQI-SRC-GR2-8.9.5 · 终止 6φ5 的奇偶平方和

家族：A · 超几何型有限求和；难度：高；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
{}_6\phi_5^{[n]}(q^{-n},Aq^n,B,-B,h^2z^2,h^2/z^2;B^2,h^2s,-h^2s,-h^2,-h^2;q,q)=\sum_{k=0}^{\lfloor n/2\rfloor}\frac{(q^{-n},Aq^n,h^2,h^2z^2,h^2/z^2;q)_{2k}(q,A/B^2;q^2)_kq^{2k^2+k}B^{2k}}{(q,h^2s,-h^2s,-h^2,Aq^{2k-1};q)_{2k}(A,B^2q;q^2)_k}\left[{}_4\phi_3^{[n-2k]}(q^{2k-n},Aq^{n+2k},hq^kz,hq^k/z;h^2sq^{2k},-h^2sq^{2k},-h^2q^{2k};q,q)\right]^2.
$$

代表来源：`GR2-8.9.5`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-8.9.5**（GR；Chapter 8, 8.9.5, 印刷p238）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。A=h⁴，B=u²，s²=q，z≠0；原书q^a=A,q^b=B,e^{iθ}=z²。以乘法参数替代指数参数。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
