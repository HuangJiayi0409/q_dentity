# 第一阶段收尾与 CAS 方法扩展实施计划

**Goal:** 按附件顺序，先对 AP-3.3.9 完成真实 ProofLink／端点／原题终验，再建立统一方法接口、递推 L3 和其余真实核心的诚实适配。

**Spec:** `/home/hjy/.codex/attachments/c2ea498d-ba38-4ba3-ba1a-10337adbb669/Codex_第一阶段收尾与第二阶段CAS扩展提示词.md`

**Architecture:** 沿用不可变 Source、Graph、事务性 C/O 和严格 checker。旧 CLI 默认 local 保持第一阶段 smoke；显式 full 范围添加受依赖条件控制的局部动作。桥证明自包含展开已验差分证明，但依赖 ID 仍显式检查。最终验收重建实际闭合证明树并重新编译原声明。第一阶段全部验收成功后才开始方法抽象。

## 约束

- 不读 benchmark Test，不改原命题／上下文／固定快照，不恢复旧 Agent/workflow，不模型调用。
- 单轮单联合动作；constructed 永不直接入 C；任何 O 替换必须有真实 Lean 连接，开放叶子等于 O。
- 固定依赖、精确命题、公理、源码和实际对象路径审计继续有效；恢复全部重新编译。
- 普通产物只留 generated；无有效本地 Git 元数据，保存 before/hash/diff。
- 不并行铺开全部方法。未通过原题终验不得进入第二阶段；环境和未解决正确性回归按附件停止规则报告。

## 执行清单

- [x] 重跑现有完整144项与原 telescoping_smoke；记录修改前基线。
- [x] `telescoping_closure.py`：完整上下文的有限求和条件桥、零端点和末端点，先失败测试再实现；真实数学探针。
- [x] 扩展数学 checker：已验依赖核对、受控闭合模板、精确原声明独立终验；保留旧Init/local路径。
- [x] Graph/adapter/CLI/loop：显式full范围，四轮各一个动作，精确输入条件和选择理由；恢复拓扑依赖重验。
- [x] 实跑原题closure、恢复、坏连接回滚；全套旧测试与local smoke通过，记录第一阶段停止门。
- [x] 门通过后才审阅现有递推核心，建立严格MethodSpec/registry，差分作为参考实现。
- [x] 递推真实Train CAS→局部Lean→残差闭环；失败则按能力等级诚实停止，不伪造L3。
- [x] 逐个审阅并适配其余实际CAS核心，每种都有适配/不适配、规范化、不误入C和失败分类测试；不凑数。7个L2、3个L0、40个顺序验收场景通过，缺依赖不冒充数学构造。
- [x] 独立审阅、最终完整测试、逐阶段验收与能力矩阵；具体命令与未完成事项写入筛选报告。最终216项全通过（0失败/0skip），旧local、完整closure与recurrence三个真实smoke均通过；报告见 agent_v2/CLOSURE_AND_CAS_REPORT.md。

## 接口分工

- `closure_blueprint(frontend)` 输出 local_id、bridge_id、两正式义务及精确 bridge proposition。
- `make_closure_candidate(frontend, task, approved_certificates, action_id)` 输出一个Candidate；bridge依赖C中的local并产生origin_action绑定义务，endpoint仅关闭精确父义务。
- `MethodAdapter.execute_action(state, action, attempt_dir, seconds)` 只执行所选任务；旧execute接口保留。
- 新Train final的report包含state，checker由state重建依赖／组装而非信任report成功标志。
- 第二阶段接口在第一阶段通过后依据真实源码确定，不预先承诺未知方法等级。
