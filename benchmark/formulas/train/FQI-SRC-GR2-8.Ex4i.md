# FQI-SRC-GR2-8.Ex4i · q-Hahn 乘积的另一有限双和

家族：A · 超几何型有限求和；难度：高；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
Q_n(x)Q_n(y)=\frac{(bq,abq^{N+2};q)_n(bq^{N+1})^{-n}}{(aq,q^{-N};q)_n}\sum_{m=0}^n\frac{(q^{-n},abq^{n+1},bq^{N-x+1},bq^{N-y+1};q)_mq^m}{(q,bq,abq^{N+2},bq^{N+1};q)_m}\sum_{k=0}^{\min(m,x,y)}\frac{1-b^{-1}q^{2k-N-m-1}}{1-b^{-1}q^{-N-m-1}}\frac{(b^{-1}q^{-N-m-1},a^{-1}b^{-1}q^{-N-m-1},b^{-1}q^{-m},q^{-m},q^{-x},q^{-y};q)_k(ab)^kq^{(x+y+2m+2-k)k}}{(q,aq,q^{-N},b^{-1}q^{-N},b^{-1}q^{x-N-m},b^{-1}q^{y-N-m};q)_k}.
$$

代表来源：`GR2-8.Ex4i`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-8.Ex4i**（GR；Chapter 8, 8.Ex4i, 印刷p246）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。0≤n,x,y≤N；Q=Q_n(·;a,b,N)，ab≠0。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
