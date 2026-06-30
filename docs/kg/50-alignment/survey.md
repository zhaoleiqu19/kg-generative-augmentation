# 宽调研:诊断端 × 生成端(survey)

> 按表示标签组织两端方法,对账后回填 [representation-map.md](representation-map.md) 的交叉判定。**当前已填:框级行**;区域 inpaint / 属性文本 / 实例掩码行待后续批次。
> - 标注:🌳=已在树 / ✅=本轮新增 / ⚠️=抓不到(unverified,未入库)。论文事实在 `../90-papers/` 原子;本文件只组织+定位。
> - **核心读法(对齐就绪度):** 诊断方法的输出**能否直接当生成规格**(grounded 框/区域配置),生成方法**能否直接消费一份 grounded 逐实例诊断规格**——决定它离"对齐"多近。
> - 整环*系统级*近邻(把诊断→生成→过滤→重训转完整的那些)见 [whole-loop-candidates.md](whole-loop-candidates.md);本文件是*方法级*(按表示行)的两端对账。

---

# A. 诊断端(产出侧)

**范围**:检测的失败诊断 / 错误切片发现 / 失败归因 / 漏检机理 / 失败预测。检测优先,分类作旁证。
**每篇打的标签**:表示(框/区域/属性文本/实例掩码)· 任务 · 是否为检测设计 · 对齐就绪度(能否直接当 grounded spec / 需再 grounding / 只是触发或解释)· 验证度。

## 框级行(box-level diagnosis)

> 找:**为检测设计、输出能落到框级/区域级(尺寸/遮挡/定位/类混淆/漏检)的诊断方法**。按角色分三档,对齐就绪度从"词汇表"到"可直接当规格"递增。

### ① 表示来源(框级失败的"词汇表"本身)
- ✅ **TIDE**(Bolya 2020, ECCV)—— 把检测误差切成**六类**(分类/定位/两者/重复/背景/漏检),并**隔离**每类对 mAP 的贡献(tf=0.5/tb=0.1 的精确定义见原子)。**【表示来源】对齐就绪度:中** —— 六类是框级失败词汇,但 **dataset 级聚合**,要当生成规格还需 instance 级 grounding。原子:[[bolya2020-tide-detection-errors]]
- ⚠️ **Hoiem 2012(Diagnosing Error in Object Detectors)** —— 最早的框级误差解剖(4 类假正 + 对尺寸/遮挡/长宽比/部件的敏感度),TIDE 前身。**作者主页 PDF 返回二进制,WebFetch 抓不到 → 未入库、unverified。** 待找可抓取等价源;概念节点暂不引用。

### ② 漏检 / 失败机制(对应 "missed / occlusion" 表示)
- ✅ **FN Mechanisms**(Miller 2022, RA-L)—— 命名导致漏检的**五种内部机制**并量化;机制分布在 benchmark 与机器人部署间**显著不同**。**【机制解释】对齐就绪度:低** —— 机制是检测器内部(anchor/阈值),到"该生成什么图"的桥**间接**。benchmark≠部署 的发现直接关系到部署域(CCTV≠COCO)。原子:[[miller2022-false-negative-mechanisms]]
- ✅ **KGFP**(Zimmermann 2026, CVPR-W)—— 运行时预测检测器何时漏掉安全攸关目标:测**检测器内部特征与视觉基础模型嵌入的角度失配**;person recall **64.3%→84.5% @5%FPR**(COCO),跨 6 个 COCO-O 域稳健。**【触发/验证器】对齐就绪度:低(但适合做闭环触发/过滤)**。原子:[[zimmermann2026-knowledge-guided-failure-prediction]]

