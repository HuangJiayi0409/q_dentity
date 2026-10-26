# FQI-SRC-GR2-7.Ex38 · 离散 q-Hermite 三项递推

家族：C · 递推与差分关系；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
H_{n+1}(x;q)=xH_n(x;q)-q^{n-1}(1-q^n)H_{n-1}(x;q),\quad H_n(x;q)=\sum_{k=0}^{\lfloor n/2\rfloor}\frac{(q;q)_n(-1)^kq^{k(k-1)}x^{n-2k}}{(q^2;q^2)_k(q;q)_{n-2k}}.
$$

代表来源：`GR2-7.Ex38`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-7.Ex38**（GR；Chapter 7, 7.Ex38, 印刷p209）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。n≥1。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
