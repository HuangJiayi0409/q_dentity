# FQI-SRC-GR2-8.3.3 · q-Hahn 多项式的 Watson 型乘积

家族：A · 超几何型有限求和；难度：高；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
Q_n(x)Q_n(y)=(-aq)^nq^{\binom n2}\frac{(bq;q)_n}{(aq;q)_n}\sum_{m=0}^n\frac{(q^{-n},abq^{n+1},q^{x-N},q^{y-N};q)_m(aq^{x+y})^{-m}}{(q,bq,q^{-N},q^{-N};q)_m}{}_4\phi_3^{[m]}(q^{-x},q^{-y},b^{-1}q^{-m},q^{-m};aq,q^{N-x+1-m},q^{N-y+1-m};q,abq^{2N+3}).
$$

代表来源：`GR2-8.3.3`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-8.3.3**（GR；Chapter 8, 8.3.3, 印刷p221）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。0≤n,x,y≤N；Q定义见7.2.22；先乘开有限积消去可去奇点，或取实际无零分母域。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
