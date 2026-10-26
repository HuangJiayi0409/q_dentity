# FQI-POCHHAMMER-NEGATIVE · 负整数长度 q-Pochhammer

家族：F · 有限乘积与局部代数关系；难度：低；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
(a;q)_{-n}=\frac1{(aq^{-n};q)_n}=\frac{(-q/a)^nq^{n(n-1)/2}}{(q/a;q)_n}.
$$

代表来源：`GR2-I-02`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-I-02**（GR；Appendix I, (I.2), 印刷p351）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。a≠0。
  变量对应：代表式；保留本条来源域。
- **FINE-18.11**（FINE；印刷页 19；式 (18.11)）：q 为形式变量；数值代入要求所有实际分母非零，Gaussian 在奇点先作多项式延拓。空乘积为 1、空和为 0。n≥0，a,q≠0；所有倒数分母非零。
  变量对应：GR 的 a=Fine 的 aq；(−aq)^−n q^{n(n+1)/2}=(−1/a)^n q^{n(n−1)/2}。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/FINE.md`
- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/FINE_supplement.md`
- `round1_source_collection/records/GR2_supplement.md`
