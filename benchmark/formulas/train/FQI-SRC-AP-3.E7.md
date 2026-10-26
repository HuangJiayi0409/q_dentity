# FQI-SRC-AP-3.E7 · Rogers–Szegő 线性化公式

家族：A · 超几何型有限求和；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
H_m(t;q)H_n(t;q)=\sum_{r=0}^{\min(m,n)}\begin{bmatrix}m\\r\end{bmatrix}_{q}\begin{bmatrix}n\\r\end{bmatrix}_{q}(q;q)_r t^r H_{m+n-2r}(t;q).
$$

代表来源：`AP-3.E7`。

局部定义：\(H_n(t;q)=\sum_{j=0}^n\begin{bmatrix}n\\j\end{bmatrix}_q t^j\)；n≥0。

来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **AP-3.E7**（ANDREWS-P；p.50, Example 7（题干起于 p.49））：m,n≥0 为整数。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_P.md`
- `round1_source_collection/records/ANDREWS_P_supplement.md`
