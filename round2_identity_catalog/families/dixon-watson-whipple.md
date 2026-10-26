# q-Dixon、q-Watson、q-Whipple 奇偶求和

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 已有自动证明流程（旧条件域） 1 条；本次未匹配到旧算法 6 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

## FQI-SRC-GR2-5.Ex19i · Gaussian 立方的对称有限和

$$
\sum_{k=-n}^n(-1)^k\begin{bmatrix}2n\\n+k\end{bmatrix}_q^3q^{k(3k+1)/2}=\frac{(q;q)_{3n}}{(q;q)_n^3}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-5.Ex19i`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-5.Ex19i**（Chapter 5, 5.Ex19i, 印刷p150）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-5.Ex19ii · Gaussian 立方的奇数上指标有限和

$$
\sum_{k=-n-1}^n(-1)^k\begin{bmatrix}2n+1\\n+k+1\end{bmatrix}_q^3q^{k(3k+1)/2}=\frac{(q;q)_{3n+1}}{(q;q)_n^3}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-5.Ex19ii`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-5.Ex19ii**（Chapter 5, 5.Ex19ii, 印刷p150）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-II-14 · 终止 q-Dixon 的 4φ3 形式

$$
{}_4\phi_3^{[n]}\!\left[\begin{matrix}a,-qs,b,q^{-n}\\-s,aq/b,aq^{n+1}\end{matrix};q,sq^{n+1}/b\right]=\frac{(aq,sq/b;q)_n}{(sq,aq/b;q)_n}
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-II-14`。

**证明算法状态：已有自动证明流程（旧条件域）**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SRC-GR2-II-14)

方法：q-Dixon 4φ3 的一阶 q-WZ。

覆盖边界：除 旧定理使用 Generic 和对所有递推层成立的非零条件；比目录仅要求当前有限式分母非零更强。尚未证明目录全部条件能推出这些假设。 外，保持 a=s² 的平方根参数化；不据此覆盖 II.15 或三个 Gaussian 的 Dixon 和。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-II-14**（Appendix II, (II.14), 印刷p355）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。n 为非负整数；q 为非零且非单位根的复数；所有显示的分母非零。 选择 s≠0，令 a=s²；b≠0；平方根在两侧一致取 s。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-II-15 · 偶数终止长度的 q-Dixon 3φ2 求和

$$
{}_3\phi_2^{[2n]}\!\left[\begin{matrix}q^{-2n},b,c\\q^{1-2n}/b,q^{1-2n}/c\end{matrix};q,q^{2-n}/(bc)\right]=\frac{(b,c;q)_n(q,bc;q)_{2n}}{(q,bc;q)_n(b,c;q)_{2n}}
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-II-15`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-II-15**（Appendix II, (II.15), 印刷p355）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。n 为非负整数；q 为非零且非单位根的复数；所有显示的分母非零。 b,c≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-II-17 · 终止 q-Watson 求和及奇偶消失

$$
{}_4\phi_3^{[n]}\!\left[\begin{matrix}q^{-n},aq^n,c,-c\\s,-s,c^2\end{matrix};q,q\right]=\begin{cases}c^n\dfrac{(q,aq/c^2;q^2)_{n/2}}{(aq,c^2q;q^2)_{n/2}},&n\text{ 为偶数},\\0,&n\text{ 为奇数}.\end{cases}
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-II-17`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-II-17**（Appendix II, (II.17), 印刷p355）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。n 为非负整数；q 为非零且非单位根的复数；所有显示的分母非零。 s,c≠0，a=s²/q（故 s²=aq）。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-II-19 · 终止 q-Whipple 的有限乘积形式

$$
{}_4\phi_3^{[n]}\!\left[\begin{matrix}q^{-n},q^{n+1},c,-c\\e,c^2q/e,-q\end{matrix};q,q\right]=q^{n(n+1)/2}\frac{(eq^{-n},c^2q^{1-n}/e;q^2)_\ell}{(eq^\epsilon,c^2q^{1+\epsilon}/e;q^2)_\ell},\quad\ell=\lceil n/2\rceil,\quad\epsilon=1-(n\bmod2).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-II-19`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-II-19**（Appendix II, (II.19), 印刷p355）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。e≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AQ-4.24 · q-Dixon 三个 Gaussian 的交错求和

$$
\sum_{k=-\min(a,b,c)}^{\min(a,b,c)}(-1)^kq^{k(3k+1)/2}\begin{bmatrix}b+c\\c+k\end{bmatrix}_q\begin{bmatrix}c+a\\a+k\end{bmatrix}_q\begin{bmatrix}a+b\\b+k\end{bmatrix}_q=\frac{(q;q)_{a+b+c}}{(q;q)_a(q;q)_b(q;q)_c}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AQ-4.24`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_Q_supplement.md](../../round1_source_collection/records/ANDREWS_Q_supplement.md)；[ANDREWS_Q.md](../../round1_source_collection/books/ANDREWS_Q.md)。

- **AQ-4.24**（印刷页 38；式 (4.24)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 a,b,c≥0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
