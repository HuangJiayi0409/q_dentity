# q-Clausen 与终止乘积/平方公式

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 本次未匹配到旧算法 11 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

## FQI-SRC-GR2-8.1.2 · 成对有限积的线性化

$$
(t,a/t;q)_j(t,a/t;q)_k=(q;q)_j(q;q)_k(a;q)_{j+k}\sum_{m=\max(j,k)}^{j+k}\frac{(t,a/t;q)_m(-1)^{j+k+m}q^{\binom j2+\binom k2+\binom{m+1}2-m(j+k)}}{(a;q)_m(q;q)_{m-j}(q;q)_{m-k}(q;q)_{j+k-m}}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-8.1.2`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-8.1.2**（Chapter 8, 8.1.2, 印刷p217）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。j,k≥0，t≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-8.1.4 · 任意序列的有限乘积展开

$$
\left[\sum_{j=0}^n\frac{(q^{-n},aq^n;q)_jB_j}{(q,b;q)_j}\right]\left[\sum_{k=0}^n\frac{(q^{-n},aq^n;q)_kC_k}{(q,c;q)_k}\right]=\sum_{m=0}^n(q^{-n},aq^n;q)_m\sum_{k=0}^m\frac{C_kq^{k^2-mk}}{(q,c;q)_k(q,b;q)_{m-k}}\sum_{j=0}^k\frac{(q^{-k},aq^m;q)_jB_{m-k+j}}{(q,bq^{m-k};q)_j}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-8.1.4`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-8.1.4**（Chapter 8, 8.1.4, 印刷p218）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。B_0…B_n,C_0…C_n任意。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-8.2.6 · Bailey 型终止 4φ3 乘积公式

$$
F_n(b,b_1,b_2,b_3)F_n(aq/b,c_1,c_2,aq/b_3)=S_n,\quad S_n=\sum_{m=0}^n\frac{(q^{-n},aq^n,c_1,c_2,qab_1/(bb_3),qab_2/(bb_3);q)_mq^m}{(q,aq/b,aq/b_3,aq/(bb_3),qab_1b_2/(bb_3),bb_3c_1c_2/(aq);q)_m}W_{10}^{[m]}(bb_3q^{-m-1}/a;b_1,b_2,bb_3c_1/(aq),bb_3c_2/(aq),bq^{-m}/a,b_3q^{-m}/a,q^{-m};q,aq^2/(b_1b_2c_1c_2)).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-8.2.6`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-8.2.6**（Chapter 8, 8.2.6, 印刷p219）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。F_n见8.2.5，所列乘除参数非零。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-8.2.12 · Bateman 型终止乘积公式

$$
F_n(b,b_1,b_2,b_3)F_n(b,bb_3c_1/(aq),bb_3/(b_1b_2c_1),b_3)=\frac{(aq/b,aq/b_3;q)_n}{(b,b_3;q)_n}\left(\frac{bb_3}{aq}\right)^n\sum_{m=0}^n\frac{(q^{-n},aq^n,b_1c_1,b_2c_1,aq/(b_1b_2c_1);q)_mq^m}{(q,aq/b,aq/b_3,b_1b_2c_1,bb_3/(b_1b_2);q)_m}W_{10}^{[m]}(\mu;b_1,b_2,b_1b_2c_1/b,b_1b_2c_1/b_3,bb_3c_1/(aq),aq^m,q^{-m};q,q),\quad\mu=b_1b_2c_1/q.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-8.2.12`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-8.2.12**（Chapter 8, 8.2.12, 印刷p220）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。F_n见8.2.5；8.2.6中c2=aq/(b1b2c1)。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-8.8.15 · 终止 q-Clausen 的多项式平方形式

$$
\left[{}_4\phi_3^{[n]}(q^{-n},\beta^2q^n,uz,u/z;\beta s,-\beta s,-\beta;q,q)\right]^2={}_5\phi_4^{[n]}(q^{-n},\beta^2q^n,\beta,\beta z^2,\beta/z^2;\beta^2,\beta s,-\beta s,-\beta;q,q),\quad u^2=\beta,\ s^2=q.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-8.8.15`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-8.8.15**（Chapter 8, 8.8.15, 印刷p235）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。βz≠0，相容平方根。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-8.9.2 · 终止 5φ4 的有限平方和

$$
{}_5\phi_4^{[n]}(q^{-n},Aq^n,B,Bz^2,B/z^2;B^2,h^2s,-h^2s,-B;q,q)=\sum_{k=0}^{\lfloor n/2\rfloor}\frac{(-1)^n(q^{-n},Aq^n,Bs,-Bs;q)_j(q,A/B^2;q^2)_k B^{2k}q^{2kj+k+j(j+1)/2}}{(q,h^2s,-h^2s,B^2q^j;q)_j(Aq^{2j+1},B^2q^{2j+2};q^2)_k}\left[{}_4\phi_3^{[j]}(q^{-j},B^2q^j,uz,u/z;Bs,-Bs,-B;q,q)\right]^2,\quad j=n-2k.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-8.9.2`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-8.9.2**（Chapter 8, 8.9.2, 印刷p237）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。A=h⁴，B=u²，s²=q，z≠0；原书q^a=A,q^b=B,e^{iθ}=z²。以乘法参数替代指数参数。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-8.9.5 · 终止 6φ5 的奇偶平方和

