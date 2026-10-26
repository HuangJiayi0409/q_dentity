# 良配求和及 Watson、Sears、Bailey 变换

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 已有自动证明流程（旧条件域） 3 条；已有 Lean 证明实现（旧条件域） 1 条；已有可复用部件，待组装 1 条；仅相关路线，未覆盖本式 1 条；本次未匹配到旧算法 20 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

## FQI-TERMINATING-6PHI5 · 终止 very-well-poised 6φ5

$$
W_6^{[n]}(a;b,c,q^{-n};q,aq^{n+1}/(bc))=\frac{(aq,aq/(bc);q)_n}{(aq/b,aq/c;q)_n}
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-II-21`。

**证明算法状态：已有自动证明流程（旧条件域）**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-TERMINATING-6PHI5)

方法：良配终止和的一阶 q-WZ。

覆盖边界：旧定理使用 Generic 和对所有递推层成立的非零条件；比目录仅要求当前有限式分母非零更强。尚未证明目录全部条件能推出这些假设。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-II-21**（Appendix II, (II.21), 印刷p356）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。n 为非负整数；q 为非零且非单位根的复数；所有显示的分母非零。 a≠0。 b,c≠0，a≠1。
  对应：代表式；保留本条来源域。
- **SILLS-1.Thm1.50**（印刷页 32；1.Thm1.50）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0，bc≠0；a=1时先约去可去因子。
  对应：展开 W_6^[n]；此式是 6φ5，不能因名称 Jackson 而并入 8φ7。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-WATSON-8PHI7 · Watson 终止 8φ7→4φ3

$$
W_8^{[n]}(a;b,c,d,e,q^{-n};q,a^2q^{n+2}/(bcde))=\frac{(aq,aq/(de);q)_n}{(aq/d,aq/e;q)_n}{}_4\phi_3^{[n]}\!\left[\begin{matrix}aq/(bc),d,e,q^{-n}\\aq/b,aq/c,deq^{-n}/a\end{matrix};q,q\right]
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-III-18`。

**证明算法状态：已有自动证明流程（旧条件域）**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-WATSON-8PHI7)

方法：Watson 双侧二阶 q-WZ 与前因子共轭。

覆盖边界：旧定理使用 Generic 和对所有递推层成立的非零条件；比目录仅要求当前有限式分母非零更强。尚未证明目录全部条件能推出这些假设。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-III-18**（Appendix III, (III.18), 印刷p360）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。n 为非负整数；q 为非零且非单位根的复数；所有显示的分母非零。 a≠0。 b,c,d,e≠0，a≠1。
  对应：代表式；保留本条来源域。
- **AQ-3.49**（印刷页 31；式 (3.49)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 N≥0；q,a,b,c,d,e≠0，a≠1（可取可去奇点极限）。
  对应：N→n；展开 W_8^[n] 与右侧 4φ3。
- **SILLS-1.98**（印刷页 46；1.98）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0，abcde≠0。
  对应：展开左侧 W_8^[n]；右侧上参数可交换次序。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SEARS-4PHI3-II · Sears 平衡 4φ3 第二形式

$$
{}_4\phi_3^{[n]}\!\left[\begin{matrix}q^{-n},a,b,c\\d,e,f\end{matrix};q,q\right]=\frac{(a,ef/(ab),ef/(ac);q)_n}{(e,f,ef/(abc);q)_n}{}_4\phi_3^{[n]}\!\left[\begin{matrix}q^{-n},e/a,f/a,ef/(abc)\\ef/(ab),ef/(ac),q^{1-n}/a\end{matrix};q,q\right]
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-III-16`。

**证明算法状态：仅相关路线，未覆盖本式**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SEARS-4PHI3-II)

方法：Sears 已有另一参数形式。

覆盖边界：未核对并实现两种形式间的完整参数变换与前因子桥接。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-III-16**（Appendix III, (III.16), 印刷p360）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。n 为非负整数；q 为非零且非单位根的复数；所有显示的分母非零。 a≠0。 b,c,e,f≠0；平衡条件 def=abc q^{1-n}。
  对应：代表式；保留本条来源域。
- **SILLS-1.104**（印刷页 48；1.104）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0，abcde≠0。
  对应：GR 的 (a,b,c,d,e,f)=(Sills b,a,c,abc q^(1−n)/(de),d,e)；平衡条件 def=abc q^(1−n) 随代换保留。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-2.3.4 · 终止 very-well-poised 4φ3 消去

$$
\sum_{k=0}^n\frac{1-aq^{2k}}{1-a}\frac{(a,q^{-n};q)_k}{(q,aq^{n+1};q)_k}q^{nk}=\delta_{n,0}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-2.3.4`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-2.3.4**（Chapter 2, 2.3.4, 印刷p42）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。a≠1。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-2.10.3 · 两侧终止的 Bailey 8φ7 变换

