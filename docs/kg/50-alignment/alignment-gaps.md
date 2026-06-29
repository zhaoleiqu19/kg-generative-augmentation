# 对齐缺口(alignment-gaps)

> 状态:**已写(2026-06-29,框级行宽调研后)**。本文件 refine 旧 `GAPS.md` 的 G1–G4,**不覆盖**旧文件(旧文件留作 Phase 0–4 记录)。证据来自 [survey-diagnosis.md](survey-diagnosis.md) / [survey-generation.md](survey-generation.md) / [representation-map.md](representation-map.md) 的框级行交叉判定。纳入与加权口径见 [alignment-thesis.md](alignment-thesis.md) 的"纳入标准"。

## 1. 一句话缺口

> **两端都已成熟,且共享同一套"逐实例 框/掩码/遮挡/属性"语言;但没有一篇已发表方法,把一份*实测的、grounded 的检测诊断切片*(诊断输出)直接转成一份*逐实例生成规格*(生成器输入)。缺的是这座桥,不是两端。**

也就是说:生成端"框/layout"接口能吃的语言,正是 grounded 检测诊断会吐出的语言——但现有工作要么**自己造框**盲扩,要么**用通用/对抗信号**驱动,没有"实测切片 → 逐实例 spec"的成品接法。

## 2. 证据 —— 诊断端(产出侧)

检测粒度的切片发现今天能产出什么、输出什么表示:

- **实例级 grounded 切片(最接近"可直接当规格")**:[[zhang2026-gh-esd-instance-slice-discovery]](GH-ESD)用 generate-and-verify 在**实例级**发现"空间/关系 grounded"的失败切片(如"被门遮挡 + 暗光的目标"),并做统计检验。对齐就绪度:**高**——输出形态最接近生成规格。
- **属性文本切片**:[[chen2025-hibug2-error-slice-discovery]](HiBug2)tag-then-slice,输出**属性文本**切片,且能**预测验证集之外**的切片(对锚点的未见失败模式有用)。对齐就绪度:**中**(表示是文本,非纯框)。
- **框级失败"词汇表"(但 dataset 级聚合)**:[[bolya2020-tide-detection-errors]](TIDE)把检测误差切成六类(分类/定位/两者/重复/背景/漏检)并隔离各类对 mAP 的贡献。对齐就绪度:**中**——是框级失败的词汇来源,但**聚合在 dataset 级**,要当生成规格还差一层 instance 级 grounding。
- **检测器内部机制 / 运行时触发(到"生成什么"的桥间接)**:[[miller2022-false-negative-mechanisms]] 命名五种导致漏检的内部机制,并指出 benchmark 与部署间机制分布**显著不同**;[[zimmermann2026-knowledge-guided-failure-prediction]](KGFP)运行时预测漏检(person recall 64.3%→84.5% @5%FPR,COCO;数字见该原子)。两者表示是**检测器内部 / 逐图**,更适合做闭环的**触发器/验证器**,而非直接的生成规格。

**诊断端小结**:框级失败的*词汇*齐了,实例级 grounding 也有(GH-ESD),但"把词汇 + grounding 合成一份'尺寸·遮挡·定位配置'规格"这一步,没有现成方法承担。

## 3. 证据 —— 生成端(消费侧)

可控的逐实例生成今天能消费什么接口:

- **逐实例接口已成熟**:[[wang2024-instancediffusion-instance-control]](InstanceDiffusion)吃每实例**点/涂鸦/框/掩码 + 自由文本**;[[zhou2024-migcpp-multi-instance]](MIGC++)吃**框&掩码 + 文本&图像属性**并治多实例属性串味。两者接口**正是** grounded 逐实例诊断会吐出的语言。对齐就绪度:**高**。
- **遮挡序**:[[li2026-occlusionformer-zorder]](OcclusionFormer)显式建 Z-order,补上多数 box 引擎缺的遮挡深度序——直接对应锚点"被遮挡的电瓶车"。
- **本地可立即跑的 box 基座**:[[chen2023-geodiffusion-geometric-control]](GeoDiffusion,box-only,本地在手);[[zhu2024-odgen-detection-generation]](ODGEN,object-wise 文本+视觉,能造多类+遮挡,域内 +25.3 mAP,见该原子)对齐就绪度高**但需逐域微调**。

**生成端小结**:缺的不是引擎。逐实例接口 + 遮挡序都到位,且本地有可跑基座——它们都在"等"一份 grounded 的逐实例 spec 来喂。

## 4. 这条缝(为什么两端语言相同却接不上)

两端的表示语言相同(逐实例 框/掩码/属性/遮挡序),但**没人把"实测 grounded 诊断切片"直接接到生成器的逐实例接口上**。最近邻各差一条轴:

- **自己造框、盲扩规模**:[[zhang2023-diffusionengine-data-engine]](DiffusionEngine)单阶段产图+框,但框是**自己生成**的,不由实测失败牵引——缺"诊断驱动"轴。
- **用通用感知信号、非 grounded 切片**:[[wang2024-detdiffusion-perception-aware]](DetDiffusion)是已发表里最干净的"对齐"实例——感知模型信号*就是*生成控制接口(P.A. loss / P.A. Attr),桥是内生的;但信号是**通用感知损失**,不是 grounded 的逐切片失败(无尺寸/遮挡/类混淆切片),且**一次性**(无重新诊断)。
- **用对抗信号induce失败、非实测切片**:[[zarei2025-authentication-rare-failure-modes]](AUTHENTICATION)用对抗引导 inpainting 造"逃避检测器"的场景,是 diagnosis→generation 的精神近邻;但"诊断"是**对抗失败诱导**,不是从真实运营数据测出的逐实例切片——缺"实测对齐"轴。

> 即:DiffusionEngine 缺诊断驱动;DetDiffusion 信号通用且一次性;AUTHENTICATION 靠对抗而非实测。**三者都不提供"实测 grounded 诊断切片 → 逐实例 spec"这条轻桥**——这正是框级行的对齐缺口。

## 5. 与旧 G1–G4 的关系(refine,不覆盖)

旧 `GAPS.md` 仍是 Phase 0–4 的历史记录;本主张把贡献面收敛、锐化:

- 旧 **G1**(检测端到端闭环)+ **G2**(检测粒度诊断)+ **G4**(切片→spec 桥)→ 收敛为本文件的**一条"对齐接口"缺口**(§1):让诊断输出的失败表示直接成为生成控制条件,从而轻量地闭合 诊断→生成→重训→**重新诊断** 的检测闭环。闭环靠"重新诊断"闭合,所以诊断输出还须是**可重复测量**的。
- 旧 **G3**(小/遮挡/域差的安全比例 / 过滤)→ **保留为度量侧子问题**:KGFP 式触发器/验证器([[zimmermann2026-knowledge-guided-failure-prediction]])适合做这一侧的过滤闸。

> 候选缺口可演示性:框级"诊断切片→逐实例 spec"桥可在 COCO 小目标切片上演示(最低生成风险),再迁移到锚点(电梯 CCTV 电瓶车)。详见后续 [generality-map.md](generality-map.md) 与 [decisions/demo-task-selection.md](decisions/demo-task-selection.md)。
