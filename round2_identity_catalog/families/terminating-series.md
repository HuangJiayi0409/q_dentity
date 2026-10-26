# 终止单底数超几何展开与降阶

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 仅相关路线，未覆盖本式 3 条；本次未匹配到旧算法 34 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

## FQI-SRC-GR2-1.Ex4ii · 任意阶终止基本超几何和反向求和

$$
{}_{r+1}\phi_s^{[n]}\!\left[\begin{matrix}a_1,\ldots,a_r,q^{-n}\\b_1,\ldots,b_s\end{matrix};q,z\right]=\frac{\prod_i(a_i;q)_n}{\prod_j(b_j;q)_n}(z/q)^n\left((-1)^nq^{n(n-1)/2}\right)^{s-r-1}\sum_{k=0}^n\frac{(q^{-n};q)_k\prod_j(q^{1-n}/b_j;q)_k}{(q;q)_k\prod_i(q^{1-n}/a_i;q)_k}\left(\frac{\prod_jb_j}{\prod_ia_i}\frac{q^{n+1}}z\right)^k.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-1.Ex4ii`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

**新框架：任意阶有限反向求和**。[qreverse_framework](../../finite_product_framework/docs/q_reverse.md)采用指标反射与列表乘积规则，公共组装已证；单参数补长度、终止因子反射、指数/前因子整理三块局部义务尚存。CAS仅预留接口，未调用或实现后端，不计为完整证明。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-1.Ex4ii**（Chapter 1, 1.Ex4ii, 印刷p25）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。r,s≥0；a_i,b_j,z非零。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-1.Ex5 · 有限乘积的终止展开

$$
\frac{(c,bq^n;q)_m}{(b;q)_m}=\frac{(b/c;q)_n}{(b;q)_n}\sum_{k=0}^n\frac{(q^{-n},c;q)_k}{(q,cq^{1-n}/b;q)_k}q^k(cq^k;q)_m.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-1.Ex5`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

**新增完整证明：共享有限Chu核的结构求值**。[两条算法及CLI](../../finite_product_framework/docs/q_basic_evaluation.md)已完成；公共核独立保存于Common/FiniteChuEvaluation.lean。Ex5走乘积吸收/反射/拼接，Ex6(i)走奇偶换底/乘积拆分；原有限分母条件内无sorry、无需CAS，支持零分子及Ex6(i)的b=0。已分别注册qproduct_expansion_framework与qdouble_step_framework，拒绝交叉路由。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-1.Ex5**（Chapter 1, 1.Ex5, 印刷p26）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。m≥0，bc≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-1.Ex6i · 双步长终止 2φ1 求和

$$
{}_2\phi_1^{[\lfloor n/2\rfloor]}\!\left[\begin{matrix}q^{-n},q^{1-n}\\qb^2\end{matrix};q^2,q^2\right]=\frac{(b^2;q^2)_n}{(b^2;q)_n}q^{-n(n-1)/2}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-1.Ex6i`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

**新增完整证明：共享有限Chu核的结构求值**。[两条算法及CLI](../../finite_product_framework/docs/q_basic_evaluation.md)已完成；公共核独立保存于Common/FiniteChuEvaluation.lean。Ex5走乘积吸收/反射/拼接，Ex6(i)走奇偶换底/乘积拆分；原有限分母条件内无sorry、无需CAS，支持零分子及Ex6(i)的b=0。已分别注册qproduct_expansion_framework与qdouble_step_framework，拒绝交叉路由。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-1.Ex6i**（Chapter 1, 1.Ex6i, 印刷p26）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-1.Ex6iii · 终止 2φ0 求值

$$
{}_2\phi_0^{[n]}\!\left[\begin{matrix}a,q^{-n}\\-\end{matrix};q,q^n/a\right]=a^{-n}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-1.Ex6iii`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

**新增完整证明：终止2φ0的卷积归约**。[实现](../../finite_product_framework/docs/q_two_phi_zero.md)沿用qproduct_convolution_framework，终止因子转Gaussian、相位消去及已有卷积特化均已闭合。任意Field、q/a非零、有限阶乘分母非零；不要求分子非零，无CAS、无sorry。CLI/tactic共用结构识别，不新增入口。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-1.Ex6iii**（Chapter 1, 1.Ex6iii, 印刷p26）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。a≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-1.Ex15i · Jackson 终止 2φ1 到 3φ2 变换

