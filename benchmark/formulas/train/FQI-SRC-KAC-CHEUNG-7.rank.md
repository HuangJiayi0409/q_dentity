# FQI-SRC-KAC-CHEUNG-7.rank · 有限域定秩矩阵计数

家族：C · 递推与差分关系；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\#\{A\in\mathbb F_q^{m\times n}:\operatorname{rank}A=j\}=\begin{bmatrix}n\\j\end{bmatrix}_q\begin{bmatrix}m\\j\end{bmatrix}_q\prod_{i=0}^{j-1}(q^j-q^i)=\begin{bmatrix}n\\j\end{bmatrix}_q\prod_{i=0}^{j-1}(q^m-q^i).
$$

代表来源：`KAC-CHEUNG-7.rank`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **KAC-CHEUNG-7.rank**（KAC-CHEUNG；印刷页 25；7.rank）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。q为素数幂；0≤j≤min(m,n)。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/KAC_CHEUNG.md`
- `round1_source_collection/records/KAC_CHEUNG_supplement.md`
