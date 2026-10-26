# Askey–Wilson、相伴多项式及差分

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 本次未匹配到旧算法 18 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

## FQI-SRC-GR2-2.Ex11 · Askey–Wilson 参数交换与奇偶关系

$$
p_n(x;a,b,c,d\mid q)=p_n(x;b,a,c,d\mid q),\qquad p_n(-x;a,b,c,d\mid q)=(-1)^np_n(x;-a,-b,-c,-d\mid q).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-2.Ex11`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-2.Ex11**（Chapter 2, 2.Ex11, 印刷p59）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。x=(t+t^{-1})/2，abt≠0；p的终止4φ3定义见辅助说明。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-7.5.3 · Askey–Wilson 三项递推

$$
(z+z^{-1})P_n(z)=A_nP_{n+1}(z)+B_nP_n(z)+C_nP_{n-1}(z),\quad A_n=\frac{1-abcdq^{n-1}}{(1-abcdq^{2n-1})(1-abcdq^{2n})},\quad C_n=\frac{(1-q^n)\prod_{uv\in\{ab,ac,ad,bc,bd,cd\}}(1-uvq^{n-1})}{(1-abcdq^{2n-2})(1-abcdq^{2n-1})},\quad B_n=a+a^{-1}-\frac{A_n}{a}(1-abq^n)(1-acq^n)(1-adq^n)-\frac{aC_n}{(1-abq^{n-1})(1-acq^{n-1})(1-adq^{n-1})}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-7.5.3`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-7.5.3**（Chapter 7, 7.5.3, 印刷p188）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。P_n(z)=a^{-n}(ab,ac,ad;q)_n4φ3^[n](q^{-n},abcdq^{n-1},az,a/z;ab,ac,ad;q,q)；az≠0，P_{−1}=0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-7.5.20 · Askey–Wilson 正交证明的有限消去式

$$
\sum_{j=0}^m\frac{(q^{-m},abcdq^{m-1};q)_jq^j}{(q,abcd;q)_j}{}_3\phi_2^{[n]}(q^{-n},abcdq^{n-1},abq^j;abcdq^j,ab;q,q)=\frac{(q,cd;q)_n(1-abcd/q)}{(abcd/q,ab;q)_n(1-abcdq^{2n-1})}(ab)^n\delta_{mn}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-7.5.20`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-7.5.20**（Chapter 7, 7.5.20, 印刷p191）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。0≤n≤m。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-7.6.2 · Askey–Wilson 有限连接公式

$$
P_n(z;\alpha,\beta,\gamma,d)=\sum_{k=0}^nc_{k,n}P_k(z;a,b,c,d),\quad c_{k,n}=\frac{(\alpha d,\beta d,\gamma d,q;q)_n(\alpha\beta\gamma dq^{n-1};q)_kq^{k^2-nk}d^{k-n}}{(\alpha d,\beta d,\gamma d,q,abcdq^{k-1};q)_k(q;q)_{n-k}}{}_5\phi_4^{[n-k]}(q^{k-n},\alpha\beta\gamma dq^{n+k-1},adq^k,bdq^k,cdq^k;abcdq^{2k},\alpha dq^k,\beta dq^k,\gamma dq^k;q,q).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-7.6.2`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-7.6.2**（Chapter 7, 7.6.2, 印刷p195）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。P见7.5.3；αad≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-7.6.8 · Askey–Wilson 单参数连接系数求值

$$
P_n(z;\alpha,b,c,d)=\sum_{k=0}^n\frac{(\alpha/a;q)_{n-k}(\alpha bcdq^{n-1};q)_k(q,bc,bd,cd;q)_na^{n-k}}{(q,bc,bd,cd;q)_k(abcdq^{k-1};q)_k(q,abcdq^{2k};q)_{n-k}}P_k(z;a,b,c,d).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-7.6.8`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-7.6.8**（Chapter 7, 7.6.8, 印刷p196）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。P见7.5.3；aα≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-7.7.6 · Askey–Wilson 差分算子作用于有限积

$$
\mathcal D_q(az,a/z;q)_n=-\frac{2a(1-q^n)}{1-q}(asz,as/z;q)_{n-1},\quad s^2=q.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-7.7.6`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-7.7.6**（Chapter 7, 7.7.6, 印刷p197）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。n≥1，z≠0；D_q f(z)=[f(sz)−f(z/s)]/[(s−s^{-1})(z−z^{-1})/2]。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-7.7.10 · Askey–Wilson 有限差分方程

