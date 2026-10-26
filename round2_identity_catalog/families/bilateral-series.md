# 双边终止基本超几何求和

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 本次未匹配到旧算法 3 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

## FQI-SRC-GR2-5.Ex11 · 双边终止 8ψ8 到 4ψ4

$$
\sum_{k=-n}^n\frac{1-aq^{2k}}{1-a}\frac{(c,d,e,f,aq^{-n},q^{-n};q)_k}{(aq/c,aq/d,aq/e,aq/f,q^{n+1},aq^{n+1};q)_k}\left(\frac{a^2q^{2n+2}}{cdef}\right)^k=\frac{(aq,q/a,aq/(cd),aq/(ef);q)_n}{(q/c,q/d,aq/e,aq/f;q)_n}\sum_{k=-n}^n\frac{(e,f,aq^{n+1}/(cd),q^{-n};q)_k}{(aq/c,aq/d,q^{n+1},ef/(aq^n);q)_k}q^k.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-5.Ex11`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-5.Ex11**（Chapter 5, 5.Ex11, 印刷p147）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。acdef≠0，a≠1；双边负指标按有限倒积。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-5.Ex18iii · Bailey 有限双边 5ψ5 求和

$$
\sum_{k=-n}^n\frac{(b,c,d,e,q^{-n};q)_k}{(q/b,q/c,q/d,q/e,q^{n+1};q)_k}q^k=\frac{(q,q/(bc),q/(bd),q/(cd);q)_n}{(q/b,q/c,q/d,q/(bcd);q)_n},\qquad bcde=q^{n+1}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-5.Ex18iii`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-5.Ex18iii**（Chapter 5, 5.Ex18iii, 印刷p150）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。bcde≠0；负指标按有限倒积。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-5.Ex18iv · Bailey 非对称长度的双边 5ψ5 求和

$$
\sum_{k=-n-1}^n\frac{(b,c,d,e,q^{-n};q)_k}{(q^2/b,q^2/c,q^2/d,q^2/e,q^{n+2};q)_k}q^k=\frac{(1-q)(q^2,q^2/(bc),q^2/(bd),q^2/(cd);q)_n}{(q^2/b,q^2/c,q^2/d,q^2/(bcd);q)_n},\qquad bcde=q^{n+3}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-5.Ex18iv`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-5.Ex18iv**（Chapter 5, 5.Ex18iv, 印刷p150）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。bcde≠0；注意下界为−n−1。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
