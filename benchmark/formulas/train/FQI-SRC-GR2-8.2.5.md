# FQI-SRC-GR2-8.2.5 · 两个平衡终止 4φ3 的一般乘积展开

家族：A · 超几何型有限求和；难度：高；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
F_n(b,b_1,b_2,b_3)F_n(c,c_1,c_2,c_3)=\sum_{m=0}^n\frac{(q^{-n},aq^n,c_1,c_2,qab_1/(bb_3),qab_2/(bb_3);q)_mq^m}{(q,c,c_3,qa/(bb_3),qac_1c_2/(cc_3),qab_1b_2/(bb_3);q)_m}\sum_{j=0}^m\frac{1-\lambda_mq^{2j}}{1-\lambda_m}\frac{(\lambda_m,b_1,b_2,bq^{-m}/a,b_3q^{-m}/a,q^{-m};q)_j}{(q,bb_3q^{-m}/(ab_1),bb_3q^{-m}/(ab_2),b_3,b,bb_3/a;q)_j}\left(\frac{bb_3q^m}{b_1b_2}\right)^j{}_5\phi_4^{[j]}(q^{-j},q^{1-m}/c,q^{1-m}/c_3,\lambda_mq^j,cc_3q^{-m}/(ac_1c_2);q^{1-m}/c_1,q^{1-m}/c_2,bq^{-m}/a,b_3q^{-m}/a;q,q),\quad\lambda_m=bb_3q^{-m-1}/a.
$$

代表来源：`GR2-8.2.5`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-8.2.5**（GR；Chapter 8, 8.2.5, 印刷p219）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。F_n(d,u,v,w)=4φ3^[n](q^{-n},aq^n,u,v;d,w,qauv/(dw);q,q)；所列乘除参数非零。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
