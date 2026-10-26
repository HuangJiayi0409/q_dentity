# FQI-SCHUR-RR-BUNDLE · Schur 两支有限 Rogers–Ramanujan

家族：A · 超几何型有限求和；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\sum_{j=0}^{\lfloor(n+1-a)/2\rfloor}q^{j^2+aj}\begin{bmatrix}n+1-a-j\\j\end{bmatrix}_{q}=\sum_{h=-n-2}^{n+2}(-1)^hq^{h(5h+1)/2-2ah}\begin{bmatrix}n+1\\\lfloor(n+1-5h)/2\rfloor+a\end{bmatrix}_{q}.
$$

代表来源：`AP-3.E10`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **AP-3.E10**（ANDREWS-P；p.50, Example 10）：n≥0 为整数；a∈{0,1}；Gaussian 下指标越界为零。
  变量对应：代表式；保留本条来源域。
- **AP-9.E4a**（ANDREWS-P；p.157, Example 4，第一式）：n≥0 为整数；a∈{0,1}；Gaussian 下指标越界为零。
  变量对应：公式、定义与条件逐字相同；仅书内定位不同。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_P.md`
- `round1_source_collection/records/ANDREWS_P_supplement.md`
