数学工具库 v1
==============

用途与表示
----------
把数学对象的含义、局部性质、适用条件和 Lean 依据放在一个公共位置，供方法查询。
计算信息保存在 catalog.py 的带类型表达式树中，可直接导出 JSON；求解器无需先解析
Lean 证明再获得这些信息。lean/Rules.lean 提供相应定义等式或基础引理。

流程：原声明 → 现有 Lean 表达式提取器 → 查询工具库 → 方法内部表达式与条件
      → 原有符号算法构造证书 → 原有 Lean 出口验证完整原声明。

库本身不做方法分类，不搜索最终证明，不收录题号到答案的映射。
它复用 benchmark/lean/Benchmark 下已有的对象定义。论文
2607.01544v3(研究的东西和我特别像).pdf 第 3.2 节和第 8 节提供的是建设基础数学库、
让后续证明使用该库的思路；本文档没有把论文描述为通用符号适配器的实现。

当前内容
--------
9 个注册对象，18 条规则；名称均对应实际 Lean 声明。

对象/结构          规则与含义
poch               有限乘积定义、零长度、长度递推、切段、参数移位交叉式、带条件商式
pochList           空参数表与非空参数表的定义展开
rogersSzego         Gaussian 系数有限和定义
phi、phiTerm       有限基本超几何和及其逐项表达式
baileySum          保留任意序列 alpha 的有限和定义
geometric          幂的有限和定义
unitBailey         零长度与 n ≠ 0 分支
gaussian           局部 Pascal 递推
Finset.sum         自然数 Ico/Icc 区间到 range 的表示规则

Finset.sum 是额外的标准结构规则，不计入上述 9 个自定义对象。
这些规则是定义和局部基础性质，未复制其他方法的证书搜索算法。

机器规则包含：id、subject、purpose、参数类型、代数结构要求、lhs/rhs、requires、
Lean 引理名称与源码位置。Nat 减法/除法、整数幂和域运算分别标记。
例如 poch_shift_quotient 必须保留 poch a q d ≠ 0；其无除法版本
poch_shift_cross 不要求该条件。不能用 q ≠ 0 替代前者的非零条件。

查询与使用
----------
在仓库根目录运行：

  python3 -m finite_product_framework.math_library lookup poch --purpose length_shift
  python3 -m finite_product_framework.math_library lookup Finset.sum --purpose interval_to_range
  python3 -m finite_product_framework.math_library export

也可以在 Python 中直接使用，不启动 Lean：

  from finite_product_framework.math_library import Library
  lib = Library()
  description = lib.lookup('poch', 'parameter_shift_quotient')
  bindings = {name: {'op': 'var', 'name': name} for name in ('a', 'q', 'd', 'k')}
  candidate = lib.instantiate('poch_shift_quotient', bindings)
  # candidate['status'] == 'conditions_unresolved'
  # candidate['requires'] 给出不能省略的非零条件。

命令行实例化读取一个 JSON 文件：

  {"rule": "poch_zero", "bindings": {
    "a": {"op": "var", "name": "a"},
    "q": {"op": "var", "name": "q"}
  }}

  python3 -m finite_product_framework.math_library instantiate request.json

查询 unknown 表示库中暂无该项。candidate 只表示得到候选转换；调用者提供的 facts
只用于结构匹配，不是证明证书。所有候选的 proof_status 都是 requires_Lean_replay。
库核对模板类型和输入树形状，但动态输入的实际类型、假设和等式仍由 Lean 检查。

独立验证数学库
--------------
以下命令要求输出目录尚不存在，并使用仓库 project 中固定的 Lean/Mathlib 环境：

  python3 -m finite_product_framework.math_library build --output /tmp/fqi-library-build

它构建 Benchmark.MathLibraryAtoms/MathLibraryRules/MathLibraryChecks，逐条验证
机器模板与 Lean 引理一致，审计全部 18 条规则的公理并保存 manifest.json。
manifest 记录目录哈希、源码哈希、编译产物哈希和 Lean 路径。
geometric 从原始文件提取准确的定义，记录来源哈希，不导入该文件所依赖的已完成
题库证明。其他对象从 Benchmark.Definitions 取得。

manifest 的 verified_catalogue 仅表示这份规则目录验证通过，不表示任何原题已证明。
独立构建不调用符号求解器，不调用 API，也不运行 Train/Test。

现有程序接入位置
----------------
1. p1/lean_pipeline.py 与 product/pipeline.py 的表达式提取器由注册对象签名扩展，
   检查完整应用的参数数量，记录 math_library_query.json。
2. p1/source_ir.py 的有限和候选从库取得 phi、rogersSzego 等的定义表示，替换原先
   散落的公式拼装；phiTerm/pochList 的字面参数表也由同一目录展开。
3. p1/general_summation.py 当前自动展开的新入口是 geometric。原 phi/Rogers–Szegő
   路线继续沿用已有证明重建。转换轨迹、原始表达式和目录哈希进入 model/plan。
4. 库文件加入使用方依赖清单。原有证书构造算法、原声明验收及公理审计仍负责
   判定整题是否成功。乘积方法仅共享表达式提取器，仍使用自身的构造与证明出口。

其余已收录局部关系目前可查询/实例化，并不意味着十二个方法已经自动使用所有规则。
尤其没有自动接通参数移位商式选择、一般区间转换或 unitBailey 的分支搜索。
新增规则的 Lean 模块可独立导入；当前方法对定义展开的等式由已有原声明出口核验，
不会仅凭目录中写了一个 Lean 引理名称就接受转换结果。

已验证与边界
------------
完整验证命令（新建独立输出目录）：

  python3 -m finite_product_framework.math_library.check --output /tmp/fqi-library-check
  python3 -m unittest finite_product_framework.math_library.test_library -v

验证包括带类型规则、公理、非零条件、篡改表达式、q=0/q=1、空范围、反向自然数
区间、变量捕获和 phi 的实际源表达式（含负整数幂）。合成 geometric 原题经过现有
望远镜求解器和完整原声明 Lean 验收；去掉 q ≠ 1 的合成假命题被拒绝。乘积方法
的现有切段原声明也做独立回归。测试产物见 generated/math_library_v1_20261021。

本轮不提供 Train 成功率结论，没有启动 Train/Test 批测。
目前仍有以下明确限制：
- 任意未知函数只保留符号；baileySum 的 alpha 不被猜测成某个已知序列。
  当前有限和核心仍不能处理一般 alpha，所以可解释定义不等于能构造证书。
- phi 参数表展开要求字面 List；一般符号列表不直接展开。
- 条件自动证明、合取/量词分解、多重和、多基底和更广函数族仍受各方法现有边界限制。
- 按完全限定名或显式注册短名查询，不按相似拼写猜测对象含义。
- 工具库不会把“认识对象”标成“方法适用”或“原题已证明”。

扩展方法
--------
先确认对象在原声明中的定义和类型，再在 OBJECTS/RULES 中登记有类型模板与条件；
在 lean/Rules.lean 添加同名基础引理。运行 build 检查目录与引理一致，再验证实际
实例化后的表达式及必要的边界/反例。最后让具体方法调用该表示并完成原声明出口。
不要只加一个名称或函数签名就宣称方法支持该结构。
修改规则或转换程序后必须重新构建并绑定新的目录/依赖哈希；已有实验快照保持冻结。
