# FQI-SRC-GR2-7.6.8 · Askey–Wilson 单参数连接系数求值

家族：A · 超几何型有限求和；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
P_n(z;\alpha,b,c,d)=\sum_{k=0}^n\frac{(\alpha/a;q)_{n-k}(\alpha bcdq^{n-1};q)_k(q,bc,bd,cd;q)_na^{n-k}}{(q,bc,bd,cd;q)_k(abcdq^{k-1};q)_k(q,abcdq^{2k};q)_{n-k}}P_k(z;a,b,c,d).
$$

代表来源：`GR2-7.6.8`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-7.6.8**（GR；Chapter 7, 7.6.8, 印刷p196）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。P见7.5.3；aα≠0。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
