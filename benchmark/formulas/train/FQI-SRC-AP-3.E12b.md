# FQI-SRC-AP-3.E12b · Schur 多项式累加恒等式

家族：A · 超几何型有限求和；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
D_n(q)=1+\sum_{j=1}^n q^jD_{j-2}(q).
$$

代表来源：`AP-3.E12b`。

局部定义：\(D_n(q)=\sum_{j=0}^{\lfloor(n+1)/2\rfloor}q^{j^2}\begin{bmatrix}n+1-j\\j\end{bmatrix}_q\)（n≥0）；为解释原习题端点，补充 D_{-1}=1。

来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **AP-3.E12b**（ANDREWS-P；p.50, Example 12，第二式）：n≥0 为整数；D_{−1}=1。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_P.md`
- `round1_source_collection/records/ANDREWS_P_supplement.md`
