# q-Dyson 与根系常数项

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 本次未匹配到旧算法 3 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

## FQI-Q-DYSON · A 型 q-Dyson 常数项

$$
\operatorname{CT}_{x_1,\ldots,x_m}\prod_{1\le i<j\le m}(x_i/x_j;q)_{a_i}(qx_j/x_i;q)_{a_j}=\frac{(q;q)_{a_1+\cdots+a_m}}{\prod_{i=1}^m(q;q)_{a_i}}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-2.NoteEx31`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-2.NoteEx31**（Chapter 2, 2.NoteEx31, 印刷p68）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。m≥1，a_i≥0；x_i为可逆交换不定元。
  对应：代表式；保留本条来源域。
- **AQ-REF-QDYSON**（印刷页 38；式 (4.23)；Theorem 4.2）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 m≥1，a_i≥0；x_i 为 Laurent 变量。
  对应：公式逐字相同；维数与各 a_i 的整数条件逐来源保留。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-6.Ex14 · Askey 单变量有限常数项恒等式

$$
\operatorname{CT}_x(qx,x^{-1};q)_j(qx^2,qx^{-2};q^2)_k=\frac{(q;q)_{2j}(q^2;q^2)_{2k}(q^{2j+1};q^2)_k}{(q;q)_j(q^2;q^2)_k(q;q)_{j+2k}}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-6.Ex14`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-6.Ex14**（Chapter 6, 6.Ex14, 印刷p171）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。j,k≥0；CT取有限Laurent多项式常数项。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AQ-4.3 · Bn有限常数项恒等式（Conjecture4.3修订）

$$
\operatorname{CT}_{x_1,\ldots,x_n}\left[\prod_{i=1}^n(x_i,q/x_i;q)_a\prod_{i<j}(x_ix_j,q/(x_ix_j),x_i/x_j,qx_j/x_i;q)_b\right]=\frac{(q;q)_{nb}}{(q;q)_b^n}\prod_{j=0}^{n-1}\frac{(q;q)_{2a+2jb}(q;q)_{2jb}}{(q;q)_{a+(n+j-1)b}(q;q)_{a+jb}}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AQ-4.3`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_Q_supplement.md](../../round1_source_collection/records/ANDREWS_Q_supplement.md)；[ANDREWS_Q.md](../../round1_source_collection/books/ANDREWS_Q.md)。

- **AQ-4.3**（p41, Conjecture4.3）：n≥1，a,b≥0为整数，q为形式变量；乘积商约去后为多项式。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