$$
q^{-n}(1-q^n)(1-abcdq^{n-1})P_n(z)=A(z)(P_n(qz)-P_n(z))+A(z^{-1})(P_n(z/q)-P_n(z)),\quad A(z)=\frac{(1-az)(1-bz)(1-cz)(1-dz)}{(1-z^2)(1-qz^2)}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-7.7.10`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-7.7.10**（Chapter 7, 7.7.10, 印刷p198）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。P见7.5.3；az≠0；有限有理域。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-7.7.7 · Askey–Wilson 多项式降阶差分

$$
\mathcal D_qP_n(z;a,b,c,d)=\frac{2q^{(1-n)/2}(1-q^n)(1-abcdq^{n-1})}{1-q}P_{n-1}(z;as,bs,cs,ds),\quad s^2=q.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-7.7.7`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-7.7.7**（Chapter 7, 7.7.7, 印刷p198）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。n≥1；P、D_q分别见7.5.3、7.7.6。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-7.Ex5 · Askey–Wilson 终止平衡 4φ3 连续关系

$$
A\varphi(a/q,bq)+B\varphi(a,b)+C\varphi(aq,b/q)=0,\quad A=b(1-b)(aq-b)(a-e)(a-f)(a-g),\quad C=-a(1-a)(a-bq)(e-b)(f-b)(g-b),\quad B=ab(a-bq)(a-b)(aq-b)(1-c)(1-d)-A-C.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-7.Ex5`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-7.Ex5**（Chapter 7, 7.Ex5, 印刷p200）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。φ(a,b)=4φ3(a,b,c,d;e,f,g;q,q)，efg=abcdq；各项按其上参数分别终止：如c=q^{-N}时共同截N；a=q^{-N},N≥1时三项长度N+1,N,N−1；互换b同理。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-7.Ex27 · Askey–Wilson 的四个三角多项式特例

$$
P_n(z;q,-q,s,-s)=(q^{n+2};q)_n\frac{z^{n+1}-z^{-n-1}}{z-z^{-1}},\quad P_n(z;1,-1,s,-s)=(q^n;q)_n(z^n+z^{-n})\ (n\ge1),\quad P_n(z;q,-1,s,-s)=(q^{n+1};q)_n\frac{z^{n+1}-z^{-n}}{z-1},\quad P_n(z;1,-q,s,-s)=(q^{n+1};q)_n\frac{z^{n+1}+z^{-n}}{z+1},\quad s^2=q.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-7.Ex27`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-7.Ex27**（Chapter 7, 7.Ex27, 印刷p206）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。P见7.5.3；z≠0，各可去奇点用多项式延拓。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-7.Ex37-finite · 加权有限多项式的 q 差分关系

$$
\mathcal D_q\left[\frac{U_n(z)}{(\rho qz,\rho q/z;q)_n}\right]=-\frac{1-\rho^2q^n}{1-q^{n+1}}\frac{T_n(z)U_{n+1}(sz)-T_n(z^{-1})U_{n+1}(z/s)}{(s-s^{-1})(z-z^{-1})/2},\quad T_n(z)=\frac{1-q^{-n}/(\rho sz)}{(\rho qs z;q)_n(\rho s/z;q)_{n+1}},\quad U_n(z)=A_{n,r}(\rho qz,\rho q/z;q)_n{}_6\phi_5^{[r-n]}(q^{n-r},\rho^2\lambda^2q^{n+r+1},\rho sq^n,\rho^2q^n,\rho q^{n+1}z,\rho q^{n+1}/z;\rho^2q^{2n+1},\rho\lambda q^{n+1},\rho^2q^{n+1},-\rho\lambda q^{n+1},-\rho sq^n;q,q),\quad A_{n,r}=\frac{(q;q)_n(\rho^2\lambda^2q;q)_{n+r}s^{3n^2+n-2nr}\rho^{2n}}{(q;q)_{r-n}(\rho q,\rho^2q,\rho\lambda q,-\rho q,-\rho s,-\rho s,-\rho\lambda q;q)_n},\quad s^2=q.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-7.Ex37-finite`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-7.Ex37-finite**（Chapter 7, 7.Ex37-finite, 印刷p208）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。1≤n≤r；U_{r+1}=0，ρ=q^ν,λ=q^λ_original非零，D_q见7.7.6。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-8.Ex11 · Askey–Wilson 的有限加法公式

$$
P_n(v;a,as,-a,-as)=\sum_{k=0}^nA_{k,n}(z,w)P_k(v;azw,a/(zw),az/w,aw/z),\quad A_{k,n}=\frac{(q;q)_n(a^4q^n,a^4/q,a^2s,-a^2s,-a^2;q)_ka^{n-k}}{(q;q)_k(q;q)_{n-k}(a^4/q;q)_{2k}(a^2s,-a^2s,-a^2;q)_n}P_{n-k}(z;as^k,as^{k+1},-as^k,-as^{k+1})P_{n-k}(w;as^k,as^{k+1},-as^k,-as^{k+1}),\quad s^2=q.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-8.Ex11`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-8.Ex11**（Chapter 8, 8.Ex11, 印刷p249）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。azwv≠0；P见7.5.3，原书x=cosθ,y=cosφ，本表以z=e^{iθ},w=e^{iφ}表示。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-8.Ex20 · 特殊 Askey–Wilson 的有限线性化

