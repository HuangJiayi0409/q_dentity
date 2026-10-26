**两种方法的固定 9＋30 题样本诊断（2026-10-21）**

本轮按已固定的 39 个题目—方法配对实际运行，并检查公式、定义与失败产物。结论是：当前最普遍的缺口在“源公式如何进入方法及如何回到原题”，核心搜索也有规模限制，但不能用扩大搜索阶数解决全部失败。后续开发应以表达式类、求和域和证书类型为单位，题号只用于验收。

本轮未修改生产求解器；诊断性改写放在独立目录，未计作实现修复。所有任务已结束，无 API 调用，未读取 Test。结果不与历史成功择优合并。

**运行范围与结果**

| 方法 | 固定样本 | 完整原题通过 | 本样本通过比例 |
| --- | ---: | ---: | ---: |
| 有限差分与望远镜求值 | 9 | 2 | 22.22% |
| 递推关系与唯一性 | 30 | 2 | 6.67% |
| 合计 | 39 | 4 | 10.26% |

通过题为 T02（AP-3.3.9）、T08（GR2-II-34）、R19（FINITE-Q-BINOMIAL）、R20（KAC-CHEUNG-4.4）。四份证明均通过原声明 Lean 检查及统一证据重新接收。这不是“新增 4 道 Train 成功”的统计，也不是全 Train 成功率。

样本来自此前的结构候选池：望远镜优先候选 9 道全取；递推从 165 道优先候选中以种子 `15068132103473328074` 等概率、不放回抽 30 道，未分层或重抽。优先候选不等于已经认证满足当前算法输入契约。例如根和、系数投影、组合定义序列，都需要额外的语义桥才能使用递推。原取样记录中的“尚未测试”是取样时的历史状态，本报告记录后续测试。

执行使用原生产入口、指定方法、公共预处理的 `structured` 视图，绕过分类器，没有跨方法尝试。8 个本地工作进程；每题总预算 900 秒、单次尝试 600 秒、分析 120 秒、符号计算 240 秒，最大阶数 4、次数 5、未知数预算 10000；子后端仍有额外限制。39/39 公共预处理均命中已有缓存，不能作为冷启动耗时。基线整轮墙钟约 288.899 秒（4 分 49 秒），逐题耗时之和 1401.643 秒（23 分 22 秒），后者不是 CPU 时间。补充诊断不包含在这两个基线时间内。

422 份运行源码、相关定义、选中原题和输入资料在运行前冻结，运行后哈希无变化。证据：[运行清单](../generated/two_method_diagnosis_20261021/manifest.json)、[基线汇总](../generated/two_method_diagnosis_20261021/summary.json)、[原题接收审计](../generated/two_method_diagnosis_20261021/final_audit.json)。

**按首次阻塞位置划分**

每题只计最先阻止本轮继续的一项；后续仍可能有其他问题。这里的细分依据下层日志，不直接把顶层 `unproved` 当数学结论。

| 首次阻塞／成功 | 望远镜 | 递推 | 合计 | 能得出的结论 |
| --- | ---: | ---: | ---: | --- |
| P1 表达式导出失败 | 3 | 17 | 20 | 尚未得到核心算法可用的输入 |
| 导出后没有可执行前端候选 | 3 | 6 | 9 | 分段、包装、和的布局或整数指标等不被接收 |
| 进入构造后移位正规化失败 | 0 | 3 | 3 | 当前正规形式不够，局部诊断已找到可有理化表示 |
| 符号计算资源限制 | 0 | 2 | 2 | 一题符号超时，一题多重精确线性代数规模受限 |
| 已构造证书但 Lean 原题重建失败 | 1 | 0 | 1 | 核心产出存在，证明出口尚未闭合 |
| 完整原题通过 | 2 | 2 | 4 | 原声明、依赖及公理核验通过 |

35 道失败中，32 道首先停在表示接入或移位正规化。**这不意味着补几条解析规则就能证明这 32 道题。** 其中既有普通表达式布局问题，也有需要从组合对象、系数或根和构造递推的数学接口问题。基线共 10 题实际尝试证书构造，其中 5 题产生证书，4 题完成原题证明。

**补充实验提供的直接证据**

