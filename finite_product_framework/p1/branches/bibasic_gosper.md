# 双基 Gosper：P1 内部的原差分分支

本分支与 q-WZ、直接单基 q-Gosper、一般 q-Zeilberger 共用 P1 的输入、证明组装及审计入口。范围仍是原 120 条主机制候选；双基首选的 3 条仅是候选，不表示全部完成。

## 构造与验证

`bibasic.py` 只接受求和项及来源元数据，不接受目标、预设证书或候选分母。对两个独立形式底数置 X=p^k、Y=q^k，令 σ(X,Y)=(pX,qY)。从原项推导后向项比 r，按不可约因子的移位轨道构造

\[
r=\frac{P}{\sigma^{-1}(P)}\frac{A}{B},\qquad
\sigma(A)f-B\sigma^{-1}(f)=P.
\]

因子支撑及系数比决定确切移位，不枚举有界移位半径。坐标单项式视为 Laurent 单位；分别比较 X、Y 方向的首尾次数，并分析首尾项抵消时的共振，导出 Laurent 指数矩形。精确线性代数求 f，然后恢复 R=Bσ⁻¹(f)/P，独立复核 Uσ(R)−R=1，其中 U=σ(F)/F。

算法依据 [Riese 的双基 Gosper 原始论文](https://www.risc.jku.at/publications/download/risc_210/bibasic.pdf) 的移位正规形及系数比较机制；本项目以 Laurent 矩形实现坐标极点处理。未安装外部求和软件，未形式化构造算法本身。每个输出仍需在 Lean 原定义上重新验证。

`bibasic_pipeline.py` 从原 Lean Expr 展开显式 Pochhammer 列表，识别两底数及 n 无关的求和项。求出证书之后，计算包含当前项的原差分 H(k)=F(k)U(k)σ(R)(k)，尝试将其写成移位起点的 Pochhammer 乘积。这个有限枚举仅用于 Lean 表示转换，不是证书搜索。表示转换不读取右端。

共享引理 `sum_inclusive_antidifference` 从 F(0)=H(0) 和区间内 F(k+1)=H(k+1)−H(k) 得到 Σ₀ⁿF=H(n)。生成器从实际原假设提取所需非零条件，利用无除法的 `poch_head`、`poch_succ` 验证局部关系，最后比较 H(n) 与原目标并审核公理。这样不要求 n+1 处的分母有定义。

## 首例与原参数域

首个验收目标是 `FQI-SRC-GR2-II-34`。符号证书有 c−1 分母，但原题允许 c=1。自动移位乘积回译消除了该形式极点：Lean 仅使用原题的 c≠0、1−a≠0 及实际有限区间分母条件。没有添加 c≠1，也没有借助原恒等式专用证明。

```bash
# 在 finite_product_framework/p1 中运行
python3 run.py --identity FQI-SRC-GR2-II-34
python3 run.py --identity FQI-SRC-GR2-II-34 --branch bibasic_gosper
python3 test_bibasic.py
python3 check.py
```

[原题运行报告](../generated/runs/FQI-SRC-GR2-II-34/report.json)、[生成证明](../generated/runs/FQI-SRC-GR2-II-34/Proof.lean)、[分支回归](../generated/bibasic_tests.json)、[统一验收](../validation.json)。原题成功只能由报告中的 `proved` 与原声明公理审计确认。

## 当前边界

- 符号层：两个独立形式底数上的有理项比，精确参数系数域。超时和未知数预算属于资源限制；`no_solution_in_derived_laurent_system` 只报告本构造系统无解，不声明原恒等式不可证。
- Lean 出口：range(n+1)，与 n 无关的项，显式 Pochhammer 乘积、整次幂及几何权重；当前支持分子起点前移 0/1 后系数为常数参数多项式的原差分表示。最多 8 个分子原子是表示搜索预算。
- 尚未接通：任意多基、相关底数、依赖 n 的双基递推搜索、更一般有理原差分回译、双基变换两侧比较。表示失败和原域失败必须保留为未完成，不计新增证明。

回归独立验证不同已知原差分的计算残差、混合因子与大移位、负 Laurent 次数和预算状态，并用改名原声明、错误右端、缺失原域条件、证书篡改检验端到端接受与拒绝。合成变体不计训练覆盖。
