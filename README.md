# 有限 q 恒等式 Benchmark 与十二种符号证明方法

本仓库副本导出自 2026-10-26 的当前项目，包含 benchmark、十二种符号证明方法及其公共依赖。原有方法源码和题库文件按字节保留；发布整理仅新增根目录说明、忽略规则和导出核验清单。

## 内容

| 路径 | 内容 |
|---|---|
| `benchmark/` | 题库数据、Train/Test 划分、Lean 声明、共享定义、构建与检查脚本，以及保留的元数据和历史说明 |
| `finite_product_framework/` | 十二方法入口、符号计算核心、Lean 证明出口、公共工作流、预处理器、选择器、数学工具库、方法测试和符号批测脚本 |
| `project/` | 固定的 Lean 工具链、Mathlib 依赖锁及基础工程配置 |
| `round2_identity_catalog/data/`、`families/`、`NOTATION.md` | benchmark 构建脚本直接引用的目录数据、定义与记号依赖 |
| `SOURCE_MANIFEST.json` | 每个原项目导出文件的相对路径、字节数与 SHA-256 |
| `UPLOAD_VALIDATION.json` | 此次源码导出的核验范围与结果；不代表新增数学证明成绩 |

题库当前说明记录 446 条题目，其中 Train 346 条、Test 100 条。目标 Lean 声明中的 `sorry` 是待证明位置，不表示已经得到证明。详见 [Benchmark 说明](benchmark/README.md)。

## 十二种方法

| 方法 | 入口 |
|---|---|
| 有限差分与望远镜 | `finite_product_framework/prove_telescoping.py` |
| 递推关系与唯一性 | `finite_product_framework/prove_recurrence.py` |
| 系数展开与有限卷积 | `finite_product_framework/prove_coefficient.py` |
| 有限乘积与指标等价 | `finite_product_framework/prove_product.py` |
| 插值、零点与有理函数主部 | `finite_product_framework/prove_interpolation.py` |
| 非交换算子等式 | `finite_product_framework/prove_noncommutative.py` |
| 加权双射与符号反转对合 | `finite_product_framework/prove_combinatorial.py` |
| 嵌套和积的差分环 | `finite_product_framework/prove_difference_ring.py` |
| 有限核变换与矩阵反演 | `finite_product_framework/prove_kernel_transform.py` |
| 有限谱正交 | `finite_product_framework/prove_spectral.py` |
| 行列式结构证书 | `finite_product_framework/prove_determinant.py` |
| MacMahon 有限分拆分析 | `finite_product_framework/prove_macmahon.py` |

各方法的适用域、证书与完整原题验收要求见 [框架说明](finite_product_framework/README.md) 和 [方法独立性原则](finite_product_framework/research/METHOD_IMPROVEMENT_PRINCIPLES.txt)。单个方法返回局部构造不等于完整原题已证明。

## 环境与入口

Lean 工具链为 `leanprover/lean4:v4.35.0-rc4`，具体依赖以 `project/lean-toolchain`、`lakefile.toml` 和 `lake-manifest.json` 为准。Mathlib 缓存不随源码上传，需要在使用环境中准备。

Python 符号计算使用 SymPy；导出环境中的版本为 1.14.0。部分多重求和计算使用可选的 `python-flint==0.9.0`，见 `finite_product_framework/p1/requirements-multisum.txt`。部分数域计算使用 PARI/GP，其项目内重建脚本为 `finite_product_framework/p1/setup_pari.py`；二进制和下载缓存不在此副本中。

可先查看具体入口参数：

```bash
python3 finite_product_framework/prove_telescoping.py --help
python3 finite_product_framework/prove_auto.py --help
python3 finite_product_framework/select_method.py --help
```

运行原题求解前须准备对应依赖和 Lean 环境。现有方法入口主要按 Train 题号加载输入。此次发布准备没有运行 Train 或 Test 求解，也没有重新执行完整 Lean 构建。

## 导出边界与已有路径限制

- 排除 API 凭据、裸模型 GPT/DeepSeek 测试运行器、运行输出 `generated/`、`.lake/` 缓存、`.tools/` 二进制、字节码和日志；保留十二方法及其相关源代码、测试和配置。
- 原文档中引用的历史运行产物未全部随源码导出。依赖旧 `generated/` 证据的检查脚本不能仅凭本源码副本回放原实验。
- `benchmark/scripts/build_split.py` 仍引用历史名称 `benchmark_four_families/inputs/`，而当前目录名为 `benchmark/`。导出保留此现状；使用该重建脚本前需提供兼容路径或修正对应引用。
- 部分原始定义出处指向当前项目本就缺失的 `round1_source_collection/`，详见 benchmark 元数据；此次导出没有补造这些来源。
- 保留现有第三方源码许可，例如 [QSUM 许可说明](finite_product_framework/p1/QSUM_LICENSE.txt)，没有替项目另行选择许可证。

Test 文件仅作为用户要求的 benchmark 内容复制和核验，不用于方法开发或能力评测。