### ③ 实例级 grounded 切片发现(= 最接近"框级切片→规格")
- 🌳 **GH-ESD**(Zhang 2026, ECCV)—— generate-and-verify:LLM 先验+视觉证据造**关系型失败假设**→VLM 在**实例级**发现切片→统计检验。**【grounded slice】对齐就绪度:高** —— 失败落在"空间/关系 grounded 的实例切片",最接近能直接当生成规格的形态。*(修订版改名 SliceLens、基准改 FeSD;我们统一沿用 GH-ESD 名。)* 原子:[[zhang2026-gh-esd-instance-slice-discovery]]
- 🌳 **HiBug2**(Chen 2025, ICLR)—— tag-then-slice:生成任务专属视觉属性→高效枚举切片,且能**预测验证集之外的切片**;多任务含检测。**【属性文本 slice】对齐就绪度:中** —— 表示是属性文本(非纯框),显式连"发现→修复"。*(recon:image-level/只标中心物体、依赖 GPT-4o、靠裁剪可对齐框,见原子 Recon findings。)* 原子:[[chen2025-hibug2-error-slice-discovery]]

### 框级行小结(诊断端缝在哪)
- **词汇有了**(TIDE 六类、Hoiem 尺寸/遮挡/长宽比),但都是 **dataset 级聚合**,非逐实例 grounded 规格。
- **漏检机制/失败预测**(FN-Mechanisms、KGFP)说"哪儿/会不会漏",但表示是**检测器内部 / 逐图**,更适合做**闭环触发器/验证器**。
- **最接近"切片→规格"的是 GH-ESD**(实例级 grounded),HiBug2 次之(属性文本、可超出验证集)。

## 其他表示行(待后续)
- **区域 inpaint 行**(哪个区域漏检/易错):待填。
- **属性文本行**:已有 [[eyuboglu2022-domino-slice-discovery]](分类)、HiBug2;待补检测向。
- **实例掩码行**:待填。

---

# B. 生成端(消费侧)

**范围**:可控生成用于检测数据——layout/box 条件、区域 inpaint、实例条件、个性化;遮挡处理、框正确性、in-distribution。检测优先。
**每篇打的标签**:控制接口 · 框正确性(输入框≈输出 GT?)· 遮挡能力(深度序)· 画质/基座 · 对齐就绪度 · 验证度。

## 框/layout 行(box / layout-conditioned generation)

> 找:**吃"类别+bbox/layout(乃至逐实例掩码/属性)"控制接口、为检测造数据**的可控生成。对齐就绪度从"整图 layout"到"逐实例 + 遮挡序"递增。