$$
W_8^{[n]}(a;b,c,d,e,q^{-n};q,a^2q^{n+2}/(bcde))=\frac{(aq,\lambda q/e;q)_n}{(aq/e,\lambda q;q)_n}W_8^{[n]}(\lambda;\lambda b/a,\lambda c/a,\lambda d/a,e,q^{-n};q,aq^{n+1}/e),\quad\lambda=qa^2/(bcd).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-2.10.3`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-2.10.3**（Chapter 2, 2.10.3, 印刷p49）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。abcdeλ≠0，a,λ≠1。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-2.10.8 · 迭代 Bailey 终止 10φ9 变换

$$
W_{10}^{[n]}(a;b,c,d,e,f,a^3q^{n+2}/(bcdef),q^{-n};q,q)=\frac{(aq,aq/(de),aq/(df),aq/(ef);q)_n}{(aq/d,aq/e,aq/f,aq/(def);q)_n}W_{10}^{[n]}(defq^{-n-1}/a;aq/(bc),d,e,f,bdefq^{-n-1}/a^2,cdefq^{-n-1}/a^2,q^{-n};q,q).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-2.10.8`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-2.10.8**（Chapter 2, 2.10.8, 印刷p50）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。abcdef≠0；各W首参数≠1。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-2.Ex5 · 不定 very-well-poised 有限和

$$
W_6^{[n]}(a;b,c,a/(bc);q,q)=\frac{(aq,bq,cq,aq/(bc);q)_n}{(q,aq/b,aq/c,bcq;q)_n}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-2.Ex5`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-2.Ex5**（Chapter 2, 2.Ex5, 印刷p58）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。abc≠0，a≠1。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-2.Ex12 · 成对参数的终止 10φ9 求和

$$
\sum_{k=0}^n\frac{1-aq^{2k}}{1-a}\frac{(a,a/b,a^2q^{n+1}/b,q^{-n};q)_k(b,bq;q^2)_kq^k}{(q,bq,bq^{-n}/a,aq^{n+1};q)_k(a^2q^2/b,a^2q/b;q^2)_k}=\frac{(aq,a^2q/b^2;q)_n}{(aq/b,a^2q/b;q)_n}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-2.Ex12`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

**组级探索：成对参数与混合底数**。已记录[公共规范化及不同证明路线](../../finite_product_framework/docs/q_mixed_base_group.md)。Ex12走二阶证书；Ex15/Ex16现有系数网格及特化组合的受限域框架。不因家族归属要求共用tactic。

**后续框架**：[显式候选驱动的二阶Lean框架](../../finite_product_framework/docs/q_mixed_base_framework.md)已生成，并注册qwz_framework using显式二阶策略；原式规范化、零初值及公共组装已证，仍有6项局部义务。候选来自此前CAS实验，本次未运行CAS；实际tactic和建议回放通过，Lean证书验证及目录域扩展未完成。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-2.Ex12**（Chapter 2, 2.Ex12, 印刷p59）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。ab≠0，a≠1。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-2.Ex14ii · 近良配6φ5到12φ11变换

