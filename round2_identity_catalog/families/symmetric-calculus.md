# 对称与一般量子差分、Taylor 基底

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 本次未匹配到旧算法 11 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

## FQI-SRC-KAC-CHEUNG-26.5 · 对称 q 导数乘法规则

$$
\widetilde D_q(fg)(x)=f(qx)\widetilde D_qg(x)+g(q^{-1}x)\widetilde D_qf(x)=f(q^{-1}x)\widetilde D_qg(x)+g(qx)\widetilde D_qf(x).
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`KAC-CHEUNG-26.5`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[KAC_CHEUNG_supplement.md](../../round1_source_collection/records/KAC_CHEUNG_supplement.md)；[KAC_CHEUNG.md](../../round1_source_collection/books/KAC_CHEUNG.md)。

- **KAC-CHEUNG-26.5**（印刷页 99；26.5）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。q²≠1；f,g为有理函数，x≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-KAC-CHEUNG-26.6 · 对称 q 导数商法则

$$
\widetilde D_q(f/g)(x)=\frac{g(q^{-1}x)\widetilde D_qf(x)-f(q^{-1}x)\widetilde D_qg(x)}{g(qx)g(q^{-1}x)}=\frac{g(qx)\widetilde D_qf(x)-f(qx)\widetilde D_qg(x)}{g(qx)g(q^{-1}x)}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`KAC-CHEUNG-26.6`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[KAC_CHEUNG_supplement.md](../../round1_source_collection/records/KAC_CHEUNG_supplement.md)；[KAC_CHEUNG.md](../../round1_source_collection/books/KAC_CHEUNG.md)。

- **KAC-CHEUNG-26.6**（印刷页 99；26.6）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。q²≠1；f,g为有理函数，xg(qx)g(q^{-1}x)≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-KAC-CHEUNG-26.7 · 对称 q 单项式导数

$$
\widetilde D_qx^n=\langle n\rangle_qx^{n-1}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`KAC-CHEUNG-26.7`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[KAC_CHEUNG_supplement.md](../../round1_source_collection/records/KAC_CHEUNG_supplement.md)；[KAC_CHEUNG.md](../../round1_source_collection/books/KAC_CHEUNG.md)。

- **KAC-CHEUNG-26.7**（印刷页 100；26.7）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。q²≠1，n≥0；n=0按0解释。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-KAC-CHEUNG-26.10 · 对称有限 q 幂的降阶导数

$$
\widetilde D_qS_n(x,a;q)=\langle n\rangle_qS_{n-1}(x,a;q).
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`KAC-CHEUNG-26.10`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[KAC_CHEUNG_supplement.md](../../round1_source_collection/records/KAC_CHEUNG_supplement.md)；[KAC_CHEUNG.md](../../round1_source_collection/books/KAC_CHEUNG.md)。

- **KAC-CHEUNG-26.10**（印刷页 100；26.10）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。q²≠1，n≥1。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-KAC-CHEUNG-26.12 · 对称有限 q 二项式定理

$$
S_n(x,-a;q)=\sum_{j=0}^n\left\langle{n\atop j}\right\rangle_q a^{n-j}x^j.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`KAC-CHEUNG-26.12`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[KAC_CHEUNG_supplement.md](../../round1_source_collection/records/KAC_CHEUNG_supplement.md)；[KAC_CHEUNG.md](../../round1_source_collection/books/KAC_CHEUNG.md)。

- **KAC-CHEUNG-26.12**（印刷页 100；26.12）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。q²≠1，n≥0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-KAC-CHEUNG-26.14 · 对称有限乘积的交换

$$
S_n(1,x;q)=(-1)^nS_n(x,1;q).
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`KAC-CHEUNG-26.14`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[KAC_CHEUNG_supplement.md](../../round1_source_collection/records/KAC_CHEUNG_supplement.md)；[KAC_CHEUNG.md](../../round1_source_collection/books/KAC_CHEUNG.md)。

- **KAC-CHEUNG-26.14**（印刷页 101；26.14）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。n≥0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-KAC-CHEUNG-26.15 · 对称有限乘积倒数的导数

