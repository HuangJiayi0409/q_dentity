# FQI-SRC-AQ-8.32 · 硬六角 F 多项式递推

家族：C · 递推与差分关系；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
F_N(\sigma;q)=F_{N-1}(\sigma;q)+q^{N-1}F_{N-2}(\sigma;q),\quad F_1(\sigma)=1,\quad F_2(0)=1+q,\ F_2(1)=1.
$$

代表来源：`AQ-8.32`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **AQ-8.32**（ANDREWS-Q；印刷页 79；式 (8.32)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 N≥3，σ∈{0,1}；F 是 (8.31) 非相邻占据序列的权重和。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_Q.md`
- `round1_source_collection/records/ANDREWS_Q_supplement.md`
