# FQI-GAUSS-ALTERNATING · Gauss 交错 Gaussian 奇偶求值

家族：A · 超几何型有限求和；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\sum_{j=0}^m(-1)^j\begin{bmatrix}m\\j\end{bmatrix}_{q}=\begin{cases}(q;q^2)_{m/2},&m\text{ even},\\0,&m\text{ odd}.\end{cases}
$$

代表来源：`AP-3.3.8`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **AP-3.3.8**（ANDREWS-P；p.37, Theorem 3.4, (3.3.8)）：m≥0 为整数。
  变量对应：代表式；保留本条来源域。
- **FINE-20.67**（FINE；印刷页 28；式 (20.67)；A general transformation）：q 为形式变量；数值代入要求所有实际分母非零，Gaussian 在奇点先作多项式延拓。空乘积为 1、空和为 0。n≥0 为整数。
  变量对应：展开 f_N(−1)=Σ_j(−1)^j[N choose j]_q；按 N=2n、2n+1 分支。
- **KAC-CHEUNG-7.14-15**（KAC-CHEUNG；印刷页 26；7.14-15）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。m≥0。
  变量对应：代表指标 m→n；两条奇偶分支相同。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_P.md`
- `round1_source_collection/books/FINE.md`
- `round1_source_collection/books/KAC_CHEUNG.md`
- `round1_source_collection/records/ANDREWS_P_supplement.md`
- `round1_source_collection/records/FINE_supplement.md`
- `round1_source_collection/records/KAC_CHEUNG_supplement.md`
