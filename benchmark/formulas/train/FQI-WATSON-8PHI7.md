# FQI-WATSON-8PHI7 · Watson 终止 8φ7→4φ3

家族：A · 超几何型有限求和；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
W_8^{[n]}(a;b,c,d,e,q^{-n};q,a^2q^{n+2}/(bcde))=\frac{(aq,aq/(de);q)_n}{(aq/d,aq/e;q)_n}{}_4\phi_3^{[n]}\!\left[\begin{matrix}aq/(bc),d,e,q^{-n}\\aq/b,aq/c,deq^{-n}/a\end{matrix};q,q\right]
$$

代表来源：`GR2-III-18`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-III-18**（GR；Appendix III, (III.18), 印刷p360）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。n 为非负整数；q 为非零且非单位根的复数；所有显示的分母非零。 a≠0。 b,c,d,e≠0，a≠1。
  变量对应：代表式；保留本条来源域。
- **AQ-3.49**（ANDREWS-Q；印刷页 31；式 (3.49)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 N≥0；q,a,b,c,d,e≠0，a≠1（可取可去奇点极限）。
  变量对应：N→n；展开 W_8^[n] 与右侧 4φ3。
- **SILLS-1.98**（SILLS；印刷页 46；1.98）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0，abcde≠0。
  变量对应：展开左侧 W_8^[n]；右侧上参数可交换次序。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_Q.md`
- `round1_source_collection/books/GR.md`
- `round1_source_collection/books/SILLS.md`
- `round1_source_collection/records/ANDREWS_Q_supplement.md`
- `round1_source_collection/records/GR2_supplement.md`
- `round1_source_collection/records/SILLS_supplement.md`
