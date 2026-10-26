# 振荡分拆与有限分拆筛

[返回本库家族索引](../FAMILIES.md) · [统一记号与条件](../NOTATION.md)

有限 q 主库；每条显示代表式，来源域通过各自代换解释。

[CAS + Lean 核对报告](../PROOF_ALGORITHMS.md) · 本次未匹配到旧算法 14 条。

“已有”仅指对应旧实现及其条件域；当前条目的 Lean 记号包装与扩域仍须完成。

## FQI-OSCILLATION-M-EVEN · 振荡分拆闭式：M-EVEN

$$
M_{k,i}(a,b;2\mu;q)=q^{\mu((4k+2)\mu+2k-2i+1)}\begin{bmatrix}a+b\\b-(2k+1)\mu\end{bmatrix}_{q}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AP-9.3.9`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：对矩形 a×b 内的分拆 λ，r_j=λ_j−λ′_j（1≤j≤Durfee长度）。正振荡从 r>2k−i−1 开始，随后 r≤−(i−1)，再交替；负振荡从后一不等式开始。取满足交替条件的递增下标子序列最大长度。P/M 分别按 q^{|λ|} 计正/负振荡长度至少指定阈值的分拆；含空分拆。

定义文件：[ANDREWS_P_supplement.md](../../round1_source_collection/records/ANDREWS_P_supplement.md)；[ANDREWS_P.md](../../round1_source_collection/books/ANDREWS_P.md)。

- **AP-9.3.9**（p.148, Theorem 9.9, (9.3.9)）：a,b≥0，b=a 或 a−1；k≥i≥1；μ≥0；均为整数。
  对应：代表式；保留本条来源域。
- **AP-9.3.13**（p.149, (9.3.13); (9.3.26)–(9.3.27), p.152）：a,b≥0，k≥i≥1，μ≥1，a−b≥−(i−1)；均为整数。
  对应：同一闭式；保留两个来源域的析取，不取条件交集或笛卡尔积。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-OSCILLATION-M-ODD · 振荡分拆闭式：M-ODD

$$
M_{k,i}(a,b;2\mu-1;q)=q^{(2\mu-1)((2k+1)\mu-2k+i-1)}\begin{bmatrix}a+b\\b-(2k+1)\mu+2k-i+1\end{bmatrix}_{q}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AP-9.3.10`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：对矩形 a×b 内的分拆 λ，r_j=λ_j−λ′_j（1≤j≤Durfee长度）。正振荡从 r>2k−i−1 开始，随后 r≤−(i−1)，再交替；负振荡从后一不等式开始。取满足交替条件的递增下标子序列最大长度。P/M 分别按 q^{|λ|} 计正/负振荡长度至少指定阈值的分拆；含空分拆。

定义文件：[ANDREWS_P_supplement.md](../../round1_source_collection/records/ANDREWS_P_supplement.md)；[ANDREWS_P.md](../../round1_source_collection/books/ANDREWS_P.md)。

- **AP-9.3.10**（p.149, Theorem 9.9, (9.3.10)）：a,b≥0，b=a 或 a−1；k≥i≥1；μ≥1；均为整数。
  对应：代表式；保留本条来源域。
- **AP-9.3.14**（p.149, (9.3.14); (9.3.26)–(9.3.27), p.152）：a,b≥0，k≥i≥1，μ≥1，a−b≥−(i−1)；均为整数。
  对应：同一闭式；保留两个来源域的析取，不取条件交集或笛卡尔积。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-OSCILLATION-P-EVEN · 振荡分拆闭式：P-EVEN

