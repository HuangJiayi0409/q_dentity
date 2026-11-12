# Agent v2 第三阶段实施计划

> **For agentic workers:** Use superpowers:executing-plans / subagent-driven-development task by task with test-driven-development. 本附件已明确授权执行；无需重复询问设计或发布方式。

**Goal:** 先完成固定 Gaussian 交替和递推整题闭环及公共核验接口，再依次尝试七个真实 Train 局部 L3 与三个真实 Train L2；达不到的项目按实际边界报告，不能假升级。

**Architecture:** 保留 Source / ResidualState / Graph / Executor / Loop / RunStore 的唯一状态与预算。独立数学模块只构造候选；Source 重建的固定 profile 决定受控证明模板和编译配置；所有 C/O 更新仍经过生产 LeanChecker 与事务。递推 full 是五个固定局部任务，每轮一个候选。

**Tech Stack:** Python 3.10、现有纯符号核心、SymPy、固定 Lean 4 工具链和 Mathlib。

**Spec:** `/home/hjy/.codex/attachments/ad32cf4b-1702-4ae8-af0e-4eff826ec272/Codex_第三阶段_十二种CAS全方法真实接入提示词.md`

## 全局边界

- 不读 benchmark Test，不改原命题／Γ／源 SHA／theorem／原域，不新增原题假设。
- 不恢复旧 Agent/workflow 控制层；只复用显式、受控的纯数学算法和引理。
- 不使用 sorry/admit/新 axiom/历史收据；不接受任意 import、脚本或 tactic。
- 每动作至多一个待验候选。连接未通过不能替换 O；开放叶子严格等于 O；O 空仍需独立原 theorem 验收。
- 基线旧测试不得删除／修改／放宽。实际错误证明必须到达真实 Lean；接口故障注入不计数学成果。
- 当前无 Git 元数据，保留 before/after、哈希和差分；不初始化 Git、不删除工作区。此次实现未要求上传。
- A/B 停止门通过前不实施 C/D；其后每次只实施一个方法。单方法数学/结构缺口可停该分支并继续下一方法；公共正确性未解决回归必须停全局推进。

## 审阅重点

1. Source 同时匹配多个 profile 时拒绝歧义，不能 first-match。
2. 递推 witness 派生 local ID 必须来自本轮真实结果，不能预取 CAS 或硬编码示例证书。
3. 冻结状态恢复只向后续检查提供本轮重验过的前驱，不能用相似 proposition 冒充跨方法证据。
4. 任意 Field 的 q=0、特征2、自然数模／除法和两个初值不能在归一化中丢失。
5. 后续局部候选必须锚定当前 Train 的实际子结构；无关矩阵恒等式、固定结果、枚举几个参数均不算接入。

## Task 0：新基线与快照

- [x] 67 个现有源码／测试／文档保存于 `agent_v2/generated/phase3_20261112/before/`，记录 SHA。
- [x] 新进程执行完整 unittest、Init real_smoke、telescoping_smoke、closure_smoke、recurrence_smoke；216项通过，0失败/错误/skip，467.802秒，四smoke通过。
- [x] 基线结束前未修改生产或测试文件，67文件哈希一致；仅在 generated 内做独立数学探针。

## Task 1：A/B 公共 profile 和严格绑定

**Files:** 新 `agent_v2/proof_profiles.py`；改 `lean_checker.py`、`math_lean_profile.py`、必要的 `recurrence_lean_profile.py`；新增 `tests/test_proof_profiles.py`。

**Interfaces:** `select_profile(source, run_root)` 返回唯一由 Source 重建的 `(profile, frontend)` 或明确不适配；多个匹配 fail closed。profile 固定 ID/version、重建入口、数学依赖、受控driver、原题支持范围；不可由候选指定调用路径。

- [x] 先添加未知／多重适配、证书 ID/profile 欺骗、跨方法依赖、旧 Init/telescoping/recurrence 保持的失败测试。
- [x] 把现有 receipt 字段／产物／公理检查参数化为所选 profile；补齐模板、ID、依赖、源锚点核对。
- [x] partial、resume、original 共用同一模板绑定；保留纯负例项送真实 Lean 的通道。
- [x] 原声明唯一 sorry 替换仍保留 theorem/参数/universe/等式方向，仅由受控前端确认语法。
- [x] 测试通过后保存差分与运行结果，不通过则解决公共回归后再继续。

## Task 2：A 的数学闭包候选

**Files:** 新 `agent_v2/recurrence_closure.py`、`tests/test_recurrence_closure.py`；数学探针在 generated/math_probe。

**Interfaces:** `closure_blueprint(frontend, approved_local)` 返回 exact propositions、stable IDs、local依赖和三个义务；`make_closure_candidate(frontend, task, approved_certificates, action_id)` 返回一个 Candidate。仅重建和生成，不写状态。