$$
{}_2\phi_1^{[n]}\!\left[\begin{matrix}q^{-n},b\\c\end{matrix};q,z\right]=(bzq^{-n}/c;q)_n\,{}_3\phi_2^{[n]}\!\left[\begin{matrix}q^{-n},c/b,0\\c,cq/(bz)\end{matrix};q,q\right].
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-1.Ex15i`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-1.Ex15i**（Chapter 1, 1.Ex15i, 印刷p28）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。bcz≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-1.Ex17 · Carlitz 有限变换

$$
\sum_{k=0}^n\frac{(a,b;q)_k}{(q;q)_k}(-ab)^{n-k}q^{(n-k)(n+k-1)/2}=(a;q)_{n+1}\sum_{k=0}^n\frac{(-b)^kq^{k(k-1)/2}}{(q;q)_k(q;q)_{n-k}(1-aq^{n-k})}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-1.Ex17`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-1.Ex17**（Chapter 1, 1.Ex17, 印刷p28）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-2.2.4 · 终止基本超几何级数的降阶展开

$$
{}_{r+4}\phi_{r+3}^{[n]}(a,b,c,\boldsymbol u,q^{-n};aq/b,aq/c,\boldsymbol v;q,z)=\sum_{j=0}^n\frac{(aq/(bc),\boldsymbol u,q^{-n};q)_j(a;q)_{2j}}{(q,aq/b,aq/c,\boldsymbol v;q)_j}\left(-\frac{bcz}{aq}\right)^jq^{-j(j-1)/2}{}_{r+2}\phi_{r+1}^{[n-j]}(aq^{2j},q^j\boldsymbol u,q^{j-n};q^j\boldsymbol v;q,bcz/(aq^{j+1})).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-2.2.4`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-2.2.4**（Chapter 2, 2.2.4, 印刷p41）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。r≥0；u长度r，v长度r+1；abc≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-2.3.2 · 终止 Bailey–Daum 的有限积求值

$$
{}_2\phi_1^{[m]}(A,q^{-m};Aq^{m+1};q,-q^{m+1})=(-q;q)_m\frac{(Aq;q^2)_{\ell}}{(Aq^{2\lfloor m/2\rfloor+2};q^2)_{\ell}},\quad\ell=\lceil m/2\rceil.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-2.3.2`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-2.3.2**（Chapter 2, 2.3.2, 印刷p41）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。m≥0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-2.Ex6 · 终止 4φ3 的奇偶求和

$$
{}_4\phi_3^{[n]}(q^{-n},b,c,-q^{1-n}/(bc);q^{1-n}/b,q^{1-n}/c,-bc;q,q)=\begin{cases}0,&n=2m+1,\\\dfrac{(q,b^2,c^2;q^2)_m(bc;q)_{2m}}{(b,c;q)_{2m}(b^2c^2;q^2)_m},&n=2m.\end{cases}
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-2.Ex6`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-2.Ex6**（Chapter 2, 2.Ex6, 印刷p58）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。bc≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-2.Ex8 · Andrews 终止奇偶求和

$$
\sum_{k=0}^n\frac{(q^{-n},a;q)_k(b;q^2)_kq^k}{(q,b;q)_k(aq^{1-n};q^2)_k}=\begin{cases}0,&n=2m+1,\\\dfrac{(q,bq/a;q^2)_m}{(bq,q/a;q^2)_m},&n=2m.\end{cases}
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-2.Ex8`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-2.Ex8**（Chapter 2, 2.Ex8, 印刷p59）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。a≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-2.Ex14i · Bailey 的终止 4φ3 求和

