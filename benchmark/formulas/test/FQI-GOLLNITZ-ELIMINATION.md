# FQI-GOLLNITZ-ELIMINATION · Göllnitz 消元式

家族：C · 递推与差分关系；难度：中；集合：test。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\begin{aligned}d_{6n+3}(t)-tq^{6n+2}d_{6n-3}(t)={}&d_{6n+5}(t)-tq^{6n+2}(1+q^2+q^3)d_{6n-1}(t)\\&+t^2q^{12n}(1+q+q^3)d_{6n-7}(t)-t^3q^{18n-7}d_{6n-13}(t).\end{aligned}
$$

代表来源：`AQ-10.23`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **AQ-10.23**（ANDREWS-Q；印刷页 103；式 (10.23)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 n≥2；d_{-1}=1。
  变量对应：代表式；保留本条来源域。
- **SILLS-2.90-91**（SILLS；印刷页 86；2.90-91）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥2。
  变量对应：G_N=d_N；全部系数逐项一致。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_Q.md`
- `round1_source_collection/books/SILLS.md`
- `round1_source_collection/records/ANDREWS_Q_supplement.md`
- `round1_source_collection/records/SILLS_supplement.md`
