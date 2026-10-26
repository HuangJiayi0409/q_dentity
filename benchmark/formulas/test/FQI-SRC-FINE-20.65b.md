# FQI-SRC-FINE-20.65b · Rogers–Szegő 混合 q-移位递推

家族：C · 递推与差分关系；难度：中；集合：test。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
q^nf_n(u)-f_n(uq)+(1-q^n)f_{n-1}(uq)=0.
$$

代表来源：`FINE-20.65b`。

局部定义：f_n(u)=\sum_{j=0}^n{n\brack j}_q u^j。

来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **FINE-20.65b**（FINE；印刷页 28；式 (20.65b)；A general transformation）：q 为形式变量；数值代入要求所有实际分母非零，Gaussian 在奇点先作多项式延拓。空乘积为 1、空和为 0。n≥1；f_n 由 (20.6) 定义。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/FINE.md`
- `round1_source_collection/records/FINE_supplement.md`
