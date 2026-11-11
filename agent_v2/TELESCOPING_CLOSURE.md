# 有限求和连接与原题验收

`--scope full` 在原有局部差分模式之上增加三个局部任务。默认 `--scope local` 保留原来的单证书行为。当前受控结构族是 Gaussian 加权前缀和；按完整源码结构识别，不按题号选择证明。

```bash
python3 -m agent_v2.cli run --identity FQI-SRC-AP-3.3.9 --method telescoping --scope full --selector rule --max-steps 4 --seconds 1800
python3 -m agent_v2.cli resume --run-dir <上条命令返回的运行目录>
python3 -m agent_v2.tests.closure_smoke --output-root agent_v2/generated/closure_acceptance
```

每轮候选只含一个局部动作，Graph 根据 C 中的依赖和 O 中的义务过滤出口。两个端点之间没有虚构的依赖，规则选择器可以选择任一尚未完成的端点。

| 动作 | 所用证据 | 经独立 Lean 验证后的变化 |
| --- | --- | --- |
| local | 本次真实 q-Gosper 返回，经安全解码、残差检查和原域回译 | C 加入逐项差分定理；O 仍为原题 |
| bridge | C 中精确绑定的逐项差分证书 | C 加入条件连接；原题替换为两个端点义务；增加 ProofLink |
| zero_endpoint | 原域 Gaussian 越界为零引理 | 只关闭零端点 |
| upper_endpoint | 自然数下标恒等式 | 只关闭末端点 |
| 最终验收 | 已验证连接构成的完整证明树 | 独立编译原声明、公理和依赖审计通过后才标记 original_theorem_proved |

连接的完整类型由 `telescoping_closure.closure_blueprint` 返回。对所选原题，两个前提分别是以下闭合命题，结论是冻结源码独立解析得到的完整原命题：

```lean
∀ {K : Type u} [Field K] (q : K) (m n : ℕ) (h_domain : True),
  FiniteQBenchmark.gaussian q (m + 0) (m + 1) = 0

∀ {K : Type u} [Field K] (q : K) (m n : ℕ) (h_domain : True),
  FiniteQBenchmark.gaussian q (m + (n + 1)) (m + 1) =
  FiniteQBenchmark.gaussian q (n + m + 1) (m + 1)
```

桥证明使用有限范围求和归纳，将已验证的逐项差分求和，再应用两个端点前提。桥证书显式记录局部证书 ID；证明项内嵌该已验证项，便于最终独立编译。端点没有 q≠0、正则性或其他新增假设，保留任意 Field 和原始参数。

证明树组装时为每个证书项保留精确类型标注，以支持带条件的 tactic 证明项作为函数应用。最终检查器保持原 theorem 名、参数、上下文及等式方向，仅替换冻结声明的证明占位；不导入 Statements 或历史原题证明。

恢复会依赖顺序重新编译全部证书，后继只接收本次新验证的前驱收据。最终验收临时失败时，当前状态仍重开原题；`final/retry.json` 仅保存待重建的树结构。恢复先重新验证全部 C，再核对该结构与当前源、证书和尝试记录，并检查开放叶子不变量，随后重新终验；它不充当证明收据，也不再次调用 CAS。

完整 smoke 检查四轮状态转移、原题验收、四份证书恢复重验、再次原题验收，以及错误桥证明被真实 Lean 拒绝后的事务回滚。控制器故障注入测试与真实数学验证分开记录。