$$
{}_4\phi_3^{[n]}(s^2,qs,b,q^{-n};s,s^2q/b,b^2q^{1-n};q,q)=\frac{(s^2/b^2,1/b,-qs/b;q)_n}{(1/b^2,s^2q/b,-s/b;q)_n}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-2.Ex14i`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

**新框架：局部归纳与有限展开**。已构建[Ex14(i)/(ii)受限域framework](../../finite_product_framework/docs/q_nearly_poised_ex14.md)，分别保留1/4项义务；内层求和侧递推尚未证明，未搜得或提供望远镜证书。本轮未调用CAS，暂不计入完整证明或完成覆盖。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-2.Ex14i**（Chapter 2, 2.Ex14i, 印刷p60）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。b≠0；以s代原书a^{1/2}。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-2.Ex27 · 平衡参数对的终止级数展开

$$
{}_{r+3}\phi_{r+2}^{[n]}(q^{-n},c,ab/c,\boldsymbol u;a,b,\boldsymbol v;q,z)=\frac{(c,ab/c;q)_n}{(a,b;q)_n}\sum_{k=0}^n\frac{(q^{-n},c/a,c/b;q)_kq^k}{(q,c,cq^{1-n}/(ab);q)_k}{}_{r+2}\phi_{r+1}^{[n-k]}(q^{k-n},c,\boldsymbol u;cq^k,\boldsymbol v;q,z).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-2.Ex27`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-2.Ex27**（Chapter 2, 2.Ex27, 印刷p64）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。r≥0，u/v均长r，abc≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-2.Ex35i · 终止3φ2有限卷积

$$
{}_3\phi_2^{[n]}(\alpha,\beta,q^{-n};\gamma,\delta;q,q)=\sum_{k=0}^n\begin{bmatrix}n\\k\end{bmatrix}_q\frac{(\lambda,\mu\delta/(\alpha\beta);q)_k(\gamma/\lambda;q)_{n-k}}{(\gamma;q)_n(\delta;q)_k}\lambda^n(\alpha\beta/(\lambda\mu))^k{}_3\phi_2^{[k]}(\mu/\alpha,\mu/\beta,q^{-k};\lambda,\delta\mu/(\alpha\beta);q,q){}_3\phi_2^{[n-k]}(\alpha\beta/\mu,\mu/\lambda,q^{k-n};\gamma/\lambda,\delta q^k;q,q).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-2.Ex35i`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-2.Ex35i**（Exercise 2.Ex35i）：参数非零、分母非零；所有实际分母非零；见修订报告。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-2.Ex35ii · Gasper 离散分式积分的有限展开（二）

$$
{}_3\phi_2^{[n]}(\alpha,\beta,q^{-n};\gamma,\delta;q,q)=\sum_{k=0}^n\begin{bmatrix}n\\k\end{bmatrix}_q\frac{(\lambda,\delta/\sigma;q)_k(\gamma/\lambda;q)_{n-k}}{(\gamma;q)_n(\delta;q)_k}\lambda^n(\sigma/\lambda)^k{}_3\phi_2^{[k]}(\alpha/\sigma,\beta,q^{-k};\lambda,\delta/\sigma;q,q){}_3\phi_2^{[n-k]}(\sigma,\beta/\lambda,q^{k-n};\gamma/\lambda,\delta q^k;q,q).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-2.Ex35ii`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-2.Ex35ii**（Chapter 2, 2.Ex35ii, 印刷p66）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。λσ≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-2.Ex35iii · Gasper 离散分式积分的有限展开（三）

$$
{}_3\phi_2^{[n]}(\alpha,\beta,q^{-n};\gamma,\delta;q,q)=\sum_{k=0}^n\begin{bmatrix}n\\k\end{bmatrix}_q\frac{(\nu;q)_n(\lambda;q)_k(\gamma\mu/(\lambda\nu);q)_{n-k}}{(\gamma,\mu;q)_n}\lambda^{n-k}{}_3\phi_2^{[n-k]}(\mu/\nu,\gamma/\nu,q^{k-n};\gamma\mu/(\lambda\nu),q^{1-n}/\nu;q,q^{1-k}/\lambda){}_4\phi_3^{[k]}(\alpha,\beta,\mu,q^{-k};\lambda,\nu,\delta;q,q).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-2.Ex35iii`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-2.Ex35iii**（Chapter 2, 2.Ex35iii, 印刷p66）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。γλµν≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-2.Ex36i · 平衡终止4φ3有限卷积

$$
{}_4\phi_3^{[n]}(\alpha,\beta,\nu q^n,q^{-n};\gamma,\delta,\rho;q,q)=\frac{(\gamma/\lambda,\nu q/\gamma;q)_n}{(\gamma,\lambda\nu q/\gamma;q)_n}\lambda^n\sum_{k=0}^n\frac{(\lambda\nu/\gamma,\lambda,\delta\mu/(\alpha\beta),\mu\rho/(\alpha\beta),\nu q^n,q^{-n};q)_k(\lambda\nu q/\gamma;q)_{2k}}{(q,\nu q/\gamma,\rho,\delta,\lambda q^{1-n}/\gamma,\lambda\nu q^{n+1}/\gamma;q)_k(\lambda\nu/\gamma;q)_{2k}}(\delta\rho/(\mu\nu))^k{}_4\phi_3^{[k]}(\mu/\alpha,\mu/\beta,\lambda\nu q^k/\gamma,q^{-k};\lambda,\delta\mu/(\alpha\beta),\mu\rho/(\alpha\beta);q,q){}_4\phi_3^{[n-k]}(\alpha\beta/\mu,\mu/\lambda,\nu q^{k+n},q^{k-n};\gamma/\lambda,\delta q^k,\rho q^k;q,q).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-2.Ex36i`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-2.Ex36i**（Exercise 2.Ex36i）：n≥0，αβνq=δγρ；所有参数非零，实际分母非零。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-2.Ex36ii · 平衡终止 4φ3 的双级数展开

