# FQI-SRC-GR2-11.6.5-p0 · Macdonald 有限乘积望远镜求和

家族：G · 差分域／环、参数关系与生成函数；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\sum_{k=0}^nV_k\prod_{j=0}^{k-1}U_j=1-\prod_{j=0}^nU_j,\quad U_j=\frac{(1-b_j)(1-c_j)(1-d_j)(1-a_j^2/(b_jc_jd_j))}{(1-a_j/b_j)(1-a_j/c_j)(1-a_j/d_j)(1-b_jc_jd_j/a_j)},\quad V_j=\frac{(1-a_j)(1-a_j/(b_jc_j))(1-a_j/(b_jd_j))(1-a_j/(c_jd_j))}{(1-a_j/(b_jc_jd_j))(1-a_j/d_j)(1-a_j/c_j)(1-a_j/b_j)}.
$$

代表来源：`GR2-11.6.5-p0`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-11.6.5-p0**（GR；Chapter 11, 11.6.5-p0, 印刷p325）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。所有所用序列项非零；可含任意q依赖。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
