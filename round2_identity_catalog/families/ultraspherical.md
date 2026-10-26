# 连续 q-超球与 Rogers 线性化

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 本次未匹配到旧算法 14 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

## FQI-SRC-GR2-1.Ex29 · 连续 q 超球多项式的两种终止表示

$$
C_n((t+t^{-1})/2;\beta\mid q)=\frac{(\beta;q)_nt^n}{(q;q)_n}{}_2\phi_1^{[n]}\!\left[\begin{matrix}q^{-n},\beta\\\beta^{-1}q^{1-n}\end{matrix};q,q/(\beta t^2)\right]=\frac{(\beta^2;q)_nt^{-n}\beta^{-n}}{(q;q)_n}{}_3\phi_2^{[n]}\!\left[\begin{matrix}q^{-n},\beta,\beta t^2\\\beta^2,0\end{matrix};q,q\right].
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-1.Ex29`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-1.Ex29**（Chapter 1, 1.Ex29, 印刷p31）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。βt≠0；C_n的有限Laurent和定义见辅助说明。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-7.4.14 · 连续 q-超球多项式的终止 4φ3 表示

$$
C_n(z;\beta)=\frac{(\beta^2;q)_n}{(q;q)_n}\beta^{-n/2}{}_4\phi_3^{[n]}(q^{-n},\beta^2q^n,\beta^{1/2}z,\beta^{1/2}/z;\beta q^{1/2},-\beta,-\beta q^{1/2};q,q).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-7.4.14`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-7.4.14**（Chapter 7, 7.4.14, 印刷p186）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。C_n(z;β)=Σ_{k=0}^n(β;q)_k(β;q)_{n−k}z^{n−2k}/((q;q)_k(q;q)_{n−k})；βz≠0，平方根相容。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-7.5.35 · 连续 q-超球偶数次数的二次变换

$$
C_{2n}(z;\beta)=\frac{(\beta,\beta s;q)_n}{(q,s;q)_n}s^{-n}{}_4\phi_3^{[n]}(q^{-n},\beta q^n,sz^2,s/z^2;\beta s,-s,-q;q,q),\quad s^2=q.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-7.5.35`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-7.5.35**（Chapter 7, 7.5.35, 印刷p193）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。βz≠0，相容平方根s；C见7.4.14。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-7.5.36 · 连续 q-超球奇数次数的二次变换

$$
C_{2n+1}(z;\beta)=\frac{z+z^{-1}}2\frac{(\beta,-1;q)_{n+1}}{(s,-s;q)_{n+1}}s^{-n}\frac{(\beta s,-qs;q)_n}{(q,-q;q)_n}{}_4\phi_3^{[n]}(q^{-n},\beta q^{n+1},sz^2,s/z^2;\beta s,-qs,-q;q,q),\quad s^2=q.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-7.5.36`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-7.5.36**（Chapter 7, 7.5.36, 印刷p193）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。βz≠0；C见7.4.14。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-7.6.14 · Rogers 连续 q-超球连接公式

$$
C_n(z;\gamma)=\sum_{k=0}^{\lfloor n/2\rfloor}\frac{\beta^k(\gamma/\beta;q)_k(\gamma;q)_{n-k}(1-\beta q^{n-2k})}{(q;q)_k(\beta q;q)_{n-k}(1-\beta)}C_{n-2k}(z;\beta).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-7.6.14`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-7.6.14**（Chapter 7, 7.6.14, 印刷p197）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。C见7.4.14；β≠0,1。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-7.Ex14 · 连续 q-超球的 Chebyshev 边界

$$
C_n(z;q)=\sum_{k=0}^nz^{n-2k}=\frac{z^{n+1}-z^{-n-1}}{z-z^{-1}},\qquad\lim_{\beta\to1}\frac{1-q^n}{2(1-\beta)}C_n(z;\beta)=\frac{z^n+z^{-n}}2\quad(n\ge1).
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-7.Ex14`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-7.Ex14**（Chapter 7, 7.Ex14, 印刷p203）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。C见7.4.14；z≠0，商形式z²≠1，可去奇点用有限和。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-7.Ex17 · 连续 q-超球在零点的奇偶求值

$$
C_n(i;\beta)=\begin{cases}0&n\text{为奇数},\\(-1)^{n/2}(\beta^2;q^2)_{n/2}/(q^2;q^2)_{n/2}&n\text{为偶数}.\end{cases}
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-7.Ex17`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-7.Ex17**（Chapter 7, 7.Ex17, 印刷p203）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。z=i对应x=0；C见7.4.14。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-7.Ex19 · 连续 q-超球的次数和参数递推

$$
(z+z^{-1})C_n(z;\beta)=\frac{1-q^{n+1}}{1-\beta q^n}C_{n+1}(z;\beta)+\frac{1-\beta^2q^{n-1}}{1-\beta q^n}C_{n-1}(z;\beta),\quad C_n(z;\beta)=\frac{1-\beta}{1-\beta q^n}\bigl(C_n(z;\beta q)-\beta C_{n-2}(z;\beta q)\bigr).
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-7.Ex19`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-7.Ex19**（Chapter 7, 7.Ex19, 印刷p203）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。C_{−1}=C_{−2}=0，C见7.4.14。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-8.4.7 · 连续 q-超球多项式的有限双和乘积