$$
P_{k,i}(a,b;2\mu;q)=q^{\mu((4k+2)\mu-2k+2i-1)}\begin{bmatrix}a+b\\b+(2k+1)\mu\end{bmatrix}_{q}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AP-9.3.11`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：对矩形 a×b 内的分拆 λ，r_j=λ_j−λ′_j（1≤j≤Durfee长度）。正振荡从 r>2k−i−1 开始，随后 r≤−(i−1)，再交替；负振荡从后一不等式开始。取满足交替条件的递增下标子序列最大长度。P/M 分别按 q^{|λ|} 计正/负振荡长度至少指定阈值的分拆；含空分拆。

定义文件：[ANDREWS_P_supplement.md](../../round1_source_collection/records/ANDREWS_P_supplement.md)；[ANDREWS_P.md](../../round1_source_collection/books/ANDREWS_P.md)。

- **AP-9.3.11**（p.149, Theorem 9.9, (9.3.11)）：a,b≥0，b=a 或 a−1；k≥i≥1；μ≥0；均为整数。
  对应：代表式；保留本条来源域。
- **AP-9.3.15**（p.149, (9.3.15); (9.3.26)–(9.3.27), p.152）：a,b≥0，k≥i≥1，μ≥1，a−b≤2k−i；均为整数。
  对应：同一闭式；保留两个来源域的析取，不取条件交集或笛卡尔积。下指标 a−(2k+1)μ 与 b+(2k+1)μ 由上指标 a+b 的 Gaussian 对称互换。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-OSCILLATION-P-ODD · 振荡分拆闭式：P-ODD

$$
P_{k,i}(a,b;2\mu-1;q)=q^{(2\mu-1)((2k+1)\mu-i)}\begin{bmatrix}a+b\\a-(2k+1)\mu+i\end{bmatrix}_{q}.
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AP-9.3.12`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：对矩形 a×b 内的分拆 λ，r_j=λ_j−λ′_j（1≤j≤Durfee长度）。正振荡从 r>2k−i−1 开始，随后 r≤−(i−1)，再交替；负振荡从后一不等式开始。取满足交替条件的递增下标子序列最大长度。P/M 分别按 q^{|λ|} 计正/负振荡长度至少指定阈值的分拆；含空分拆。

定义文件：[ANDREWS_P_supplement.md](../../round1_source_collection/records/ANDREWS_P_supplement.md)；[ANDREWS_P.md](../../round1_source_collection/books/ANDREWS_P.md)。

- **AP-9.3.12**（p.149, Theorem 9.9, (9.3.12)）：a,b≥0，b=a 或 a−1；k≥i≥1；μ≥1；均为整数。
  对应：代表式；保留本条来源域。
- **AP-9.3.16**（p.149, (9.3.16); (9.3.26)–(9.3.27), p.152）：a,b≥0，k≥i≥1，μ≥1，a−b≤2k−i；均为整数。
  对应：同一闭式；保留两个来源域的析取，不取条件交集或笛卡尔积。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AP-9.3.5 · 振荡分拆的M混合差分递推

$$
M_{k,i}(a,b;\mu;q)-M_{k,i}(a-1,b;\mu;q)-M_{k,i}(a,b-1;\mu;q)+M_{k,i}(a-1,b-1;\mu;q)=q^{a+b-1}\begin{cases}M_{k,i}(a-1,b-1;\mu;q),&a-b>-(i-1),\\P_{k,i}(a-1,b-1;\mu-1;q),&a-b\le-(i-1).\end{cases}
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`AP-9.3.5`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：对矩形 a×b 内的分拆 λ，r_j=λ_j−λ′_j（1≤j≤Durfee长度）。正振荡从 r>2k−i−1 开始，随后 r≤−(i−1)，再交替；负振荡从后一不等式开始。取满足交替条件的递增下标子序列最大长度。P/M 分别按 q^{|λ|} 计正/负振荡长度至少指定阈值的分拆；含空分拆。

定义文件：[ANDREWS_P_supplement.md](../../round1_source_collection/records/ANDREWS_P_supplement.md)；[ANDREWS_P.md](../../round1_source_collection/books/ANDREWS_P.md)。

- **AP-9.3.5**（p.145, (9.3.5)）：a,b≥1，μ≥1，k≥i≥1；均为整数。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AP-9.3.6 · 振荡分拆的P混合差分递推

