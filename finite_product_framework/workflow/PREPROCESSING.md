# 十二方法与公共预处理的接入

使用显式 `--preprocess` 开关启用新路径。默认路径仍保留历史行为，旧 4152 项批测和 23/346 基线不被覆盖。新路径解除旧三类方法的历史家族/名单准入条件，只允许当前 Train；后端的实际数学输入范围不随之扩大。

## 调用

```bash
python3 finite_product_framework/prove_product.py \
  --identity FQI-POCHHAMMER-RESIDUES \
  --preprocess \
  --output-root finite_product_framework/generated/product_preprocessed
```

十二个独立入口均使用相同开关，仍由调用者明确指定方法。兼容入口 `prove.py` 也支持该开关；没有分类器或跨方法自动选择。

后续全量批测的命令接口是：

```bash
python3 finite_product_framework/batch/train.py \
  --run-dir finite_product_framework/generated/train12_with_preprocessing \
  --workers 24 --preprocess
```

**本次没有执行上述全量批测。** 只对调度器运行了独立目录中的 `--prepare-only` 检查。使用新目录，续跑时必须保持预处理开关、并发和冻结源码一致。

## 实际数据通路

```text
原题快照
  → 公共预处理（输出标准表示与等价证明，独立回放）
  → 方法侧加载同一原题的完整依赖
  → preprocess_enter：读取标准目标并检查等价证据
  → 选定方法自己的读取器、符号算法与证明重建
  → Eq.mpr 将新目标证明连接回原目标
  → 原声明 Lean 编译、公理审计及历史恒等式依赖检查
```

`workflow/preprocessed.py` 是方法侧的接入代码，负责依赖环境和原题证明位置。它不改变预处理规则，不产生某个算法专属的等价公式。现有方法暂时通过 Lean 中的同一个标准目标读取表达式，并不是每个 Python 求解器都直接解析公共 DAG；各方法已有的读取范围仍可能导致明确拒绝。

`preprocess_enter` 在分析和证明两个阶段都执行。它核对原上下文、标准目标与证明项，通过内核检查后创建标准目标的证明义务，并用 `Eq.mpr` 连接到原目标；原题声明文本保留。预处理失败会停止该次方法调用，不静默回退到旧原题。日志 `preprocessing_consumed.json` 记录方法实际消费的标准目标结构哈希。

完整加载原始共享文件可能同时带入历史恒等式。因此，预处理模式下的成功结果还必须通过 `auditCompleted`：递归检查实际证明依赖，拒绝调用 `Batch*Proofs`、`BatchAuxiliary`、`InitialValues`、`Representation` 或 `Statements` 中的既有定理；允许原有通用 Gaussian/Auxiliary 支持引理和方法自己的证明规则。该策略较保守，可能拒绝一些合法但尚未单独审查的共享引理，不能绕过审计计成功。

## 预算与产物

`--preprocessing-seconds` 默认 600 秒，计入 `--seconds` 默认 900 秒的总预算。独立 worker 的进程组超时覆盖 Lean 子进程。预处理当前会重新编译依赖；尚未构建跨题/跨方法缓存，因此新路径的总耗时包含这部分开销。

每次调用的 `report.json` 增加 `preprocessing` 阶段；完整输入产物保存在该次调用的 `preprocessing/input/`。方法分析和证明分别保留原有结果格式，成功时还保存 `preprocessing_acceptance.json`，绑定原题、原证明及等价证据的哈希。

转换成功不等于方法适用，更不等于原题证明成功。`FQI-BAILEY-INVERSION` 的接入样例通过预处理并进入递推入口后，仍因旧 P1 读取器不支持 `alpha 0` 而明确拒绝；这类结果不能记作数学不可证明。

## 验收证据

本轮三个完整原题调用通过：`FQI-POCHHAMMER-RESIDUES`（乘积）、`FQI-SRC-KAC-CHEUNG-4.4`（递推）、`FQI-SRC-GR2-II-34`（双基望远镜）。第三题发生了三步实际整理：Pochhammer 列表构造子拆分、空列表化简、单位因子化简。三个结果均通过原声明验证与额外依赖审计；它们均属于既有基线成功题，不计作新增覆盖。

记录位于 `finite_product_framework/generated/preprocessing_connection_20261018/`（项目根相对路径）：

- `synthetic_v3/validation.json`：9 项转换、回放、条件与篡改检查。
- `dependency_audit/validation.json`：自建证明通过、借用历史定理拒绝、`sorryAx` 拒绝。
- `all_method_analysis/validation.json`：同一份标准目标经十二个实际分析入口的连接检查，不代表十二种方法都适用或证明成功。
- `final_*/`：少量当前 Train 原题的完整调用结果。
- `validation.json`：本轮汇总，包括范围、已通过检查和未执行的全量评测。

新增 `test_preprocessing_connection.py` 覆盖十二入口证明位置、旧名单与新范围隔离、失败不继续以及证据篡改拒绝；已有 `test_workflow.py`、`p1/test_pipeline.py` 作为回归。原 `test_workflow.py` 中两个已移出当前 Train 的成员资格样例已改用当前 Train 样例，不读取 Test。
