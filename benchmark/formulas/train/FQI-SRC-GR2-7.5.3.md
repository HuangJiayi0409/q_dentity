# FQI-SRC-GR2-7.5.3 · Askey–Wilson 三项递推

家族：C · 递推与差分关系；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
(z+z^{-1})P_n(z)=A_nP_{n+1}(z)+B_nP_n(z)+C_nP_{n-1}(z),\quad A_n=\frac{1-abcdq^{n-1}}{(1-abcdq^{2n-1})(1-abcdq^{2n})},\quad C_n=\frac{(1-q^n)\prod_{uv\in\{ab,ac,ad,bc,bd,cd\}}(1-uvq^{n-1})}{(1-abcdq^{2n-2})(1-abcdq^{2n-1})},\quad B_n=a+a^{-1}-\frac{A_n}{a}(1-abq^n)(1-acq^n)(1-adq^n)-\frac{aC_n}{(1-abq^{n-1})(1-acq^{n-1})(1-adq^{n-1})}.
$$

代表来源：`GR2-7.5.3`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-7.5.3**（GR；Chapter 7, 7.5.3, 印刷p188）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。P_n(z)=a^{-n}(ab,ac,ad;q)_n4φ3^[n](q^{-n},abcdq^{n-1},az,a/z;ab,ac,ad;q,q)；az≠0，P_{−1}=0。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
