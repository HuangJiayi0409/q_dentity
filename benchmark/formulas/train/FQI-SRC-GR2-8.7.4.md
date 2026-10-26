# FQI-SRC-GR2-8.7.4 · q-Racah乘积双重展开修正式

家族：A · 超几何型有限求和；难度：高；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
W_n(x;a,b,c,N)W_n(y;\alpha,ab/\alpha,\gamma,M)=\frac{(bq,aq/c;q)_nc^n}{(aq,bcq;q)_n}\sum_{r=0}^n\sum_{s=0}^{n-r}\frac{(q^{-n},abq^{n+1};q)_{r+s}(q^{-x},cq^{x-N},q^{-y},\gamma q^{y-M};q)_r}{(q^{-N};q)_{r+s}(q,\alpha q,q^{-M},ab\gamma q/\alpha,cq^{1-s};q)_r}\frac{(q^{x-N},c^{-1}q^{-x};q)_s(1-cq^{r-s})q^{r+s-rs}}{(q,bq,aq/c;q)_s(1-cq^{-s})}A_{r,s}.
$$

代表来源：`GR2-8.7.4`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-8.7.4**（GR；Chapter 8, 8.7.4, 印刷p230）：0≤n,x≤N≤M，0≤y≤M；A_{r,s}及W见8.Ex8。取r≤min(n,x,y)，s≤min(n−r,N−x)；外系数为零的项不计算内部级数；实际分母非零。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
