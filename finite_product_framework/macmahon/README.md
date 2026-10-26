# MacMahon 分拆分析与有理 Ω 消元

**后续输入适配已接通**：`adapter.py` 将固定维数的有限 range/Icc、嵌套线性区间和指数线性权重编码为有理 Ω 请求。符号上界保留为系数指标，临时正权重标记在消元后依据有限纤维去除。实际接通 2 道 Train 中的 4 个求和子表达式；不是完整原题证明。范围、79 项验收与拒绝边界见 [当前说明](RATIONAL_OMEGA.md) 及 [适配报告](../generated/omega_adapter_20261014/validation.json)。符号维数分拆等仍不能直接输入这一固定维数核心。

**当前核心升级（2026-10-14）**：已新增 `solve_core.py --input ...` 的 `rational_omega`，从正权重 Elliott 有理生成函数自动构造多辅助变量的非负部／常数项消元。使用分组部分分式与精确模逆，支持重因子、非互素指数和混合约束。输入、推导、示例与边界见 [RATIONAL_OMEGA.md](RATIONAL_OMEGA.md)，验收见 [validation.json](../generated/omega_core_20261014/validation.json)。本轮只接入核心接口；下文的旧原题入口及 Lean 规则未改，未运行 Train/Test/Lean。下文“一般有理消元尚未实现”属于旧版范围，现由上述契约取代；任意迭代 Laurent 展开、CTEuclid 高性能实现、符号维数和任意原对象自动编码依旧不在本轮范围。

## 旧原题流程与既有证明

完整中文推导与代码对应关系见 [MacMahon证明流程说明](MacMahon证明流程说明.md)。

独立入口：`python3 prove_macmahon.py --identity FQI-RECTANGLE-PARTITIONS`。
后端：`finite_omega_elimination`；当前类内包含有限Omega和链式几何生成函数两个计划。
按实际表达式选计划，不按题号路由，不跨方法回退。

## 原题结果

`FQI-RECTANGLE-PARTITIONS` 已在原声明上证明：任意域K、任意q，以及k≤n，
`gaussian q n k = rectangleWeight q (n-k) k`。
运行产物：`generated/macmahon/12f36842274642ddb30f09af60f908cd/`。
没有增加q≠0、q非单位根、特征零或分母非零假设；不是固定尺寸枚举。
原题公理审计仅为propext、Classical.choice、Quot.sound，无sorryAx。

此前首版只完成表示桥接，原题未解决；本次新增完整的链约束消元与生成函数求值，取代该限制。

## 从约束到求值

令R(a,b)为原始矩形分拆加权和，F_b(t)=∑a≥0 R(a,b)t^a。
这里使用Lean的形式幂级数PowerSeries，t是独立形式变量，无数值收敛要求。

1. `rectangle_omega`：原对象与多辅助变量Omega编码相等，涵盖任意宽高。
2. `headEquiv`：将链分解为最大部件r和剩余链，双向映射、边界及权重均证明。
3. `rectangle_head_elimination`：得到R(a,b+1)=∑r≤a q^r R(r,b)。这是逐层消去有序链约束的通用规则。
4. `rectangle_series_step`：有限系数卷积推出F_(b+1)(t)=F_b(qt)/(1-t)，其中1/(1-t)由系数全为1的形式几何级数定义，不做标量除法。
5. `rectangle_series_factorization`：归纳消元得到F_b(t)=∏i=0..b geometric(q^i)，即∏i=0..b (1-q^i t)^(-1)。
6. `gaussian_series_factorization`：从冻结Gaussian定义及共享局部Pascal规则验证同一个生成函数的Gaussian系数。该步骤在本类内部完成，不调用递推/系数pipeline。
7. `omega_rectangle_evaluation`：比较两边同一形式幂级数的第a项系数，回到Omega与原对象，最后核验n-k+k=n的原始指标条件。

`geometric_denominator`和`cone_denominator`另外给出精确有理表示证书：
`coneProduct q b * ∏i≤b (1-C(q^i)*X) = 1`。每个分母形式级数的常数项是1；原题证明通过共同几何乘积比较系数，无须给q添加一般位置条件。

这些是已证明的符号参数消元模板。后端识别受支持的链/Omega表达式并实例化、重建证书；不是自动发现任意锥分解或任意消元规则的系统。

## 保留的有限Omega能力

在真正的AddMonoidAlgebra R ℤ上定义加法同态omegaGE，保留非负指数再令辅助变量为1；omegaAll筛选一族指数。先卷积后投影，绝不把Omega当作乘法同态。

支持任意有限点集的加权编码、两因子带符号仿射约束、任意符号上界的单位三角约束、显式有限因子展开、嵌套辅助投影。有限部分允许任意交换半环、零权重及负指数。

符号计算在Lean内进行：形式级数系数运算、通用有限重编号、整数条件和精确环规范化。没有外部CAS。Lean的omega tactic是整数算术工具，不是MacMahon Omega算子。

## 信任边界及限制

独立编译冻结Definitions及抽出的rectangle/rectangleWeight定义。Gaussian依赖只抽取零值、对角与越界引理，再编译共享`p1/lean/GaussianRules.lean`的局部多项式关系；不导入Benchmark目标证明，也不调用其他类后端。实际源、依赖、证明与证书均有哈希和公理审计。

尚未实现一般Elliott/CTEuclid有理Omega、任意线性Diophantine系统、迭代Laurent级数展开域、Barvinok/Polyhedral Omega或任意组合对象自动编码。支持符号维数的有序链专用规则，不等于通用符号维数消元。资源与搜索失败仍返回未解决。

## 验证

运行`python3 macmahon/check.py`，证据见`generated/macmahon_validation.json`。
本次专项21项符合预期：15个完整模块证明、6个错误目标拒绝，另有证书篡改拒绝；模块证明与Train覆盖分别记录。新增测试覆盖生成函数因子化、有理分母证书、原题变量改名/反向、q=0和q=1，以及缺少k≤n、错误权重和漏因子的拒绝。
统一审计入口为`python3 check.py --audit-existing`；历史成功产物审计不等于全部重跑。

全目录构建/验证此前分别缺`pending16_resolutions.json`与`validate_sills`；本次日志见`generated/macmahon_chain_project_checks.json`。

文献背景：[Xin的CTEuclid](https://arxiv.org/abs/1208.6074)、[Polyhedral Omega](https://arxiv.org/abs/1501.07773)。本实现采用有限投影及链式形式生成函数规则，不宣称移植了这两篇论文的通用算法。