$$
{}_6\phi_5^{[n]}(q^{-n},Aq^n,B,-B,h^2z^2,h^2/z^2;B^2,h^2s,-h^2s,-h^2,-h^2;q,q)=\sum_{k=0}^{\lfloor n/2\rfloor}\frac{(q^{-n},Aq^n,h^2,h^2z^2,h^2/z^2;q)_{2k}(q,A/B^2;q^2)_kq^{2k^2+k}B^{2k}}{(q,h^2s,-h^2s,-h^2,Aq^{2k-1};q)_{2k}(A,B^2q;q^2)_k}\left[{}_4\phi_3^{[n-2k]}(q^{2k-n},Aq^{n+2k},hq^kz,hq^k/z;h^2sq^{2k},-h^2sq^{2k},-h^2q^{2k};q,q)\right]^2.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-8.9.5`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-8.9.5**（Chapter 8, 8.9.5, 印刷p238）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。A=h⁴，B=u²，s²=q，z≠0；原书q^a=A,q^b=B,e^{iθ}=z²。以乘法参数替代指数参数。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-8.9.9 · 一般终止 6φ5 的有限平方展开

$$
{}_6\phi_5^{[n]}(q^{-n},Aq^n,h^2,B,h^2z^2,h^2/z^2;h^2s,D,AB/D,-h^2s,-h^2;q,q)=\sum_{j=0}^n\frac{(q^{-n},Aq^n,h^2,A/D,D/B,h^2z^2,h^2/z^2;q)_j(-1)^jB^jq^{j(j+1)/2}}{(q,h^2s,-h^2s,-h^2,Aq^{j-1},D,AB/D;q)_j}\left[{}_4\phi_3^{[n-j]}(q^{j-n},Aq^{j+n},hs^jz,hs^j/z;h^2sq^j,-h^2sq^j,-h^2q^j;q,q)\right]^2.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-8.9.9`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-8.9.9**（Chapter 8, 8.9.9, 印刷p239）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。A=h⁴，B=u²，s²=q，z≠0；原书q^a=A,q^b=B,e^{iθ}=z²。以乘法参数替代指数参数。D=q^c非零。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-8.Ex17i · 二次底数 q-Clausen 平方公式

$$
\left[{}_4\phi_3^{[L]}(a^2,b^2,abz,ab/z;a^2b^2q,-ab,-abq;q^2,q^2)\right]^2={}_5\phi_4^{[R]}(a^2,b^2,ab,abz,ab/z;a^2b^2,abs,-abs,-ab;q,q),\quad s^2=q.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-8.Ex17i`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-8.Ex17i**（Chapter 8, 8.Ex17i, 印刷p251）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。所有级数均终止；例如a=q^{-n}时L=n,R=2n；或abz=q^{-2n}时L=n,R=2n；取各侧实际最短长度。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-8.Ex17ii · q² 底数的 Clausen 有限平方公式

$$
\left[{}_4\phi_3^{[L]}(a^2,b^2,abz,ab/z;abs,-abs,-a^2b^2;q,q)\right]^2={}_5\phi_4^{[R]}(a^4,b^4,a^2b^2,a^2b^2z^2,a^2b^2/z^2;a^4b^4,a^2b^2q,-a^2b^2q,-a^2b^2;q^2,q^2),\quad s^2=q.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-8.Ex17ii`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-8.Ex17ii**（Chapter 8, 8.Ex17ii, 印刷p251）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。所有级数均终止；例如a=q^{-n}时L=R=2n；或abz=q^{-n}时L=R=n；取各侧实际最短长度。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-III-22 · 终止 q-Clausen 平方公式

$$
\left[\sum_{k=0}^L\frac{(a,b,abz,ab/z;q)_kq^k}{(q,-ab;q)_k(a^2b^2q;q^2)_k}\right]^2=\sum_{k=0}^R\frac{(a^2,b^2,ab,abz,ab/z;q)_kq^k}{(q,-ab,a^2b^2;q)_k(a^2b^2q;q^2)_k}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-III-22`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-III-22**（Appendix III, (III.22), 印刷p361）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。z≠0，两侧均终止；abz=q^{-n}时L=R=n；a=q^{-n}时L=n、R=2n。互换a,b或z↦1/z同理。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
