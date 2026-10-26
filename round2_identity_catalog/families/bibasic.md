# 双底数、多底数与二次/三次变换

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 本次未匹配到旧算法 36 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

## FQI-SRC-GR2-1.Ex35 · 非交换有限 q 二项式的双底数表示

$$
(X+Y)^n=\sum_{k=0}^n\begin{bmatrix}n\\k\end{bmatrix}_qY^kX^{n-k}=\sum_{k=0}^n\begin{bmatrix}n\\k\end{bmatrix}_{q^{-1}}X^kY^{n-k},\qquad XY=qYX.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-1.Ex35`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-1.Ex35**（Chapter 1, 1.Ex35, 印刷p33）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。含幺结合代数，q与X,Y交换。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-3.6.6 · 双底数乘积的差分

$$
T_k-T_{k-1}=\frac{(1-ap^kq^k)(1-bp^kq^{-k})(a,b;p)_k(c,a/(bc);q)_kq^k}{(1-a)(1-b)(q,aq/b;q)_k(ap/c,bcp;p)_k},\quad T_k=\frac{(ap,bp;p)_k(cq,aq/(bc);q)_k}{(q,aq/b;q)_k(ap/c,bcp;p)_k},\quad T_{-1}=0.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-3.6.6`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-3.6.6**（Chapter 3, 3.6.6, 印刷p80）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。k≥0；abc≠0；p为另一合法底数。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-3.6.10 · 四参数双底数乘积差分

$$
S_k-S_{k-1}=\frac{d(1-c/d)(1-ad/(bc))(1-adp^kq^k)(1-bp^k/(dq^k))}{(1-a)(1-b)(1-c)(1-ad^2/(bc))}\frac{(a,b;p)_k(c,ad^2/(bc);q)_kq^k}{(dq,adq/b;q)_k(adp/c,bcp/d;p)_k},\quad S_k=\frac{(ap,bp;p)_k(cq,ad^2q/(bc);q)_k}{(dq,adq/b;q)_k(adp/c,bcp/d;p)_k}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-3.6.10`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-3.6.10**（Chapter 3, 3.6.10, 印刷p81）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。k为整数；abcd≠0；p为另一合法底数，负长度用有限倒积。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-3.6.16 · 终止双底数求和与消去

$$
\sum_{k=0}^n\frac{(1-adp^kq^k)(1-bp^k/(dq^k))(a,b;p)_k(q^{-n},ad^2q^n/b;q)_kq^k}{(1-ad)(1-b/d)(dq,adq/b;q)_k(adpq^n,bpq^{-n}/d;p)_k}=\frac{(1-d)(1-ad/b)(1-adq^n)(1-dq^n/b)}{(1-ad)(1-d/b)(1-dq^n)(1-adq^n/b)}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-3.6.16`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-3.6.16**（Chapter 3, 3.6.16, 印刷p83）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。abd≠0；p为另一底数。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-3.8.14 · 有限双底数和到二次 10φ9

$$
\sum_{k=0}^n\frac{1-acq^{3k}}{1-ac}\frac{(a,b,cq/b;q)_k(f,a^2c^2q^{2n+1}/f,q^{-2n};q^2)_kq^k}{(cq^2,acq^2/b,abq;q^2)_k(acq/f,fq^{-2n}/(ac),acq^{2n+1};q)_k}=\frac{(acq;q)_{2n}(ac^2q^2/(bf),abq/f;q^2)_n}{(acq/f;q)_{2n}(abq,ac^2q^2/b;q^2)_n}W_{10}^{[n]}(ac^2/b;f,ac/b,c,cq/b,cq^2/b,a^2c^2q^{2n+1}/f,q^{-2n};q^2,q^2).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-3.8.14`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-3.8.14**（Chapter 3, 3.8.14, 印刷p92）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。abcf≠0，ac≠1；W首参数≠1。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-3.8.15 · 长度两倍的有限双底数二次变换

$$
\sum_{k=0}^{2n}\frac{1-acq^{3k}}{1-ac}\frac{(d,f,a^2c^2q/(df);q^2)_k(a,cq^{2n+1},q^{-2n};q)_kq^k}{(acq/d,acq/f,df/(ac);q)_k(cq^2,aq^{1-2n},acq^{2n+2};q^2)_k}=\frac{(acq^2,dq/(ac),fq/(ac),acq^2/(df);q^2)_n}{(q/(ac),acq^2/d,acq^2/f,dfq/(ac);q^2)_n}W_{10}^{[n]}(acq^{-2n-1};c,d,f,a^2c^2q/(df),aq^{-2n-1},q^{1-2n},q^{-2n};q^2,q^2).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-3.8.15`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-3.8.15**（Chapter 3, 3.8.15, 印刷p92）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。acdf≠0，ac≠1；W首参数≠1。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-3.9.5 · 终止多底数级数的有限展开

