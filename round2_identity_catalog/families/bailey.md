# Bailey 对、有限反演与链

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 已有可复用部件，待组装 1 条；仅相关路线，未覆盖本式 1 条；本次未匹配到旧算法 24 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

## FQI-BAILEY-INVERSION · 有限 Bailey 反演

$$
\alpha_0=\beta_0,\qquad \alpha_n=(1-aq^{2n})\sum_{j=0}^n\frac{(aq;q)_{n+j-1}(-1)^{n-j}q^{(n-j)(n-j-1)/2}}{(q;q)_{n-j}}\beta_j\quad(n\ge1).
$$

类型：identity / rewrite_rule；范围：finite_q。

代表式记号上下文：`AQ-3.40`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_Q_supplement.md](../../round1_source_collection/records/ANDREWS_Q_supplement.md)；[ANDREWS_Q.md](../../round1_source_collection/books/ANDREWS_Q.md)。

- **AQ-3.40**（印刷页 29；式 (3.40)）：\(\beta_n=\sum_{r=0}^n\alpha_r/((q;q)_{n-r}(aq;q)_{n+r})\)；所有出现的有限分母非零。
  对应：代表式；保留本条来源域。
- **SILLS-2.31**（印刷页 60；2.31）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0；n=r=0时(xq;q)₋₁=1/(1−x)，可去奇点约去；(α,β) 是关于x的Bailey对。
  对应：x→a，r→j；n=0 单列 α₀=β₀，约去 (1−a)(aq;q)_−1，避免伪奇点。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-BAILEY-LEMMA · 有限 Bailey 引理

$$
\sum_{r=0}^n\frac{(\rho_1,\rho_2;q)_r(aq/(\rho_1\rho_2))^r(aq/(\rho_1\rho_2);q)_{n-r}}{(aq/\rho_1,aq/\rho_2;q)_n(q;q)_{n-r}}\beta_r=\sum_{r=0}^n\frac{(\rho_1,\rho_2;q)_r(aq/(\rho_1\rho_2))^r\alpha_r}{(aq/\rho_1,aq/\rho_2;q)_r(q;q)_{n-r}(aq;q)_{n+r}}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AQ-REF-BAILEY`。

**证明算法状态：仅相关路线，未覆盖本式**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-BAILEY-LEMMA)

方法：旧弱 Bailey 框架仅作相关路线。

覆盖边界：目标不同，且旧弱 Bailey 自动输出仍有 7 个开放义务。

定义文件：[ANDREWS_Q_supplement.md](../../round1_source_collection/records/ANDREWS_Q_supplement.md)；[ANDREWS_Q.md](../../round1_source_collection/books/ANDREWS_Q.md)。

- **AQ-REF-BAILEY**（印刷页 25,26；式 (3.28)；Theorem 3.3, (3.27)–(3.30)）：\(\beta_n=\sum_{r=0}^n\alpha_r/((q;q)_{n-r}(aq;q)_{n+r})\)；所有出现的有限分母非零。 n≥0；q,a,ρ₁,ρ₂≠0。
  对应：代表式；保留本条来源域。
- **SILLS-2.34**（印刷页 61；2.34）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0，ρ₁ρ₂≠0；(α,β) 是关于x的Bailey对。
  对应：x→a，左侧 j→r；把与求和指标无关的两个分母提出。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-BAILEY-UNIT · 一般参数单位 Bailey 对

$$
\sum_{r=0}^n\frac{u_r(a)}{(q;q)_{n-r}(aq;q)_{n+r}}=\delta_{n,0},\quad u_0(a)=1,\quad u_r(a)=\frac{(-1)^rq^{r(r-1)/2}(1-aq^{2r})(aq;q)_{r-1}}{(q;q)_r}\ (r\ge1).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AQ-3.48`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_Q_supplement.md](../../round1_source_collection/records/ANDREWS_Q_supplement.md)；[ANDREWS_Q.md](../../round1_source_collection/books/ANDREWS_Q.md)。

- **AQ-3.48**（印刷页 31；式 (3.48)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 n≥0。
  对应：代表式；保留本条来源域。
- **SILLS-2.Ex2a**（印刷页 72；2.Ex2a）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0；所有分母非零。
  对应：取定义 (d,e,k)=(1,1,1)，x→a；r≥1 时 (a;q)_r/(1−a)=(aq;q)_(r−1)，r=0 单列为1。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AQ-3.23 · Bailey 转置求和（有限支持特化）

