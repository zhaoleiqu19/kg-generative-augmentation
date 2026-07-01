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

**已核实(2026-07-01,对 repo `cure-lab/HiBug2` 的 `prompts/get_base_attrs.py` + `get_aux_tags.py`):HiBug2 的属性 type 只有两类——`main object` / `background`**(prompt 原文:"attribute type: `main object` or `background`";全仓 grep 无 `global` 类)。每条属性再带一个 selection type `single | multi | binary`。**先前笔记里"main-object / background / global 三类(含 resolution/noise/brightness/camera-angle)的说法是错的、无 repo 依据,已更正**(见 [[chen2025-hibug2-error-slice-discovery]] 同步订正)。两类正好映射生成器的两层输入:

| HiBug2 属性 type | 例子(repo 实测 tag) | 路由到 |
|---|---|---|
| **background** | `single, background, background lighting`(暗光)、杂乱背景、`dominant background color` | → **全局 caption** |
| **main object** | `single, main object, object size`(小)、`object color`(深色)、形状/姿态/可见性/遮挡 | → **逐实例 caption** |

> 光照在 HiBug2 里是 **background 属性**(如 `background lighting`,见 `merge_attrs.py` 示例),不是单独的"全局"类;路由到全局 caption。
> 旁证:InstanceDiffusion 电梯 demo 的全局 caption 含 "bright fluorescent ceiling light, CCTV view",光照确被渲染——但"CCTV 视角"这类**不是** HiBug2 原生属性名,别当它的输出写。

**重要分水岭——只有自由文本接口的生成器能吃属性:**

| 生成器 | 吃光照/背景(全局 caption) | 吃物体属性(实例 caption) |
|---|---|---|
| InstanceDiffusion / MIGC++ / 3DIS | ✅ | ✅ |
| **GeoDiffusion**([[chen2023-geodiffusion-geometric-control]]) | ❌ box-only,固定模板,类别限 COCO-Stuff 词表 | ❌ |

→ **HiBug2 属性增强这条路线只在 InstanceDiffusion / MIGC++ / 3DIS 上成立;GeoDiffusion 上失效**(它只能摆框,控不了光照/背景)。

## 4b. genspec 的两层格式 + 字段来源(已对源码核实,2026-07-01)

诊断结果分**两层**:第 1 层是三件诊断工具的并集(富记录),桥把它塌成第 2 层(生成器真正吃的输入)。

### 第 1 层 — 组合诊断结果(每图一条)

```json
{
  "image_id": 367680, "file_name": "000000367680.jpg",
  "width": 640, "height": 480,
  "scene_attrs": { "background lighting": "low_light", "background": "cluttered" },
  "annos": [
    { "bbox": [140.6,148.8,33.5,60.1], "category_id": 19, "category_name": "horse",
      "size_bucket": "small", "tide_error": "Miss", "max_iou": 0.0,
      "obj_attrs": { "occlusion": "partially_occluded", "object color": "dark" } }
  ]
}
```

**字段来源表(每个字段谁产出,均有据):**

| 字段 | 来源 | 依据 |
|---|---|---|
| `bbox`(像素 **xywh**)、`category_id`、`size_bucket`、`max_iou` | **pycocotools** | 现有 `diag_mvp/slice_missed_small.json` 实产;size 档=COCO area<32² |
| `tide_error`(Miss/Loc/…) | **按 TIDE 阈值从 `max_iou` 推**(iou≤tb=0.1→Miss/Bkg;tb≤iou≤tf=0.5→Loc) | TIDE 六类定义见 [[bolya2020-tide-detection-errors]]。**注:TIDE 本体只出数据集级 dAP;逐实例标签是我们按其口径复算的,不是 TIDE 直接产物** |
| `scene_attrs`(background 类)、`obj_attrs`(main object 类) | **HiBug2** | type 仅 `main object`/`background`,见 §4(repo 核实) |

### 第 2 层 — InstanceDiffusion 输入(桥的产物)

**已对 `gen_tools/InstanceDiffusion/inference.py` 核实(2026-07-01)**,它只读这些键:

```json
{
  "caption": "a cluttered indoor scene, low light; a small dark horse",
  "width": 640, "height": 427,
  "annos": [
    { "bbox": [140.6,148.8,33.5,60.1], "mask": [], "category_name": "horse",
      "caption": "a small dark partially-occluded horse" }
  ]
}
```

