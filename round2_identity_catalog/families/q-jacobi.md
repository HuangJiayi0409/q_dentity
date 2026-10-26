# 小/大/连续 q-Jacobi

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 本次未匹配到旧算法 13 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

## FQI-SRC-GR2-1.Ex33 · 小 q-Jacobi 多项式的有限连接公式

$$
p_n(x;c,d;q)=\sum_{k=0}^n A_{k,n}p_k(x;a,b;q),\quad A_{k,n}=\frac{(-1)^kq^{k(k+1)/2}(q^{-n},aq,cdq^{n+1};q)_k}{(q,cq,abq^{k+1};q)_k}{}_3\phi_2^{[n-k]}\!\left[\begin{matrix}q^{k-n},cdq^{n+k+1},aq^{k+1}\\cq^{k+1},abq^{2k+2}\end{matrix};q,q\right].
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-1.Ex33`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-1.Ex33**（Chapter 1, 1.Ex33, 印刷p33）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。p_n(x;a,b;q)={}_2φ₁^{[n]}(q^{-n},abq^{n+1};aq;q,qx)。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-2.Ex29 · 终止级数的 q-Jacobi 型连接展开

$$
{}_{r+2}\phi_{r+1}^{[n]}(q^{-n},cdq^{n+1},\boldsymbol u;cq,\boldsymbol v;q,z)=\sum_{k=0}^n\frac{(-1)^kq^{k(k+1)/2}(aq,cdq^{n+1},q^{-n};q)_k}{(q,cq,abq^{k+1};q)_k}{}_3\phi_2^{[n-k]}(q^{k-n},cdq^{n+k+1},aq^{k+1};cq^{k+1},abq^{2k+2};q,q){}_{r+2}\phi_{r+1}^{[k]}(q^{-k},abq^{k+1},\boldsymbol u;aq,\boldsymbol v;q,z).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-2.Ex29`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-2.Ex29**（Chapter 2, 2.Ex29, 印刷p64）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。r≥0，u/v均长r。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-7.3.6 · 小 q-Jacobi 三项递推

$$
x\ell_n(x)=A_n(\ell_{n+1}(x)-\ell_n(x))-C_n(\ell_n(x)-\ell_{n-1}(x)),\quad A_n=-\frac{q^n(1-abq^{n+1})(1-aq^{n+1})}{(1-abq^{2n+1})(1-abq^{2n+2})},\quad C_n=-\frac{aq^n(1-q^n)(1-bq^n)}{(1-abq^{2n})(1-abq^{2n+1})}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-7.3.6`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-7.3.6**（Chapter 7, 7.3.6, 印刷p182）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。ℓ_n(x)=2φ1^[n](q^{-n},abq^{n+1};aq;q,qx)，ℓ_{−1}=0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-7.3.17 · 双重有限和的正交消去

$$
\sum_{j=0}^m\sum_{k=0}^n\frac{(q^{-m},abq^{m+1};q)_j(q^{-n},abq^{n+1};q)_kq^{j+k}}{(q;q)_j(q;q)_k(abq^2;q)_{j+k}}=\frac{(q^{-n},abq^{n+1};q)_n}{(abq^2;q)_{2n}}(abq^{n+2})^n\delta_{mn}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-7.3.17`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-7.3.17**（Chapter 7, 7.3.17, 印刷p183）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。0≤m≤n。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-7.Ex10 · 大 q-Jacobi 三项递推

