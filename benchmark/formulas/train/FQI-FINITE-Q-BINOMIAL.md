# FQI-FINITE-Q-BINOMIAL · 有限 q-二项式定理

家族：A · 超几何型有限求和；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\sum_{k=0}^n(-1)^kz^kq^{k(k-1)/2}\begin{bmatrix}n\\k\end{bmatrix}_q=(z;q)_n.
$$

代表来源：`SILLS-1.56`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **SILLS-1.56**（SILLS；印刷页 35；1.56）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。n≥0。
  变量对应：代表式；保留本条来源域。
- **AP-3.3.6**（ANDREWS-P；p.36, Theorem 3.3, (3.3.6)）：N≥0 为整数；z,q 为形式变量。
  变量对应：N→n，j→k，交换等号两侧。
- **FINE-6.23**（FINE；印刷页 5；式 (6.23)）：q 为形式变量；数值代入要求所有实际分母非零，Gaussian 在奇点先作多项式延拓。空乘积为 1、空和为 0。N≥0 为整数；t、q 为参数。
  变量对应：z=tq；q≠0 时可逆代换；q=0 的原式单独按多项式解释。
- **GR2-II-04**（GR；Appendix II, (II.4), 印刷p354）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。n 为非负整数；q 为非零且非单位根的复数；所有显示的分母非零。
  变量对应：展开有限 1φ0 并用 (q^−n;q)_k/(q;q)_k=(−1)^k q^{k(k−1)/2−nk}[n choose k]_q；令原 z=q^n z。
- **KAC-CHEUNG-5.5**（KAC-CHEUNG；印刷页 15；5.5）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。n≥0。
  变量对应：P_n(x,−a;q)=x^n(−a/x;q)_n；取 z=−a/x 后乘 x^n，x=0 由多项式恒等式延拓。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_P.md`
- `round1_source_collection/books/FINE.md`
- `round1_source_collection/books/GR.md`
- `round1_source_collection/books/KAC_CHEUNG.md`
- `round1_source_collection/books/SILLS.md`
- `round1_source_collection/records/ANDREWS_P_supplement.md`
- `round1_source_collection/records/FINE_supplement.md`
- `round1_source_collection/records/GR2_supplement.md`
- `round1_source_collection/records/KAC_CHEUNG_supplement.md`
- `round1_source_collection/records/SILLS_supplement.md`
