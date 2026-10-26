# FQI-SRC-GR2-2.2.2 · Bailey 的有限序列双和展开

家族：G · 差分域／环、参数关系与生成函数；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\sum_{k=0}^n\frac{(b,c,q^{-n};q)_k}{(q,aq/b,aq/c;q)_k}A_k=\sum_{j=0}^n\frac{(aq/(bc),aq^j,q^{-n};q)_j}{(q,aq/b,aq/c;q)_j}(-1)^jq^{-j(j-1)/2}\sum_{i=0}^{n-j}\frac{(q^{j-n},aq^{2j};q)_i}{(q,aq^j;q)_i}q^{-ij}\left(\frac{bc}{aq}\right)^{i+j}A_{i+j}.
$$

代表来源：`GR2-2.2.2`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-2.2.2**（GR；Chapter 2, 2.2.2, 印刷p40）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。abc≠0；A₀,…,Aₙ为任意标量序列。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
