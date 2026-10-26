# FQI-SRC-KAC-CHEUNG-26.23 · 对称q-Taylor基底的正确有限构造

家族：G · 差分域／环、参数关系与生成函数；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
T_0(x)=1,\qquad T_n(x)=\frac{x^n}{\langle n\rangle_q!}-\sum_{k=0}^{n-1}\frac{a^{n-k}}{\langle n-k\rangle_q!}T_k(x),\qquad\widetilde D_qT_n=T_{n-1},\quad T_n(a)=0\ (n\ge1).
$$

代表来源：`KAC-CHEUNG-26.23`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **KAC-CHEUNG-26.23**（KAC-CHEUNG；p104, (26.23)的替代构造；边界见p103）：n≥0；d_j=⟨j⟩_q=(q^j−q^{-j})/(q−q^{-1})，d₀!=1，d_j!=∏_{i=1}^j d_i；q≠0,±1且d_1,…,d_n≠0。D̃_qf=(f(qx)−f(q^{-1}x))/((q−q^{-1})x)，x=0按多项式延拓。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/KAC_CHEUNG.md`
- `round1_source_collection/records/KAC_CHEUNG_supplement.md`
