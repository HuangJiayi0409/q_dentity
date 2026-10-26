# FQI-SRC-FINE-7.GH · q-移位迭代的有限累积系数

家族：A · 超几何型有限求和；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
H_n=\frac{(b/a;q)_{n+1}}{(bq;q)_{n+1}(b/(at);q)_{n+1}},\qquad G_n=-\frac{b/(at)}{1-b/(at)}\sum_{j=0}^n\frac{(b/a;q)_j q^j}{(bq;q)_j(bq/(at);q)_j}.
$$

代表来源：`FINE-7.GH`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **FINE-7.GH**（FINE；印刷页5；§7 开头、(7.1) 前的无编号 H_n、G_n）：q 为形式变量；数值代入要求所有实际分母非零，Gaussian 在奇点先作多项式延拓。空乘积为 1、空和为 0。n≥0，at≠0；L_j=bq^j/(bq^j−at)，M_j=(bq^j−a)t/((1−bq^{j+1})(bq^j−at))；H_{−1}=1,G_{−1}=0；H_n=M_nH_{n−1},G_n=G_{n−1}+L_nH_{n−1}。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/FINE.md`
- `round1_source_collection/records/FINE_supplement.md`
