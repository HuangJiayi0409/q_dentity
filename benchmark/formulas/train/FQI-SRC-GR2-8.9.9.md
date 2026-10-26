# FQI-SRC-GR2-8.9.9 · 一般终止 6φ5 的有限平方展开

家族：A · 超几何型有限求和；难度：高；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
{}_6\phi_5^{[n]}(q^{-n},Aq^n,h^2,B,h^2z^2,h^2/z^2;h^2s,D,AB/D,-h^2s,-h^2;q,q)=\sum_{j=0}^n\frac{(q^{-n},Aq^n,h^2,A/D,D/B,h^2z^2,h^2/z^2;q)_j(-1)^jB^jq^{j(j+1)/2}}{(q,h^2s,-h^2s,-h^2,Aq^{j-1},D,AB/D;q)_j}\left[{}_4\phi_3^{[n-j]}(q^{j-n},Aq^{j+n},hs^jz,hs^j/z;h^2sq^j,-h^2sq^j,-h^2q^j;q,q)\right]^2.
$$

代表来源：`GR2-8.9.9`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-8.9.9**（GR；Chapter 8, 8.9.9, 印刷p239）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。A=h⁴，B=u²，s²=q，z≠0；原书q^a=A,q^b=B,e^{iθ}=z²。以乘法参数替代指数参数。D=q^c非零。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
