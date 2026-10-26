# 有限 q 恒等式的十二条独立证明流程

2026-10-20 最新选择策略：保留 v1 的结构特征、评分规则与权重，十二方法全部未知且评分并列时明确返回 `unclassified`，不再把名称排序的第一项当作分类结果。默认只标记；`prove_auto.py --unknown-policy all` 可对此类输入共用一次预处理并尝试全部十二方法，默认4方法并行、每方法独立预算，成功后仍完成全部记录。其他输入保持首选单方法执行。分类状态与逐方法证明结果分别保存，详见 [选择器说明](selection/README.md)。

2026-10-20：新增 [AHP/TOPSIS 方法选择器](selection/README.md)。`select_method.py --identity ...` 核验预处理后只选择一个方法；`prove_auto.py --identity ...` 在同一总预算内进一步执行该方法并核验原题。十二方法保持独立，自动模式无跨方法回退；评分是结构优先度，不是证明成功概率。当前为第一版，不声明全量 Train 成功率提高。

当前入口整理（2026-10-19）：按用户要求删除另设的五核心原题流程 `prove_core.py`、`e2e/` 及其专属批测脚本 `batch/core_train.py`、`batch/proof_train.py`。项目继续使用十二方法入口及公共预处理；启用预处理仍需 `--preprocess`。递推/望远镜已复用的源表达式适配、Lean 生成工具和合成题模板迁至 `p1/source_ir.py`、`p1/sum_lean.py`、`p1/proof_fixture.py`。`p1` 中的符号算法和仅用于局部计算的 `solve_core.py` 保留，后者不是另一套原题证明流程。旧五核心结果与源码快照仅作历史归档，不再恢复该批测；删除及验证记录见 `generated/five_core_removal_20261019/`（相对框架目录）。

历史记录（已停止维护独立五核心流程）：2026-10-14 的局部核心 Train 批测已完成：24 进程、每题每系统 60 秒、346×5=1730 个状态单元；79 道实际调用核心，30 道产生至少一种局部构造。各系统局部构造为 q 求和 23、q-Ore 5、q-holonomic 10、差分域 1、MacMahon 2，存在重叠；不是原题证明数。本轮未运行 Lean、未读取 Test，旧 24 道原题证明基线未变。报告在 `finite_product_framework/generated/train_core5_20261014_24/report.html`（路径相对项目根），源码冻结及 1730 项结果核验通过。

最新：已补 MacMahon 符号上界有限求和适配器，26 项专项、9 项批测输入及 44 项 Ω 回归通过；2 道 Train 中 4 个求和子表达式接通，尚非原题证明。契约见 `macmahon/RATIONAL_OMEGA.md`，证据见 `generated/omega_adapter_20261014/validation.json`（路径相对框架目录）。该轮五核心评测入口已删除；上述记录仅说明当时的局部构造，旧证据保留。

**第五阶段 MacMahon 有理 Ω 核心（2026-10-14）**：统一 `solve_core.py` 新增 `rational_omega`，自动构造正权重 Elliott 有理函数的多变量非负部／常数项消元；采用按展开方向分组的精确部分分式，支持重因子、非互素指数和混合约束。见 [输入契约与算法](macmahon/RATIONAL_OMEGA.md)、[验收报告](generated/omega_core_20261014/validation.json)。这是原 MacMahon 流程的核心升级，原题前端及 Lean 规则未改，未跑 Train/Test/Lean。固定有限维数的适用范围不等于任意迭代 Laurent 域或符号维数求解；CTEuclid 仍是后续性能扩展。

每类方法各有一个完整证明入口。调用者选择大方法，该入口自动处理类内的结构识别、构造、闭合义务和 Lean 验证。十二条流程共享基础设施，运行时不跨方法探测或回退。

**第四阶段核心算法已闭合（2026-10-14）**：已补一般高阶 ΠΣ PLDE、代数数系数递归、一般可逆耦合系统，以及根式乘积依赖、常数参数和周期高阶下降。旧两个有已知证书的失败输入现均自动构造成功。完成范围是经检查的 ΠΣ* 塔及所声明的有限代数适配；任意代数函数常数域、不可归约输入塔和奇异系统仍不在范围内。见 [当前算法与边界](p1/DIFFERENCE_GENERAL.md)、[最新验收](generated/difference_general_20261014/validation.json)。未跑 Train/Test/Lean，原题证明数未变。

