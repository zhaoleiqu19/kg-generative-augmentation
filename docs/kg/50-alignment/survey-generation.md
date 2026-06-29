# 宽调研:生成方向(survey-generation)

> 按控制接口组织生成端方法。**当前已填:框/layout 行**;区域 inpaint / 属性文本 / 实例掩码行待后续。
> - 标注:🌳=已在树 / ✅=本轮新增 / ⚠️=偏离本行。
> - 论文事实在 `../90-papers/` 原子;本文件只组织+定位。
>
> **核心读法(对齐就绪度):** 一个生成方法**能不能直接消费一份 grounded 的逐实例诊断规格**(每实例:框/掩码 + 属性 + 遮挡序),决定它离"对齐"多近——还是只吃整张 layout、或干脆自己造框(盲扩)。

## 范围
可控生成用于检测数据:layout/box 条件、区域 inpaint、实例条件、个性化;遮挡处理、框正确性、in-distribution。检测优先。

## 每篇要打的标签
- **控制接口**:框/layout / 区域inpaint / 属性文本 / 实例掩码(= 它消费什么条件)
- **框正确性**:输入框 ≈ 输出 GT?还是需反检测?
- **遮挡能力**:能否渲染真实遮挡 + 正确深度序
- **画质 / 基座**:SD1.x / SDXL / Flux / 其他(影响真实感天花板)
- **对齐就绪度**:能否直接被逐实例诊断规格驱动、批量按 spec 生成
- **验证度**:代码 / 被引 / 已复现

---

## 框/layout 行(box / layout-conditioned generation)

> 这一行要找:**吃"类别+bbox/layout(乃至逐实例掩码/属性)"控制接口、为检测造数据**的可控生成。按子角色分,对齐就绪度从"整图 layout"到"逐实例 + 遮挡序"递增。

### ① 通用 box/layout→图 基座
- ✅ **InstanceDiffusion**(Wang 2024, CVPR)—— 逐实例控制:每实例 **点/涂鸦/框/掩码 + 自由文本**;COCO 上框/掩码大幅超前 SOTA(~2.0×AP50 / ~1.7×IoU,数字待正文);UniFusion/ScaleU/Multi-instance Sampler。**【对齐就绪度:高】** 接口正是 grounded 逐实例诊断会吐出的语言。原子:[[wang2024-instancediffusion-instance-control]]
- ✅ **MIGC++**(Zhou 2024, TPAMI)—— 多实例:**框&掩码定位 + 文本&图像属性**,divide-and-conquer 治**属性串味**,Consistent-MIG 保一致。**【对齐就绪度:高】** 多相似实例(多电瓶车/人)各保属性时更稳。**开源**(github limuloo/MIGC,权重含 SD1.5/SD2/SDXL)。原子:[[zhou2024-migcpp-multi-instance]]
- ✅ **3DIS / 3DIS-FLUX**(Zhou 2024/2025, ICLR2025 spotlight)—— **深度解耦**多实例:先出场景深度图定位 → ControlNet **免训练**渲染属性,可挂任意基座(SD2/SDXL/**Flux**)。**【对齐就绪度:高;遮挡 native + Flux 画质】** 开源(github limuloo/MIGC 同组)。原子:[[zhou2024-3dis-depth-decoupled-instance]]
- 🌳 **GeoDiffusion**(框→图,**本地在手**,快 4×)—— box-only,无逐实例文本。**【对齐就绪度:中】** 原子:[[chen2023-geodiffusion-geometric-control]]
- 🌳 **ODGEN**(object-wise 文本+视觉,能造多类+遮挡;域内 +25.3 mAP)。**【对齐就绪度:高,但需逐域微调】** 原子:[[zhu2024-odgen-detection-generation]]
- 🌳 **DiffusionEngine**(单阶段产图+框)—— **自己造框**、盲扩规模。**【对齐就绪度:低】** 原子:[[zhang2023-diffusionengine-data-engine]]
- 🌳 **DetDiffusion**(感知信号拌进生成)。**【对齐就绪度:中,信号通用非 grounded】** 原子:[[wang2024-detdiffusion-perception-aware]]

### ② 遮挡 / Z序(直接打锚点:被遮挡的电瓶车)
- ✅ **OcclusionFormer**(Li 2026, ICML)—— 显式建 **Z-order**:实例解耦 + 体渲染合成,SA-Z 数据集 + Queried Alignment Loss;补上多数 box 引擎缺的**遮挡序**。**【对齐就绪度:高(遮挡轴)】** 原子:[[li2026-occlusionformer-zorder]]
- 🌳 ODGEN 通过 object-wise 微调隐式处理遮挡(见上)。

### ③ 领域 / 遥感
- 🌳 **AeroGen**(遥感 layout 生成)。原子:[[tang2024-aerogen-remote-sensing-generation]]

### ⚠️ 偏离本行(据实标注)
- ✅ **GenDet**(Min 2026)—— 名为"画框"实为**检测即生成(图→框)**,是扩散检测器/自动标注,**不是 框→图 数据引擎**,不填本行。原子:[[min2026-gendet-detection-as-generation]]

### 框/layout 行小结
- **逐实例接口已成熟**:InstanceDiffusion / MIGC++ 能吃"每实例框/掩码 + 属性",正是 grounded 诊断规格的语言;**遮挡序**也由 OcclusionFormer 补上;**本地有 GeoDiffusion** 可立即跑(box-only)。
- 缺的不是引擎,而是**没人把"实测的 grounded 检测诊断"接到这些引擎的逐实例接口上**——现有的要么自己造框(DiffusionEngine)、要么用通用/对抗信号(DetDiffusion / AUTHENTICATION),没有"诊断切片→逐实例 spec→InstanceDiffusion/OcclusionFormer"的成品桥。

---

## 其他控制接口行(待后续)
- **区域 inpaint 行**:已有 [[petersen2025-scene-aware-location]] / [[girella2024-diag-indistribution-defect]] / SDXL-Inpaint(本地);待系统补。
- **属性文本行**:[[ruiz2022-dreambooth-subject-driven]] / Flux klein(本地纯 T2I);待补。
- **实例掩码行**:InstanceDiffusion / MIGC++ 已覆盖掩码;待与诊断实例掩码行对账。

---

## 本轮抓取台账(2026-06,框/layout 行)
- **新建 4 篇**:InstanceDiffusion、MIGC++、OcclusionFormer、GenDet(后者标偏离本行)。
- **纠错**:`2402.03040` 非 InstanceDiffusion(实为 InteractiveVideo);正确 id = `2402.03290`,已用。
- **已入库(本次补)**:3DIS / 3DIS-FLUX(`2410.12669` / `2501.05131`)——见上 ① 行。
- **候选留作下批**:GLIGEN(`2301.07093`,开源+已并入 HF diffusers)、BoxDiff(`2307.10816`,免训练)、TerraGen(`2510.21391`)、POCI-Diff(`2601.14056`)。

## 下一步
与 survey-diagnosis 框级行对账 → 回填 representation-map "框/layout" 行的交叉判定(见该文件)。
