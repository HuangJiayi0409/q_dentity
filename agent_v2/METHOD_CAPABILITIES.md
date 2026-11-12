# CAS 方法能力边界

本表对应第三阶段最终冻结源码与全新统一回归。注册能力与每次执行的实际结果分开记录；只有生产 LeanChecker 接受的候选才能进入 C，只有原 theorem 独立验收通过才是整题成功。阶段进度与冻结版本证据见 [PHASE3.md](PHASE3.md)。

L3 表示存在受控 Source → 实际数学构造 → 局部 Lean 的已验路线，不表示任意同族题目可解。L2 表示存在实际符号构造，入口可以是已接通的完整 Source 或显式 typed `core_request`，以各方法契约为准；它没有生产 Lean 证明出口。L0 表示该入口尚无新框架可执行的真实证书出口。以下“前→后”以第三阶段开始前为基线，未验方法保持原 L0/L2。

| 方法 ID | 方法族 | 第三阶段前→当前 | 版本 | 局部 Lean | `full_original` | 本阶段已验记录 |
| --- | --- | --- | --- | --- | --- | --- |
| telescoping | 差分／望远镜 | L3→L3 | 2.0 | 是 | true，限定结构族 | [最终验收卡](generated/phase3_20261112/final_validation_01/report_metadata/telescoping_acceptance_card.json) |
| recurrence | 递推关系与唯一性 | L3→L3 | 2.0 | 是 | true，本阶段补齐 | [最终验收卡](generated/phase3_20261112/final_validation_01/report_metadata/recurrence_acceptance_card.json) |
| coefficient | 系数展开与有限卷积 | L2→L3 | 2.0 | 是 | false | [最终验收卡](generated/phase3_20261112/final_validation_01/report_metadata/coefficient_acceptance_card.json) |
| interpolation | 插值、零点与有理函数主部 | L2→L3 | 2.0 | 是 | false | [最终验收卡](generated/phase3_20261112/final_validation_01/report_metadata/interpolation_acceptance_card.json) |
| determinant | 行列式结构证书 | L2→L3 | 2.0 | 是 | false | [最终验收卡](generated/phase3_20261112/final_validation_01/report_metadata/determinant_acceptance_card.json) |
| kernel_transform | 有限核变换与矩阵反演 | L2→L3 | 2.0 | 是 | false | [最终验收卡](generated/phase3_20261112/final_validation_01/report_metadata/kernel_transform_acceptance_card.json) |
| spectral | 有限谱正交 | L2→L2 | 1.0 | 否 | false | [最终停止卡](generated/phase3_20261112/final_validation_01/report_metadata/spectral_acceptance_card.json) |
| difference_ring | 嵌套和积的差分环 | L2→L3 | 2.0 | 是 | false | [最终验收卡](generated/phase3_20261112/final_validation_01/report_metadata/difference_ring_acceptance_card.json) |
| macmahon | MacMahon 有理 Ω 消元 | L2→L3 | 2.0 | 是 | false | [最终验收卡](generated/phase3_20261112/final_validation_01/report_metadata/macmahon_acceptance_card.json) |
| product | 有限乘积与指标等价 | L0→L2 | 2.0 | 否 | false | [最终验收卡](generated/phase3_20261112/final_validation_01/report_metadata/product_acceptance_card.json) |
| noncommutative | 非交换算子等式 | L0→L2 | 2.0 | 否 | false | [最终验收卡](generated/phase3_20261112/final_validation_01/report_metadata/noncommutative_acceptance_card.json) |
| combinatorial | 加权双射与符号反转对合 | L0→L2 | 2.0 | 否 | false | [最终验收卡](generated/phase3_20261112/final_validation_01/report_metadata/combinatorial_acceptance_card.json) |

当前注册合计 **8 个 L3、4 个 L2**。已有 **11 种方法接通真实 Train Source 路线**；谱方法的 L2 仍仅是旧显式核心请求能力，没有成功 Train Source 入口。最终统一源码的 475 项回归与逐方法复验已通过，详细证据见 [总体验收报告](PHASE3_VALIDATION.md)；谱方法缺口使第三阶段整体仍为部分完成。

已验 Source 入口均从完整冻结声明重建受控语法与上下文，以下文件名相对 `agent_v2/`。不按题号选择数学证明，也不从任意源文本接受自选导入或证明命令。

