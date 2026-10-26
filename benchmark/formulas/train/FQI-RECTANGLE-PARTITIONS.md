# FQI-RECTANGLE-PARTITIONS · 矩形分拆的 Gaussian 生成多项式

家族：G · 差分域／环、参数关系与生成函数；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\begin{bmatrix}n\\k\end{bmatrix}_q=\sum_{\substack{n-k\ge\lambda_1\ge\cdots\ge\lambda_k\ge0}}q^{\lambda_1+\cdots+\lambda_k}.
$$

代表来源：`GR2-1.NoteEx2-partition`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-1.NoteEx2-partition**（GR；Chapter 1, 1.NoteEx2-partition, 印刷p35）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。0≤k≤n；零部件只用于补齐长度。
  变量对应：代表式；保留本条来源域。
- **AP-3.2.1**（ANDREWS-P；p.33, Theorem 3.1, (3.2.1)）：N,M 为非负整数；q 为形式变量。
  变量对应：n=N+M，k=M；补零到恰 M 个部分，按大小 s 分组。
- **SILLS-1.Thm1.53**（SILLS；印刷页 34；1.Thm1.53）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。k,ℓ≥0；p计数部件≤k且长度≤ℓ的分拆。
  变量对应：n=k+ℓ；按分拆大小 r 分组；矩形共轭允许交换边长。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_P.md`
- `round1_source_collection/books/GR.md`
- `round1_source_collection/books/SILLS.md`
- `round1_source_collection/records/ANDREWS_P_supplement.md`
- `round1_source_collection/records/GR2_supplement.md`
- `round1_source_collection/records/SILLS_supplement.md`
