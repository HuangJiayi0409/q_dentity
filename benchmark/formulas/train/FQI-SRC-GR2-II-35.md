# FQI-SRC-GR2-II-35 · Gosper 双底数求和扩展

家族：A · 超几何型有限求和；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\sum_{k=0}^n\frac{(1-ap^kq^k)(1-bp^kq^{-k})}{(1-a)(1-b)}\frac{(a,b;p)_k(c,a/(bc);q)_k}{(q,aq/b;q)_k(ap/c,bcp;p)_k}q^k=\frac{(ap,bp;p)_n(cq,aq/(bc);q)_n}{(q,aq/b;q)_n(ap/c,bcp;p)_n}.
$$

代表来源：`GR2-II-35`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-II-35**（GR；Appendix II, (II.35), 印刷p358）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。abc≠0，a,b≠1；p也是非零非单位根底数。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