| 方法 | 实际 Source 入口／固定配置 | 当前可证范围与剩余工作 |
| --- | --- | --- |
| telescoping | `formal_frontend.analyze_source`／`gaussian_weighted_range_v1` | Gaussian 加权有限和的局部差分、条件连接及两个端点；限定族可完整验收。没有模型驱动的通用表示搜索。 |
| recurrence | `recurrence_frontend.analyze_source`／`gaussian_geometric_recurrence_v1` | q-Zeilberger 二阶递推、依赖局部证书的唯一性连接、原右端递推与两个初值；限定奇偶／Pochhammer 结构族已完整验收。其他算子不能自动获得该出口。 |
| coefficient | `coefficient_frontend.analyze_source`／`qbinomial_product_coefficients_v1` | 原 Pochhammer 的多项式求值桥及所有自然数指标的零次／后继系数关系，实际调用 `p2/run.py:construct`；Gaussian 系数公式和整题尚开放。 |
| interpolation | `interpolation_frontend.analyze_source`／`poch_tail_factor_interpolation_v1` | 原整数移位和全部 `j < n-k` 尾段因子；实际 `zero_certificate` 给出一次多项式的双节点证书，独立核对后由 Lean 验证。乘积、商式与原题尚开放。 |
| determinant | `determinant_frontend.analyze_source`／`carlitz_matrix_minor_v1` | 原任意维数矩阵中任意所选二阶子式；实际无除法 Berkowitz 结果经独立 Leibniz 核对和 Lean 验证。原维数未设为 2；整行列式及 `planePi` 恒等式尚开放。 |
| kernel_transform | `kernel_transform_frontend.analyze_source`／`bailey_triangular_kernel_v1` | 任意 CommRing、任意 N 的原三角求和转置；实际置换搜索、双向域与指标证书及独立检查。局部结果尚未连接原右端；显式矩阵逆／复合路线仍是非形式符号构造。 |
| spectral | 自动 Train Source 入口尚无；仅 `symbolic_methods.analyze_source` 的 core-request 契约 | `spectral/construct.py:construct` 仅支持固定大小 1–4 的显式矩阵分离器；任意 N 的原序列特征关系、边界、分母与范数均未桥接。原对角分支不适用现有 0/1 分离器，真实诊断失败；没有 Source 绑定的局部 Lean 证书。 |
| difference_ring | `difference_ring_frontend.analyze_source`／`pochhammer_evaluated_difference_v1` | `difference_ring/algebra.py:reduce_goal` 给出原 Pochhammer 步进关系的整数乘子；关系先由 Lean 从原 `hn` 和 `poch_succ` 推出，再证明所有原 `n≥1` 的末端增量。独立检查拒绝 QQ 分母；首项抽取／尾段参数移位及整题仍开放。 |
| macmahon | `macmahon_frontend.analyze_source`／`chebyshev_laurent_omega_v1` | `p1/core.py:compute` 实际分派至有理 Ω 核心；两因子 Laurent 和经正／严格负块核对、有限 fiber 和 regulator 代入后，由单态 Lean 验证形式分母与原系数。原三个 ultraspherical／商式／极限合取仍开放。一般 Ω 编码、参数特化与其他 Source 尚不支持。 |
| product | `product_frontend.analyze_source`／`pochhammer_residue_index_v1`，无 Lean profile | 原 Field、任意 `m>0,n≥0` 的 Pochhammer 剩余类乘积；实际 `product/index_construct.py` 搜索轴顺序，构造商余数双射并独立检查六条自然数规则和因子幂次。尚无 Lean 定义展开／乘积重排桥，`C=0`、原题义务保留。旧通用 standalone 入口仍为 L0。 |
| noncommutative | `noncommutative_frontend.analyze_source`／`polynomial_q_shift_words_v1`，无 Lean profile | 原任意 Field 与多项式 f；实际 `noncommutative/operator_construct.py` 从定义计算有序算子对任意 `c*x^d` 的作用，独立核对 M-before-X 配对和正规形。有限线性扩张仅记录为符号规则，尚无 Lean 桥；旧通用 standalone 仍为 L0。 |
| combinatorial | `combinatorial_frontend.analyze_source`／`qbinomial_ranked_choices_v1`，无 Lean profile | 原 Pochhammer 右端的固定秩子集↔子集↔布尔选择；实际 `combinatorial/choice_construct.py` 构造并检查泛型布尔逆映射、六条 rank 规则、符号权重及有限分配律。Gaussian↔固定秩权重桥 pending；未使用符号反转或不动点消去，无 Lean 证书，旧通用 standalone 仍 L0。 |

六种新 L3 方法当前都只有 `C=1`、`O={original}`、`links=[]`，`original_identity_proved=false`。上表的 `full_original=true` 仅适用于望远镜与递推各自登记的结构范围；不能解释为两方法可处理任意输入。MacMahon 使用原 `ℂ` 命题的固定空宇宙参数配置，旧方法仍保留多态检查；这不允许把任意原 Field 特化为具体域。

三个 D 方法的 Source L2 成功后停在 `incomplete / symbolic_translation_pending`，只扣一次真实动作费用；恢复不重跑 CAS，且没有可重验的 Lean 证书。显式拒绝该作用域返回正式候选或新义务，`C=0`、`O={original}`、`links=[]` 保持。

谱方法门为 `branch_stopped / passed=false`，证据检查通过不等于接入通过；该分支仍为 `C=0`、`O={original}`。其单分量核心负例只说明当前构造器限制，不是原题反例或新证明成绩。只要此缺口尚未另行验收解决，第三阶段整体仍是部分完成。

已实现的 standalone/core-request 执行，即使方法注册为 L3，本次执行能力仍记录为 L2，另列注册能力；禁止产生正式 `C_partial`／`O_res`。三个 D 方法的新入口仅接受 Source，不提供通用 `execute_request`；旧 `method-demo --method product`、`--method noncommutative` 和 `--method combinatorial` 实测仍返回 L0／`capability_unavailable`。`method-demo` 只演示符号构造，不创建形式化断点或报告原题成功。输入示例由 `agent_v2.symbolic_methods.example_request(method_id)` 生成。

矩阵方法共享 `finite_product_framework/workflow/matrix_symbolic.py` 的纯数学编解码与残差核对，并核验其来源。核变换新增纯仿射证书搜索；未恢复 `workflow.contracts`、`workflow.preprocessed` 或旧 Agent 控制器。共享基础引理／检查器不被计作其他方法求解核心的调用。

底层求解器与方法族是不同层次。`core-demo` 原有 q-Gosper、q-Zeilberger 和 parameterized q-Gosper 入口继续保留；同族其他底层 modes 不因本表登记而自动获得新框架适配或 Lean 桥。
