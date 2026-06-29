# 决策:演示任务 + 组件选型(demo-task-selection)

> 状态:**criteria + 候选清单已写(2026-06-29,Task 5)**;诊断/生成的最终选定由 Task 6(诊断 spike)/ Task 7(生成选型)回填,Task 8 加"决策摘要"块收口。
> 这是 Plan 1 的最终输出,被 Plan 2(MVP 搭建)直接消费。依据:[../alignment-gaps.md](../alignment-gaps.md)(对齐缺口)+ [../generality-map.md](../generality-map.md)(选 COCO 小目标行)+ [gen-toolkit.md](gen-toolkit.md)(本地已验证工具)。

## 1. 已固定的决策(不再讨论)

- **演示任务 = COCO 小子集的"小目标"切片**(small-object slice)。理由见 [../generality-map.md](../generality-map.md) 的读出结论:最低风险代表行,有现成 size-specific AP 度量镜,所有候选生成器都在 COCO/类似规模验证过,且承载锚点核心难点。
- **成功标准 = 闭环跑通 + 结果可解释**;**up / flat / down 都算有效**(不是"必须涨点")。闭环靠"重新诊断"闭合,所以诊断输出必须可重复测量。
- **不做新方法**:不设计新架构、不自研新算法(一个月预算)。全部用现成组件组装。
- **对齐为平局决胜,不是唯一标准**(见 [../alignment-thesis.md](../alignment-thesis.md)):别为了好对齐选弱诊断/弱生成。

## 2. 选型标准表(诊断端 × 生成端)

| 标准 | 诊断端 | 生成端 |
|---|---|---|
| 粒度 | 逐实例、可定位的切片 | 在该粒度可控(layout / 框 / 掩码) |
| **对齐(核心)** | 输出能直接当生成条件 | 控制接口能消费诊断输出 → 桥最轻 |
| 检测就绪 | 切片带样本 id + 度量 | 产出图像 + COCO-json 标注 |
| 覆盖失败模式 | 能切出小/遮挡 | 能渲染小/遮挡且标注正确 |
| **可复现 / 可跑** | 仓库能跑(spike 验证) | 权重就位、本地已验证 |

## 3. 候选清单 + 当前已知状态

### 诊断端候选(状态由 Task 6 的 spike 回填)

