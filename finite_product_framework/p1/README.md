# P1 输入驱动的证明流程

原题证明分别使用[三类流程](../README.md)中的 `../prove_telescoping.py`（有限差分求值）或 `../prove_recurrence.py`（递推唯一性）；本目录入口保留为后端调试。每类内部在适用后端构造或验证失败后继续尝试，不跨类切换。

正式范围仅保留有限差分求值与递推唯一性证明。已撤出的实验移至[隔离目录](../../deferred_work/2026-10-13/README.md)，不再提供正式入口；全框架范围见[工作范围](../README.md)。

新增[多重 q 创造性望远镜分支](branches/multisum.md)：多维符号内核与二维三角域原生 Lean 出口已接通，GR2-10.Ex18 原声明完整通过，P1 累计 **12 条**。高维原题自动 Lean 出口仍待扩展。本轮验收见 [multisum_validation.json](generated/multisum_validation.json)，历史统一验收不代表本轮全量重跑。

新增[q-Ore 闭包与消元分支](branches/ore_closure.md)：从定义自动取得递推，再计算乘积状态及非齐次关系，已闭合 Rogers–Szegő 有限 Turán 原题 GR2-7.Ex40，当时累计 **11 条**。下文各扩展章节保留历史记录；历史统一验收见 [validation.json](validation.json)。

P1 采用共享流程与多个证明分支。现有目标引导的一阶 q-WZ、直接 q-Gosper、一般 q-Zeilberger、双基 Gosper、Ore 闭包和多重 q 创造性望远镜六个分支，共享目标导出、局部验证、公理审计和求和引理。已自动证明 **12 条原始 train 目标**：终止 q-Kampé de Fériet 双重求和 GR2-10.Ex18、Rogers–Szegő 有限 Turán 式、双基 Gosper 有限求和 GR2-II-34、Gauss 交错 Gaussian、有限 q 二项式、Gaussian 加权 hockey-stick、Kac–Cheung 4.4、AP-13.E3、GR2-1.Ex3i、GR2-1.Ex6iii，以及两种 q-Chu–Vandermonde；当前分支验收见 [multisum_validation.json](generated/multisum_validation.json)，此前统一验收见 [validation.json](validation.json)。不以覆盖全部第一族为目标。

具体题目的证书、分母、次数、递推、边界、初值和证明不得预填；允许通用算法、数学改写规则、共享 Lean 引理与资源限制。旧专用试点位于[停用档案](archive/preset_pilot/README.md)，不参与当前运行或自动覆盖。

双基分支的算法、原域处理及当前出口限制见[双基 Gosper](branches/bibasic_gosper.md)。它直接搜索原差分，首例不新增 c≠1 假设。

## 运行

在本目录执行：

```bash
python3 run.py --identity FQI-FINITE-Q-BINOMIAL
python3 run.py --identity FQI-GAUSS-ALTERNATING
python3 run.py --identity FQI-SRC-GR2-II-34
python3 run.py --identity FQI-SRC-GR2-7.Ex40
python3 run.py --identity FQI-SRC-AP-3.3.9
python3 run.py --identity FQI-SRC-KAC-CHEUNG-4.4
python3 run.py --identity FQI-SRC-AP-13.E3
python3 run.py --identity FQI-SRC-GR2-1.Ex3i
python3 run.py --identity FQI-SRC-GR2-1.Ex6iii
python3 run.py --identity FQI-CHU-VANDERMONDE-Q
python3 run.py --identity FQI-CHU-VANDERMONDE-BALANCED
python3 check.py
```

原生入口直接读取并核对原 train 声明，按表达式结构选择分支，不按 ID 选择证明。每条公式的证明及报告独立保存在 `generated/runs/<identity>/`，`generated/run.json` 只是最近一次运行。`check.py` 重跑十一条原题、17项基础测试，以及原一阶分支3项、直接分支4项、有限乘积扩展4项、卷积扩展5项及终止phi扩展3项、有限参数域扩展7项及一般q-Zeilberger分支13项及双基Gosper分支14项及Ore分支13项检查；合成变体均不计训练覆盖。

