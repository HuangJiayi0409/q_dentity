# 自主流程精选审计包（2026-11-12）

本目录打包本轮 Agent 自主流程的现场记录、冻结源码、回归日志和独立审阅。它是保留原始字节的精选审计材料；不是完整运行环境镜像，不承诺解压后可直接恢复旧 checkpoint。所有包内路径保持仓库相对路径。

## 文件与核验

- `autonomous_20261112_audit.tar.xz`：精选原始证据。
- `members.json.xz`：压缩的成员清单；解压为 `members.json` 后可读到每个包成员的路径、SHA256 和字节数，以及逐项省略编译物和收据/依赖引用的定位或未打包原因。本地保留原 JSON，但发布只选 `.xz`。
- `manifest.json`：原白名单目录的文件数、字节数、目录清单哈希、选择范围和排除策略。
- `sensitive_scan.json`：已知本地凭据精确匹配和令牌模式扫描结果；没有密钥值。
- `verification.json`：实际解包、逐成员哈希、路径安全及两次确定性打包核验。
- `SHA256SUMS`：`manifest.json` 中 `publication_files` 所列实际发布文件的 SHA256；不包含它自身，也不列本地原 `members.json`。
- `build_transport.py`：只读原始材料、只写本目录的构建脚本，不联网、不调用模型、不运行 Lean。

先在本目录执行 `sha256sum -c SHA256SUMS`，再用 `tar -xJf autonomous_20261112_audit.tar.xz -C 空目录` 解压。xz 采用 preset 9（64 MiB 字典），成员字节、路径和省略策略与原 gzip 版本一致。`members.json` 对应包内全部成员；它与其余交付说明位于压缩包外，避免自引用哈希。

用 `xz -dc members.json.xz > members.json` 解压成员清单，然后执行 `sha256sum members.json`，应等于 `verification.json` 中 `compressed_member_inventory.decompressed_sha256`。该记录同时给出解压后字节数和第二次压缩一致性。发布端应严格按 `manifest.json` 的 `publication_files` 选择文件，避免上传本地 13 MiB 原 JSON。

## 优先阅读

以 `agent_v2/generated/autonomous_20261112/` 为下列路径的公共前缀：

1. `final_validation.json`、`train_preregistration.json`、`changed_files.json`。
2. `after/agent_v2/AUTONOMOUS_VALIDATION.md` 和 `after/agent_v2/AUTONOMOUS.md`。
3. `final_revision_01/unittest.log`（553 项）和 `final_revision_02/targeted_unittest.log`（66 项）；两组有重叠，不能相加为独立总数。
4. 两个版本的 `source_manifest.json` 与 `frozen/agent_v2/`；`before/`、`after/`、`changes.diff` 保留修改前后材料。
5. 下列四次运行中的 `run.json`、`graph.json`、`checkpoint_manifest.json`、`checkpoints/`、`rounds/` 和存在的 `final/`。
6. `math_probe/live_hockey_audit.md`、对应 `.json/.py` 与首题 `independent_audit/`。
7. `math_probe/runtime_review.md`、`math_probe/local_security_review.md`、`task2_independent_review.md`，以及它们对应的复现脚本/结果。

| 运行目录 | 所属版本及结果 |
|---|---|
| `final_revision_01/live_hockey/20261112T055221Z-05ffaad720/` | 原题通过；保留暂停恢复检查、缺协议字段的模型响应、修复及独立终验 |
| `final_revision_01/live_recurrence/20261112T055819Z-d489a737b9/` | 原题通过；保留局部递推与现场模型修订 |
| `final_revision_01/live_multi_method/20261112T055459Z-062bba8130/` | 两个开放义务；保留 Jev 4 次调用、低置信度回退、分解及导航 |
| `final_revision_02/live_controlled_expansion/20261112T060938Z-aeac5e776a/` | 受控 Graph→CAS→原题通过；首次动作受测试指定，不计自主策略效果 |

重复启动的 `final_revision_01/live_multi_method/20261112T055756Z-1e4da7f531/` 连同 `excluded_duplicate.json` 和额外请求保留，明确排除成绩。`final_revision_01/checker_train/` 保存整套测试中的实际混合验收。已报告的配置预检失败也保留，但不计 Train 解题结果。

## 省略与复现边界

去掉 `.olean/.ilean/.o/.c/.ir`、构建输出、缓存和外部工具链本体；未选入临时开发运行。原收据、依赖清单和哈希没有改写，`members.json` 逐项解释被引用编译物的省略。源码若以不同路径保存，提供相同内容哈希的包内定位。

包外的 Lean/Mathlib、CAS 源码、项目清单和原环境依赖仍需匹配版本。它们的原路径及哈希只作为审计依据保留，不表示本包已经包含所有依赖。重新编译须另行准备匹配仓库与外部环境；编译产物哈希也不保证在另一环境中相同。历史绝对路径不能直接当作解包后的恢复路径。

两版各自冻结源码、原版本日志及原运行归属保持不变。第二版只改停止分类，第一版现场证明没有被冒称为第二版重跑。本轮为预选小样本集成验证，不是全 Train 成功率实验。

打包仅枚举本轮明确白名单，不扫描或读取 benchmark Test，不读取旧 Agent 方案，不发网络请求。`API_GPT/API_Jev/API_deepseek` 仅在内存中用于精确密钥匹配；凭据文件和值均不进入交付物。扫描只记录可疑文件路径和规则名。