$$
\sum_{n=0}^N\alpha_n\sum_{r=n}^N\delta_r u_{r-n}v_{r+n}=\sum_{r=0}^N\delta_r\sum_{n=0}^r\alpha_n u_{r-n}v_{r+n}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`AQ-3.23`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_Q_supplement.md](../../round1_source_collection/records/ANDREWS_Q_supplement.md)；[ANDREWS_Q.md](../../round1_source_collection/books/ANDREWS_Q.md)。

- **AQ-3.23**（印刷页 24；式 (3.23)）：N≥0；α、δ、u、v 为任意在交换环中取值的有限向量。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AQ-3.35 · Rogers–Ramanujan Bailey 对的有限等式

$$
\frac1{(q;q)_n}=\frac1{(q;q)_n^2}+\sum_{r=1}^n\frac{(-1)^rq^{r(3r-1)/2}(1+q^r)}{(q;q)_{n-r}(q;q)_{n+r}}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AQ-3.35`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_Q_supplement.md](../../round1_source_collection/records/ANDREWS_Q_supplement.md)；[ANDREWS_Q.md](../../round1_source_collection/books/ANDREWS_Q.md)。

- **AQ-3.35**（印刷页 28；式 (3.35)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 n≥0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AQ-3.37 · a=q 的单位 Bailey 对

$$
\sum_{r=0}^n\frac{(-1)^rq^{r(r-1)/2}(1-q^{2r+1})}{(1-q)(q;q)_{n-r}(q^2;q)_{n+r}}=\delta_{n,0}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AQ-3.37`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_Q_supplement.md](../../round1_source_collection/records/ANDREWS_Q_supplement.md)；[ANDREWS_Q.md](../../round1_source_collection/books/ANDREWS_Q.md)。

- **AQ-3.37**（印刷页 28；式 (3.37)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 n≥0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AQ-3.42 · Bailey 链逆变换（显式修订）

$$
\beta_n=\sum_{j=0}^n\frac{(aq/\rho_1,aq/\rho_2;q)_j(\rho_1\rho_2/(aq);q)_{n-j}(\rho_1\rho_2/(aq))^j}{(\rho_1,\rho_2;q)_n(q;q)_{n-j}}\beta_j^{\prime}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`AQ-3.42`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_Q_supplement.md](../../round1_source_collection/records/ANDREWS_Q_supplement.md)；[ANDREWS_Q.md](../../round1_source_collection/books/ANDREWS_Q.md)。

- **AQ-3.42**（印刷页 29；式 (3.42)）：\(\beta_n=\sum_{r=0}^n\alpha_r/((q;q)_{n-r}(aq;q)_{n+r})\)；所有出现的有限分母非零。 q,a,ρ₁,ρ₂≠0；β′ 由 (3.30) 定义。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AQ-3.43 · 有限 k 重 Bailey 链

