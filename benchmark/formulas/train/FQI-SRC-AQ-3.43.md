# FQI-SRC-AQ-3.43 · 有限 k 重 Bailey 链

家族：G · 差分域／环、参数关系与生成函数；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\begin{aligned}&\sum_{r=0}^N\frac{(q^{-N};q)_r}{(aq^{N+1};q)_r}\prod_{i=1}^k\frac{(b_i,c_i;q)_r}{(aq/b_i,aq/c_i;q)_r}\left(\frac{a^kq^{k+N}}{\prod_{i=1}^kb_ic_i}\right)^r(-1)^rq^{-r(r-1)/2}\alpha_r\\&=\frac{(aq,aq/(b_kc_k);q)_N}{(aq/b_k,aq/c_k;q)_N}\sum_{0\le n_1\le\cdots\le n_k\le N}\frac{(q^{-N};q)_{n_k}\beta_{n_1}}{(b_kc_kq^{-N}/a;q)_{n_k}}\prod_{i=1}^k(b_i,c_i;q)_{n_i}\prod_{i=1}^{k-1}\frac{(aq/(b_ic_i);q)_{n_{i+1}-n_i}(aq/(b_ic_i))^{n_i}}{(q;q)_{n_{i+1}-n_i}(aq/b_i,aq/c_i;q)_{n_{i+1}}}\,q^{n_k}.\end{aligned}
$$

代表来源：`AQ-3.43`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **AQ-3.43**（ANDREWS-Q；印刷页 30；式 (3.43)）：\(\beta_n=\sum_{r=0}^n\alpha_r/((q;q)_{n-r}(aq;q)_{n+r})\)；所有出现的有限分母非零。 k≥1，N≥0；a,q,b_i,c_i≠0。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_Q.md`
- `round1_source_collection/records/ANDREWS_Q_supplement.md`
