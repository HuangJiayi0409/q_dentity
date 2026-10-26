# FQI-SRC-GR2-8.Ex24 · 连续 q-Jacobi 特例的有限线性化

家族：A · 超几何型有限求和；难度：高；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
r_n(z)r_{n-m}(z)=\sum_{k=0}^{2(n-m)}c_kr_{m+k}(z),\quad c_k=\frac{(ab;q)_{2m}(ab;q)_{2n-2m}(q,-as,bs,-ab;q)_n}{(abq;q)_{2n}(q,-as,bs,-ab;q)_m(-q,as,-bs,ab;q)_{n-m}}\frac{(1-abq^{2m+2k})(abq^{2m},-q^{m+1},-bsq^m,a/b,a^2b^2q^{2n},q^{2m-2n};q)_kq^{n-m}s^ka^{-k}}{(1-ab)(q,-abq^m,-asq^m,b^2q^{2m+1},q^{2m-2n+1}/(ab),abq^{2n+1};q)_k}W_{10}^{[\lfloor k/2\rfloor]}(b^2q^{2m};b^2,b^2q^{2n+1},q^{2m-2n+1}/a^2,abq^{2m+k},abq^{2m+k+1},q^{1-k},q^{-k};q^2,q^2),\quad s^2=q.
$$

代表来源：`GR2-8.Ex24`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-8.Ex24**（GR；Chapter 8, 8.Ex24, 印刷p253）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。0≤m≤n；r_j(z)=4φ3^[j](q^{-j},abq^j,sz,s/z;as,−bs,−q;q,q)，abz≠0。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
