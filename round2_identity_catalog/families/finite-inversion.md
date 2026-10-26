# 有限序列、三角矩阵与 Lagrange 反演

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 本次未匹配到旧算法 5 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

## FQI-SRC-GR2-2.2.2 · Bailey 的有限序列双和展开

$$
\sum_{k=0}^n\frac{(b,c,q^{-n};q)_k}{(q,aq/b,aq/c;q)_k}A_k=\sum_{j=0}^n\frac{(aq/(bc),aq^j,q^{-n};q)_j}{(q,aq/b,aq/c;q)_j}(-1)^jq^{-j(j-1)/2}\sum_{i=0}^{n-j}\frac{(q^{j-n},aq^{2j};q)_i}{(q,aq^j;q)_i}q^{-ij}\left(\frac{bc}{aq}\right)^{i+j}A_{i+j}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-2.2.2`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-2.2.2**（Chapter 2, 2.2.2, 印刷p40）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。abc≠0；A₀,…,Aₙ为任意标量序列。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-2.8.2 · Bailey 有限支持序列展开

$$
\sum_{k=0}^N\frac{(a,b,c;q)_k}{(q,aq/b,aq/c;q)_k}A_k=\sum_{j=0}^N\frac{(\lambda;q)_j(1-\lambda q^{2j})(\lambda b/a,\lambda c/a,aq/(bc);q)_j(a;q)_{2j}}{(q;q)_j(1-\lambda)(aq/b,aq/c,qa^2/(\lambda bc);q)_j(\lambda q;q)_{2j}}\left(\frac a\lambda\right)^j\sum_{k=0}^{N-j}\frac{(aq^{2j},a/\lambda,\lambda bcq^j/a;q)_k}{(q,\lambda q^{2j+1},a^2q^{j+1}/(\lambda bc);q)_k}A_{j+k}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-2.8.2`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-2.8.2**（Chapter 2, 2.8.2, 印刷p45）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。N≥0，abcλ≠0，λ≠1；A_k=0对k>N。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-3.6.17 · Bressoud–Gasper 双底数正交核

$$
\sum_{k=0}^n\frac{(1-ap^kq^k)(1-bp^kq^{-k})(a,b;p)_k(q^{-n},aq^n/b;q)_kq^k}{(1-a)(1-b)(q,aq/b;q)_k(apq^n,bpq^{-n};p)_k}=\delta_{n,0}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-3.6.17`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-3.6.17**（Chapter 3, 3.6.17, 印刷p83）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。ab≠0；p为另一底数。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-3.6.18 · 双底数有限三角矩阵反演

$$
\sum_{j=m}^n A_{nj}B_{jm}=\delta_{n,m},\qquad\sum_{j=m}^n B_{nj}A_{jm}=\delta_{n,m},\quad A_{nj}=\frac{(-1)^{n+j}(1-ap^jq^j)(1-bp^jq^{-j})(apq^n,bpq^{-n};p)_{n-1}}{(q;q)_{n-j}(apq^n,bpq^{-n};p)_j(bq^{1-2n}/a;q)_{n-j}},\quad B_{jm}=\frac{(ap^mq^m,bp^mq^{-m};p)_{j-m}}{(q,aq^{1+2m}/b;q)_{j-m}}(-aq^{1+2m}/b)^{j-m}q^{(j-m)(j-m-1)}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-3.6.18`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-3.6.18**（Chapter 3, 3.6.18, 印刷p83）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。0≤m≤n，ab≠0；p为另一底数；n=0时有限负长度按倒积。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-3.Ex23 · 双底数 q-Lagrange 的有限系数反演

$$
f_j=\sum_{n=0}^jB_{jn}c_n\quad\Longleftrightarrow\quad c_n=\sum_{j=0}^nA_{nj}f_j.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-3.Ex23`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-3.Ex23**（Chapter 3, 3.Ex23, 印刷p107）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。A,B为(3.6.18–20)的有限三角矩阵；取任意有限前缀。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
