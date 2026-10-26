# FQI-SRC-SILLS-5.6-8 · Motivated proof 中的有限系数多项式递推

家族：C · 递推与差分关系；难度：中；集合：test。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
A_{i+1}=A_i+B_i,\quad B_{i+1}=q^iA_i,\quad A_3=1,\ B_3=0;\qquad A_{i+1}=A_i+q^{i-1}A_{i-1}\ (i\ge4).
$$

代表来源：`SILLS-5.6-8`。

局部定义：等价地A_i为从{3,…,i−2}选取互不相邻整数的q权之和，B_i=q^{i−1}A_{i−1}（i≥4）；这个有限集合解释用于独立核验。

来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **SILLS-5.6-8**（SILLS；印刷页 142；5.6-8）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。耦合递推i≥3；A₄=1。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/SILLS.md`
- `round1_source_collection/records/SILLS_supplement.md`
