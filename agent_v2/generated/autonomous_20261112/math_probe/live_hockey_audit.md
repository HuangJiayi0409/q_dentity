# 现场 hockey-stick 运行独立验收

**通过。** 对 `final_revision_01/live_hockey/20261112T055221Z-05ffaad720`
保存的现场记录完成独立核对，并使用 checkpoint 内唯一的 LocalTask 注册表建立
新的 LocalLeanChecker，对同一最终 state 执行一次 accept_original。真实重新编译
依赖别名和原题，43.712 秒后返回 `original_theorem_proved`。

独立结果见 `live_hockey_audit.json`；新 Lean 事务与完整 receipt 位于该 run 的
`independent_audit/`。旧 checkpoint、run.json、模型响应及原有 receipt 均未修改。

## 现场链路核对

| 阶段 | 本次记录与独立检查 |
|---|---|
| 第 1 轮 CAS | telescoping 构造源式绑定的局部差分引理；真实 Lean 接收 1 项证书，原题仍开放 |
| 暂停 | 保存的不可变 checkpoint：round=1、status=incomplete、C=1、O=[original]、model_calls=0 |
| fresh resume | 新的 resume_checks 事务重新通过同一局部引理，43.370 秒；id/type/proof/dependencies 不变，旧 receipt 被新的实际验证 evidence 替换 |
| 第 2 轮模型 | 请求记录 transport=http，经 `https://www.cctq.ai/v1/responses`；网关返回 completed、模型名 gpt-6-astra、独立 response id 和 usage。输出只有 proof_term，缺少 kind，按格式错误拒绝，新增证书 0 |
| 第 3 轮模型 | 第二个实际 HTTP 请求；输出补上 kind=prove，证明正文与第一次响应完全一致；真实 Lean 接收该证明 |
| 原题终验 | 原运行原题通过；本次独立 accept_original 又重新通过，未调用模型/API |

两次响应 id 分别为：

- `resp_06762231011a3483016af5548d33b887d282df82a13b54a6d0`
- `resp_08f8922379500d98016af5549a0e5487d2b850bd551951d420`

两次 proof_term 的 SHA-256 完全相同：
`d4835ab7a5f1a95fe6216a408a8b1997f2390c66e75f7402a5b5e2f0c117d03d`。
最终证书中的模型证明正文与第二个 provider 响应逐字一致；无需主控补写或修改证明。
初次模型输入未包含完整的最终证明，已验 CAS 引理仅通过名称、类型和证书 id 暴露。
第二次属于**输出格式修复**，不能描述成 Lean 数学错误修复。

HTTP 来源判断基于保存的请求 transport、请求/响应哈希、provider completed 对象、
模型名/usage，以及审计时未漂移的实际客户端代码；它不等于对外部网关身份的密码学证明，
也不将网关报告的模型名进一步解释为直接连接官方服务。

## 独立数学验收及不可变性

- 精确原题：`FiniteQBenchmark.Identity272.statement`，即 Train 的
  `FQI-SRC-AP-3.3.9`；源文件和冻结副本均为
  `d9a88ffda89d1bbb38da774ac9f30bba41b11674e6057b698c11d0407dc26efa`。
- 从 manifest 指向的、哈希一致的不可变 checkpoint generation 读取 state；与
  checkpoint.json 内容一致，O 为空，证明树不变量通过。
- 独立编译实际审计 theorem 为 `FiniteQBenchmark.Identity272.statement`，
  保留 1 个 universe 参数；axioms 仅有 propext、Classical.choice、Quot.sound。
  原始任意 Field、全部 q 值及原有 True 条件均保留。
- 独立 Lean 事务绑定 14,401 个实际依赖文件；最终模块表没有 benchmark Statements、
  Benchmark.Representation 或 Benchmark.Batch3Proofs 导入。
- revision01 manifest 的 **81 个 runtime 文件**在独立验收前、后均逐项哈希一致。
- 原 run 的 **169 个已有文件**在验收前、后逐项哈希完全一致；仅新增
  independent_audit 事务，本报告亦写在单独的 math_probe 目录。
- 本次审计模型/API 调用数为 0；独立复编不改写原实验的时间、调用次数或成功记录。

这是 CAS 局部结果 → 现场模型连接证明 → 精确原题的真实单题通过证据。
本 run 的表示节点始终是 original、expansions=0，未执行新的表示分解、Jev 选择或
扩展后的第二个 CAS 数学任务；这些能力不能由本题成功外推。81 项无漂移结论针对
本次 revision01 独立验收前后，后续 revision02 修改应另行冻结和验证。
