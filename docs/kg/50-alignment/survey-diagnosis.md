# 宽调研:诊断方向(survey-diagnosis)

> 按表示标签组织诊断端方法。**当前已填:框级行**;区域 / 属性文本 / 实例掩码行待后续批次。
> - 标注:🌳=已在树 / ✅=本轮新增 / ⚠️=抓不到(unverified,未入库)。
> - 论文事实在 `../90-papers/` 原子;本文件只组织+定位。
>
> **核心读法(对齐就绪度):** 一个诊断方法的输出**能否直接当生成规格**(grounded 的框/区域配置),决定它离"对齐"多近——还是只是 dataset 级聚合 / 检测器内部机制 / 逐图判定。下面每篇打这个标。

## 范围
检测的失败诊断 / 错误切片发现 / 失败归因 / 漏检机理 / 失败预测。检测优先,分类作旁证。

## 每篇要打的标签
- **表示标签**:框 / 区域 / 属性文本 / 实例掩码(= 它输出什么形式的失败描述)
- **任务**:检测 / 分类 / 分割
- **是否为检测设计**:purpose-built / 多任务含检测 / 仅分类可迁移
- **对齐就绪度**:输出能否直接当生成规格(grounded spec)/ 需再 grounding / 只是触发或解释
- **验证度**:有代码 / 被引 / 已复现(新 ≠ 已验证)

---

## 框级行(box-level diagnosis)

> 这一行要找:**为检测设计、输出能落到框级/区域级(尺寸/遮挡/定位/类混淆/漏检)的诊断方法**。按"在框级里扮演什么角色"分三档,对齐就绪度从"词汇表"到"可直接当规格"递增。

### ① 表示来源(框级失败的"词汇表"本身)
- ✅ **TIDE**(Bolya 2020, ECCV)—— 把检测误差切成**六类**:分类 / 定位 / 两者 / 重复 / 背景 / 漏检,并**隔离**每类对 mAP 的贡献。**【表示来源】对齐就绪度:中** —— 六类正是框级失败词汇,但是 **dataset 级聚合**,要当生成规格还需 instance 级 grounding。原子:[[bolya2020-tide-detection-errors]]
- ⚠️ **Hoiem 2012(Diagnosing Error in Object Detectors)** —— 最早的框级误差解剖(4 类假正 + 对尺寸/遮挡/长宽比/部件的敏感度),TIDE 的前身。**作者主页 PDF 返回二进制,WebFetch 抓不到 → 未入库、unverified。** 待找可抓取等价源(HTML/会议库)再补;在概念节点中暂不引用。

### ② 漏检 / 失败机制(对应 "missed / occlusion" 表示)
- ✅ **FN Mechanisms**(Miller 2022, RA-L)—— 打开检测器黑盒,命名导致漏检的**五种内部机制**,并量化;发现机制分布在 benchmark 与机器人部署间**显著不同**。**【机制解释】对齐就绪度:低** —— 机制是检测器内部(anchor/阈值),非场景级描述,到"该生成什么图"的桥**间接**。benchmark≠部署 的发现直接关系到锚点(电梯 CCTV≠COCO)。原子:[[miller2022-false-negative-mechanisms]]
- ✅ **KGFP / Knowledge-Guided Failure Prediction**(Zimmermann 2026, CVPR-W)—— 运行时预测检测器何时漏掉安全攸关目标:测**检测器内部特征与视觉基础模型嵌入的角度失配**;person recall **64.3%→84.5% @5%FPR**(COCO),跨 6 个 COCO-O 域稳健。**【触发/验证器】对齐就绪度:低(但适合做闭环触发/过滤)** —— 它说"这帧会不会漏",不说"生成什么配置"。原子:[[zimmermann2026-knowledge-guided-failure-prediction]]

### ③ 实例级 grounded 切片发现(= 最接近"框级切片→规格")
- 🌳 **GH-ESD**(Zhang 2026, ECCV)—— generate-and-verify:LLM 先验+视觉证据造**关系型失败假设**→VLM 在**实例级**发现切片→统计检验。**【grounded slice】对齐就绪度:高** —— 失败落在"空间/关系 grounded 的实例切片"(如"被门遮挡的电瓶车、暗光"),最接近能直接当生成规格的形态。*(注:此篇修订版改名 SliceLens、基准改 FeSD;我们统一沿用 **GH-ESD** 名。)* 原子:[[zhang2026-gh-esd-instance-slice-discovery]]
- 🌳 **HiBug2**(Chen 2025)—— tag-then-slice:生成任务专属视觉属性→高效枚举切片,且能**预测验证集之外的切片**;多任务含检测。**【属性文本 slice】对齐就绪度:中** —— 表示是**属性文本**(非纯框),但显式连"发现→修复",且"超出验证集"对锚点(电梯未见失败模式)有用。原子:[[chen2025-hibug2-error-slice-discovery]]

### 框级行小结(缝在哪)
- **词汇有了**(TIDE 的六类、Hoiem 的尺寸/遮挡/长宽比),但都是 **dataset 级聚合**,不是逐实例 grounded 的规格。
- **漏检机制/失败预测**(FN-Mechanisms、KGFP)告诉你"哪儿/会不会漏",但表示是**检测器内部 / 逐图**,到生成规格的桥间接——更适合做**闭环的触发器/验证器**。
- **最接近"切片→规格"的是 GH-ESD**(实例级 grounded),HiBug2 次之(属性文本、可超出验证集)。
- **对齐缺口**:把 TIDE 式的**框级失败词汇**与 GH-ESD 式的**实例级 grounding** 合起来、直接吐出"尺寸·遮挡·定位配置"的生成规格——这一步**还没有现成方法**,正对生成端的"框/layout"行。

---

## 其他表示行(待后续批次)
- **区域 inpaint 行**(哪个区域漏检/易错):待填。
- **属性文本行**(自然语言属性切片):已有 [[eyuboglu2022-domino-slice-discovery]](分类)、HiBug2;待补检测向。
- **实例掩码行**(像素/实例级):待填。

---

## 本轮抓取台账(2026-06,框级行)
- **新建 3 篇**:TIDE、FN-Mechanisms、KGFP(已立原子)。
- **纳入已有 2 篇**:GH-ESD、HiBug2(沿用原名,未改动原子)。
- ⚠️ **unverified 1 篇**:Hoiem 2012(PDF 抓不到)——未入库,待等价源。
- **候选留作下批**:CB-SLICE(`2605.29836`)、Manifold-Compactness(`2501.19032`)、Introspective FN(PMC)、Black-box 误差诊断工具综述(`2201.06444`)。

## 下一步
1. (可选)给 Hoiem 找可抓取等价源补 unverified 缺口。
2. 下沉生成端"框/layout"行宽调研(survey-generation),与本行对账 → 回填 representation-map 的"框级"行交叉判定。
