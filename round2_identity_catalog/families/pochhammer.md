# 有限 q-Pochhammer 移位、拼接与反向

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 已有 Lean 证明实现（旧条件域） 3 条；已有可复用部件，待组装 21 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

## FQI-POCHHAMMER-NEGATIVE · 负整数长度 q-Pochhammer

$$
(a;q)_{-n}=\frac1{(aq^{-n};q)_n}=\frac{(-q/a)^nq^{n(n-1)/2}}{(q/a;q)_n}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-I-02`。

**证明算法状态：已有可复用部件，待组装**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-POCHHAMMER-NEGATIVE)

方法：负长度定义与反射组合。

覆盖边界：记录是两个等号的组合，不能仅因负长度定义已证就标整条完成。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-I-02**（Appendix I, (I.2), 印刷p351）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。a≠0。
  对应：代表式；保留本条来源域。
- **FINE-18.11**（印刷页 19；式 (18.11)）：q 为形式变量；数值代入要求所有实际分母非零，Gaussian 在奇点先作多项式延拓。空乘积为 1、空和为 0。n≥0，a,q≠0；所有倒数分母非零。
  对应：GR 的 a=Fine 的 aq；(−aq)^−n q^{n(n+1)/2}=(−1/a)^n q^{n(n−1)/2}。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-1.Ex1ii · 独立负移位的有限乘积

$$
(aq^{-k-n};q)_n=\frac{(q/a;q)_{n+k}}{(q/a;q)_k}(-a/q)^nq^{-nk-n(n-1)/2}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-1.Ex1ii`。

**证明算法状态：已有可复用部件，待组装**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SRC-GR2-1.Ex1ii)

方法：Pochhammer 拼接／反射引理组合。

覆盖边界：新组合的 Lean 证明与安全分母条件尚未接入；不能把几个基础引理视为整个家族已自动完成。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-1.Ex1ii**（Chapter 1, 1.Ex1ii, 印刷p24）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。k≥0，a≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-I-03 · q-Pochhammer 倒底数

$$
(a;q^{-1})_n=(-a)^nq^{-n(n-1)/2}(a^{-1};q)_n
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-I-03`。

**证明算法状态：已有可复用部件，待组装**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SRC-GR2-I-03)

方法：Pochhammer 拼接／反射引理组合。

覆盖边界：新组合的 Lean 证明与安全分母条件尚未接入；不能把几个基础引理视为整个家族已自动完成。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-I-03**（Appendix I, (I.3), 印刷p351）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。n 为非负整数；q 为非零且非单位根的复数；所有显示的分母非零。 a≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-I-07 · 有限乘积反向排列

$$
(a;q)_n=(-a)^nq^{n(n-1)/2}(q^{1-n}/a;q)_n
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-I-07`。

**证明算法状态：已有可复用部件，待组装**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SRC-GR2-I-07)

方法：Pochhammer 拼接／反射引理组合。

覆盖边界：新组合的 Lean 证明与安全分母条件尚未接入；不能把几个基础引理视为整个家族已自动完成。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-I-07**（Appendix I, (I.7), 印刷p351）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。n 为非负整数；q 为非零且非单位根的复数；所有显示的分母非零。 a≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-I-08 · 负移位、非负长度的乘积

$$
(aq^{-n};q)_n=(-a/q)^nq^{-n(n-1)/2}(q/a;q)_n
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-I-08`。

**证明算法状态：已有 Lean 证明实现（旧条件域）**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SRC-GR2-I-08)

方法：有限乘积反射与幂指数归一化。

覆盖边界：旧引理位于 NormedField 文件，q,a≠0；没有 ‖q‖<1 假设，但一般 Field 的无范数包装仍需整理。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-I-08**（Appendix I, (I.8), 印刷p351）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。n 为非负整数；q 为非零且非单位根的复数；所有显示的分母非零。 a≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-I-09 · 负移位乘积之比

$$
\frac{(aq^{-n};q)_n}{(bq^{-n};q)_n}=\frac{(q/a;q)_n}{(q/b;q)_n}(a/b)^n.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-I-09`。

**证明算法状态：已有可复用部件，待组装**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SRC-GR2-I-09)

