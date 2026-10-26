# FQI-Q-DYSON · A 型 q-Dyson 常数项

家族：G · 差分域／环、参数关系与生成函数；难度：高；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\operatorname{CT}_{x_1,\ldots,x_m}\prod_{1\le i<j\le m}(x_i/x_j;q)_{a_i}(qx_j/x_i;q)_{a_j}=\frac{(q;q)_{a_1+\cdots+a_m}}{\prod_{i=1}^m(q;q)_{a_i}}.
$$

代表来源：`GR2-2.NoteEx31`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-2.NoteEx31**（GR；Chapter 2, 2.NoteEx31, 印刷p68）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。m≥1，a_i≥0；x_i为可逆交换不定元。
  变量对应：代表式；保留本条来源域。
- **AQ-REF-QDYSON**（ANDREWS-Q；印刷页 38；式 (4.23)；Theorem 4.2）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 m≥1，a_i≥0；x_i 为 Laurent 变量。
  变量对应：公式逐字相同；维数与各 a_i 的整数条件逐来源保留。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_Q.md`
- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/ANDREWS_Q_supplement.md`
- `round1_source_collection/records/GR2_supplement.md`
