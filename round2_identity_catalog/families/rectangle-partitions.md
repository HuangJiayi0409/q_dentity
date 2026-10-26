# 矩形分拆与有限生成多项式

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 本次未匹配到旧算法 4 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

## FQI-RECTANGLE-PARTITIONS · 矩形分拆的 Gaussian 生成多项式

$$
\begin{bmatrix}n\\k\end{bmatrix}_q=\sum_{\substack{n-k\ge\lambda_1\ge\cdots\ge\lambda_k\ge0}}q^{\lambda_1+\cdots+\lambda_k}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-1.NoteEx2-partition`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-1.NoteEx2-partition**（Chapter 1, 1.NoteEx2-partition, 印刷p35）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。0≤k≤n；零部件只用于补齐长度。
  对应：代表式；保留本条来源域。
- **AP-3.2.1**（p.33, Theorem 3.1, (3.2.1)）：N,M 为非负整数；q 为形式变量。
  对应：n=N+M，k=M；补零到恰 M 个部分，按大小 s 分组。
- **SILLS-1.Thm1.53**（印刷页 34；1.Thm1.53）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。k,ℓ≥0；p计数部件≤k且长度≤ℓ的分拆。
  对应：n=k+ℓ；按分拆大小 r 分组；矩形共轭允许交换边长。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AP-3.2.7 · 受限分拆递推

$$
G(N,M;q)-G(N,M-1;q)=q^M G(N-1,M;q).
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`AP-3.2.7`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：G 同 AP-3.2.1。

定义文件：[ANDREWS_P_supplement.md](../../round1_source_collection/records/ANDREWS_P_supplement.md)；[ANDREWS_P.md](../../round1_source_collection/books/ANDREWS_P.md)。

- **AP-3.2.7**（p.34, (3.2.7)）：N,M≥1 为整数。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AP-4.2.COMPOSITIONS · 有界有序组成的有限生成多项式

$$
\sum_{n=M}^{MN}c(N,M,n)q^n=\left(\sum_{j=1}^{N}q^j\right)^M.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AP-4.2.COMPOSITIONS`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：c(N,M,n)=#{(a₁,…,a_M)∈{1,…,N}^M : a₁+⋯+a_M=n}，计数有序组成，不是无序分拆。

定义文件：[ANDREWS_P_supplement.md](../../round1_source_collection/records/ANDREWS_P_supplement.md)；[ANDREWS_P.md](../../round1_source_collection/books/ANDREWS_P.md)。

- **AP-4.2.COMPOSITIONS**（p.55, Theorem 4.2 证明，无编号等式）：N,M≥1 为整数；q 为形式变量。等式为整系数多项式恒等式，也可在任意复数 q（包括0、1及单位根）处求值。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-1.ExDistinct · 有界不同部件分拆的有限生成多项式

$$
\sum_{r=0}^{j(j+1)/2}\sum_{\ell=0}^jQ(j,\ell,r)z^\ell q^r=(-zq;q)_j.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`SILLS-1.ExDistinct`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-1.ExDistinct**（印刷页 51；1.ExDistinct）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。j≥0；Q计数恰有ℓ个不同正部件、各≤j、总和r的分拆。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
