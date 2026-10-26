# Gaussian 对称、递推与互反

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 已有 Lean 证明实现（旧条件域） 5 条；已有可复用部件，待组装 1 条；本次未匹配到旧算法 7 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

**第一版框架算法已完成（2026-09-22）**：[算法与条件域](../../finite_product_framework/docs/gaussian.md)。13 条目录公式在固定分支、非单位根条件域对应 17 个目标，支持 Python 和 `gaussian_framework` tactic；生成框架保留 66 个开放义务。包含乘积代数及两类归纳框架，不表示完整形式化证明或多项式延拓域已覆盖。下方旧实现匹配状态按原审计口径保留。

## FQI-GAUSSIAN-SYMMETRY · Gaussian 对称性

$$
\begin{bmatrix}n\\k\end{bmatrix}_q=\begin{bmatrix}n\\n-k\end{bmatrix}_q.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-I-39`。

**证明算法状态：已有 Lean 证明实现（旧条件域）**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-GAUSSIAN-SYMMETRY)

方法：Gaussian 定义展开、阶乘递推与代数归一化。

覆盖边界：旧 qBinom 是有分母定义；Pascal 主引理要求 0<k，k=0 需端点引理。多项式延拓域不可只由除法定义推出。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-I-39**（Appendix I, (I.39), 印刷p353）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。0≤k≤n。
  对应：代表式；保留本条来源域。
- **AP-3.3.2**（p.35, Theorem 3.2, (3.3.2)）：0≤m≤n，均为整数；Gaussian 下指标越界为零。
  对应：m→k。
- **SILLS-1.49**（印刷页 33；1.49）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0。
  对应：逐项相同。
- **KAC-CHEUNG-6.1**（印刷页 17；6.1）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。n≥0，j∈Z。
  对应：j→k；越界采用普通 Gaussian 零延拓。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-PASCAL-Q-N-K · Gaussian Pascal：权 q^(n−k)

$$
\begin{bmatrix}n\\k\end{bmatrix}_q=\begin{bmatrix}n-1\\k\end{bmatrix}_q+q^{n-k}\begin{bmatrix}n-1\\k-1\end{bmatrix}_q.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`SILLS-1.50`。

**证明算法状态：已有 Lean 证明实现（旧条件域）**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-PASCAL-Q-N-K)

方法：Gaussian 定义展开、阶乘递推与代数归一化。

覆盖边界：旧 qBinom 是有分母定义；Pascal 主引理要求 0<k，k=0 需端点引理。多项式延拓域不可只由除法定义推出。

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-1.50**（印刷页 33；1.50）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥1，0≤k≤n。
  对应：代表式；保留本条来源域。
- **AP-3.3.3**（p.35, Theorem 3.2, (3.3.3)）：n≥1，0≤m≤n，均为整数；Gaussian 下指标越界为零。
  对应：m→k。
- **AQ-3.8**（印刷页 22；式 (3.8)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 A≥1，0≤B≤A。
  对应：A→n，B→k。
- **KAC-CHEUNG-6.3**（印刷页 17；6.3）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。n≥1，0≤j≤n。
  对应：j→k；注意本书称第二递推。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-PASCAL-Q-K · Gaussian Pascal：权 q^k

$$
\begin{bmatrix}n\\k\end{bmatrix}_q=q^k\begin{bmatrix}n-1\\k\end{bmatrix}_q+\begin{bmatrix}n-1\\k-1\end{bmatrix}_q.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`SILLS-1.51`。

**证明算法状态：已有 Lean 证明实现（旧条件域）**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-PASCAL-Q-K)

方法：Gaussian 定义展开、阶乘递推与代数归一化。

覆盖边界：旧 qBinom 是有分母定义；Pascal 主引理要求 0<k，k=0 需端点引理。多项式延拓域不可只由除法定义推出。

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-1.51**（印刷页 33；1.51）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥1，0≤k≤n。
  对应：代表式；保留本条来源域。
- **AP-3.3.4**（p.35, Theorem 3.2, (3.3.4)）：n≥1，0≤m≤n，均为整数；Gaussian 下指标越界为零。
  对应：m→k，交换右侧两项次序。
- **AQ-3.9**（印刷页 22；式 (3.9)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 A≥1，0≤B≤A。
  对应：A→n，B→k，交换右侧两项次序。
- **KAC-CHEUNG-6.2**（印刷页 17；6.2）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。n≥1，0≤j≤n。
  对应：j→k；注意本书称第一递推。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-GAUSSIAN-RECIPROCITY · 普通 Gaussian 倒底数

$$
\begin{bmatrix}n\\k\end{bmatrix}_{1/q}=q^{k(k-n)}\begin{bmatrix}n\\k\end{bmatrix}_q.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`SILLS-1.53`。

**证明算法状态：已有 Lean 证明实现（旧条件域）**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-GAUSSIAN-RECIPROCITY)

方法：Gaussian 定义展开、阶乘递推与代数归一化。

覆盖边界：旧 qBinom 是有分母定义；Pascal 主引理要求 0<k，k=0 需端点引理。多项式延拓域不可只由除法定义推出。

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-1.53**（印刷页 34；1.53）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0，0≤k≤n。
  对应：代表式；保留本条来源域。
- **KAC-CHEUNG-6.reciprocity**（印刷页 19；6.reciprocity）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。n≥0，0≤j≤n。
  对应：j→k；−j(n−j)=j(j−n)。
- **AP-3.5.RECIP**（p.47, Theorem 3.10 证明，跨 pp.47–48）：N,M≥0 为整数；在 Laurent 多项式环中写出，整理后为多项式等式。
  对应：展开 G(N,M;q)=[N+M choose M]_q，n=N+M，k=M；NM=k(n−k)。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-I-42 · Gaussian 的终止参数表示

$$
\begin{bmatrix}n\\k\end{bmatrix}_q=(-q^n)^kq^{-k(k-1)/2}\frac{(q^{-n};q)_k}{(q;q)_k}
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-I-42`。

