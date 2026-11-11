# 第一阶段收尾与第二阶段 CAS 扩展验收

第一阶段整题闭环已通过；第二阶段完成两个 L3 方法、七个 L2 纯符号适配和三个明确不可执行的 L0 边界。方法等级不代表全 Train 解题率。

## 第一阶段收尾

固定 Train：`FQI-SRC-AP-3.3.9`，最终定理 `FiniteQBenchmark.Identity272.statement`。原始源文件、上下文、参数及等式方向保持不变。

| 轮次 | 实际动作 | C 数量 | 开放义务数 | ProofLink 数 | 实际秒数 |
| --- | --- | --- | --- | --- | --- |
| 1 | local | 1 | 1 | 0 | 44.627 |
| 2 | bridge | 2 | 2 | 1 | 44.034 |
| 3 | zero_endpoint | 3 | 1 | 2 | 43.977 |
| 4 | upper_endpoint | 4 | 0 | 3 | 43.829 |

有限求和条件连接的精确 Lean 类型：

```lean
(∀ {K : Type u} [Field K] (q : K) (m : ℕ) (n : ℕ) (h_domain : True), FiniteQBenchmark.gaussian q (m + 0) (m + 1) = 0) → (∀ {K : Type u} [Field K] (q : K) (m : ℕ) (n : ℕ) (h_domain : True), FiniteQBenchmark.gaussian q (m + (n + 1)) (m + 1) = FiniteQBenchmark.gaussian q (n + m + 1) (m + 1)) → (∀ {K : Type u} [Field K] (q : K) (m : ℕ) (n : ℕ) (h_domain : True), ((FiniteQBenchmark.gaussian q ((n + m) + 1) (m + 1)) = (∑ j ∈ Finset.range (n + 1), ((q ^ j) * (FiniteQBenchmark.gaussian q (m + j) m)))))
```

四份证书经实际 Lean 检查后才进入 C；连接通过才替换原题 O。O 为空后从证明树组装，再独立编译原声明并审计公理。恢复重新验证四份证书并再次验收原题，没有重复 CAS 或动作扣款。错误桥证明在真实 Lean 中被拒绝，父义务和独立局部证书保留。

这里四轮都是同一表示上的局部任务；identity 保持当前表示，选择器依据 C/O 选择下一任务。本轮没有实现 LLM 自主扩图或跨表示探索。

## 第二阶段

递推选择 `FQI-GAUSS-ALTERNATING`：其交替权重 Gaussian 有限和与现有二阶证书重建范围匹配。核心实际搜索零、一阶后构造二阶证书；系数来自本次输出，安全解析后独立核对有理残差，再复用纯数学生成器并重新编译。

本次通过的精确局部递推：

```lean
∀ {K : Type u} [Field K] (q : K) (m : ℕ), (∑ j ∈ Finset.range ((m + 2) + 1), (((-1) ^ j) * (FiniteQBenchmark.gaussian q (m + 2) j))) + (((-1) + ((q^m) * q)) * (∑ j ∈ Finset.range (m + 1), (((-1) ^ j) * (FiniteQBenchmark.gaussian q m j))) + (0) * (∑ j ∈ Finset.range ((m + 1) + 1), (((-1) ^ j) * (FiniteQBenchmark.gaussian q (m + 1) j)))) = 0
```

该运行是 C=1、O={original}、links=[]。恢复重验通过，保留 witness 头的错误证明被真实 Lean 拒绝；右端递推、两个初值及唯一性连接仍未完成，不能算整题证明成功。

方法能力与全部入口见 [METHOD_CAPABILITIES.md](METHOD_CAPABILITIES.md)。

| 等级 | 方法 | 当前含义 |
| --- | --- | --- |
| L3 | telescoping, recurrence | 真实 Train 局部 Lean 与残差状态；望远镜另有整题验收 |
| L2 | coefficient, interpolation, difference_ring, kernel_transform, spectral, determinant, macmahon | 真实数学核心，仅显式 typed core_request；没有自动 Train 导出或 Lean 桥 |
| L0 | product, noncommutative, combinatorial | 有结构契约；现有可独立部分只是规则选择，真实执行依赖缺口明确拒绝 |

L2 接口保留原始请求/返回、精确源码前后哈希、实际进程状态、成本与未验证候选，始终不向 C/O 导出成果。矩阵方法仅复用 `workflow/matrix_symbolic.py` 纯数学辅助，没有恢复旧 Agent 或 workflow 控制层。三个 L0 方法没有被假装成已接通。

## 验证与复现

修改前：144/144，通过，无失败或 skip，117.922 秒。最终：216/216，无失败或 skip，467.915 秒。原有测试文件哈希未改变，旧局部 smoke 同样通过。

```bash
python3 -m unittest discover -s agent_v2/tests -v
python3 -m agent_v2.tests.telescoping_smoke --output-root /tmp/agent_v2_local_fresh
python3 -m agent_v2.tests.closure_smoke --output-root /tmp/agent_v2_closure_fresh
python3 -m agent_v2.tests.recurrence_smoke --output-root /tmp/agent_v2_recurrence_fresh
python3 -m agent_v2.cli methods
python3 -m agent_v2.cli method-demo --method coefficient --input agent_v2/generated/closure_and_methods_20261111/method_adaptation/final_v2/coefficient/example_request.json
```

