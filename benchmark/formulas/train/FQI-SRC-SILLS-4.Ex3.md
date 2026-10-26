# FQI-SRC-SILLS-4.Ex3 · Borwein 多项式的耦合递推

家族：C · 递推与差分关系；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\begin{aligned}\mathsf A_n&=(1+q^{2n-1})\mathsf A_{n-1}+q^n(\mathsf B_{n-1}+\mathsf C_{n-1}),\\\mathsf B_n&=(1+q^{2n-1})\mathsf B_{n-1}+q^{n-1}\mathsf A_{n-1}-q^n\mathsf C_{n-1},\\\mathsf C_n&=(1+q^{2n-1})\mathsf C_{n-1}+q^{n-1}(\mathsf A_{n-1}-\mathsf B_{n-1}).\end{aligned}
$$

代表来源：`SILLS-4.Ex3`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **SILLS-4.Ex3**（SILLS；印刷页 137；4.Ex3）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥1；A₀=1，B₀=C₀=0。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/SILLS.md`
- `round1_source_collection/records/SILLS_supplement.md`
