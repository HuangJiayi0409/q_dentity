# 多重 q 创造性望远镜：多维内核与二维端到端验收

本分支属于 P1「差分、望远镜与递推证明」的 120 条结构候选范围。首个原生二维验收对象 `FQI-SRC-GR2-10.Ex18` 已通过原声明的 Lean 完整证明与公理审计，本分支新增 1 条，P1 累计 12 条。覆盖数量以原声明通过 Lean 和公理审计为准，合成二维/三维实验不计入 train 证明数。

## 算法与输入

从实际 Lean Expr 提取嵌套有限和、求和域、参数假设和右端。符号内核接受任意有限指标列表 `i0,...,i(d-1)`，由原始项自动推导外参数与各求和方向的移位比，联合搜索

```
sum_r c_r(Q) F(n+r,k) = sum_i Delta_i (R_i F)(n,k).
```

搜索器不接受目标、预设递推或预设证书。公共分母来自移位比；分子按总次数枚举，允许指定 Laurent 下界。当前是有界向量有理证书搜索，不保证搜索完备，也不是 qMultiSum 软件的完整复刻。

线性系统先作单项和两项精确消元，再使用 python-flint 做逐行取本原部分的无分式消元。模素数探测只用于筛选独立行或证明当前空间列满秩；最终解在所有原始符号方程中复核，再独立验证有理残差。特化退化和预算耗尽均不表示恒等式不可证明。

## 原题证明出口

当前原生 Lean 编译器闭合二维三角域、一阶外参数递推、单基 Pochhammer 乘积的受限语法：长度为 `j`、`k`、`j+k`，外参数在乘积起点按一步 q 移位，域假设提供所需有限乘积分母非零条件。所有项、递推和通量表达式由输入与本次证书生成；生产代码没有题号判断或原题证书查表。

1. 将证书改写为 `G_i = F(n+1) * (R_i / V)`，其中 `V=F(n+1)/F(n)`，避免把旧核在斜边上的极点当作零边界。
2. 用 Pochhammer 前缀与起点移位引理，从原题在 `n+1` 的有限域假设推出归纳所需的 `n` 域，不增加全局参数假设。
3. 在 Lean 中验证乘积局部差分，分别处理两个坐标轴、上边界内部及端点，并抵消移动支撑新增壳层。
4. 对证书参数极点单独处理特化。首例的 `a=c` 由 `(1;q)_m` 消失规则闭合，原题允许的参数值全部保留。
5. 验证目标递推与初值，生成冻结原声明的证明，并审计公理。只有最终成功才报告 `proved`。

`MultisumRules.lean` 中的有限域离散散度规则适用于任意有限维数；新增三角求和、边界重排、移动壳层及递推规则完成二维实例化。`MultisumProductRules.lean` 提供通用乘积域引理。高维原题的自动 Lean 出口仍需扩展，不能把三维合成证书视为三维原题已证明。

## 运行

安装可选精确计算后端，再在 P1 目录执行：

```bash
python3 -m pip install -r requirements-multisum.txt
python3 run.py --identity FQI-SRC-GR2-10.Ex18 --branch multisum --seconds 500 --max-order 1 --max-degree 5 --laurent-floor -1
python3 test_multisum.py
python3 test_multisum_native.py
```

当前工作区已准备 `/home/hjy/Project/.venv-finiteq-multisum/bin/python`，可直接代替上述 `python3`。符号构造和 Lean 验证分别有资源限制；超时如实报告，不降级为预设证明。

## 验收证据

- [原题报告](../generated/runs/FQI-SRC-GR2-10.Ex18/report.json)：实时构造、原声明证明、哈希与公理依赖。
- [原题 Lean 证明](../generated/runs/FQI-SRC-GR2-10.Ex18/Proof.lean)。
- [符号与边界回归](../generated/multisum_tests.json)：包括二维/三维搜索、精确消元、退化特化、篡改拒绝、角点和壳层。
- [原生变体回归](../generated/multisum_native_tests.json)：改名、整体缩放、错误初值及证书/域拒绝。变体复用本次运行生成的证书并独立核验，不计新增 train 证明。

历史探索报告保留当时的失败和预算信息；当前状态以上述验收证据及其代码哈希为准。
