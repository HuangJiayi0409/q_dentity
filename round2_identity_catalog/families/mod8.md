# Mod 8、q-Pell 与 Ramanujan–Slater

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 本次未匹配到旧算法 2 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

## FQI-SRC-SILLS-4.47 · Mod 8 的 q-Pell 多项式递推

$$
P_n=(1+q^{2n-1})P_{n-1}+q^{2n-2}P_{n-2},\quad P_0=1,\ P_1=1+q.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`SILLS-4.47`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：P_n=\sum_{j=0}^n\sum_{k=0}^{\min(j,n-j)}q^{j^2+k^2}{j\brack k}_{q^2}{n-k\brack j}_{q^2}.

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-4.47**（印刷页 134；4.47）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥2。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-4.Mod8 · 有限 Ramanujan–Slater Mod 8 恒等式

$$
\sum_{j=0}^n\sum_{k=0}^{\min(j,n-j)}q^{j^2+k^2}\begin{bmatrix}j\\k\end{bmatrix}_{q^2}\begin{bmatrix}n-k\\j\end{bmatrix}_{q^2}=\sum_{j=-n-1}^{n+1}(-1)^jq^{4j^2+j}\bigl(T_0(n,4j;q)+T_0(n,4j+1;q)\bigr).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`SILLS-4.Mod8`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-4.Mod8**（印刷页 135；4.Mod8）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0；T₀见辅助定义。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