$$
{}_6\phi_5^{[n]}(s^2,qs,b,c,d,q^{-n};s,s^2q/b,s^2q/c,s^2q/d,s^4q^{1-n}/\lambda^2;q,q)=\frac{(\lambda/s^2,\lambda^2/s^2,-\lambda q/s;q)_n}{(\lambda q,\lambda^2/s^4,-\lambda/s;q)_n}\sum_{k=0}^n\frac{(1-\lambda q^{2k})(\lambda,\lambda b/s^2,\lambda c/s^2,\lambda d/s^2,qs,-s,\lambda^2q^n/s^2,q^{-n};q)_k(s^2q;q^2)_kq^k}{(1-\lambda)(q,s^2q/b,s^2q/c,s^2q/d,\lambda/s,-\lambda q/s,s^2q^{1-n}/\lambda,\lambda q^{n+1};q)_k(\lambda^2q/s^2;q^2)_k}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-2.Ex14ii`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

**新框架：局部归纳与有限展开**。已构建[Ex14(i)/(ii)受限域framework](../../finite_product_framework/docs/q_nearly_poised_ex14.md)，分别保留1/4项义务；内层求和侧递推尚未证明，未搜得或提供望远镜证书。本轮未调用CAS，暂不计入完整证明或完成覆盖。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-2.Ex14ii**（Exercise 2.Ex14ii）：n≥0，a=s²，λ=qs⁴/(bcd)，参数非零，所有分母非零。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-2.Ex19 · 平衡终止 10φ9 的参数重排

$$
W_{10}^{[n]}(a;b,c,d,e,f,g,q^{-n};q,q)=\frac{(aq,aq/(ce),aq/(de),aq/(ef),aq/(eg),b;q)_n}{(aq/c,aq/d,aq/e,aq/f,aq/g,b/e;q)_n}e^nW_{10}^{[n]}(eq^{-n}/b;e,aq/(bc),aq/(bd),aq/(bf),aq/(bg),eq^{-n}/a,q^{-n};q,q).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-2.Ex19`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-2.Ex19**（Chapter 2, 2.Ex19, 印刷p62）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。abcdefg≠0，a³q^{n+2}=bcdefg；W首参数≠1。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-2.Ex20 · 终止 10φ9 的有限 4φ3 展开

$$
W_{10}^{[n]}(a;b,c,d,e,f,g,q^{-n};q,a^3q^{n+3}/(bcdefg))=\frac{(aq,aq/(fg);q)_n}{(aq/f,aq/g;q)_n}\sum_{j=0}^n\frac{(q^{-n},f,g,aq/(de);q)_jq^j}{(q,aq/d,aq/e,fgq^{-n}/a;q)_j}{}_4\phi_3^{[j]}(q^{-j},d,e,aq/(bc);aq/b,aq/c,deq^{-j}/a;q,q).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-2.Ex20`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

**新框架：Watson/Pfaff嵌套展开**。[受限域框架](../../finite_product_framework/docs/q_nested_watson.md)已接入qtransform_framework；权重桥接、乘法反写及换序组装已证，Watson实例、核分解、Pfaff实例、最终乘积桥接4块义务保留。无CAS，实际调用和建议回放通过；完整目录域未完成。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-2.Ex20**（Chapter 2, 2.Ex20, 印刷p62）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。abcdefg≠0，a≠1。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-2.Ex28 · 良配终止级数的有限展开

$$
{}_{r+3}\phi_{r+2}^{[n]}(a,\boldsymbol b,c,q^{-n};aq/\boldsymbol b,aq/c,aq^{n+1};q,qz)=\frac{(aq/(cz),q^{1-n}/c;q)_n}{(aq/c,q^{1-n}/(cz);q)_n}\sum_{k=0}^n\frac{(q^{-n}/(cz),1/z,q^{-n}/a,q^{-n};q)_k(1-q^{2k-n}/(cz))}{(q,aq/(cz),q/(cz),q^{1-n}/c;q)_k(1-q^{-n}/(cz))}\left(\frac{aq^{n+1}}c\right)^k{}_{r+3}\phi_{r+2}^{[n-k]}(a,\boldsymbol b,czq^{-k},q^{k-n};aq/\boldsymbol b,aq^{k+1}/(cz),aq^{n+1-k};q,q).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-2.Ex28`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

