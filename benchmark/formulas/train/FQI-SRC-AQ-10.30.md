# FQI-SRC-AQ-10.30 · Euler 乘积系数的有限递推

家族：G · 差分域／环、参数关系与生成函数；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
b_0=1,\quad D_j=\sum_{d\mid j}d\,a_d,\quad nb_n=\sum_{j=1}^nD_jb_{n-j}.
$$

代表来源：`AQ-10.30`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **AQ-10.30**（ANDREWS-Q；印刷页 104,105；式 (10.30)）：n≥1；\(b_n=[q^n]\prod_{m=1}^{n}(1-q^m)^{-a_m}\)，a_m 为整数。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_Q.md`
- `round1_source_collection/records/ANDREWS_Q_supplement.md`
