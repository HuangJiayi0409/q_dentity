# q-Krawtchouk 有限正交

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 本次未匹配到旧算法 3 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

## FQI-SRC-GR2-7.Ex8i · q-Krawtchouk 有限正交（一）

$$
\sum_{x=0}^NK_m(q^{-x})K_n(q^{-x})\frac{(q^{-N};q)_x}{(q;q)_x}(-a)^x=(-q/a;q)_Na^Nq^{-N(N+1)/2}\frac{(q;q)_n(1+1/a)(-q^{N+1}/a;q)_n}{(-1/a;q)_n(1+q^{2n}/a)(q^{-N};q)_n}(-aq^{N+1})^{-n}q^{n(n+1)}\delta_{mn}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-7.Ex8i`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-7.Ex8i**（Chapter 7, 7.Ex8i, 印刷p201）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。0≤m,n≤N；K_n(t)=3φ2^[n](q^{-n},t,-q^n/a;q^{-N},0;q,q)，a≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-7.Ex8ii · q-Krawtchouk 有限正交（二）

$$
\sum_{x=0}^N\widetilde K_m(q^{-x})\widetilde K_n(q^{-x})\frac{(aq;q)_{N-x}(-1)^{N-x}q^{x(x-1)/2}}{(q;q)_x(q;q)_{N-x}}=\frac{(q,aq;q)_n(q;q)_{N-n}}{(q;q)_N^2}(-1)^na^Nq^{(N+n+1)(N+n)/2-n(n+1)}\delta_{mn}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-7.Ex8ii`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-7.Ex8ii**（Chapter 7, 7.Ex8ii, 印刷p201）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。0≤m,n≤N；K̃_n(t)=2φ1^[n](q^{-n},t;q^{-N};q,aq^{n+1})。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-7.Ex11 · 仿射 q-Krawtchouk 有限正交

$$
\sum_{x=0}^NK_m^{\rm Aff}(q^{-x})K_n^{\rm Aff}(q^{-x})\frac{(aq,q^{-N};q)_x}{(q;q)_x}\left(-\frac{q^{N-1}}a\right)^xq^{-x(x-1)/2}=\delta_{mn}/h_n,\quad h_n=\frac{(aq,q^{-N};q)_n}{(q;q)_n}(-1)^n(aq)^{N-n}q^{Nn-n(n-1)/2}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-7.Ex11`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-7.Ex11**（Chapter 7, 7.Ex11, 印刷p202）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。0≤m,n≤N；K_n^Aff(t)=3φ2^[n](q^{-n},t,0;aq,q^{-N};q,q)，a≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