**新框架：任意权重6φ5核展开**。[受限域框架](../../finite_product_framework/docs/q_nested_expansion.md)已接入qtransform_framework；换序及条件式组装已证，核匹配、6φ5依赖、闭式桥接共3块义务保留。无CAS，完整目录域与自动提前截断尚缺，不增加完整证明数。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-2.Ex28**（Chapter 2, 2.Ex28, 印刷p64）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。r≥0，b向量长r，acz及各b_i非零。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-6.6.10 · 终止 8φ7 与有限部分和的变换

$$
W_8^{[m]}(a^2bc;abcd,ab,ac,a^2q^{m+1},q^{-m};q,q/(ad))=\frac{(a^2bcq,q,aq/b,aq/c;q)_m}{(qa^2,abq,acq,q/(bc);q)_m}\sum_{k=0}^m\frac{(1-a^2q^{2k})(a^2,ab,ac,ad;q)_k}{(1-a^2)(q,aq/b,aq/c,aq/d;q)_k}\left(\frac q{abcd}\right)^k.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-6.6.10`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

**新框架：有限部分和与代数退化**。[三条独立策略](../../finite_product_framework/docs/q_finite_degenerations.md)已接入qtransform_framework，分别保留6/4/3块义务；无CAS。共同和、零长度及代数代入机制已证；上游Watson/Heine与局部桥接未闭合，不增加完整证明数。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-6.6.10**（Chapter 6, 6.6.10, 印刷p165）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。m≥0，abcd≠0，a²≠1，a²bc≠1。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-8.7.9-finite · 终止良配 4φ3 的 2φ1 变换

$$
\sum_{k=0}^n\frac{1-aq^{2k}}{1-a}\frac{(a,q^{-n};q)_k}{(q,w;q)_k}\left(\frac{w}{aq}\right)^k=\frac{(wq^{-n-1}/a;q)_n}{(w;q)_n}{}_2\phi_1^{[\max(0,n-1)]}(q^{-n},q^{1-n};wq^{-n}/a;q,wq^n).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-8.7.9-finite`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

**新框架：有限部分和与代数退化**。[三条独立策略](../../finite_product_framework/docs/q_finite_degenerations.md)已接入qtransform_framework，分别保留6/4/3块义务；无CAS。共同和、零长度及代数代入机制已证；上游Watson/Heine与局部桥接未闭合，不增加完整证明数。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-8.7.9-finite**（Chapter 8, 8.7.9-finite, 印刷p230）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。aw≠0；n=0时右级数取单项1。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-8.Ex15 · 终止 4φ3 到 12W11 的变换

$$
{}_4\phi_3^{[n]}(a,b,c,d;bq/a,cq/a,dq/a;q,q^2/a^2)=\frac{(q^{1-n}/d,acq^{-n}/d;q)_n}{(aq^{-n}/d,cq^{1-n}/d;q)_n}W_{12}^{[n]}(bc/d;v,-v,u,-u,ab/d,ac/d,a,b,c;q,q/a),\quad b=q^{-n},\ u^2=bcq^2/(ad),\ v^2=bcq/(ad).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-8.Ex15`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

**组级探索：成对参数与混合底数**。已记录[公共规范化及不同证明路线](../../finite_product_framework/docs/q_mixed_base_group.md)。Ex12走二阶证书；Ex15/Ex16现有系数网格及特化组合的受限域框架。不因家族归属要求共用tactic。

**新框架：系数网格与特化组合**。[Ex15/Ex16受限域框架](../../finite_product_framework/docs/q_mixed_transform.md)已生成：有理式编译、保护网格延拓、Ex15组装和Ex16特化桥接已证；两条均保留Rogers系数恒等式及两侧逐项整理共3项上游义务。独立qcoefficient_framework已注册，实际调用及建议回放通过；无CAS，未接入qwz_framework；完整目录域及自动c终止转换尚缺。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-8.Ex15**（Chapter 8, 8.Ex15, 印刷p250）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。bcd≠0；c=q^{-n}分支由b,c对称性得到；原书还声称a=q^{-n}分支，n=0已有反例，该分支另存隔离。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-8.Ex16 · 终止 10W9 的 4φ3 表示

$$
W_{10}^{[n]}(a;s,-s,-q,a^2/b,a^2/c,b,c;q,q/a)=\frac{(aq,a^2/c;q)_n}{(a^2,aq/c;q)_n}{}_4\phi_3^{[n]}(a,b,c,bc/a;bq/a,cq/a,bcq/a^2;q,q^2/a^2),\quad b=q^{-n},\ s^2=q.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-8.Ex16`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