1. 在 8 个包装定义／布局案例上使用已有 `expanded` 视图，只检查准入。T07 与 R24 能进入候选；R15 继续被合取目标阻塞，R09、R16、R21、R25 继续被前因子内部的求和阻塞，R30 继续被 `n/2` 上界阻塞。可见“全部展开”不是完整接入方案。
2. 对准入的 T07、R24 再用同样预算完整运行。T07 在符号工作进程超时，总耗时 273.027 秒；R24 在移位正规化报 `nonlinear shift exponent`，总耗时 33.208 秒。两题都未证明，未替换原基线。
3. R10 把 `(-q^(n+1))^k` 按整数指数拆成 `(-1)^k*q^(k*(n+1))`，R12 利用原假设 `t²=q` 选择 t 为共同基，R26 将共同乘积中的 `a^(k+1)+a^(-k)` 分为两个分量，均可得到外层指标及求和指标的有理移位商。R26 两分量还精确重组为原项，符号残差为零。这些仅是局部表示诊断，未完成递推、初值、支撑和 Lean 原域运输。
4. T09 已构造双基原函数。原证明生成器未直接取出 `regular q` 中的非零事实，逆元正规式也不统一。独立副本显式提取原有非零假设并加入乘积逆元／幂逆元化简后，基础非零错误消失，两处等式被化简关闭；但固定追加的 `ring` 因目标已关闭报错，局部 `field_simp` 仍超过 100 万 heartbeats。没有提高预算，整题仍失败。这支持修复通用证明生成策略，不支持宣称该题已经解决。

证据：[展开准入](../generated/two_method_diagnosis_20261021/expanded_probes/summary.json)、[展开后完整运行](../generated/two_method_diagnosis_20261021/expanded_full/summary.json)、[三个正规化实验](../generated/two_method_diagnosis_20261021/normalization_probes.json)、[双基重建诊断](../generated/two_method_diagnosis_20261021/reconstruction_probe/result.json)。

R13 检查中一度怀疑括号造成源公式错误，随后按实际 Lean 表达式核验，`q=1/2,n=2` 的右端为 `13/8`，疑点已排除。失败的反例尝试保留为过程记录，不构成原题错误证据，也不构成一般恒等式证明。[核查记录](../generated/two_method_diagnosis_20261021/source_semantics/summary.json)。

**方法范围应怎样据此落实**

望远镜法至少要分清三种可实现子类：

- 单基超几何项的原函数构造：给出被加数、离散指标、参数与求和域；在明确的有理移位域寻找证书，再单独验证目标和端点。目标含 `ite` 不应先阻止被加数的局部构造。
- 前缀乘积的有限差分：T04 具有 `P(k)=∏_{j<k}U(j)`，认证 `V(k)=1-U(k)` 后，`V(k)P(k)=P(k)-P(k+1)`。这个类别允许任意序列参数；不要求完整被加数的相邻项比有理。应提供通用前缀乘积规则及局部因子等式证明。
- 多基／整数双边和：当前 T08 已证明的是受限双基分支；T05 涉及四个基参数、组合基和负指标，不能称为当前双基入口仅差一个函数名。需要显式声明基关系、整数移位规则与双端点出口，再实现相应算法。

递推法也不能等同于单重 q-Zeilberger：

- 单基有限超几何和以及有限线性组合：共享明确的移位域，通过创造性伸缩构造递推；这里最先补表示层。q 与 q² 是相关基，不能按名称说成两个独立基；原假设 t²=q 也应进入基关系环境。
- 固定维数多重和：既要多方向证书，也要实际求和域各个边界的通量与初值。R11 已调用多重核心，不能说当前程序完全没有多重算法；当前原题出口仍受二维单纯形、一阶及核形式限制。
- 带已认证递推的序列及其闭包：递归定义、有限和定义、组合对象、系数投影和根和需要不同的证明桥，最后才能共享“共同递推＋初值＋唯一性”。例如 aqG 已有递归定义；aqF 是组合枚举定义，必须先证明对象分解产生递推。

一个样本需要系数提取或组合分解作为前置步骤，不表示其他方法已经能够自动完成它。当前轮只检测指定的两个方法，未运行其他十种方法，也没有根据失败将题目自动交给其他入口。

**改进单元与优先顺序**

建议优先实施 U1、U3、U4：U1 消除重复的表示屏障，U3 已有三个局部可行证据，U4 针对已成功生成证书的最后一段出口。若只选最短的完整证明闭环，优先检查 U4；若选对更多结构有共同收益的基础工程，优先 U1＋U3。以上是工程判断，不是承诺修后通过数量。

