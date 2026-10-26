# FQI-PASCAL-Q-K · Gaussian Pascal：权 q^k

家族：F · 有限乘积与局部代数关系；难度：低；集合：test。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\begin{bmatrix}n\\k\end{bmatrix}_q=q^k\begin{bmatrix}n-1\\k\end{bmatrix}_q+\begin{bmatrix}n-1\\k-1\end{bmatrix}_q.
$$

代表来源：`SILLS-1.51`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **SILLS-1.51**（SILLS；印刷页 33；1.51）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥1，0≤k≤n。
  变量对应：代表式；保留本条来源域。
- **AP-3.3.4**（ANDREWS-P；p.35, Theorem 3.2, (3.3.4)）：n≥1，0≤m≤n，均为整数；Gaussian 下指标越界为零。
  变量对应：m→k，交换右侧两项次序。
- **AQ-3.9**（ANDREWS-Q；印刷页 22；式 (3.9)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 A≥1，0≤B≤A。
  变量对应：A→n，B→k，交换右侧两项次序。
- **KAC-CHEUNG-6.2**（KAC-CHEUNG；印刷页 17；6.2）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。n≥1，0≤j≤n。
  变量对应：j→k；注意本书称第一递推。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_P.md`
- `round1_source_collection/books/ANDREWS_Q.md`
- `round1_source_collection/books/KAC_CHEUNG.md`
- `round1_source_collection/books/SILLS.md`
- `round1_source_collection/records/ANDREWS_P_supplement.md`
- `round1_source_collection/records/ANDREWS_Q_supplement.md`
- `round1_source_collection/records/KAC_CHEUNG_supplement.md`
- `round1_source_collection/records/SILLS_supplement.md`
