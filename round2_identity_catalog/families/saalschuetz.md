# q-Pfaff–Saalschütz 与系数卷积

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 已有自动证明流程（旧条件域） 1 条；本次未匹配到旧算法 2 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

## FQI-PFAFF-SAALSCHUETZ · 终止 q-Pfaff–Saalschütz

$$
{}_3\phi_2^{[n]}\!\left[\begin{matrix}a,b,q^{-n}\\c,abq^{1-n}/c\end{matrix};q,q\right]=\frac{(c/a,c/b;q)_n}{(c,c/(ab);q)_n}
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-II-12`。

**证明算法状态：已有自动证明流程（旧条件域）**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-PFAFF-SAALSCHUETZ)

方法：终止 3φ2 一阶 q-WZ。

覆盖边界：旧定理使用 Generic 和对所有递推层成立的非零条件；比目录仅要求当前有限式分母非零更强。尚未证明目录全部条件能推出这些假设。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-II-12**（Appendix II, (II.12), 印刷p355）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。n 为非负整数；q 为非零且非单位根的复数；所有显示的分母非零。 a≠0。 b,c≠0。
  对应：代表式；保留本条来源域。
- **AP-3.3.12**（p.38, (3.3.12)）：N≥0 为整数；a,b,c,q 非零，所有所列分母非零；或在有理函数域中解释。
  对应：N→n；合并多参数 Pochhammer 后正是有限 3φ2 定义。
- **AQ-3.25**（印刷页 25；式 (3.25)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 N≥0，q,a,b,c≠0。
  对应：N→n；展开有限 3φ2。
- **SILLS-1.Thm1.49**（印刷页 32；1.Thm1.49）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0，abc≠0。
  对应：补显式截断上限 n。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AP-3.3.11 · 三 Gaussian 的 q-Saalschütz 求和

$$
\sum_{r=0}^{\min(M-m,N)}\begin{bmatrix}M-m\\r\end{bmatrix}_{q}\begin{bmatrix}N+m\\m+r\end{bmatrix}_{q}\begin{bmatrix}m+n+r\\M+N\end{bmatrix}_{q}q^{(N-r)(M-r-m)}=\begin{bmatrix}m+n\\M\end{bmatrix}_{q}\begin{bmatrix}n\\N\end{bmatrix}_{q}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AP-3.3.11`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_P_supplement.md](../../round1_source_collection/records/ANDREWS_P_supplement.md)；[ANDREWS_P.md](../../round1_source_collection/books/ANDREWS_P.md)。

- **AP-3.3.11**（p.37, Theorem 3.4, (3.3.11)）：m,n,M,N≥0，M≥m，均为整数；Gaussian 下指标越界为零。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AP-3.3.14 · Saalschütz 的系数卷积形式

$$
\sum_{j=0}^N\frac{(a;q)_j(b;q)_j(c/(ab);q)_{N-j}}{(q;q)_j(c;q)_j(q;q)_{N-j}}\left(\frac{ab}{c}\right)^{N-j}=\frac{(c/a;q)_N(c/b;q)_N}{(q;q)_N(c;q)_N}\left(\frac{ab}{c}\right)^N.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AP-3.3.14`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_P_supplement.md](../../round1_source_collection/records/ANDREWS_P_supplement.md)；[ANDREWS_P.md](../../round1_source_collection/books/ANDREWS_P.md)。

- **AP-3.3.14**（p.39, (3.3.14)（编号由下方正文指认））：N≥0 为整数；abc≠0，各有限分母非零。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
