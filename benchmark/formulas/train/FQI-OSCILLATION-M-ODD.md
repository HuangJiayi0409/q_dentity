# FQI-OSCILLATION-M-ODD · 振荡分拆闭式：M-ODD

家族：C · 递推与差分关系；难度：高；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
M_{k,i}(a,b;2\mu-1;q)=q^{(2\mu-1)((2k+1)\mu-2k+i-1)}\begin{bmatrix}a+b\\b-(2k+1)\mu+2k-i+1\end{bmatrix}_{q}.
$$

代表来源：`AP-9.3.10`。

局部定义：对矩形 a×b 内的分拆 λ，r_j=λ_j−λ′_j（1≤j≤Durfee长度）。正振荡从 r>2k−i−1 开始，随后 r≤−(i−1)，再交替；负振荡从后一不等式开始。取满足交替条件的递增下标子序列最大长度。P/M 分别按 q^{|λ|} 计正/负振荡长度至少指定阈值的分拆；含空分拆。

来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **AP-9.3.10**（ANDREWS-P；p.149, Theorem 9.9, (9.3.10)）：a,b≥0，b=a 或 a−1；k≥i≥1；μ≥1；均为整数。
  变量对应：代表式；保留本条来源域。
- **AP-9.3.14**（ANDREWS-P；p.149, (9.3.14); (9.3.26)–(9.3.27), p.152）：a,b≥0，k≥i≥1，μ≥1，a−b≥−(i−1)；均为整数。
  变量对应：同一闭式；保留两个来源域的析取，不取条件交集或笛卡尔积。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_P.md`
- `round1_source_collection/records/ANDREWS_P_supplement.md`
