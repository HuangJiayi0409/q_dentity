# FQI-SCHUR-RR-FIRST · Schur 第一有限 Rogers–Ramanujan

家族：A · 超几何型有限求和；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\sum_{j=0}^{\lfloor n/2\rfloor}q^{j^2}\begin{bmatrix}n-j\\j\end{bmatrix}_q=\sum_{j=-n-1}^{n+1}(-1)^jq^{j(5j+1)/2}\begin{bmatrix}n\\\lfloor(n+5j+1)/2\rfloor\end{bmatrix}_q.
$$

代表来源：`SILLS-4.14`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **SILLS-4.14**（SILLS；印刷页 123；4.14）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0。
  变量对应：代表式；保留本条来源域。
- **AQ-8.36**（ANDREWS-Q；印刷页 79；式 (8.36)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 N≥1；F 的递推与初值见 (8.32)–(8.35)。
  变量对应：F_N(0)=D_N=Σ_j q^(j²)[N−j choose j]_q；n=N，Gaussian 对称将 floor((n−5j)/2) 换成 floor((n+5j+1)/2)。两边多余尾项均为0。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_Q.md`
- `round1_source_collection/books/SILLS.md`
- `round1_source_collection/records/ANDREWS_Q_supplement.md`
- `round1_source_collection/records/SILLS_supplement.md`