|原始训练目标|实际分支|证明及报告|
|---|---|---|
|有限 q 二项式|目标引导 q-WZ，调用 q-Gosper|[证明](generated/runs/FQI-FINITE-Q-BINOMIAL/Proof.lean)、[报告](generated/runs/FQI-FINITE-Q-BINOMIAL/report.json)|
|Gaussian 加权 hockey-stick|直接 q-Gosper，验证端点|[证明](generated/runs/FQI-SRC-AP-3.3.9/Proof.lean)、[报告](generated/runs/FQI-SRC-AP-3.3.9/report.json)|
|Kac–Cheung 4.4：单项式的有限 q 幂展开|原有目标引导 q-WZ，调用 q-Gosper|[证明](generated/runs/FQI-SRC-KAC-CHEUNG-4.4/Proof.lean)、[报告](generated/runs/FQI-SRC-KAC-CHEUNG-4.4/report.json)|
|AP-13.E3：三变量 q-下降乘积卷积|原有目标引导 q-WZ，调用 q-Gosper|[证明](generated/runs/FQI-SRC-AP-13.E3/Proof.lean)、[报告](generated/runs/FQI-SRC-AP-13.E3/report.json)|
|GR2-1.Ex3i：两种有限 q 卷积（两个子式均完成）|每个子式调用同一 q-WZ 分支，再组装合取|[证明](generated/runs/FQI-SRC-GR2-1.Ex3i/Proof.lean)、[报告](generated/runs/FQI-SRC-GR2-1.Ex3i/report.json)|

## 11条候选的公共能力扩展：再闭合两条

[本轮逐条结果](research/shared11/index.html)、[独立审计](research/shared11/validation.json)、[机器统计](research/shared11/summary.json)。两种q-Chu–Vandermonde现在都由统一入口完成原statement证明，完整覆盖从6条增至8条；本批11条全部重试，另9条尚未完整闭合，没有判定它们不适用于P1。

|新增完整目标|证明及执行报告|
|---|---|
|q-Chu–Vandermonde，自变量q|[证明](generated/runs/FQI-CHU-VANDERMONDE-Q/Proof.lean)、[报告](generated/runs/FQI-CHU-VANDERMONDE-Q/report.json)|
|平衡型q-Chu–Vandermonde|[证明](generated/runs/FQI-CHU-VANDERMONDE-BALANCED/Proof.lean)、[报告](generated/runs/FQI-CHU-VANDERMONDE-BALANCED/report.json)|

公共扩展包括：由phiDefined提取有限支撑内的非零分母；乘积前缀、尾段和移位起点规则；终止上参数转换；必要时用非零q的三角次幂清除负幂；Gaussian相邻指标关系。表示桥接不含求和求值答案。q-WZ证书及相邻关系的组合系数均由输入和搜索结果计算，最后在原定义上验证。没有增加原假设，不要求全局regular q，不除以可能为零的目标值。

[新增7项回归](generated/domain_tests.json)检查移位起点与零起点、两条原题改名、缺失有限分母假设、错误证书、错误初值目标，以及不带任何非零假设的通用尾乘积多项式恒等式。合成变体不计训练覆盖。

另9条在研究入口完成了由Lean实际执行的表示预处理：显式Pochhammer列表展开、命名项展开且保留分段条件、已有参数等式代换；其中3条双边求和已在原目标中重编号。公共整数Gaussian支撑桥接引理也已验证。预处理以刻意的P1_EXPORT_ONLY结束，不是原目标证明；随后连接整数幂、相关基底、通量可去极点和端点的生成仍未完成。生产入口对这9条仍报告unsupported_structure。

重现本批运行 `python3 research/shared11/run_batch.py` 与 `python3 research/shared11/check_batch.py`；完整覆盖用 `python3 check.py` 验收。下面的12条记录保留扩展前的历史状态。

## 剩余12条的整批推进（上一轮，累计6条）

[逐条结果和剩余义务](research/remaining12/index.html)、[机器统计](research/remaining12/summary.json)、[CSV](research/remaining12/table.csv)。12条全部通过原声明类型检查，全部从实际Lean表达式重新构造出证书，全部清分母后的局部代数关系通过Lean。局部关系不承担原表达式转换、原参数域、边界和初值的证明，因此本批只新增完整原题证明1条，另11条尚未完成；不能把这些实现缺口判为P1算法不适用。

