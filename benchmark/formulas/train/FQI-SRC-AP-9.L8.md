# FQI-SRC-AP-9.L8 · 分拆筛辅助有限和的递推

家族：C · 递推与差分关系；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
f(A,r;X,Y,L)-f(A,r-1;X,Y,L)-f(A-1,r+1;X,Y,L)+f(A-1,r;X,Y,L)=q^{L+2A+2Y+r}\begin{bmatrix}2A+X+r-2\\A+Y\end{bmatrix}_{q}.
$$

代表来源：`AP-9.L8`。

局部定义：\(f(A,r;X,Y,L)=F(2A+X,A+Y+1,r,L)\)，其中 \(F(T,D,R,E)=q^E[R+1]_{q^D}{T\brack D-1}_q+\sum_{j=0}^{R-2}q^{E+D+j+1}[R-j-1]_{q^D}{T+j\brack D-2}_q\)，\([s]_z=\sum_{h=0}^{s-1}z^h\)（s≥0）；空和为0。

来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **AP-9.L8**（ANDREWS-P；p.147, Lemma 9.8）：r≥1，A,X,Y,L 为整数，2A+X≥2；q 可逆。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_P.md`
- `round1_source_collection/records/ANDREWS_P_supplement.md`
