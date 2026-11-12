# 最终统一源码：递推精确声明、五轮轨迹与原题审计

以下来自 final_validation_01 的全新实际运行，绑定最终冻结源码。较早 A/B 阶段轨迹仍在 AB_EXACT_EVIDENCE.md 单独保留。

## 原始完整声明

- identity：`FQI-GAUSS-ALTERNATING`
- theorem：`FiniteQBenchmark.Identity009.statement`
- SHA-256：`c49f5a4417e3d4d19df4463a377c4d3117cea07619d1867156eccb454ca8123c`

下方是冻结的原题输入声明，原输入中的 `sorry` 仅标记待证题；实际验收证明从证书树另外构造并编译。

```lean
import Benchmark.Representation

open scoped BigOperators
open FiniteQBenchmark
set_option autoImplicit false
set_option linter.unusedVariables false

/- FQI-GAUSS-ALTERNATING — Gauss 交错 Gaussian 奇偶求值
Original representative source: AP-3.3.8
Frozen statement: formulas/train/FQI-GAUSS-ALTERNATING.md
Source formula:
\sum_{j=0}^m(-1)^j\begin{bmatrix}m\\j\end{bmatrix}_{q}=\begin{cases}(q;q^2)_{m/2},&m\text{ even},\\0,&m\text{ odd}.\end{cases}
Only this target theorem's proof is deferred. Shared auxiliary results are proved.
-/
namespace FiniteQBenchmark.Identity009
variable {K : Type*} [Field K]

theorem statement (q : K) (m : ℕ) :
 (∑ j ∈ Finset.range (m+1), (-1)^j*gaussian q m j) =
 if m%2 = 0 then poch q (q^2) (m/2) else 0 := by
  sorry

end FiniteQBenchmark.Identity009
```

## 五轮实际顺序与精确命题

实际动作顺序为局部递推 → 唯一性连接 → 初值 1 → 初值 0 → 右端递推。连接获验后才建立后三个义务；初值与右端的执行顺序由当时合法候选选择决定。

### 第 1 轮：local

候选 `recurrence-local-3026508a6dc7cb8598c724e0`；动作 `route-d3f7090a72469c0bc7d9c433`；依赖 `无`。

```lean
∀ {K : Type u} [Field K] (q : K) (m : ℕ), (∑ j ∈ Finset.range ((m + 2) + 1), (((-1) ^ j) * (FiniteQBenchmark.gaussian q (m + 2) j))) + (((-1) + ((q^m) * q)) * (∑ j ∈ Finset.range (m + 1), (((-1) ^ j) * (FiniteQBenchmark.gaussian q m j))) + (0) * (∑ j ∈ Finset.range ((m + 1) + 1), (((-1) ^ j) * (FiniteQBenchmark.gaussian q (m + 1) j)))) = 0
```

### 第 2 轮：uniqueness_bridge

候选 `recurrence-uniqueness-bridge-338af80c4b8b821e85c425b4`；动作 `route-fe6de1bf1377aefb5fef8cde`；依赖 `recurrence-local-3026508a6dc7cb8598c724e0`。

```lean
(∀ {K : Type u} [Field K] (q : K) (m : ℕ), (if (((m + 2) % 2) = 0) then (FiniteQBenchmark.poch q (q ^ 2) ((m + 2) / 2)) else 0) + (((-1) + ((q^m) * q)) * (if ((m % 2) = 0) then (FiniteQBenchmark.poch q (q ^ 2) (m / 2)) else 0) + (0) * (if (((m + 1) % 2) = 0) then (FiniteQBenchmark.poch q (q ^ 2) ((m + 1) / 2)) else 0)) = 0) → (∀ {K : Type u} [Field K] (q : K) (m : ℕ), (∑ j ∈ Finset.range (0 + 1), (((-1) ^ j) * (FiniteQBenchmark.gaussian q 0 j))) = (if ((0 % 2) = 0) then (FiniteQBenchmark.poch q (q ^ 2) (0 / 2)) else 0)) → (∀ {K : Type u} [Field K] (q : K) (m : ℕ), (∑ j ∈ Finset.range (1 + 1), (((-1) ^ j) * (FiniteQBenchmark.gaussian q 1 j))) = (if ((1 % 2) = 0) then (FiniteQBenchmark.poch q (q ^ 2) (1 / 2)) else 0)) → (∀ {K : Type u} [Field K] (q : K) (m : ℕ), ((∑ j ∈ Finset.range (m + 1), (((-1) ^ j) * (FiniteQBenchmark.gaussian q m j))) = (if ((m % 2) = 0) then (FiniteQBenchmark.poch q (q ^ 2) (m / 2)) else 0)))
```

