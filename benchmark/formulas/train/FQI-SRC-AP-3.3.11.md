# FQI-SRC-AP-3.3.11 · 三 Gaussian 的 q-Saalschütz 求和

家族：A · 超几何型有限求和；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\sum_{r=0}^{\min(M-m,N)}\begin{bmatrix}M-m\\r\end{bmatrix}_{q}\begin{bmatrix}N+m\\m+r\end{bmatrix}_{q}\begin{bmatrix}m+n+r\\M+N\end{bmatrix}_{q}q^{(N-r)(M-r-m)}=\begin{bmatrix}m+n\\M\end{bmatrix}_{q}\begin{bmatrix}n\\N\end{bmatrix}_{q}.
$$

代表来源：`AP-3.3.11`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **AP-3.3.11**（ANDREWS-P；p.37, Theorem 3.4, (3.3.11)）：m,n,M,N≥0，M≥m，均为整数；Gaussian 下指标越界为零。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_P.md`
- `round1_source_collection/records/ANDREWS_P_supplement.md`
