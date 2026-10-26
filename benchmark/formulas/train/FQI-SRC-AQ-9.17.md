# FQI-SRC-AQ-9.17 · G 多项式的有限系数展开（显式修订移位）

家族：A · 超几何型有限求和；难度：高；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
G_N(0;q)=\sum_{\substack{n,j\ge0\\3n+2j\le N+1}}q^{n(3n-1)/2+j}\begin{bmatrix}n+N+1-3n-2j\\n\end{bmatrix}_q\begin{bmatrix}n+j-1\\j\end{bmatrix}_{q^2}.
$$

代表来源：`AQ-9.17`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **AQ-9.17**（ANDREWS-Q；印刷页 90；式 (9.17)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 N≥0；n=0 时第二 Gaussian 按 δ_{j,0} 解释。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_Q.md`
- `round1_source_collection/records/ANDREWS_Q_supplement.md`
