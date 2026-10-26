# FQI-GOLLNITZ-SHIFT · Göllnitz 参数移位

家族：C · 递推与差分关系；难度：高；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
d_{6n+3}(t)-tq^{6n+2}d_{6n-3}(t)=(1+tq^2)(1+tq^4)(1+tq^5)d_{6n-7}(tq^6).
$$

代表来源：`AQ-10.18`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **AQ-10.18**（ANDREWS-Q；印刷页 102；式 (10.18)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 n≥1，d_{-1}=1；d_N 为 (10.16) 的有界分拆多项式。
  变量对应：代表式；保留本条来源域。
- **SILLS-2.84**（SILLS；印刷页 86；2.84）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥1。
  变量对应：G_N(t,q)=d_N(t)，其余参数原样；两书采用修订后的较大部件约束及相同 t 权。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_Q.md`
- `round1_source_collection/books/SILLS.md`
- `round1_source_collection/records/ANDREWS_Q_supplement.md`
- `round1_source_collection/records/SILLS_supplement.md`
