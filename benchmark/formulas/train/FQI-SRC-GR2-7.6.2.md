# FQI-SRC-GR2-7.6.2 · Askey–Wilson 有限连接公式

家族：A · 超几何型有限求和；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
P_n(z;\alpha,\beta,\gamma,d)=\sum_{k=0}^nc_{k,n}P_k(z;a,b,c,d),\quad c_{k,n}=\frac{(\alpha d,\beta d,\gamma d,q;q)_n(\alpha\beta\gamma dq^{n-1};q)_kq^{k^2-nk}d^{k-n}}{(\alpha d,\beta d,\gamma d,q,abcdq^{k-1};q)_k(q;q)_{n-k}}{}_5\phi_4^{[n-k]}(q^{k-n},\alpha\beta\gamma dq^{n+k-1},adq^k,bdq^k,cdq^k;abcdq^{2k},\alpha dq^k,\beta dq^k,\gamma dq^k;q,q).
$$

代表来源：`GR2-7.6.2`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-7.6.2**（GR；Chapter 7, 7.6.2, 印刷p195）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。P见7.5.3；αad≠0。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
