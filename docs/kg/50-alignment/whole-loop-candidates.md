# 整体层全貌(诊断↔生成对齐:whole-loop 近邻)

> **这是新方向"整体层"的完整视图**:回答"有没有人做过/做过相似的整条流程(诊断→生成→过滤→重训→再诊断)"。
> - 内容 = **上一批的闭环骨架** ＋ **本轮(2026-06)新增**,统一标注(🌳=已在树 / ✅=本轮新增 / ♻️=去重 / ⚠️=抓不到)。
> - 论文事实都在 `../90-papers/` 原子里;本文件只组织+定位,不复制原子。
> - 原 landscape 节点 `../10-landscape/related-systems-whole-loop.md` 作为 Phase 0–4 历史保留不动;本文件是新方向下的完整对账版。
>
> **结论先行**:环的每一段都有人做过,但**没有任何一篇把"实测的、落到框级/区域级的 grounded 检测诊断"接到"可控、能处理遮挡、真实图"的生成器 + 明确验证器闭环**。最近的两篇分别只占住一条轴(见下)。这道缝=我们的位置。

---

## 怎么读这一层

**环(四步):**
```
① 诊断 —— 模型在哪类样本上栽了?(找弱点)
② 生成 —— 照弱点造对应新图(+正确的框)
③ 过滤 —— 留好的、扔坏的
④ 重训 —— 训回去 →(回①)再诊断,确认补上
```
关键不在某步炫技,而在 **①的输出能不能直接当②的输入**(=对齐主张)。

**两种"最接近"要分开看**(同一篇很难两条都占):
- **闭环完整度**最高 = 真把环转完整(有过滤+重训)的那几个 → A 类前排的骨架。
- **对齐度**最高 = 把①②焊在一起(诊断输出=生成接口)的 → DetDiffusion。

---

## A 类:整环近邻(诊断/反馈信号 → 生成)
> 按"用什么信号牵引生成"从糙到贴。

- 🌳 **LTDA-Drive**(Yurt 2025)—— generate→insert→**LLM 过滤**,用于长尾 3D 检测;KITTI 稀有类 **+34.75%**。**检测**。**【闭环完整度高】** 缺:由**盲长尾**牵引,非实测逐切片诊断。 `90-papers/yurt2025-ltda-drive-longtail.md`
- 🌳 **GALOT**(Hong 2024)—— 明确 **AL 准则 → 生成**闭环;**【闭环完整度高】** 但**分类**、纯合成、文本伪标签、**无框**。 `90-papers/hong2024-galot-generative-active-learning.md`
- 🌳 **SafeFix**(Ouyang 2025)—— 诊断→针对性生成→**VLM 过滤**→重训;已发表的**闭环模板**,**【闭环完整度高】** 但以**分类**为中心。 `90-papers/ouyang2025-safefix-model-repair.md`
- 🌳 **Chegini**(2023)—— 诊断→扩散生成,困难子群 **~21%**;**分类**。 `90-papers/chegini2023-clip-diffusion-failure-mitigation.md`
- ✅ **DetDiffusion**(Wang 2024, CVPR)—— 感知模型信号(**P.A. loss + 属性**)焊进扩散训练,生成天然偏检测器所需;COCO layout 生成 **SOTA**(具体 mAP 待正文)。**检测**。**【对齐度最高】** 但信号**通用**非 grounded、且**一次性**(不回头重新诊断)。 `90-papers/wang2024-detdiffusion-perception-aware.md`
- ✅ **AUTHENTICATION**(Zarei 2025)—— 抠目标掩码→**反转成环境掩码**+prompt→SD-inpaint,用**对抗噪声**生成"骗过检测器"的场景,并产自然语言描述。**检测/AV**。诊断=**对抗造假**,非实测真实切片。 `90-papers/zarei2025-authentication-rare-failure-modes.md`
- ✅ **Improving-OD-XAI**(Mital 2024)—— XAI 显著图→**人手改 3D mesh**→重渲染;XAI 引导再 **+1.5 到 mAP50=96.1%**。**检测**,但**渲染图 + 人在环**,非自动桥。 `90-papers/mital2024-xai-modify-synthetic-data.md`