**第三轮历史记录**：周期加权方程、耦合ΠΣ系统、有限代数变量归约及多方向Σ扩张下降已接入；38项新增、195项既有回归和21个CLI验收通过。旧代数系数反例已解决，但任意代数系数乘积与一般不可拆分高阶系统仍未实现，`stage_complete=false`。见 [当前算法与具体缺口](p1/DIFFERENCE_COMPLETION.md) 和 [最新验收](generated/difference_completion_20261014/validation.json)。未跑Train/Test/Lean，未增加原题证明数。

**第二轮历史记录：一般差分域与有限差分环**：统一入口新增 `difference_field` 和 `finite_difference_ring`，完成受支持域内的一般有理ΠΣ*一阶求解、交错和积、乘积依赖换基、周期下降、有限商代数与根单位计算。53项专项、142项旧核心回归通过；12个CLI样例分别记录构造成功、无关系和一个仍不支持的代数系数域反例。详细算法及剩余任务见 [DIFFERENCE_FIELD.md](p1/DIFFERENCE_FIELD.md)，证据见 [报告](generated/difference_full_20261014/validation.json)。不分裂代数系数域参与后续移位等缺口尚未补齐，`stage_complete=false`；没有新增Train证明数。

**第四阶段核心升级**：统一 `solve_core.py` 新增 `difference_ring`，从和积移位关系自动构造参数化求和证书及完整解空间。支持基域有理乘积比的 Laurent 乘积块及其上的有限层多项式和塔；自动检查 Π/Σ 扩张，推导次数/支持界，并将冗余扩张化为带自由常数的表示，最后回代原变量。44项专项和98项旧核心回归通过，9个CLI例子已保存。见 [算法契约与推导](p1/DIFFERENCE_CORE.md) 和 [验收记录](generated/difference_core_20261014/validation.json)。一般扩张变量分母、任意和积交错及根单位环仍未支持；尚未接入原题转换或Lean层，没有新增Train覆盖声明。