### ① 通用 box/layout→图 基座
- ✅ **InstanceDiffusion**(Wang 2024, CVPR)—— 逐实例控制:每实例 **点/涂鸦/框/掩码 + 自由文本**;COCO 框/掩码大幅超前 SOTA(~2.0×AP50 / ~1.7×IoU,数字待正文)。**【对齐就绪度:高】** 接口正是 grounded 逐实例诊断会吐出的语言;**本地验证可用**(`instdiff` env)。原子:[[wang2024-instancediffusion-instance-control]]
- ✅ **MIGC++**(Zhou 2024, TPAMI)—— 多实例:**框&掩码 + 文本&图像属性**,divide-and-conquer 治**属性串味**。**【对齐就绪度:高】** 多相似实例各保属性更稳。**开源**(limuloo/MIGC,权重含 SD1.5/SD2/SDXL),本地可用。原子:[[zhou2024-migcpp-multi-instance]]
- ✅ **3DIS / 3DIS-FLUX**(Zhou 2024/2025, ICLR spotlight)—— **深度解耦**多实例:先出场景深度图定位 → ControlNet **免训练**渲染,可挂任意基座(SD2/SDXL/**Flux**)。**【对齐就绪度:高;遮挡 native + Flux 画质】** 本地仅 layout→depth 段可跑(FLUX 渲染段缺 gated 权重)。原子:[[zhou2024-3dis-depth-decoupled-instance]]
- 🌳 **GeoDiffusion**(框→图,**本地在手**,快 4×)—— box-only,无逐实例文本。**【对齐就绪度:中】** 原子:[[chen2023-geodiffusion-geometric-control]]
- 🌳 **ODGEN**(object-wise 文本+视觉,能造多类+遮挡;域内 +25.3 mAP)。**【对齐就绪度:高,但需逐域微调】** 原子:[[zhu2024-odgen-detection-generation]]
- 🌳 **DiffusionEngine**(单阶段产图+框)—— **自己造框**、盲扩规模。**【对齐就绪度:低】** 原子:[[zhang2023-diffusionengine-data-engine]]
- 🌳 **DetDiffusion**(感知信号拌进生成)。**【对齐就绪度:中,信号通用非 grounded】** 原子:[[wang2024-detdiffusion-perception-aware]]

### ② 遮挡 / Z序
- ✅ **OcclusionFormer**(Li 2026, ICML)—— 显式建 **Z-order**:实例解耦 + 体渲染合成;补上多数 box 引擎缺的**遮挡序**。**【对齐就绪度:高(遮挡轴)】** 原子:[[li2026-occlusionformer-zorder]]
- 🌳 ODGEN 通过 object-wise 微调隐式处理遮挡(见上)。

### ③ 领域 / 遥感
- 🌳 **AeroGen**(遥感 layout 生成)。原子:[[tang2024-aerogen-remote-sensing-generation]]

### ⚠️ 偏离本行
- ✅ **GenDet**(Min 2026)—— 名为"画框"实为**检测即生成(图→框)**,是扩散检测器/自动标注,不是 框→图 数据引擎,不填本行。原子:[[min2026-gendet-detection-as-generation]]

### 框/layout 行小结(生成端缝在哪)
- **逐实例接口已成熟**:InstanceDiffusion / MIGC++ 能吃"每实例框/掩码 + 属性";**遮挡序**由 OcclusionFormer 补上;**本地有 GeoDiffusion** 可立即跑(box-only)。
- 缺的不是引擎,而是**没人把"实测 grounded 检测诊断"接到这些引擎的逐实例接口上**——现有的要么自己造框(DiffusionEngine)、要么用通用/对抗信号(DetDiffusion)。

## 其他控制接口行(待后续)
- **区域 inpaint 行**:已有 [[petersen2025-scene-aware-location]] / [[girella2024-diag-indistribution-defect]] / SDXL-Inpaint(本地);待系统补。
- **属性文本行**:[[ruiz2022-dreambooth-subject-driven]] / Flux klein(本地纯 T2I);待补。
- **实例掩码行**:InstanceDiffusion / MIGC++ 已覆盖掩码;待与诊断实例掩码行对账。

---

# 对账小结(两端 → 缺口)

两端的表示语言相同(逐实例 框/掩码/属性/遮挡序),且各自都已成熟、本地有可跑基座——但**没人把"实测 grounded 诊断切片"直接接到生成器的逐实例接口上**。把 TIDE 式**框级失败词汇** + GH-ESD 式**实例级 grounding** 合成"尺寸·遮挡·定位配置"规格、直接喂 InstanceDiffusion/OcclusionFormer —— 这一步**还没有现成方法**。完整论证见 [alignment-gaps.md](alignment-gaps.md);交叉判定回填见 [representation-map.md](representation-map.md)。

---

# 本轮抓取台账(2026-06,框级行)

- **诊断端**:新建 3 篇(TIDE、FN-Mechanisms、KGFP);纳入已有 2 篇(GH-ESD、HiBug2);⚠️ unverified 1 篇(Hoiem 2012,PDF 抓不到);候选留下批(CB-SLICE `2605.29836`、Manifold-Compactness `2501.19032`、Introspective FN、Black-box 误差诊断综述 `2201.06444`)。
- **生成端**:新建 4 篇(InstanceDiffusion、MIGC++、OcclusionFormer、GenDet〔标偏离〕);纠错(`2402.03040` 实为 InteractiveVideo,正确 id `2402.03290`);补入库 3DIS/3DIS-FLUX(`2410.12669`/`2501.05131`);候选留下批(GLIGEN `2301.07093`、BoxDiff `2307.10816`、TerraGen `2510.21391`、POCI-Diff `2601.14056`)。

# 下一步
- 给 Hoiem 找可抓取等价源补 unverified 缺口(可选)。
- 下沉其余表示行(区域 inpaint / 属性文本 / 实例掩码)两端对账 → 回填 representation-map 对应行。
