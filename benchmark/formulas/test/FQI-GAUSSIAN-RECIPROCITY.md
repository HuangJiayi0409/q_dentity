# FQI-GAUSSIAN-RECIPROCITY · 普通 Gaussian 倒底数

家族：F · 有限乘积与局部代数关系；难度：低；集合：test。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\begin{bmatrix}n\\k\end{bmatrix}_{1/q}=q^{k(k-n)}\begin{bmatrix}n\\k\end{bmatrix}_q.
$$

代表来源：`SILLS-1.53`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **SILLS-1.53**（SILLS；印刷页 34；1.53）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0，0≤k≤n。
  变量对应：代表式；保留本条来源域。
- **KAC-CHEUNG-6.reciprocity**（KAC-CHEUNG；印刷页 19；6.reciprocity）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。n≥0，0≤j≤n。
  变量对应：j→k；−j(n−j)=j(j−n)。
- **AP-3.5.RECIP**（ANDREWS-P；p.47, Theorem 3.10 证明，跨 pp.47–48）：N,M≥0 为整数；在 Laurent 多项式环中写出，整理后为多项式等式。
  变量对应：展开 G(N,M;q)=[N+M choose M]_q，n=N+M，k=M；NM=k(n−k)。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_P.md`
- `round1_source_collection/books/KAC_CHEUNG.md`
- `round1_source_collection/books/SILLS.md`
- `round1_source_collection/records/ANDREWS_P_supplement.md`
- `round1_source_collection/records/KAC_CHEUNG_supplement.md`
- `round1_source_collection/records/SILLS_supplement.md`
