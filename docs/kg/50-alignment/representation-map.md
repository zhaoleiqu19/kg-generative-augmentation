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

## 失败类型 × 生成复杂度(框级行细化,2026-06-30)

> 把上表第 1 行("框/layout")按**具体失败类型**展开。诊断词汇已核实:[[bolya2020-tide-detection-errors]] 6 类(tf=0.5/tb=0.1)+ pycocotools 尺寸/逐类切片 + [[chen2025-hibug2-error-slice-discovery]] 属性切片(主体/背景/全局)。**复杂度不是一维**,拆成三轴:**可表达性**(接口能否描述)×**保真度**(生成器能否画出)×**可验证性**(是否需多采样+过滤)。

| 失败类型(诊断) | 生成任务 | 可表达性 | 保真度 | 可验证性 | 桥重量 |
|---|---|---|---|---|---|
| **Miss / 尺寸 / 逐类**(漏检) | 同类同尺寸多放实例 | 高(框原生) | 中(小框有天花板) | 低 | **轻** |
| **Loc**(定位松) | 造不同尺度/位置/截断/拥挤的框 | 高(框原生) | 中 | 低 | **轻—中** |
| **Cls**(类混淆) | 易混类共场景对照 | 中 | **低**(细粒度类身份难) | 高(要 CLIP/LLM 过滤) | **重** |
| **遮挡 / 姿态 / 暗色**(属性) | 造被遮挡/特殊姿态/低对比实例 | 中(属性入实例 caption) | **低** | 高 | **重** |
| **背景 / 光照 / 视角**(属性) | 暗光/杂乱/CCTV 视角场景 | 高(全局 caption) | 中(SD1.5 暗光弱) | 中 | **中** |
| **Bkg**(背景误检) | 造"难负样本"(无目标却易误检) | 中(目标反转) | 中 | 中 | **中** |
| **Dupe**(重复) | —(NMS/检测头问题) | — | — | — | **数据增强不可修** |

**两条贯穿结论:**
1. **接口落差**:[[chen2025-hibug2-error-slice-discovery]] 的属性切片是**图像级/只标中心物体**,要变"框可控生成"必须再用 pycocotools **重新 grounding 到框**——任何"属性驱动生成"都比"框驱动生成"多一步 join。
2. **对主张的诚实修正**:alignment 主张"对齐则桥轻"**只在"框可表达"的失败上成立**(Miss/Loc/尺寸);身份/属性类失败(Cls/遮挡)即使表示对齐,桥仍重(软文本控制 + 过滤)。这本身是一条 [alignment-gaps.md](alignment-gaps.md) 值得记的细化。

### 实验前先排除(a-priori 三重过滤,缩小实验范围)

不必每类都做实验——三条先验过滤能砍掉一部分:

1. **过滤A|根因必须是"训练分布"**:根因在推理/后处理或架构的,加数据治不了 → **Dupe 直接排除**(NMS/分数标定问题,且 dAP 仅 0.25)。
2. **过滤B|layout→image 只产正样本**:修误检(假阳)要"负样本生成",是另一条管线 → **Bkg 移出核心闭环**,单列负样本生成轨。
3. **过滤C|部分可修要标注非数据成分**:**Loc** 一部分是回归头/特征分辨率(非数据),预期有天花板 → 保留但别期望全治。

**过滤后的实验范围**:核心闭环 = **Miss(+Loc 作为框原生的低成本搭车项)**;**Cls / 属性切片**= 更重的第二阶段(且属性切片**门控于 HiBug2 可用性**,见下)。

### HiBug2 对"框为单位"的可用程度(2026-06-30 实测 recon)

- **能对齐,但要我们自己裁剪**:HiBug2 原生单位 = `{类: [图]}` + 逐图 correctness,检测任务下**每张"图"= 一个实例裁剪**(KITTI Car/Pedestrian 即此)。我们已有框(pycocotools grounding)+ 漏检/命中标签 → 喂逐实例裁剪即可;HiBug2 只补"为什么难"的属性,**框 grounding 由我们提供**。"主体 vs 框"的错位**靠裁剪可解**。
- **硬限制(它做不到的程度)**:① 依赖 **GPT-4o**(`VLMAgent(api_key, base_url)`,支持自定义 base_url=可走镜像;但环境内**当前无 key**=阻断);② `utils.readImg` **只缩不放**,**极小目标裁剪发给 GPT-4o ≈ 不可读** → 对 <32px(我们 542/698 的目标档)属性标注不可靠,**恰好在我们最在意的那档最弱**;③ 背景/全局属性需带 margin 裁剪或整图,密集场景下"指哪个物体"会含糊;④ 它**不自带像素/框 grounding**。

> 注:本表的复杂度判断尚是设计推断,需被 [decisions/loop-mvp-pilot.md](decisions/loop-mvp-pilot.md) 的消融实测验证;该文件同时记录了试点执行中的红队漏洞(val 泄漏 / cascade 关闭 / A/B 混淆等)。HiBug2 详细 recon 见 [[chen2025-hibug2-error-slice-discovery]]。

## 框级行交叉判定(已调研两端,2026-06)

> 详见 [survey.md](survey.md) 的诊断端框级行 + 生成端框/layout 行。

- **生成端**(消费侧)**已成熟**:InstanceDiffusion / MIGC++ 吃"逐实例 框/掩码 + 属性",OcclusionFormer 补"遮挡 Z-order",GeoDiffusion 本地可跑。接口正是 grounded 诊断会吐出的语言。
- **诊断端**(产出侧)**词汇有、grounding 偏少**:TIDE/Hoiem 给框级误差词汇(但 dataset 级聚合),GH-ESD 给实例级 grounded 切片(最接近规格),HiBug2 给属性文本切片;FN-Mechanisms/KGFP 更像触发器/验证器。
- **交叉状态 = 可交叉(就是 gap)**:两端语言相同(逐实例 框/掩码/属性/遮挡序),但**没有现成方法把"实测 grounded 检测诊断切片"直接转成逐实例 spec 去驱动 InstanceDiffusion / OcclusionFormer**。现有要么自己造框(DiffusionEngine)、要么用通用/对抗信号(DetDiffusion / AUTHENTICATION)。**这条"诊断切片→逐实例生成 spec"的轻桥,就是框级行的对齐缺口。**

> 待办:其余行(区域 inpaint / 属性文本 / 实例掩码)按同法各补"近期 SOTA + 交叉判定";框级缺口写进 [alignment-gaps.md](alignment-gaps.md)。
