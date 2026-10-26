# FQI-SRC-GR2-2.8.2 · Bailey 有限支持序列展开

家族：G · 差分域／环、参数关系与生成函数；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\sum_{k=0}^N\frac{(a,b,c;q)_k}{(q,aq/b,aq/c;q)_k}A_k=\sum_{j=0}^N\frac{(\lambda;q)_j(1-\lambda q^{2j})(\lambda b/a,\lambda c/a,aq/(bc);q)_j(a;q)_{2j}}{(q;q)_j(1-\lambda)(aq/b,aq/c,qa^2/(\lambda bc);q)_j(\lambda q;q)_{2j}}\left(\frac a\lambda\right)^j\sum_{k=0}^{N-j}\frac{(aq^{2j},a/\lambda,\lambda bcq^j/a;q)_k}{(q,\lambda q^{2j+1},a^2q^{j+1}/(\lambda bc);q)_k}A_{j+k}.
$$

代表来源：`GR2-2.8.2`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-2.8.2**（GR；Chapter 2, 2.8.2, 印刷p45）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。N≥0，abcλ≠0，λ≠1；A_k=0对k>N。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
