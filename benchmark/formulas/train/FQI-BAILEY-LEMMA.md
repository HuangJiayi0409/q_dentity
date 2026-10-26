# FQI-BAILEY-LEMMA · 有限 Bailey 引理

家族：G · 差分域／环、参数关系与生成函数；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\sum_{r=0}^n\frac{(\rho_1,\rho_2;q)_r(aq/(\rho_1\rho_2))^r(aq/(\rho_1\rho_2);q)_{n-r}}{(aq/\rho_1,aq/\rho_2;q)_n(q;q)_{n-r}}\beta_r=\sum_{r=0}^n\frac{(\rho_1,\rho_2;q)_r(aq/(\rho_1\rho_2))^r\alpha_r}{(aq/\rho_1,aq/\rho_2;q)_r(q;q)_{n-r}(aq;q)_{n+r}}.
$$

代表来源：`AQ-REF-BAILEY`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **AQ-REF-BAILEY**（ANDREWS-Q；印刷页 25,26；式 (3.28)；Theorem 3.3, (3.27)–(3.30)）：\(\beta_n=\sum_{r=0}^n\alpha_r/((q;q)_{n-r}(aq;q)_{n+r})\)；所有出现的有限分母非零。 n≥0；q,a,ρ₁,ρ₂≠0。
  变量对应：代表式；保留本条来源域。
- **SILLS-2.34**（SILLS；印刷页 61；2.34）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0，ρ₁ρ₂≠0；(α,β) 是关于x的Bailey对。
  变量对应：x→a，左侧 j→r；把与求和指标无关的两个分母提出。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_Q.md`
- `round1_source_collection/books/SILLS.md`
- `round1_source_collection/records/ANDREWS_Q_supplement.md`
- `round1_source_collection/records/SILLS_supplement.md`
