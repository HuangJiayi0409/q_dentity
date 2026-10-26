# Cayley 有限有理分解

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 本次未匹配到旧算法 1 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

## FQI-CAYLEY · Cayley 有限有理分解

$$
\frac1{(q;q)_n}=\sum_{\substack{p_1,\ldots,p_n\ge0\\\sum_{j=1}^n jp_j=n}}\prod_{j=1}^n\frac1{j^{p_j}p_j!(1-q^j)^{p_j}}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AP-5.CAYLEY`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_P_supplement.md](../../round1_source_collection/records/ANDREWS_P_supplement.md)；[ANDREWS_P.md](../../round1_source_collection/books/ANDREWS_P.md)。

- **AP-5.CAYLEY**（p.81, Examples 1–2 后的 Cayley general decomposition）：n≥0；有理函数域 Q(q)；n=0 时空指标项为1。
  对应：代表式；保留本条来源域。
- **AP-12.E1**（p.209, Example 1）：n≥0；有理函数域 Q(q)；n=0 时空指标项为1。
  对应：公式、定义与条件逐字相同；仅书内定位不同。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
