# FQI-SRC-GR2-8.2.12 · Bateman 型终止乘积公式

家族：A · 超几何型有限求和；难度：高；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
F_n(b,b_1,b_2,b_3)F_n(b,bb_3c_1/(aq),bb_3/(b_1b_2c_1),b_3)=\frac{(aq/b,aq/b_3;q)_n}{(b,b_3;q)_n}\left(\frac{bb_3}{aq}\right)^n\sum_{m=0}^n\frac{(q^{-n},aq^n,b_1c_1,b_2c_1,aq/(b_1b_2c_1);q)_mq^m}{(q,aq/b,aq/b_3,b_1b_2c_1,bb_3/(b_1b_2);q)_m}W_{10}^{[m]}(\mu;b_1,b_2,b_1b_2c_1/b,b_1b_2c_1/b_3,bb_3c_1/(aq),aq^m,q^{-m};q,q),\quad\mu=b_1b_2c_1/q.
$$

代表来源：`GR2-8.2.12`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-8.2.12**（GR；Chapter 8, 8.2.12, 印刷p220）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。F_n见8.2.5；8.2.6中c2=aq/(b1b2c1)。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
