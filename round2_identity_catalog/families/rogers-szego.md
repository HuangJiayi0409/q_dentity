# Rogers–Szegő、q-Hermite 与连接系数

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 本次未匹配到旧算法 17 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

## FQI-GAUSS-ALTERNATING · Gauss 交错 Gaussian 奇偶求值

$$
\sum_{j=0}^m(-1)^j\begin{bmatrix}m\\j\end{bmatrix}_{q}=\begin{cases}(q;q^2)_{m/2},&m\text{ even},\\0,&m\text{ odd}.\end{cases}
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AP-3.3.8`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_P_supplement.md](../../round1_source_collection/records/ANDREWS_P_supplement.md)；[ANDREWS_P.md](../../round1_source_collection/books/ANDREWS_P.md)。

- **AP-3.3.8**（p.37, Theorem 3.4, (3.3.8)）：m≥0 为整数。
  对应：代表式；保留本条来源域。
- **FINE-20.67**（印刷页 28；式 (20.67)；A general transformation）：q 为形式变量；数值代入要求所有实际分母非零，Gaussian 在奇点先作多项式延拓。空乘积为 1、空和为 0。n≥0 为整数。
  对应：展开 f_N(−1)=Σ_j(−1)^j[N choose j]_q；按 N=2n、2n+1 分支。
- **KAC-CHEUNG-7.14-15**（印刷页 26；7.14-15）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。m≥0。
  对应：代表指标 m→n；两条奇偶分支相同。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-ROGERS-SZEGO-RECURRENCE · Rogers–Szegő 三项递推

$$
H_{n+1}(t;q)=(1+t)H_n(t;q)-(1-q^n)tH_{n-1}(t;q).
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`AP-3.E6`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：\(H_n(t;q)=\sum_{j=0}^n\begin{bmatrix}n\\j\end{bmatrix}_q t^j\)；n≥0。

定义文件：[ANDREWS_P_supplement.md](../../round1_source_collection/records/ANDREWS_P_supplement.md)；[ANDREWS_P.md](../../round1_source_collection/books/ANDREWS_P.md)。

- **AP-3.E6**（p.49, Example 6）：n≥1 为整数。
  对应：代表式；保留本条来源域。
- **FINE-20.63b**（印刷页 28；式 (20.63b)；A general transformation）：q 为形式变量；数值代入要求所有实际分母非零，Gaussian 在奇点先作多项式延拓。空乘积为 1、空和为 0。n≥1；f_0(u)=1，f_1(u)=1+u。
  对应：f_n(u)=H_n(u;q)，u→t；将后两项移到右侧。
- **KAC-CHEUNG-7.RogersSzego**（印刷页 26；7.RogersSzego）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。n≥1。
  对应：H_n(t)=H_n(t;q)；q^n−1=−(1−q^n)。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-ROGERS-SZEGO-SQRT · Rogers–Szegő 平方根特值

$$
H_n(u;u^2)=(-u;u)_n.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AP-3.E5`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：\(H_n(t;q)=\sum_{j=0}^n\begin{bmatrix}n\\j\end{bmatrix}_q t^j\)；n≥0。

定义文件：[ANDREWS_P_supplement.md](../../round1_source_collection/records/ANDREWS_P_supplement.md)；[ANDREWS_P.md](../../round1_source_collection/books/ANDREWS_P.md)。

- **AP-3.E5**（p.49, Example 5）：n≥0；u 为形式变量。
  对应：代表式；保留本条来源域。
- **FINE-20.68**（印刷页 29；式 (20.68)；A general transformation）：q 为形式变量；数值代入要求所有实际分母非零，Gaussian 在奇点先作多项式延拓。空乘积为 1、空和为 0。n≥0；选择 q^{1/2} 的一个平方根。
  对应：选定 u=q_Fine^(1/2)，底数 q_Fine=u²；H_n(u;u²)=(−u;u)_n。根分支随来源保留。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-7.Ex38 · 离散 q-Hermite 三项递推