$$
\widetilde D_q\frac1{S_n(1,x;q)}=\frac{\langle n\rangle_q}{S_{n+1}(1,x;q)}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`KAC-CHEUNG-26.15`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[KAC_CHEUNG_supplement.md](../../round1_source_collection/records/KAC_CHEUNG_supplement.md)；[KAC_CHEUNG.md](../../round1_source_collection/books/KAC_CHEUNG.md)。

- **KAC-CHEUNG-26.15**（印刷页 101；26.15）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。q²≠1，n≥0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-KAC-CHEUNG-26.21 · 一般量子 Taylor 多项式根和递推

$$
s_n=\frac{[n]_{q,r}}{[n-1]_{q,r}}s_{n-1}+\frac{n(q^{n-1}h-r^{n-1}h^{\prime})-[n]_{q,r}(h-h^{\prime})}{q^{n-1}-r^{n-1}}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`KAC-CHEUNG-26.21`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：一般量子差分、根和s_n及非嵌套Taylor基底T_n的定义见辅助说明。

定义文件：[KAC_CHEUNG_supplement.md](../../round1_source_collection/records/KAC_CHEUNG_supplement.md)；[KAC_CHEUNG.md](../../round1_source_collection/books/KAC_CHEUNG.md)。

- **KAC-CHEUNG-26.21**（印刷页 103；26.21）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。n≥2；q≠r，q^{n−1}≠r^{n−1}；所用[k]_{q,r}非零。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-KAC-CHEUNG-26.22 · 相同伸缩参数下的根和递推

$$
s_n=\frac{nq}{n-1}s_{n-1}+\frac{n(h+h^{\prime})}{2}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`KAC-CHEUNG-26.22`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：s_n为一般量子Taylor多项式T_n的根和；见辅助说明。

定义文件：[KAC_CHEUNG_supplement.md](../../round1_source_collection/records/KAC_CHEUNG_supplement.md)；[KAC_CHEUNG.md](../../round1_source_collection/books/KAC_CHEUNG.md)。

- **KAC-CHEUNG-26.22**（印刷页 103；26.22）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。n≥2；r=q≠0，h≠h′。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-KAC-CHEUNG-26.rootsum · 相同平移参数的根和有限解

$$
s_n=(a-h)[n]_{q,r}+h[n]_{q,r}\sum_{j=1}^n\frac{j}{[j]_{q,r}},\qquad s_1=a.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`KAC-CHEUNG-26.rootsum`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：s_n为一般量子Taylor多项式T_n的根和；见辅助说明。

定义文件：[KAC_CHEUNG_supplement.md](../../round1_source_collection/records/KAC_CHEUNG_supplement.md)；[KAC_CHEUNG.md](../../round1_source_collection/books/KAC_CHEUNG.md)。

- **KAC-CHEUNG-26.rootsum**（印刷页 103；26.rootsum）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。n≥1；h′=h，q≠r；所用[j]_{q,r}非零。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-KAC-CHEUNG-26.23 · 对称q-Taylor基底的正确有限构造

$$
T_0(x)=1,\qquad T_n(x)=\frac{x^n}{\langle n\rangle_q!}-\sum_{k=0}^{n-1}\frac{a^{n-k}}{\langle n-k\rangle_q!}T_k(x),\qquad\widetilde D_qT_n=T_{n-1},\quad T_n(a)=0\ (n\ge1).
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`KAC-CHEUNG-26.23`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[KAC_CHEUNG_supplement.md](../../round1_source_collection/records/KAC_CHEUNG_supplement.md)；[KAC_CHEUNG.md](../../round1_source_collection/books/KAC_CHEUNG.md)。

- **KAC-CHEUNG-26.23**（p104, (26.23)的替代构造；边界见p103）：n≥0；d_j=⟨j⟩_q=(q^j−q^{-j})/(q−q^{-1})，d₀!=1，d_j!=∏_{i=1}^j d_i；q≠0,±1且d_1,…,d_n≠0。D̃_qf=(f(qx)−f(q^{-1}x))/((q−q^{-1})x)，x=0按多项式延拓。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