$$
\begin{aligned}&\sum_{r=0}^N\frac{(q^{-N};q)_r}{(aq^{N+1};q)_r}\prod_{i=1}^k\frac{(b_i,c_i;q)_r}{(aq/b_i,aq/c_i;q)_r}\left(\frac{a^kq^{k+N}}{\prod_{i=1}^kb_ic_i}\right)^r(-1)^rq^{-r(r-1)/2}\alpha_r\\&=\frac{(aq,aq/(b_kc_k);q)_N}{(aq/b_k,aq/c_k;q)_N}\sum_{0\le n_1\le\cdots\le n_k\le N}\frac{(q^{-N};q)_{n_k}\beta_{n_1}}{(b_kc_kq^{-N}/a;q)_{n_k}}\prod_{i=1}^k(b_i,c_i;q)_{n_i}\prod_{i=1}^{k-1}\frac{(aq/(b_ic_i);q)_{n_{i+1}-n_i}(aq/(b_ic_i))^{n_i}}{(q;q)_{n_{i+1}-n_i}(aq/b_i,aq/c_i;q)_{n_{i+1}}}\,q^{n_k}.\end{aligned}
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AQ-3.43`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_Q_supplement.md](../../round1_source_collection/records/ANDREWS_Q_supplement.md)；[ANDREWS_Q.md](../../round1_source_collection/books/ANDREWS_Q.md)。

- **AQ-3.43**（印刷页 30；式 (3.43)）：\(\beta_n=\sum_{r=0}^n\alpha_r/((q;q)_{n-r}(aq;q)_{n+r})\)；所有出现的有限分母非零。 k≥1，N≥0；a,q,b_i,c_i≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AQ-8.56 · Andrews–Baxter–Forrester 双端终止变换

$$
\begin{aligned}&\sum_{r=-R}^N\frac{1-aq^{2r}}{1-a}\frac{(aq^{-R},q^{-N};q)_r}{(q^{R+1},aq^{N+1};q)_r}\prod_{i=1}^k\frac{(b_i,c_i;q)_r}{(aq/b_i,aq/c_i;q)_r}\left(\frac{a^kq^{k+N+R}}{\prod_{i=1}^kb_ic_i}\right)^r\\&=\frac{(q/a,aq/(b_1c_1);q)_R(aq,aq/(b_kc_k);q)_N}{(q/b_1,q/c_1;q)_R(aq/b_k,aq/c_k;q)_N}\sum_{\substack{m_1\ge-R,\ m_2,\ldots,m_{k-1}\ge0\\M_{k-1}\le N}}\frac{(aq^{R+1}/(b_1c_1);q)_{m_1}}{(q^{R+1};q)_{m_1}}\prod_{i=2}^{k-1}\frac{(aq/(b_ic_i);q)_{m_i}}{(q;q)_{m_i}}\\&\qquad\times\prod_{i=1}^{k-1}\frac{(b_{i+1},c_{i+1};q)_{M_i}}{(aq/b_i,aq/c_i;q)_{M_i}}\frac{(q^{-N};q)_{M_{k-1}}}{(b_kc_kq^{-N}/a;q)_{M_{k-1}}}\frac{a^{\sum_{i=1}^{k-2}M_i}q^{\sum_{i=1}^{k-1}M_i}}{\prod_{i=1}^{k-2}(b_{i+1}c_{i+1})^{M_i}}.\end{aligned}
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AQ-8.56`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_Q_supplement.md](../../round1_source_collection/records/ANDREWS_Q_supplement.md)；[ANDREWS_Q.md](../../round1_source_collection/books/ANDREWS_Q.md)。

- **AQ-8.56**（印刷页 83；式 (8.56)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 k≥2，N,R≥0；q,a,b_i,c_i≠0，a≠1；\(M_i=\sum_{j=1}^im_j\)；负长度定义 \((x;q)_{-s}=1/(xq^{-s};q)_s\)，这些倒数分母亦须非零。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AQ-10.12 · Bailey 对逐项反求递推

$$
\alpha_0=\beta_0,\quad \alpha_n=(aq;q)_{2n}\beta_n-\sum_{r=0}^{n-1}\frac{(aq^{n+r+1};q)_{n-r}}{(q;q)_{n-r}}\alpha_r.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`AQ-10.12`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_Q_supplement.md](../../round1_source_collection/records/ANDREWS_Q_supplement.md)；[ANDREWS_Q.md](../../round1_source_collection/books/ANDREWS_Q.md)。

- **AQ-10.12**（印刷页 99；式 (10.12)）：\(\beta_n=\sum_{r=0}^n\alpha_r/((q;q)_{n-r}(aq;q)_{n+r})\)；所有出现的有限分母非零。 n≥1。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-2.30 · Bailey 关系的终止超几何重写

$$
\beta_n=\frac1{(q,xq;q)_n}\sum_{r=0}^n\frac{(q^{-n};q)_r}{(xq^{n+1};q)_r}(-1)^rq^{nr-r(r-1)/2}\alpha_r.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`SILLS-2.30`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-2.30**（印刷页 60；2.30）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0；(α,β) 是关于x的Bailey对。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-2.Pair112 · 基本 Bailey 有限和

$$
\mathcal B_n[\alpha;x,q]=1/(q;q)_n,\qquad \alpha_r=\alpha_r^{(1,1,2)}(x^1,q^1)
$$

类型：identity；范围：finite_q。

代表式记号上下文：`SILLS-2.Pair112`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：\mathcal B_n[\alpha;x,q]:=\sum_{r=0}^n\alpha_r/((q;q)_{n-r}(xq;q)_{n+r}).