$$
\sum_{k=0}^N\frac{(a,b,c;q)_k}{(q,aq/b,aq/c;q)_k}H_kz^k=\sum_{j=0}^N\frac{(aq/(bc);q)_j(a;q)_{2j}}{(q,aq/b,aq/c;q)_j}\left(-\frac{bcz}{aq}\right)^jq^{-j(j-1)/2}\sum_{k=0}^{N-j}\frac{(aq^{2j};q)_k}{(q;q)_k}H_{j+k}\left(\frac{bcz}{aq^{j+1}}\right)^k,\quad H_k=\prod_{i=1}^m\frac{(\boldsymbol c_i;q_i)_k}{(\boldsymbol d_i;q_i)_k}\left((-1)^kq_i^{k(k-1)/2}\right)^{s_i-r_i}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-3.9.5`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-3.9.5**（Chapter 3, 3.9.5, 印刷p95）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。各向量c_i长r_i，d_i长s_i；至少一上参数c_{i,j}=q_i^{-N}；abc≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-3.10.3 · Nassrallah–Rahman 有限二次变换

$$
\Phi_n[a^2,-aq^2,b^2,c^2;-a,a^2q^2/b^2,a^2q^2/c^2\mid-aq/w,q^{-n};w,-aq^{n+1};q^2,q;awq^{n+2}/(b^2c^2)]=\frac{(w/a,-aq;q)_n}{(w,-q;q)_n}{}_5\phi_4^{[n]}(a,aq,a^2q^2/w^2,a^2q^2/(b^2c^2),q^{-2n};a^2q^2/b^2,a^2q^2/c^2,aq^{1-n}/w,aq^{2-n}/w;q^2,q^2).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-3.10.3`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-3.10.3**（Chapter 3, 3.10.3, 印刷p97）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。abcw≠0；Φ为辅助说明中的有限双底数和。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-3.10.5 · 有限双底数求和（一）

$$
\Phi_n[a^2,aq^2,-aq^2;a,-a\mid-aq/w,q^{-n};w,-aq^{n+1};q^2,q;wq^{n-1}/a]=\frac{(-aq,aq^2/w,w/(aq);q)_n}{(-q,aq/w,w;q)_n}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-3.10.5`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-3.10.5**（Chapter 3, 3.10.5, 印刷p98）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。aw≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-3.10.6 · 有限双底数求和（二）

$$
\Phi_n[a^2,-aq^2,b^2;-a,a^2q^2/b^2\mid-aq^n/b^2,q^{-n};b^2q^{1-n},-aq^{n+1};q^2,q;q^2]=\frac{(q^n/b^2,-aq;q)_n(aq/b^2,aq^2/b^2;q^2)_n}{(aq^n/b^2,-q;q)_n(q/b^2,a^2q^2/b^2;q^2)_n}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-3.10.6`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-3.10.6**（Chapter 3, 3.10.6, 印刷p98）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。ab≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-3.10.7 · 有限双底数求和（三）