方法：Pochhammer 拼接／反射引理组合。

覆盖边界：新组合的 Lean 证明与安全分母条件尚未接入；不能把几个基础引理视为整个家族已自动完成。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-I-09**（Appendix I, (I.9), 印刷p351）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。ab≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-I-10 · 长度 n−k 的反向改写

$$
(a;q)_{n-k}=\frac{(-q/a)^kq^{k(k-1)/2-nk}(a;q)_n}{(q^{1-n}/a;q)_k}
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-I-10`。

**证明算法状态：已有可复用部件，待组装**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SRC-GR2-I-10)

方法：Pochhammer 拼接／反射引理组合。

覆盖边界：新组合的 Lean 证明与安全分母条件尚未接入；不能把几个基础引理视为整个家族已自动完成。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-I-10**（Appendix I, (I.10), 印刷p351）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。n 为非负整数；q 为非零且非单位根的复数；所有显示的分母非零。 a≠0。 k 为整数且 0≤k≤n。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-I-11 · 互补长度乘积之比

$$
\frac{(a;q)_{n-k}}{(b;q)_{n-k}}=\frac{(a;q)_n(q^{1-n}/b;q)_k}{(b;q)_n(q^{1-n}/a;q)_k}(b/a)^k.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-I-11`。

**证明算法状态：已有可复用部件，待组装**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SRC-GR2-I-11)

方法：Pochhammer 拼接／反射引理组合。

覆盖边界：新组合的 Lean 证明与安全分母条件尚未接入；不能把几个基础引理视为整个家族已自动完成。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-I-11**（Appendix I, (I.11), 印刷p351）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。ab≠0，0≤k≤n。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-I-12 · 终止参数 q^{-n} 的乘积

$$
(q^{-n};q)_k=(-1)^kq^{k(k-1)/2-nk}\frac{(q;q)_n}{(q;q)_{n-k}}
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-I-12`。

**证明算法状态：已有可复用部件，待组装**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SRC-GR2-I-12)

方法：Pochhammer 拼接／反射引理组合。

覆盖边界：新组合的 Lean 证明与安全分母条件尚未接入；不能把几个基础引理视为整个家族已自动完成。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-I-12**（Appendix I, (I.12), 印刷p351）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。n 为非负整数；q 为非零且非单位根的复数；所有显示的分母非零。 k 为整数且 0≤k≤n。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-I-13 · 独立长度的负移位

$$
(aq^{-n};q)_k=\frac{(a;q)_k(q/a;q)_n}{(q^{1-k}/a;q)_n}q^{-nk}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-I-13`。

**证明算法状态：已有可复用部件，待组装**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SRC-GR2-I-13)

方法：Pochhammer 拼接／反射引理组合。

覆盖边界：新组合的 Lean 证明与安全分母条件尚未接入；不能把几个基础引理视为整个家族已自动完成。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-I-13**（Appendix I, (I.13), 印刷p351）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。a≠0，k≥0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-I-14 · 互补长度的负移位

$$
(aq^{-n};q)_{n-k}=\frac{(q/a;q)_n}{(q/a;q)_k}(-a/q)^{n-k}q^{k(k-1)/2-n(n-1)/2}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-I-14`。

**证明算法状态：已有可复用部件，待组装**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SRC-GR2-I-14)

方法：Pochhammer 拼接／反射引理组合。

覆盖边界：新组合的 Lean 证明与安全分母条件尚未接入；不能把几个基础引理视为整个家族已自动完成。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-I-14**（Appendix I, (I.14), 印刷p352）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。a≠0，0≤k≤n。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-I-15 · 双倍负移位

$$
(aq^{-2n};q)_n=\frac{(q/a;q)_{2n}}{(q/a;q)_n}(-a/q^2)^nq^{-3n(n-1)/2}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-I-15`。

**证明算法状态：已有可复用部件，待组装**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SRC-GR2-I-15)

方法：Pochhammer 拼接／反射引理组合。

覆盖边界：新组合的 Lean 证明与安全分母条件尚未接入；不能把几个基础引理视为整个家族已自动完成。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-I-15**（Appendix I, (I.15), 印刷p352）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。a≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-I-16 · 整数倍负移位