| 单元 | 通用改动及位置 | 样本证据 | 验收应证明什么 |
| --- | --- | --- | --- |
| U1：语义保真的表达式接入 | 对接公共预处理已有表达式、定义与运输证明；为有限和建立线性组合表示，支持 `A(n)*Σf`、双方多项和；按需要展开非递归包装；见 `p1/lean/Extract.lean`、`source_ir.py`、`general_summation.py`、`workflow/worker.py` | 20 个导出失败与 9 个无候选含多种接入缺口；展开实验进一步定位布局问题 | 原式与内部表示在 Lean 中相等；不依赖题号；乘法交换、变量改名、等价包装后的输入保持相同行为。未知函数仍不得凭名字接收 |
| U2：逻辑及分支目标 | 拆分并重组 And、ite、奇偶与初值；将局部证书构造和目标值核验分开 | T03、T06、R08、R15、R23 等 | 所有原分支都闭合，保留 n=0；不能只证明其中一个等式或添加原题没有的假设 |
| U3：移位前正规化 | 有限分量分配、整数幂的符号／乘积展开、携带原假设的共同基表示；复用既有联合伸缩与 Ore 公左倍式 | R10、R12、R26 局部成功；R24 展开后仍卡幂表达式 | 输出有理移位商及原域运输证据；精确验证分量和；不把整数幂规则扩张到任意复指数，不遗漏参数零值 |
| U4：双基证书原题出口 | 从结构假设显式提取非零条件，规范逆元与幂；使用可组合战术和局部有界分母证明，避免每个小目标反复全局 `simp at *; aesop`；见 `bibasic_pipeline.py` | T08 成功、T09 已有证书但失败 | 完整原声明、端点与公理审计通过；变量改名、分母因子重排、端点为零等结构变体仍正确 |
| U5：前缀乘积及多基差分子类 | 先建立任意序列的前缀乘积差分规则；独立声明更多基、signed Pochhammer 与双边端点子类，不能把两者混成单基扩容 | T04、T05 | 每条子类有输入范围和可核验证书；超出范围时明确拒绝或未知，而非承诺任意多基可解 |
| U6：求和域与支撑 | Icc 到 range 的认证重索引、整数零延拓、同余类／floor 上界、三角约束、自然数截断减法 | R06、R08、R13、R14、R17、R18、R22、R28、R30 等 | 移动端点、分支接缝和边界项完整；不得把 Nat 减法或 Int.toNat 当普通代数减法 |
| U7：序列关系接口 | 通用“对象定义→认证递推与初值”接口，分别接递归定义、有限和、组合分解、系数投影、Vieta 根和；再作闭包 | R02、R03、R04、R05、R07、R13、R23、R27、R29 等 | 关系来自原定义且可核验；不同对象桥独立验收。仅把函数当不透明符号送入求解器并不能获得递推 |
| U8：规模与诊断 | 记录正规化、建矩阵、消元、验残差各阶段耗时；披露实际未知数和矩阵限额；改善精确线性代数与后端可用性；传播真实失败类型 | R01、R11；补充 T07 超时 | 所有加速结果仍精确回代；超时、搜索用尽、证明出口失败分开记录；支持断点诊断而非盲增总时限 |

U8 的明确实现证据：`multisum.py` 将模板未知数限制为 `min(max_unknowns,256)`，精确系数复杂度默认限额 20000；R11 在化简后仍过限，而当前环境缺少可选 `python-flint`。仓库已存在该精确运算后端接口，不能把本轮现象写成“尚无多重算法”，也不能声称仅安装依赖就会完成整题。R01 的现有日志只定位到符号进程超时，尚不足以判定主要时间究竟花在求分母、建立方程还是消元。

状态记录也需要修正：表示异常在候选记录中有时被记成 `core_domain=rejected`，但实际没有验证数学域条件；符号超时被压成 `construction_failed`，多重 `resource_exhausted` 最终又表现为 `unproved`。至少应分别保留表示缺口、准入未知、声明域外、资源耗尽、有限搜索用尽和原题义务未闭合。此次诊断保留原结果，另加首次阻塞分类，没有回写旧成绩。

这些单元之间存在依赖：例如先打开一个包装定义，可能随后遇到奇偶域，再遇到搜索规模或 Lean 端点问题。应逐层记录达到哪一步，不能将“准入增加几题”报告成“证明增加几题”。表中题目集合存在重叠，不能相加作为预计收益。

**39 题逐项记录**

T 为望远镜样本，R 为递推样本；保持原取样顺序。每题链接原公式及本次原始报告。首次阻塞是实跑证据；“后续义务”包含源结构审查的判断，不表示已经运行到该阶段。

