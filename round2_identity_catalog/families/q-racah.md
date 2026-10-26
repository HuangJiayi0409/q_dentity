# q-Racah 递推、正交与乘积核

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 本次未匹配到旧算法 9 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

## FQI-SRC-GR2-2.Ex10 · q-Racah 多项式反射变换

$$
R_n(x;a,b,c,N;q)=\frac{(aq/c,bq;q)_n}{(aq,bcq;q)_n}c^nR_n(N-x;b,a,c^{-1},N;q).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-2.Ex10`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-2.Ex10**（Chapter 2, 2.Ex10, 印刷p59）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。0≤n≤N，c≠0；R的有限定义见辅助说明，q^x按固定分支。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-7.2.1 · q-Racah 三项递推

$$
(t+cdq/t-1-cdq)R_n(t)=A_n(R_{n+1}(t)-R_n(t))-C_n(R_n(t)-R_{n-1}(t)),\quad A_n=\frac{(1-abq^{n+1})(1-aq^{n+1})(1-cq^{n+1})(1-bdq^{n+1})}{(1-abq^{2n+1})(1-abq^{2n+2})},\quad C_n=\frac{cdq(1-q^n)(1-bq^n)(1-abq^n/c)(1-aq^n/d)}{(1-abq^{2n})(1-abq^{2n+1})}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-7.2.1`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-7.2.1**（Chapter 7, 7.2.1, 印刷p177）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。R_n(t)=4φ3^[n](q^{-n},abq^{n+1},t,cdq/t;aq,cq,bdq;q,q)，tcd≠0；R_{−1}=0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-7.2.12 · q-Racah 一阶差分

$$
R_n(t)-R_{n-1}(t)=-\frac{q^{1-n}(1-abq^{2n})(1-t)(1-cdq/t)}{(1-aq)(1-cq)(1-bdq)}{}_4\phi_3^{[n-1]}(q^{1-n},abq^{n+1},qt,cdq^2/t;aq^2,cq^2,bdq^2;q,q).
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-7.2.12`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-7.2.12**（Chapter 7, 7.2.12, 印刷p178）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。n≥1，R同7.2.1。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-7.2.18 · q-Racah 有限正交及对偶正交

$$
\sum_{x=0}^N\rho_x W_m(x)W_n(x)=\delta_{mn}/h_n,\qquad\sum_{n=0}^Nh_nW_n(x)W_n(y)=\delta_{xy}/\rho_x,\quad\rho_x=\frac{(cq^{-N},aq,bcq,q^{-N};q)_x(1-cq^{2x-N})}{(q,cq^{-N}/a,q^{-N}/b,cq;q)_x(1-cq^{-N})}(abq)^{-x},\quad h_n=\frac{(bq,aq/c;q)_N}{(abq^2,1/c;q)_N}\frac{(abq,aq,bcq,q^{-N};q)_n(1-abq^{2n+1})q^{Nn}c^{-n}}{(q,bq,aq/c,abq^{N+2};q)_n(1-abq)}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-7.2.18`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-7.2.18**（Chapter 7, 7.2.18, 印刷p180）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。N≥0，0≤m,n,x,y≤N；W_n(x)=4φ3^[min(n,x)](q^{-n},abq^{n+1},q^{-x},cq^{x-N};aq,q^{-N},bcq;q,q)，abc≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-8.7.4 · q-Racah乘积双重展开修正式

$$
W_n(x;a,b,c,N)W_n(y;\alpha,ab/\alpha,\gamma,M)=\frac{(bq,aq/c;q)_nc^n}{(aq,bcq;q)_n}\sum_{r=0}^n\sum_{s=0}^{n-r}\frac{(q^{-n},abq^{n+1};q)_{r+s}(q^{-x},cq^{x-N},q^{-y},\gamma q^{y-M};q)_r}{(q^{-N};q)_{r+s}(q,\alpha q,q^{-M},ab\gamma q/\alpha,cq^{1-s};q)_r}\frac{(q^{x-N},c^{-1}q^{-x};q)_s(1-cq^{r-s})q^{r+s-rs}}{(q,bq,aq/c;q)_s(1-cq^{-s})}A_{r,s}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-8.7.4`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-8.7.4**（Chapter 8, 8.7.4, 印刷p230）：0≤n,x≤N≤M，0≤y≤M；A_{r,s}及W见8.Ex8。取r≤min(n,x,y)，s≤min(n−r,N−x)；外系数为零的项不计算内部级数；实际分母非零。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-8.7.6 · 有限 q-Racah 离散核展开

$$
\sum_{n=0}^z\frac{(q^{-z};q)_n}{(q^{-K};q)_n}h_nW_n(x;a,b,c,N)W_n(y;\alpha,ab/\alpha,\gamma,M)=h_0\sum_{r=0}^z\sum_{s=0}^{z-r}\frac{(q^{-z};q)_{r+s}(abq^2;q)_{2r+2s}(-1)^{r+s}q^{(r+s)(2N-r-s+1)/2}}{(q^{-K},abq^{N+2};q)_{r+s}}H_{r,s}A_{r,s}B_{r,s},\quad B_{r,s}=\sum_{j=0}^{z-r-s}\frac{1-\lambda q^{2j}}{1-\lambda}\frac{(\lambda,q^{r+s-N},q^{r+s-z};q)_j}{(q,abq^{N+r+s+2},q^{r+s-K};q)_j}q^{(N-r-s)j},\quad\lambda=abq^{2r+2s+1}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-8.7.6`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-8.7.6**（Chapter 8, 8.7.6, 印刷p230）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。0≤z≤min(K,N)，N≤M，x≤N,y≤M非负整数；h_n见7.2.18，H,A及零系数约定见8.Ex8。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-8.7.13 · 有限 q-Racah Poisson 核展开

