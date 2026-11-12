# 残差驱动的自主证明入口

`auto` 在现有 `s=(G,Γ,r,C,O,b)` 上逐轮运行。它允许 CAS 提供独立局部证书，再由模型证明当前义务、构造辅助引理，或提出最多三个子目标并证明它们到当前目标的连接。所有结果先经过 Lean；原题只有在最终重新编译和审计通过后才算成功。

## 运行

在项目根目录执行：

```bash
python3 -m agent_v2.cli auto \
  --identity FQI-SRC-AP-3.3.9 \
  --methods all --selector rule \
  --seconds 1200 --action-seconds 180 \
  --max-steps 12 --max-model-calls 8 \
  --output-root agent_v2/generated/autonomous_runs
```

需要真实模型服务。默认从项目根目录 `API_GPT` 读取模型接口与密钥，使用已配置的 `gpt-6-astra`、`high` 推理设置。可用 `--model`、`--model-credential`、`--model-endpoint` 显式设置。密钥不写入提示词或证据；公开端点、模型、请求、响应及服务实际返回的 usage 会记录。模型客户端不自动重试 HTTP 请求。

`--selector jev` 使用 `API_Jev` 中的凭据，经 TypeSafe 有类型选择接口，从程序已经过滤的候选中选择一项。只有一个候选时直接执行；服务异常、非法选择或置信度低于 0.5 时回退规则选择，并在 `selection.json` 明确记录。回退不能计作 Jev 成功选择。两种选择器均只决定当前一步。

```bash
python3 -m agent_v2.cli auto \
  --identity FQI-FINITE-Q-BINOMIAL --selector jev \
  --seconds 1200 --max-steps 12 --pause-after 1

python3 -m agent_v2.cli resume --run-dir /绝对路径/本次运行目录
```

`--pause-after` 只暂停本次调用，不增加总预算。恢复时重新核验所有已保存证书，沿用原接口配置、调用计数和剩余预算。源代码、源题或冻结依赖发生变化时，旧运行拒绝恢复；应创建新运行。

复现受控的“模型新表示 → CAS”接线检查（会调用真实模型，最多两次）：

```bash
python3 -m agent_v2.tests.autonomous_expansion_smoke --execute \
  --seconds 1200 --action-seconds 480 --max-steps 4 \
  --output-root agent_v2/generated/controlled_expansion
```

去掉 `--execute` 只准备输入和检查点，不调用模型。该驱动明确指定首个扩展动作与所需子目标结构，随后回到普通规则调度；它不提供证明文本，也不伪装成自主选路实验。

## 每轮怎样推进

1. 从 Train 原声明重建闭合命题，分别检查所选方法的实际输入契约；仅适用的方法获得初始 CAS 出口。`--methods` 可指定逗号分隔的方法列表。
2. 根据当前 `r`、开放义务 `O` 和已验证证书 `C` 生成合法联合动作。预算不足、重复失败、已完成局部任务、错误来源或未验证的连接会被过滤。
3. CAS 接收原题结构和所选任务。对新子目标，只允许与该方法实际支持的局部命题精确匹配；不把任意子目标偷偷改回原题求解。
4. 模型收到当前目标、证书的类型和安全引用名称、基础数学库声明类型、真实 Lean 反馈。它返回一个证明项，或“子目标列表＋子目标推出父目标的证明项”。模型不指定源文件、导入或原题假设。
5. Lean 用固定环境检查命题、证明、依赖、宇宙参数与公理。通过的证书进入 `C`；只有连接证明通过后才修改 `O` 和加入表示节点。失败保留原有证书和待证义务。
6. 现有路线耗尽后，可增加有反馈的修复或扩展请求；后续仍须经过同样的验证。最终 `O` 为空时，重建证明树并独立检查原始 theorem。

## Graph 的边

`identity` 严格保持当前节点。`decomposition` 对应已经验证的证明树连接；多子目标分解必须保留所有开放兄弟目标，单个子目标不被当作与原题等价。`focus_obligation` 显式切换到同一已验证证明树中的另一个开放目标，只改变工作位置，不声称数学等价。普通蕴含转换仍需精确匹配的已验证桥。

Graph 保留历史节点、边和失败记录。新节点来自当前实际证明状态，不预先写好整条证明路线。当前扩展采用“先验证子目标到父目标的连接，再登记子目标”的形式；尚无任意未验证符号表示之间的自由转换。

## 预算与证据

总墙钟包含初始化、库查询、选路、CAS、模型、Lean、保存及恢复重验。每次执行消耗一个动作；模型 HTTP 次数另有上限。在调用前原子保存预算和调用预留，崩溃后的未知请求按保守计数处理，不盲目重发。

`--max-repairs` 限制因反馈新增的修复出口数；`--max-expansions` 限制路线耗尽后新增的扩展出口数。它们不等于数学子目标数量。所有正常模型动作及其主动分解都仍受 `--max-model-calls`、动作数和墙钟限制。

每轮保存状态前后、合法与被过滤候选、选择、实际请求响应、原始后端结果、Lean 检查及残差更新。`graph.json` 可检查真实表示和连接；原子 checkpoint 同时包含任务注册表、Graph、残差、接口配置和调用计数。`run.json` 的 `original_identity_proved` 是结果入口，不能以 CAS 找到证书、模型给出代码或局部 Lean 通过替代。

## 当前能力边界

数学方法仍保留原来的结构范围和证书翻译限制。默认扫描十二种注册方法不表示十二种方法都适用于当前题目，符号候选也不自动成为 Lean 证书。

生成证明采用严格限定的 Lean 数学语法与纯 tactic 白名单；没有开放任意 Lean 元编程、IO、插件、`sorry` 或 `native_decide`。当前原题翻译采用已有正式 Source 配置；只有符号入口、没有正式原题翻译的结构会在模型调用前明确停止。Library 是有限的真实声明类型库，不是全库语义检索器。

原有 `run --method ... --scope local/full` 保留固定单方法行为。新入口不使用已遗弃 Agent，不访问 benchmark Test，不自动启动全 Train 批测。