### 第 3 轮：initial_one

候选 `recurrence-initial-one-proof-454fa646d9021f2b7c302731`；动作 `route-8f3f366d80cce2ce1c06a5aa`；依赖 `无`。

```lean
∀ {K : Type u} [Field K] (q : K) (m : ℕ), (∑ j ∈ Finset.range (1 + 1), (((-1) ^ j) * (FiniteQBenchmark.gaussian q 1 j))) = (if ((1 % 2) = 0) then (FiniteQBenchmark.poch q (q ^ 2) (1 / 2)) else 0)
```

### 第 4 轮：initial_zero

候选 `recurrence-initial-zero-proof-d96c092440ad5058df64a241`；动作 `route-96eaf44702ce51ff620045da`；依赖 `无`。

```lean
∀ {K : Type u} [Field K] (q : K) (m : ℕ), (∑ j ∈ Finset.range (0 + 1), (((-1) ^ j) * (FiniteQBenchmark.gaussian q 0 j))) = (if ((0 % 2) = 0) then (FiniteQBenchmark.poch q (q ^ 2) (0 / 2)) else 0)
```

### 第 5 轮：rhs_recurrence

候选 `recurrence-rhs-recurrence-proof-ce2cd6df6cb0fd91b1f511ec`；动作 `route-f905e1991800472e323e706d`；依赖 `无`。

```lean
∀ {K : Type u} [Field K] (q : K) (m : ℕ), (if (((m + 2) % 2) = 0) then (FiniteQBenchmark.poch q (q ^ 2) ((m + 2) / 2)) else 0) + (((-1) + ((q^m) * q)) * (if ((m % 2) = 0) then (FiniteQBenchmark.poch q (q ^ 2) (m / 2)) else 0) + (0) * (if (((m + 1) % 2) = 0) then (FiniteQBenchmark.poch q (q ^ 2) ((m + 1) / 2)) else 0)) = 0
```

## C/O/links/r/预算轨迹

| 轮 | task | C 前→后 | O 前→后 | links 前→后 | r | 动作预算 | 秒预算前→后 | 实际动作秒 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | local | 0→1 | 1→1 | 0→0 | original | 5→4 | 4000.000000→3953.323230 | 46.676770 |
| 2 | uniqueness_bridge | 1→2 | 1→3 | 0→1 | original | 4→3 | 3909.102793→3863.223603 | 45.879190 |
| 3 | initial_one | 2→3 | 3→2 | 1→2 | original | 3→2 | 3773.847511→3730.232423 | 43.615088 |
| 4 | initial_zero | 3→4 | 2→1 | 2→3 | original | 2→1 | 3730.232423→3686.552220 | 43.680203 |
| 5 | rhs_recurrence | 4→5 | 1→0 | 3→4 | original | 1→0 | 3510.534683→3467.057082 | 43.477602 |

轮间差额包含真实恢复重验，因此上一轮结束秒数不一定等于下一轮动作前秒数。完整精度、义务命题和逐阶段预算见同目录 `final_ab_exact_evidence.json`。

## 数学关系

定义 S(m) 为原 Gaussian 交错和，R(m) 为原奇偶 Pochhammer 右端。局部与右端证书分别给出 X(m+2)+(q^(m+1)-1)X(m)=0；实际符号系数保留中间的零项，不改变原式。初值证书给 S(0)=R(0)=1 与 S(1)=R(1)=0。唯一性连接依赖已验 S 递推，对自然数作强归纳，由同一二阶关系和两个初值得到所有 m 的 S(m)=R(m)。

## 原 theorem 审计与负例

真实恢复候选检查 17 次，重复动作 0 次；独立原 theorem 编译 2 次。两次 theorem 均为 `FiniteQBenchmark.Identity009.statement`，公理均为 `propext, Classical.choice, Quot.sound`。

五类候选各一次实际错误 Lean 证明均被拒绝；唯一性错误连接在替换义务之前失败，前后状态相同。没有以局部 theorem 审计替代原题审计。