新增完整证明为[GR2-1.Ex6iii](generated/runs/FQI-SRC-GR2-1.Ex6iii/Proof.lean)：公共终止上参数规则把2φ0的每一项改写为Gaussian与有限乘积；统一q-WZ入口随后从改写后的输入实时计算递推和证书，Lean验证完整原statement。`PhiRules.lean`只包含表示等式，没有预填求和结果。仍是原来的两个分支，没有新增证明算法。

[终止phi回归](generated/phi_tests.json)检查改名输入、删除参数非零假设以及篡改证书。后两项必须被Lean拒绝。其余11条的具体缺口分为：两条带下参数的phi、一条外部乘数与移位乘积、两条直接原差分的分段端点、三条双边支撑、三条相关基底与分母条件。对应表逐条列出未完成义务，不将形式有理函数的分母自动加入原定理假设。

重现本批：依次运行 `research/remaining12/audit.py`、`native_symbolic.py`、`verify_local.py`、`summarize.py`（后三者同目录）。原式完整证明仍由 `run.py` 和 `check.py` 验收。最初15条符号成功候选中累计4条完整闭合、11条未完成；加上更早两条，共6条原始train证明。

## 卷积扩展：再闭合两条原始 train（上一轮）

AP-13.E3与GR2-1.Ex3i均由统一原生入口完整证明。前者从实际Finset.prod绑定变量和乘积因子识别有限q幂，再由公共乘积等式桥接回原表达式；后者从原And表达式识别两个子式，分别实时计算证书，最后在同一个原statement中验证两者。GR2-1.Ex3i只计一条训练公式。

新增证书表示允许把Q/X重写为求和支撑内的q^(n-k)，前提是重写后为多项式；局部证明明确拆分k=n与k<n并验证自然数减法、乘积后继及Gaussian递推。最终仍直接在原多项式定义上验证，没有加入q或其他参数非零假设，也不依赖形式商在特殊参数处有定义。

这仍是已有q-WZ分支的公共表示与证明生成扩展。当时最初15条符号成功候选中累计3条完整闭合（含此前Kac–Cheung 4.4），剩余12条待推进；加上更早的两条，共5条完整证明。[卷积回归](generated/convolution_tests.json)检查改名并加倍权重的原始乘积、篡改含n-k证书、两个合取子式改名、只篡改第二个证书、只改错第二个目标。

## 15 条符号候选中的首条完整闭合（上一轮）

Kac–Cheung 4.4已从局部符号成功推进到完整原始train证明。统一入口直接读取原式，识别反向等式、Gaussian与有限乘积原子，实时推导移位比并运行q-Gosper。证书先平移到实际求和指标，再检查能否用多项式乘移位求和项表示；没有从研究日志读取证书。

新增公共规则只有有限乘积的零长度与后继长度展开。生成器在原Gaussian递推和乘积定义上验证局部恒等式、两个端点、初值及目标递推。因此符号搜索中出现的形式商不会变成原定理的新假设，x=0保留；目标仍沿用原statement的全部条件。原源码中的`kacPowerNat`定义逐字提取并记录哈希，不导入Batch5Proofs或旧恒等式证明。

这没有新增算法分支。当时15条符号候选中1条完整闭合，另14条待推进。下方41条试验表和审计是扩展前的历史快照，保留当时“新增Lean证明0”的结论；当前证明覆盖以本页顶部及最新validation.json为准。[有限乘积扩展检查](generated/product_tests.json)覆盖取消q非零/非一假设、参数改名及平方、篡改证书拒绝、错误目标初值拒绝。

## 18+23 条候选的实际符号试验（扩展前快照）

本轮只尝试这41条，另8条暂不处理。按奇偶、支撑情形及多个子式拆成50个局部问题，使用当前q-Gosper内核逐项构造，没有预填证书或递推答案。详见[逐条结果表](research/trials41/index.html)、[CSV](research/trials41/table.csv)、[统计](research/trials41/summary.json)及[独立审计](research/trials41/validation.json)。

|本次结果（按原公式计）|18条优先候选|23条条件候选|合计|
|---|---:|---:|---:|
|全部已列局部问题构造出证书|9|6|15|
|构造超时|9|15|24|
|所选局部差分返回无q超几何原差分|0|2|2|

