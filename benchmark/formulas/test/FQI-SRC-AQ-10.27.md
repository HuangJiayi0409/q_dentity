# FQI-SRC-AQ-10.27 · Göllnitz 递推算子的相容关系

家族：C · 递推与差分关系；难度：中；集合：test。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\begin{aligned}\mathcal F(n-1,tq^6;G_n,G_{n-1},G_{n-2},G_{n-3},G_{n-4})={}&J_{n+1}-tq^{6n-6}(q^2+q^4+q^5)J_n\\&+t^2q^{12n-12}(1+q+q^3)J_{n-1}-t^3q^{18n-25}J_{n-2}.\end{aligned}
$$

代表来源：`AQ-10.27`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **AQ-10.27**（ANDREWS-Q；印刷页 103；式 (10.27)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 n≥5；F 为 (10.22) 的五元线性算子；J_n=F(n,t;d_{6n-1},…,d_{6n-25})；G_n 由 (10.24) 给出。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_Q.md`
- `round1_source_collection/records/ANDREWS_Q_supplement.md`