$$
(x-1)J_n(x)=A_n(J_{n+1}(x)-J_n(x))+C_n(J_n(x)-J_{n-1}(x)),\quad A_n=\frac{(1-aq^{n+1})(1-cq^{n+1})(1-abq^{n+1})}{(1-abq^{2n+1})(1-abq^{2n+2})},\quad C_n=\frac{acq^{n+1}(1-q^n)(1-bq^n)(1-abq^n/c)}{(1-abq^{2n})(1-abq^{2n+1})}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-7.Ex10`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-7.Ex10**（Chapter 7, 7.Ex10, 印刷p202）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。J_n(x)=3φ2^[n](q^{-n},abq^{n+1},x;aq,cq;q,q)，c≠0，J_{−1}=0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-7.Ex32 · 两种连续 q-Jacobi 的反射关系

$$
\mathscr J_n(-z;A,B)=(-1)^n\mathscr J_n(z;B,A),\qquad\mathscr K_n(-z;A,B)=(-A/B)^n\mathscr K_n(z;B,A),\quad\mathscr K_n(z;A,B)=\frac{(A^2s;q)_n}{(q;q)_n}{}_4\phi_3^{[n]}(q^{-n},A^2B^2q^n,Az,A/z;A^2s,-AB,-ABs;q,q),\quad s^2=q.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-7.Ex32`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-7.Ex32**（Chapter 7, 7.Ex32, 印刷p207）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。ABz≠0；𝒥见9.Ex17ii条件，其定义不依赖连接公式。𝒦对应原书q^{(2α+1)/4}=A,q^{(2β+1)/4}=B。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-7.Ex41 · 小 q-Jacobi 的有限加法公式

$$
\ell_n(q^z;1,1)\ell_y(q^z;q^x,0)=\ell_n(q^{x+y};1,1)\ell_n(q^y;1,1)\ell_y(q^z;q^x,0)+\sum_{k=1}^n\frac{(q;q)_{x+y+k}(q;q)_{n+k}q^{k(k+y-n)}}{(q;q)_{x+y}(q;q)_{n-k}(q;q)_k^2}\ell_{n-k}(q^{x+y};q^k,q^k)\ell_{n-k}(q^y;q^k,q^k)\ell_{y+k}(q^z;q^x,0)+\sum_{k=1}^{\min(n,y)}\frac{(q;q)_y(q;q)_{n+k}q^{k(x+y-n+1)}}{(q;q)_{y-k}(q;q)_{n-k}(q;q)_k^2}\ell_{n-k}(q^{x+y-k};q^k,q^k)\ell_{n-k}(q^{y-k};q^k,q^k)\ell_{y-k}(q^z;q^x,0).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-7.Ex41`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-7.Ex41**（Chapter 7, 7.Ex41, 印刷p210）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。x,y,z,n非负整数；ℓ_n(t;a,b)=2φ1^[n](q^{-n},abq^{n+1};aq;q,qt)。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-8.Ex1i · 小 q-Jacobi 乘积的有限双和（一）

$$
\ell_n(x)\ell_n(y)=(-aq)^nq^{\binom n2}\frac{(bq;q)_n}{(aq;q)_n}\sum_{m=0}^n\frac{(q^{-n},abq^{n+1},x^{-1},y^{-1};q)_m}{(q,bq;q)_m}\left(\frac{xyq^{1-m}}a\right)^m\sum_{k=0}^m\frac{(q^{-m},b^{-1}q^{-m};q)_k(abxy)^kq^{k^2+2k}}{(q,aq,xq^{1-m},yq^{1-m};q)_k}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-8.Ex1i`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-8.Ex1i**（Chapter 8, 8.Ex1i, 印刷p245）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。ℓ=ℓ_n(·;a,b)，abxy≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-8.Ex1ii · 小 q-Jacobi 乘积的有限三重和

