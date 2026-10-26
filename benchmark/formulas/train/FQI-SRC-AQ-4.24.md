# FQI-SRC-AQ-4.24 · q-Dixon 三个 Gaussian 的交错求和

家族：A · 超几何型有限求和；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\sum_{k=-\min(a,b,c)}^{\min(a,b,c)}(-1)^kq^{k(3k+1)/2}\begin{bmatrix}b+c\\c+k\end{bmatrix}_q\begin{bmatrix}c+a\\a+k\end{bmatrix}_q\begin{bmatrix}a+b\\b+k\end{bmatrix}_q=\frac{(q;q)_{a+b+c}}{(q;q)_a(q;q)_b(q;q)_c}.
$$

代表来源：`AQ-4.24`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **AQ-4.24**（ANDREWS-Q；印刷页 38；式 (4.24)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 a,b,c≥0。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_Q.md`
- `round1_source_collection/records/ANDREWS_Q_supplement.md`
