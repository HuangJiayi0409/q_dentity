# FQI-SRC-SILLS-4.47 · Mod 8 的 q-Pell 多项式递推

家族：C · 递推与差分关系；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
P_n=(1+q^{2n-1})P_{n-1}+q^{2n-2}P_{n-2},\quad P_0=1,\ P_1=1+q.
$$

代表来源：`SILLS-4.47`。

局部定义：P_n=\sum_{j=0}^n\sum_{k=0}^{\min(j,n-j)}q^{j^2+k^2}{j\brack k}_{q^2}{n-k\brack j}_{q^2}.

来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **SILLS-4.47**（SILLS；印刷页 134；4.47）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥2。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/SILLS.md`
- `round1_source_collection/records/SILLS_supplement.md`
