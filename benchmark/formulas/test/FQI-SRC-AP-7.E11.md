# FQI-SRC-AP-7.E11 · 有最大部分限制的 Göllnitz 型有限公式

家族：G · 差分域／环、参数关系与生成函数；难度：高；集合：test。

[统一记号与条件](../../metadata/NOTATION.md)

在以下来源条件及记号约定下，证明所列关系。

$$
d_{6n-1}(q)=\sum_{j=0}^{\lfloor n/2\rfloor}q^{6nj-3j^2+2j}\begin{bmatrix}n-j\\j\end{bmatrix}_{q^6}\Lambda_{n-2j}(q).
$$

代表来源：`AP-7.E11`。

局部定义：d_m(q)=Σ_λ q^{|λ|}，λ₁≤m，最小部分≠1,3，相邻差≥6，若较小部分≡0,1,3 (mod 6) 则差>6；空分拆计1。原书定义 Λ_n：(−xq²;q⁶)_∞(−xq⁴;q⁶)_∞(−xq⁵;q⁶)_∞/(x;q⁶)_∞=Σ_{n≥0}Λ_n x^n/(q⁶;q⁶)_n。固定 n 的系数可用有限运算得到；该无限生成式只作辅助定义，不另计有限恒等式。

来源条件分别适用，并按所列变量对应解释，不将不同来源的条件直接合取。

- **AP-7.E11**（ANDREWS-P；p.118, Example 11*（定义起于 p.117））：n≥1 为整数；q 为形式变量。
  变量对应：独立保留；未据名称或家族推断等价。

原目录的定义文件引用（保留出处路径，文件可用性见 README）：

- `round1_source_collection/books/ANDREWS_P.md`
- `round1_source_collection/records/ANDREWS_P_supplement.md`
