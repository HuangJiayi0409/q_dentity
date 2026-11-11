# GitHub 发布范围

本仓库保留 Agent v2 源码、测试、说明文档、实施计划和精选文本验收记录。Python 缓存、Lean 编译产物、完整运行目录及重复源码快照留在开发环境，不批量上传。

历史证据中的绝对路径与哈希记录原运行环境，不能当作在另一台机器上可直接恢复的断点。请按 README 在自己的项目环境创建新运行；记录中引用的 `.olean` 需重新生成。文本证明和哈希记录用于审阅，不替代重新执行 Lean 验收。

2026-11-12 发布的第一阶段收尾与第二阶段 CAS 扩展：`FQI-SRC-AP-3.3.9` 已完成四轮局部动作和独立原题 Lean 终验，最终 C=4、O=空、ProofLink=3；`FQI-GAUSS-ALTERNATING` 仅完成局部递推 Lean 验证，原题仍开放。注册表为 2 个 L3、7 个 L2、3 个 L0；L2 尚无局部 Lean 桥，L0 明确拒绝不可执行能力。最终 216 项测试通过，无失败或跳过。

本轮结果见 [完整验收报告](CLOSURE_AND_CAS_REPORT.md) 和 [方法能力矩阵](METHOD_CAPABILITIES.md)。精选记录说明见 [EVIDENCE_README.md](generated/closure_and_methods_20261111/EVIDENCE_README.md)。此前的 VALIDATION、REVIEW_FIXES、TELESCOPING_PHASE1 及旧运行记录保留其历史含义，不替代本轮结论。

本文件在验收后仅更新发布说明，因此历史 `final_frozen_hashes.json` 中本文件的哈希对应更新前版本；不改写该历史清单。生产代码与测试文件仍与本轮验收版本一致。
