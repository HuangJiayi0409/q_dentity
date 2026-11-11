# Agent v2 真实 Train 差分局部闭环实施计划

> **For agentic workers:** Use superpowers:executing-plans for the controller and scoped delegated implementation/review. Track the checkboxes below; the supplied specification already authorizes implementation.

**Goal:** 对唯一选定的 Train 原题产生真实 CAS 局部证书，经真实 Lean 检查写入 C，保留未证明的原义务 O，并支持重新编译验证后的恢复。

**Architecture:** 保留现有单动作控制与残差不变量。新增独立窄结构前端、q-Gosper 结果到无除法 Gaussian 差分候选的受控回译、固定数学依赖的 Lean 检查配置。采用附件允许的结果 A：独立局部证书成功，原题仍开放；不扩图，不接其他方法。

**Tech Stack:** Python 3、现有 SymPy q-Gosper CoreAdapter、仓库固定 Lean 4.35.0-rc4 与 Mathlib。

**Spec:** `/home/hjy/.codex/attachments/9d802510-1a8e-4e67-a0f4-c5d54e72e239/Codex_第一阶段_差分望远镜CAS真实闭环提示词.md`

## Global Constraints

- 只选择一道真实 Train 命题，不读取 Test，不运行全 Train 批测。
- 不调用 LLM、Jev、网络模型，不恢复旧 Agent/workflow，不把历史证明当作本次成果。
- 保留全部原参数、假设、自然数范围与定义域；不能添加非零或正则假设。
- 每轮仅一个合法联合动作；identity 保持 source == target == state.r。
- constructed、partial_lean_verified、original_theorem_proved 严格区分；只有真实 Lean 验收进入 C。
- 无连接定理时保持 O 与原题开放；坏连接回滚，但保留独立已验成果。
- 固定导入，保留精确 proposition/source/依赖绑定、公理审计、候选实际重编译、恢复实际重验。
- 不删除、跳过或放宽旧测试；普通运行证据不批量发布。

## Review Focus

- 通用有理函数证书不能直接特化至 q=0 或单位根；回译为无除法表达式后在原 Field 域重新证明。
- 前端必须完整消费受支持语法；未知 binder、假设、索引和类型转换须 not_applicable。
- 多态 Field 的 universe 不能缩成 Type 0；新审计独立于旧 Init 限制。
- 原题模块不得进入证明依赖；实际 Lean 导入闭包必须与冻结白名单一致。
- 局部成功和恢复后仍开放的原目标应报告 incomplete，而非伪称完整证明；预算/环境/完整性失败仍区分。

## 选择与实现边界

选择 `FQI-SRC-AP-3.3.9`，源 `benchmark/lean/Benchmark/Statements/Train/Identity272.lean`。其原上下文为 `{K : Type*} [Field K] (q : K) (m n : ℕ) (h_domain : True)`，范围 `Finset.range (n+1)`，项 `q^j * gaussian q (m+j) m`。真实 q-Gosper 输入为 `q*(1-a*X)/(1-q*X)`，映射 `a=q^(m+1), X=q^j`；CAS 已在独立侦察中返回 R=(X-1)/(X*a-X)。候选用 Gaussian 相邻下标表示，原域验证 `G(j+1)-G(j)=F(j)`；剩余有限求和、端点和原式方向连接本轮诚实保留在原义务中。

现有 `prove_telescoping.py` 不存在；不恢复它。现有 direct.py 数学邻接表示思路可复用，但不引入其旧 workflow 依赖。工作区无有效 Git 元数据，已保存修复前文件与哈希，直接在当前目录增量修改。

## Task 1：基线与前端/回译

**Files:** 新增 `agent_v2/formal_frontend.py`、`agent_v2/telescoping_translation.py` 及各自测试。

**Interfaces:** `analyze_source(source: dict, run_root=None) -> dict` 返回 applicable/not_applicable 与原始 source 绑定、完整 binder/AST、original_proposition、local_proposition、core_request、mapping、profile；`translate_candidate(frontend: dict, core_raw: dict) -> dict` 从实际 CAS 回包恢复受支持无除法 flux，返回候选或 translation_pending。`local_proof(frontend)` 为检查器提供受控证明模板，不包含目标整题答案。

