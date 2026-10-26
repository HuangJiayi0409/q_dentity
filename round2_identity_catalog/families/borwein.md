# Borwein A/B/C 多项式

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 本次未匹配到旧算法 7 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

## FQI-SRC-SILLS-4.51 · Borwein A 多项式的 Gaussian 展开

$$
\mathsf A_n(q)=\sum_{j=-n-1}^{n+1}(-1)^jq^{j(9j+1)/2}\begin{bmatrix}2n\\n+3j+0\end{bmatrix}_q.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`SILLS-4.51`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-4.51**（印刷页 136；4.51）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0；\mathsf A,B,C 由(q;q³)_n(q²;q³)_n=A_n(q³)−qB_n(q³)−q²C_n(q³)定义；区别于§4.3的B_n。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-4.52 · Borwein B 多项式的 Gaussian 展开

$$
\mathsf B_n(q)=\sum_{j=-n-1}^{n+1}(-1)^jq^{j(9j-5)/2}\begin{bmatrix}2n\\n+3j-1\end{bmatrix}_q.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`SILLS-4.52`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-4.52**（印刷页 136；4.52）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0；\mathsf A,B,C 由(q;q³)_n(q²;q³)_n=A_n(q³)−qB_n(q³)−q²C_n(q³)定义；区别于§4.3的B_n。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-4.53 · Borwein C 多项式的 Gaussian 展开

$$
\mathsf C_n(q)=\sum_{j=-n-1}^{n+1}(-1)^jq^{j(9j+7)/2}\begin{bmatrix}2n\\n+3j+1\end{bmatrix}_q.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`SILLS-4.53`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-4.53**（印刷页 136；4.53）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0；\mathsf A,B,C 由(q;q³)_n(q²;q³)_n=A_n(q³)−qB_n(q³)−q²C_n(q³)定义；区别于§4.3的B_n。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-4.54 · Borwein A 多项式的正向有限和

$$
\mathsf A_n(q)=\sum_{j=0}^{\lfloor n/3\rfloor}\frac{(q^3;q^3)_{n-j-1}(1-q^{2n})(q;q)_{3j}q^{3j^2}}{(q;q)_{n-3j}(q^3;q^3)_{2j}(q^3;q^3)_j}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`SILLS-4.54`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-4.54**（印刷页 136；4.54）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥1；n=0另设A₀=1。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-4.55 · Borwein B 多项式的正向有限和

$$
\mathsf B_n(q)=\sum_{j=0}^{\lfloor(n-1)/3\rfloor}\frac{(q^3;q^3)_{n-j-1}(1-q^{3j+2}-q^{n+3j+2}+q^{n+1})(q;q)_{3j}q^{3j^2+3j}}{(q;q)_{n-3j-1}(q^3;q^3)_{2j+1}(q^3;q^3)_j}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`SILLS-4.55`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-4.55**（印刷页 136；4.55）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥1；B₀=0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-4.56 · Borwein C 多项式的正向有限和

$$
\mathsf C_n(q)=\sum_{j=0}^{\lfloor(n-1)/3\rfloor}\frac{(q^3;q^3)_{n-j-1}(1-q^{3j+1}-q^{n+3j+2}+q^n)(q;q)_{3j}q^{3j^2+3j}}{(q;q)_{n-3j-1}(q^3;q^3)_{2j+1}(q^3;q^3)_j}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`SILLS-4.56`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-4.56**（印刷页 136；4.56）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥1；C₀=0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-4.Ex3 · Borwein 多项式的耦合递推

$$
\begin{aligned}\mathsf A_n&=(1+q^{2n-1})\mathsf A_{n-1}+q^n(\mathsf B_{n-1}+\mathsf C_{n-1}),\\\mathsf B_n&=(1+q^{2n-1})\mathsf B_{n-1}+q^{n-1}\mathsf A_{n-1}-q^n\mathsf C_{n-1},\\\mathsf C_n&=(1+q^{2n-1})\mathsf C_{n-1}+q^{n-1}(\mathsf A_{n-1}-\mathsf B_{n-1}).\end{aligned}
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`SILLS-4.Ex3`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-4.Ex3**（印刷页 137；4.Ex3）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥1；A₀=1，B₀=C₀=0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
