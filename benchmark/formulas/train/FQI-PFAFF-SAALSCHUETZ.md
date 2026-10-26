# FQI-PFAFF-SAALSCHUETZ · 终止 q-Pfaff–Saalschütz

家族：A · 超几何型有限求和；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
{}_3\phi_2^{[n]}\!\left[\begin{matrix}a,b,q^{-n}\\c,abq^{1-n}/c\end{matrix};q,q\right]=\frac{(c/a,c/b;q)_n}{(c,c/(ab);q)_n}
$$

代表来源：`GR2-II-12`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-II-12**（GR；Appendix II, (II.12), 印刷p355）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。n 为非负整数；q 为非零且非单位根的复数；所有显示的分母非零。 a≠0。 b,c≠0。
  变量对应：代表式；保留本条来源域。
- **AP-3.3.12**（ANDREWS-P；p.38, (3.3.12)）：N≥0 为整数；a,b,c,q 非零，所有所列分母非零；或在有理函数域中解释。
  变量对应：N→n；合并多参数 Pochhammer 后正是有限 3φ2 定义。
- **AQ-3.25**（ANDREWS-Q；印刷页 25；式 (3.25)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 N≥0，q,a,b,c≠0。
  变量对应：N→n；展开有限 3φ2。
- **SILLS-1.Thm1.49**（SILLS；印刷页 32；1.Thm1.49）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0，abc≠0。
  变量对应：补显式截断上限 n。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_P.md`
- `round1_source_collection/books/ANDREWS_Q.md`
- `round1_source_collection/books/GR.md`
- `round1_source_collection/books/SILLS.md`
- `round1_source_collection/records/ANDREWS_P_supplement.md`
- `round1_source_collection/records/ANDREWS_Q_supplement.md`
- `round1_source_collection/records/GR2_supplement.md`
- `round1_source_collection/records/SILLS_supplement.md`