$$
P_{k,i}(a,b;\mu;q)-P_{k,i}(a-1,b;\mu;q)-P_{k,i}(a,b-1;\mu;q)+P_{k,i}(a-1,b-1;\mu;q)=q^{a+b-1}\begin{cases}M_{k,i}(a-1,b-1;\mu-1;q),&a-b>2k-i-1,\\P_{k,i}(a-1,b-1;\mu;q),&a-b\le2k-i-1.\end{cases}
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`AP-9.3.6`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：对矩形 a×b 内的分拆 λ，r_j=λ_j−λ′_j（1≤j≤Durfee长度）。正振荡从 r>2k−i−1 开始，随后 r≤−(i−1)，再交替；负振荡从后一不等式开始。取满足交替条件的递增下标子序列最大长度。P/M 分别按 q^{|λ|} 计正/负振荡长度至少指定阈值的分拆；含空分拆。

定义文件：[ANDREWS_P_supplement.md](../../round1_source_collection/records/ANDREWS_P_supplement.md)；[ANDREWS_P.md](../../round1_source_collection/books/ANDREWS_P.md)。

- **AP-9.3.6**（p.146, (9.3.6)）：a,b≥1，μ≥1，k≥i≥1；均为整数。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AP-9.3.7 · 振荡阈值为零的初值

$$
P_{k,i}(a,b;0;q)=M_{k,i}(a,b;0;q)=\begin{bmatrix}a+b\\a\end{bmatrix}_{q}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`AP-9.3.7`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：对矩形 a×b 内的分拆 λ，r_j=λ_j−λ′_j（1≤j≤Durfee长度）。正振荡从 r>2k−i−1 开始，随后 r≤−(i−1)，再交替；负振荡从后一不等式开始。取满足交替条件的递增下标子序列最大长度。P/M 分别按 q^{|λ|} 计正/负振荡长度至少指定阈值的分拆；含空分拆。

定义文件：[ANDREWS_P_supplement.md](../../round1_source_collection/records/ANDREWS_P_supplement.md)；[ANDREWS_P.md](../../round1_source_collection/books/ANDREWS_P.md)。

- **AP-9.3.7**（p.146, Lemma 9.6, (9.3.7)）：a,b≥0，k≥i≥1；均为整数。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AP-9.3.8 · 空矩形的振荡初值

$$
P_{k,i}(0,b;\mu;q)=P_{k,i}(a,0;\mu;q)=M_{k,i}(0,b;\mu;q)=M_{k,i}(a,0;\mu;q)=0.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`AP-9.3.8`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：对矩形 a×b 内的分拆 λ，r_j=λ_j−λ′_j（1≤j≤Durfee长度）。正振荡从 r>2k−i−1 开始，随后 r≤−(i−1)，再交替；负振荡从后一不等式开始。取满足交替条件的递增下标子序列最大长度。P/M 分别按 q^{|λ|} 计正/负振荡长度至少指定阈值的分拆；含空分拆。

定义文件：[ANDREWS_P_supplement.md](../../round1_source_collection/records/ANDREWS_P_supplement.md)；[ANDREWS_P.md](../../round1_source_collection/books/ANDREWS_P.md)。

- **AP-9.3.8**（p.146, Lemma 9.6, (9.3.8)）：a,b≥0，μ≥1，k≥i≥1；均为整数。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AP-9.L7 · Gaussian 混合差分引理

$$
q^L\left(\begin{bmatrix}A+B\\B-X\end{bmatrix}_{q}-\begin{bmatrix}A+B-1\\B-X\end{bmatrix}_{q}-\begin{bmatrix}A+B-1\\B-X-1\end{bmatrix}_{q}+\begin{bmatrix}A+B-2\\B-X-1\end{bmatrix}_{q}\right)=q^{L+A+B-1}\begin{bmatrix}A+B-2\\B-X-1\end{bmatrix}_{q}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`AP-9.L7`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

定义文件：[ANDREWS_P_supplement.md](../../round1_source_collection/records/ANDREWS_P_supplement.md)；[ANDREWS_P.md](../../round1_source_collection/books/ANDREWS_P.md)。

