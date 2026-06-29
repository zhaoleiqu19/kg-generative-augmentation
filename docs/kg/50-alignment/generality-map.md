# 适用性地图(generality-map):这套方法在哪些检测子场景成立

> 状态:**已写(2026-06-29)**。目的:框出"诊断驱动生成式增强"在不同检测子场景里的适用性与证据强度,从而说明 **为什么 MVP 选 COCO 小目标切片** 作演示是最低风险的代表行。
> 读法:列"增强增益"区分两类——**通用/盲增强已有增益**(很多)vs **诊断驱动(实测切片牵引)增益**(几乎没有,正是 [alignment-gaps.md](alignment-gaps.md) 的缝)。证据只引 `../90-papers/` 已有原子;数字均标来源。

## 适用性表

| 检测子场景 | 主要失败模式 | 增强增益(✓通用增强已报 / ✗诊断驱动尚无)+ 原子 | 哪个生成器覆盖 | 证据强度 |
|---|---|---|---|---|
| **通用 COCO 式** | 类混淆 / 定位 / 重复 / 背景误报(TIDE 六类) | ✓ layout 控制生成提升下游检测:[[wang2024-detdiffusion-perception-aware]](称 COCO layout-guided 生成 SOTA,mAP 待正文)、[[wang2024-instancediffusion-instance-control]](逐实例控制,~2.0×AP50 待正文);✗ 无"按实测切片"驱动 | GeoDiffusion / DetDiffusion / InstanceDiffusion / MIGC++ | **强**(多方法、有代码) |
| **小目标** | 低分辨率 / 背景干扰 / 类不均衡;用 size-specific AP 量 | ✓ 综述确认挑战与评测口径:[[nikouei2025-small-object-detection-survey]](挑战="低分辨率、遮挡、背景干扰、类不均衡",size-specific AP 为评测镜);copy-paste 路线 [[zhao2023-xpaste-copy-paste]](LVIS +2.6 box AP 总体);✗ 无诊断驱动的小目标切片→生成 | GeoDiffusion(本地)/ ODGEN / X-Paste 式合成 | **中-强**(综述+通用增强;诊断驱动空缺) |
| **遮挡 / 拥挤** | 漏检、深度序错、属性串味 | ✓ 生成端能渲染遮挡:[[li2026-occlusionformer-zorder]](显式 Z-order)、[[zhu2024-odgen-detection-generation]](object-wise 含遮挡,域内 +25.3 mAP)、[[zhou2024-migcpp-multi-instance]](多实例治属性串味);✗ 无"实测遮挡切片→spec" | OcclusionFormer / ODGEN / MIGC++ | **中-强**(生成侧成熟;诊断接入空缺) |
| **长尾 / 稀有类** | 尾类样本稀缺 | ✓ 造尾类有增益:[[yurt2025-ltda-drive-longtail]](KITTI 尾类 3D +34.75% vs 对照,绝对值待正文)、[[zhao2023-xpaste-copy-paste]](LVIS 稀有类 +6.8 box / +6.5 mask AP)、[[zarei2025-authentication-rare-failure-modes]](对抗诱导稀有失败,无 mAP);✗ 多为盲长尾/对抗,非实测诊断牵引 | LTDA-Drive 式 generate-insert / X-Paste / AUTHENTICATION | **中**(增益明确但非诊断驱动) |
| **域漂移** | benchmark≠部署、跨域漏检 | ✓ 触发/验证侧证据:[[miller2022-false-negative-mechanisms]](机制分布 benchmark 与部署显著不同)、[[zimmermann2026-knowledge-guided-failure-prediction]](跨 6 个 COCO-O 域稳健,person recall 64.3%→84.5%@5%FPR);✗ 无"测出域差切片→定向生成补" | (诊断侧为主;生成补数据待接) | **中**(诊断/触发证据强,生成闭环空缺) |
| **电梯 CCTV 电瓶车(锚点)** | 小目标 + 遮挡 + 室内域差 + 稀有事件叠加 | **目标行,数据待采**(target, pending data)——尚无本场景的实测切片或生成增益原子 | 计划:GeoDiffusion/SDXL-Inpaint(本地)→ 视 Plan 2 | **无(待建)** |

## 读出结论(MVP 选哪一行)

**MVP 应在"小目标 / COCO 子集"行演示**,理由:它是最低风险的代表行——(1) COCO 标准化了 small/medium/large AP,给闭环一个**现成、可解释的度量镜**(size-specific AP),up/flat/down 都能读;(2) 所有候选生成器(GeoDiffusion 本地在手、ODGEN、X-Paste 式合成)都**已在 COCO/类似规模验证过**,生成风险最小;(3) 小目标行同时**承载锚点的核心难点**(锚点 = 小目标 + 遮挡 + 室内域差的叠加,见末行),所以它既好落地、又对锚点有迁移意义。遮挡/长尾/域差行虽各有强证据,但都掺入了"生成侧成熟但诊断接入空缺"或"非诊断驱动"的折扣,作首个闭环演示风险更高;锚点行数据未采,留作 Plan 2 之后的迁移目标。

> 共同事实(跨行):**"定向 beats 盲增"**有量化支撑——[[nguyen2025-tada-targeted-augmentation]] 显示只增强 30–40% 的"难学子集"即 +2.8%(分类,需在检测上按 size-specific AP 重测)。这正是诊断驱动闭环应**按切片下规格、而非洪水式造数据**的依据。
