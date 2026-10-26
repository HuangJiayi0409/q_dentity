# FQI-SRC-AQ-2.38 · 连接系数递推

家族：G · 差分域／环、参数关系与生成函数；难度：中；集合：test。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
T(r,0)=1,\qquad T(r,N)=-\sum_{j=1}^{\lfloor N/2\rfloor}\begin{bmatrix}r+2j\\j\end{bmatrix}_q T(r+2j,N-2j)\quad(N\ge1).
$$

代表来源：`AQ-2.38`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **AQ-2.38**（ANDREWS-Q；印刷页 14；式 (2.38)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 r≥0。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_Q.md`
- `round1_source_collection/records/ANDREWS_Q_supplement.md`
