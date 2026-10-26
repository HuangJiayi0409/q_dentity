# FQI-SRC-AQ-3.23 · Bailey 转置求和（有限支持特化）

家族：G · 差分域／环、参数关系与生成函数；难度：低；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\sum_{n=0}^N\alpha_n\sum_{r=n}^N\delta_r u_{r-n}v_{r+n}=\sum_{r=0}^N\delta_r\sum_{n=0}^r\alpha_n u_{r-n}v_{r+n}.
$$

代表来源：`AQ-3.23`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **AQ-3.23**（ANDREWS-Q；印刷页 24；式 (3.23)）：N≥0；α、δ、u、v 为任意在交换环中取值的有限向量。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_Q.md`
- `round1_source_collection/records/ANDREWS_Q_supplement.md`
