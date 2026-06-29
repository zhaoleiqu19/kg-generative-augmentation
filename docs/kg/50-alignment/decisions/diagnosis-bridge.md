# 设计笔记:诊断→生成 的轻桥(diagnosis-bridge)

> 状态:**设计/方向记录(2026-06-29),未敲定**。三件诊断工具尚未逐一上手实测;本文件只记录"打算怎么接",实测后再在 [demo-task-selection.md](demo-task-selection.md) 定稿。对接的是 [alignment-thesis.md](alignment-thesis.md) 说的"桥塌缩成一层轻策略"。

## 1. 目标:把诊断输出变成生成器的原生输入

生成器([[wang2024-instancediffusion-instance-control]] / [[zhou2024-3dis-depth-decoupled-instance]] / [[zhou2024-migcpp-multi-instance]])吃 **全局 caption + 逐实例 `{box, caption}`**。桥要做的就是从检测器的实测失败,产出这份规格。

## 2. 三件全开源诊断工具的分工(替代无代码的 [[zhang2026-gh-esd-instance-slice-discovery]])

| 缺的那块 | 谁补 | 产物 |
|---|---|---|
| **哪类失败**(选轴) | **TIDE**([[bolya2020-tide-detection-errors]]) | 6 类误差的 dAP 隔离贡献 → 锁定主导失败类型(小目标常为 Miss/Loc) |
| **失败在哪**(grounding) | **COCO eval / pycocotools** | 取未匹配 GT 框 = 具体 `(类别, bbox, 尺寸档)` |
| **失败长啥样**(属性) | **HiBug2**([[chen2025-hibug2-error-slice-discovery]]) | 属性切片 → 逐实例/场景 caption 文本 |

> 核心:HiBug2 缺的"框在哪",用 COCO 评测里漏检/低分的 GT 框补上 —— 全开源件 DIY 出 GH-ESD 想给的 grounded 实例切片,不需 GH-ESD 代码。

## 3. 数据流(COCO 小目标演示)

```
检测器在 COCO 推理
  → ① TIDE:dAP 分型,定"漏检小目标"轴
  → ② pycocotools:捞出 漏检+small 的 GT 实例 = (class, bbox, size, 图)
  → ③ HiBug2:给这批失败的属性切片(背景/光照/物体属性)
  → 组装生成规格(见 §4 路由)
  → InstanceDiffusion/3DIS 生成 新图+框(框=输入 GT)= 新标注数据
  → 检测器重训 → 再跑 TIDE:Miss 的 dAP 降了吗?(闭环靠重新诊断闭合,可量化)
```

桥"轻"在:无需训练的翻译器,TIDE 选类型 + pycocotools 取框 + HiBug2 给词,拼成 `{box, caption}` 基本是模板 + 采样策略。

## 4. HiBug2 属性 → 两层 caption 的路由(关键对接点)

HiBug2 属性本就分 **主体物体 / 背景 / 全局** 三类,正好映射生成器的两层输入:

| HiBug2 属性类 | 例子 | 路由到 |
|---|---|---|
| **全局**(光照、视角、天气) | 暗光、CCTV 视角 | → **全局 caption** |
| **背景** | 杂乱背景、电梯内 | → **全局 caption** |
| **主体物体**(颜色/姿态/遮挡/尺寸) | 小、被遮挡、深色 | → **逐实例 caption** |

已验证:InstanceDiffusion 的电梯 demo 全局 caption 含 "bright fluorescent ceiling light, CCTV view",光照/视角确被渲染。

**重要分水岭——只有自由文本接口的生成器能吃属性:**

| 生成器 | 吃光照/背景(全局 caption) | 吃物体属性(实例 caption) |
|---|---|---|
| InstanceDiffusion / MIGC++ / 3DIS | ✅ | ✅ |
| **GeoDiffusion**([[chen2023-geodiffusion-geometric-control]]) | ❌ box-only,固定模板,类别限 COCO-Stuff 词表 | ❌ |

→ **HiBug2 属性增强这条路线只在 InstanceDiffusion / MIGC++ / 3DIS 上成立;GeoDiffusion 上失效**(它只能摆框,控不了光照/背景)。

## 5. 两步走(降风险)

- **最小闭环 = TIDE + pycocotools**:选"漏检小目标"→取漏检小框→caption 只写类别→生成更多。不依赖 HiBug2 即可跑通,风险最低。
- **+ HiBug2 = 属性增强层**:caption 带上"为什么难"的属性,使文本条件生成器造出更贴近真实失败分布的难样本。先跑通最小闭环,再加 HiBug2。

## 6. 诚实的边界(实测要验证的点)

1. **HiBug2 是图像级属性,非逐实例像素 grounding**:把切片级属性贴到具体框上是近似;若 recon 后拿不到实例级关联,这层近似要写明(GH-ESD 在此更干净)。
2. **自由文本是软控制**:框位置硬约束,但"暗光/遮挡"属性是概率性影响,需多采样 + 过滤(参 [[zhao2023-xpaste-copy-paste]] 的 CLIP 过滤、[[yurt2025-ltda-drive-longtail]] 的 LLM 过滤)。
3. **画质天花板**:InstanceDiffusion=SD1.5,暗光真实感弱于 3DIS-FLUX(Flux 底座)——若失败强依赖光照真实感,3DIS 可能更合适(横评要看)。

## 7. 实测验证(2026-06-29,诊断半环 + grounding)

诊断半环 + grounding 已端到端跑通(无需生成器、无需训练)。**数据 = COCO val2017 前 500 图子集**(代表性数字待全量 val2017 复跑);检测器 = torchvision 预训练 **Faster R-CNN R50-FPN**(COCO_V1,未微调);脚本/产物在仓库外 `/data1/qushiduo/diag_mvp/`。

- **size-specific AP(pycocotools)**:AP@[.50:.95] all=0.419,**small=0.258**,medium=0.457,large=0.528 → 小目标最弱。
- **TIDE dAP(吃 mAP 的误差)**:Loc=6.05、Miss=5.91 主导;Bkg=3.94、Cls=2.74、Both=1.15、Dupe=0.25;特类 FP=17.47 / FN=12.51。→ 失败轴 = **定位 + 漏检**,集中在小目标(印证 §3 数据流第一步的假设)。
- **grounding(pycocotools)**:漏检+小目标实例 **698 / 1312 小目标 GT**,**小目标召回 ≈ 0.47**;漏检最多的类:person(115)、chair(42)、book(40)、cup(29)、bird(29)…
- **生成规格产物**:`genspec_missed_small.json` = **183 张图**各带其漏检小目标的 `{bbox, caption:"a small <cat>"}` —— 正是生成器(InstanceDiffusion/3DIS/MIGC++)吃的逐实例输入形状。下一步把 HiBug2 的全局/物体属性拼到 caption 上,即成完整生成规格。

> 工程备注:借用现成 `ovdeim_stage3` env(已含 torch2.6/torchvision0.21/pycocotools/cv2/matplotlib),只加装 seaborn/appdirs/tidecv;大文件下载(torchvision 权重、大 wheel)**必须不带代理**(代理对大体下载会 IncompleteRead)。详见会话记忆 hf-download-recipe。