$$
\Phi_n[a^2,aq^2,-aq^2,b^2;a,-a,a^2q^2/b^2\mid-aq^n/b^2,q^{-n};b^2q^{1-n},-aq^{n+1};q^2,q;q]=\frac{(-aq,a/b^2;q)_nq^n(1/b^2;q^2)_n}{(-q,1/b^2;q)_n(a^2q^2/b^2;q^2)_n}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-3.10.7`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-3.10.7**（Chapter 3, 3.10.7, 印刷p98）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。ab≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-3.10.8 · 有限双底数求和（四）

$$
\Phi_n[a^2,aq^2,-aq^2,b^2;a,-a,a^2q^2/b^2\mid-aq^{n-1}/b^2,q^{-n};b^2q^{2-n},-aq^{n+1};q^2,q;q^2]=\frac{(-aq,a/(qb^2);q)_n(aq/b^2,1/(b^2q^2);q^2)_nq^n}{(-q,1/(qb^2);q)_n(a/(qb^2),a^2q^2/b^2;q^2)_n}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-3.10.8`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-3.10.8**（Chapter 3, 3.10.8, 印刷p98）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。ab≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-3.10.11 · 终止 4φ3 的二次变换

$$
{}_4\phi_3^{[n]}(a,b,-w/b,q^{-n};aq/b,-bq^{-n},w;q,q)=\frac{(w/a,-aq/b;q)_n}{(w,-q/b;q)_n}{}_4\phi_3^{[n]}(a,a^2q^2/w^2,aq/b^2,q^{-2n};a^2q^2/b^2,aq^{1-n}/w,aq^{2-n}/w;q^2,q^2).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-3.10.11`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-3.10.11**（Chapter 3, 3.10.11, 印刷p99）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。abw≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-3.10.14 · 第二类有限双底数二次变换

$$
\Phi_n[a^2,aq^2,-aq^2,b^2,c^2;a,-a,a^2q^2/b^2,a^2q^2/c^2\mid-aq/w,q^{-n};w,-aq^{n+1};q^2,q;awq^{n+1}/(b^2c^2)]=\frac{(-aq,aq^2/w,w/(aq);q)_n}{(-q,aq/w,w;q)_n}{}_5\phi_4^{[n]}(aq,aq^2,a^2q^2/(b^2c^2),a^2q^2/w^2,q^{-2n};a^2q^2/b^2,a^2q^2/c^2,aq^{2-n}/w,aq^{3-n}/w;q^2,q^2).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-3.10.14`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-3.10.14**（Chapter 3, 3.10.14, 印刷p99）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。abcw≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-3.10.15 · 有限双底数到 10φ9 的变换（一）

$$
\Phi_n[a^2,-aq^2,b^2,c^2,d^2;-a,a^2q^2/b^2,a^2q^2/c^2,a^2q^2/d^2\mid-\lambda q^{n+1}/a,q^{-n};a^2q^{-n}/\lambda,-aq^{n+1};q^2,q;q]=\frac{(-aq,\lambda q/a;q)_n(\lambda q^2/a^2;q^2)_n}{(-q,\lambda q/a^2;q)_n(\lambda q^2;q^2)_n}W_{10}^{[n]}(\lambda;a,aq,\lambda b^2/a^2,\lambda c^2/a^2,\lambda d^2/a^2,\lambda^2q^{2n+2}/a^2,q^{-2n};q^2,qa^2/\lambda),\quad\lambda=(qa^2/(bcd))^2.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-3.10.15`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-3.10.15**（Chapter 3, 3.10.15, 印刷p99）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。abcdλ≠0，λ≠1。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-3.10.16 · 有限双底数到 10φ9 的变换（二）

$$
\Phi_n[a^2,aq^2,-aq^2,b^2,c^2,d^2;a,-a,a^2q^2/b^2,a^2q^2/c^2,a^2q^2/d^2\mid-\lambda q^n/a,q^{-n};a^2q^{1-n}/\lambda,-aq^{n+1};q^2,q;q]=\frac{(\lambda/a,-aq;q)_n(\lambda/a^2;q^2)_nq^n}{(\lambda/a^2,-q;q)_n(\lambda q^2;q^2)_n}W_{10}^{[n]}(\lambda;aq,aq^2,\lambda b^2/a^2,\lambda c^2/a^2,\lambda d^2/a^2,\lambda^2q^{2n}/a^2,q^{-2n};q^2,qa^2/\lambda),\quad\lambda=(qa^2/(bcd))^2.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-3.10.16`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-3.10.16**（Chapter 3, 3.10.16, 印刷p100）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。abcdλ≠0，λ≠1。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-3.Ex3 · 终止 3φ2 的二次变换