成功的15条共16个局部证书；两条无原差分返回是AQ-3.17和AQ-3.18。其余32个局部问题超时。

这是研究层的算法试验：输入是显式转录的求和项、目标及候选变换，尚未从原Lean表达式自动提取。成功状态只表示所有已列出的局部问题构造出了证书；原参数域、变换合法性、零支撑、边界及初值仍需验证，**本轮新增完整Lean证明0条**。原有2条完整证明及生产代码保持不变。

每个局部问题准备预算60秒、构造预算30秒，4个任务并行。`timeout`不表示P1不适用；`no_antidifference_for_chosen_local_problems`只描述所选局部差分及形式函数类，不排除更换递推构造或其他方法。精确有限取值检查用于筛查转录错误，不代替一般证明。

复现：

```bash
python3 research/trials41/run_trials.py
python3 research/trials41/check_trials.py
```

下一步优先从证书已构造成功的候选中补齐原语义及边界义务，再接入统一Lean输出。全目录构建/验证仍被既有缺失依赖阻塞，见[工程检查记录](research/trials41/project_checks.json)，不计作本轮试验审计通过。

## 当前定位与数学适用性复审

P1 是多种符号证明方法中的一种，不以覆盖全部 197 条公式为目标。筛选先判断当前两条路线的数学结构，再决定是否值得做符号试验；不以原生前端能否解析作为数学适用标准。未入选的公式保留给其他方法，不作不可证明结论。

对原 51 条初筛候选逐条复审后：**2 条已完整验证、18 条优先符号试验、23 条先核查关键条件、8 条本轮转交其他流程**。逐条理由、支撑/平衡/参数条件、后续动作及备选方法见[复审表](research/applicability/index.html)和[CSV](research/applicability/review.csv)。这不是互斥或完备分类，也未重新排除其余 146 条。

当前 q-WZ 路线要求经合法变换后求和项的两个移位比及目标相邻比可以在单基移位变量中有理表示；仍需 q-Gosper 成功构造局部原差分，并闭合原域、边界和初值。直接 q-Gosper 路线允许外部参数固定后对实际求和项求原差分，再比较端点；数学上允许项依赖外部 n，尽管当前程序回译更窄。有理项比只是候选依据，不保证证书存在。

本轮对两种 q-Chu–Vandermonde、GR2-1.Ex6iii 的终止2φ0、Kac–Cheung-4.4下降积展开进行了4次研究性试验：全部从显式转录的求和项与目标计算移位比，调用现有 q-Gosper，得到证书并独立复核局部有理恒等式。没有预填证书或递推答案。**转录尚未由原 Lean Expr 自动导出，也未验证原域、边界与初值，因此新增完整 Lean 证明为0。** 16个精确有限检查/条仅作转录诊断，不代替一般证明。

[复审审计](research/applicability/validation.json)核对51条原文件及4份共享定义的哈希、4个证书的独立残差与生产代码未变。下一步优先把已有符号构造证据的候选接入完整原生流程，只为这些入选公式补必要公共能力。

## 197 条 train 筛选与实测

本轮没有增加算法分支或证明规则。全部 197 条均调用同一 `run.run` 原生流程，共享定义在批次开始时重编译一次，各条运行前核对源文件和编译产物哈希；成功证明后再次核对。代码版本、预算、每条失败原文、证明及哈希均保存。

|结果|全部 197 条|现有两分支的 51 条结构候选|
|---|---:|---:|
|原始 Lean 目标完整通过|2|2|
|定义上下文缺口|166|30|
|表达式导出缺口|29|19|

51 条候选来自已有逐条结构审阅：43 条含 q-WZ 路线、10 条含直接 q-Gosper 路线，重叠 2 条。候选列表不保证方法适用，也不是可解范围的上界。其他条目仍实际运行，未按旧分类跳过。

只有原有两条进入符号构造并完整通过，本轮新增证明为 0。其余 195 条未到达符号构造，不能称为 q-Gosper 搜索失败或数学上不可证明。当前隔离环境尚未加载许多原声明需要的定义（例如 `regular`）；`pochList`、`phi`、整数幂与其他表达式导出也有缺口。每条只观察到首个阻塞阶段，后续是否还有障碍尚不确定。

