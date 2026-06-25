# 对齐表:诊断输出 × 生成输入(representation-map)

> 核心轴 = **共享表示**。左=生成器的控制接口,中=与之对齐的诊断输出,右=桥要做的事 + 已有原子(wikilink 引用 `../90-papers/`)。宽调研每收一篇,就往对应行补。

## 表

| 生成控制接口 | 对齐的诊断输出 | 桥的工作量 | 已有原子(引用) |
|---|---|---|---|
| **框 / layout**(类别+bbox) | 框级 / 尺寸带 / 遮挡 / 定位误差 / 类混淆 | **极轻**:按失败的尺寸·遮挡配置发框 | 生成:[[chen2023-geodiffusion-geometric-control]] [[zhu2024-odgen-detection-generation]] [[zhu2025-recon-region-controllable]] [[tang2024-aerogen-remote-sensing-generation]] · 诊断:[[zhang2026-gh-esd-instance-slice-discovery]] |
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

> 待办:宽调研后,每行补"近期 SOTA + 表示标签",并标出哪几对**已交叉 / 可交叉 / 无交叉但值得读**。
