# FQI-SRC-SILLS-4.38 · Bressoud 多项式的五阶递推

家族：C · 递推与差分关系；难度：高；集合：test。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\begin{aligned}0={}&B_{n+5}-(1+q+q^2+q^3+q^4+q^{2n+7}+q^{2n+8}+q^{2n+9})B_{n+4}\\&+q(q^{4n+12}+q^{2n+10}+q^{2n+6}+q^{2n+7}+2q^{2n+8}+2q^{2n+9}+q^{4n+13}+q^{4n+14}+q^6+q^5+2q^4+2q^3+2q^2+q+1)B_{n+3}\\&-q^3(q^{4n+12}+q^{2n+7}+q^{2n+8}+q^{2n+9}+q^{4n+11}+q^{6n+15}+q^6+q^5+2q^4+2q^3+2q^2+q+1)B_{n+2}\\&-q^6(q^{5n+10}+q^{2n+3}+q^{2n+4}+q^{2n+5}+q^{5n+8}-q^4-q^3-q^2-q-1)B_{n+1}\\&-q^{10}(q^{2n+1}-1)(q^{2n+2}-1)B_n.\end{aligned}
$$

代表来源：`SILLS-4.38`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **SILLS-4.38**（SILLS；印刷页 129；4.38）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0；B_n见(4.32)/(4.37)。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/SILLS.md`
- `round1_source_collection/records/SILLS_supplement.md`
