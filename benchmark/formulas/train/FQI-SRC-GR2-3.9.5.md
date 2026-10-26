# FQI-SRC-GR2-3.9.5 · 终止多底数级数的有限展开

家族：A · 超几何型有限求和；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\sum_{k=0}^N\frac{(a,b,c;q)_k}{(q,aq/b,aq/c;q)_k}H_kz^k=\sum_{j=0}^N\frac{(aq/(bc);q)_j(a;q)_{2j}}{(q,aq/b,aq/c;q)_j}\left(-\frac{bcz}{aq}\right)^jq^{-j(j-1)/2}\sum_{k=0}^{N-j}\frac{(aq^{2j};q)_k}{(q;q)_k}H_{j+k}\left(\frac{bcz}{aq^{j+1}}\right)^k,\quad H_k=\prod_{i=1}^m\frac{(\boldsymbol c_i;q_i)_k}{(\boldsymbol d_i;q_i)_k}\left((-1)^kq_i^{k(k-1)/2}\right)^{s_i-r_i}.
$$

代表来源：`GR2-3.9.5`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-3.9.5**（GR；Chapter 3, 3.9.5, 印刷p95）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。各向量c_i长r_i，d_i长s_i；至少一上参数c_{i,j}=q_i^{-N}；abc≠0。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