| 样本 | 原题与公式 | 首次阻塞／成功 | 结构与改进单元 | 后续义务／补充观察 |
| --- | --- | --- | --- | --- |
| T01 | [FQI-BAILEY-UNIT](../../benchmark/formulas/train/FQI-BAILEY-UNIT.md)<br>一般参数单位 Bailey 对 | [Converter 不接收 unitBailey](../generated/two_method_diagnosis_20261021/tasks/telescoping/FQI-BAILEY-UNIT/attempts/8c808ba049f444e98991064dc2f557c5/report.json) | Bailey 核与分段单位序列；U1,U2 | 展开定义并分离 n=0 分支；支撑、分母及端点仍须证明 |
| T02 | [FQI-SRC-AP-3.3.9](../../benchmark/formulas/train/FQI-SRC-AP-3.3.9.md)<br>Gaussian 加权 hockey-stick 求和 | [direct_q_gosper 完整原题通过](../generated/two_method_diagnosis_20261021/tasks/telescoping/FQI-SRC-AP-3.3.9/attempts/ad9847eb20ed4960931da981f130b419/report.json) | 单基 Gaussian 加权有限和；regression | 保留为直接望远镜回归 |
| T03 | [FQI-SRC-AQ-3.37](../../benchmark/formulas/train/FQI-SRC-AQ-3.37.md)<br>a=q 的单位 Bailey 对 | [Converter 不接收目标中的 ite](../generated/two_method_diagnosis_20261021/tasks/telescoping/FQI-SRC-AQ-3.37/attempts/ecc19e99e5cf4b93b2ac31ff2145eb65/report.json) | 单基有限和等于分段常数 δ(n,0)；U1,U2 | 求原函数与核验分段目标分离；不能据 ite 判核心域不适用 |
| T04 | [FQI-SRC-GR2-11.6.5-p0](../../benchmark/formulas/train/FQI-SRC-GR2-11.6.5-p0.md)<br>Macdonald 有限乘积望远镜求和 | [P1 Export 不接收任意函数应用 a k](../generated/two_method_diagnosis_20261021/tasks/telescoping/FQI-SRC-GR2-11.6.5-p0/attempts/721ab9b1d8284e95881f12d1ddc5926c/report.json) | 任意序列因子及其前缀乘积；U5 | 认证 V(k)=1-U(k)，再应用前缀乘积差分；不要求原被加数有有理移位商 |
| T05 | [FQI-SRC-GR2-11.6.6-p0](../../benchmark/formulas/train/FQI-SRC-GR2-11.6.6-p0.md)<br>多底数有限双边求和 | [P1 Export 不接收 pochListInt](../generated/two_method_diagnosis_20261021/tasks/telescoping/FQI-SRC-GR2-11.6.6-p0/attempts/8a036ba274214817a3bc67cdefb73291/report.json) | 整数双边区间、四个基参数及乘法组合基；U5,U6 | 负长度 Pochhammer、基关系、双端点与原域非零条件；超出现双基后端语法 |
| T06 | [FQI-SRC-GR2-2.3.4](../../benchmark/formulas/train/FQI-SRC-GR2-2.3.4.md)<br>终止 very-well-poised 4φ3 消去 | [Converter 不接收目标中的 ite](../generated/two_method_diagnosis_20261021/tasks/telescoping/FQI-SRC-GR2-2.3.4/attempts/078d553ee1154f689352ee22eb1326f2/report.json) | 终止 very-well-poised 求和及分段零值；U1,U2 | 外层零值分支、终止支撑及分母需独立核验 |
| T07 | [FQI-SRC-GR2-2.Ex5](../../benchmark/formulas/train/FQI-SRC-GR2-2.Ex5.md)<br>不定 very-well-poised 有限和 | [P1 Export 不接收 wellPoisedRaw](../generated/two_method_diagnosis_20261021/tasks/telescoping/FQI-SRC-GR2-2.Ex5/attempts/a59e8ad1aad348b393544a393abbcbce/report.json) | 包装定义下的单基有限超几何和；U1,U8 | expanded 可准入；后续实跑符号工作进程超时，并未产生完整证明 |
| T08 | [FQI-SRC-GR2-II-34](../../benchmark/formulas/train/FQI-SRC-GR2-II-34.md)<br>Gosper 不定双底数有限求和 | [bibasic_gosper 完整原题通过](../generated/two_method_diagnosis_20261021/tasks/telescoping/FQI-SRC-GR2-II-34/attempts/b56e4e0c95e8433481f862ce98816422/report.json) | 双基、被加数与外层截断参数无关；regression | 保留为双基证书与端点回归 |
| T09 | [FQI-SRC-GR2-II-35](../../benchmark/formulas/train/FQI-SRC-GR2-II-35.md)<br>Gosper 双底数求和扩展 | [双基证书已构造，原题 Lean 重建失败](../generated/two_method_diagnosis_20261021/tasks/telescoping/FQI-SRC-GR2-II-35/attempts/19074878ab3e43e9a83fe5b49fa471b1/report.json) | 双基原函数与原式间的逆元、分母和端点运输；U4 | 显式提取 regular 的非零事实；统一逆元；局部 field_simp 超 heartbeats |

