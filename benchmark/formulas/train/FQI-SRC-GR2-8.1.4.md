# FQI-SRC-GR2-8.1.4 · 任意序列的有限乘积展开

家族：G · 差分域／环、参数关系与生成函数；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\left[\sum_{j=0}^n\frac{(q^{-n},aq^n;q)_jB_j}{(q,b;q)_j}\right]\left[\sum_{k=0}^n\frac{(q^{-n},aq^n;q)_kC_k}{(q,c;q)_k}\right]=\sum_{m=0}^n(q^{-n},aq^n;q)_m\sum_{k=0}^m\frac{C_kq^{k^2-mk}}{(q,c;q)_k(q,b;q)_{m-k}}\sum_{j=0}^k\frac{(q^{-k},aq^m;q)_jB_{m-k+j}}{(q,bq^{m-k};q)_j}.
$$

代表来源：`GR2-8.1.4`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-8.1.4**（GR；Chapter 8, 8.1.4, 印刷p218）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。B_0…B_n,C_0…C_n任意。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
