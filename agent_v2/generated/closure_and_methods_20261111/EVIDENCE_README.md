# 精选发布证据

这些文件摘自 2026-11-11 的实际验收，随 2026-11-12 发布保存：216 项测试全通过；望远镜原题完整通过；递推只通过局部 Lean；其余十方法的 40 个场景通过。详情见上层 [验收报告](../../CLOSURE_AND_CAS_REPORT.md)。

本目录仅发布摘要、测试日志、环境与源码哈希、方法边界、复现脚本及十个输入样例。完整的 rounds、resume_checks、before/after、候选编译目录、工具链缓存和开发失败日志保留在原开发环境。JSON 内的绝对路径、产物清单和相应哈希记录当时的执行，不表示这些完整产物也已上传，更不能代替新的 Lean 验证或当作可移植断点。

`method_adaptation/validate_adaptations.py` 可在新空目录中复现十方法的纯符号接口检查；真实 Lean 检查请运行 `agent_v2.tests.telescoping_smoke`、`closure_smoke` 和 `recurrence_smoke`，指定新的 `--output-root`。完整复现命令见验收报告。

历史 `final_frozen_hashes.json` 保留验收时的 65 文件哈希。发布时仅追加报告／证据，并更新 `agent_v2/PUBLISHING.md` 中过时的能力说明；没有修改通过测试的生产代码或测试。