2026-10-14 核心算法建设：新增独立入口 [solve_core.py](solve_core.py)，在现有 `p1/qgosper.py` 和 `p1/zeilberger.py` 基础上提供 q-Gosper、参数化 q-Gosper、q-Zeilberger 的标准化符号输入接口。它不要求 Train 编号或目标答案，不运行 Lean；`constructed` 只表示构造了局部符号证书。新共享内核计算右端线性组合，递推搜索检查移位相容性、支持从零阶开始，并输出多项式化的递推及同步缩放的证书。详细契约、用法和阶段边界见 [QGOSPER.md](p1/QGOSPER.md#2026-10-14独立核心求解器)。

已完成的 Train 基线为 4152 项任务、24 道不同公式成功，保存在 [train_baseline_20261014_24](generated/train_baseline_20261014_24/summary.json)。本轮算法修改后不重跑该基线；原始核心文件另存 [baseline_sources.json](generated/core_solver_20261014/baseline_sources.json)。下方 2026-10-13 的审核与验收记录属于此前版本。

核心第二阶段已接入同一入口的 `q_ore`：在已有 Ore 内核上增加左右除法、带 Bezout 见证的最大公右因子、多对象混合次数多项式闭包与正负移位，完善公左倍式和多项式规范化。给定递推后自动构造组合序列的递推；输入递推是前提，求和项局部关系不能绕过边界处理直接充当该前提。18 项 Ore 专项及 37 项旧算法回归通过；用法和边界见 [Ore 核心契约](p1/branches/ore_closure.md)，结果见 [validation.json](generated/ore_core_20261014/validation.json)。这仍是单变量递推核心，不代表完整多变量 holonomic 已实现。

核心第三阶段第一步已接入 `q_zeilberger_joint`：多个 q-超几何求和分量共享递推系数，所有 Laurent 方程联合求解，分别自动构造并精确检查证书。18项专项及55项旧算法回归通过，4个CLI样例通过，包含两个不同权重Gaussian分量的共同二阶关系。见 [联合算法契约](p1/QGOSPER.md) 和 [验证记录](generated/joint_core_20261014/validation.json)。当前支持对角分量系统，未利用跨分量相消，也未实现耦合矩阵方程；没有新增Train覆盖声明。

**第三阶段后续已完成有限秩耦合核心**：新增 `q_holonomic` 和 `parameterized_q_system`，通过逐坐标消元、算法推导的通用分母界及 q 幂共振次数界，在原耦合方程中联合构造有理证书。固定右端基的求解支持完整解空间基；创造性伸缩逐阶调用它。源表达式入口还能合并精确可识别的有理倍数及相消。完成范围为特征零形式 q、两个可逆相容移位、一个求和指标的有限秩模块；外层递推阶数搜索仍受预算控制。详见 [完整契约与界的推导](p1/QGOSPER.md) 和 [本阶段验收](generated/holonomic_core_20261014/validation.json)。上段第一步及更早报告保留为历史。

2026-10-13 更新：静态审核发现核反演、谱正交、行列式的一般分支依赖给定证书，现已为三条入口加入独立的自动符号构造器，并移除生产入口中的纯上下文证书回放。当前支持 1–5 阶、含符号参数的有限矩阵；任意符号阶数仍未实现。本次只运行合成专项检查，不运行 Train、不读取 Test。见[自动构造说明](research/automatic_matrix_construction_20261013.md)。此前[源码审核记录](research/symbolic_method_audit_20261013.json)保留为修改前快照。

|大方法|独立入口|内部后端|完整证明路径|
|---|---|---|---|
|有限差分与望远镜求值|[prove_telescoping.py](prove_telescoping.py)|直接 q-Gosper、双基 Gosper|原式表示 → 原差分构造 → 原域恒等式 → 有限求和和真实端点 → 原目标|
|递推关系与唯一性|[prove_recurrence.py](prove_recurrence.py)|目标引导 q-WZ、一般 q-Zeilberger、Ore 闭包、multisum|原式表示 → 构造递推及见证 → 边界与初值 → 递推唯一性 → 原目标|
|系数展开与有限卷积|[prove_coefficient.py](prove_coefficient.py)|Cauchy 系数展开、精确环规范化|表达式展开 → 系数及有限卷积 → 系数恒等式闭合 → 等式组装 → 原目标|
|MacMahon有限分拆分析|[prove_macmahon.py](prove_macmahon.py)|有限Omega、链式形式生成函数消元、Gaussian系数证书|原对象编码 → 约束消元 → 几何因子乘积 → 系数与原目标Lean；[首版边界](macmahon/README.md)|
|有限乘积与指标等价|[prove_product.py](prove_product.py)|有界指标重写搜索、幂规范化、精确环运算|冻结定义展开 → 拼接/分块/剩余类/反射证书 → 因子合并及逐项等式 → 原目标|
|嵌套和积的差分环证明|[prove_difference_ring.py](prove_difference_ring.py)|三角和积移位、目标引导差分不变量、SymPy多项式约化|求值表示 → 移位关系 → 局部或初值/不变量证书 → 原域Lean重建|
|有限核变换与矩阵反演|[prove_kernel_transform.py](prove_kernel_transform.py)|三角支撑转置、自动逆核与核乘积构造|表达式 → 支撑核验 → 核等式 → 任意序列作用 → Lean|
|有限谱正交证明|[prove_spectral.py](prove_spectral.py)|精确线性系统综合加权自伴分离算子|有限配对 → 构造算子 → 自伴与本征关系核验 → 原配对正交 → Lean|
|行列式结构证书|[prove_determinant.py](prove_determinant.py)|自动PLU及无除法行列式构造、结构求值|原对象桥接 → 结构识别／证书核验 → 行列式计算 → 原题Lean|
|加权双射与符号反转对合|[prove_combinatorial.py](prove_combinatorial.py)|对象表示、权重保持双射、对合消去|实际对象集 → 映射及权重证书 → 求和组装 → 原目标验证|
|非交换算子等式|[prove_noncommutative.py](prove_noncommutative.py)|算子定义展开、非交换词重写、加法正规化|实际Expr → 语义展开 → 局部关系下的有限词计算 → 原目标Lean验证|
|插值、零点与有理函数主部|[prove_interpolation.py](prove_interpolation.py)|精确节点证书、SymPy部分分式及重构|原域清分母 → 次数与互异节点证书 → 根数定理；主部分支另验证完整分解桥接 → 原目标|

```bash
# 在 finite_product_framework 目录运行
python3 prove_telescoping.py --identity FQI-SRC-AP-3.3.9
python3 prove_recurrence.py --identity FQI-GAUSS-ALTERNATING
python3 prove_coefficient.py --identity FQI-SRC-FINE-15.2
python3 prove_product.py --identity FQI-POCHHAMMER-RESIDUES
python3 prove_interpolation.py --identity FQI-SRC-KAC-CHEUNG-1.11-12
python3 prove_noncommutative.py --identity FQI-SRC-KAC-CHEUNG-5.7
python3 prove_combinatorial.py --identity FQI-SRC-KAC-CHEUNG-6.5
python3 prove_difference_ring.py --identity FQI-SRC-FINE-2.3
python3 prove_kernel_transform.py --identity FQI-SRC-AQ-3.23
python3 prove_macmahon.py --identity FQI-RECTANGLE-PARTITIONS
# 下两条用于记录尚未闭合的原题义务；当前预期 unproved
python3 prove_spectral.py --identity FQI-SRC-GR2-7.2.22
python3 prove_determinant.py --identity FQI-SRC-AP-11.2.4
# 独立入口验收：15条原题成功，谱/行列式原题未解决，另有专项模块验收
python3 check.py
# 审计已有的各类运行产物，并执行流程及共享基础回归
python3 check.py --audit-existing
```

工作区解释器 `/home/hjy/Project/.venv-finiteq-multisum/bin/python` 包含 multisum 所需 python-flint。十二个入口都有 `--help`；不接受更换大方法的 `--method` 参数。旧 `prove.py` 仅为显式指定 `--method` 的兼容调度命令，不提供默认或 `auto` 模式。

## 每条流程内部的组织

每条均按“冻结原 train 声明 → 本类表示分析 → 本类候选计划 → 构造及 Lean 验证 → 证据接收”执行。分析阶段即排除其他类的前端，构造进程再次校验所属方法。构造、表示、边界闭合或 Lean 验证失败后只尝试本类下一候选；全部失败则报告未完成，不偷偷换用另一类证明。

只有原声明、原域、端点或初值等义务全部闭合，Lean 编译及精确目标公理审计通过，且来源、依赖、证明文件哈希一致，才返回 `proved`。不接收仅有符号关系或后端成功标记的结果；伪成功返回 `integrity_error`。失败不表示恒等式不可证明。

默认总预算 900 秒、单次尝试 600 秒、分析 120 秒、符号构造 240 秒；可用 `--seconds`、`--attempt-seconds`、`--analysis-seconds`、`--symbolic-seconds` 调整。超时终止整个进程组，包括 Lean 和符号计算子进程。

## 共享代码与独立产物

- 十二个 `prove_<method>.py` 固定各自的方法边界；复用命令参数解析。
- `workflow/engine.py` 为每条流程提供状态管理、类内计划、预算和失败处理；没有跨类 auto 路径。
- `workflow/worker.py` 在独立进程中接入已有数学后端，避免旧 P1/P2 同名模块冲突；仅探测所选类。
- `workflow/contracts.py` 复用原声明快照和严格证明接收规则。
- `p1/`、`p2/` 保留数学构造器、Lean 生成器和公共引理；它们是历史代码位置，不是这三类方法的入口划分。

结果分别保存到 `generated/telescoping/<run-id>/`、`generated/recurrence/<run-id>/`、`generated/coefficient/<run-id>/` 、`generated/product/<run-id>/` 、`generated/interpolation/<run-id>/` 、`generated/noncommutative/<run-id>/` 、`generated/combinatorial/<run-id>/`、`generated/difference_ring/<run-id>/`、`generated/kernel_transform/<run-id>/`、`generated/spectral/<run-id>/` 和 `generated/determinant/<run-id>/`。每次运行有独立 `report.json`，包含分析、类内计划、尝试、未闭合义务与最终证明路径；底层原生报告保存具体构造及 Lean 输出。

修改前的历史验收报告为 [method_pipelines_validation.json](generated/method_pipelines_validation.json)，检验十二个实际 CLI、15条成功原题及2条未解决原题，并审计对合模块证据、流程隔离与共享基础回归；`mode` 区分重新运行CLI与已有证据审计。旧 [workflow_validation.json](generated/workflow_validation.json) 仅记录先前合并入口的验收。product原题在本次构建中实际运行；验收脚本不自行统计全库新增去重覆盖，旧代表题的重检不重复增加覆盖。

## 数学能力边界

旧三类范围仍由既有 P1/P2 train 分配限定，不读取 test 或 P3。新增 product、interpolation、noncommutative、combinatorial、difference_ring、kernel_transform、spectral、determinant 和 macmahon 类读取全部 Train 清单并按实际表达式判断支持，不导入隔离区代码。范围表控制输入授权，不按题号提供证明或选择后端。各后端仍受已有表达式、参数域和预算限制：递推出口沿用已有一/二阶、对象闭包及二维三角域支持；系数流程限于当前 Fine 表示和能通过逐项环恒等式闭合的有限卷积。

本次修正流程组织，不新增一般高阶、高维出口，也未实现任意引理分解、跨方法递归合作或 P2 自动调用 P1 证明一般系数核。原有专项测试没有因此视为全部重跑。全目录构建与验证存在的缺失依赖见[历史工程检查](generated/workflow_project_checks.json)。

除新授权的 product、interpolation、noncommutative、combinatorial、difference_ring、kernel_transform、spectral、determinant 和 macmahon 类外，其他候选方法的实现继续暂停。reduction_ct 与 P3 诊断保存在[隔离目录](../deferred_work/2026-10-13/README.md)，不参与正式入口、导入或验收。

## 有限乘积与指标等价：首版能力

独立入口 `prove_product.py`；数学后端在 `product/`。从冻结声明展开 `poch`/`pochList`，导出实际 Lean 表达式，识别自然数 `range` 乘积。Python 根据长度表达式枚举至多两步的类内重写计划；Lean 验证通用的区间拼接、分块、剩余类重排或显式反射，再通过同域乘积合并、逐项合同、幂恒等式和 `ring` 精确运算闭合。未调用外部 CAS，不按题号挑证明，不预存目标恒等式证书。

成功产物包括 `Proof.lean`、绑定原声明与证明哈希的 `certificate.json`、逐候选日志和原目标公理审计。通用重排引理对任意交换幺半群成立；因子环证明保留原参数域，支持零参数和空乘积。

首版不支持任意整数区间、负长度、单位根分解、一般带分母约消，或任意深度重编号搜索。未支持的语法和未闭合的等式返回未证明。反射目前支持显式反射指标的乘积，不承诺完成倒底数公式。

原题验收选择 `FQI-POCHHAMMER-RESIDUES`，证明任意域及符号长度的剩余类拆分。执行 `python3 product/check.py` 检查改名、反向等式、拼接、因子合并、显式反射及错误公式拒绝；结果见 `generated/product_validation.json`，合成用例不计入 Train 覆盖。

## 插值、零点与主部：首版能力

入口 `prove_interpolation.py`，独立数学实现 `interpolation/`，按实际表达式选择类内后端。需安装SymPy（当前验收版本1.14.0）。

|阶段|构造算法|Lean闭合义务|
|---|---|---|
|表示与原域处理|提取标量算术AST，其他表达式保留为原子；可展开冻结jackson定义及拆分合取|只替换原声明证明槽；field_simp从原假设验证分母条件|
|多项式零点证书|递归计算某个原子的次数上界d；SymPy在0至d逐点精确计算符号残差|compute_degree验证上界；CharZero证明节点互异；逐点精确证明后用根数定理得零多项式，再代回原式|
|主部重建|SymPy apart与线性因子分解，提取各极点各阶主部及多项式部分|两侧到共同分解的完整桥接均须在原域成立；清分母后的残差使用零点证书验证|
|验收|保存certificate.json、Proof.lean、候选日志和输入快照|原定理公理列表、源码/依赖/证书/证明哈希绑定|

这是真正使用多项式根数定理的证明路径。采样值是保留其他参数的精确符号值；有限数值试验不是证明。主部分支使用完整代数重建，不依赖解析留数或只比较极点的论证。

首版要求CharZero；支持可表示的固定数值次数上界，默认max-degree为5，可设至12。尚无符号次数、任意维数q-Dyson、多变量稀疏网格的证书构造。主部分支限于所选变量上的线性因子及其幂；重极点和多项式部分均保留。额外分母不能由原假设证明时报告未完成，不添加一般位置假设。

原题验收：KAC-CHEUNG-1.11-12经两个零点证书证明乘法规则完整合取；KAC-CHEUNG-1.13-14经两个主部分解和四个零点证书证明商法则完整合取，原参数域不变。执行 `python3 interpolation/check.py` 运行模块验证，结果见 `generated/interpolation_validation.json`。合成用例不计Train覆盖；全Train覆盖率尚未测定。

## 非交换算子等式：首版能力

独立入口 `prove_noncommutative.py`，后端 `operator_word_normalization`，实现位于 `noncommutative/`。这条流程证明算子作用与有限非交换词等式，与递推类的 Ore 闭包用途不同。

|阶段|算法／工具|证明义务|
|---|---|---|
|表示与范围检查|Lean Expr导出，Python语法检查|保留变量类型、原假设与冻结定义；仅允许显式不超过12的幂，拒绝任意n、有限和及未知函数原子|
|算子语义展开|Lean simp，Polynomial.mul_comp / X_comp / C_mul'|由真实kacX、kacM定义展开多项式复合；验证标量作用和乘法的相容性|
|非交换词计算|noncomm_ring：分配展开、右结合、数值幂展开、局部等式重写|保持乘积次序；标量移出乘积必须由原域上的类型类提供合法性|
|系数与加法整理|simp标量作用规则、abel加法正规化|只在加法层重排，不能无假设交换两个乘法因子|
|原目标验收|Lean kernel、精确目标公理审计、哈希绑定|原声明完整保留；Proof.lean与certificate.json、原始来源及依赖一致，无未闭合义务|

符号计算在Lean内完成，未调用外部CAS。证书记录实际表达式、局部关系、阶段和证明脚本，最终可重放证据是Lean证明；不声称输出逐项换位日志。生产逻辑不按题号路由，也不导入Benchmark已有目标证明。复用product模块的进程执行／文本拼接工具，不调用其数学后端。

已验收Train原题 `FQI-SRC-KAC-CHEUNG-5.7`：任意域上真实多项式算子的 `M_q X = q X M_q`，无新增假设。模块测试还检查非交换平方展开、含q交换关系的平方、变量改名、错误交换关系／系数的拒绝。运行 `python3 noncommutative/check.py`，结果见 [noncommutative_validation.json](generated/noncommutative_validation.json)。合成测试不计为Train覆盖。

首版是不完备的有限词化简器，不保证任意给定关系都有合流正规形，不做逆向除q、Knuth–Bendix补全或非交换Gröbner基；一般符号系数多项式合并也可能留下目标。`FQI-SRC-KAC-CHEUNG-5.8` 含任意n及Gaussian有限和，需要额外的归纳与系数递推桥接，当前明确返回未证明。未进行全Train批量覆盖测量。


## 加权双射与符号反转对合：首版能力

独立入口 [prove_combinatorial.py](prove_combinatorial.py)，实现位于 `combinatorial/`。包含 `weighted_bijection` 和 `sign_reversing_involution` 两个类内后端。按实际Lean表达式选择对象与映射模板，不按题号选证明。

|阶段|算法／工具|核验义务|
|---|---|---|
|对象与权重表示|Lean Expr导出，Python结构匹配|原域、对象集和完整权重；未知表示不能略过|
|映射构造|有限模板：自然区间反射、整数区间反射、子集插入/删除、子集元素切换|映射在定义域内，单射/满射或显式逆映射；分解子集时两类互斥且覆盖|
|权重计算|simp、幂运算、ring/linear_combination；omega核验指标边界|双射保持权重；对合配对权重和为零|
|求和组装|sum_bij、sum_image、sum_union、sum_involution|对合的固定点必须另证权重为零；不得由2w=0擅自除2|
|原题验证|Lean kernel、公理审计、哈希证书|原声明不变，表示和全部局部义务闭合才返回proved|

Gaussian子集表示另有已核验的桥接：任意权重的 `subset_split` 先将固定基数子集分成不含/含新最大元两类；插入的逆映射为删除。对权重 `∏ i ∈ s, q^i`，插入使权重乘以 `q^(n+1)`。对符号n归纳，结合共享的Gaussian局部递推得到 `geometric_subsets`，最后验证原式的整数指数归一化。原始乘积权重桥接在q=0也成立，归一化使用原假设q≠0。未导入Benchmark现成目标证明；未调用递推入口。

已通过Train原声明 `FQI-SRC-KAC-CHEUNG-6.5`，不是固定n枚举。符号反转分支的元素切换支持权重 `(-1)^|t| * w(t.erase a)`：切换a改变符号而保留其余权重，且没有固定点。元素切换与反射对合通过模块用例验证；尚未宣称该分支证明了另一条Train原题。所有合成用例单独记录，不计Train覆盖。符号计算在Lean内完成，无外部CAS依赖；证书包含选定映射、逆映射/固定点说明、实际表达式及可重放证明脚本，不声称提供完整逐对象轨迹。

当前候选集有限：反射要求匹配的区间；子集切换仅自动试0和1；并非任意组合对象双射发现器。未支持一般分拆、格路径局部变换、Franklin/Garsia–Milne对合搜索，也没有任意非零固定点剩余和的自动识别。未完成全Train覆盖测量；未闭合映射、权重、表示或固定点义务时只报告未证明。

运行 `python3 combinatorial/check.py` 检查反射、子集切换、变量改名、错误权重/定义域、空底集、特征2非零固定点、缺失q非零条件及证书篡改。结果见 [combinatorial_validation.json](generated/combinatorial_validation.json)。原始Train文件哈希见 [combinatorial_source_audit.json](generated/combinatorial_source_audit.json)。


## 嵌套和积的差分环证明：首版能力

独立入口 [prove_difference_ring.py](prove_difference_ring.py)，实现位于 `difference_ring/`，后端 `triangular_difference_ring`。首版是目标引导的、具有真实序列求值的三角差分环约化；不是完整Karr/Sigma，也不保证发现任意差分原函数。目标给出的候选等式被视为待验证差分不变量，无法在当前关系中约化时返回未证明。

|阶段|算法／工具|证明义务|
|---|---|---|
|和积表示|Lean Expr提取；冻结poch、pochList、fineC定义；Python提取嵌套前缀节点|必须连接真实序列，首版求和/求积域限于自然数range|
|移位扩张|sum_range_succ、prod_range_succ、pow_succ及新证poch_shift|S(k+1)=S(k)+f(k)，P(k+1)=P(k)f(k)，q幂乘法移位；嵌套关系由真实定义重建|
|目标引导约化|SymPy精确多项式展开和reduced|局部移位残差为零，或移位后的等式残差属于当前等式关系生成的理想；输出乘子及零余式|
|求值与初值闭合|Lean归纳、空和/空积规则；field_simp使用原假设|不允许用形式移位恒等式跳过初值；约消分母须非零；允许乘积因子为零而不做逆向约消|
|证明重建|ring、linear_combination、Lean kernel及公理/哈希审计|CAS乘子逐条重建，原声明、原域、所有初值和局部义务完整闭合|

该流程有“局部移位”和“差分不变量”两种类内计划，后者至多尝试前四个自然数参数。共享序列求值规则，不调用Gosper、q-Zeilberger、Ore闭包或其他类的入口。SymPy原子独立只用于保守构造，绝不把代数独立性、常数域保持或乘法生成元可逆性当作原题假设。

Train原题 `FQI-SRC-FINE-2.3` 已完整证明：乘积商fineC的移位关系，保持所有原始分母条件。此题在经过核验的移位与分母化简后直接闭合，不将它说成嵌套和覆盖或CAS求解难例。嵌套累积和、前缀平方、以累积和为因子的累积积等另由 [check.py](difference_ring/check.py) 验证，结果以 [difference_ring_validation.json](generated/difference_ring_validation.json) 为准；合成用例不计Train覆盖。

例如混合嵌套用例取 `S(k)=∑ i<k, f(i)`、`P(k)=∏ j<k, (1+S(j))`，自动证明 `∑ k<n, S(k)P(k)=P(n)-1`。将外层和记为 `T(n)`，移位后残差为 `T(n)+S(n)P(n)-((1+S(n))P(n)-1)`；CAS将其约化为归纳关系 `T(n)-P(n)+1`，返回乘子1。Lean重建这个等式，并单独验证初值 `0=1-1`。这里的嵌套求值、符号约化和初值检查共同构成完整证明。

默认多项式总次数上限5、至多32个原子，项数受max_unknowns约束；可通过公共预算参数调整次数与项数，整个构造进程受symbolic_seconds限制。理想约化采用有序多项式除法，未做完整Gröbner基补全；关系不足时允许失败。尚未实现一般分母界求解、参数化望远镜、扩张最小化、深度最优化、任意移动上下界和多指标递推。未批量测量全部Train覆盖。

产物包含源声明、识别出的和积节点、移位后目标/原关系、CAS乘子及余式、Proof.lean、公理审计和绑定来源/证明的certificate.json。节点记录不是最小代数独立ΠΣ扩张声明。原Train文件完整性见 [difference_ring_source_audit.json](generated/difference_ring_source_audit.json)。


## 有限核变换与矩阵反演：自动构造

入口 [prove_kernel_transform.py](prove_kernel_transform.py)。[构造器](kernel_transform/construct.py)只从原核 A 求符号逆矩阵，或从 A、B 计算复合核 A B，再证明计算结果与原目标中的核相等。目标给出的逆核不参与求逆搜索。Lean 逐项验证核恒等式后组装任意序列作用。三角支撑转置仍保留为独立的类内计算计划；任意有限指标集上仅靠已有逆核假设的分支已退出生产入口。

支持 1–5 阶、含符号参数的矩阵；分母非零义务必须由原题条件闭合。没有任意符号阶数的 q 超几何闭式逆核发现器。历史 Bailey 转置原题成功不代表一般反演覆盖。专项证据见 [kernel_transform_validation.json](generated/kernel_transform_validation.json)。

## 有限谱正交：自动构造

入口 [prove_spectral.py](prove_spectral.py)。[构造器](spectral/construct.py)从原配对的权重 w 和向量 f、g 建立精确线性系统，求未知算子 A，使 A f = 0、A g = g、diag(w) A = Aᵀ diag(w)。Lean 核验构造出的算子及两组本征关系，再由本征值 0、1 分离推出原配对为零。不需要用户先提供算子。

当前限 1–5 维配对，不自动发现 q-Hahn/q-Racah 的符号维差分算子，不计算整族范数；不能构造或无法证明原域义务时返回未证明。原先仅依靠现成谱/范数条件的入口分支已移除。专项证据见 [spectral_validation.json](generated/spectral_validation.json)。

## 行列式结构证书：自动构造

入口 [prove_determinant.py](prove_determinant.py)。[构造器](determinant/construct.py)只从原矩阵计算 P、L、U 以及精确行列式值，目标右端不参与搜索。Lean 验证 P A = L U、各因子行列式及原目标。若参数主元引入无法证明的分母，改用 Berkowitz 值和 Lean 余子式展开，保留参数为零等原始情形。

自动矩阵构造限 1–5 阶；Vandermonde、对角等结构求值仍保留。没有任意阶闭式分解或组合枚举到行列式的自动桥接，Carlitz 原题此前的桥接缺口尚未解决。专项证据见 [determinant_validation.json](generated/determinant_validation.json)。

三条入口保存原始声明、构造输入、数学证书、Lean 证明和依赖哈希。共享导出与验证运输层，不跨类路由。只在 Lean 证明完整原声明且无 sorryAx 后接受成功。本轮证据与能力边界见[自动构造说明](research/automatic_matrix_construction_20261013.md)；旧统一 Train 验收报告不代表修改后的覆盖结果。
