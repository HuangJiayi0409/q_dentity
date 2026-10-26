# 通用有限区间求和出口（2026-10-19）

本次补强原有 `direct_q_gosper` 与 `general_q_zeilberger`，不增加第十三类方法，不修改预处理或分类器。`general_summation.py` 负责源表达式适配和符号构造，`general_sum_emit.py` 负责非可信证明生成，`lean/GeneralSumRules.lean` 提供 Lean 已证明的有限区间组装与递推唯一性规则。

## 已通过专项验收的结构化乘积出口

`poch_recurrence_emit.py` 已接入同一递推入口。它保留原 `phi` 的整数幂类型，实际调用 q-Zeilberger 和 Ore 构造器，再由以下五层生成 Lean 证明：

1. 原表达式与有限和之间的定义展开等式；不替换原声明或按题号选择公式。
2. 独立验证最终局部证书，以及 Ore 左乘前的种子证书与左乘子。先提升通量本身，避免用移位被加数之比引入可去的分母零点。
3. `poch_intervals.py` 构造公共乘积区间；`PochShiftRules.lean` 通过无除法区间分解证明移位。所有长度等式、支撑范围、短前缀均保留为内核义务。分母非零由原题 `phiDefined` 或乘积分母假设的实际因子与子区间导出。
4. 保留每个移位的全部尾项；在区间尚未重叠的有限前缀逐项分支，检查全部递推初值，并调用有限阶唯一性定理。
5. 完整原声明编译与证明依赖审计。形式约分、局部伸缩或生成 tactic 均不算成功。

第五环节的生成器从当前乘积长度提取需要检查的前缀与末项索引；高阶递推不能只沿用一阶的固定索引。每条非零证据仍须由原假设及 Lean 的长度不等式推出，无法推出的证据不会成为前提。较长移位的局部有理恒等式使用 `as_aux_lemma` 封装为内核检查的辅助定理；短移位直接重建，以避免不必要的封装开销；这不跳过原声明或公理审计。

结构化 `general_recurrence` 的内部 Lean 验证上限为 600 秒、800 万 heartbeats，其他通用求和出口仍为 240 秒、400 万 heartbeats。外层任务总预算仍由调用者控制，原 900 秒批测预算没有改变；本轮没有启动批测。超时仅保留诊断输出 `lean_timeout.log` 并报告未验证，不计成功；因此不能把不同预算下的结果解释成纯算法提速。

本轮第五环节在下述声明范围通过专项验收：四道选定 Train 原题和结构化二阶出口完整通过，13 份成功证明重新接收核验通过。最终证据为 `../generated/recurrence_full_20261019/step5_validation.json`，使用 `audit_step5.py` 重新检查原声明、证明哈希和依赖；`step5_sources.json` 固定最终实现。12 项 Lean 规则、9 项结构化正反例、17 项通用求和、17 项 P1、21 项工作流及 10 项区间/证书代数检查通过。最终证据采用 `*_pruned` 目录；此前超时、失败或取消的诊断目录不计成功。通用奇异参数分支、任意长度/参数运动仍不能宣称完成。下方“当前边界”描述前轮基础出口；新增能力以本段和本轮实际验收记录为准。

## 符号构造和证明义务

- 旧 Gaussian 专用适配器仍优先；不在其输入语法内的目标才进入新适配器。正式 P1 调度和统一工作流分析入口已连接。另设五核心原题流程已按用户要求删除；当前使用十二方法入口，共享源适配和 Lean 打印工具位于 `source_ir.py`、`sum_lean.py`。
- 新输入为等式，至少一边是完整的单指标有限和；区间是 `range (a*n+b)`，其中 `a,b` 是非负整数，所有和共享同一个外层指标。支持的原子由现有 IR 定义。
- 直接伸缩调用实际 q-Gosper。证明生成前独立检查 `V R(qX)-R=1`；再尝试约去 `R F` 中的可消因子，最后由 Lean 在原声明的参数域验证局部差分和实际端点。形式约分本身不是证明。含参数的 Pochhammer 合成例子不添加 `a≠0` 或 `q≠0` 前提。
- 递推调用实际 q-Zeilberger 或多分量联合伸缩，最低搜索阶数为 1。每个分量都有局部证书；多分量采用一致缩放的 primitive relation。
- 等式两边分别构造关系，再用 q-Ore 的最小公左倍式取得共同关系。对原算子的左乘子也作用于局部证书，而非只修改递推系数。再次以源 IR 的实际分量检查残差。
- 有限和出口使用共同前缀 `a*n+b`，并保留第 `j` 个移位的全部 `a*j` 个尾项。没有偷偷假设尾项为零，也不以数值抽样代替边界证明。
- Lean 检查两边边界强迫项相等、全部初值以及递推应用范围。通用唯一性定理支持任意正有限阶、非首一关系；首项系数为零时要求额外证明。当前自动生成器尝试证明首项非零，尚不自动生成一般奇异分支的单独证明。

