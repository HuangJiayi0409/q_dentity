# FQI-SRC-GR2-3.Ex21-mixed · 双底数与普通超几何的混合有限变换

家族：G · 差分域／环、参数关系与生成函数；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
\sum_{k=0}^nK_k(a,b,c;p,q)\frac{(C-A-n)_k(-B-C-n)_k(\mu B-\mu A-n)_k(-n)_k}{(-\mu C-n)_k(\mu B+\mu C-\mu A-n)_k(-A-n)_k(-B-n)_k}=T_n(a,b,c;p,q)\frac{n!(\mu A+1-\mu B)_n(A+1-C)_n(B+C+1)_n}{(A+1)_n(B+1)_n(\mu C+1)_n(\mu A+1-\mu B-\mu C)_n}\sum_{k=0}^n\frac{(A+k+k/\mu)(B+k-k/\mu)}{AB}\frac{(A)_k(B)_k(\mu C)_k(\mu A-\mu B-\mu C)_k}{k!(\mu A+1-\mu B)_k(A+1-C)_k(B+C+1)_k}R_{n,k}(a,b,c;p,q).
$$

代表来源：`GR2-3.Ex21-mixed`。


来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **GR2-3.Ex21-mixed**（GR；Chapter 3, 3.Ex21-mixed, 印刷p106）：n为非负整数；底数非零且非单位根；所有实际有限乘积/求和项的分母非零。空积为1，求和显式截断后不计算尾部0/0。K,T,R同四底数变换；(x)_k为普通上升阶乘；ABµabc≠0。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/GR.md`
- `round1_source_collection/records/GR2_supplement.md`