$$
{}_3\phi_2^{[n]}(a,q/a,q^{-n};c,-q;q,q)=\frac{(-q^{1-n}/c;q)_n}{(-q^{-n};q)_n}{}_3\phi_2^{[n]}(c/a,ac/q,q^{-2n};c^2,0;q^2,q^2).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-3.Ex3`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-3.Ex3**（Chapter 3, 3.Ex3, 印刷p101）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。ac≠0；原书两侧终止条件取z=q^{-n}的显式共同分支。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-3.Ex12 · 倒序型有限双底数二次变换

$$
\Phi_n[q^{-2n},-q^{2-n},b^2,c^2;-q^{-n},q^{2-2n}/b^2,q^{2-2n}/c^2\mid d,-q^{1-n}/w;-q^{1-n}/d,w;q^2,q;wq^{2-n}/(b^2c^2d)]=\frac{(-1,w/d;q)_n}{(-d,w;q)_n}d^n{}_5\phi_4^{[\lfloor n/2\rfloor]}(d^2,q^{2-2n}/(b^2c^2),q^{2-2n}/w^2,q^{-n},q^{1-n};q^{2-2n}/b^2,q^{2-2n}/c^2,dq^{1-n}/w,dq^{2-n}/w;q^2,q^2).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-3.Ex12`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-3.Ex12**（Chapter 3, 3.Ex12, 印刷p103）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。bcdw≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-3.Ex13i · 有限双底数到 10φ9 的变换（三）

$$
\Phi_n[a^2,-aq^2,b^2,c^2,d^2;-a,a^2q^2/b^2,a^2q^2/c^2,a^2q^2/d^2\mid-\lambda q^n/a,q^{-n};a^2q^{1-n}/\lambda,-aq^{n+1};q^2,q;q^2]=\frac{(-aq,\lambda/a;q)_n(\lambda/a^2,\lambda q^2/a;q^2)_n}{(-q,\lambda/a^2;q)_n(\lambda q^2,\lambda/a;q^2)_n}W_{10}^{[n]}(\lambda;a,aq,\lambda b^2/a^2,\lambda c^2/a^2,\lambda d^2/a^2,\lambda^2q^{2n}/a^2,q^{-2n};q^2,a^2q^3/\lambda),\quad\lambda=a^4q^2/(b^2c^2d^2).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-3.Ex13i`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-3.Ex13i**（Chapter 3, 3.Ex13i, 印刷p104）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。abcdλ≠0，λ≠1。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-3.Ex13ii · 有限双底数到 10φ9 的变换（四）

$$
\Phi_n[a^2,aq^2,-aq^2,b^2,c^2,d^2;a,-a,a^2q^2/b^2,a^2q^2/c^2,a^2q^2/d^2\mid-\lambda q^{n-1}/a,q^{-n};a^2q^{2-n}/\lambda,-aq^{n+1};q^2,q;q^2]=\frac{(-aq,\lambda/(aq);q)_n(\lambda/(a^2q^2);q^2)_n(1-\lambda q^{2n-1}/a)q^n}{(-q,\lambda/(a^2q);q)_n(\lambda q^2;q^2)_n(1-\lambda/(aq))}W_{10}^{[n]}(\lambda;aq,aq^2,\lambda b^2/a^2,\lambda c^2/a^2,\lambda d^2/a^2,\lambda^2q^{2n-2}/a^2,q^{-2n};q^2,a^2q^3/\lambda),\quad\lambda=a^4q^2/(b^2c^2d^2).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-3.Ex13ii`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-3.Ex13ii**（Chapter 3, 3.Ex13ii, 印刷p104）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。abcdλ≠0，λ≠1。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-3.Ex21-mixed · 双底数与普通超几何的混合有限变换