| 样本 | 原题与公式 | 首次阻塞／成功 | 结构与改进单元 | 后续义务／补充观察 |
| --- | --- | --- | --- | --- |
| R01 | [FQI-SRC-GR2-2.Ex14i](../../benchmark/formulas/train/FQI-SRC-GR2-2.Ex14i.md)<br>Bailey 的终止 4φ3 求和 | [general_q_zeilberger 符号工作进程超时](../generated/two_method_diagnosis_20261021/tasks/recurrence/FQI-SRC-GR2-2.Ex14i/attempts/e219cffe8d8a4fcc82e91aca8d5a9530/report.json) | 单基终止 4φ3 求值；U8 | 补阶段耗时及矩阵规模记录后优化；不能从超时判断不存在证书 |
| R02 | [FQI-SRC-AQ-8.32](../../benchmark/formulas/train/FQI-SRC-AQ-8.32.md)<br>硬六角 F 多项式递推 | [P1 Export 不接收 aqF](../generated/two_method_diagnosis_20261021/tasks/recurrence/FQI-SRC-AQ-8.32/attempts/33f7b589fefc469e923e45298d2219f0/report.json) | 无相邻占位集合的加权枚举多项式；U7 | 从有限对象分解认证递推；aqF 并非已有递推定义，不能只加白名单 |
| R03 | [FQI-SRC-AQ-9.17](../../benchmark/formulas/train/FQI-SRC-AQ-9.17.md)<br>G 多项式的有限系数展开（显式修订移位） | [P1 Export 不接收 aqG](../generated/two_method_diagnosis_20261021/tasks/recurrence/FQI-SRC-AQ-9.17/attempts/e818af7f05d944d8b46d7a384db75609/report.json) | 已有三阶递归定义与受线性约束的有限双和；U6,U7 | 提取定义递推和全部初值，另一侧构造共同递推及支撑 |
| R04 | [FQI-SRC-KAC-CHEUNG-26.22](../../benchmark/formulas/train/FQI-SRC-KAC-CHEUNG-26.22.md)<br>相同伸缩参数下的根和递推 | [P1 Export 不接收 quantumRootSum](../generated/two_method_diagnosis_20261021/tasks/recurrence/FQI-SRC-KAC-CHEUNG-26.22/attempts/d4838a63264e47ae89b7043a311fb01c/report.json) | 满足缩放差分关系的多项式之根和；U7 | 须有次数、Vieta 系数运输及根和递推桥；不是直接 q-超几何被加数 |
| R05 | [FQI-SRC-SILLS-4.Mod8](../../benchmark/formulas/train/FQI-SRC-SILLS-4.Mod8.md)<br>有限 Ramanujan–Slater Mod 8 恒等式 | [P1 Export 不接收 sillsP](../generated/two_method_diagnosis_20261021/tasks/recurrence/FQI-SRC-SILLS-4.Mod8/attempts/64fd233feaaf4e62b24054e76f78e587/report.json) | 定义序列与交错有限 Gaussian 和；U6,U7 | 序列定义、奇偶支撑及相同递推/初值的认证 |
| R06 | [FQI-SRC-SILLS-4.26-corrected](../../benchmark/formulas/train/FQI-SRC-SILLS-4.26-corrected.md)<br>偶数 E 多项式的倒数对偶 | [P1 Export 不接收 schurE q⁻¹ (2*m)](../generated/two_method_diagnosis_20261021/tasks/recurrence/FQI-SRC-SILLS-4.26-corrected/attempts/fc7504eaf6e944df8b687fae38fcda7b/report.json) | 偶指标序列、倒数基、整数区间与合取目标；U1,U2,U6,U7 | 基变换、整数支撑、分支条件及子序列递推 |
| R07 | [FQI-SRC-AP-3.E12a](../../benchmark/formulas/train/FQI-SRC-AP-3.E12a.md)<br>Schur 多项式倍指标恒等式 | [P1 Export 不接收 schurDInt](../generated/two_method_diagnosis_20261021/tasks/recurrence/FQI-SRC-AP-3.E12a/attempts/ab39e0473cb24129a417eb1b84490b38/report.json) | 倍指标序列与含 n-1-j 的卷积；U6,U7 | 整数零延拓、卷积及序列递推闭包；不能直接忽略负指标 |
| R08 | [FQI-SRC-GR2-II-19](../../benchmark/formulas/train/FQI-SRC-GR2-II-19.md)<br>终止 q-Whipple 的有限乘积形式 | [Converter 不接收 HMod.hMod](../generated/two_method_diagnosis_20261021/tasks/recurrence/FQI-SRC-GR2-II-19/attempts/daca21ecb67944d5bea2d0d127ada1f9/report.json) | 奇偶分支和 ceil(n/2) 长度乘积；U2,U6 | n=2m 与 n=2m+1 子序列分别表示并合并；核验全部初值 |
| R09 | [FQI-SRC-GR2-III-27](../../benchmark/formulas/train/FQI-SRC-GR2-III-27.md)<br>近良配 7φ6 到 12φ11 变换 | [Converter 不接收前因子内部的 Finset.sum](../generated/two_method_diagnosis_20261021/tasks/recurrence/FQI-SRC-GR2-III-27/attempts/fe2f75b90d224b7faae8c6586863896c/report.json) | 乘积前因子乘有限和的两和变换；U1 | 双方线性求和表示、前因子随 n 移位及共同递推；已有联合求解器可复用 |
| R10 | [FQI-SRC-GR2-2.3.2](../../benchmark/formulas/train/FQI-SRC-GR2-2.3.2.md)<br>终止 Bailey–Daum 的有限积求值 | [representation_gap: nonlinear shift exponent](../generated/two_method_diagnosis_20261021/tasks/recurrence/FQI-SRC-GR2-2.3.2/attempts/d4ac6d1e77e548028e2ed3f938dd1896/report.json) | 带负号的移动底数 (-q^(n+1))^k；U3,U2 | 局部拆幂后两个方向移位商均有理；目标奇偶/取整及完整证明仍未完成 |
| R11 | [FQI-SRC-GR2-10.Ex18](../../benchmark/formulas/train/FQI-SRC-GR2-10.Ex18.md)<br>终止 q-Kampé de Fériet 双重求和 | [multisum 精确系数复杂度预算耗尽，python-flint 不可用](../generated/two_method_diagnosis_20261021/tasks/recurrence/FQI-SRC-GR2-10.Ex18/attempts/e8873e032aa0481cbd3ca6a922862d19/report.json) | 单基二维单纯形有限双和；U8 | 已进入多重求解；后续还须符合二维一阶出口的核与原域条件 |
| R12 | [FQI-SRC-SILLS-2.Lem2.53](../../benchmark/formulas/train/FQI-SRC-SILLS-2.Lem2.53.md)<br>半整数幂 Bailey 有限和 | [representation_gap: not a single-base rational shift](../generated/two_method_diagnosis_20261021/tasks/recurrence/FQI-SRC-SILLS-2.Lem2.53/attempts/7c3ca40124234dac848d598ea81ebb33/report.json) | 含 t^(2k²+k)，原假设 t²=q；U3 | 以 t 为基统一后移位商有理；仍须原域等式运输及允许参数特化 |
| R13 | [FQI-SRC-SILLS-4.55](../../benchmark/formulas/train/FQI-SRC-SILLS-4.55.md)<br>Borwein B 多项式的正向有限和 | [P1 Export 不接收 borweinB](../generated/two_method_diagnosis_20261021/tasks/recurrence/FQI-SRC-SILLS-4.55/attempts/5d4b62bc00fd47f3bd1e48bd6db8dc3f/report.json) | 模 3 系数投影、floor((n-1)/3) 有限和与初值合取；U2,U6,U7 | 系数投影转耦合递推及分支支撑；原 RHS 的疑似排版问题已排除 |
| R14 | [FQI-SRC-SILLS-2.Ex2c](../../benchmark/formulas/train/FQI-SRC-SILLS-2.Ex2c.md)<br>三步长 Bailey 有限和 | [Converter 不接收 sillsAlpha](../generated/two_method_diagnosis_20261021/tasks/recurrence/FQI-SRC-SILLS-2.Ex2c/attempts/2150d904cf2a4b45b877aceee30ac5e8/report.json) | 按三步长支撑定义的 Bailey 被加数；U2,U6 | 展开分段序列并作同余类重索引，保持零延拓语义 |
| R15 | [FQI-SRC-GR2-2.Ex11](../../benchmark/formulas/train/FQI-SRC-GR2-2.Ex11.md)<br>Askey–Wilson 参数交换与奇偶关系 | [P1 Export 不接收 askeyWilson](../generated/two_method_diagnosis_20261021/tasks/recurrence/FQI-SRC-GR2-2.Ex11/attempts/0e83c3c311324b26a1f96919b3997bdf/report.json) | 超几何定义的多项式对称性与奇偶关系合取；U1,U2,U7 | expanded 后仍因 And 不是 Eq 被拒；拆子目标后证明完整合取 |
| R16 | [FQI-SRC-GR2-7.4.14](../../benchmark/formulas/train/FQI-SRC-GR2-7.4.14.md)<br>连续 q-超球多项式的终止 4φ3 表示 | [P1 Export 不接收 ultraspherical](../generated/two_method_diagnosis_20261021/tasks/recurrence/FQI-SRC-GR2-7.4.14/attempts/234a92ba320d4b5e9135536c4819e426/report.json) | 多项式有限和与前因子乘 4φ3；U1,U7 | expanded 后仍被内部 Finset.sum 阻塞；两和及参数变换运输 |
| R17 | [FQI-SRC-SILLS-4.19](../../benchmark/formulas/train/FQI-SRC-SILLS-4.19.md)<br>E 多项式的 q-三项式展开 | [P1 Export 不接收 schurE](../generated/two_method_diagnosis_20261021/tasks/recurrence/FQI-SRC-SILLS-4.19/attempts/88c29def9a6242b2bebc913b3f0f2b57/report.json) | 序列与整数区间上的 q-三项式展开；U6,U7 | sillsC 定义内含和、整数转自然数与零支撑；不仅是名字导出 |
| R18 | [FQI-SRC-SILLS-2.Ex2e](../../benchmark/formulas/train/FQI-SRC-SILLS-2.Ex2e.md)<br>偶指标 Bailey 有限和 II | [Converter 不接收 sillsAlpha](../generated/two_method_diagnosis_20261021/tasks/recurrence/FQI-SRC-SILLS-2.Ex2e/attempts/c989e90be5ee49838d600839b8e007de/report.json) | 偶指标支撑的 Bailey 有限和；U2,U6 | 分支展开、偶指标重索引及 floor 上界 |
| R19 | [FQI-FINITE-Q-BINOMIAL](../../benchmark/formulas/train/FQI-FINITE-Q-BINOMIAL.md)<br>有限 q-二项式定理 | [target_first_order 完整原题通过](../generated/two_method_diagnosis_20261021/tasks/recurrence/FQI-FINITE-Q-BINOMIAL/attempts/03a2bf4b9b4249de8d693c64821afb07/report.json) | 单基 Gaussian 权重有限和的一阶递推；regression | 保留原题、初值及端点回归 |
| R20 | [FQI-SRC-KAC-CHEUNG-4.4](../../benchmark/formulas/train/FQI-SRC-KAC-CHEUNG-4.4.md)<br>单项式的有限 q 幂展开 | [target_first_order 完整原题通过](../generated/two_method_diagnosis_20261021/tasks/recurrence/FQI-SRC-KAC-CHEUNG-4.4/attempts/025bc82bbbb247e2b3cf2ff46c2f67a2/report.json) | 单项式的有限 q 幂展开；regression | 保留原题及参数特殊值回归 |
| R21 | [FQI-SRC-GR2-III-25](../../benchmark/formulas/train/FQI-SRC-GR2-III-25.md)<br>近良配 5φ4 到 12φ11 变换 | [Converter 不接收前因子内部的 Finset.sum](../generated/two_method_diagnosis_20261021/tasks/recurrence/FQI-SRC-GR2-III-25/attempts/23067d340339467d85b064631dd6088b/report.json) | 乘积前因子乘有限和的两和变换；U1 | expanded 仍同样拒绝；将线性组合送入现有共同递推构造器 |
| R22 | [FQI-SRC-SILLS-4.18](../../benchmark/formulas/train/FQI-SRC-SILLS-4.18.md)<br>D 多项式的 q-三项式展开 | [P1 Export 不接收 schurD](../generated/two_method_diagnosis_20261021/tasks/recurrence/FQI-SRC-SILLS-4.18/attempts/2000dc7af8d44af189f88e298bd56f46/report.json) | 序列与整数区间上的 q-三项式展开；U6,U7 | 隐藏多重和、整数支撑及已知序列的递推闭包 |
| R23 | [FQI-SRC-AQ-2.23](../../benchmark/formulas/train/FQI-SRC-AQ-2.23.md)<br>连续 q-Hermite 多项式递推 | [P1 Export 不接收 aqHermite](../generated/two_method_diagnosis_20261021/tasks/recurrence/FQI-SRC-AQ-2.23/attempts/0ead2c4d817b42ceb31060b34a073532/report.json) | 显式 Gaussian 和定义、多项式递推及初值合取；U1,U2,U7 | 展开定义并接收多项序列关系，最后合并初值目标 |
| R24 | [FQI-SRC-GR2-3.10.5](../../benchmark/formulas/train/FQI-SRC-GR2-3.10.5.md)<br>有限双底数求和（一） | [P1 Export 不接收 bibasicPhi](../generated/two_method_diagnosis_20261021/tasks/recurrence/FQI-SRC-GR2-3.10.5/attempts/0fd90a80f6b24635ae39ef8ba4a5f87d/report.json) | 底数 q² 和 q 的有限和，非两个独立基；U1,U3 | expanded 可准入，实跑仍报 nonlinear shift exponent；尚未证明 |
| R25 | [FQI-SRC-GR2-3.8.14](../../benchmark/formulas/train/FQI-SRC-GR2-3.8.14.md)<br>有限双底数和到二次 10φ9 | [P1 Export 不接收 wellPoisedRaw](../generated/two_method_diagnosis_20261021/tasks/recurrence/FQI-SRC-GR2-3.8.14/attempts/f32e608a09524c8a82681c66671511a7/report.json) | 相关基的两和变换及乘积前因子；U1,U3 | expanded 仍在前因子内部的 Finset.sum 被拒；共同递推与参数移动 |
| R26 | [FQI-SRC-SILLS-2.Ex7a-corrected](../../benchmark/formulas/train/FQI-SRC-SILLS-2.Ex7a-corrected.md)<br>关于q的参数 Bailey 有限和 | [representation_gap: not a single-base rational shift](../generated/two_method_diagnosis_20261021/tasks/recurrence/FQI-SRC-SILLS-2.Ex7a-corrected/attempts/4b57a5890e4c4142a8226389accb84f3/report.json) | 共同乘积内含 a^(k+1)+a^(-k) 的两个分量；U3 | 分配律拆成两个超几何项后均可有理化；共同递推及 Lean 分配律运输仍待做 |
| R27 | [FQI-SRC-SILLS-4.52](../../benchmark/formulas/train/FQI-SRC-SILLS-4.52.md)<br>Borwein B 多项式的 Gaussian 展开 | [P1 Export 不接收 borweinB](../generated/two_method_diagnosis_20261021/tasks/recurrence/FQI-SRC-SILLS-4.52/attempts/8c729b83614649ed924950acadd48f41/report.json) | 模 3 系数投影与整数 Gaussian 展开；U6,U7 | 系数递推、整数区间与 Gaussian 零延拓 |
| R28 | [FQI-SRC-GR2-5.Ex19i](../../benchmark/formulas/train/FQI-SRC-GR2-5.Ex19i.md)<br>Gaussian 立方的对称有限和 | [Converter 不接收 gaussianInt](../generated/two_method_diagnosis_20261021/tasks/recurrence/FQI-SRC-GR2-5.Ex19i/attempts/c74a3542482541cd9a0c451d014dbb05/report.json) | Icc[-n,n] 上的 Gaussian 立方和；U6 | 认证 k=j-n 重索引及自然数截断支撑，再送入单基核心 |
| R29 | [FQI-SRC-GR2-1.3.25](../../benchmark/formulas/train/FQI-SRC-GR2-1.3.25.md)<br>对称 q 指数的有限系数递推 | [P1 Export 不接收 PowerSeries.coeff](../generated/two_method_diagnosis_20261021/tasks/recurrence/FQI-SRC-GR2-1.3.25/attempts/b0fd92e696fd4447b05b7fa633a8f33a/report.json) | 幂级数缩放差分初值问题与有限系数公式；U7 | 从 hIVP 取系数形成递推，保留 u²=q 的关系及初值 |
| R30 | [FQI-SRC-GR2-11.Ex24ii](../../benchmark/formulas/train/FQI-SRC-GR2-11.Ex24ii.md)<br>底数 q² 的 12W11 到 10W9 变换 | [P1 Export 不接收 wellPoisedRaw](../generated/two_method_diagnosis_20261021/tasks/recurrence/FQI-SRC-GR2-11.Ex24ii/attempts/0ea1f86118d848e0a7fe907632276991/report.json) | 相关基 q² 的两和变换及 floor(n/2) 上界；U1,U2,U6 | expanded 后明确拒绝非整数仿射 range；需要按奇偶重索引 |

