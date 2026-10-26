# FQI-SRC-AP-11.2.10 · MacMahon 盒内平面分拆有限乘积

家族：G · 差分域／环、参数关系与生成函数；难度：高；集合：test。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\Pi_{k,r}(n;q)=\prod_{j=0}^{k-1}\frac{(q;q)_j(q;q)_{n+r+j}}{(q;q)_{r+j}(q;q)_{n+j}}.
$$

代表来源：`AP-11.2.10`。

局部定义：π_r(n₁,…,n_k;q) 按体积计平面分拆：至多 k 行、r 列，第 i 行首项恰为 n_i（允许补零）。Π_{k,r}(n;q) 按体积计 k×r 矩形内、所有项≤n 的平面分拆。原书后者也用 π，此处改大写 Π 以区分。

来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **AP-11.2.10**（ANDREWS-P；p.183, Theorem 11.2, (11.2.10)）：k,r≥1；n≥0 为整数；乘积商按有理函数解释，约去后为多项式。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_P.md`
- `round1_source_collection/records/ANDREWS_P_supplement.md`