$$
\sum_{k=0}^nK_k(a,b,c;p,q)\frac{(C-A-n)_k(-B-C-n)_k(\mu B-\mu A-n)_k(-n)_k}{(-\mu C-n)_k(\mu B+\mu C-\mu A-n)_k(-A-n)_k(-B-n)_k}=T_n(a,b,c;p,q)\frac{n!(\mu A+1-\mu B)_n(A+1-C)_n(B+C+1)_n}{(A+1)_n(B+1)_n(\mu C+1)_n(\mu A+1-\mu B-\mu C)_n}\sum_{k=0}^n\frac{(A+k+k/\mu)(B+k-k/\mu)}{AB}\frac{(A)_k(B)_k(\mu C)_k(\mu A-\mu B-\mu C)_k}{k!(\mu A+1-\mu B)_k(A+1-C)_k(B+C+1)_k}R_{n,k}(a,b,c;p,q).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-3.Ex21-mixed`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-3.Ex21-mixed**（Chapter 3, 3.Ex21-mixed, 印刷p106）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。K,T,R同四底数变换；(x)_k为普通上升阶乘；ABµabc≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-3.Ex21-quad · 四底数有限变换

$$
\sum_{k=0}^n K_k(a,b,c;p,q)R_{n,k}(A,B,C;P,Q)=\frac{T_n(a,b,c;p,q)}{T_n(A,B,C;P,Q)}\sum_{k=0}^nK_k(A,B,C;P,Q)R_{n,k}(a,b,c;p,q),\quad K_k=\frac{(1-ap^kq^k)(1-bp^kq^{-k})(a,b;p)_k(c,a/(bc);q)_kq^k}{(1-a)(1-b)(q,aq/b;q)_k(ap/c,bcp;p)_k},\quad T_n=\frac{(ap,bp;p)_n(cq,aq/(bc);q)_n}{(q,aq/b;q)_n(ap/c,bcp;p)_n},\quad R_{n,k}(a,b,c;p,q)=\frac{(cp^{-n}/a,p^{-n}/(bc);p)_k(q^{-n},bq^{-n}/a;q)_k}{(q^{-n}/c,bcq^{-n}/a;q)_k(p^{-n}/a,p^{-n}/b;p)_k}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-3.Ex21-quad`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-3.Ex21-quad**（Chapter 3, 3.Ex21-quad, 印刷p106）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。abcABC≠0；p,q,P,Q为合法底数。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-3.Ex31i · 有限三次变换（一）

$$
\sum_{k=0}^n\frac{1-acq^{4k}}{1-ac}\frac{(a,b;q)_k(cq/b;q)_{2k}(a^2bcq^{3n},q^{-3n};q^3)_kq^k}{(cq^3,acq^3/b;q^3)_k(ab;q)_{2k}(q^{1-3n}/(ab),acq^{3n+1};q)_k}=\frac{(1-acq^2)(1-ab/q^2)(1-abq^{3n})(1-acq^{3n})}{(1-acq^{3n+2})(1-abq^{3n-2})(1-ab)(1-ac)}\sum_{k=0}^n\frac{1-acq^{6k+2}}{1-acq^2}\frac{(aq^2,bq^2,cq^2/b,cq^3/b,a^2bcq^{3n},q^{-3n};q^3)_kq^{3k}}{(cq^3,acq^3/b,abq^3,abq^2,q^{5-3n}/(ab),acq^{3n+5};q^3)_k}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-3.Ex31i`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-3.Ex31i**（Chapter 3, 3.Ex31i, 印刷p109）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。ab≠0，ac≠1。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-3.Ex31ii · 有限三次变换（二）

$$
\sum_{k=0}^n\frac{(1-aq^{4k})(1-bq^{-2k})}{(1-a)(1-b)}\frac{(a,1/(ab);q)_k(abq;q)_{2k}(c,a/(bc);q^3)_kq^{3k}}{(q^3,a^2bq^3;q^3)_k(q/b;q)_{2k}(aq/c,bcq;q)_k}=\frac{(aq,bq;q)_n(cq^3,aq^3/(bc);q^3)_n}{(aq/c,bcq;q)_n(q^3,aq^3/b;q^3)_n}W_{10}^{[n]}(a/b;1/(ab^2),c,a/(bc),aq^{n+1},aq^{n+2},aq^{n+3},q^{-3n};q^3,q^3).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-3.Ex31ii`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-3.Ex31ii**（Chapter 3, 3.Ex31ii, 印刷p110）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。abc≠0，a,b,a/b≠1。所有实际分母非零；见修订报告。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-11.6.5-p0 · Macdonald 有限乘积望远镜求和

