# FQI-SRC-GR2-2.Ex28 · 良配终止级数的有限展开

家族：A · 超几何型有限求和；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
{}_{r+3}\phi_{r+2}^{[n]}(a,\boldsymbol b,c,q^{-n};aq/\boldsymbol b,aq/c,aq^{n+1};q,qz)=\frac{(aq/(cz),q^{1-n}/c;q)_n}{(aq/c,q^{1-n}/(cz);q)_n}\sum_{k=0}^n\frac{(q^{-n}/(cz),1/z,q^{-n}/a,q^{-n};q)_k(1-q^{2k-n}/(cz))}{(q,aq/(cz),q/(cz),q^{1-n}/c;q)_k(1-q^{-n}/(cz))}\left(\frac{aq^{n+1}}c\right)^k{}_{r+3}\phi_{r+2}^{[n-k]}(a,\boldsymbol b,czq^{-k},q^{k-n};aq/\boldsymbol b,aq^{k+1}/(cz),aq^{n+1-k};q,q).
$$

代表来源：`GR2-2.Ex28`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-2.Ex28**（GR；Chapter 2, 2.Ex28, 印刷p64）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。r≥0，b向量长r，acz及各b_i非零。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