\alpha^{(d,e,k)}_r(x^e,q^e)=\begin{cases}\displaystyle\frac{(-1)^s x^{(k-d)s}q^{d(2k-2d+1)s^2/2-ds/2}(1-xq^{2ds})(x;q^d)_s}{(1-x)(q^d;q^d)_s},&r=ds,\\0,&d\nmid r.\end{cases}

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-2.Pair112**（印刷页 63；2.Pair112）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0；所有分母非零。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-2.Pair122 · 二步长 Bailey 有限和

$$
\mathcal B_n[\alpha;x^2,q^2]=1/((q^2;q^2)_n(-xq;q)_{2n}),\qquad \alpha_r=\alpha_r^{(1,2,2)}(x^2,q^2)
$$

类型：identity；范围：finite_q。

代表式记号上下文：`SILLS-2.Pair122`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：\mathcal B_n[\alpha;x,q]:=\sum_{r=0}^n\alpha_r/((q;q)_{n-r}(xq;q)_{n+r}).

\alpha^{(d,e,k)}_r(x^e,q^e)=\begin{cases}\displaystyle\frac{(-1)^s x^{(k-d)s}q^{d(2k-2d+1)s^2/2-ds/2}(1-xq^{2ds})(x;q^d)_s}{(1-x)(q^d;q^d)_s},&r=ds,\\0,&d\nmid r.\end{cases}

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-2.Pair122**（印刷页 64；2.Pair122）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0；所有分母非零。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-2.Lem2.31 · 关于1的双边 Bailey 有限和

$$
\sum_{r=-n}^n\begin{bmatrix}2n\\n+r\end{bmatrix}_q a^rq^{r^2/2}=(-a\sqrt q,-\sqrt q/a;q)_n.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`SILLS-2.Lem2.31`。

**证明算法状态：已有可复用部件，待组装**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SRC-SILLS-2.Lem2.31)

方法：有限 JTP 的平方根参数特化。

覆盖边界：平方根分支和指数解释必须与目录一致；未找到已闭合包装。

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-2.Lem2.31**（印刷页 71；2.Lem2.31）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0，a≠0，选定√q；用q=t²解释。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-2.Ex2b · 二步长带符号 Bailey 有限和

$$
\mathcal B_n[\alpha;x^2,q^2]=(-1)^nq^{n^2}/((q^2;q^2)_n(-xq;q)_{2n}),\qquad \alpha_r=\alpha_r^{(1,2,1)}(x^2,q^2)
$$

类型：identity；范围：finite_q。

代表式记号上下文：`SILLS-2.Ex2b`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：\mathcal B_n[\alpha;x,q]:=\sum_{r=0}^n\alpha_r/((q;q)_{n-r}(xq;q)_{n+r}).

\alpha^{(d,e,k)}_r(x^e,q^e)=\begin{cases}\displaystyle\frac{(-1)^s x^{(k-d)s}q^{d(2k-2d+1)s^2/2-ds/2}(1-xq^{2ds})(x;q^d)_s}{(1-x)(q^d;q^d)_s},&r=ds,\\0,&d\nmid r.\end{cases}

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-2.Ex2b**（印刷页 72；2.Ex2b）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0；所有分母非零。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-2.Ex2c · 三步长 Bailey 有限和

$$
\mathcal B_n[\alpha;x^3,q^3]=(xq;q)_{3n}/((q^3;q^3)_n(x^3q^3;q^3)_{2n}),\qquad \alpha_r=\alpha_r^{(1,3,2)}(x^3,q^3)
$$

类型：identity；范围：finite_q。

代表式记号上下文：`SILLS-2.Ex2c`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：\mathcal B_n[\alpha;x,q]:=\sum_{r=0}^n\alpha_r/((q;q)_{n-r}(xq;q)_{n+r}).

\alpha^{(d,e,k)}_r(x^e,q^e)=\begin{cases}\displaystyle\frac{(-1)^s x^{(k-d)s}q^{d(2k-2d+1)s^2/2-ds/2}(1-xq^{2ds})(x;q^d)_s}{(1-x)(q^d;q^d)_s},&r=ds,\\0,&d\nmid r.\end{cases}

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-2.Ex2c**（印刷页 72；2.Ex2c）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0；所有分母非零。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-2.Ex2d · 偶指标 Bailey 有限和 I

$$
\mathcal B_n[\alpha;x,q]=q^{n(n-1)/2}/((q;q)_n(xq;q^2)_n),\qquad \alpha_r=\alpha_r^{(2,1,2)}(x^1,q^1)
$$