- [x] 先测局部 witness 重建、缺失／篡改依赖、binder 改名、反向等式、错误 RHS 结构、义务 ID/origin 与关闭目标。
- [x] 固定 S 的已有真实二阶 witness；R 的奇偶与 poch 步进、两个初值、两步／强归纳唯一性均在任意 Field 真实证明。
- [x] 唯一性候选类型为 R递推 → 初值0 → 初值1 → 原题，依赖精确已验 S 证书，并内联重编其证明。
- [x] RHS 与两个初值是独立候选；原题不加 q≠0 等假设。
- [x] 生产 checker 验证全部候选与真实负例，保存源码/输出/审计，不以纯数学探针替代接口验收。

## Task 3：A 的五轮动作、恢复与完整终验

**Files:** 改 `recurrence_adapter.py`、`cli.py`、固定任务契约／Graph 接口、必要的 loop；新 `tests/recurrence_closure_smoke.py`、事务与恢复回归。

**Interfaces:** tasks=`local,uniqueness_bridge,rhs_recurrence,initial_zero,initial_one`。沿用 witness 派生的真实 local ID；仅在其批准后绑定预声明后续任务的依赖，不生成新表示、转换边或任意数学任务。

- [x] 先测任务依赖过滤、重复任务抑制、非法 handles、单轮成本、普通 Lean 失败回滚、inflight 和最终失败重开。
- [x] 每轮生成一个候选；状态由 C1/Ooriginal/links0 → C2/O3/links1 → C5/O0/links4。
- [x] 五份候选及精确 Identity009 原声明在生产 checker 真实通过之后，才正式启用 recurrence full 能力声明。
- [x] 真实 CLI 至少两个阶段恢复；全部拓扑重验，无重复 CAS／动作扣款；错误连接、RHS、初值通过真实 Lean 拒绝。
- [x] 原题终验、完整旧测试及望远镜闭环／恢复全通过后写 A/B gate。未通过禁止进入十方法升级。

## Task 4：C/D 实际匹配清单（仅 A/B gate 后）

- [x] 逐项读取十方法真实核心与 Train；写 identity/theorem/hash/完整声明、typed请求、Lean映射、预期局部证书、缺口／限制。
- [x] 不预先承诺未知结构；无真实匹配记录具体证据，不改原题造样例。

## Tasks 5–11：C 七方法依次实施

顺序：coefficient → interpolation → determinant → kernel_transform → spectral → difference_ring → macmahon。

七个分支已依次尝试；单方法停止按附件 9.3 处理，没有跳过失败后升级。

| 方法 | 实际验收结果 |
| --- | --- |
| coefficient | Source、核心与独立核对、局部 Lean 正反例、恢复和绑定检查通过，L3 |
| interpolation | 同上，L3 |
| determinant | 同上，L3 |
| kernel_transform | 同上，L3 |
| spectral | Source 接入和 Lean 桥未完成；保留失败日志和停止卡，仍 L2 |
| difference_ring | Source、核心与独立核对、局部 Lean 正反例、恢复和绑定检查通过，L3 |
| macmahon | 同上，L3；另完成受控单态驱动与旧多态检查兼容 |

- [x] 六种通过方法均只增加一个局部 C，O 保持 original、links 为空、full_original=false。
- [x] 逐方法验收卡、冻结源码、真实失败与复现材料已保存。
- [ ] 七种全部达到 L3：未达成，谱方法仍有明确结构和形式桥缺口。

## Tasks 12–14：D 三方法依次实施

顺序：product → noncommutative → combinatorial。每方法分别：

- [x] 三种均完成真实 Train 导出、适配／不适配、独立证书核对和失败分类测试。
- [x] 接入受限纯数学核心，没有恢复旧控制器。
- [x] 保留 formal Train state，C_partial/O_res均空，links不变，整题false，预算和进程留档。
- [x] product 核对范围／空积／混合进制逆映射；noncommutative 保留算子顺序；combinatorial 核对参数化映射、秩和带符号权重。
- [x] 各有真实 Train 正例后才升 L2，三张正式验收卡通过。组合 Gaussian 表示桥仍为 pending；三者均无 Lean 桥。

## Task 15：最终审阅与交付

- [x] 独立审阅公共正确性与逐方法实际能力，定向回归通过，无未解决 Important/Critical。
- [x] 冻结 262 个代码／数学／测试源；最终 475 项全通过、0 skip，recurrence/telescoping full、六新增局部 L3／三个 Source L2 及谱停止边界全部按实际能力复验。
- [x] 最小可审计证据包含请求、候选 Lean 源／日志、状态、恢复／负例、原题审计与哈希；最终 23 包、6691 复制文件核对通过，419 项缓存省略有明细。
- [x] 总报告、README、能力矩阵、12 张最终卡与复现入口已更新并核对链接；A/B/D 完成、C 六种通过而谱方法未完成，整体明确为第三阶段部分完成。