$$
(aq^{-kn};q)_n=\frac{(q/a;q)_{kn}}{(q/a;q)_{(k-1)n}}(-a)^nq^{n(n-1)/2-kn^2}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-I-16`。

**证明算法状态：已有可复用部件，待组装**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SRC-GR2-I-16)

方法：Pochhammer 拼接／反射引理组合。

覆盖边界：新组合的 Lean 证明与安全分母条件尚未接入；不能把几个基础引理视为整个家族已自动完成。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-I-16**（Appendix I, (I.16), 印刷p352）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。a≠0，k≥1。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-I-17 · 有限乘积拼接

$$
(a;q)_{n+k}=(a;q)_n(aq^n;q)_k
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-I-17`。

**证明算法状态：已有 Lean 证明实现（旧条件域）**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SRC-GR2-I-17)

方法：有限乘积区间拼接。

覆盖边界：旧引理在一般 Field 下，无额外分母约束。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-I-17**（Appendix I, (I.17), 印刷p352）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。n 为非负整数；q 为非零且非单位根的复数；所有显示的分母非零。 k 为非负整数。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-I-18 · 交换两个移位长度

$$
(aq^n;q)_k=\frac{(aq^k;q)_n(a;q)_k}{(a;q)_n}
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-I-18`。

**证明算法状态：已有可复用部件，待组装**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SRC-GR2-I-18)

方法：Pochhammer 拼接／反射引理组合。

覆盖边界：新组合的 Lean 证明与安全分母条件尚未接入；不能把几个基础引理视为整个家族已自动完成。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-I-18**（Appendix I, (I.18), 印刷p352）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。n 为非负整数；q 为非零且非单位根的复数；所有显示的分母非零。 k 为非负整数。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-I-19 · 整数倍长度的尾段

$$
(aq^{kn};q)_n=\frac{(a;q)_{(k+1)n}}{(a;q)_{kn}}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-I-19`。

**证明算法状态：已有可复用部件，待组装**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SRC-GR2-I-19)

方法：Pochhammer 拼接／反射引理组合。

覆盖边界：新组合的 Lean 证明与安全分母条件尚未接入；不能把几个基础引理视为整个家族已自动完成。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-I-19**（Appendix I, (I.19), 印刷p352）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。k≥0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-I-20 · 从有限乘积截出尾段

$$
(aq^k;q)_{n-k}=\frac{(a;q)_n}{(a;q)_k}
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-I-20`。

**证明算法状态：已有可复用部件，待组装**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SRC-GR2-I-20)

方法：Pochhammer 拼接／反射引理组合。

覆盖边界：新组合的 Lean 证明与安全分母条件尚未接入；不能把几个基础引理视为整个家族已自动完成。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-I-20**（Appendix I, (I.20), 印刷p352）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。n 为非负整数；q 为非零且非单位根的复数；所有显示的分母非零。 a≠0。 k 为整数且 0≤k≤n。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-I-21 · 双倍移位与互补长度

$$
(aq^{2k};q)_{n-k}=\frac{(a;q)_n(aq^n;q)_k}{(a;q)_{2k}}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-I-21`。

**证明算法状态：已有可复用部件，待组装**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SRC-GR2-I-21)

方法：Pochhammer 拼接／反射引理组合。

覆盖边界：新组合的 Lean 证明与安全分母条件尚未接入；不能把几个基础引理视为整个家族已自动完成。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-I-21**（Appendix I, (I.21), 印刷p352）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。0≤k≤n。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-I-22 · 整数倍移位与互补长度

