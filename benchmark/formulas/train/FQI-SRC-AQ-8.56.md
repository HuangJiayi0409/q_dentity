# FQI-SRC-AQ-8.56 · Andrews–Baxter–Forrester 双端终止变换

家族：A · 超几何型有限求和；难度：高；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\begin{aligned}&\sum_{r=-R}^N\frac{1-aq^{2r}}{1-a}\frac{(aq^{-R},q^{-N};q)_r}{(q^{R+1},aq^{N+1};q)_r}\prod_{i=1}^k\frac{(b_i,c_i;q)_r}{(aq/b_i,aq/c_i;q)_r}\left(\frac{a^kq^{k+N+R}}{\prod_{i=1}^kb_ic_i}\right)^r\\&=\frac{(q/a,aq/(b_1c_1);q)_R(aq,aq/(b_kc_k);q)_N}{(q/b_1,q/c_1;q)_R(aq/b_k,aq/c_k;q)_N}\sum_{\substack{m_1\ge-R,\ m_2,\ldots,m_{k-1}\ge0\\M_{k-1}\le N}}\frac{(aq^{R+1}/(b_1c_1);q)_{m_1}}{(q^{R+1};q)_{m_1}}\prod_{i=2}^{k-1}\frac{(aq/(b_ic_i);q)_{m_i}}{(q;q)_{m_i}}\\&\qquad\times\prod_{i=1}^{k-1}\frac{(b_{i+1},c_{i+1};q)_{M_i}}{(aq/b_i,aq/c_i;q)_{M_i}}\frac{(q^{-N};q)_{M_{k-1}}}{(b_kc_kq^{-N}/a;q)_{M_{k-1}}}\frac{a^{\sum_{i=1}^{k-2}M_i}q^{\sum_{i=1}^{k-1}M_i}}{\prod_{i=1}^{k-2}(b_{i+1}c_{i+1})^{M_i}}.\end{aligned}
$$

代表来源：`AQ-8.56`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **AQ-8.56**（ANDREWS-Q；印刷页 83；式 (8.56)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 k≥2，N,R≥0；q,a,b_i,c_i≠0，a≠1；\(M_i=\sum_{j=1}^im_j\)；负长度定义 \((x;q)_{-s}=1/(xq^{-s};q)_s\)，这些倒数分母亦须非零。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_Q.md`
- `round1_source_collection/records/ANDREWS_Q_supplement.md`
