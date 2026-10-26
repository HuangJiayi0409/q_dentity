# FQI-SRC-GR2-8.Ex8 · 任意有限权序列的 q-Racah 双线性变换

家族：G · 差分域／环、参数关系与生成函数；难度：高；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\sum_{n=0}^z\frac{(aq,abq,bcq;q)_n(-c)^{-n}\lambda_nq^{\binom n2}}{(q,bq,aq/c;q)_n(abq;q)_{2n}}W_n(x;a,b,c,N)W_n(y;\alpha,ab/\alpha,\gamma,M)=\sum_{r=0}^z\sum_{s=0}^{z-r}\frac{(q^{-z};q)_{r+s}}{(q^{-N};q)_{r+s}}H_{r,s}A_{r,s}\mu_{r+s},\quad\lambda_n=\sum_{k=0}^{z-n}\frac{(q^{-z};q)_{n+k}\mu_{n+k}}{(q,abq^{2n+2};q)_k},\quad H_{r,s}=\frac{(q^{-x},cq^{x-N},q^{-y},\gamma q^{y-M};q)_r(q^{x-N},c^{-1}q^{-x};q)_s(1-cq^{r-s})q^{-rs}}{(q,\alpha q,q^{-M},ab\gamma q/\alpha,cq^{1-s};q)_r(q,bq,aq/c;q)_s(1-cq^{-s})},\quad A_{r,s}={}_5\phi_4^{[s]}(q^{-s},q^{r-y},\gamma q^{r+y-M},aq^{r+1},bcq^{r+1};\alpha q^{r+1},q^{r-M},ab\gamma q^{r+1}/\alpha,cq^{1+r-s};q,q).
$$

代表来源：`GR2-8.Ex8`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-8.Ex8**（GR；Chapter 8, 8.Ex8, 印刷p248）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。0≤z,x≤N≤M，0≤y≤M；µ_0…µ_z任意，abcαγ≠0。外系数为零的项整项置零且不计算其内部未定义级数；有效r≤x,y、s≤N−x。W见7.2.18。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