$$
\sum_{n=0}^Nt^nh_nW_n(x;a,b,c,N)W_n(y;\alpha,ab/\alpha,\gamma,M)=h_0\sum_{r=0}^x\sum_{s=0}^{N-x}\frac{(abq^2;q)_{2r+2s}}{(abq^{N+2};q)_{r+s}}H_{r,s}A_{r,s}C_{r,s}(-t)^{r+s}q^{(r+s)(2N-r-s+1)/2},\quad C_{r,s}=\sum_{j=0}^{N-r-s}\frac{1-\lambda q^{2j}}{1-\lambda}\frac{(\lambda,q^{r+s-N};q)_j}{(q,abq^{N+r+s+2};q)_j}(tq^{N-r-s})^j,\quad\lambda=abq^{2r+2s+1}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-8.7.13`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-8.7.13**（Chapter 8, 8.7.13, 印刷p231）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。0≤x≤N≤M，0≤y≤M；h,H,A和零系数约定见7.2.18及8.Ex8。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-8.Ex8 · 任意有限权序列的 q-Racah 双线性变换

$$
\sum_{n=0}^z\frac{(aq,abq,bcq;q)_n(-c)^{-n}\lambda_nq^{\binom n2}}{(q,bq,aq/c;q)_n(abq;q)_{2n}}W_n(x;a,b,c,N)W_n(y;\alpha,ab/\alpha,\gamma,M)=\sum_{r=0}^z\sum_{s=0}^{z-r}\frac{(q^{-z};q)_{r+s}}{(q^{-N};q)_{r+s}}H_{r,s}A_{r,s}\mu_{r+s},\quad\lambda_n=\sum_{k=0}^{z-n}\frac{(q^{-z};q)_{n+k}\mu_{n+k}}{(q,abq^{2n+2};q)_k},\quad H_{r,s}=\frac{(q^{-x},cq^{x-N},q^{-y},\gamma q^{y-M};q)_r(q^{x-N},c^{-1}q^{-x};q)_s(1-cq^{r-s})q^{-rs}}{(q,\alpha q,q^{-M},ab\gamma q/\alpha,cq^{1-s};q)_r(q,bq,aq/c;q)_s(1-cq^{-s})},\quad A_{r,s}={}_5\phi_4^{[s]}(q^{-s},q^{r-y},\gamma q^{r+y-M},aq^{r+1},bcq^{r+1};\alpha q^{r+1},q^{r-M},ab\gamma q^{r+1}/\alpha,cq^{1+r-s};q,q).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-8.Ex8`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-8.Ex8**（Chapter 8, 8.Ex8, 印刷p248）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。0≤z,x≤N≤M，0≤y≤M；µ_0…µ_z任意，abcαγ≠0。外系数为零的项整项置零且不计算其内部未定义级数；有效r≤x,y、s≤N−x。W见7.2.18。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-8.Ex9 · q-Racah 有限双线性求值

$$
\sum_{n=0}^z\frac{1-abq^{2n+1}}{1-abq}\frac{(abq,aq,d,e,bcq,q^{-z};q)_n}{(q,bq,abq^2/d,abq^2/e,aq/c,abq^{z+2};q)_n}\left(\frac{abq^{z+2}}{cde}\right)^nW_n(x;a,b,c,N)W_n(y;\alpha,ab/\alpha,\gamma,M)=\frac{(abq^2,abq^2/(de);q)_z}{(abq^2/d,abq^2/e;q)_z}\sum_{r=0}^z\sum_{s=0}^{z-r}\frac{(q^{-z},d,e;q)_{r+s}q^{r+s}}{(q^{-N},deq^{-z-1}/(ab);q)_{r+s}}H_{r,s}A_{r,s}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-8.Ex9`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-8.Ex9**（Chapter 8, 8.Ex9, 印刷p249）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。0≤z,x≤N≤M，0≤y≤M，abcdeαγ≠0；H,A和零系数约定见8.Ex8。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
