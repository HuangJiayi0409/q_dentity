# FQI-CAYLEY · Cayley 有限有理分解

家族：G · 差分域／环、参数关系与生成函数；难度：中；集合：test。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\frac1{(q;q)_n}=\sum_{\substack{p_1,\ldots,p_n\ge0\\\sum_{j=1}^n jp_j=n}}\prod_{j=1}^n\frac1{j^{p_j}p_j!(1-q^j)^{p_j}}.
$$

代表来源：`AP-5.CAYLEY`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **AP-5.CAYLEY**（ANDREWS-P；p.81, Examples 1–2 后的 Cayley general decomposition）：n≥0；有理函数域 Q(q)；n=0 时空指标项为1。
  变量对应：代表式；保留本条来源域。
- **AP-12.E1**（ANDREWS-P；p.209, Example 1）：n≥0；有理函数域 Q(q)；n=0 时空指标项为1。
  变量对应：公式、定义与条件逐字相同；仅书内定位不同。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_P.md`
- `round1_source_collection/records/ANDREWS_P_supplement.md`
