# FQI-SRC-AP-9.3.17 · M振荡闭式的剩余参数域

家族：C · 递推与差分关系；难度：高；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
M_{k,i}(a-1,a+i-1+r;2\mu;q)=F(2a+i-3,a+i-1-(2k+1)\mu,r+1,\mu((4k+2)\mu+2k-2i+1)).
$$

代表来源：`AP-9.3.17`。

局部定义：对矩形 a×b 内的分拆 λ，r_j=λ_j−λ′_j（1≤j≤Durfee长度）。正振荡从 r>2k−i−1 开始，随后 r≤−(i−1)，再交替；负振荡从后一不等式开始。取满足交替条件的递增下标子序列最大长度。P/M 分别按 q^{|λ|} 计正/负振荡长度至少指定阈值的分拆；含空分拆。 \(f(A,r;X,Y,L)=F(2A+X,A+Y+1,r,L)\)，其中 \(F(T,D,R,E)=q^E[R+1]_{q^D}{T\brack D-1}_q+\sum_{j=0}^{R-2}q^{E+D+j+1}[R-j-1]_{q^D}{T+j\brack D-2}_q\)，\([s]_z=\sum_{h=0}^{s-1}z^h\)（s≥0）；空和为0。

来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **AP-9.3.17**（ANDREWS-P；p.150, (9.3.17); (9.3.26)–(9.3.27), p.152）：a≥1，r≥−1；k≥i≥1，μ≥1；均为整数；q 可逆。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_P.md`
- `round1_source_collection/records/ANDREWS_P_supplement.md`