**证明算法状态：已有可复用部件，待组装**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SRC-GR2-I-42)

方法：终止参数反射与 Gaussian 定义。

覆盖边界：未找到相同最终签名；终止参数桥接尚未写。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-I-42**（Appendix I, (I.42), 印刷p353）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。n 为非负整数；q 为非零且非单位根的复数；所有显示的分母非零。 k 为整数且 0≤k≤n；取作者参数 a=n。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-I-43 · 移位上指标的有限乘积

$$
\begin{bmatrix}k+\alpha\\k\end{bmatrix}_q=\frac{(q^{\alpha+1};q)_k}{(q;q)_k}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-I-43`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-I-43**（Appendix I, (I.43), 印刷p353）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。k≥0；q^α按固定对数分支；左侧按有限整数下指标定义。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-I-44 · Gaussian 负上指标转换

$$
\begin{bmatrix}-\alpha\\k\end{bmatrix}_q=\begin{bmatrix}\alpha+k-1\\k\end{bmatrix}_q(-q^{-\alpha})^kq^{-k(k-1)/2}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-I-44`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-I-44**（Appendix I, (I.44), 印刷p353）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。k≥0；q^α按固定分支；上下两侧均为有限乘积定义。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-I-45 · 一般上指标的两种 q-Pascal 递推

$$
\begin{bmatrix}\alpha+1\\k\end{bmatrix}_q=q^k\begin{bmatrix}\alpha\\k\end{bmatrix}_q+\begin{bmatrix}\alpha\\k-1\end{bmatrix}_q=\begin{bmatrix}\alpha\\k\end{bmatrix}_q+q^{\alpha+1-k}\begin{bmatrix}\alpha\\k-1\end{bmatrix}_q.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-I-45`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-I-45**（Appendix I, (I.45), 印刷p353）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。k≥0，整数下指标−1定义为0；q^α固定分支。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-I-46 · 移位上指标的互补下指标

$$
\begin{bmatrix}n+\alpha\\n-k\end{bmatrix}_q=\frac{(q^{\alpha+1};q)_n}{(q;q)_{n-k}(q^{\alpha+1};q)_k}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-I-46`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-I-46**（Appendix I, (I.46), 印刷p353）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。0≤k≤n；q^α固定分支。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-I-47 · 一般上指标的 Gaussian 倒底数

$$
\begin{bmatrix}\alpha\\k\end{bmatrix}_{q^{-1}}=q^{k^2-\alpha k}\begin{bmatrix}\alpha\\k\end{bmatrix}_q.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-I-47`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-I-47**（Appendix I, (I.47), 印刷p353）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。k≥0；q^α固定分支，倒底数取相容的q^{-α}。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AP-3.3.1 · Gaussian 端点

$$
\begin{bmatrix}n\\0\end{bmatrix}_{q}=\begin{bmatrix}n\\n\end{bmatrix}_{q}=1.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`AP-3.3.1`。

**证明算法状态：已有 Lean 证明实现（旧条件域）**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SRC-AP-3.3.1)

方法：Gaussian 定义展开、阶乘递推与代数归一化。

覆盖边界：旧 qBinom 是有分母定义；Pascal 主引理要求 0<k，k=0 需端点引理。多项式延拓域不可只由除法定义推出。

定义文件：[ANDREWS_P_supplement.md](../../round1_source_collection/records/ANDREWS_P_supplement.md)；[ANDREWS_P.md](../../round1_source_collection/books/ANDREWS_P.md)。

- **AP-3.3.1**（p.35, Theorem 3.2, (3.3.1)）：n≥0，均为整数；Gaussian 下指标越界为零。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AP-3.3.9 · Gaussian 加权 hockey-stick 求和

$$
\begin{bmatrix}n+m+1\\m+1\end{bmatrix}_{q}=\sum_{j=0}^n q^j\begin{bmatrix}m+j\\m\end{bmatrix}_{q}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AP-3.3.9`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_P_supplement.md](../../round1_source_collection/records/ANDREWS_P_supplement.md)；[ANDREWS_P.md](../../round1_source_collection/books/ANDREWS_P.md)。

- **AP-3.3.9**（p.37, Theorem 3.4, (3.3.9)）：m,n≥0 为整数。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-KAC-CHEUNG-6.5 · Gaussian 的加权子集表示

$$
\begin{bmatrix}n\\j\end{bmatrix}_q=\sum_{\substack{S\subseteq\{1,\ldots,n\}\\|S|=j}}q^{\sum_{s\in S}s-j(j+1)/2}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`KAC-CHEUNG-6.5`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[KAC_CHEUNG_supplement.md](../../round1_source_collection/records/KAC_CHEUNG_supplement.md)；[KAC_CHEUNG.md](../../round1_source_collection/books/KAC_CHEUNG.md)。

- **KAC-CHEUNG-6.5**（印刷页 19；6.5）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。n≥0，0≤j≤n。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