$$
r_n(z)r_n(w)=\frac{1+a^2q^n}{1+a^2}(-q^{-1/2})^n\sum_{m=0}^n\frac{(q^{-n},a^4q^n,-sz/w,-a^2sw/z;q)_mq^m}{(q,a^2s,-a^2s,-a^2q;q)_m}{}_4\phi_3^{[m]}(q^{-m},a^2,a^2w^2,a^2/z^2;a^4,-a^2sw/z,-sq^{-m}w/z;q,q),\quad s^2=q.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-8.4.7`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-8.4.7**（Chapter 8, 8.4.7, 印刷p224）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。r_n(z)=4φ3^[n](q^{-n},a^4q^n,az,a/z;a²s,−a²,−a²s;q,q)，azw≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-8.5.1 · Rogers 连续 q-超球线性化公式

$$
C_m(z;\beta)C_n(z;\beta)=\sum_{k=0}^{\min(m,n)}\frac{(q;q)_{m+n-2k}(\beta;q)_{m-k}(\beta;q)_{n-k}(\beta;q)_k(\beta^2;q)_{m+n-k}(1-\beta q^{m+n-2k})}{(\beta^2;q)_{m+n-2k}(q;q)_{m-k}(q;q)_{n-k}(q;q)_k(\beta q;q)_{m+n-k}(1-\beta)}C_{m+n-2k}(z;\beta).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-8.5.1`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-8.5.1**（Chapter 8, 8.5.1, 印刷p226）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。m,n≥0，C见7.4.14。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-8.9.8 · 双连续 q-超球平方展开（修订）

$$
{}_7\phi_6^{[n]}(q^{-n},q^{n+\alpha+2},q^{(\alpha+1)/2},q^{(\alpha+1)/2}z^2,q^{(\alpha+1)/2}/z^2,q^{(\alpha+2)/2}w^2,q^{(\alpha+2)/2}/w^2;q^{\alpha+1},q^{(\alpha+3)/2},-q^{(\alpha+3)/2},-q^{(\alpha+2)/2},-q^{(\alpha+2)/2},-q^{(\alpha+1)/2};q,q)=\sum_{j=0}^n\frac{(q^{-n},q^{n+\alpha+2},q^{(\alpha+2)/2},q^{(\alpha+2)/2}w^2,q^{(\alpha+2)/2}/w^2;q)_j(-1)^jq^{j+\binom j2}}{(q,q^{(\alpha+3)/2},-q^{(\alpha+3)/2},-q^{(\alpha+2)/2},q^{j+\alpha+1};q)_j}\left[\frac{(q;q)_j(q;q)_{n-j}q^{[n(\alpha+2)+2j(n-j)-j]/4}}{(q^{\alpha+1};q)_j(q^{2j+\alpha+2};q)_{n-j}}C_j(z;q^{(\alpha+1)/2})C_{n-j}(w;q^{j+(\alpha+2)/2})\right]^2.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-8.9.8`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-8.9.8**（Chapter 8, 8.9.8, 印刷p238）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。zw≠0；所有幂取相容分支。所有实际分母非零；见修订报告。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-8.Ex12 · Rogers 线性化的逆公式

$$
C_{m+n}(z;\beta)=\sum_{k=0}^{\min(m,n)}\frac{(q;q)_m(q;q)_n(\beta;q)_{m+n}}{(\beta;q)_m(\beta;q)_n(q;q)_{m+n}}\frac{(\beta^{-2}q^{-m-n},\beta^{-1};q)_k(1-\beta^{-2}q^{2k-m-n})}{(q,\beta^{-1}q^{1-m-n};q)_k(1-\beta^{-2}q^{-m-n})}(\beta^2/q)^kC_{m-k}(z;\beta)C_{n-k}(z;\beta).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-8.Ex12`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-8.Ex12**（Chapter 8, 8.Ex12, 印刷p249）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。m,n≥0，βz≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-8.Ex28 · 相伴连续 q-超球线性化公式

$$
C_m^\alpha(z;\beta)C_n^\alpha(z;\beta)=\sum_{k=0}^{\min(m,n)}L_kC_{m+n-2k}^\alpha(z;\beta),\quad L_k=\frac{(q;q)_m(q;q)_n(\alpha q;q)_{m+n-2k}(\alpha\beta;q)_{m-k}(\alpha\beta;q)_{n-k}(\alpha\beta;q)_k}{(\alpha q;q)_m(\alpha q;q)_n(\alpha\beta^2;q)_{m+n-2k}(q;q)_{m-k}(q;q)_{n-k}(q;q)_k}\frac{(\alpha\beta^2;q)_{m+n-k}(q^{k-m-n}/\alpha;q)_k\alpha^k(1-\alpha\beta q^{m+n-2k})}{(\alpha\beta q;q)_{m+n-k}(q^{k-m-n};q)_k(1-\alpha\beta)}W_{10}^{[k]}(q^{k-m-n-1};q^{k-m-n}/(\alpha\beta),q^{k-m-n}/(\alpha\beta),\alpha,\alpha\beta^2/q,q^{k-m},q^{k-n},q^{-k};q,q).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-8.Ex28`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-8.Ex28**（Chapter 8, 8.Ex28, 印刷p255）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。C_{−1}^α=0,C_0^α=1；(z+z^{-1})C_n^α=(1−αq^{n+1})/(1−αβq^n) C_{n+1}^α+(1−αβ²q^{n−1})/(1−αβq^n) C_{n−1}^α；αβz≠0；当W提前终止按最小长度计算。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-9.Ex7 · 相伴连续 q-超球的有限卷积

$$
C_n^\alpha(z;\beta)=\sum_{k=0}^n\frac{1-\alpha}{1-\alpha q^k}\beta^kC_k(z;q/\beta)C_{n-k}(z;\beta).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-9.Ex7`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-9.Ex7**（Chapter 9, 9.Ex7, 印刷p273）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。相伴C由8.Ex28的递推定义，普通C见7.4.14；αβz≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
