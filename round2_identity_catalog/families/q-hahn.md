# q-Hahn 与对偶 q-Hahn

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 本次未匹配到旧算法 10 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

## FQI-SRC-GR2-7.2.22 · q-Hahn 有限正交

$$
\sum_{x=0}^NQ_m(x)Q_n(x)\frac{(aq;q)_x(bq;q)_{N-x}}{(q;q)_x(q;q)_{N-x}}(aq)^{-x}=\frac{(abq^2;q)_N(aq)^{-N}}{(q;q)_N}\frac{(q;q)_n(1-abq)(bq,abq^{N+2};q)_n}{(abq;q)_n(1-abq^{2n+1})(aq,q^{-N};q)_n}(-aq)^nq^{n(n-1)/2-Nn}\delta_{mn}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-7.2.22`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-7.2.22**（Chapter 7, 7.2.22, 印刷p180）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。N≥0，0≤m,n≤N；Q_n(x)=3φ2^[min(n,x)](q^{-n},abq^{n+1},q^{-x};aq,q^{-N};q,q)，a≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-7.2.24 · 对偶 q-Hahn 有限正交

$$
\sum_{x=0}^ND_m(x)D_n(x)\frac{(cq^{-N},bcq,q^{-N};q)_x(1-cq^{2x-N})}{(q,q^{-N}/b,cq;q)_x(1-cq^{-N})}q^{Nx-x(x-1)/2}(-bcq)^{-x}=\frac{(1/c;q)_N(q,bq;q)_n}{(bq;q)_N(bcq,q^{-N};q)_n}(cq^{-N})^n\delta_{mn}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-7.2.24`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-7.2.24**（Chapter 7, 7.2.24, 印刷p181）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。N≥0，0≤m,n≤N；D_n(x)=3φ2^[min(n,x)](q^{-n},q^{-x},cq^{x-N};q^{-N},bcq;q,q)，bc≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-8.3.3 · q-Hahn 多项式的 Watson 型乘积

$$
Q_n(x)Q_n(y)=(-aq)^nq^{\binom n2}\frac{(bq;q)_n}{(aq;q)_n}\sum_{m=0}^n\frac{(q^{-n},abq^{n+1},q^{x-N},q^{y-N};q)_m(aq^{x+y})^{-m}}{(q,bq,q^{-N},q^{-N};q)_m}{}_4\phi_3^{[m]}(q^{-x},q^{-y},b^{-1}q^{-m},q^{-m};aq,q^{N-x+1-m},q^{N-y+1-m};q,abq^{2N+3}).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-8.3.3`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-8.3.3**（Chapter 8, 8.3.3, 印刷p221）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。0≤n,x,y≤N；Q定义见7.2.22；先乘开有限积消去可去奇点，或取实际无零分母域。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-8.Ex4i · q-Hahn 乘积的另一有限双和

$$
Q_n(x)Q_n(y)=\frac{(bq,abq^{N+2};q)_n(bq^{N+1})^{-n}}{(aq,q^{-N};q)_n}\sum_{m=0}^n\frac{(q^{-n},abq^{n+1},bq^{N-x+1},bq^{N-y+1};q)_mq^m}{(q,bq,abq^{N+2},bq^{N+1};q)_m}\sum_{k=0}^{\min(m,x,y)}\frac{1-b^{-1}q^{2k-N-m-1}}{1-b^{-1}q^{-N-m-1}}\frac{(b^{-1}q^{-N-m-1},a^{-1}b^{-1}q^{-N-m-1},b^{-1}q^{-m},q^{-m},q^{-x},q^{-y};q)_k(ab)^kq^{(x+y+2m+2-k)k}}{(q,aq,q^{-N},b^{-1}q^{-N},b^{-1}q^{x-N-m},b^{-1}q^{y-N-m};q)_k}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-8.Ex4i`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-8.Ex4i**（Chapter 8, 8.Ex4i, 印刷p246）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。0≤n,x,y≤N；Q=Q_n(·;a,b,N)，ab≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-8.Ex4ii · q-Hahn 乘积的有限三重和

