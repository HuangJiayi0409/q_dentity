# FQI-SRC-GR2-II-36 · 有限双边双底数求和

家族：A · 超几何型有限求和；难度：中；集合：test。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\sum_{k=-m}^n\frac{(1-adp^kq^k)(1-bp^k/(dq^k))}{(1-ad)(1-b/d)}\frac{(a,b;p)_k(c,ad^2/(bc);q)_k}{(dq,adq/b;q)_k(adp/c,bcp/d;p)_k}q^k=\frac{(1-a)(1-b)(1-c)(1-ad^2/(bc))}{d(1-ad)(1-b/d)(1-c/d)(1-ad/(bc))}\left[\frac{(ap,bp;p)_n(cq,ad^2q/(bc);q)_n}{(dq,adq/b;q)_n(adp/c,bcp/d;p)_n}-\frac{(c/(ad),d/(bc);p)_{m+1}(1/d,b/(ad);q)_{m+1}}{(1/c,bc/(ad^2);q)_{m+1}(1/a,1/b;p)_{m+1}}\right].
$$

代表来源：`GR2-II-36`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-II-36**（GR；Appendix II, (II.36), 印刷p358）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。m≥0，abcd≠0；p也是非零非单位根底数；负指标按有限倒积。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