$$
\sum_{k=0}^nV_k\prod_{j=0}^{k-1}U_j=1-\prod_{j=0}^nU_j,\quad U_j=\frac{(1-b_j)(1-c_j)(1-d_j)(1-a_j^2/(b_jc_jd_j))}{(1-a_j/b_j)(1-a_j/c_j)(1-a_j/d_j)(1-b_jc_jd_j/a_j)},\quad V_j=\frac{(1-a_j)(1-a_j/(b_jc_j))(1-a_j/(b_jd_j))(1-a_j/(c_jd_j))}{(1-a_j/(b_jc_jd_j))(1-a_j/d_j)(1-a_j/c_j)(1-a_j/b_j)}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-11.6.5-p0`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-11.6.5-p0**（Chapter 11, 11.6.5-p0, 印刷p325）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。所有所用序列项非零；可含任意q依赖。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-11.6.6-p0 · 多底数有限双边求和

$$
\sum_{k=-m}^n\frac{(1-ad(rst/q)^k)(1-br^k/(dq^k))(1-cs^k/(dq^k))(1-adt^k/(bcq^k))}{(1-ad)(1-b/d)(1-c/d)(1-ad/(bc))}\frac{(a;rst/q^2)_k(b;r)_k(c;s)_k(ad^2/(bc);t)_kq^k}{(dq;q)_k(adst/(bq);st/q)_k(adrt/(cq);rt/q)_k(bcrs/(dq);rs/q)_k}=\frac{(1-a)(1-b)(1-c)(1-ad^2/(bc))}{d(1-ad)(1-b/d)(1-c/d)(1-ad/(bc))}\left[\frac{(arst/q^2;rst/q^2)_n(br;r)_n(cs;s)_n(ad^2t/(bc);t)_n}{(dq;q)_n(adst/(bq);st/q)_n(adrt/(cq);rt/q)_n(bcrs/(dq);rs/q)_n}-\frac{(c/(ad);rt/q)_{m+1}(d/(bc);rs/q)_{m+1}(1/d;q)_{m+1}(b/(ad);st/q)_{m+1}}{(1/c;s)_{m+1}(bc/(ad^2);t)_{m+1}(1/a;rst/q^2)_{m+1}(1/b;r)_{m+1}}\right].
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-11.6.6-p0`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-11.6.6-p0**（Chapter 11, 11.6.6-p0, 印刷p326）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。m,n≥0；abcdqrst非零，负指标用有限倒积。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-11.6.21-p0 · 有限支撑的多底数序列展开（修订）