$$
H_{n+1}(x;q)=xH_n(x;q)-q^{n-1}(1-q^n)H_{n-1}(x;q),\quad H_n(x;q)=\sum_{k=0}^{\lfloor n/2\rfloor}\frac{(q;q)_n(-1)^kq^{k(k-1)}x^{n-2k}}{(q^2;q^2)_k(q;q)_{n-2k}}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-7.Ex38`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-7.Ex38**（Chapter 7, 7.Ex38, 印刷p209）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。n≥1。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-7.Ex40 · Rogers–Szegő 的有限 Turán 恒等式

$$
h_n(x)^2-h_{n+1}(x)h_{n-1}(x)=(1-q)(q;q)_{n-1}\sum_{k=1}^{n}\frac{q^{n-k}x^k}{(q;q)_{n-k}}h_{n-k}(x)^2,\quad h_n(x)=\sum_{k=0}^n\begin{bmatrix}n\\k\end{bmatrix}_qx^k.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-7.Ex40`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-7.Ex40**（Chapter 7, 7.Ex40, 印刷p210）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。n≥1。所有实际分母非零；见修订报告。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-9.Ex10ii · 连续 q-Hermite 的底数平方变换

$$
\sum_{k=0}^n\begin{bmatrix}n\\k\end{bmatrix}_{q^2}z^{n-2k}=P_n(z;s,-s,0,0\mid q),\quad s^2=q.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-9.Ex10ii`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-9.Ex10ii**（Chapter 9, 9.Ex10ii, 印刷p274）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。z≠0；P见7.5.3，零参数允许。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AP-3.E7 · Rogers–Szegő 线性化公式

$$
H_m(t;q)H_n(t;q)=\sum_{r=0}^{\min(m,n)}\begin{bmatrix}m\\r\end{bmatrix}_{q}\begin{bmatrix}n\\r\end{bmatrix}_{q}(q;q)_r t^r H_{m+n-2r}(t;q).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AP-3.E7`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：\(H_n(t;q)=\sum_{j=0}^n\begin{bmatrix}n\\j\end{bmatrix}_q t^j\)；n≥0。

定义文件：[ANDREWS_P_supplement.md](../../round1_source_collection/records/ANDREWS_P_supplement.md)；[ANDREWS_P.md](../../round1_source_collection/books/ANDREWS_P.md)。

- **AP-3.E7**（p.50, Example 7（题干起于 p.49））：m,n≥0 为整数。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AQ-2.23 · 连续 q-Hermite 多项式递推

$$
A_r(x)=(x+x^{-1})A_{r-1}(x)-(1-q^{r-1})A_{r-2}(x),\quad A_0=1,\ A_1=x+x^{-1}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`AQ-2.23`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_Q_supplement.md](../../round1_source_collection/records/ANDREWS_Q_supplement.md)；[ANDREWS_Q.md](../../round1_source_collection/books/ANDREWS_Q.md)。

- **AQ-2.23**（印刷页 13；式 (2.23)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 r≥2，x≠0；\(A_r(x)=\sum_{j=0}^r{r\brack j}_q x^{r-2j}\)。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AQ-2.29 · q-Hermite 的有限 Fourier 展开

$$
A_r(e^{i\theta})=\sum_{j=0}^r\begin{bmatrix}r\\j\end{bmatrix}_q\cos((r-2j)\theta)=\sum_{j=0}^r\begin{bmatrix}r\\j\end{bmatrix}_q e^{i(r-2j)\theta}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AQ-2.29`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_Q_supplement.md](../../round1_source_collection/records/ANDREWS_Q_supplement.md)；[ANDREWS_Q.md](../../round1_source_collection/books/ANDREWS_Q.md)。

- **AQ-2.29**（印刷页 14；式 (2.29)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 r≥0；A 由 (2.23) 及其初值确定。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AQ-2.35 · Rogers 连接系数的有限反演关系

$$
\sum_{j=0}^{\lfloor N/2\rfloor}\begin{bmatrix}r+2j\\j\end{bmatrix}_q T(r+2j,N-2j)=\delta_{N,0}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AQ-2.35`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_Q_supplement.md](../../round1_source_collection/records/ANDREWS_Q_supplement.md)；[ANDREWS_Q.md](../../round1_source_collection/books/ANDREWS_Q.md)。

- **AQ-2.35**（印刷页 14；式 (2.35)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 r,N≥0；T 见 (2.39)。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AQ-2.38 · 连接系数递推

$$
T(r,0)=1,\qquad T(r,N)=-\sum_{j=1}^{\lfloor N/2\rfloor}\begin{bmatrix}r+2j\\j\end{bmatrix}_q T(r+2j,N-2j)\quad(N\ge1).
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`AQ-2.38`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_Q_supplement.md](../../round1_source_collection/records/ANDREWS_Q_supplement.md)；[ANDREWS_Q.md](../../round1_source_collection/books/ANDREWS_Q.md)。

