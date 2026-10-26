# 有限 Jacobi/五重乘积

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 已有自动证明流程（旧条件域） 1 条；已有可复用部件，待组装 1 条；仅相关路线，未覆盖本式 2 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

## FQI-SRC-AP-3.E1 · 有限 Jacobi 三重积

$$
\sum_{j=-n}^n q^{j^2}x^j\begin{bmatrix}2n\\n+j\end{bmatrix}_{q^2}=(-x^{-1}q;q^2)_n(-xq;q^2)_n.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AP-3.E1`。

**证明算法状态：已有可复用部件，待组装**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SRC-AP-3.E1)

方法：有限 JTP 的平方底数特化。

覆盖边界：代换明确，但未找到旧库已写出的平方底数包装；Generic 的特化义务未关闭。

定义文件：[ANDREWS_P_supplement.md](../../round1_source_collection/records/ANDREWS_P_supplement.md)；[ANDREWS_P.md](../../round1_source_collection/books/ANDREWS_P.md)。

- **AP-3.E1**（p.49, Example 1）：n≥0 为整数；x 可逆。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-1.JacobiFinite · Jacobi 乘积证明中的有限双边二项式

$$
(q/x,x;q)_m=\sum_{j=-m}^m(-1)^jq^{j(j-1)/2}x^j\begin{bmatrix}2m\\m+j\end{bmatrix}_q.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`SILLS-1.JacobiFinite`。

**证明算法状态：已有自动证明流程（旧条件域）**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SRC-SILLS-1.JacobiFinite)

方法：仿射上界 2n 的有限 theta q-WZ。

覆盖边界：旧定理使用 Generic 和对所有递推层成立的非零条件；比目录仅要求当前有限式分母非零更强。尚未证明目录全部条件能推出这些假设。

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-1.JacobiFinite**（印刷页 36；1.JacobiFinite）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。m≥0，x≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-1.75 · Paule 有限五重乘积恒等式

$$
\sum_{k=-n}^{n}\frac{(-1)^kq^{k(3k+1)/2}x^{3k}\begin{bmatrix}2n\\n+k\end{bmatrix}_q(1-x^2q^{2k+1})}{(x^2q^2;q)_{n+k}(x^{-2};q)_{n-k}}=\frac{1-x^2q}{(xq,x^{-1};q)_n}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`SILLS-1.75`。

**证明算法状态：仅相关路线，未覆盖本式**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SRC-SILLS-1.75)

方法：旧五重积多块链仅作相关路线。

覆盖边界：有限化不同；最终无限五重积相同不意味着有限式相同。

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-1.75**（印刷页 39；1.75）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0，x≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-1.75-rec · 有限五重乘积和的一阶递推

$$
f_n=\frac{f_{n-1}}{(1-q^{n-1}/x)(1-xq^n)},\quad f_0=1-x^2q.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`SILLS-1.75-rec`。

**证明算法状态：仅相关路线，未覆盖本式**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SRC-SILLS-1.75-rec)

方法：旧五重积多块链仅作相关路线。

覆盖边界：有限化不同；最终无限五重积相同不意味着有限式相同。

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-1.75-rec**（印刷页 39；1.75-rec）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥1，f_n是(1.75)左侧。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