- **AP-9.L7**（p.146, Lemma 9.7（证明续 p.147））：A,B,X,L 为整数，A+B≥2；q 可逆，Gaussian 下指标越界为零。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AP-9.L8 · 分拆筛辅助有限和的递推

$$
f(A,r;X,Y,L)-f(A,r-1;X,Y,L)-f(A-1,r+1;X,Y,L)+f(A-1,r;X,Y,L)=q^{L+2A+2Y+r}\begin{bmatrix}2A+X+r-2\\A+Y\end{bmatrix}_{q}.
$$

类型：rewrite_rule；范围：finite_q。

代表式记号上下文：`AP-9.L8`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：\(f(A,r;X,Y,L)=F(2A+X,A+Y+1,r,L)\)，其中 \(F(T,D,R,E)=q^E[R+1]_{q^D}{T\brack D-1}_q+\sum_{j=0}^{R-2}q^{E+D+j+1}[R-j-1]_{q^D}{T+j\brack D-2}_q\)，\([s]_z=\sum_{h=0}^{s-1}z^h\)（s≥0）；空和为0。

定义文件：[ANDREWS_P_supplement.md](../../round1_source_collection/records/ANDREWS_P_supplement.md)；[ANDREWS_P.md](../../round1_source_collection/books/ANDREWS_P.md)。

- **AP-9.L8**（p.147, Lemma 9.8）：r≥1，A,X,Y,L 为整数，2A+X≥2；q 可逆。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AP-9.3.17 · M振荡闭式的剩余参数域

$$
M_{k,i}(a-1,a+i-1+r;2\mu;q)=F(2a+i-3,a+i-1-(2k+1)\mu,r+1,\mu((4k+2)\mu+2k-2i+1)).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AP-9.3.17`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：对矩形 a×b 内的分拆 λ，r_j=λ_j−λ′_j（1≤j≤Durfee长度）。正振荡从 r>2k−i−1 开始，随后 r≤−(i−1)，再交替；负振荡从后一不等式开始。取满足交替条件的递增下标子序列最大长度。P/M 分别按 q^{|λ|} 计正/负振荡长度至少指定阈值的分拆；含空分拆。 \(f(A,r;X,Y,L)=F(2A+X,A+Y+1,r,L)\)，其中 \(F(T,D,R,E)=q^E[R+1]_{q^D}{T\brack D-1}_q+\sum_{j=0}^{R-2}q^{E+D+j+1}[R-j-1]_{q^D}{T+j\brack D-2}_q\)，\([s]_z=\sum_{h=0}^{s-1}z^h\)（s≥0）；空和为0。

定义文件：[ANDREWS_P_supplement.md](../../round1_source_collection/records/ANDREWS_P_supplement.md)；[ANDREWS_P.md](../../round1_source_collection/books/ANDREWS_P.md)。

- **AP-9.3.17**（p.150, (9.3.17); (9.3.26)–(9.3.27), p.152）：a≥1，r≥−1；k≥i≥1，μ≥1；均为整数；q 可逆。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AP-9.3.18 · M振荡闭式的剩余参数域

$$
M_{k,i}(a-1,a+i-1+r;2\mu-1;q)=F(2a+i-3,a-(2k+1)\mu+2k,r+1,(2\mu-1)((2k+1)\mu-2k+i-1)).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AP-9.3.18`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：对矩形 a×b 内的分拆 λ，r_j=λ_j−λ′_j（1≤j≤Durfee长度）。正振荡从 r>2k−i−1 开始，随后 r≤−(i−1)，再交替；负振荡从后一不等式开始。取满足交替条件的递增下标子序列最大长度。P/M 分别按 q^{|λ|} 计正/负振荡长度至少指定阈值的分拆；含空分拆。 \(f(A,r;X,Y,L)=F(2A+X,A+Y+1,r,L)\)，其中 \(F(T,D,R,E)=q^E[R+1]_{q^D}{T\brack D-1}_q+\sum_{j=0}^{R-2}q^{E+D+j+1}[R-j-1]_{q^D}{T+j\brack D-2}_q\)，\([s]_z=\sum_{h=0}^{s-1}z^h\)（s≥0）；空和为0。

