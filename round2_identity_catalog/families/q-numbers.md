# q 数、阶乘与对称 q 数

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 本次未匹配到旧算法 2 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

**共享引擎适配已完成（2026-09-22）**：[第一版说明](../../finite_product_framework/docs/q_numbers.md)。两条目录公式的固定对数分支版本支持 Python 和 `qnumber_framework` tactic，生成框架保留 9 个待证义务。此记录指框架生成能力，下方旧实现匹配状态按原审计口径保留。

## FQI-SRC-GR2-1.2.47 · q 数阶乘与有限乘积转换

$$
[\alpha]_{q;n}=(1-q)^{-n}(q^\alpha;q)_n.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-1.2.47`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-1.2.47**（Chapter 1, 1.2.47, 印刷p7）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。q^α按固定分支；[α]_{q;n}=∏_{j=0}^{n−1}(1−q^{α+j})/(1−q)。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-1.2.55 · 对称 q 数阶乘转换

$$
\prod_{j=0}^{n-1}\frac{q^{(\alpha+j)/2}-q^{-(\alpha+j)/2}}{q^{1/2}-q^{-1/2}}=\frac{(q^\alpha;q)_n}{(1-q)^n}q^{n(1-\alpha)/2-n(n-1)/4}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-1.2.55`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-1.2.55**（Chapter 1, 1.2.55, 印刷p8）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。各分数幂按同一对数分支。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
