# FQI-SRC-GR2-III-21 · Singh 有限二次变换

家族：A · 超几何型有限求和；难度：高；集合：test。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\sum_{k=0}^L\frac{(A,B,c,d;q)_kq^k}{(q,-cd;q)_k(ABq;q^2)_k}=\sum_{k=0}^R\frac{(A,B,c^2,d^2;q^2)_kq^{2k}}{(q^2,ABq,-cd,-cdq;q^2)_k}.
$$

代表来源：`GR2-III-21`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-III-21**（GR；Appendix III, (III.21), 印刷p361）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。两侧均终止；例如c=q^{-n}时L=R=n，或A=q^{-2n}时L=2n、R=n。参数互换同理，提前终止时取各侧最小长度。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