**组级探索：成对参数与混合底数**。已记录[公共规范化及不同证明路线](../../finite_product_framework/docs/q_mixed_base_group.md)。Ex12走二阶证书；Ex15/Ex16现有系数网格及特化组合的受限域框架。不因家族归属要求共用tactic。

**新框架：系数网格与特化组合**。[Ex15/Ex16受限域框架](../../finite_product_framework/docs/q_mixed_transform.md)已生成：有理式编译、保护网格延拓、Ex15组装和Ex16特化桥接已证；两条均保留Rogers系数恒等式及两侧逐项整理共3项上游义务。独立qcoefficient_framework已注册，实际调用及建议回放通过；无CAS，未接入qwz_framework；完整目录域及自动c终止转换尚缺。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-8.Ex16**（Chapter 8, 8.Ex16, 印刷p251）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。ac≠0；c=q^{-n}分支互换b,c；原印a=q^{-n}分支含未定义的无限乘积0/0，不作为有效有限分支；见覆盖清单。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-II-22 · Jackson 终止平衡 8φ7 求和

$$
W_8^{[n]}(a;b,c,d,e,q^{-n};q,q)=\frac{(aq,aq/(bc),aq/(bd),aq/(cd);q)_n}{(aq/b,aq/c,aq/d,aq/(bcd);q)_n}
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-II-22`。

**证明算法状态：已有 Lean 证明实现（旧条件域）**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SRC-GR2-II-22)

方法：已实现 Jackson 一阶 q-WZ 证书证明。

覆盖边界：旧定理使用 Generic 和对所有递推层成立的非零条件；比目录仅要求当前有限式分母非零更强。尚未证明目录全部条件能推出这些假设。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-II-22**（Appendix II, (II.22), 印刷p356）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。n 为非负整数；q 为非零且非单位根的复数；所有显示的分母非零。 a≠0。 b,c,d,e≠0，a≠1；平衡条件 a²q=bcde q^{-n}，即 e=a²q^{n+1}/(bcd)。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-III-14 · Sears–Carlitz 终止变换

$$
{}_3\phi_2^{[n]}\!\left[\begin{matrix}a,b,c\\aq/b,aq/c\end{matrix};q,aqz/(bc)\right]=(az;q)_n\sum_{k=0}^{\lfloor n/2\rfloor}\frac{(a;q)_{2k}(aq/(bc);q)_k}{(q,aq/b,aq/c,az,q/z;q)_k}q^k,\qquad a=q^{-n}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-III-14`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

**新框架：Pfaff与有限q-二项式半长度展开**。[III.14受限域框架](../../finite_product_framework/docs/q_sears_carlitz.md)已接入qtransform_framework；终止支撑、行及整体组装已证，6块局部/上游义务保留，无CAS。完整目录域传递尚缺，不增加完整证明数。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-III-14**（Appendix III, (III.14), 印刷p360）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。bcz≠0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-III-15 · Sears 平衡终止 4φ3 变换

