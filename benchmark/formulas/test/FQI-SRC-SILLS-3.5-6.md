# FQI-SRC-SILLS-3.5-6 · Bailey 链第二步有限变换

家族：A · 超几何型有限求和；难度：中；集合：test。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\mathcal B_n[\alpha;x,q]=\frac1{(xq/\rho_1,xq/\rho_2;q)_n}\sum_{j=0}^n\frac{(\rho_1,\rho_2;q)_j(xq/(\rho_1\rho_2);q)_{n-j}(xq/(\rho_1\rho_2))^j}{(q;q)_j(q;q)_{n-j}},\qquad \alpha_r=\frac{(\rho_1,\rho_2;q)_r(xq/(\rho_1\rho_2))^r}{(xq/\rho_1,xq/\rho_2;q)_r}\alpha_r^{(1,1,2)}(x,q)
$$

代表来源：`SILLS-3.5-6`。

局部定义：\mathcal B_n[\alpha;x,q]:=\sum_{r=0}^n\alpha_r/((q;q)_{n-r}(xq;q)_{n+r}).

来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **SILLS-3.5-6**（SILLS；印刷页 108；3.5-6）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0；所有分母非零。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/SILLS.md`
- `round1_source_collection/records/SILLS_supplement.md`