$$
P_m(z;a,q/a,-b,-q/b)P_n(z;a,q/a,-b,-q/b)=\sum_{k=0}^{2\min(m,n)}L_kP_{m+n-k}(z;a,q/a,-b,-q/b),\quad L_k=\frac{(q;q)_{2m}(q;q)_{2n}(q;q)_{m+n}}{(q;q)_m(q;q)_n(q;q)_{2m+2n}}b^{-k}q^{(3m+3n+1)k-3\binom k2}\frac{1-q^{2m+2n+1-2k}}{1-q^{2m+2n+1-k}}\frac{(q^{-2m-2n},-bq^{-m-n}/a,-abq^{-m-n-1};q)_k}{(q,q^{-2m},q^{-2n},q^{-m-n};q)_k}T_k(-bq^{m+n+1-k}/a,-bq^{-m-n}/a)T_k(-abq^{m+n-k},-abq^{-m-n-1}),\quad T_k(U,V)=\sum_{j=\max(0,k-m,k-n)}^{\min(k,m,n)}\frac{(q^{-k},q^{-m},q^{-n},U;q)_j(q^{-m},q^{-n};q)_{k-j}}{(q,V;q)_j}q^{(2k-m-n)j-j^2}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-8.Ex20`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-8.Ex20**（Chapter 8, 8.Ex20, 印刷p252）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。m,n≥0；a,b>0，P见7.5.3。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-8.Ex21 · Askey–Wilson 有限卷积恒等式

$$
\sum_{k=0}^{m+n}b^{m-k}\begin{bmatrix}m+n\\k\end{bmatrix}_q\frac{(b^2;q)_n(a^2b^2c^2q^{m+n-1};q)_k(c^2;q)_m}{(c^2,b^2c^2q^{k-1};q)_k(b^2c^2q^{2k};q)_{m+n-k}}{}_4\phi_3^{[\min(k,n)]}(q^{-k},b^2c^2q^{k-1},q^{-n},a^2b^2q^{n-1};b^2,a^2b^2c^2q^{m+n-1},q^{-m-n};q,q)P_k(w_2;bw_1,b/w_1,cs,c/s)P_{m+n-k}(w_1;at,a/t,bcsq^k,bcq^k/s)=P_n(w_1;at,a/t,bw_2,b/w_2)P_m(w_2;abtq^n,abq^n/t,cs,c/s).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-8.Ex21`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-8.Ex21**（Chapter 8, 8.Ex21, 印刷p252）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。m,n≥0；abcstw1w2≠0；P见7.5.3。所有实际分母非零；见修订报告。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-8.Ex26 · 相伴 Askey–Wilson 的有限 10W9 展开

