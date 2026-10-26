# FQI-SRC-GR2-8.Ex4ii · q-Hahn 乘积的有限三重和

家族：A · 超几何型有限求和；难度：高；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
Q_n(x)Q_n(y)=\frac{(bq,abq^{N+2};q)_n(bq^{N+1})^{-n}}{(aq,q^{-N};q)_n}\sum_{m=0}^n\frac{(q^{-n},abq^{n+1},bq^{N+1-x-y};q)_mq^{(x+1)m}}{(q,bq,abq^{N+2};q)_m}\sum_{k=0}^{\min(m,x,y)}\frac{(q^{-m},abq^{m+1},q^{-x},q^{-y};q)_k(bq^{N-x+2})^k}{(q,aq,q^{-N},bq^{N+1-x-y};q)_k}{}_3\phi_2^{[\min(m-k,x-k)]}(q^{k-m},q^{k-x},bq^{N+1-x};0,bq^{N+1-x-y+k};q,q).
$$

代表来源：`GR2-8.Ex4ii`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-8.Ex4ii**（GR；Chapter 8, 8.Ex4ii, 印刷p246）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。0≤n,x,y≤N；Q=Q_n(·;a,b,N)，ab≠0。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