- [完整可筛选结果表](generated/train_a_screen/index.html)：197 条、依据、结果与独立日志。
- [现有分支的 51 条候选 CSV](generated/train_a_screen/current_candidates.csv)。
- [全部结果 CSV](generated/train_a_screen/table.csv)与[统计及版本](generated/train_a_screen/summary.json)。
- [独立审计及瓶颈分析](generated/train_a_screen/analysis.json)：394 个原文件哈希、运行报告、代码及依赖、成功证明的公理审计全部通过；篡改批次快照被拒绝。

复现及核查：

```bash
python3 batch.py --workers 4 --seconds 30
python3 review_batch.py
```

上述批次反映实现故障，不决定数学适用性。工程扩展范围以最新数学复审的入选公式为准，不以消除全部197条的输入缺口为目标。

## 目标引导分支的完整链路

1. [Lean Expr 导出](lean/Extract.lean)：在保留原声明上下文的情况下 elaboration 目标；不导入含占位的原题定理。
2. [表达式转换](expressions.py)：从实际求和项和右端推导移位比 U、V 和目标相邻系数 c。
3. [q-WZ 构造](search.py)调用 [q-Gosper](qgosper.py)：计算正规形、Laurent 次数界、解系数方程，恢复并复核证书 R。
4. [证明生成](lean_pipeline.py)：从 R 与实际项比构造望远镜项 G；使用通用 Gaussian Pascal、幂和多项式改写生成局部、尾项、初值及目标递推证明。
5. [共享引理](lean/Shared.lean)完成有限求和及归纳；Lean 的 `change` 核对原目标，编译和公理审计全部通过才报告 `proved`。

最终证明直接验证原 Gaussian 多项式语义，不把符号搜索中的形式分母非零作为新假设。首例保留任意域 K 中全部 q、z，包括零值及单位根；不含 `sorryAx`。这属于逐次结果验证，并非将 q-Gosper 算法本身形式化。

## 直接 q-Gosper 分支

[direct.py](direct.py) 处理不依赖上限参数的求和项：从原项计算移位比，由 q-Gosper 求原差分比 R；再从原 Gaussian 原子及其邻接指标构造候选表示，计算系数是否为多项式。得到 G 后，在原定义上验证 F(k)=G(k+1)−G(k)，求和并验证实际端点等于目标。

目前表示转换只支持 Gaussian 下指标移位 0/1，以及现有 Pascal 改写能闭合的表达式。这是 Lean 表示与验证能力限制，不是 q-Gosper 的分母或次数搜索范围；表示失败报告 `domain_unresolved`，不报告原差分不存在。没有输入证书或预填端点答案。[集成检查](generated/direct_tests.json)涵盖改名、三倍权重、篡改原差分及错误目标端点；三倍权重必须自动产生系数 3。

## 当前范围与缺口

目标引导分支前端处理range(n+1)单和、Gaussian(q,n,k)权重、Pochhammer、有限q幂乘积原子及因子形如x-a*q^i的显式range乘积，允许等式反向及有限合取；Gaussian底数与上限须为变量。目标可以是已支持算术表达式，能提取不保证递推证明成功。符号移位须可有理化；证明生成只回译能写成多项式乘F(n,k)或F(n,k−1)的证书，允许受支撑约束的q^(n-k)，并受现有公共改写规则限制。

直接分支新增 Gaussian 上指标随求和变量变化、Gaussian 目标和等式反向；含显式分母、奇偶分段、其他支撑及高阶递推仍待扩展；未闭合时明确报告失败，不能解释为恒等式不可证明。没有按题目 ID 选取证明内容。通用规则对所有符合结构的输入执行同一流程，已通过改名与平方参数、正权重两个变体检查，见[集成结果](generated/lean_tests.json)。

`--problem examples/finite_q_binomial.formula.json` 仍是独立的符号实验入口，只能报告 `constructed_not_proved`，不计训练覆盖。当前 CAS 后端是基于 QSUM 算法步骤的 Python/SymPy 实现，未运行 Mathematica 或 REDUCE。全部开发和输出位于 benchmark 之外，只使用 train。
