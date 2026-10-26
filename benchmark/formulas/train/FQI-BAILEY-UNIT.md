# FQI-BAILEY-UNIT · 一般参数单位 Bailey 对

家族：A · 超几何型有限求和；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\sum_{r=0}^n\frac{u_r(a)}{(q;q)_{n-r}(aq;q)_{n+r}}=\delta_{n,0},\quad u_0(a)=1,\quad u_r(a)=\frac{(-1)^rq^{r(r-1)/2}(1-aq^{2r})(aq;q)_{r-1}}{(q;q)_r}\ (r\ge1).
$$

代表来源：`AQ-3.48`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **AQ-3.48**（ANDREWS-Q；印刷页 31；式 (3.48)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 n≥0。
  变量对应：代表式；保留本条来源域。
- **SILLS-2.Ex2a**（SILLS；印刷页 72；2.Ex2a）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0；所有分母非零。
  变量对应：取定义 (d,e,k)=(1,1,1)，x→a；r≥1 时 (a;q)_r/(1−a)=(aq;q)_(r−1)，r=0 单列为1。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_Q.md`
- `round1_source_collection/books/SILLS.md`
- `round1_source_collection/records/ANDREWS_Q_supplement.md`
- `round1_source_collection/records/SILLS_supplement.md`