$$
Q_n(x)Q_n(y)=\frac{(bq,abq^{N+2};q)_n(bq^{N+1})^{-n}}{(aq,q^{-N};q)_n}\sum_{m=0}^n\frac{(q^{-n},abq^{n+1},bq^{N+1-x-y};q)_mq^{(x+1)m}}{(q,bq,abq^{N+2};q)_m}\sum_{k=0}^{\min(m,x,y)}\frac{(q^{-m},abq^{m+1},q^{-x},q^{-y};q)_k(bq^{N-x+2})^k}{(q,aq,q^{-N},bq^{N+1-x-y};q)_k}{}_3\phi_2^{[\min(m-k,x-k)]}(q^{k-m},q^{k-x},bq^{N+1-x};0,bq^{N+1-x-y+k};q,q).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-8.Ex4ii`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-8.Ex4ii**（Chapter 8, 8.Ex4ii, 印刷p246）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。0≤n,x,y≤N；Q=Q_n(·;a,b,N)，ab≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-8.Ex7i · q-Hahn 有限离散双线性核

$$
\sum_{n=0}^z\frac{(abq,aq,q^{-z};q)_n(1-abq^{2n+1})(-aq)^{-n}q^{Nn-\binom n2}}{(q,bq,abq^{N+2};q)_n(1-abq)}Q_n(x;a,b,N)Q_n(y;a,b,M)=\sum_{r=0}^z\sum_{s=0}^{z-r}\frac{(q^{-z};q)_{r+s}(abq^2;q)_{2r+2s}(q^{-x},q^{-y};q)_r(q^{x-N},q^{y-M};q)_s(q^{N-z};q)_{z-r-s}(-1)^{r+s}a^{-s}q^{(r+s)(2N-r-s+1)/2-(x+y+1)s}}{(q^{-M},q^{-N},abq^{N+2};q)_{r+s}(q,aq;q)_r(q,bq;q)_s(abq^{N+r+s+2};q)_{z-r-s}}{}_2\phi_1^{[\max(0,z-r-s-1)]}(q^{r+s-z},q^{1+r+s-z};q^{1+N-z};q,abq^{N+z+2}).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-8.Ex7i`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-8.Ex7i**（Chapter 8, 8.Ex7i, 印刷p247）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。0≤z,x≤N≤M，0≤y≤M；零外系数项整体为零。Q见7.2.22。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-9.Ex4i · q-Hahn 有限生成函数（一，原印）

$$
\sum_{n=0}^N\frac{(q^{-N};q)_n}{(q,bq;q)_n}Q_n(x;a,b,N)t^n={}_2\phi_1^{[N-x]}(q^{x-N},0;bq;q,tq^{-x}){}_1\phi_1^{[x]}(q^{-x};aq;q,aqt).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-9.Ex4i`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-9.Ex4i**（Chapter 9, 9.Ex4i, 印刷p272）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。0≤x≤N；Q见7.2.22。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-9.Ex4ii · q-Hahn 有限生成函数（二）

$$
\sum_{n=0}^N\frac{(aq,q^{-N};q)_n}{(q;q)_n}q^{-\binom n2}Q_n(x;a,b,N)t^n={}_2\phi_1^{[x]}(q^{-x},bq^{N-x+1};0;q,-atq^{x-N+1}){}_2\phi_0^{[N-x]}(q^{x-N},aq^{x+1};-;q,-tq^{-x}).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-9.Ex4ii`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-9.Ex4ii**（Chapter 9, 9.Ex4ii, 印刷p273）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。0≤x≤N。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-9.Ex5i · 对偶 q-Hahn 有限生成函数（一，定义核正）

$$
\sum_{n=0}^N\frac{(q^{-N};q)_n}{(q;q)_n}D_n(x;b,c,N)t^n={}_2\phi_1^{[x]}(q^{-x},c^{-1}q^{-x};bq;q,bctq^{x+1})(tq^{-N};q)_{N-x}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-9.Ex5i`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-9.Ex5i**（Chapter 9, 9.Ex5i, 印刷p273）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。0≤x≤N；D_n在本习题统一为3φ2^[min(n,x)](q^{-n},q^{-x},bcq^{x+1};q^{-N},bq;q,q)。它等于7.2.23的D_n(x;q^{-N-1}/c,bcq^{N+1},N)，并非原印声称的同参数D_n；来源定义冲突和反例另存。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-9.Ex5ii · 对偶 q-Hahn 有限生成函数（二，定义核正）

$$
\sum_{n=0}^N\frac{(q^{-N},bq;q)_n}{(q,c^{-1}q^{-N};q)_n}D_n(x;b,c,N)t^n={}_2\phi_1^{[N-x]}(q^{x-N},bq^{x+1};c^{-1}q^{-N};q,tq^{-x})(bcqt;q)_x.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-9.Ex5ii`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-9.Ex5ii**（Chapter 9, 9.Ex5ii, 印刷p273）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。0≤x≤N；D同9.Ex5i。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