$$
{}_4\phi_3^{[n]}(\alpha,\beta,\nu q^n,q^{-n};\gamma,\delta,\rho;q,q)=\frac{(\gamma/\lambda,\nu q/\gamma;q)_n}{(\gamma,\lambda\nu q/\gamma;q)_n}\lambda^n\sum_{k=0}^n\frac{(\lambda\nu/\gamma,\lambda,\rho/\alpha,\delta/\sigma,\nu q^n,q^{-n};q)_k(\lambda\nu q/\gamma;q)_{2k}}{(q,\nu q/\gamma,\delta,\rho\sigma/\alpha,\lambda q^{1-n}/\gamma,\nu\lambda q^{n+1}/\gamma;q)_k(\lambda\nu/\gamma;q)_{2k}}(\sigma q/\gamma)^k{}_4\phi_3^{[k]}(\alpha/\sigma,\beta,\lambda\nu q^k/\gamma,q^{-k};\lambda,\delta/\sigma,\rho;q,q){}_4\phi_3^{[n-k]}(\sigma,\beta/\lambda,\nu q^{n+k},q^{k-n};\gamma/\lambda,\delta q^k,\sigma\rho q^k/\alpha;q,q).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-2.Ex36ii`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-2.Ex36ii**（Chapter 2, 2.Ex36ii, 印刷p67）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。αβνq=δγρ；αλγσν≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-2.Ex36iii · 任意阶终止级数的 Gasper 展开

$$
{}_{r+2}\phi_{s+1}^{[n]}(q^{-n},\nu,\boldsymbol a;\gamma,\boldsymbol b;q,z)=\frac{(\lambda,\nu;q)_n}{(\gamma,\mu;q)_n}\sum_{k=0}^n\frac{(q^{-n},\gamma\mu/(\lambda\nu);q)_{n-k}}{(q,q^{1-n}/\lambda;q)_{n-k}}q^{n-k}{}_3\phi_2^{[n-k]}(\mu/\nu,\gamma/\nu,q^{k-n};\gamma\mu/(\lambda\nu),q^{1-n}/\nu;q,q^{1-k}/\lambda){}_{r+2}\phi_{s+1}^{[k]}(q^{-k},\mu,\boldsymbol a;\lambda,\boldsymbol b;q,z).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-2.Ex36iii`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-2.Ex36iii**（Chapter 2, 2.Ex36iii, 印刷p67）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。r,s≥0，a长r、b长s；λν≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-3.2.6 · 终止 type-II 3φ2 变换

$$
{}_3\phi_2^{[n]}(q^{-n},aq^n,b;d,e;q,de/(ab))=\frac{(aq/d,aq/e;q)_n}{(d,e;q)_n}(de/(aq))^n{}_3\phi_2^{[n]}(q^{-n},aq^n,abq/(de);aq/d,aq/e;q,q/b).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-3.2.6`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-3.2.6**（Chapter 3, 3.2.6, 印刷p71）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。abde≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-3.Ex4-odd · 有限 3φ1 的奇数消去

$$
\sum_{k=0}^{2m+1}\frac{(q^{-2m-1},b,-b;q)_k}{(q,b^2;q)_k}q^{(2m+1)k-k(k-1)/2}=0.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-3.Ex4-odd`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-3.Ex4-odd**（Chapter 3, 3.Ex4-odd, 印刷p101）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。m≥0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-3.Ex4-transform · 终止 4φ3(q²) 到 4φ2(q)