$$
{}_4\phi_3^{[n]}\!\left[\begin{matrix}q^{-n},a,b,c\\d,e,f\end{matrix};q,q\right]=a^n\frac{(e/a,f/a;q)_n}{(e,f;q)_n}{}_4\phi_3^{[n]}\!\left[\begin{matrix}q^{-n},a,d/b,d/c\\d,aq^{1-n}/e,aq^{1-n}/f\end{matrix};q,q\right]
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-III-15`。

**证明算法状态：已有自动证明流程（旧条件域）**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SRC-GR2-III-15)

方法：Sears 双侧二阶 q-WZ 与前因子共轭。

覆盖边界：旧定理使用 Generic 和对所有递推层成立的非零条件；比目录仅要求当前有限式分母非零更强。尚未证明目录全部条件能推出这些假设。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-III-15**（Appendix III, (III.15), 印刷p360）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。n 为非负整数；q 为非零且非单位根的复数；所有显示的分母非零。 a≠0。 b,c,e,f≠0；平衡条件 def=abc q^{1-n}。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-III-19 · 终止平衡 4φ3 的 very-well-poised 反写

$$
{}_4\phi_3^{[n]}\!\left[\begin{matrix}q^{-n},a,b,c\\d,e,f\end{matrix};q,q\right]=\frac{(d/b,d/c;q)_n}{(d,d/(bc);q)_n}W_8^{[n]}(\sigma;f/a,e/a,b,c,q^{-n};q,efq^n/(bc)),\quad\sigma=ef/(aq).
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`GR2-III-19`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-III-19**（Appendix III, (III.19), 印刷p361）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。abcdef≠0，σ≠1；def=abcq^{1−n}。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-III-25 · 近良配 5φ4 到 12φ11 变换

$$
{}_5\phi_4^{[n]}\!\left[\begin{matrix}a,b,c,d,q^{-n}\\aq/b,aq/c,aq/d,a^2q^{-n}/\lambda^2\end{matrix};q,q\right]=\frac{(\lambda q/a,\lambda^2q/a;q)_n}{(\lambda q,\lambda^2q/a^2;q)_n}\mathcal V_n(\lambda;b\lambda/a,c\lambda/a,d\lambda/a;a,aq;\lambda^2q^{n+1}/a,q^{-n}),\quad\lambda=qa^2/(bcd).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-III-25`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

**新框架：原书展开＋局部CAS证书**。已构建[III.25受限域framework](../../finite_product_framework/docs/q_nearly_poised.md)，实时搜索内层Pfaff证书；CAS路线7项义务，直接路线4项。目录条件域扩展尚缺，未计入完整证明或原有覆盖汇总。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-III-25**（Appendix III, (III.25), 印刷p362）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。abcdλ≠0，λ≠1；V的显式有限定义见辅助说明。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-III-26 · 终止近良配 5φ4 的半长度变换

$$
{}_5\phi_4^{[n]}\!\left[\begin{matrix}q^{-n},b,c,d,e\\q^{1-n}/b,q^{1-n}/c,q^{1-n}/d,eq^{-2n}/\mu^2\end{matrix};q,q\right]=\frac{(\mu^2q^{n+1},\mu q/e;q)_n}{(\mu^2q^{n+1}/e,\mu q;q)_n}\mathcal V_{\lfloor n/2\rfloor}(\mu;\mu bq^n,\mu cq^n,\mu dq^n;q^{-n},q^{1-n};e,\mu^2q^{n+1}/e),\quad\mu=q^{1-2n}/(bcd).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-III-26`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

**证书路线标记：符号计算尚未做得了**（一般参数证书尚未求出）。另已构建无需CAS的[原书有限展开framework](../../finite_product_framework/docs/q_half_length_expansion.md)，qtransform_framework仅接收显式中间分母条件，保留5项局部义务；目录条件域扩展未完成，暂不计入完成覆盖。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-III-26**（Appendix III, (III.26), 印刷p362）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。bcdeµ≠0，µ≠1；V见辅助说明。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-III-27 · 近良配 7φ6 到 12φ11 变换

$$
\sum_{k=0}^n\frac{1-aq^{2k}}{1-a}\frac{(a,b,c,d,q^{-n};q)_k}{(q,aq/b,aq/c,aq/d,a^2q^{2-n}/\lambda^2;q)_k}q^k=\frac{(\lambda/(aq),\lambda^2/(aq);q)_n}{(\lambda q,\lambda^2/(a^2q);q)_n}\frac{1-\lambda^2q^{2n-1}/a}{1-\lambda^2/(aq)}\mathcal V_n(\lambda;b\lambda/a,c\lambda/a,d\lambda/a;aq,aq^2;\lambda^2q^{n-1}/a,q^{-n}),\quad\lambda=qa^2/(bcd).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-III-27`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

