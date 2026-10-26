# FQI-SRC-SILLS-1.90 · q-三项式 Laurent 多项式递推

家族：C · 递推与差分关系；难度：中；集合：test。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\mathcal T_n(x,q)=(1+xq^{3n-2}+x^{-1}q^{3n-1})\mathcal T_{n-1}(x,q)+q^{3n-3}(1-q^{3n-3})\mathcal T_{n-2}(x,q).
$$

代表来源：`SILLS-1.90`。

局部定义：\mathcal T_n(x,q)=\sum_{j=-n}^nx^jq^{j(3j-1)/2}C_n(j;q^3).

来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **SILLS-1.90**（SILLS；印刷页 44；1.90）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥2，x≠0；T₀=1，T₁=1+xq+x⁻¹q²。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/SILLS.md`
- `round1_source_collection/records/SILLS_supplement.md`