$$
{}_4\phi_3^{[\lfloor n/2\rfloor]}(q^{-n},q^{1-n},a,aq;qb^2,d,dq;q^2,q^2)=\frac{(d/a;q)_n}{(d;q)_n}a^n{}_4\phi_2^{[n]}(q^{-n},a,b,-b;b^2,aq^{1-n}/d;q,-q/d).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-3.Ex4-transform`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-3.Ex4-transform**（Chapter 3, 3.Ex4-transform, 印刷p101）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。ad≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-3.Ex34 · 二次底数的终止 4φ3 求和

$$
{}_4\phi_3^{[n]}(q^{-2n},c^2,a,qa;q^2a^2,cq^{-n},cq^{1-n};q^2,q^2)=\frac{(-q,qa/c;q)_n}{(-aq,q/c;q)_n}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-3.Ex34`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-3.Ex34**（Chapter 3, 3.Ex34, 印刷p110）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。c≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-8.2.5 · 两个平衡终止 4φ3 的一般乘积展开

$$
F_n(b,b_1,b_2,b_3)F_n(c,c_1,c_2,c_3)=\sum_{m=0}^n\frac{(q^{-n},aq^n,c_1,c_2,qab_1/(bb_3),qab_2/(bb_3);q)_mq^m}{(q,c,c_3,qa/(bb_3),qac_1c_2/(cc_3),qab_1b_2/(bb_3);q)_m}\sum_{j=0}^m\frac{1-\lambda_mq^{2j}}{1-\lambda_m}\frac{(\lambda_m,b_1,b_2,bq^{-m}/a,b_3q^{-m}/a,q^{-m};q)_j}{(q,bb_3q^{-m}/(ab_1),bb_3q^{-m}/(ab_2),b_3,b,bb_3/a;q)_j}\left(\frac{bb_3q^m}{b_1b_2}\right)^j{}_5\phi_4^{[j]}(q^{-j},q^{1-m}/c,q^{1-m}/c_3,\lambda_mq^j,cc_3q^{-m}/(ac_1c_2);q^{1-m}/c_1,q^{1-m}/c_2,bq^{-m}/a,b_3q^{-m}/a;q,q),\quad\lambda_m=bb_3q^{-m-1}/a.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-8.2.5`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-8.2.5**（Chapter 8, 8.2.5, 印刷p219）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。F_n(d,u,v,w)=4φ3^[n](q^{-n},aq^n,u,v;d,w,qauv/(dw);q,q)；所列乘除参数非零。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-8.9.1 · 终止 5φ4 的有限乘积展开

$$
{}_5\phi_4^{[n]}(q^{-n},Aq^n,B,Bz^2,B/z^2;B^2,h^2s,-h^2s,-B;q,q)=\sum_{j=0}^n\frac{(q^{-n},Aq^n,Bs,-Bs;q)_j(-1)^jq^{j(j+1)/2}}{(q,h^2s,-h^2s,B^2q^j;q)_j}{}_4\phi_3^{[n-j]}(q^{j-n},Aq^{j+n},Bsq^j,-Bsq^j;B^2q^{2j+1},h^2sq^j,-h^2sq^j;q,q){}_5\phi_4^{[j]}(q^{-j},B^2q^j,B,Bz^2,B/z^2;B^2,Bs,-Bs,-B;q,q).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-8.9.1`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-8.9.1**（Chapter 8, 8.9.1, 印刷p237）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。A=h⁴，B=u²，s²=q，z≠0；原书q^a=A,q^b=B,e^{iθ}=z²。以乘法参数替代指数参数。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-10.Ex18 · 终止 q-Kampé de Fériet 双重求和

