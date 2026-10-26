# FQI-SRC-GR2-2.2.4 · 终止基本超几何级数的降阶展开

家族：A · 超几何型有限求和；难度：中；集合：test。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
{}_{r+4}\phi_{r+3}^{[n]}(a,b,c,\boldsymbol u,q^{-n};aq/b,aq/c,\boldsymbol v;q,z)=\sum_{j=0}^n\frac{(aq/(bc),\boldsymbol u,q^{-n};q)_j(a;q)_{2j}}{(q,aq/b,aq/c,\boldsymbol v;q)_j}\left(-\frac{bcz}{aq}\right)^jq^{-j(j-1)/2}{}_{r+2}\phi_{r+1}^{[n-j]}(aq^{2j},q^j\boldsymbol u,q^{j-n};q^j\boldsymbol v;q,bcz/(aq^{j+1})).
$$

代表来源：`GR2-2.2.4`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-2.2.4**（GR；Chapter 2, 2.2.4, 印刷p41）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。r≥0；u长度r，v长度r+1；abc≠0。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
