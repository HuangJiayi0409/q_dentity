# FQI-BAILEY-INVERSION · 有限 Bailey 反演

家族：G · 差分域／环、参数关系与生成函数；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\alpha_0=\beta_0,\qquad \alpha_n=(1-aq^{2n})\sum_{j=0}^n\frac{(aq;q)_{n+j-1}(-1)^{n-j}q^{(n-j)(n-j-1)/2}}{(q;q)_{n-j}}\beta_j\quad(n\ge1).
$$

代表来源：`AQ-3.40`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **AQ-3.40**（ANDREWS-Q；印刷页 29；式 (3.40)）：\(\beta_n=\sum_{r=0}^n\alpha_r/((q;q)_{n-r}(aq;q)_{n+r})\)；所有出现的有限分母非零。
  变量对应：代表式；保留本条来源域。
- **SILLS-2.31**（SILLS；印刷页 60；2.31）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0；n=r=0时(xq;q)₋₁=1/(1−x)，可去奇点约去；(α,β) 是关于x的Bailey对。
  变量对应：x→a，r→j；n=0 单列 α₀=β₀，约去 (1−a)(aq;q)_−1，避免伪奇点。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_Q.md`
- `round1_source_collection/books/SILLS.md`
- `round1_source_collection/records/ANDREWS_Q_supplement.md`
- `round1_source_collection/records/SILLS_supplement.md`