类型：identity；范围：finite_q。

代表式记号上下文：`SILLS-2.Ex2d`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：\mathcal B_n[\alpha;x,q]:=\sum_{r=0}^n\alpha_r/((q;q)_{n-r}(xq;q)_{n+r}).

\alpha^{(d,e,k)}_r(x^e,q^e)=\begin{cases}\displaystyle\frac{(-1)^s x^{(k-d)s}q^{d(2k-2d+1)s^2/2-ds/2}(1-xq^{2ds})(x;q^d)_s}{(1-x)(q^d;q^d)_s},&r=ds,\\0,&d\nmid r.\end{cases}

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-2.Ex2d**（印刷页 72；2.Ex2d）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0；所有分母非零。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-2.Ex2e · 偶指标 Bailey 有限和 II

$$
\mathcal B_n[\alpha;x,q]=1/((q;q)_n(xq;q^2)_n),\qquad \alpha_r=\alpha_r^{(2,1,3)}(x^1,q^1)
$$

类型：identity；范围：finite_q。

代表式记号上下文：`SILLS-2.Ex2e`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：\mathcal B_n[\alpha;x,q]:=\sum_{r=0}^n\alpha_r/((q;q)_{n-r}(xq;q)_{n+r}).

\alpha^{(d,e,k)}_r(x^e,q^e)=\begin{cases}\displaystyle\frac{(-1)^s x^{(k-d)s}q^{d(2k-2d+1)s^2/2-ds/2}(1-xq^{2ds})(x;q^d)_s}{(1-x)(q^d;q^d)_s},&r=ds,\\0,&d\nmid r.\end{cases}

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-2.Ex2e**（印刷页 72；2.Ex2e）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0；所有分母非零。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-2.Ex2f · 三倍指标 Bailey 有限和

$$
\mathcal B_n[\alpha;x,q]=(x;q^3)_n/((q;q)_n(x;q)_{2n}),\qquad \alpha_r=\alpha_r^{(3,1,4)}(x^1,q^1)
$$

类型：identity；范围：finite_q。

代表式记号上下文：`SILLS-2.Ex2f`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：\mathcal B_n[\alpha;x,q]:=\sum_{r=0}^n\alpha_r/((q;q)_{n-r}(xq;q)_{n+r}).

\alpha^{(d,e,k)}_r(x^e,q^e)=\begin{cases}\displaystyle\frac{(-1)^s x^{(k-d)s}q^{d(2k-2d+1)s^2/2-ds/2}(1-xq^{2ds})(x;q^d)_s}{(1-x)(q^d;q^d)_s},&r=ds,\\0,&d\nmid r.\end{cases}

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-2.Ex2f**（印刷页 72；2.Ex2f）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0；所有分母非零。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-2.Ex7a-corrected · 关于q的参数 Bailey 有限和

$$
\mathcal B_n[\alpha;q,q]=(-a;q)_{n+1}(-q/a;q)_n(1-q)/(q;q)_{2n+1},\qquad \alpha_r=(a^{r+1}+a^{-r})q^{r(r+1)/2}
$$

类型：identity；范围：finite_q。

代表式记号上下文：`SILLS-2.Ex7a-corrected`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：\mathcal B_n[\alpha;x,q]:=\sum_{r=0}^n\alpha_r/((q;q)_{n-r}(xq;q)_{n+r}).

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-2.Ex7a-corrected**（印刷页 74；2.Ex7a-corrected）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0；所有分母非零。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-2.Lem2.53 · 半整数幂 Bailey 有限和

$$
\mathcal B_n[\alpha;q,q]=1/((q^{3/2};q)_n(q;q)_n),\qquad \alpha_r=q^{r^2+r/2}(1+q^{r+1/2})/(1+\sqrt q)
$$

类型：identity；范围：finite_q。

代表式记号上下文：`SILLS-2.Lem2.53`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：\mathcal B_n[\alpha;x,q]:=\sum_{r=0}^n\alpha_r/((q;q)_{n-r}(xq;q)_{n+r}).

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-2.Lem2.53**（印刷页 88；2.Lem2.53）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0；所有分母非零。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-2.108 · Mock theta 相关的有限 Bailey 对

