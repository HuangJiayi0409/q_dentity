# FQI-SRC-AQ-6.18 · Schur 辅助系数递推

家族：C · 递推与差分关系；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
a_0(q)=1,\quad a_n(q)=\frac{(1+q^{3n-1})(1+q^{3n-2})}{1-q^{3n}}a_{n-1}(q)\quad(n\ge1).
$$

代表来源：`AQ-6.18`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **AQ-6.18**（ANDREWS-Q；印刷页 55；式 (6.18)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 \(a_n=[x^n]G_0(x)/(x;q^3)_\infty\)，见 (6.15)–(6.17)。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_Q.md`
- `round1_source_collection/records/ANDREWS_Q_supplement.md`
