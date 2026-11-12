# 第三阶段完整精选证据压缩包

本目录提供 [完整压缩包](agent_v2_phase3_evidence_20261112.tar.xz)、[运输校验清单](transport_manifest.json)和[逐文件清单](members.json)。压缩包包含最终交付的全部 23 个证据包及索引，共 6801 个文件、1,146,424,463 个原始字节；压缩后 7,255,636 字节（约 6.92 MiB）。所有成员已逐一解压核对 SHA-256 和大小，打包前后源文件一致。

其中 6691 个文件由原证据包的复制清单登记，另 110 个为顶层索引、映射及元数据。完整保留候选 Lean 源码和相应证明产物、原始 CAS 请求／返回、stdout／stderr、Lean 收据、运行断点、原声明与冻结源码。原证据包明确排除的缓存和外部 Lean／Mathlib 工具链不在此包中；不能将它视为整个开发目录的镜像。

从本仓库根目录执行以下命令，先校验，再恢复精选证据目录：

```bash
sha256sum -c output/github_agent_v2_phase3_20261112/transport/SHA256SUMS
tar -xJf output/github_agent_v2_phase3_20261112/transport/agent_v2_phase3_evidence_20261112.tar.xz
```

解压结果位于 `output/agent_v2_phase3_evidence_20261112/`。原 [pack_index.json](../../agent_v2_phase3_evidence_20261112/pack_index.json)记录各包及来源映射；每个包中的 manifest 可用于进一步核对。仓库直接展示的同名索引与压缩包内字节一致。压缩只规范 tar 外层时间、用户和权限字段，所有原文件内容保持不变。

历史绝对路径与哈希保留原运行环境，不提供跨机器直接 resume 保证。重新验证需要安装相应 Lean／Mathlib 与 Python 依赖，并按 [最终验收报告](../../../agent_v2/PHASE3_VALIDATION.md)在新的输出目录运行。

当前实现为 11 种真实 Train Source 方法、8 个 L3 和 4 个 L2；谱方法的真实 Train Source 接入尚未完成。第三阶段结论仍为部分完成。运输包生成不产生新的证明或测试结果，475 项测试结论来自报告记录的最终冻结源码运行。