## B 类:位置近邻(只解决②里的"往哪儿放")
- 🌳 **Scene-Aware**(Petersen 2025)—— 学概率位置模型 + inpainting,**+1.4 mAP**(比随机放好 **2.8×**);位置来自**场景先验**,非诊断。 `90-papers/petersen2025-scene-aware-location.md`
- 🌳 **DIAG**(Girella 2024)—— **人手框区域**,免训练在分布内造缺陷,**+18~28 AP**;= 切片→规格标记的**人工版**。 `90-papers/girella2024-diag-indistribution-defect.md`

→ 对应 representation-map 的"区域 inpaint"行,但触发靠先验/人手,不是诊断。

## C 类:纯生成引擎(只管②造得好,不碰①)
- 🌳 **ODGEN**(Zhu 2024)—— object-wise 条件,能造**多类+遮挡**;域内 **+25.3 mAP@.50:.95**,COCO 比前法 **+5.6**。 `90-papers/zhu2024-odgen-detection-generation.md`
- 🌳 **GeoDiffusion**(框→图,本地在手)· **ReCon**(区域矫正)· **AeroGen**(遥感)· **X-Paste**(copy-paste)。 见各自原子。
- ✅ **DiffusionEngine**(Zhang 2023)—— 单阶段产"**图+框**",Detection-Adapter 把扩散的语义/位置知识对齐到检测信号;**+3.1 COCO / +7.6 VOC / +11.5 Clipart**。属引擎、**非诊断驱动**(盲扩规模)。 `90-papers/zhang2023-diffusionengine-data-engine.md`

→ 给定 layout/框就能造检测数据,是我们生成端**现成的手**。

## 校准预期(泼冷水)
- 🌳 **Big-Data-Myth**(Voetman 2023)—— 简单任务上纯合成接近真实(**AP 差 0.09~0.12**);合成更多是"替代",简单场景不一定是"放大器",别高估。 `90-papers/voetman2023-big-data-myth-detection.md`

## 定位用综述(打边界,非整环系统)
- ✅ **UniDiffDA**(Li 2026)—— 把 DiffDA 全流程拆成**微调/生成/利用**三件并公平基准;**仅分类**,不覆盖检测的框级接口。 `90-papers/li2026-unidiffda-systematic-analysis.md`
- 🌳 **Alimisis Review**(2024)—— 扩散数据增强的方法/模型/指标/方向综述。 `90-papers/alimisis2024-diffusion-augmentation-review.md`

---

## 整体层结论(缝在哪)
- **闭环完整度**最高的(LTDA / GALOT / SafeFix)信号糙、且多为**分类**,不碰框。
- **对齐度**最高的(DetDiffusion)是**检测**、把①②焊一起,但用**通用感知信号**代替"具体哪类切片在栽",且**一次性**。
- 其余要么是**对抗/人工/渲染图**(AUTHENTICATION / Mital),要么是**先验/人手放置**(Scene-Aware / DIAG),要么是**盲扩引擎**(ODGEN / DiffusionEngine…)。

**没有一篇同时占满"闭环完整 + 对齐 + 检测 + 真实图 + 可控遮挡 + 明确验证器"。** 这正是下沉局部时要重点查的:**诊断端能否产出框级/区域级、且能直接当生成规格的表示。**

---

## 本轮抓取台账(2026-06)
- **新建 5 篇**(已立原子、已并入上表):DetDiffusion、AUTHENTICATION、Improving-OD-XAI、DiffusionEngine、UniDiffDA。
- **去重 2 篇**:`2512.24592` 抓回来是 **GH-ESD**(树里已有 `zhang2026-gh-esd-instance-slice-discovery`,搜索把 "SliceLens" 错配到此 url;真 SliceLens 暂无可核实 url);`2407.04103` = **Alimisis**(树里已有)。均不重复建。
- ⚠️ **unverified 1 篇**:Neurosymbolic Slice Discovery(sagepub,HTTP 403 抓不到)——按反幻觉规则不写、不进概念节点;要纳入需找可抓取的等价来源。

## 下一步(下沉局部,走 RUNBOOK)
按表示标签做诊断端 / 生成端两条宽调研 → 回填 `representation-map` 各行的"已交叉 / 可交叉 / 无交叉但值得读"。建议起点:**诊断端"框级"那行**(最薄、价值最高;候选 TIDE / Hoiem / FN-mechanisms / CB-SLICE / 真 SliceLens)。