$$
\ell_n(x)\ell_n(y)=(-bq)^{-n}q^{-\binom n2}\frac{(bq;q)_n}{(aq;q)_n}\sum_{m=0}^n\frac{(q^{-n},abq^{n+1};q)_m}{(q,bq;q)_m}(-byq^2)^mq^{\binom m2}\sum_{k=0}^m\frac{(q^{-m},abq^{m+1};q)_k(xq)^k}{(q,aq;q)_k}{}_2\phi_1^{[m-k]}(q^{k-m},bxq;0;q,(by)^{-1}).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-8.Ex1ii`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-8.Ex1ii**（Chapter 8, 8.Ex1ii, 印刷p245）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。ℓ=ℓ_n(·;a,b)，by≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-8.Ex2 · 大 q-Jacobi 的有限乘积公式

$$
J_n(x)J_n(y)=(-aq)^nq^{\binom n2}\frac{(bq;q)_n}{(aq;q)_n}\sum_{m=0}^n\frac{(q^{-n},abq^{n+1},cq/x,cq/y;q)_m}{(q,bq,cq,cq;q)_m}(xy/a)^m{}_4\phi_3^{[m]}(q^{-m},b^{-1}q^{-m},x,y;aq,xq^{-m}/c,yq^{-m}/c;q,abq/c^2).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-8.Ex2`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-8.Ex2**（Chapter 8, 8.Ex2, 印刷p245）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。J=J_n(·;a,b,c)，abcxy≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-8.Ex24 · 连续 q-Jacobi 特例的有限线性化

$$
r_n(z)r_{n-m}(z)=\sum_{k=0}^{2(n-m)}c_kr_{m+k}(z),\quad c_k=\frac{(ab;q)_{2m}(ab;q)_{2n-2m}(q,-as,bs,-ab;q)_n}{(abq;q)_{2n}(q,-as,bs,-ab;q)_m(-q,as,-bs,ab;q)_{n-m}}\frac{(1-abq^{2m+2k})(abq^{2m},-q^{m+1},-bsq^m,a/b,a^2b^2q^{2n},q^{2m-2n};q)_kq^{n-m}s^ka^{-k}}{(1-ab)(q,-abq^m,-asq^m,b^2q^{2m+1},q^{2m-2n+1}/(ab),abq^{2n+1};q)_k}W_{10}^{[\lfloor k/2\rfloor]}(b^2q^{2m};b^2,b^2q^{2n+1},q^{2m-2n+1}/a^2,abq^{2m+k},abq^{2m+k+1},q^{1-k},q^{-k};q^2,q^2),\quad s^2=q.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-8.Ex24`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-8.Ex24**（Chapter 8, 8.Ex24, 印刷p253）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。0≤m≤n；r_j(z)=4φ3^[j](q^{-j},abq^j,sz,s/z;as,−bs,−q;q,q)，abz≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-9.2.2 · 小 q-Jacobi 的另一终止 2φ1 表示

$$
\ell_n(x;a,b)=\frac{(x^{-1};q)_n}{(aq;q)_n}(-x)^nq^{-\binom n2}{}_2\phi_1^{[n]}(q^{-n},bxq;xq^{1-n};q,aq^{n+1}).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-9.2.2`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-9.2.2**（Chapter 9, 9.2.2, 印刷p260）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。x≠0；ℓ见7.3.6。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-9.Ex17ii · 连续 q-Jacobi 的有限连接公式（归一化核正）

$$
\mathscr J_m(z;A,B)=\sum_{n=0}^mg(n,m)\mathscr J_n(z;U,V),\quad g(n,m)=\frac{(Aq,-Bq;q)_m(UVq,-q;q)_n(ABq^{m+1};q)_nq^{n(n-m)}}{(-q;q)_m(UVq;q)_{2n}(q;q)_{m-n}(Aq,-Bq;q)_n}{}_4\phi_3^{[m-n]}(q^{n-m},ABq^{n+m+1},Uq^{n+1},-Vq^{n+1};UVq^{2n+2},Aq^{n+1},-Bq^{n+1};q,q).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-9.Ex17ii`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-9.Ex17ii**（Chapter 9, 9.Ex17ii, 印刷p277）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。A=q^a,B=q^b,U=q^α,V=q^β；𝒥_j(z;A,B)=(Aq,−Bq;q)j/(q,−q;q)j ·4φ3^[j](q^{-j},ABq^{j+1},sz,s/z;Aq,−Bq,−q;q,q)，s²=q。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