$$
\sum_{j=0}^n\sum_{k=0}^{n-j}\frac{(q^{-n};q)_{j+k}(a/c,c/d,c/e;q)_j(c/a,b/d,b/e;q)_kq^{j+k}}{(bc/(de);q)_{j+k}(q,a,q^{1-n}/b;q)_j(q,b,q^{1-n}/a;q)_k}=\frac{(c,ab/c;q)_n}{(a,b;q)_n}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-10.Ex18`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-10.Ex18**（Chapter 10, 10.Ex18, 印刷p300）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。abcde≠0；原印Φ_{1:2;2}^{1:3;3}按10.2.10展开，指数修正全为0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-III-06 · 终止 2φ1 到 3φ2 变换（一）

$$
{}_2\phi_1^{[n]}\!\left[\begin{matrix}q^{-n},b\\c\end{matrix};q,z\right]=\frac{(c/b;q)_n}{(c;q)_n}(bz/q)^n{}_3\phi_2^{[n]}\!\left[\begin{matrix}q^{-n},q/z,q^{1-n}/c\\bq^{1-n}/c,0\end{matrix};q,q\right]
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-III-06`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-III-06**（Appendix III, (III.6), 印刷p359）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。n 为非负整数；q 为非零且非单位根的复数；所有显示的分母非零。 b,c,z≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-III-07 · 终止 2φ1 到 3φ2 变换（二）

$$
{}_2\phi_1^{[n]}\!\left[\begin{matrix}q^{-n},b\\c\end{matrix};q,z\right]=\frac{(c/b;q)_n}{(c;q)_n}{}_3\phi_2^{[n]}\!\left[\begin{matrix}q^{-n},b,bzq^{-n}/c\\bq^{1-n}/c,0\end{matrix};q,q\right]
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-III-07`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-III-07**（Appendix III, (III.7), 印刷p359）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。n 为非负整数；q 为非零且非单位根的复数；所有显示的分母非零。 b,c≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-III-08 · 终止 2φ1 到 3φ1 变换（第二版原印）

$$
{}_2\phi_1^{[n]}\!\left[\begin{matrix}q^{-n},b\\c\end{matrix};q,z\right]=b^n\frac{(c/b;q)_n}{(c;q)_n}{}_3\phi_1^{[n]}\!\left[\begin{matrix}q^{-n},b,q/z\\bq^{1-n}/c\end{matrix};q,z/c\right]
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-III-08`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-III-08**（Appendix III, (III.8), 印刷p359）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。n 为非负整数；q 为非零且非单位根的复数；所有显示的分母非零。 b,c,z≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-III-11 · 终止 3φ2 变换（一）

$$
{}_3\phi_2^{[n]}\!\left[\begin{matrix}q^{-n},b,c\\d,e\end{matrix};q,q\right]=\frac{(de/(bc);q)_n}{(e;q)_n}(bc/d)^n{}_3\phi_2^{[n]}\!\left[\begin{matrix}q^{-n},d/b,d/c\\d,de/(bc)\end{matrix};q,q\right]
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-III-11`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-III-11**（Appendix III, (III.11), 印刷p360）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。n 为非负整数；q 为非零且非单位根的复数；所有显示的分母非零。 b,c,d≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-III-12 · 第二版确认的终止 3φ2 变换

$$
{}_3\phi_2^{[n]}\!\left[\begin{matrix}q^{-n},b,c\\d,e\end{matrix};q,q\right]=c^n\frac{(e/c;q)_n}{(e;q)_n}{}_3\phi_2^{[n]}\!\left[\begin{matrix}q^{-n},c,d/b\\d,cq^{1-n}/e\end{matrix};q,bq/e\right]
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-III-12`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-III-12**（Appendix III, (III.12), 印刷p360）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。bce≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-III-13 · 终止 3φ2 变换（三）

$$
{}_3\phi_2^{[n]}\!\left[\begin{matrix}q^{-n},b,c\\d,e\end{matrix};q,deq^n/(bc)\right]=\frac{(e/c;q)_n}{(e;q)_n}{}_3\phi_2^{[n]}\!\left[\begin{matrix}q^{-n},c,d/b\\d,cq^{1-n}/e\end{matrix};q,q\right]
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-III-13`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-III-13**（Appendix III, (III.13), 印刷p360）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。n 为非负整数；q 为非零且非单位根的复数；所有显示的分母非零。 b,c,e≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AQ-2.40 · 终止 Heine 变换的有限乘积形式

$$
\sum_{j=0}^n\frac{(a,q^{-n};q)_jz^j}{(q,c;q)_j}=\frac1{(c;q)_n}\sum_{j=0}^n\frac{(q^{-n},azq^{-n}/c;q)_j(cq^n)^j}{(q;q)_j}(zq^{j-n};q)_{n-j}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AQ-2.40`。

