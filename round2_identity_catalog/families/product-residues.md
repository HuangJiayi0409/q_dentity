# 乘积步长、单位根与根参数分解

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 本次未匹配到旧算法 7 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

**新框架算法已完成（2026-09-22）**：[第一版范式与用法](../../finite_product_framework/docs/product_residues.md)。全部 7 条可由受限 Lean statement 生成框架，共 8 个等式目标，均通过含 `sorry` 的 Lean 检查。此完成记录指范式与生成器，下方旧算法匹配状态仍按原审计口径保留。

## FQI-POCHHAMMER-RESIDUES · 有限乘积按剩余类拆分

$$
(a;q)_{mn}=\prod_{j=0}^{m-1}(aq^j;q^m)_n
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-I-27`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-I-27**（Appendix I, (I.27), 印刷p352）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。n 为非负整数；q 为非零且非单位根的复数；所有显示的分母非零。 m 为正整数（作者源码中的 k 在此改名 m）。
  对应：代表式；保留本条来源域。
- **SILLS-2.49**（印刷页 65；(2.49)）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。d≥1，r≥0。
  对应：Q→q，d→m，r→n。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-POCHHAMMER-ROOTS · 单位根参数有限乘积分解

$$
(a^m;q^m)_n=\prod_{j=0}^{m-1}(a\omega_m^j;q)_n,\qquad\omega_m=e^{2\pi i/m}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-I-30`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-I-30**（Appendix I, (I.30), 印刷p352）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。m≥1。
  对应：代表式；保留本条来源域。
- **SILLS-2.RootFactor**（印刷页 65；2.RootFactor）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。e≥1，r≥0，ζ_e为本原e次单位根。
  对应：z→a，Q→q，e→m，r→n；h=1..m 与 j=0..m−1 枚举同一单位根集合。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-I-25 · 按偶数和奇数位置拆分

$$
(a;q)_{2n}=(a;q^2)_n(aq;q^2)_n
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-I-25`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-I-25**（Appendix I, (I.25), 印刷p352）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。n 为非负整数；q 为非零且非单位根的复数；所有显示的分母非零。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-I-26 · 按模 3 拆分

$$
(a;q)_{3n}=(a;q^3)_n(aq;q^3)_n(aq^2;q^3)_n
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-I-26`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-I-26**（Appendix I, (I.26), 印刷p352）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。n 为非负整数；q 为非零且非单位根的复数；所有显示的分母非零。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-I-28 · 正负参数合并

$$
(a^2;q^2)_n=(a;q)_n(-a;q)_n
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-I-28`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-I-28**（Appendix I, (I.28), 印刷p352）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。n 为非负整数；q 为非零且非单位根的复数；所有显示的分母非零。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-I-33 · 单位根参数的有限伸缩比

$$
\prod_{j=0}^{m-1}\frac{(qs\omega_m^j;q)_n}{(s\omega_m^j;q)_n}=\frac{(s^mq^m;q^m)_n}{(s^m;q^m)_n}=\frac{1-s^mq^{mn}}{1-s^m}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-I-33`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-I-33**（Appendix I, (I.33), 印刷p352）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。m≥1，s^m≠1。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-FINE-21.product · 根单位与分数底数的有限乘积重组

$$
\prod_{r=1}^p\prod_{j=0}^{k-1}(aq\zeta^j s^{r-1};q)_n=((aq)^k;s^k)_{np},\quad q=s^p,\quad\zeta=e^{2\pi i/k}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`FINE-21.product`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[FINE_supplement.md](../../round1_source_collection/records/FINE_supplement.md)；[FINE.md](../../round1_source_collection/books/FINE.md)。

- **FINE-21.product**（印刷页 31；(21.31) 之后、(21.32) 之前的无编号乘积）：q 为形式变量；数值代入要求所有实际分母非零，Gaussian 在奇点先作多项式延拓。空乘积为 1、空和为 0。n≥0，k,p≥1；a,s 为参数，所有幂使用同一 s。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
