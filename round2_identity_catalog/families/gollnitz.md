# Göllnitz 有界分拆多项式

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 本次未匹配到旧算法 6 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

## FQI-GOLLNITZ-RECURRENCE · Göllnitz 有界分拆递推

$$
G_N=G_{N-1}+\begin{cases}tq^NG_{N-6},&N\equiv2,4,5\pmod6,\\t^2q^NG_{N-7},&N\equiv0,1,3\pmod6.\end{cases}
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`SILLS-2.82-83`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：G_N(t,q)计数最大部件≤N的分拆：不含1、3；相邻差≥6，当较大部件≡0,1,3 mod6时差>6。部件≡2,4,5 mod6的t权为1，其余为2；q权为总和。G₋₁=1，G₋₇=0。

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-2.82-83**（印刷页 85；2.82-83）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。N≥7；G₀=G₁=1，G₂=G₃=1+tq²，G₄=1+tq²+tq⁴，G₅=1+tq²+tq⁴+tq⁵，G₆=G₅+t²q⁶。
  对应：代表式；保留本条来源域。
- **AQ-10.17**（印刷页 102；式 (10.17)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 n≥2，a∈{0,…,5}；χ(a)=1 当 a∈{1,2,4}，否则为0；d_N 定义及初值见书籍说明。
  对应：d_N(t)=G_N(t,q)，N=6n−a；χ(a)=1 对应 N≡2,4,5，其余三类为0。保留 AQ n≥2 与 Sills N≥7 的各自域。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-GOLLNITZ-SHIFT · Göllnitz 参数移位

$$
d_{6n+3}(t)-tq^{6n+2}d_{6n-3}(t)=(1+tq^2)(1+tq^4)(1+tq^5)d_{6n-7}(tq^6).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AQ-10.18`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_Q_supplement.md](../../round1_source_collection/records/ANDREWS_Q_supplement.md)；[ANDREWS_Q.md](../../round1_source_collection/books/ANDREWS_Q.md)。

- **AQ-10.18**（印刷页 102；式 (10.18)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 n≥1，d_{-1}=1；d_N 为 (10.16) 的有界分拆多项式。
  对应：代表式；保留本条来源域。
- **SILLS-2.84**（印刷页 86；2.84）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥1。
  对应：G_N(t,q)=d_N(t)，其余参数原样；两书采用修订后的较大部件约束及相同 t 权。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-GOLLNITZ-ORDER4 · Göllnitz 四阶递推

$$
\begin{aligned}d_{6n-1}(t)={}&(1+tq^{6n}(q^{-1}+q^{-2}+q^{-4}))d_{6n-7}(t)\\&+t^2q^{6n}(q^{-3}+q^{-5}+q^{-6})(1-q^{6n-6})d_{6n-13}(t)\\&+t^3q^{12n-13}(t(q^{-1}+q^{-2}+q^{-4})+q^{6n-12})d_{6n-19}(t)+t^6q^{18n-32}d_{6n-25}(t).\end{aligned}
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`AQ-10.21`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_Q_supplement.md](../../round1_source_collection/records/ANDREWS_Q_supplement.md)；[ANDREWS_Q.md](../../round1_source_collection/books/ANDREWS_Q.md)。

- **AQ-10.21**（印刷页 102,103；式 (10.21)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 n≥3；d_{-1}=1，d_{-7}=0。
  对应：代表式；保留本条来源域。
- **SILLS-2.88**（印刷页 86；2.88）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥3。
  对应：按本条 definitions 展开 F；把四项移到等号右侧；G_N=d_N，G_−1=1、G_−7=0。使用修订后 W 项负号。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-GOLLNITZ-ELIMINATION · Göllnitz 消元式

$$
\begin{aligned}d_{6n+3}(t)-tq^{6n+2}d_{6n-3}(t)={}&d_{6n+5}(t)-tq^{6n+2}(1+q^2+q^3)d_{6n-1}(t)\\&+t^2q^{12n}(1+q+q^3)d_{6n-7}(t)-t^3q^{18n-7}d_{6n-13}(t).\end{aligned}
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`AQ-10.23`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_Q_supplement.md](../../round1_source_collection/records/ANDREWS_Q_supplement.md)；[ANDREWS_Q.md](../../round1_source_collection/books/ANDREWS_Q.md)。

- **AQ-10.23**（印刷页 103；式 (10.23)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 n≥2；d_{-1}=1。
  对应：代表式；保留本条来源域。
- **SILLS-2.90-91**（印刷页 86；2.90-91）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥2。
  对应：G_N=d_N；全部系数逐项一致。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AP-7.E11 · 有最大部分限制的 Göllnitz 型有限公式

$$
d_{6n-1}(q)=\sum_{j=0}^{\lfloor n/2\rfloor}q^{6nj-3j^2+2j}\begin{bmatrix}n-j\\j\end{bmatrix}_{q^6}\Lambda_{n-2j}(q).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AP-7.E11`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：d_m(q)=Σ_λ q^{|λ|}，λ₁≤m，最小部分≠1,3，相邻差≥6，若较小部分≡0,1,3 (mod 6) 则差>6；空分拆计1。原书定义 Λ_n：(−xq²;q⁶)_∞(−xq⁴;q⁶)_∞(−xq⁵;q⁶)_∞/(x;q⁶)_∞=Σ_{n≥0}Λ_n x^n/(q⁶;q⁶)_n。固定 n 的系数可用有限运算得到；该无限生成式只作辅助定义，不另计有限恒等式。

定义文件：[ANDREWS_P_supplement.md](../../round1_source_collection/records/ANDREWS_P_supplement.md)；[ANDREWS_P.md](../../round1_source_collection/books/ANDREWS_P.md)。

- **AP-7.E11**（p.118, Example 11*（定义起于 p.117））：n≥1 为整数；q 为形式变量。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AQ-10.27 · Göllnitz 递推算子的相容关系

$$
\begin{aligned}\mathcal F(n-1,tq^6;G_n,G_{n-1},G_{n-2},G_{n-3},G_{n-4})={}&J_{n+1}-tq^{6n-6}(q^2+q^4+q^5)J_n\\&+t^2q^{12n-12}(1+q+q^3)J_{n-1}-t^3q^{18n-25}J_{n-2}.\end{aligned}
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`AQ-10.27`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_Q_supplement.md](../../round1_source_collection/records/ANDREWS_Q_supplement.md)；[ANDREWS_Q.md](../../round1_source_collection/books/ANDREWS_Q.md)。

- **AQ-10.27**（印刷页 103；式 (10.27)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 n≥5；F 为 (10.22) 的五元线性算子；J_n=F(n,t;d_{6n-1},…,d_{6n-25})；G_n 由 (10.24) 给出。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
