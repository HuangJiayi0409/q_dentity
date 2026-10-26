# FQI-SRC-GR2-9.5.3-finite · 有限支撑权序列的 Askey–Wilson 双线性变换

家族：G · 差分域／环、参数关系与生成函数；难度：高；集合：test。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\sum_{n=0}^N\nu_nk_nr_n(z)r_n(v)=\sum_{n=0}^N\frac{(dz,d/z,dv,d/v;q)_nw_n}{(q,bd,cd,d/a;q)_n}W_{10}^{[n]}(aq^{-n}/d;q^{1-n}/(bd),q^{1-n}/(cd),q^{-n},az,a/z,av,a/v;q,bcq/(ad)),\quad\nu_n=\frac{(bc,ad;q)_n(-ad)^nq^{\binom n2}}{(abcd;q)_{2n}}\sum_{j=0}^{N-n}\frac{(adq^n,adq^n;q)_j}{(q,abcdq^{2n};q)_j}w_{n+j},\quad k_n=\frac{1-abcdq^{2n-1}}{1-abcd/q}\frac{(abcd/q,ab,ac,ad;q)_n}{(q,bc,bd,cd;q)_n}a^{-2n}.
$$

代表来源：`GR2-9.5.3-finite`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-9.5.3-finite**（GR；Chapter 9, 9.5.3-finite, 印刷p269）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。w_0…w_N任意且之后为0；r_n(z)=4φ3^[n](q^{-n},abcdq^{n−1},az,a/z;ab,ac,ad;q,q)，abcdzv≠0。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