| 候选 | 表示 / 对齐就绪度 | 原子 | 当前状态 |
|---|---|---|---|
| **HiBug2** | 属性文本切片;对齐就绪度**中**;能预测验证集外切片 | [[chen2025-hibug2-error-slice-discovery]] | ✅ **开源** [cure-lab/HiBug2](https://github.com/cure-lab/HiBug2);**主候选,待实测**(输出 schema 需 recon) |
| **TIDE**(互补) | 框级 6 类误差 + 各自 mAP 隔离贡献(选"哪类失败") | [[bolya2020-tide-detection-errors]] | ✅ **开源** [dbolya/tide](https://github.com/dbolya/tide)(pip `tidecv`);**待实测** |
| **COCO 度量切片器**(互补) | per-size AP / 未匹配实例框 → grounded 失败框 | —(pycocotools 自建) | **待实测**;兼作兜底 |
| GH-ESD | 实例级 grounded 切片;对齐就绪度**高** | [[zhang2026-gh-esd-instance-slice-discovery]] | ✗ **无官方代码出局**(数据集称录用后放,repo 未见;待放码再评) |

> **诊断端:尚未敲定(2026-06-29)。** GH-ESD 对齐最优但无代码 → 出局(同 ODGEN)。当前**待验证的工作假设**:用全开源的 **HiBug2(属性切片)+ TIDE(选失败类型)+ COCO 度量切片器(取漏检框做 grounding)** 组合,DIY 出 GH-ESD 想要的 grounded 实例切片,直接喂生成器的 `{box, caption}` 接口。**三者尚未逐一上手实测**,需先 clone HiBug2 看输出 schema、跑通 TIDE/度量切片器后再决定是否成组采用——故此处只记录方向,不作最终决策。

### 生成端候选(状态由 Task 7 的选型回填;本地状态据 [gen-toolkit.md](gen-toolkit.md))

| 候选 | 控制接口 / 对齐就绪度 | 原子 | 当前状态 |
|---|---|---|---|
| **GeoDiffusion**(COCO-512) | 框/layout→检测图;对齐**中**(box-only,无逐实例文本) | [[chen2023-geodiffusion-geometric-control]] | ✅ 本地验证可用(`geodiff` env;输入框≈输出 GT;画质受 SD1.x 限,近景大人脸弱) |
| **SDXL-Inpaint** | 区域 inpaint;对齐**中** | —(工具,见 gen-toolkit.md) | ✅ 本地验证可用(`flux2` env;~4.6s/张;物体略溢出框) |
| **InstanceDiffusion** | 逐实例 框/点/掩码+文本;对齐**高**(最接近缺口需要的接口) | [[wang2024-instancediffusion-instance-control]] | ✅ **验证可用**(`instdiff` env;官方 + 电梯锚点 demo 跑通,2026-06-26;见 [gen-toolkit.md](gen-toolkit.md)) |
| **ODGEN** | object-wise 文本+视觉,含遮挡;对齐**高但需逐域微调**(域内 +25.3 mAP) | [[zhu2024-odgen-detection-generation]] | 未搭建 |

## 4. Task 7:生成端按 5 条标准打分 + 决策(2026-06-29)

打分:✅满足 / ◐部分 / ✗不满足。5 条标准见上表(能跑 · 对齐 · 粒度 · 失败模式(小/遮挡)· 检测就绪)。

| 候选 | 1 能跑 | 2 对齐(核心) | 3 粒度 | 4 小/遮挡 | 5 检测就绪 | 小结 |
|---|:--:|:--:|:--:|:--:|:--:|---|
| **InstanceDiffusion** | ✅ 本地+锚点跑通 | ✅ 逐实例 框+文本=诊断语言 | ✅ 逐实例 | ✅ 电梯 demo 已现遮挡;小目标可控(SD1.5 画质顶) | ◐ 图+框;**框贴合度待复核**才能出紧致 GT | **当前胜出**:硬门槛全过,对齐+粒度最高 |
| **MIGC++** | ◐ 开源,安装中(另窗) | ✅ 逐实例 框&掩码+文本/图像属性 | ✅ 逐实例 | ◐ 治属性串味;遮挡未单独验证 | ◐ 图+框(同 InstDiff,待复核) | 同类强候选;**SDXL 权重画质或更优**;待横评 |
| **3DIS / 3DIS-FLUX** | ◐ 开源,安装中(另窗) | ✅ 深度解耦逐实例 | ✅ 逐实例 | ✅ **深度解耦→遮挡 native**;Flux 画质高 | ◐ 图+框(待复核) | InstDiff 的**潜在升级**(遮挡+Flux);待横评 |
| **GeoDiffusion** | ✅ 本地 | ◐ box-only,无逐实例文本 | ◐ 框级(无逐实例属性) | ✅ 输入框≈输出 GT,含遮挡深度序;近景大人脸弱 | ✅ 为检测造数据,框=GT | **兜底首选**:框正确性最稳 |
| **SDXL-Inpaint** | ✅ 本地 | ◐ 区域 inpaint,非逐实例 spec | ◐ 区域级 | ◐ 真实图改区域;**物体溢出框,非紧致 GT** | ◐ 框需反检测 | 备选:强画质弱框 |
| **ODGEN** | ✗ **无官方开源代码** | ✅ 高(但需逐域微调) | ✅ object-wise | ✅ 多类+遮挡(域内 +25.3 mAP) | ✅ 检测向 | **淘汰**:Apple 论文未放码,无法搭建 |

### 决策(暂定 — 待横向对比定稿)

**当前选 [[wang2024-instancediffusion-instance-control]](InstanceDiffusion)作 MVP 生成器的工作基线;MIGC++ 与 [[zhou2024-3dis-depth-decoupled-instance]](3DIS)正在另一 CC 窗口安装,与 InstDiff/GeoDiffusion 做横向对比后定稿。**

- **InstanceDiffusion 现状最稳**:硬门槛全过(1 能跑 / 4 小+遮挡 / 5◐),对齐(2)+粒度(3)最高,已在**锚点电梯场景**跑通(含遮挡)。横评出结果前,它是默认基线,不阻塞主线。
- **横评要看的两件事**:(a) **画质**——MIGC++(SDXL)、3DIS-FLUX(Flux)天花板可能高于 InstDiff(SD1.5);(b) **遮挡 + 框贴合度**——3DIS 的深度解耦对锚点"被遮挡电瓶车"可能更准。谁在"对齐不降级"前提下画质/遮挡更好,谁就接替基线。
- **ODGEN 淘汰**(无官方开源代码,见上表);SDXL-Inpaint 框不紧致,作画质备选。
- **兜底 = GeoDiffusion**(已验证、框正确性最稳):若上述逐实例引擎的**输入 bbox↔渲染目标贴合度**都复核不过关,退回 box-only 路线。
- **遗留给 Plan 2 的前置检查**:对最终选定引擎量化输出框贴合度(IoU(输入框, 渲染目标)),决定是否需要"渲染后反检测校正框"的轻步骤。