原题上下文和声明保留，只有延后证明槽被替换。成功须通过原声明 Lean 编译、公理检查和统一证据接收；局部证书构造成功不是原题成功。

## 适用范围与未支持输入

结构化乘积出口目前接在原有递推入口的 `phi` 等定义桥接分支上；没有把所有旧 `Finset.sum` 或直接 Gosper 输入迁到此出口。独立五核心流程已删除，不再列为待升级入口。这项区分决定了“局部规则已经具备”是否等于“某个原题入口已经能用”。

- 公共区间规则支持整数起点移位、短前缀和尾部，全部等式由 Lean 检查。`n-k` 长度及其尾因子的正例、缺支撑条件反例已验证；不能据此声称任意截断表达式的原题适配已完成。
- 原域非零条件从实际 `phiDefined`、乘积分母假设及子区间导出。目前的参数运输覆盖常量和非正整数倍的外层 q 幂移动；任意参数运动没有通用出口。
- Ore 左乘保留种子关系与种子通量，最终证书和种子证书分别核验。生成器检查全部初值及全部移动尾项；有限阶唯一性定理本身没有一、二阶限制，但资源预算和前端表示仍限制自动适用范围。
- 清分母同时转换原有的乘积非零证据。形式上约掉的因子不被自动认为非零，分母非零也不能从抽象有理函数域直接带入原参数域。
- 原题声明及参数假设不变。分母条件不能重建、首项存在无法处理的奇异分支或其他义务没有闭合时，结果必须是未证明。当前没有一般奇异参数分支的自动重建器。
- 任意负长度、min/max 截断、多重求和、一般分段目标、任意代数参数塔不在已验证的自动出口范围。

因此不能把这次贯通有限和证明链、或几道原题通过，描述成覆盖所有符号计算方法、解决大部分 Train 或任意 q-holonomic 输入已经完备。

## 验收

本轮证据目录：`../generated/general_summation_20261019/`。总验收以 `validation.json` 为准，合成正反例见 `regression/validation.json`，四道原题专项见 `train_pilot/validation.json`。没有运行全量 Train，没有读取 Test，未改变 benchmark 原声明。原基线和中断前源码快照保留。

可重放合成验收：

```sh
python3 finite_product_framework/p1/test_general_summation.py
python3 -m unittest discover -s finite_product_framework/p1 -p test_general_certificate.py
```

本轮结构化出口的可重放专项命令（先运行通用回归以建立依赖缓存）：

```sh
python3 finite_product_framework/p1/test_general_summation.py --output finite_product_framework/generated/recurrence_full_20261019/regression
python3 -m unittest discover -s finite_product_framework/p1 -p test_poch_intervals.py
python3 finite_product_framework/p1/test_poch_rules.py
python3 finite_product_framework/p1/test_poch_recurrence.py
python3 finite_product_framework/p1/test_poch_order.py
python3 finite_product_framework/p1/test_poch_train.py
```

`test_poch_train.py` 只选取四道已声明的 Train 专项原题，不运行全量 Train。Chu–Vandermonde 已在历史十二方法 23 题基线内，新出口接通不能再算整体新增；Pfaff–Saalschütz 不在该基线内。不同版本的生成/超时目录保留为诊断，成功与否必须匹配该次 `Proof.lean` 的哈希及验证结果。
