# FQI-GAUSSIAN-VANDERMONDE · Gaussian q-Vandermonde 卷积

家族：A · 超几何型有限求和；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\sum_{k=\max(0,h-m)}^{\min(h,n)} \begin{bmatrix}n\\k\end{bmatrix}_{q}\begin{bmatrix}m\\h-k\end{bmatrix}_{q}q^{(n-k)(h-k)}=\begin{bmatrix}m+n\\h\end{bmatrix}_{q}.
$$

代表来源：`AP-3.3.10`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **AP-3.3.10**（ANDREWS-P；p.37, Theorem 3.4, (3.3.10)）：m,n≥0，0≤h≤m+n，均为整数。
  变量对应：代表式；保留本条来源域。
- **KAC-CHEUNG-7.6**（KAC-CHEUNG；印刷页 23；7.6）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。m,n≥0，0≤k≤m+n；Gaussian越界为0。
  变量对应：原 (m,n,k,j)→(n,m,h,k)，零支撑将 j=0..h 缩至有效区间。
- **AP-13.E6**（ANDREWS-P；p.225, Example 6）：m,n≥0，0≤h≤m+n，均为整数。
  变量对应：在代表式中换 (n,m,k)→(m,n,h−k)；指数成为 k(m−h+k)，因子交换。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_P.md`
- `round1_source_collection/books/KAC_CHEUNG.md`
- `round1_source_collection/records/ANDREWS_P_supplement.md`
- `round1_source_collection/records/KAC_CHEUNG_supplement.md`