**证明算法状态：仅相关路线，未覆盖本式**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SRC-AQ-2.40)

方法：旧 Heine 解析变换仅作相关路线。

覆盖边界：无限级数发射器不直接接受当前有限输入；不能按 Heine 名称判定覆盖。

定义文件：[ANDREWS_Q_supplement.md](../../round1_source_collection/records/ANDREWS_Q_supplement.md)；[ANDREWS_Q.md](../../round1_source_collection/books/ANDREWS_Q.md)。

- **AQ-2.40**（印刷页 15；式 (2.40)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 n≥0，q,c≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AQ-3.12 · Rogers 奇指标抵消和

$$
\sum_{r=-n-1}^{n}(-1)^rq^{3r(r+1)/2}\begin{bmatrix}2n+1\\n-r\end{bmatrix}_q=0.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AQ-3.12`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_Q_supplement.md](../../round1_source_collection/records/ANDREWS_Q_supplement.md)；[ANDREWS_Q.md](../../round1_source_collection/books/ANDREWS_Q.md)。

- **AQ-3.12**（印刷页 23；式 (3.12)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 n≥0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AQ-3.17 · Rogers 有限交错和（奇上指标）

$$
\sum_{r=-n}^{n-1}(-1)^rq^{r(3r+1)/2}\begin{bmatrix}2n-1\\n-1-r\end{bmatrix}_q=(q^n;q)_n.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AQ-3.17`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_Q_supplement.md](../../round1_source_collection/records/ANDREWS_Q_supplement.md)；[ANDREWS_Q.md](../../round1_source_collection/books/ANDREWS_Q.md)。

- **AQ-3.17**（印刷页 22,23；式 (3.17)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 n≥1。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AQ-3.18 · Rogers 有限交错和（偶上指标）

$$
\sum_{r=-n}^{n}(-1)^rq^{r(3r+1)/2}\begin{bmatrix}2n\\n-r\end{bmatrix}_q=(q^{n+1};q)_n.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AQ-3.18`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_Q_supplement.md](../../round1_source_collection/records/ANDREWS_Q_supplement.md)；[ANDREWS_Q.md](../../round1_source_collection/books/ANDREWS_Q.md)。

- **AQ-3.18**（印刷页 23；式 (3.18)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 n≥0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-1.94-corrected · Andrews 有限 Heine 变换

$$
{}_3\phi_2^{[n]}\!\left[\begin{matrix}a,b,q^{-n}\\c,q^{1-n}/t\end{matrix};q,q\right]=\frac{(b,at;q)_n}{(c,t;q)_n}{}_3\phi_2^{[n]}\!\left[\begin{matrix}c/b,t,q^{-n}\\at,q^{1-n}/b\end{matrix};q,q\right].
$$

类型：identity；范围：finite_q。

代表式记号上下文：`SILLS-1.94-corrected`。

**证明算法状态：仅相关路线，未覆盖本式**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SRC-SILLS-1.94-corrected)

方法：旧 Heine 解析变换仅作相关路线。

覆盖边界：无限级数发射器不直接接受当前有限输入；不能按 Heine 名称判定覆盖。

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-1.94-corrected**（印刷页 45；1.94-corrected）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0，bt≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-1.95 · 有限 Heine 和的二阶递推

$$
f_n+\frac{-abtq^{2n}+atq^{n+1}+btq^{n+1}-ctq^{2n}+cq^{n+1}+q^{n+2}-q^3-q^2}{q^2(1-cq^{n-1})(1-tq^{n-1})}f_{n-1}+\frac{q(1-q^{n-1})(1-atq^{n-2})(1-btq^{n-2})}{(1-cq^{n-1})(1-tq^{n-2})(1-tq^{n-1})}f_{n-2}=0.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`SILLS-1.95`。

**证明算法状态：仅相关路线，未覆盖本式**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SRC-SILLS-1.95)

方法：旧 Heine 解析变换仅作相关路线。

覆盖边界：无限级数发射器不直接接受当前有限输入；不能按 Heine 名称判定覆盖。

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-1.95**（印刷页 45；1.95）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥2；f_n 是(1.94)左侧终止和。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
