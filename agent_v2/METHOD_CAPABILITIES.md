# CAS 方法能力边界

注册表描述可执行范围，不构成证明证据。L3 的局部证明仍需生产 LeanChecker 验证；L2 仅执行显式 typed core_request，没有自动 Train 导出器；L0 不执行数学构造。

| ID | 方法族 | 等级 | 实际入口／检查配置 | 当前限制 |
| --- | --- | --- | --- | --- |
| telescoping | 差分／望远镜 | L3 | `gaussian_weighted_range_v1` | only the stated structural family；no model-driven transformations；fixed safe proof templates; CAS construction alone never certifies a theorem |
| recurrence | 递推关系与唯一性 | L3 | `gaussian_geometric_recurrence_v1` | native Lean translation requires monic polynomial order two and supported flux；original RHS recurrence, two initial values and uniqueness connection remain open；other constructed operators are translation_pending, never checked certificates |
| coefficient | 系数展开与有限卷积 | L2 | `finite_product_framework/p2/run.py:construct` | no automatic Source-to-coefficient exporter; unknown sums remain atoms；standalone core request only; Train export and local Lean bridge unavailable；historical full workflow is not invoked; constructed never enters C |
| product | 有限乘积与指标等价 | L0 | `finite_product_framework/product/pipeline.py:plans` | plans() only chooses structural rules, not certificates; actual construction/replay requires missing workflow.contracts/preprocessed；standalone core request only; Train export and local Lean bridge unavailable；historical full workflow is not invoked; constructed never enters C |
| interpolation | 插值、零点与有理函数主部 | L2 | `finite_product_framework/interpolation/algebra.py:zero_certificate` | finite-node certificate only; original source extraction and Lean reconstruction unavailable；standalone core request only; Train export and local Lean bridge unavailable；historical full workflow is not invoked; constructed never enters C |
| noncommutative | 非交换算子等式 | L0 | `finite_product_framework/noncommutative/pipeline.py:prove_source` | actual normalization is Lean operator_words; native environment depends on missing workflow.contracts/preprocessed；standalone core request only; Train export and local Lean bridge unavailable；historical full workflow is not invoked; constructed never enters C |
| combinatorial | 加权双射与符号反转对合 | L0 | `finite_product_framework/combinatorial/pipeline.py:prove_source` | plans and map descriptions are not constructed certificates; actual map/weight reconstruction requires unavailable workflow and Lean exporter；standalone core request only; Train export and local Lean bridge unavailable；historical full workflow is not invoked; constructed never enters C |
| difference_ring | 嵌套和积的差分环 | L2 | `finite_product_framework/difference_ring/algebra.py:reduce_goal` | evaluated tower relation core only; original shift/evaluation bridges and Lean replay remain open；standalone core request only; Train export and local Lean bridge unavailable；historical full workflow is not invoked; constructed never enters C |
| kernel_transform | 有限核变换与矩阵反演 | L2 | `finite_product_framework/kernel_transform/construct.py:construct` | computed inverse/composition certificate only; target-kernel bridge and Lean obligations remain open；standalone core request only; Train export and local Lean bridge unavailable；historical full workflow is not invoked; constructed never enters C |
| spectral | 有限谱正交 | L2 | `finite_product_framework/spectral/construct.py:construct` | operator/eigenvalue separator certificate only; rational denominators and original pairing require Lean replay；standalone core request only; Train export and local Lean bridge unavailable；historical full workflow is not invoked; constructed never enters C |
| determinant | 行列式结构证书 | L2 | `finite_product_framework/determinant/construct.py:construct` | matrix-only certificate construction; target determinant value and original-domain conditions require Lean replay；standalone core request only; Train export and local Lean bridge unavailable；historical full workflow is not invoked; constructed never enters C |
| macmahon | MacMahon 有理 Ω 消元 | L2 | `finite_product_framework/p1/qomega.py:compute` | at most 8 factors, 4 auxiliary/8 external variables, exponent magnitude 8; core degree 32/states 16/terms 256; no original-object encoding or Lean bridge；standalone core request only; Train export and local Lean bridge unavailable；historical full workflow is not invoked; constructed never enters C |

L0 的三个方法保留了数学 Lean 模块，但现有 Python 部分只有规则／计划选择，原提取和执行路径依赖已移除的控制基础设施。当前不会把这些计划标成符号证书。

矩阵方法共享 `finite_product_framework/workflow/matrix_symbolic.py` 的纯数学编解码与残差核对，并核验其来源。未恢复 `workflow.contracts`、`workflow.preprocessed` 或旧 Agent。

底层求解器与方法族是不同层次。`core-demo` 原有的 q-Gosper、q-Zeilberger 和 parameterized q-Gosper 入口继续保留；同族的其他底层 modes 不因本表注册而自动获得新框架适配或 Lean 桥。

输入示例由 `agent_v2.symbolic_methods.example_request(method_id)` 生成；入口是 `python3 -m agent_v2.cli method-demo --method <ID> --input <JSON文件>`。符号演示不创建形式化断点，也不报告原题成功。
