# 多变量 A/D 型终止求和与变换

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 本次未匹配到旧算法 5 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

## FQI-SRC-GR2-11.7.1 · Milne 的多变量有限 q 求和

$$
\sum_{\substack{k_1,\ldots,k_d\ge0\\|k|=N}}\frac{\Delta(zq^k)}{\Delta(z)}\prod_{r,s=1}^d\frac{(a_rz_s/z_r;q)_{k_s}}{(qz_s/z_r;q)_{k_s}}=\frac{(a_1\cdots a_d;q)_N}{(q;q)_N},\quad\Delta(z)=\prod_{r<s}(z_r-z_s).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-11.7.1`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-11.7.1**（Chapter 11, 11.7.1, 印刷p331）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。d≥1,N≥0，z_r非零且两两不同。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-11.7.8-p0 · Milne 的 A 型多变量 Jackson 求和

$$
\sum_{\substack{k_1,\ldots,k_d\ge0\\|k|=N}}\frac{\Delta(zq^k)}{\Delta(z)}\prod_{r=1}^d\frac{\prod_{s=1}^{d+1}(a_sz_r;q)_{k_r}}{(bz_r;q)_{k_r}\prod_{s=1}^d(qz_r/z_s;q)_{k_r}}=\frac{(b/a_1,\ldots,b/a_{d+1};q)_N}{(q,bz_1,\ldots,bz_d;q)_N},\quad b=\prod_{s=1}^{d+1}a_s\prod_{r=1}^dz_r.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-11.7.8-p0`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-11.7.8-p0**（Chapter 11, 11.7.8-p0, 印刷p332）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。d≥1,N≥0，a_s,z_r非零，Δ同11.7.1。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-11.Ex38-p0 · D 型多变量有限 Jackson 求和

$$
\sum_{\substack{k_1,\ldots,k_d\ge0\\|k|=N}}\frac{\Delta(zq^k)}{\Delta(z)}\prod_{r<s}\frac1{(z_rz_s;q)_{k_r+k_s}}\prod_{s=1}^d\frac{z_s^{k_s}q^{\binom{k_s}2}\prod_{r=1}^{d-1}(z_sa_r,z_s/a_r;q)_{k_s}}{(bz_s,z_sq^{1-N}/b;q)_{k_s}\prod_{r=1}^d(qz_s/z_r;q)_{k_s}}=(-bq^{N-1})^N\frac{\prod_{s=1}^{d-1}(ba_s,b/a_s;q)_N}{(q;q)_N\prod_{s=1}^d(bz_s,b/z_s;q)_N}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-11.Ex38-p0`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-11.Ex38-p0**（Chapter 11, 11.Ex38-p0, 印刷p348）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。d≥1,N≥0；a_s,b,z_s非零，Δ同11.7.1。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-11.Ex39-p0 · D 型 Jackson 的有限单纯形变式（已注明修订）

$$
\sum_{\substack{k_1,\ldots,k_d\ge0\\|k|\le N}}\frac{\Delta(zq^k)}{\Delta(z)}\prod_{s=1}^d\frac{1-az_sq^{k_s+|k|}}{1-az_s}\prod_{r<s}\frac1{(z_rz_s;q)_{k_r+k_s}}\prod_{r,s=1}^d\frac{(z_sb_r,z_s/b_r;q)_{k_s}}{(qz_s/z_r;q)_{k_s}}\prod_{r=1}^d\frac{(az_r;q)_{|k|}(aq/z_r;q)_{|k|-k_r}}{(aqb_r,aq/b_r;q)_{|k|}}\frac{(q^{-N},c,a^2q^{N+1}/c;q)_{|k|}q^{|k|}}{\prod_{s=1}^d(aqz_s/c,cz_s/(aq^N),az_sq^{N+1};q)_{k_s}}=\prod_{s=1}^d\frac{(aqz_s,aq/z_s,aqb_s/c,aq/(b_sc);q)_N}{(aqz_s/c,aq/(z_sc),aqb_s,aq/b_s;q)_N}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-11.Ex39-p0`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-11.Ex39-p0**（Chapter 11, 11.Ex39-p0, 印刷p348）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。d≥1,N≥0，ab_scz_s非零。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-11.Ex40-p0 · 多变量终止 Bailey 变换

$$
\mathcal S(a;b,c,d;e,f,g)=\left(\frac a\lambda\right)^{|m|}\frac{(\lambda q/f,\lambda q/g;q)_{|m|}}{(aq/f,aq/g;q)_{|m|}}\prod_{s=1}^{\ell}\frac{(aqz_s,\lambda qz_s/d;q)_{m_s}}{(\lambda qz_s,aqz_s/d;q)_{m_s}}\mathcal S(\lambda;\lambda b/a,\lambda c/a,d;\lambda e/a,f,g),\quad\lambda=a^2q/(bce),\quad a^3q^{2+|m|}=bcdefg,\quad\mathcal S(A;B,C,D;E,F,G)=\sum_{0\le k_s\le m_s}\frac{\Delta(zq^k)}{\Delta(z)}q^{|k|}\prod_{s=1}^{\ell}\frac{1-Az_sq^{k_s+|k|}}{1-Az_s}\frac{(B,C,D;q)_{|k|}}{(Aq/E,Aq/F,Aq/G;q)_{|k|}}\prod_{r=1}^{\ell}\frac{(Az_r;q)_{|k|}}{(Az_rq^{m_r+1};q)_{|k|}}\prod_{s=1}^{\ell}\frac{(Ez_s,Fz_s,Gz_s;q)_{k_s}}{(Aqz_s/B,Aqz_s/C,Aqz_s/D;q)_{k_s}}\prod_{r,s=1}^{\ell}\frac{(q^{-m_r}z_s/z_r;q)_{k_s}}{(qz_s/z_r;q)_{k_s}}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-11.Ex40-p0`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-11.Ex40-p0**（Chapter 11, 11.Ex40-p0, 印刷p349）：ℓ≥1，m_s≥0，z_s两两不同；a³q^{2+|m|}=bcdefg，λ=a²q/(bce)；所有实际分母非零；p=0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
