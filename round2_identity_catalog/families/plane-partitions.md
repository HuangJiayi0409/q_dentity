# 平面分拆、行列式与盒内乘积

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 本次未匹配到旧算法 6 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

## FQI-SRC-AP-11.2.1 · 固定首列平面分拆的有限递推

$$
\pi_{r+1}(n_1,\ldots,n_k;q)=q^{n_1+\cdots+n_k}\sum_{\substack{n_i\ge m_i\ge0\ (1\le i\le k)\\m_1\ge\cdots\ge m_k}}\pi_r(m_1,\ldots,m_k;q).
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`AP-11.2.1`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：π_r(n₁,…,n_k;q) 按体积计平面分拆：至多 k 行、r 列，第 i 行首项恰为 n_i（允许补零）。Π_{k,r}(n;q) 按体积计 k×r 矩形内、所有项≤n 的平面分拆。原书后者也用 π，此处改大写 Π 以区分。

定义文件：[ANDREWS_P_supplement.md](../../round1_source_collection/records/ANDREWS_P_supplement.md)；[ANDREWS_P.md](../../round1_source_collection/books/ANDREWS_P.md)。

- **AP-11.2.1**（p.180, (11.2.1)）：k,r≥1；n₁≥…≥n_k≥0 为整数。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AP-11.2.4 · Carlitz 固定首列行列式

$$
\pi_r(n_1,\ldots,n_k;q)=q^{n_1+\cdots+n_k}\det\left(q^{(i-j)(i-j-1)/2}\begin{bmatrix}n_j+r-1\\r-i+j-1\end{bmatrix}_{q}\right)_{1\le i,j\le k}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AP-11.2.4`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：π_r(n₁,…,n_k;q) 按体积计平面分拆：至多 k 行、r 列，第 i 行首项恰为 n_i（允许补零）。Π_{k,r}(n;q) 按体积计 k×r 矩形内、所有项≤n 的平面分拆。原书后者也用 π，此处改大写 Π 以区分。

定义文件：[ANDREWS_P_supplement.md](../../round1_source_collection/records/ANDREWS_P_supplement.md)；[ANDREWS_P.md](../../round1_source_collection/books/ANDREWS_P.md)。

- **AP-11.2.4**（p.181, Theorem 11.1, (11.2.4)）：k,r≥1；n₁≥…≥n_k≥0 为整数。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AP-11.2.9 · 盒内平面分拆行列式

$$
\Pi_{k,r}(n;q)=\det\left(q^{(i-j)(i-j-1)/2}\begin{bmatrix}n+r\\r-i+j\end{bmatrix}_{q}\right)_{1\le i,j\le k}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AP-11.2.9`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：π_r(n₁,…,n_k;q) 按体积计平面分拆：至多 k 行、r 列，第 i 行首项恰为 n_i（允许补零）。Π_{k,r}(n;q) 按体积计 k×r 矩形内、所有项≤n 的平面分拆。原书后者也用 π，此处改大写 Π 以区分。

定义文件：[ANDREWS_P_supplement.md](../../round1_source_collection/records/ANDREWS_P_supplement.md)；[ANDREWS_P.md](../../round1_source_collection/books/ANDREWS_P.md)。

- **AP-11.2.9**（p.183, (11.2.9)）：k,r≥1；n≥0 为整数。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AP-11.2.10 · MacMahon 盒内平面分拆有限乘积

$$
\Pi_{k,r}(n;q)=\prod_{j=0}^{k-1}\frac{(q;q)_j(q;q)_{n+r+j}}{(q;q)_{r+j}(q;q)_{n+j}}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AP-11.2.10`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：π_r(n₁,…,n_k;q) 按体积计平面分拆：至多 k 行、r 列，第 i 行首项恰为 n_i（允许补零）。Π_{k,r}(n;q) 按体积计 k×r 矩形内、所有项≤n 的平面分拆。原书后者也用 π，此处改大写 Π 以区分。

定义文件：[ANDREWS_P_supplement.md](../../round1_source_collection/records/ANDREWS_P_supplement.md)；[ANDREWS_P.md](../../round1_source_collection/books/ANDREWS_P.md)。

- **AP-11.2.10**（p.183, Theorem 11.2, (11.2.10)）：k,r≥1；n≥0 为整数；乘积商按有理函数解释，约去后为多项式。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AP-11.2.2 · 固定首列平面分拆的初值

$$
\pi_1(n_1,\ldots,n_k;q)=q^{n_1+\cdots+n_k}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`AP-11.2.2`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：π_r(n₁,…,n_k;q) 按体积计平面分拆：至多 k 行、r 列，第 i 行首项恰为 n_i（允许补零）。Π_{k,r}(n;q) 按体积计 k×r 矩形内、所有项≤n 的平面分拆。原书后者也用 π，此处改大写 Π 以区分。

定义文件：[ANDREWS_P_supplement.md](../../round1_source_collection/records/ANDREWS_P_supplement.md)；[ANDREWS_P.md](../../round1_source_collection/books/ANDREWS_P.md)。

- **AP-11.2.2**（p.180, (11.2.2)）：k≥1，n₁≥…≥n_k≥0 为整数。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AP-11.2.8 · 固定首列与盒内平面分拆的有限求和关系

$$
\Pi_{k,r}(n;q)=\sum_{n\ge n_1\ge\cdots\ge n_k\ge0}\pi_r(n_1,\ldots,n_k;q)=q^{-kn}\pi_{r+1}(\underbrace{n,\ldots,n}_{k};q).
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`AP-11.2.8`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：π_r(n₁,…,n_k;q) 按体积计平面分拆：至多 k 行、r 列，第 i 行首项恰为 n_i（允许补零）。Π_{k,r}(n;q) 按体积计 k×r 矩形内、所有项≤n 的平面分拆。原书后者也用 π，此处改大写 Π 以区分。

定义文件：[ANDREWS_P_supplement.md](../../round1_source_collection/records/ANDREWS_P_supplement.md)；[ANDREWS_P.md](../../round1_source_collection/books/ANDREWS_P.md)。

- **AP-11.2.8**（p.183, (11.2.8)）：k,r≥1，n≥0 为整数；末式在 Laurent 多项式环中解释。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