$$
\sum_{j=0}^N\frac{A_jB_j(xw)^j}{(q;q)_j}=\sum_{n=0}^N\frac{(1-\gamma(rst/q)^n)(1-\sigma(r/q)^n)(-x)^nq^{n+\binom n2}}{(q;q)_n}\sum_{k=0}^{N-n}\frac{(1-\gamma\sigma^{-1}(st)^{n+k})B_{n+k}x^k(s/q)^{\binom{k+1}2}}{(s;s)_k(\gamma rs^{n+k}t/q;rt/q)_n(\sigma rs^{1-n-k}/q;rs/q)_n}\sum_{j=0}^n\frac{(1-\gamma\sigma^{-1}s^{n+k}t^nq^{j-n})(1-s^{-k}q^{j-n})(q^{-n};q)_j}{(1-s^{j-n-k})(q;q)_j}(\gamma\sigma^{-1}(st)^{n+1}q^{j-n-1};st/q)_{k-1}(\gamma\sigma^{-1}s^{n+k}t^{j+1};t)_{n-j-1}(\gamma rs^jt/q;rt/q)_j(\gamma(rst)^{j+1}q^{-j-2};rst/q^2)_{n-j-1}(\sigma rs^{1-j}/q;rs/q)_j(\sigma r^{j+1}q^{-j};r)_{n-j-1}A_jC_{j,n+k-j}w^jq^{n(j-n-k)}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-11.6.21-p0`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-11.6.21-p0**（Chapter 11, 11.6.21-p0, 印刷p330）：N≥0，B_j=0(j>N)，A_j任意，C_{j,0}=1。r,s,t,q,γ,σ非零，实际分母非零；负长度按有限倒积。j=n,k=0的相同零因子比先约为1；s=q时同理。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-11.Ex21-p0 · 有限二次求和的两个基本超几何分支

$$
\sum_{k=0}^n\frac{1-aq^{3k}}{1-a}\frac{(b,c,d;q)_k(e,f,q^{-2n};q^2)_kq^k}{(aq^2/b,aq^2/c,aq^2/d;q^2)_k(aq/e,aq/f,aq^{2n+1};q)_k}=\frac{(aq^2,a^2q^2/(bce),a^2q^2/(bde),aq^2/(cd);q^2)_n}{(a^2q^2/(be),aq^2/c,aq^2/d,a^2q^2/(bcde);q^2)_n}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-11.Ex21-p0`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-11.Ex21-p0**（Chapter 11, 11.Ex21-p0, 印刷p341）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。bcd=aq，ef=a²q^{2n+1}，且b=a或e=a；abcdef≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-11.Ex22-p0 · 有限三次求和的基本超几何分支

$$
\sum_{k=0}^n\frac{1-aq^{4k}}{1-a}\frac{(b,c;q)_k(d;q)_{2k}(e,q^{-3n};q^3)_kq^k}{(aq^3/b,aq^3/c;q^3)_k(aq/d;q)_{2k}(aq/e,aq^{3n+1};q)_k}=\frac{(aq^3,a^2q^3/(bce),a^2q^3/(bde),aq^3/(cd);q^3)_n}{(a^2q^3/(be),aq^3/c,aq^3/d,a^2q^3/(bcde);q^3)_n}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-11.Ex22-p0`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-11.Ex22-p0**（Chapter 11, 11.Ex22-p0, 印刷p341）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。bcd=aq，de=a²q^{3n+1}，b=a；abcde≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-11.Ex23ii · 12W11 到底数 q² 的 10W9 变换

$$
W_{12}^{[n]}(a;b,-b,c,-c,dq^n,-dq^n,q^{-n},-q^{-n},qa^2/\lambda^2;q,q)=\frac{(a^2q^2,d^2/\lambda^2,b^2d^2/a^2,c^2d^2/a^2;q^2)_n}{(d^2/a^2,q^2\lambda^2,a^2q^2/b^2,a^2q^2/c^2;q^2)_n}W_{10}^{[n]}(\lambda^2;b^2,c^2,d^2q^{2n},a^2q^2/\lambda^2,q^{-2n},-\lambda^2/a,-\lambda^2q/a;q^2,\lambda^2q/a^2),\quad\lambda=bcd/(aq).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-11.Ex23ii`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-11.Ex23ii**（Chapter 11, 11.Ex23ii, 印刷p341）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。abcd≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-11.Ex24ii · 底数 q² 的 12W11 到 10W9 变换

