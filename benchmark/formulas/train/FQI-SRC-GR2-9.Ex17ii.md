# FQI-SRC-GR2-9.Ex17ii · 连续 q-Jacobi 的有限连接公式（归一化核正）

家族：A · 超几何型有限求和；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\mathscr J_m(z;A,B)=\sum_{n=0}^mg(n,m)\mathscr J_n(z;U,V),\quad g(n,m)=\frac{(Aq,-Bq;q)_m(UVq,-q;q)_n(ABq^{m+1};q)_nq^{n(n-m)}}{(-q;q)_m(UVq;q)_{2n}(q;q)_{m-n}(Aq,-Bq;q)_n}{}_4\phi_3^{[m-n]}(q^{n-m},ABq^{n+m+1},Uq^{n+1},-Vq^{n+1};UVq^{2n+2},Aq^{n+1},-Bq^{n+1};q,q).
$$

代表来源：`GR2-9.Ex17ii`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-9.Ex17ii**（GR；Chapter 9, 9.Ex17ii, 印刷p277）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。A=q^a,B=q^b,U=q^α,V=q^β；𝒥_j(z;A,B)=(Aq,−Bq;q)j/(q,−q;q)j ·4φ3^[j](q^{-j},ABq^{j+1},sz,s/z;Aq,−Bq,−q;q,q)，s²=q。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
