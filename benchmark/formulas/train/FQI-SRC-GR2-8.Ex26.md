# FQI-SRC-GR2-8.Ex26 · 相伴 Askey–Wilson 的有限 10W9 展开

家族：A · 超几何型有限求和；难度：高；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
r_n^{\rho}(z)=\sum_{k=0}^n\frac{(q^{-n},abcd\rho^2q^{n-1},abcd\rho^2/q,az,a/z;q)_kq^k}{(q,ab\rho,ac\rho,ad\rho,abcd\rho/q;q)_k}W_{10}^{[n-k]}(abcd\rho^2q^{k-2};\rho,bc\rho/q,bd\rho/q,cd\rho/q,q^{k+1},abcd\rho^2q^{n+k-1},q^{k-n};q,a^2).
$$

代表来源：`GR2-8.Ex26`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-8.Ex26**（GR；Chapter 8, 8.Ex26, 印刷p254）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。ρ=q^α；r_{−1}=0,r_0=1，(z+z^{-1}−a−a^{-1}+A(ρq^n)+C(ρq^n))r_n=A(ρq^n)r_{n+1}+C(ρq^n)r_{n−1}，A(v)=a^{-1}(1−abv)(1−acv)(1−adv)(1−abcdv/q)/((1−abcdv²/q)(1−abcdv²))，C(v)=a(1−bcv/q)(1−bdv/q)(1−cdv/q)(1−v)/((1−abcdv²/q²)(1−abcdv²/q))；abcdρz≠0。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
