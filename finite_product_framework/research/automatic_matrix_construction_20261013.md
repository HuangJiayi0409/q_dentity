# 三条符号证明流程的自动构造改造

日期：2026-10-13。本次用户要求把依赖现成证书的分支改为自动构造。只使用独立合成用例验证，不运行 Train、不读取 Test；本文不报告 Train 覆盖率。

## 为什么此前会依赖现成证书

旧实现先建立了核恒等式、谱正交和行列式分解的 Lean 验证/组装定理，但一般分支通过上下文中的逆核关系、自伴/本征关系或 LU 分解假设来完成证明。验证定理是正确的，然而缺少从原式产生这些关系的算法，因此不能把它当作完整的自动证书构造器。

此次保留数学验证定理，为三个独立入口补上构造器，并撤下生产入口中仅回放这些假设的计划。原题的参数域假设仍然用于消除分母等必要义务。

## 当前构造流程

|方法|实际构造算法|Lean 如何证明原题|
|---|---|---|
|核反演/复合|从 A 精确计算 A⁻¹；复合从 A、B 计算 A B。目标里的候选逆核/复合核不用于求解|验证计算矩阵的核关系，证明它与原目标中的核相等，再组装任意向量上的作用|
|谱正交|对未知 A 求解 A f=0、A g=g、diag(w) A=Aᵀ diag(w) 的精确线性系统；自由算子未知量取零|验证构造出的加权自伴算子、本征关系及 0≠1，再推出原配对为零|
|行列式|从 A 计算置换矩阵 P、L、U，并独立计算 Berkowitz 行列式值|验证 P A=L U 及各行列式，再比较原目标；若无法证明参数主元分母非零，尝试无主元除法的值并通过余子式展开重建|

谱构造只搜索上述分离算子：即使某个配对为零，也不保证存在或能在原域内表示这种算子。它不是整族正交多项式的算子发现或范数算法。

共同执行路径：原 Lean 表达式 → 精确矩阵导出 → 方法自身的 SymPy 构造 → 候选证书及证明脚本 → Lean 验证未修改的原声明 → 公理与来源哈希检查 → 接受成功。CAS 结果本身不是证明。任何桥接、分母或终点义务未闭合，都不能记为成功。

## 范围及尚未完成的能力

- 自动矩阵导出限于 `Fin n`，其中 n 是 1–5 的具体整数；矩阵系数允许符号参数，因此不是参数数值采样。
- 支持精确标量代数表达式；其他标量表达式可作为独立原子处理，不自动推导它们的额外关系。
- 不添加一般位置或主元非零假设；原题没有的假设不能通过 CAS 偷渡。
- 尚未支持任意符号阶数的逆核闭式、q-Hahn/q-Racah 差分算子、整族范数或组合对象到行列式的一般自动桥接。
- 核的三角支撑转置和行列式的结构求值仍作为类内计算计划保留。谱入口没有纯上下文证书回放后备分支。三个入口不跨类调用求解器。
- 一次失败只说明当前表示、算法和预算未能证明，不能据此断言该数学方法不可能证明该公式。

## 验证与复现

当前结果：38 个合成用例全部符合预期，19 个完整证明（16 个自动构造证书、3 个保留的结构计算计划），19 个按预期未证明。逆核、谱算子、L 因子三种错误见证均被 Lean 拒绝；核反演及行列式另通过目标候选独立性检查。所有成功证据通过当前依赖哈希和原声明一致性检查。这些数字不是 Train 覆盖率。

在 `finite_product_framework` 目录依次运行：

```bash
python3 kernel_transform/check.py
python3 spectral/check.py
python3 determinant/check.py
python3 workflow/check_matrix_construction.py
```

这些脚本只构造合成声明。每条方法包含正确原题、错误目标或缺失条件的拒绝检查，并检查接受证书的哈希绑定。部分用例强制要求 `certificate_origin = computed_witness` 和指定构造计划，不能用已有模板成功冒充自动构造。最后一个脚本审计当前依赖和成功证明，并把逆矩阵、谱算子、L 因子分别改成零，实际重新编译以确认错误见证被拒绝。

汇总报告：[matrix_construction_validation.json](../generated/matrix_construction_validation.json)。分项报告：[核](../generated/kernel_transform_validation.json)、[谱](../generated/spectral_validation.json)、[行列式](../generated/determinant_validation.json)。旧 `method_pipelines_validation.json` 和静态源码审核记录属于修改前状态，不能作为修改后 Train 覆盖证据。

## 代码入口

- [矩阵表达式导出](../workflow/MatrixExport.lean)、[精确标量接口](../workflow/matrix_symbolic.py)、[构造与原题重建运输层](../workflow/matrix_synthesis.py)。
- [核构造器](../kernel_transform/construct.py)、[谱构造器](../spectral/construct.py)、[行列式构造器](../determinant/construct.py)。

产物中 `synthesis_input.json` 保存导出的输入，`construction.json` 保存候选及数学构造，`Synthesized*.lean` 保存尝试，只有完整通过的原题才产生被接受的 `Proof.lean` 和 `certificate.json`。这允许分别统计“成功构造”和“成功证明原题”。