$$
(aq^{jk};q)_{n-k}=\frac{(a;q)_n(aq^n;q)_{(j-1)k}}{(a;q)_{jk}}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-I-22`。

**证明算法状态：已有可复用部件，待组装**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SRC-GR2-I-22)

方法：Pochhammer 拼接／反射引理组合。

覆盖边界：新组合的 Lean 证明与安全分母条件尚未接入；不能把几个基础引理视为整个家族已自动完成。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-I-22**（Appendix I, (I.22), 印刷p352）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。j≥1，0≤k≤n。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-FINE-2.1 · q-Pochhammer 首项递推

$$
(aq;q)_n=(1-aq)(aq^2;q)_{n-1}\quad(n\ge1).
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`FINE-2.1`。

**证明算法状态：已有 Lean 证明实现（旧条件域）**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SRC-FINE-2.1)

方法：首项分离与有限乘积重指标。

覆盖边界：n≥1 时有 (n−1)+1=n；只需指标包装。

定义文件：[FINE_supplement.md](../../round1_source_collection/records/FINE_supplement.md)；[FINE.md](../../round1_source_collection/books/FINE.md)。

- **FINE-2.1**（印刷页 1；式 (2.1)）：q 为形式变量；数值代入要求所有实际分母非零，Gaussian 在奇点先作多项式延拓。空乘积为 1、空和为 0。n≥1；分母不涉及。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-KAC-CHEUNG-3.6 · 有限 q 幂的指标相加

$$
P_{m+n}(x,a;q)=P_m(x,a;q)P_n(x,q^ma;q).
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`KAC-CHEUNG-3.6`。

**证明算法状态：已有可复用部件，待组装**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SRC-KAC-CHEUNG-3.6)

方法：有限 q 幂转 Pochhammer 后拼接。

覆盖边界：旧项目没有目录 P_n 的定义桥接；不可悄悄排除 x=0。

定义文件：[KAC_CHEUNG_supplement.md](../../round1_source_collection/records/KAC_CHEUNG_supplement.md)；[KAC_CHEUNG.md](../../round1_source_collection/books/KAC_CHEUNG.md)。

- **KAC-CHEUNG-3.6**（印刷页 8；3.6）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。m,n∈Z。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-KAC-CHEUNG-3.9 · 有限 q 幂的交换与倒序

$$
P_n(a,x;q)=(-1)^nq^{n(n-1)/2}P_n(x,q^{1-n}a;q).
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`KAC-CHEUNG-3.9`。

**证明算法状态：已有可复用部件，待组装**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SRC-KAC-CHEUNG-3.9)

方法：有限乘积反射。

覆盖边界：目录局部对象与旧 qpoch 未接入。

定义文件：[KAC_CHEUNG_supplement.md](../../round1_source_collection/records/KAC_CHEUNG_supplement.md)；[KAC_CHEUNG.md](../../round1_source_collection/books/KAC_CHEUNG.md)。

- **KAC-CHEUNG-3.9**（印刷页 11；3.9）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。n∈Z。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-KAC-CHEUNG-13.10 · 倒底数有限乘积转换

$$
\prod_{j=0}^{n-1}(a-q^{-j})=(-1)^nq^{-n(n-1)/2}(a;q)_n.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`KAC-CHEUNG-13.10`。

**证明算法状态：已有可复用部件，待组装**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SRC-KAC-CHEUNG-13.10)

方法：逐因子倒底数反射。

覆盖边界：旧项目有反射工具，但未找到此式的同签名证明。

定义文件：[KAC_CHEUNG_supplement.md](../../round1_source_collection/records/KAC_CHEUNG_supplement.md)；[KAC_CHEUNG.md](../../round1_source_collection/books/KAC_CHEUNG.md)。

- **KAC-CHEUNG-13.10**（印刷页 44；13.10）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。n≥0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-KAC-CHEUNG-15.cancellation · 双边求和证明中的有限乘积消去

$$
\frac{(q/(ax);q)_{M-1}x^{M-1}}{(q^{1-M}ax;q)_{M-1}}=(-1)^{M-1}q^{M(M-1)/2}a^{1-M}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`KAC-CHEUNG-15.cancellation`。

**证明算法状态：已有可复用部件，待组装**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SRC-KAC-CHEUNG-15.cancellation)

方法：反射后有限积约消。

覆盖边界：需实现指数整理及分母非零桥接。

定义文件：[KAC_CHEUNG_supplement.md](../../round1_source_collection/records/KAC_CHEUNG_supplement.md)；[KAC_CHEUNG.md](../../round1_source_collection/books/KAC_CHEUNG.md)。

- **KAC-CHEUNG-15.cancellation**（印刷页 53；15.cancellation）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。M≥1，ax≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
