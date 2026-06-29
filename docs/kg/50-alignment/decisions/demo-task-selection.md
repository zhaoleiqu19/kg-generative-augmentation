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
| **GH-ESD** | 实例级 grounded 切片;对齐就绪度**高**(最接近可直接当 spec) | [[zhang2026-gh-esd-instance-slice-discovery]] | 未 spike(Task 6 跑) |
| **HiBug2** | 属性文本切片;对齐就绪度**中**;能预测验证集外切片 | [[chen2025-hibug2-error-slice-discovery]] | 未 spike(Task 6 跑) |
| *兜底* | 无现成工具能跑时:**metric-based slicer**(per-size AP → 最差切片) | —(Plan 2 自建) | 限时盒到期则启用 |

### 生成端候选(状态由 Task 7 的选型回填;本地状态据 [gen-toolkit.md](gen-toolkit.md))

| 候选 | 控制接口 / 对齐就绪度 | 原子 | 当前状态 |
|---|---|---|---|
| **GeoDiffusion**(COCO-512) | 框/layout→检测图;对齐**中**(box-only,无逐实例文本) | [[chen2023-geodiffusion-geometric-control]] | ✅ 本地验证可用(`geodiff` env;输入框≈输出 GT;画质受 SD1.x 限,近景大人脸弱) |
| **SDXL-Inpaint** | 区域 inpaint;对齐**中** | —(工具,见 gen-toolkit.md) | ✅ 本地验证可用(`flux2` env;~4.6s/张;物体略溢出框) |
| **InstanceDiffusion** | 逐实例 框/点/掩码+文本;对齐**高**(最接近缺口需要的接口) | [[wang2024-instancediffusion-instance-control]] | ⏸ env 未建(gen-toolkit 记权重亦未下;Task 7 复核) |
| **ODGEN** | object-wise 文本+视觉,含遮挡;对齐**高但需逐域微调**(域内 +25.3 mAP) | [[zhu2024-odgen-detection-generation]] | 未搭建 |

> 选型逻辑预告(Task 7 执行):优先 **检测就绪 + 能处理小目标 + 现在能跑**,用**对齐**(控制接口能否直接消费 Task 6 的诊断输出)作平局决胜。若对齐最优者(如 InstanceDiffusion)未建,则记为 (a) Plan 2 前置的小型 build-probe,或 (b) 退回已验证模型(GeoDiffusion / SDXL-Inpaint)。
