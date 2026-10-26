# FQI-SCHUR-EVEN-RECIPROCAL · Schur D 偶指标倒数的两种展开

家族：A · 超几何型有限求和；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
q^{m^2}D_{2m}(q^{-1})=\sum_{j=0}^mq^{j^2}\begin{bmatrix}m+j\\2j\end{bmatrix}_q=\sum_{k=-m-2}^{m+2}\left(q^{15k^2-k}\begin{bmatrix}2m\\m+5k\end{bmatrix}_q-q^{15k^2-11k+2}\begin{bmatrix}2m\\m+5k-2\end{bmatrix}_q\right).
$$

代表来源：`SILLS-4.23`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **SILLS-4.23**（SILLS；印刷页 125；4.23）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。m≥0。
  变量对应：代表式；保留本条来源域。
- **AQ-REF-8.42**（ANDREWS-Q；印刷页 80；式 (8.42)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 N≥0；F₀(0)=1 为与原递推相容的延拓。
  变量对应：N→m；F_(2N)(0)=D_(2N)；双边和 k→−k，再用 Gaussian 对称，得到两项指数 15k²−k、15k²−11k+2。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_Q.md`
- `round1_source_collection/books/SILLS.md`
- `round1_source_collection/records/ANDREWS_Q_supplement.md`
- `round1_source_collection/records/SILLS_supplement.md`
