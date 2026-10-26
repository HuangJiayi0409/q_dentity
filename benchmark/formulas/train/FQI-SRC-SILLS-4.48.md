# FQI-SRC-SILLS-4.48 · T₁ 与 T₀ 的 q-三项式递推

家族：C · 递推与差分关系；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
T_1(n,j;q)=T_1(n-1,j;q)+q^{n+j}T_0(n-1,j+1;q)+q^{n-j}T_0(n-1,j-1;q).
$$

代表来源：`SILLS-4.48`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **SILLS-4.48**（SILLS；印刷页 135；4.48）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥1。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/SILLS.md`
- `round1_source_collection/records/SILLS_supplement.md`
