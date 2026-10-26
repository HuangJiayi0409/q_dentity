# Andrews–Baxter q-三项式

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 本次未匹配到旧算法 8 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

## FQI-SRC-SILLS-1.87 · Andrews–Baxter q-三项式递推

$$
C_n(j;q)=q^{n+j}C_{n-1}(j+1;q)+C_{n-1}(j;q)+q^{n-j}C_{n-1}(j-1;q)+q^{n-1}(1-q^{n-1})C_{n-2}(j;q).
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`SILLS-1.87`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：C_n(j;q)=\sum_{k=0}^nq^{k(k+j)}{n\brack k}_q{n-k\brack k+j}_q\quad\text{(1.86)}.

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-1.87**（印刷页 43；1.87）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥2；n=1时最后项按0解释。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-1.90 · q-三项式 Laurent 多项式递推

$$
\mathcal T_n(x,q)=(1+xq^{3n-2}+x^{-1}q^{3n-1})\mathcal T_{n-1}(x,q)+q^{3n-3}(1-q^{3n-3})\mathcal T_{n-2}(x,q).
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`SILLS-1.90`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：\mathcal T_n(x,q)=\sum_{j=-n}^nx^jq^{j(3j-1)/2}C_n(j;q^3).

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-1.90**（印刷页 44；1.90）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥2，x≠0；T₀=1，T₁=1+xq+x⁻¹q²。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-2.75 · Schur 有界分拆的有限 q-三项式恒等式

$$
S_{3n-1}(x,q)=\sum_{j=-n}^nx^jq^{j(3j-1)/2}C_n(j;q^3).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`SILLS-2.75`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：S_N=\sum_\lambda x^{h(\lambda)}q^{|\lambda|}，λ为最大部件≤N、相邻差≥3、不能有相邻的3倍数的分拆；h=#(部件≡1 mod3)−#(部件≡2 mod3)。

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-2.75**（印刷页 78；2.75）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0，x≠0，S₋₁=1。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-4.18 · D 多项式的 q-三项式展开

$$
D_n=\sum_{k=-n-2}^{n+2}\left(q^{10k^2+k}C_n(5k;q)-q^{10k^2-9k+2}C_n(5k-2;q)\right).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`SILLS-4.18`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-4.18**（印刷页 124；4.18）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0；D_n见(4.8)，C_n见(1.86)。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-4.19 · E 多项式的 q-三项式展开

$$
E_{n-1}=\sum_{k=-n-2}^{n+2}\left(q^{10k^2+3k}C_n(5k+1;q)-q^{10k^2-7k+1}C_n(5k-2;q)\right).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`SILLS-4.19`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-4.19**（印刷页 124；4.19）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥1；E_n见(4.16)。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-4.48 · T₁ 与 T₀ 的 q-三项式递推

$$
T_1(n,j;q)=T_1(n-1,j;q)+q^{n+j}T_0(n-1,j+1;q)+q^{n-j}T_0(n-1,j-1;q).
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`SILLS-4.48`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-4.48**（印刷页 135；4.48）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥1。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-4.49 · T₀ 与 T₁ 的 q-三项式递推

$$
T_0(n,j;q)=T_0(n-1,j-1;q)+q^{n+j}T_1(n-1,j;q)+q^{2n+2j}T_0(n-1,j+1;q).
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`SILLS-4.49`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-4.49**（印刷页 135；4.49）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥1。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-4.50 · T₀、T₁ 的相邻指标关系

$$
T_1(n,j;q)-q^{n-j}T_0(n,j;q)-T_1(n,j+1;q)+q^{n+j+1}T_0(n,j+1;q)=0.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`SILLS-4.50`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-4.50**（印刷页 135；4.50）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