$$
r_n^{\rho}(z)=\sum_{k=0}^n\frac{(q^{-n},abcd\rho^2q^{n-1},abcd\rho^2/q,az,a/z;q)_kq^k}{(q,ab\rho,ac\rho,ad\rho,abcd\rho/q;q)_k}W_{10}^{[n-k]}(abcd\rho^2q^{k-2};\rho,bc\rho/q,bd\rho/q,cd\rho/q,q^{k+1},abcd\rho^2q^{n+k-1},q^{k-n};q,a^2).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-8.Ex26`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-8.Ex26**（Chapter 8, 8.Ex26, 印刷p254）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。ρ=q^α；r_{−1}=0,r_0=1，(z+z^{-1}−a−a^{-1}+A(ρq^n)+C(ρq^n))r_n=A(ρq^n)r_{n+1}+C(ρq^n)r_{n−1}，A(v)=a^{-1}(1−abv)(1−acv)(1−adv)(1−abcdv/q)/((1−abcdv²/q)(1−abcdv²))，C(v)=a(1−bcv/q)(1−bdv/q)(1−cdv/q)(1−v)/((1−abcdv²/q²)(1−abcdv²/q))；abcdρz≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-8.Ex27 · 相伴 Askey–Wilson 的双重有限和

$$
r_n^{\rho}(z)=\frac{(abcd\rho^2/q,\rho q;q)_n\rho^{-n}}{(q,abcd\rho/q;q)_n}\sum_{k=0}^n\frac{(q^{-n},abcd\rho^2q^{n-1},a\rho z,a\rho/z;q)_kq^k}{(\rho q,ab\rho,ac\rho,ad\rho;q)_k}\sum_{j=0}^k\frac{(\rho,ab\rho/q,ac\rho/q,ad\rho/q;q)_jq^j}{(q,abcd\rho^2/q^2,a\rho z,a\rho/z;q)_j}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-8.Ex27`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-8.Ex27**（Chapter 8, 8.Ex27, 印刷p254）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。r和ρ的定义见8.Ex26。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-9.5.3-finite · 有限支撑权序列的 Askey–Wilson 双线性变换

$$
\sum_{n=0}^N\nu_nk_nr_n(z)r_n(v)=\sum_{n=0}^N\frac{(dz,d/z,dv,d/v;q)_nw_n}{(q,bd,cd,d/a;q)_n}W_{10}^{[n]}(aq^{-n}/d;q^{1-n}/(bd),q^{1-n}/(cd),q^{-n},az,a/z,av,a/v;q,bcq/(ad)),\quad\nu_n=\frac{(bc,ad;q)_n(-ad)^nq^{\binom n2}}{(abcd;q)_{2n}}\sum_{j=0}^{N-n}\frac{(adq^n,adq^n;q)_j}{(q,abcdq^{2n};q)_j}w_{n+j},\quad k_n=\frac{1-abcdq^{2n-1}}{1-abcd/q}\frac{(abcd/q,ab,ac,ad;q)_n}{(q,bc,bd,cd;q)_n}a^{-2n}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-9.5.3-finite`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-9.5.3-finite**（Chapter 9, 9.5.3-finite, 印刷p269）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。w_0…w_N任意且之后为0；r_n(z)=4φ3^[n](q^{-n},abcdq^{n−1},az,a/z;ab,ac,ad;q,q)，abcdzv≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-9.Ex17i · 终止 Askey–Wilson 双线性展开（修订）

$$
\sum_{n=0}^N\frac{(q^{-N},UVq^{N-1};q)_n(1-abcdq^{2n-1})(abcd/q,ab,ac,-ab;q)_nq^{n(n+1)/2}(d/a)^n}{(U,-V;q)_n(1-abcd/q)(q,bd;q)_n(abcd;q)_{2n}}{}_4\phi_3^{[N-n]}(q^{n-N},UVq^{n+N-1},abq^n,-cdq^n;abcdq^{2n},Uq^n,-Vq^n;q,q)r_n(z)r_n(v)=(-1)^N\frac{(-U,V;q)_N}{(U,-V;q)_N}\sum_{m=0}^N\frac{(q^{-N},UVq^{N-1},-ab,dz,d/z,dv,d/v;q)_mq^m}{(q,ad,ad,bd,-U,V,d/a;q)_m}W_{10}^{[m]}(aq^{-m}/d;q^{1-m}/(bd),q^{1-m}/(cd),q^{-m},az,a/z,av,a/v;q,bcq/(ad)).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-9.Ex17i`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-9.Ex17i**（Chapter 9, 9.Ex17i, 印刷p277）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。U=αβ,V=γδ非零；r同9.5.3-finite，原书未列额外参数关系。所有实际分母非零；见修订报告。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