$$
W_{12}^{[\lfloor n/2\rfloor]}(a;a^2/\lambda^2,b,bq,c,cq,dq^n,dq^{n+1},q^{1-n},q^{-n};q^2,q^2)=\frac{(aq,d/\lambda,\lambda q/b,\lambda q/c;q)_n}{(\lambda q,d/a,aq/b,aq/c;q)_n}W_{10}^{[n]}(\lambda;a/\lambda,\mu,-\mu,b,c,dq^n,q^{-n};q,-q\lambda/a),\quad\lambda=bcd/(aq),\quad\mu^2=\lambda^2q/a.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-11.Ex24ii`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-11.Ex24ii**（Chapter 11, 11.Ex24ii, 印刷p342）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。abcd≠0；成对µ按有限积合并，不依赖选根。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-II-34 · Gosper 不定双底数有限求和

$$
\sum_{k=0}^n\frac{1-ap^kq^k}{1-a}\frac{(a;p)_k(c;q)_k}{(q;q)_k(ap/c;p)_k}c^{-k}=\frac{(ap;p)_n(cq;q)_n}{(q;q)_n(ap/c;p)_n}c^{-n}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-II-34`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-II-34**（Appendix II, (II.34), 印刷p358）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。c≠0，a≠1，p也是非零非单位根底数。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-II-35 · Gosper 双底数求和扩展

$$
\sum_{k=0}^n\frac{(1-ap^kq^k)(1-bp^kq^{-k})}{(1-a)(1-b)}\frac{(a,b;p)_k(c,a/(bc);q)_k}{(q,aq/b;q)_k(ap/c,bcp;p)_k}q^k=\frac{(ap,bp;p)_n(cq,aq/(bc);q)_n}{(q,aq/b;q)_n(ap/c,bcp;p)_n}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-II-35`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-II-35**（Appendix II, (II.35), 印刷p358）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。abc≠0，a,b≠1；p也是非零非单位根底数。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-II-36 · 有限双边双底数求和

$$
\sum_{k=-m}^n\frac{(1-adp^kq^k)(1-bp^k/(dq^k))}{(1-ad)(1-b/d)}\frac{(a,b;p)_k(c,ad^2/(bc);q)_k}{(dq,adq/b;q)_k(adp/c,bcp/d;p)_k}q^k=\frac{(1-a)(1-b)(1-c)(1-ad^2/(bc))}{d(1-ad)(1-b/d)(1-c/d)(1-ad/(bc))}\left[\frac{(ap,bp;p)_n(cq,ad^2q/(bc);q)_n}{(dq,adq/b;q)_n(adp/c,bcp/d;p)_n}-\frac{(c/(ad),d/(bc);p)_{m+1}(1/d,b/(ad);q)_{m+1}}{(1/c,bc/(ad^2);q)_{m+1}(1/a,1/b;p)_{m+1}}\right].
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-II-36`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-II-36**（Appendix II, (II.36), 印刷p358）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。m≥0，abcd≠0；p也是非零非单位根底数；负指标按有限倒积。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-II-37 · 双底数有限差分消去

$$
(1-a/q)(1-b/q)\sum_{k=0}^n\frac{(ap^k,bp^{-k};q)_{n-1}(1-ap^{2k}/b)}{(p;p)_k(p;p)_{n-k}(ap^k/b;p)_{n+1}}(-1)^kp^{k(k-1)/2}=\delta_{n,0}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-II-37`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-II-37**（Appendix II, (II.37), 印刷p358）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。ab≠0；p也是非零非单位根底数；n=0时长度−1按有限倒积。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-III-21 · Singh 有限二次变换

$$
\sum_{k=0}^L\frac{(A,B,c,d;q)_kq^k}{(q,-cd;q)_k(ABq;q^2)_k}=\sum_{k=0}^R\frac{(A,B,c^2,d^2;q^2)_kq^{2k}}{(q^2,ABq,-cd,-cdq;q^2)_k}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-III-21`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-III-21**（Appendix III, (III.21), 印刷p361）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。两侧均终止；例如c=q^{-n}时L=R=n，或A=q^{-2n}时L=2n、R=n。参数互换同理，提前终止时取各侧最小长度。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
