# FQI-POCHHAMMER-RESIDUES · 有限乘积按剩余类拆分

家族：F · 有限乘积与局部代数关系；难度：低；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
(a;q)_{mn}=\prod_{j=0}^{m-1}(aq^j;q^m)_n
$$

代表来源：`GR2-I-27`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-I-27**（GR；Appendix I, (I.27), 印刷p352）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。n 为非负整数；q 为非零且非单位根的复数；所有显示的分母非零。 m 为正整数（作者源码中的 k 在此改名 m）。
  变量对应：代表式；保留本条来源域。
- **SILLS-2.49**（SILLS；印刷页 65；(2.49)）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。d≥1，r≥0。
  变量对应：Q→q，d→m，r→n。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/books/SILLS.md`
- `round1_source_collection/records/GR2_supplement.md`
- `round1_source_collection/records/SILLS_supplement.md`