机器记录：[39 题诊断 CSV](../generated/two_method_diagnosis_20261021/per_sample_diagnosis.csv)、[诊断 JSON](../generated/two_method_diagnosis_20261021/diagnosis.json)、[基线逐题耗时](../generated/two_method_diagnosis_20261021/per_identity.csv)、[诊断证据复核](../generated/two_method_diagnosis_20261021/diagnosis_audit.json)。补充实验属于定向诊断，不是随机对照，也没有新增原题通过。`generated/two_method_diagnosis_20261021/audit.py` 可只读复核已保存证据，不重新提交求解任务。

**后续修复的统一验收口径**

保留本次固定样本及冻结基线。按上述结构单元修改生产实现后，在独立目录复测；记录每题是否通过“表示接收→准入→构造证书→支撑／边界／初值→原声明验收”。四道已有成功要保留，失败样本不替换，所有尝试和真实资源限制都保留。新增结构规则需用变量改名、等价布局、参数特殊值及边界变化检验；负例用于确认不会遗漏分支或分母条件。最终成功仍只计完整原声明通过，局部符号等式或目标中的一个子句不计成功。

本轮完成的是检测与定位，生产修复尚未开始。沿用的范围设计见[十二方法契约](method_scope_contracts_20261021.md)，此前实现审查见[实现审计](method_implementation_audit_20261021.md)。本报告补充当前版本在这 39 个样本上的动态证据，不替代数学完备性声明。
