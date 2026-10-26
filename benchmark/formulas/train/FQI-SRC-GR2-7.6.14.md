# FQI-SRC-GR2-7.6.14 · Rogers 连续 q-超球连接公式

家族：A · 超几何型有限求和；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
C_n(z;\gamma)=\sum_{k=0}^{\lfloor n/2\rfloor}\frac{\beta^k(\gamma/\beta;q)_k(\gamma;q)_{n-k}(1-\beta q^{n-2k})}{(q;q)_k(\beta q;q)_{n-k}(1-\beta)}C_{n-2k}(z;\beta).
$$

代表来源：`GR2-7.6.14`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-7.6.14**（GR；Chapter 7, 7.6.14, 印刷p197）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。C见7.4.14；β≠0,1。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
