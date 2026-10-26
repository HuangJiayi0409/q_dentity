# FQI-SRC-AQ-2.23 · 连续 q-Hermite 多项式递推

家族：C · 递推与差分关系；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
A_r(x)=(x+x^{-1})A_{r-1}(x)-(1-q^{r-1})A_{r-2}(x),\quad A_0=1,\ A_1=x+x^{-1}.
$$

代表来源：`AQ-2.23`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **AQ-2.23**（ANDREWS-Q；印刷页 13；式 (2.23)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 r≥2，x≠0；\(A_r(x)=\sum_{j=0}^r{r\brack j}_q x^{r-2j}\)。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_Q.md`
- `round1_source_collection/records/ANDREWS_Q_supplement.md`