**新框架：原书展开与内层变换组合**。已构建[III.27受限域framework](../../finite_product_framework/docs/q_nearly_poised_second.md)，内层III.25特化与Jackson求和保留显式依赖，共6项局部义务；本轮无需CAS，目录条件域扩展未完成，暂不计入完成覆盖。

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-III-27**（Appendix III, (III.27), 印刷p362）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。abcdλ≠0，a,λ≠1；V见辅助说明。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-GR2-III-28 · Bailey 终止 10φ9 变换

$$
W_{10}^{[n]}(a;b,c,d,e,f,\lambda aq^{n+1}/(ef),q^{-n};q,q)=\frac{(aq,aq/(ef),\lambda q/e,\lambda q/f;q)_n}{(aq/e,aq/f,\lambda q/(ef),\lambda q;q)_n}W_{10}^{[n]}(\lambda;\lambda b/a,\lambda c/a,\lambda d/a,e,f,\lambda aq^{n+1}/(ef),q^{-n};q,q),\quad\lambda=qa^2/(bcd).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`GR2-III-28`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[GR2_supplement.md](../../round1_source_collection/records/GR2_supplement.md)；[GR.md](../../round1_source_collection/books/GR.md)。

- **GR2-III-28**（Appendix III, (III.28), 印刷p363）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。abcdefλ≠0，a,λ≠1。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-1.99 · Watson 终止和二阶递推

$$
f_n=\frac{(aq^n-1)(q^n-q)(aq^n-q)(bcde-a^2q^n)}{q(b-aq^n)(c-aq^n)(d-aq^n)(e-aq^n)}f_{n-2}+\frac{aq^n-1}{q(b-aq^n)(c-aq^n)(d-aq^n)(e-aq^n)}\bigl[a^3(q+1)q^{3n}+q^{n+1}(a^2q+a(bec+bed+bcd+cde)+bcde)-aq^{2n}(aq(a+b+c+d+e)+bcde)-bcde(q+1)q\bigr]f_{n-1}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`SILLS-1.99`。

**证明算法状态：已有可复用部件，待组装**。 [核对依据](../PROOF_ALGORITHMS.md#proof-FQI-SRC-SILLS-1.99)

方法：Watson 和的二阶递推系数重写。

覆盖边界：旧定理使用 Generic 和对所有递推层成立的非零条件；比目录仅要求当前有限式分母非零更强。尚未证明目录全部条件能推出这些假设。 本次未形式化两种系数排版的相等性。

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-1.99**（印刷页 46；1.99）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥2；f_n 为(1.98)左侧终止和。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-SILLS-2.9-corrected · Watson 极限的终止有限式

$$
\sum_{k=0}^n\frac{(1-aq^{2k})(a,q^{-n};q)_k a^{2k}q^{(n+2)k+4\binom k2}}{(1-a)(q;q)_k(aq^{n+1};q)_k}=(aq;q)_n\sum_{k=0}^n\frac{(q^{-n};q)_k}{(q;q)_k}(-1)^ka^kq^{(n+1)k+\binom k2}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`SILLS-2.9-corrected`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

**新框架：有限部分和与代数退化**。[三条独立策略](../../finite_product_framework/docs/q_finite_degenerations.md)已接入qtransform_framework，分别保留6/4/3块义务；无CAS。共同和、零长度及代数代入机制已证；上游Watson/Heine与局部桥接未闭合，不增加完整证明数。

定义文件：[SILLS_supplement.md](../../round1_source_collection/records/SILLS_supplement.md)；[SILLS.md](../../round1_source_collection/books/SILLS.md)。

- **SILLS-2.9-corrected**（印刷页 56；2.9-corrected）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
