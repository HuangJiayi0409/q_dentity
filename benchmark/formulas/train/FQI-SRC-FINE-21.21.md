# FQI-SRC-FINE-21.21 · basic multinomial 的分数幂特化

家族：A · 超几何型有限求和；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
Q_n(1,q^{1/p},q^{2/p},\ldots,q^{(p-1)/p})=\frac{(q;q)_n}{(q^{1/p};q^{1/p})_n}.
$$

代表来源：`FINE-21.21`。

局部定义：Q_n(u_1,…,u_k)=\sum_{r_1+…+r_k=n,\,r_i≥0}(q;q)_n\prod_{i=1}^k u_i^{r_i}/(q;q)_{r_i}。

来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **FINE-21.21**（FINE；印刷页 30；式 (21.21)；The basic multinomial）：q 为形式变量；数值代入要求所有实际分母非零，Gaussian 在奇点先作多项式延拓。空乘积为 1、空和为 0。p≥1，n≥0 为整数；选择 q^{1/p}。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/FINE.md`
- `round1_source_collection/records/FINE_supplement.md`
