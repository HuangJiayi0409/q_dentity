# FQI-ROGERS-SZEGO-RECURRENCE · Rogers–Szegő 三项递推

家族：C · 递推与差分关系；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
H_{n+1}(t;q)=(1+t)H_n(t;q)-(1-q^n)tH_{n-1}(t;q).
$$

代表来源：`AP-3.E6`。

局部定义：\(H_n(t;q)=\sum_{j=0}^n\begin{bmatrix}n\\j\end{bmatrix}_q t^j\)；n≥0。

来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **AP-3.E6**（ANDREWS-P；p.49, Example 6）：n≥1 为整数。
  变量对应：代表式；保留本条来源域。
- **FINE-20.63b**（FINE；印刷页 28；式 (20.63b)；A general transformation）：q 为形式变量；数值代入要求所有实际分母非零，Gaussian 在奇点先作多项式延拓。空乘积为 1、空和为 0。n≥1；f_0(u)=1，f_1(u)=1+u。
  变量对应：f_n(u)=H_n(u;q)，u→t；将后两项移到右侧。
- **KAC-CHEUNG-7.RogersSzego**（KAC-CHEUNG；印刷页 26；7.RogersSzego）：空积为1；整数指标；q≠0,1，所有实际分母非零。多项式恒等式可在约分后延拓。n≥1。
  变量对应：H_n(t)=H_n(t;q)；q^n−1=−(1−q^n)。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_P.md`
- `round1_source_collection/books/FINE.md`
- `round1_source_collection/books/KAC_CHEUNG.md`
- `round1_source_collection/records/ANDREWS_P_supplement.md`
- `round1_source_collection/records/FINE_supplement.md`
- `round1_source_collection/records/KAC_CHEUNG_supplement.md`