| 键 | 是否被生成器使用 | 源码依据(inference.py) |
|---|---|---|
| `caption`(顶层全局) | ✅ 用作 prompt | `prompt = data['caption']`(L199) |
| `width` / `height` | ✅ 用于把 box 归一化 | `rescale_box(box, width, height)`(L239) |
| `annos[].bbox` = **xywh** | ✅ 必填 | `rescale_box`:`x1=x0+bbox[2]`(L132–137)→ 证明是 `[x,y,w,h]` |
| `annos[].caption`(逐实例) | ✅ | `instance_captions.append(...)`(L231) |
| `annos[].mask` | 可选,`[]` 即无 | L202 |
| `annos[].category_name` | ⚠️ **被读但注释掉、不参与生成** | L230 `# class_names.append(...)` |

> 关键:**`category_name` 不影响生成**——它只为我们自己回填合成 GT 的类别标签用;别声称它驱动生成。box 用像素 xywh、直接放原图尺寸即可(width/height 缺省则内部当 512)。

**桥的映射** = 第1层→第2层:`obj_attrs`+size+类别 → 拼 `annos[].caption`;`scene_attrs` → 拼顶层 `caption`;`bbox/width/height` 直接搬;`category_id` 另存去建训练用合成 GT。

## 5. 两步走(降风险)

- **最小闭环 = TIDE + pycocotools**:选"漏检小目标"→取漏检小框→caption 只写类别→生成更多。不依赖 HiBug2 即可跑通,风险最低。
- **+ HiBug2 = 属性增强层**:caption 带上"为什么难"的属性,使文本条件生成器造出更贴近真实失败分布的难样本。先跑通最小闭环,再加 HiBug2。

## 6. 诚实的边界(实测要验证的点)

1. **HiBug2 是图像级属性,非逐实例像素 grounding**:把切片级属性贴到具体框上是近似;若 recon 后拿不到实例级关联,这层近似要写明(GH-ESD 在此更干净)。
2. **自由文本是软控制**:框位置硬约束,但"暗光/遮挡"属性是概率性影响,需多采样 + 过滤(参 [[zhao2023-xpaste-copy-paste]] 的 CLIP 过滤、[[yurt2025-ltda-drive-longtail]] 的 LLM 过滤)。
3. **画质天花板**:InstanceDiffusion=SD1.5,暗光真实感弱于 3DIS-FLUX(Flux 底座)——若失败强依赖光照真实感,3DIS 可能更合适(横评要看)。

## 7. 实测验证(2026-06-29,诊断半环 + grounding)

诊断半环 + grounding 已端到端跑通(无需生成器、无需训练)。**数据 = COCO val2017 前 500 图子集**(代表性数字待全量 val2017 复跑);检测器 = torchvision 预训练 **Faster R-CNN R50-FPN**(COCO_V1,未微调);脚本/产物在 `diag_mvp/`(repo 内、但 `.gitignore`,不入 git;2026-06-30 由 `/data1` 迁入)。

- **size-specific AP(pycocotools)**:AP@[.50:.95] all=0.419,**small=0.258**,medium=0.457,large=0.528 → 小目标最弱。
- **TIDE dAP(吃 mAP 的误差)**:Loc=6.05、Miss=5.91 主导;Bkg=3.94、Cls=2.74、Both=1.15、Dupe=0.25;特类 FP=17.47 / FN=12.51。→ 失败轴 = **定位 + 漏检**,集中在小目标(印证 §3 数据流第一步的假设)。
- **grounding(pycocotools)**:漏检+小目标实例 **698 / 1312 小目标 GT**,**小目标召回 ≈ 0.47**;漏检最多的类:person(115)、chair(42)、book(40)、cup(29)、bird(29)…
- **生成规格产物**:`genspec_missed_small.json` = **183 张图**各带其漏检小目标的 `{bbox, caption:"a small <cat>"}` —— 正是生成器(InstanceDiffusion/3DIS/MIGC++)吃的逐实例输入形状。下一步把 HiBug2 的全局/物体属性拼到 caption 上,即成完整生成规格。

> 工程备注:借用现成 `ovdeim_stage3` env(已含 torch2.6/torchvision0.21/pycocotools/cv2/matplotlib),只加装 seaborn/appdirs/tidecv;大文件下载(torchvision 权重、大 wheel)**必须不带代理**(代理对大体下载会 IncompleteRead)。详见会话记忆 hf-download-recipe。