- [x] 保存现有 Agent 源文件与哈希，运行修改前 100 项测试。
- [x] 先写所选真实题识别、真实不匹配 Train 题、完整上下文和源绑定负例；记录失败。
- [x] 实现完整消费的窄语法结构匹配，禁止按 ID 分派数学答案。
- [x] 安全解析 CAS 有理式并验证证书关系/邻接表示，回译只消费实际 constructed 结果。
- [x] 测试通过；审查范围与原域特化边界。

## Task 2：真实 Lean 检查配置

**Files:** 修改 `agent_v2/lean_checker.py`，新增聚焦的数学依赖/检查辅助模块及专用 Lean 审计驱动；新增 integration 测试。

**Interfaces:** `check_partial` 的 context 增加 `source=state.G.to_dict()`；新配置由重新读取的前端识别结果选择，候选不能指定导入。expected proposition 独立重算。

- [x] 先写真实局部正例、错误证明、sorry、错命题/错哈希、超时/缺环境等测试并见失败。
- [x] 固定 Benchmark 基础数学依赖及 GaussianRules；冻结并审计源码、实际导入模块、编译产物、工具链和运行库。
- [x] 保留 universe 参数及原上下文；每次重新编译候选，严格公理审计。
- [x] 真实 Lean 正反例通过，旧 Init 测试保持通过。

## Task 3：适配器、残差与 CLI

**Files:** 修改 `agent_v2/cas_adapter.py`、`executor.py`、`loop.py`、`cli.py`，新增本阶段集成测试。

- [x] MethodAdapter 调前端、真实 CoreAdapter、回译；保存逐层证据，constructed 不自动入 C。
- [x] 执行和恢复检查器传完整 Source；前端识别后冻结闭合原命题而不改变 Γ/源声明。
- [x] 已验独立局部证书增加 C，O 原样开放；局部能力边界停止为 incomplete。
- [x] 检查失败分类、无连接/坏连接/合法连接、不盲目信任恢复收据；保留所有旧来源/预算测试。

## Task 4：最终验收与报告

- [x] 全部单测与标记的真实 integration 测试。
- [x] 正式 CLI 对唯一所选 Train 题执行真实 CAS→Lean；实际恢复并重编译局部证书。
- [x] 真实错误证明负例与运行产物/源哈希独立核验。
- [x] 审阅全部 diff，修复重要问题并有针对性复验。
- [x] 筛选验收说明：完整原声明、精确局部命题、命令、计数、C/O 前后、完整原题未验收、支持与不支持范围。普通运行产物保留本地。

## 实施记录

- 修改前基线：100/100，29.690 秒，零失败/跳过；保存 28 个原 Agent 文件。
- Task 1：完成，前端/回译 13 项先红后绿；真实 CAS 与生成局部证明的开发探针均通过。
- Task 3 接线：局部作用域与原有控制器/执行器共 45 项通过；方法适配器 5 项通过，原 CLI 11 项通过。单元测试替身不计真实证明成果。
- Ruling：全局 Test 路径守卫不变；固定 Lean 导入链经过 `Std.Http.Test.Helpers`（标准库 HTTP 基础设施，非 benchmark 留出集）。数学依赖审计仅可在验证固定工具链根、模块名、文件后缀和解析后仍包含于固定子树的条件下读取这些标准库文件。仍拒绝 benchmark Test 和工具链外同名路径；测试该边界。若不区分两者，真实固定工具链的完整依赖审计无法完成。

- 最终验收：144/144，0 失败、0 跳过，115.037 秒；真实CLI、恢复重编译、真实错误证明拒绝全部通过。结果A，C=1，O=原题，incomplete；ordinary generated artifacts不批量发布。
- 最终审阅：两项Important均经针对性反例关闭，无未解决Critical/Important；32源码/测试/驱动哈希一致。
