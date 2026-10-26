# FQI-SRC-SILLS-1.99 · Watson 终止和二阶递推

家族：C · 递推与差分关系；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
f_n=\frac{(aq^n-1)(q^n-q)(aq^n-q)(bcde-a^2q^n)}{q(b-aq^n)(c-aq^n)(d-aq^n)(e-aq^n)}f_{n-2}+\frac{aq^n-1}{q(b-aq^n)(c-aq^n)(d-aq^n)(e-aq^n)}\bigl[a^3(q+1)q^{3n}+q^{n+1}(a^2q+a(bec+bed+bcd+cde)+bcde)-aq^{2n}(aq(a+b+c+d+e)+bcde)-bcde(q+1)q\bigr]f_{n-1}.
$$

代表来源：`SILLS-1.99`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **SILLS-1.99**（SILLS；印刷页 46；1.99）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥2；f_n 为(1.98)左侧终止和。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/SILLS.md`
- `round1_source_collection/records/SILLS_supplement.md`
