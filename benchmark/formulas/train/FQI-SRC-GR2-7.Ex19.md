# FQI-SRC-GR2-7.Ex19 · 连续 q-超球的次数和参数递推

家族：C · 递推与差分关系；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
(z+z^{-1})C_n(z;\beta)=\frac{1-q^{n+1}}{1-\beta q^n}C_{n+1}(z;\beta)+\frac{1-\beta^2q^{n-1}}{1-\beta q^n}C_{n-1}(z;\beta),\quad C_n(z;\beta)=\frac{1-\beta}{1-\beta q^n}\bigl(C_n(z;\beta q)-\beta C_{n-2}(z;\beta q)\bigr).
$$

代表来源：`GR2-7.Ex19`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-7.Ex19**（GR；Chapter 7, 7.Ex19, 印刷p203）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。C_{−1}=C_{−2}=0，C见7.4.14。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
