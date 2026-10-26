# 有限 q-二项式及 q-交换二项式

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 已有自动证明流程（旧条件域） 1 条；本次未匹配到旧算法 5 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

**有限 q-二项式旧路线适配已完成（2026-09-22，仅本家族 1 条）**：[适配说明](../../finite_product_framework/docs/q_binomial.md)。FQI-FINITE-Q-BINOMIAL 支持受限 statement、Python 与 `qbinomial_framework`；默认调用 Maple/qEKHAD 搜索并检查 q-WZ 证书，框架保留 3 个核心义务，另可复用迁入的完整旧证明。显式 replay 保留为离线模式；实时搜索失败时直接报错、不回退。其余五条已另行完成[结构化扩展](../../finite_product_framework/docs/q_binomial_structure.md)，使用 `qbinomial_structure`，不调用 CAS：四条框架共 18 个局部义务，算子交换生成证明已闭合；多项式 Gaussian 与旧商式之间的 Lean 桥接不在本轮完成范围。下方旧审计统计不变。

## FQI-FINITE-Q-BINOMIAL · 有限 q-二项式定理

$$
\sum_{k=0}^n(-1)^kz^kq^{k(k-1)/2}\begin{bmatrix}n\\k\end{bmatrix}_q=(z;q)_n.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`SILLS-1.56`。

**证明算法状态：已有自动证明流程（旧条件域）**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-FINITE-Q-BINOMIAL)

方法：一阶 q-WZ：移动上界、证书、望远镜及归纳。

覆盖边界：旧定理要求 i∈range(n+1) 时 q^(i+1)≠1；目录各来源还涉及多项式延拓，延拓域须另接。

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-1.56**（印刷页 35；1.56）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0。
  对应：代表式；保留本条来源域。
- **AP-3.3.6**（p.36, Theorem 3.3, (3.3.6)）：N≥0 为整数；z,q 为形式变量。
  对应：N→n，j→k，交换等号两侧。
- **FINE-6.23**（印刷页 5；式 (6.23)）：q 为形式变量；数值代入要求所有实际分母非零，Gaussian 在奇点先作多项式延拓。空乘积为 1、空和为 0。N≥0 为整数；t、q 为参数。
  对应：z=tq；q≠0 时可逆代换；q=0 的原式单独按多项式解释。
- **GR2-II-04**（Appendix II, (II.4), 印刷p354）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。n 为非负整数；q 为非零且非单位根的复数；所有显示的分母非零。
  对应：展开有限 1φ0 并用 (q^−n;q)_k/(q;q)_k=(−1)^k q^{k(k−1)/2−nk}[n choose k]_q；令原 z=q^n z。
- **KAC-CHEUNG-5.5**（印刷页 15；5.5）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。n≥0。
  对应：P_n(x,−a;q)=x^n(−a/x;q)_n；取 z=−a/x 后乘 x^n，x=0 由多项式恒等式延拓。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AP-13.E3 · 三变量 q-下降乘积卷积

$$
\prod_{i=0}^{n-1}(X-Zq^i)=\sum_{k=0}^n \begin{bmatrix}n\\k\end{bmatrix}_{q}\prod_{j=0}^{k-1}(Y-Zq^j)\prod_{h=0}^{n-k-1}(X-Yq^h).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AP-13.E3`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_P_supplement.md](../../round1_source_collection/records/ANDREWS_P_supplement.md)；[ANDREWS_P.md](../../round1_source_collection/books/ANDREWS_P.md)。

- **AP-13.E3**（p.225, Example 3）：n≥0 为整数；X,Y,Z,q 为形式变量。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AP-13.E5 · q-下降阶乘基上的线性泛函

$$
L(X^n)=\sum_{k=0}^n \begin{bmatrix}n\\k\end{bmatrix}_{q}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AP-13.E5`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：上述首一多项式逐次数构成一组基，故条件唯一确定 L。

定义文件：[ANDREWS_P_supplement.md](../../round1_source_collection/records/ANDREWS_P_supplement.md)；[ANDREWS_P.md](../../round1_source_collection/books/ANDREWS_P.md)。

- **AP-13.E5**（p.225, Example 5）：n≥0；固定 q；L 为线性泛函，满足所有 j≥0 时 L(∏_{i=0}^{j−1}(X−q^i))=1。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-KAC-CHEUNG-4.4 · 单项式的有限 q 幂展开

$$
x^n=\sum_{j=0}^n\begin{bmatrix}n\\j\end{bmatrix}_qP_j(x,1;q).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`KAC-CHEUNG-4.4`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[KAC_CHEUNG_supplement.md](../../round1_source_collection/records/KAC_CHEUNG_supplement.md)；[KAC_CHEUNG.md](../../round1_source_collection/books/KAC_CHEUNG.md)。

- **KAC-CHEUNG-4.4**（印刷页 12；4.4）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。n≥0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-KAC-CHEUNG-5.7 · 乘法算子和 q 移位的交换

$$
M_qX=qXM_q,\qquad (Xf)(x)=xf(x),\quad(M_qf)(x)=f(qx).
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`KAC-CHEUNG-5.7`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[KAC_CHEUNG_supplement.md](../../round1_source_collection/records/KAC_CHEUNG_supplement.md)；[KAC_CHEUNG.md](../../round1_source_collection/books/KAC_CHEUNG.md)。

- **KAC-CHEUNG-5.7**（印刷页 15；5.7）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。作用于多项式。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-KAC-CHEUNG-5.8 · q 交换算子的有限二项式定理

$$
(X+Y)^n=\sum_{j=0}^n\begin{bmatrix}n\\j\end{bmatrix}_qX^jY^{n-j},\qquad YX=qXY.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`KAC-CHEUNG-5.8`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[KAC_CHEUNG_supplement.md](../../round1_source_collection/records/KAC_CHEUNG_supplement.md)；[KAC_CHEUNG.md](../../round1_source_collection/books/KAC_CHEUNG.md)。

- **KAC-CHEUNG-5.8**（印刷页 15；5.8）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。n≥0；含单位元的结合代数。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