定义文件：[ANDREWS_P_supplement.md](../../round1_source_collection/records/ANDREWS_P_supplement.md)；[ANDREWS_P.md](../../round1_source_collection/books/ANDREWS_P.md)。

- **AP-9.3.18**（p.150, (9.3.18); (9.3.26)–(9.3.27), p.152）：a≥1，r≥−1；k≥i≥1，μ≥1；均为整数；q 可逆。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AP-9.3.19 · P振荡闭式的剩余参数域

$$
P_{k,i}(b+2k-i-1+r,b-1;2\mu;q)=F(2b+2k-i-2,b+2k-i-(2k+1)\mu,r,\mu((4k+2)\mu-2k+2i-1)).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AP-9.3.19`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：对矩形 a×b 内的分拆 λ，r_j=λ_j−λ′_j（1≤j≤Durfee长度）。正振荡从 r>2k−i−1 开始，随后 r≤−(i−1)，再交替；负振荡从后一不等式开始。取满足交替条件的递增下标子序列最大长度。P/M 分别按 q^{|λ|} 计正/负振荡长度至少指定阈值的分拆；含空分拆。 \(f(A,r;X,Y,L)=F(2A+X,A+Y+1,r,L)\)，其中 \(F(T,D,R,E)=q^E[R+1]_{q^D}{T\brack D-1}_q+\sum_{j=0}^{R-2}q^{E+D+j+1}[R-j-1]_{q^D}{T+j\brack D-2}_q\)，\([s]_z=\sum_{h=0}^{s-1}z^h\)（s≥0）；空和为0。

定义文件：[ANDREWS_P_supplement.md](../../round1_source_collection/records/ANDREWS_P_supplement.md)；[ANDREWS_P.md](../../round1_source_collection/books/ANDREWS_P.md)。

- **AP-9.3.19**（p.150, (9.3.19); (9.3.26)–(9.3.27), p.152）：b≥1，r≥0；k≥i≥1，μ≥1；均为整数；q 可逆。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。

## FQI-SRC-AP-9.3.20 · P振荡闭式的剩余参数域

$$
P_{k,i}(b+2k-i-1+r,b-1;2\mu-1;q)=F(2b+2k-i-2,b+2k-(2k+1)\mu,r,(2\mu-1)((2k+1)\mu-i)).
$$

类型：identity；范围：finite_q。

代表式记号上下文：`AP-9.3.20`。

**证明算法状态：本次未匹配到旧算法**。 [核对依据](../PROOF_ALGORITHMS.md)

局部定义：对矩形 a×b 内的分拆 λ，r_j=λ_j−λ′_j（1≤j≤Durfee长度）。正振荡从 r>2k−i−1 开始，随后 r≤−(i−1)，再交替；负振荡从后一不等式开始。取满足交替条件的递增下标子序列最大长度。P/M 分别按 q^{|λ|} 计正/负振荡长度至少指定阈值的分拆；含空分拆。 \(f(A,r;X,Y,L)=F(2A+X,A+Y+1,r,L)\)，其中 \(F(T,D,R,E)=q^E[R+1]_{q^D}{T\brack D-1}_q+\sum_{j=0}^{R-2}q^{E+D+j+1}[R-j-1]_{q^D}{T+j\brack D-2}_q\)，\([s]_z=\sum_{h=0}^{s-1}z^h\)（s≥0）；空和为0。

定义文件：[ANDREWS_P_supplement.md](../../round1_source_collection/records/ANDREWS_P_supplement.md)；[ANDREWS_P.md](../../round1_source_collection/books/ANDREWS_P.md)。

- **AP-9.3.20**（p.151, (9.3.20); (9.3.26)–(9.3.27), p.152）：b≥1，r≥0；k≥i≥1，μ≥1；均为整数；q 可逆。
  对应：独立保留；未据名称或家族推断等价。

来源完整公式、修订及验证出处见 [normalized_sources.json](../data/normalized_sources.json)。