复现 smoke 时必须使用新的空输出目录，避免覆盖已有证据；如上述 /tmp 目录已经存在，请更换名称。实际命令、环境、逐轮证据与失败记录保存在 `generated/closure_and_methods_20261111/`。最终 smoke 目录为 `final_local`、`final_closure`、`final_recurrence`，其余方法取 `method_adaptation/final_v2`；不合并开发失败记录择优计数。测试替身只验证控制器边界，不计数学结果。

真实执行过：两道 Train 的上述闭环、恢复与错误证明检查；七个 L2 的合成核心正例、不适配与失败/超时；三个 L0 的结构与不可执行边界。没有读取 benchmark Test、调用模型 API、复用历史证明收据或运行全 Train 批测。

修改职责：`telescoping_closure.py` 与数学 checker 完成正式连接/端点/原题审计；Graph、Executor、loop、CLI 完成多轮选路、精确组装及恢复；`method_registry.py` 管理版本与能力；四个 recurrence 模块复用真实递推核心及局部 Lean 桥；`symbolic_methods.py`/`symbolic_worker.py` 提供有界纯符号适配。全部修改和新增文件列于同目录 `validation.json`，before/after 和 `changes.diff` 保留。

未完成：递推整题出口；七个 L2 的认证原题导出和局部 Lean 桥；三个 L0 的新执行接口；自动扩图和外部模型路由。当前成果支持继续逐项扩展，不表示这些能力已经实现。

其余十个方法按顺序完成 40 个验收场景。全部入口、请求范围、依赖缺口和未接的同族底层模式见 [详细能力矩阵](generated/closure_and_methods_20261111/method_adaptation/能力矩阵.md)。实际样例以外的参数与结构没有穷尽运行。

下一步建议：先完成递推右端、两个初值和唯一性连接，再为一个 L2 方法建立认证 Source 导出及局部 Lean 桥。

## 实际环境与 CLI 命令

Python 3.10.12 (main, Aug 31 2026, 10:18:17) [GCC 11.4.0]；SymPy 1.14.0；Lean `/home/hjy/.elan/toolchains/leanprover--lean4---v4.35.0-rc4/bin/lean`，SHA-256 `bf8d54e4714cc4b03d3f6bb34c83b7202b87e49c8bfcbff6895c085bb90ceb38`。

```bash
/usr/bin/python3 -m agent_v2.cli run --identity FQI-SRC-AP-3.3.9 --method telescoping --selector rule --max-steps 1 --seconds 600.0 --output-root /home/hjy/Project/finite_q_identity_catalog/agent_v2/generated/closure_and_methods_20261111/final_local/runs
/usr/bin/python3 -m agent_v2.cli resume --run-dir /home/hjy/Project/finite_q_identity_catalog/agent_v2/generated/closure_and_methods_20261111/final_local/runs/20261111T154534Z-531f8e40bd
/usr/bin/python3 -m agent_v2.cli run --identity FQI-SRC-AP-3.3.9 --method telescoping --scope full --selector rule --max-steps 4 --seconds 1800.0 --output-root /home/hjy/Project/finite_q_identity_catalog/agent_v2/generated/closure_and_methods_20261111/final_closure/runs
/usr/bin/python3 -m agent_v2.cli resume --run-dir /home/hjy/Project/finite_q_identity_catalog/agent_v2/generated/closure_and_methods_20261111/final_closure/runs/20261111T154534Z-d8d4e0eba6
/usr/bin/python3 -m agent_v2.cli run --identity FQI-GAUSS-ALTERNATING --method recurrence --scope local --selector rule --max-steps 1 --seconds 1200.0 --output-root /home/hjy/Project/finite_q_identity_catalog/agent_v2/generated/closure_and_methods_20261111/final_recurrence/runs
/usr/bin/python3 -m agent_v2.cli resume --run-dir /home/hjy/Project/finite_q_identity_catalog/agent_v2/generated/closure_and_methods_20261111/final_recurrence/runs/20261111T154534Z-a9d0a6c68f
/usr/bin/python3 -m agent_v2.cli run --identity FQI-SRC-AP-3.3.9 --method recurrence --scope local --selector rule --max-steps 1 --seconds 1200.0 --output-root /home/hjy/Project/finite_q_identity_catalog/agent_v2/generated/closure_and_methods_20261111/final_recurrence/mismatched-runs
/usr/bin/python3 -m agent_v2.cli core-demo --input /home/hjy/Project/finite_q_identity_catalog/agent_v2/generated/closure_and_methods_20261111/final_recurrence/recurrence_core_request.json --seconds 1200.0 --output-root /home/hjy/Project/finite_q_identity_catalog/agent_v2/generated/closure_and_methods_20261111/final_recurrence/symbolic-runs
```
