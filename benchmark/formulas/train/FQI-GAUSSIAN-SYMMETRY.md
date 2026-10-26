# FQI-GAUSSIAN-SYMMETRY · Gaussian 对称性

家族：F · 有限乘积与局部代数关系；难度：低；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\begin{bmatrix}n\\k\end{bmatrix}_q=\begin{bmatrix}n\\n-k\end{bmatrix}_q.
$$

代表来源：`GR2-I-39`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-I-39**（GR；Appendix I, (I.39), 印刷p353）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。0≤k≤n。
  变量对应：代表式；保留本条来源域。
- **AP-3.3.2**（ANDREWS-P；p.35, Theorem 3.2, (3.3.2)）：0≤m≤n，均为整数；Gaussian 下指标越界为零。
  变量对应：m→k。
- **SILLS-1.49**（SILLS；印刷页 33；1.49）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0。
  变量对应：逐项相同。
- **KAC-CHEUNG-6.1**（KAC-CHEUNG；印刷页 17；6.1）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。n≥0，j∈Z。
  变量对应：j→k；越界采用普通 Gaussian 零延拓。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_P.md`
- `round1_source_collection/books/GR.md`
- `round1_source_collection/books/KAC_CHEUNG.md`
- `round1_source_collection/books/SILLS.md`
- `round1_source_collection/records/ANDREWS_P_supplement.md`
- `round1_source_collection/records/GR2_supplement.md`
- `round1_source_collection/records/KAC_CHEUNG_supplement.md`
- `round1_source_collection/records/SILLS_supplement.md`
