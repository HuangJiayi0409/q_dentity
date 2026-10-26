# 四家族 Benchmark（2026-10-18）

共 446 条题目，Train 346 条、Test 100 条。新划分使用 A、C、F、G 四个家族；G 合并原 B、D、E。旧版 `benchmark/` 已删除，当前目录为保留版本。

| 家族 | 总数 | Train | Test |
|---|---:|---:|---:|
| A · 超几何型有限求和 | 253 | 196 | 57 |
| C · 递推与差分关系 | 67 | 52 | 15 |
| F · 有限乘积与局部代数关系 | 74 | 58 | 16 |
| G · 差分域／环、参数关系与生成函数 | 52 | 40 | 12 |
| 合计 | 446 | 346 | 100 |

沿用已确认的修订版难度标签；本轮按家族比例分层，不另外设置难度配额。

| 难度 | 总数 | Train | Test |
|---|---:|---:|---:|
| 低 | 84 | 65 | 19 |
| 中 | 255 | 201 | 54 |
| 高 | 107 | 80 | 27 |

入口：[Train 题目索引](TRAIN.md)、[Test 题目索引](TEST.md)、[完整划分表](splits/all_446.csv)。
清单为 `splits/train.jsonl` 和 `splits/test.jsonl`；带公式、条件及各来源原式的数据为同目录的 `train_problems.jsonl` 和 `test_problems.jsonl`。
每题 Markdown 位于 `formulas/train/` 或 `formulas/test/`。逐题 Markdown 保留无证明提示的题目文本；另外迁入旧 benchmark 的全部 Lean 声明和共享辅助模块。目标定理仍保留 `sorry`，不是已完成证明。

划分规则：以 100/446 的比例计算四家族整数配额，最小化配额平方误差；固定种子 20261018，按已有 391 个关联组整体抽取，首个满足精确配额的结果即固定。已记录关联边不跨集合；该隔离依据已有记录，不表示穷尽所有数学等价关系。不参考旧系统证明结果，也不要求新旧成员相同。

公式和条件来自原目录，保留不同来源的参数域与变量对应。共同记号见 [NOTATION.md](metadata/NOTATION.md)。部分题目的原始辅助定义引用指向当前仓库中缺失的 `round1_source_collection/`；本次保留出处并在 [定义引用清单](metadata/definition_references.json) 标明可用性，没有重构这些辅助文件，不能把这次题目划分视为已完成自包含声明整理。

难度采用修订版 V2 的 84 条低、255 条中、107 条高；源标注的待复核状态仍保留在元数据中。本轮不重新评定难度。

重建：`python3 benchmark_four_families/scripts/build_split.py`

只读校验：`python3 benchmark_four_families/scripts/build_split.py --check`

校验覆盖 446 个唯一 ID、346/100 数量、四家族配额、难度标签、关联组及关联边隔离、源文件哈希和所有生成文件的一致性。生成器只写入本目录。

## 形式化迁移

沿用旧目录的 `formulas/`、`splits/`、`metadata/`、`lean/`、`formalization/` 和 `scripts/` 布局。已确认的划分冻结在 `metadata/frozen_split.json`；重建必须逐项匹配，不会重新选择成员。

446 条声明按原公式 ID 对应迁入 `lean/Benchmark/Statements/Train/`（346 条）和 `Test/`（100 条）。保留 Identity 编号、命名空间和定理内容，仅更新文件内的公式路径注释；重建 `Benchmark/Train.lean`、`Test.lean` 的 imports。工具链、依赖锁和共享模块沿用旧版，不复制缓存或已有证明运行结果。旧 benchmark 已删除；重建仅使用本目录的冻结输入和原公式目录。

`metadata/lean_statements.json` 与两份 split 清单记录新路径、新哈希及原批次。迁移来源、旧新集合和逐文件哈希见 [migration.json](formalization/migration.json)。原五批数学审阅和编译记录归档在本目录 `history/formalization/`，是历史证据，不是新划分的测试成绩。

迁移后的完整类型检查：`python3 benchmark_four_families/scripts/check_lean.py --workers 8`。检查依赖顺序、全部声明及总入口，复用项目 mathlib 缓存；新编译产物和日志只写入本目录。结果见 `reports/lean_validation.json`。`sorry` 警告符合原目标证明待完成的约定，类型检查通过不表示证明完成。

结构校验也可运行：`python3 benchmark_four_families/scripts/validate_split.py`。
