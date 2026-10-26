# FQI-SRC-AP-13.E3 · 三变量 q-下降乘积卷积

家族：A · 超几何型有限求和；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\prod_{i=0}^{n-1}(X-Zq^i)=\sum_{k=0}^n \begin{bmatrix}n\\k\end{bmatrix}_{q}\prod_{j=0}^{k-1}(Y-Zq^j)\prod_{h=0}^{n-k-1}(X-Yq^h).
$$

代表来源：`AP-13.E3`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **AP-13.E3**（ANDREWS-P；p.225, Example 3）：n≥0 为整数；X,Y,Z,q 为形式变量。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_P.md`
- `round1_source_collection/records/ANDREWS_P_supplement.md`