$$
\mathcal B_n[\alpha;1,q]=1/(-q;q)_n,\qquad \alpha_0=1,\quad\alpha_r=q^{r(3r+1)/2}\sum_{j=-r}^{r}(-1)^jq^{-j^2}-q^{r(3r-1)/2}\sum_{j=-r+1}^{r-1}(-1)^jq^{-j^2}\ (r\ge1)
$$

类型：identity；范围：finite_q。

代表式记号上下文：`SILLS-2.108`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：\mathcal B_n[\alpha;x,q]:=\sum_{r=0}^n\alpha_r/((q;q)_{n-r}(xq;q)_{n+r}).

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-2.108**（印刷页 92；2.108）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0；所有分母非零。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-3.5-6 · Bailey 链第二步有限变换

$$
\mathcal B_n[\alpha;x,q]=\frac1{(xq/\rho_1,xq/\rho_2;q)_n}\sum_{j=0}^n\frac{(\rho_1,\rho_2;q)_j(xq/(\rho_1\rho_2);q)_{n-j}(xq/(\rho_1\rho_2))^j}{(q;q)_j(q;q)_{n-j}},\qquad \alpha_r=\frac{(\rho_1,\rho_2;q)_r(xq/(\rho_1\rho_2))^r}{(xq/\rho_1,xq/\rho_2;q)_r}\alpha_r^{(1,1,2)}(x,q)
$$

类型：identity；范围：finite_q。

代表式记号上下文：`SILLS-3.5-6`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：\mathcal B_n[\alpha;x,q]:=\sum_{r=0}^n\alpha_r/((q;q)_{n-r}(xq;q)_{n+r}).

\alpha^{(d,e,k)}_r(x^e,q^e)=\begin{cases}\displaystyle\frac{(-1)^s x^{(k-d)s}q^{d(2k-2d+1)s^2/2-ds/2}(1-xq^{2ds})(x;q^d)_s}{(1-x)(q^d;q^d)_s},&r=ds,\\0,&d\nmid r.\end{cases}

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-3.5-6**（印刷页 108；3.5-6）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0；所有分母非零。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-3.7 · Bailey 链的有限双和

$$
\mathcal B_n[\alpha;x,q]=\sum_{j=0}^nx^jq^{j^2}/((q;q)_j(q;q)_{n-j}),\qquad \alpha_r=(-1)^rx^{2r}q^{r(5r-1)/2}(1-xq^{2r})(x;q)_r/((1-x)(q;q)_r)
$$

类型：identity；范围：finite_q。

代表式记号上下文：`SILLS-3.7`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：\mathcal B_n[\alpha;x,q]:=\sum_{r=0}^n\alpha_r/((q;q)_{n-r}(xq;q)_{n+r}).

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-3.7**（印刷页 108；3.7）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0；所有分母非零。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-3.Lem3.3 · 偶模数 Bailey 有限和

$$
\mathcal B_n[\alpha;x,q]=1/(q^2;q^2)_n,\qquad \alpha_r=(-1)^rq^{r^2}(1-xq^{2r})(x^2;q^2)_r/((1-x)(q^2;q^2)_r)
$$

类型：identity；范围：finite_q。

代表式记号上下文：`SILLS-3.Lem3.3`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：\mathcal B_n[\alpha;x,q]:=\sum_{r=0}^n\alpha_r/((q;q)_{n-r}(xq;q)_{n+r}).

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-3.Lem3.3**（印刷页 109；3.Lem3.3）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0；所有分母非零。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-6.Ex1-corrected · Capparelli 相关的有限 Bailey 对

$$
\mathcal B_n[\alpha;1,q]=(-1;q^3)_n/((q;q)_{2n}(-1;q)_n),\qquad \alpha_n=\begin{cases}1,&n=0,\\-q^{(9r^2+9r+2)/2},&n=3r+1,\\-q^{(9r^2-9r+2)/2},&n=3r-1,\\q^{3r(3r-1)/2}(1+q^{3r}),&n=3r>0,\end{cases}
$$

类型：identity；范围：finite_q。

代表式记号上下文：`SILLS-6.Ex1-corrected`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：\mathcal B_n[\alpha;x,q]:=\sum_{r=0}^n\alpha_r/((q;q)_{n-r}(xq;q)_{n+r}).

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-6.Ex1-corrected**（印刷页 162；6.Ex1-corrected）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0；所有分母非零。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
