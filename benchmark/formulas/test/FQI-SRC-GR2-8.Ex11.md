# FQI-SRC-GR2-8.Ex11 · Askey–Wilson 的有限加法公式

家族：A · 超几何型有限求和；难度：高；集合：test。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
P_n(v;a,as,-a,-as)=\sum_{k=0}^nA_{k,n}(z,w)P_k(v;azw,a/(zw),az/w,aw/z),\quad A_{k,n}=\frac{(q;q)_n(a^4q^n,a^4/q,a^2s,-a^2s,-a^2;q)_ka^{n-k}}{(q;q)_k(q;q)_{n-k}(a^4/q;q)_{2k}(a^2s,-a^2s,-a^2;q)_n}P_{n-k}(z;as^k,as^{k+1},-as^k,-as^{k+1})P_{n-k}(w;as^k,as^{k+1},-as^k,-as^{k+1}),\quad s^2=q.
$$

代表来源：`GR2-8.Ex11`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-8.Ex11**（GR；Chapter 8, 8.Ex11, 印刷p249）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。azwv≠0；P见7.5.3，原书x=cosθ,y=cosφ，本表以z=e^{iθ},w=e^{iφ}表示。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
