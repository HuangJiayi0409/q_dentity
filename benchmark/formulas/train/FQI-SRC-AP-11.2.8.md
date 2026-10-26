# FQI-SRC-AP-11.2.8 · 固定首列与盒内平面分拆的有限求和关系

家族：G · 差分域／环、参数关系与生成函数；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\Pi_{k,r}(n;q)=\sum_{n\ge n_1\ge\cdots\ge n_k\ge0}\pi_r(n_1,\ldots,n_k;q)=q^{-kn}\pi_{r+1}(\underbrace{n,\ldots,n}_{k};q).
$$

代表来源：`AP-11.2.8`。

局部定义：π_r(n₁,…,n_k;q) 按体积计平面分拆：至多 k 行、r 列，第 i 行首项恰为 n_i（允许补零）。Π_{k,r}(n;q) 按体积计 k×r 矩形内、所有项≤n 的平面分拆。原书后者也用 π，此处改大写 Π 以区分。

来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **AP-11.2.8**（ANDREWS-P；p.183, (11.2.8)）：k,r≥1，n≥0 为整数；末式在 Laurent 多项式环中解释。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_P.md`
- `round1_source_collection/records/ANDREWS_P_supplement.md`
