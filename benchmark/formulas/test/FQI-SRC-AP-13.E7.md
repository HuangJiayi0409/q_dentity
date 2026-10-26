# FQI-SRC-AP-13.E7 · Bender广义q-Vandermonde卷积（修订）

家族：G · 差分域／环、参数关系与生成函数；难度：中；集合：test。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\begin{bmatrix}N\\n\end{bmatrix}_q=\sum_{k=0}^n q^{(n-k)(a_{k+1}-k)}\begin{bmatrix}a_k\\k\end{bmatrix}_q\begin{bmatrix}N-a_{k+1}\\n-k\end{bmatrix}_q.
$$

代表来源：`AP-13.E7`。

局部定义：一般整数上指标 {v\brack k}_q=\prod_{i=0}^{k-1}(1-q^{v-i})/(q;q)_k；{v\brack0}_q=1，k<0时为0。

来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **AP-13.E7**（ANDREWS-P；pp.225–226, Chapter13 Example7）：n≥0，N与a_i为整数，a_{i+1}−a_i∈{0,1} (1≤i<n)。a₀、a_{n+1}任意；q≠0，(q;q)_n≠0；n=0两边为1。允许负上指标，不能沿用仅非负Gaussian越界为零的规则。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_P.md`
- `round1_source_collection/records/ANDREWS_P_supplement.md`
