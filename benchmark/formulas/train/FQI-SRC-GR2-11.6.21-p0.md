# FQI-SRC-GR2-11.6.21-p0 · 有限支撑的多底数序列展开（修订）

家族：G · 差分域／环、参数关系与生成函数；难度：高；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\sum_{j=0}^N\frac{A_jB_j(xw)^j}{(q;q)_j}=\sum_{n=0}^N\frac{(1-\gamma(rst/q)^n)(1-\sigma(r/q)^n)(-x)^nq^{n+\binom n2}}{(q;q)_n}\sum_{k=0}^{N-n}\frac{(1-\gamma\sigma^{-1}(st)^{n+k})B_{n+k}x^k(s/q)^{\binom{k+1}2}}{(s;s)_k(\gamma rs^{n+k}t/q;rt/q)_n(\sigma rs^{1-n-k}/q;rs/q)_n}\sum_{j=0}^n\frac{(1-\gamma\sigma^{-1}s^{n+k}t^nq^{j-n})(1-s^{-k}q^{j-n})(q^{-n};q)_j}{(1-s^{j-n-k})(q;q)_j}(\gamma\sigma^{-1}(st)^{n+1}q^{j-n-1};st/q)_{k-1}(\gamma\sigma^{-1}s^{n+k}t^{j+1};t)_{n-j-1}(\gamma rs^jt/q;rt/q)_j(\gamma(rst)^{j+1}q^{-j-2};rst/q^2)_{n-j-1}(\sigma rs^{1-j}/q;rs/q)_j(\sigma r^{j+1}q^{-j};r)_{n-j-1}A_jC_{j,n+k-j}w^jq^{n(j-n-k)}.
$$

代表来源：`GR2-11.6.21-p0`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-11.6.21-p0**（GR；Chapter 11, 11.6.21-p0, 印刷p330）：N≥0，B_j=0(j>N)，A_j任意，C_{j,0}=1。r,s,t,q,γ,σ非零，实际分母非零；负长度按有限倒积。j=n,k=0的相同零因子比先约为1；s=q时同理。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
