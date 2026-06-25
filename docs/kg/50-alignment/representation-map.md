# 对齐表:诊断输出 × 生成输入(representation-map)

> 核心轴 = **共享表示**。左=生成器的控制接口,中=与之对齐的诊断输出,右=桥要做的事 + 已有原子(wikilink 引用 `../90-papers/`)。宽调研每收一篇,就往对应行补。

## 表

| 生成控制接口 | 对齐的诊断输出 | 桥的工作量 | 已有原子(引用) |
|---|---|---|---|
| **框 / layout**(类别+bbox) | 框级 / 尺寸带 / 遮挡 / 定位误差 / 类混淆 | **极轻**:按失败的尺寸·遮挡配置发框 | 生成:[[wang2024-instancediffusion-instance-control]] [[zhou2024-migcpp-multi-instance]] [[li2026-occlusionformer-zorder]] [[chen2023-geodiffusion-geometric-control]] [[zhu2024-odgen-detection-generation]] [[zhang2023-diffusionengine-data-engine]] [[wang2024-detdiffusion-perception-aware]] [[zhu2025-recon-region-controllable]] [[tang2024-aerogen-remote-sensing-generation]] · 诊断:[[zhang2026-gh-esd-instance-slice-discovery]] [[bolya2020-tide-detection-errors]] [[chen2025-hibug2-error-slice-discovery]] [[miller2022-false-negative-mechanisms]] [[zimmermann2026-knowledge-guided-failure-prediction]] |
| **区域 inpaint**(背景+mask) | "哪个区域缺 / 漏检 / 易错" | **轻**:区域即 spec | 生成:[[petersen2025-scene-aware-location]] [[girella2024-diag-indistribution-defect]] · (诊断:漏检/区域类待补) |
| **自由文本 / 属性 prompt** | 自然语言属性切片 | **轻**:文本直通 | 诊断:[[chen2025-hibug2-error-slice-discovery]] [[eyuboglu2022-domino-slice-discovery]] [[chegini2023-clip-diffusion-failure-mitigation]] · 生成:[[ruiz2022-dreambooth-subject-driven]] |
| **实例掩码**(逐实例) | 像素 / 实例级失败 | 中:掩码↔实例对应 | 生成:InstanceDiffusion(待入库) · (诊断待补) |

## 现状速记(本地已验证的生成端)

- **框/layout**:GeoDiffusion(COCO-512,本地可跑;多框含遮挡落位准;画质受 SD1.5 限,近景大人脸弱)。详见 [decisions/gen-toolkit.md](decisions/gen-toolkit.md)。
- **区域 inpaint**:SDXL-Inpaint(本地可跑;柔边融合优于 copy-paste;物体会略溢出框)。
- **纯 T2I**:本地 Flux klein(不吃任何空间条件,仅作前景素材/copy-paste)。

## 观察(喂给宽调研的假设)

- **生成端框/区域两行已较成熟且本地在手**;**诊断端与之对齐的"框级/区域级、且为检测设计"的方法明显偏少**——这正是要重点宽调研的方向。
- 经典检测误差分类法(尺寸/遮挡/定位/类混淆)天然就是"框/layout"行的诊断输出表示——是该行最现成的**表示来源**(但需用近期方法承载)。

## 框级行交叉判定(已调研两端,2026-06)

> 详见 [survey-diagnosis.md](survey-diagnosis.md) 框级行 + [survey-generation.md](survey-generation.md) 框/layout 行。

- **生成端**(消费侧)**已成熟**:InstanceDiffusion / MIGC++ 吃"逐实例 框/掩码 + 属性",OcclusionFormer 补"遮挡 Z-order",GeoDiffusion 本地可跑。接口正是 grounded 诊断会吐出的语言。
- **诊断端**(产出侧)**词汇有、grounding 偏少**:TIDE/Hoiem 给框级误差词汇(但 dataset 级聚合),GH-ESD 给实例级 grounded 切片(最接近规格),HiBug2 给属性文本切片;FN-Mechanisms/KGFP 更像触发器/验证器。
- **交叉状态 = 可交叉(就是 gap)**:两端语言相同(逐实例 框/掩码/属性/遮挡序),但**没有现成方法把"实测 grounded 检测诊断切片"直接转成逐实例 spec 去驱动 InstanceDiffusion / OcclusionFormer**。现有要么自己造框(DiffusionEngine)、要么用通用/对抗信号(DetDiffusion / AUTHENTICATION)。**这条"诊断切片→逐实例生成 spec"的轻桥,就是框级行的对齐缺口。**

> 待办:其余行(区域 inpaint / 属性文本 / 实例掩码)按同法各补"近期 SOTA + 交叉判定";框级缺口写进 [alignment-gaps.md](alignment-gaps.md)。
