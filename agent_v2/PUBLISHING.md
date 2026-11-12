# GitHub 发布范围

本仓库保留 Agent v2 源码、测试、说明文档、实施计划和可直接浏览的验收记录。第三阶段另提供完整精选证据的压缩包，包含实际候选 Lean 源码、证明产物、原始请求／返回、运行日志、检查收据、断点与冻结源码；它不包含整个开发目录或外部 Lean／Mathlib 工具链。

证据中的绝对路径与哈希记录原运行环境，不能当作在另一台机器上可直接恢复的断点。请按 README 在自己的项目环境创建新运行。压缩包内保留的 `.olean` 仅为原验收产物；跨环境使用仍须重新生成。源码、日志和哈希用于审阅，不替代重新执行 Lean 验收。

2026-11-12 第三阶段发布：11 种方法接通真实 Train Source，注册等级为 8 个 L3、4 个 L2。望远镜与递推完成限定结构族的原 theorem 验收；其余六个 L3 仅完成局部证明，三个新增 Source L2 尚无 Lean 出口。谱方法保留旧显式核心 L2，真实 Train Source 接入未完成，因此第三阶段整体仍为部分完成。最终冻结源码的 475 项测试通过，0 失败、0 错误、0 跳过；发布前再次核对 262 个源码／测试／数学依赖文件哈希一致，本次上传没有重新运行这些测试。

当前结果见 [第三阶段验收报告](PHASE3_VALIDATION.md) 和 [方法能力矩阵](METHOD_CAPABILITIES.md)。完整精选证据共 23 包、6801 个实际文件；[压缩包说明与校验方法](../output/github_agent_v2_phase3_20261112/transport/README.md)提供下载、SHA-256 校验和解压命令。原 [证据索引](../output/agent_v2_phase3_evidence_20261112/pack_index.json)及最终报告保持原字节，解压后可按索引查找具体文件。

历史发布（第一阶段收尾与第二阶段 CAS 扩展）：`FQI-SRC-AP-3.3.9` 完成四轮局部动作和独立原题 Lean 终验，最终 C=4、O=空、ProofLink=3；当时 `FQI-GAUSS-ALTERNATING` 仅完成局部递推 Lean 验证，原题仍开放。当时注册表为 2 个 L3、7 个 L2、3 个 L0，216 项测试通过，无失败或跳过。这些旧记录不代表第三阶段当前状态。

历史结果见 [第一阶段收尾与第二阶段报告](CLOSURE_AND_CAS_REPORT.md) 和 [旧精选记录说明](generated/closure_and_methods_20261111/EVIDENCE_README.md)。此前的 VALIDATION、REVIEW_FIXES、TELESCOPING_PHASE1 及旧运行记录保留其历史含义，不替代第三阶段结论。

本文件在验收后仅更新发布说明，因此历史 `final_frozen_hashes.json` 中本文件的哈希对应更新前版本；不改写任何历史冻结清单。生产代码与测试文件仍与第三阶段最终验收版本一致。
