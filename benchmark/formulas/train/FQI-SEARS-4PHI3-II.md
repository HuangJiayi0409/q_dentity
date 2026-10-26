# FQI-SEARS-4PHI3-II · Sears 平衡 4φ3 第二形式

家族：A · 超几何型有限求和；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
{}_4\phi_3^{[n]}\!\left[\begin{matrix}q^{-n},a,b,c\\d,e,f\end{matrix};q,q\right]=\frac{(a,ef/(ab),ef/(ac);q)_n}{(e,f,ef/(abc);q)_n}{}_4\phi_3^{[n]}\!\left[\begin{matrix}q^{-n},e/a,f/a,ef/(abc)\\ef/(ab),ef/(ac),q^{1-n}/a\end{matrix};q,q\right]
$$

代表来源：`GR2-III-16`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-III-16**（GR；Appendix III, (III.16), 印刷p360）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。n 为非负整数；q 为非零且非单位根的复数；所有显示的分母非零。 a≠0。 b,c,e,f≠0；平衡条件 def=abc q^{1-n}。
  变量对应：代表式；保留本条来源域。
- **SILLS-1.104**（SILLS；印刷页 48；1.104）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0，abcde≠0。
  变量对应：GR 的 (a,b,c,d,e,f)=(Sills b,a,c,abc q^(1−n)/(de),d,e)；平衡条件 def=abc q^(1−n) 随代换保留。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/books/SILLS.md`
- `round1_source_collection/records/GR2_supplement.md`
- `round1_source_collection/records/SILLS_supplement.md`
