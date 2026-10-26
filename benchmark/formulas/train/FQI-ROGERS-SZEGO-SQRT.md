# FQI-ROGERS-SZEGO-SQRT · Rogers–Szegő 平方根特值

家族：A · 超几何型有限求和；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
H_n(u;u^2)=(-u;u)_n.
$$

代表来源：`AP-3.E5`。

局部定义：\(H_n(t;q)=\sum_{j=0}^n\begin{bmatrix}n\\j\end{bmatrix}_q t^j\)；n≥0。

来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **AP-3.E5**（ANDREWS-P；p.49, Example 5）：n≥0；u 为形式变量。
  变量对应：代表式；保留本条来源域。
- **FINE-20.68**（FINE；印刷页 29；式 (20.68)；A general transformation）：q 为形式变量；数值代入要求所有实际分母非零，Gaussian 在奇点先作多项式延拓。空乘积为 1、空和为 0。n≥0；选择 q^{1/2} 的一个平方根。
  变量对应：选定 u=q_Fine^(1/2)，底数 q_Fine=u²；H_n(u;u²)=(−u;u)_n。根分支随来源保留。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_P.md`
- `round1_source_collection/books/FINE.md`
- `round1_source_collection/records/ANDREWS_P_supplement.md`
- `round1_source_collection/records/FINE_supplement.md`