- **AQ-2.38**（印刷页 14；式 (2.38)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 r≥0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AQ-2.39 · Rogers 连接系数乘积公式

$$
T(r,0)=1,\quad T(r,2n+1)=0,\quad T(r,2n)=\frac{(-1)^nq^{n(n-1)/2}(q^{r+1};q)_{n-1}(1-q^{r+2n})}{(q;q)_n}\ (n\ge1).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AQ-2.39`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_Q_supplement.md](../../round1_source_collection/records/ANDREWS_Q_supplement.md)；[ANDREWS_Q.md](../../round1_source_collection/books/ANDREWS_Q.md)。

- **AQ-2.39**（印刷页 15；式 (2.39)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 r≥0；T 由 (2.38) 定义。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-FINE-20.64b · Rogers–Szegő q-移位递推

$$
f_n(uq)-f_n(u)+u(1-q^n)f_{n-1}(u)=0.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`FINE-20.64b`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：f_n(u)=\sum_{j=0}^n{n\brack j}_q u^j。

定义文件：[FINE_supplement.md](../../round1_source_collection/records/FINE_supplement.md)；[FINE.md](../../round1_source_collection/books/FINE.md)。

- **FINE-20.64b**（印刷页 28；式 (20.64b)；A general transformation）：q 为形式变量；数值代入要求所有实际分母非零，Gaussian 在奇点先作多项式延拓。空乘积为 1、空和为 0。n≥1；f_n 由 (20.6) 定义。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-FINE-20.65b · Rogers–Szegő 混合 q-移位递推

$$
q^nf_n(u)-f_n(uq)+(1-q^n)f_{n-1}(uq)=0.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`FINE-20.65b`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：f_n(u)=\sum_{j=0}^n{n\brack j}_q u^j。

定义文件：[FINE_supplement.md](../../round1_source_collection/records/FINE_supplement.md)；[FINE.md](../../round1_source_collection/books/FINE.md)。

- **FINE-20.65b**（印刷页 28；式 (20.65b)；A general transformation）：q 为形式变量；数值代入要求所有实际分母非零，Gaussian 在奇点先作多项式延拓。空乘积为 1、空和为 0。n≥1；f_n 由 (20.6) 定义。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-FINE-20.66b · Rogers–Szegő 倒数变换

$$
f_n(u^{-1})=u^{-n}f_n(u).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`FINE-20.66b`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：f_n(u)=\sum_{j=0}^n{n\brack j}_q u^j。

定义文件：[FINE_supplement.md](../../round1_source_collection/records/FINE_supplement.md)；[FINE.md](../../round1_source_collection/books/FINE.md)。

- **FINE-20.66b**（印刷页 28；式 (20.66b)；A general transformation）：q 为形式变量；数值代入要求所有实际分母非零，Gaussian 在奇点先作多项式延拓。空乘积为 1、空和为 0。n≥0；u≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-FINE-20.69 · Rogers–Szegő 在 q^{-1/2} 处的特殊值

$$
f_n(q^{-1/2})=q^{-n/2}f_n(q^{1/2}).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`FINE-20.69`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[FINE_supplement.md](../../round1_source_collection/records/FINE_supplement.md)；[FINE.md](../../round1_source_collection/books/FINE.md)。

- **FINE-20.69**（印刷页 29；式 (20.69)；A general transformation）：q 为形式变量；数值代入要求所有实际分母非零，Gaussian 在奇点先作多项式延拓。空乘积为 1、空和为 0。n≥0；q≠0，选择同一平方根约定。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-KAC-CHEUNG-7.8 · Galois 数递推

$$
G_{n+1}=2G_n+(q^n-1)G_{n-1},\quad G_0=1,\quad G_1=2.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`KAC-CHEUNG-7.8`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：G_n=\sum_{j=0}^n{n\brack j}_q\quad\text{(7.7)}.

定义文件：[KAC_CHEUNG_supplement.md](../../round1_source_collection/records/KAC_CHEUNG_supplement.md)；[KAC_CHEUNG.md](../../round1_source_collection/books/KAC_CHEUNG.md)。

- **KAC-CHEUNG-7.8**（印刷页 25；7.8）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。n≥1。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
