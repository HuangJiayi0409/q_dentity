# FQI-GOLLNITZ-RECURRENCE · Göllnitz 有界分拆递推

家族：C · 递推与差分关系；难度：中；集合：train。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
G_N=G_{N-1}+\begin{cases}tq^NG_{N-6},&N\equiv2,4,5\pmod6,\\t^2q^NG_{N-7},&N\equiv0,1,3\pmod6.\end{cases}
$$

代表来源：`SILLS-2.82-83`。

局部定义：G_N(t,q)计数最大部件≤N的分拆：不含1、3；相邻差≥6，当较大部件≡0,1,3 mod6时差>6。部件≡2,4,5 mod6的t权为1，其余为2；q权为总和。G₋₁=1，G₋₇=0。

来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **SILLS-2.82-83**（SILLS；印刷页 85；2.82-83）：整数指标；q 为形式变量或使实际分母非零的数。空积为1；Gaussian在0≤k≤n之外为0；有负幂时q≠0。N≥7；G₀=G₁=1，G₂=G₃=1+tq²，G₄=1+tq²+tq⁴，G₅=1+tq²+tq⁴+tq⁵，G₆=G₅+t²q⁶。
  变量对应：代表式；保留本条来源域。
- **AQ-10.17**（ANDREWS-Q；印刷页 102；式 (10.17)）：q 为形式变量（有理式在分母非零处解释）；所有长度、上指标为非负整数；Gaussian 越界为零。 n≥2，a∈{0,…,5}；χ(a)=1 当 a∈{1,2,4}，否则为0；d_N 定义及初值见书籍说明。
  变量对应：d_N(t)=G_N(t,q)，N=6n−a；χ(a)=1 对应 N≡2,4,5，其余三类为0。保留 AQ n≥2 与 Sills N≥7 的各自域。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_Q.md`
- `round1_source_collection/books/SILLS.md`
- `round1_source_collection/records/ANDREWS_Q_supplement.md`
- `round1_source_collection/records/SILLS_supplement.md`
