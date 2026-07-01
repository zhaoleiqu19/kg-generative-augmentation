# loop_mvp 试点:执行记录 + 红队复盘

> 状态:**进行中(2026-06-30)**。这是诊断→生成→重训"最小闭环"的第一个端到端试点;代码/产物在 `loop_mvp/`(repo 内、但 `.gitignore`,不入 git;2026-06-30 由 `/data1` 迁入)。本文件记录**已做了什么 + 思考里的漏洞**,供下一步修正。对接 [diagnosis-bridge.md](diagnosis-bridge.md)(桥设计)与 [representation-map.md](../representation-map.md)(失败类型×生成复杂度)。

## 1. 试点是什么

把 [diagnosis-bridge.md](diagnosis-bridge.md) 的设计跑成一条最小可量化闭环:

```
诊断(FRCNN+TIDE+pycocotools, val2017)
  → genspec_missed_small.json(183 图、698 个漏检小目标的 {bbox, caption})
  → 适配器 build_instdiff_inputs.py → InstanceDiffusion 输入 + 合成 GT(512 空间)
  → 生成新图(框=输入 GT)
  → 冻结 backbone、微调检测头 → 量 ΔAP_small
```

生成器 = [[wang2024-instancediffusion-instance-control]](本地 `instdiff` env,GPU8)。

## 2. 已完成

- **适配器**:`build_instdiff_inputs.py` → 183 个输入 JSON + `synth_layout_512.json`(698 框,category_id 全部复原、0 缺失;542/698 为 <32px 小框)。
- **de-risk**:3 个代表布局 ×(1~2 seed)生成 + 框叠加,目检框贴合度。
- **A/B(full-scene)**:对最糊的两张(120420、340175)改用**完整 COCO 布局**重生成,与"只喂漏检小框"对照。

## 3. 表面发现(注意:被 §4 部分推翻)

- 只喂漏检小框时,小框渲染成"色块/糊";full-scene(喂全部框)后场景连贯、小目标落在真实语境里。
- **初步结论(待证)**:糊主要来自"我们只喂了漏检小目标、丢掉了场景锚定大物体",不是生成器分辨率天花板。

## 4. 红队:思考里的漏洞(按严重度)

> 这一节是本文件的重点。上面的"发现"在下列漏洞修正前**不能当结论**。

### 🔴 致命 — val2017 泄漏 — **已定方案(2026-06-30)**
诊断与 `genspec` 全部来自 **val2017**;若用 val 布局生成训练图、再在 val 上量 ΔAP_s,则**训练见过评测场景的近复制 = 泄漏**,ΔAP_s 虚高。**致命点 = "从 val 布局生成"**:合成图复刻 val 场景构图(同框⇒同布局),检测头在评测场景的近复制上训练 → ΔAP_s 测的是**记忆**而非小目标检测能力。

**修正设计(推荐,最小且干净)**——硬保证 *训练像素 ∩ 评测 = ∅*:

| 阶段 | 数据池 | 角色 |
|---|---|---|
| 诊断 | val2017 | **仅参谋**:定失败轴(漏检小目标)+ 弱类(person/chair/book/cup/bird)。**此处无像素进训练。** |
| 生成源 | **train2017** | 选含这些弱类小实例的 train 图 → 其 GT 框喂 InstanceDiffusion → 合成图 + GT。 |
| 训练 | real train ∪ synth-from-train | 两 arm,仅增强部分不同。 |
| 评测 | val2017(不动) | ΔAP_s = AP_aug − AP_base。 |

干净的根据:每张训练场景来自 train2017,评测是 val2017,COCO train ∩ val = ∅(天然不重叠)→ ΔAP_s 测泛化,非记忆。**标签也不泄漏**:输入框即合成图的 GT,来自 train。**保险栓**:synth↔val2017 跑 perceptual-hash/embedding 近重检测,丢掉过近的合成图。

**残留 caveat(诚实)**:诊断仍读 val = 用评测集选"增强什么",是 *meta 泄漏*,所有诊断驱动增强固有。(A,推荐)接受+披露,硬保证仍成立=标准做法;(B,可发表)三分不重叠 image-id:诊断 train-A / 生成 train-B / 评测 val2017,连 meta 泄漏也去掉。先上 A,B 留作论文级升级。

**数据已就绪**:`/data/COCO` 含 train2017(118,287 图 + `instances_train2017.json`)与 val2017(5,000)。诊断脚本 `diag_mvp/run_frcnn_tide.py` 的 `COCO_ROOT=/data/COCO`。

### 🟠 高 — 把生成器质量调低了再下结论
de-risk/peek 全程 `--cascade_strength 0`,而默认 **0.35(SDXL-Refiner 精修)**(`inference.py` L112/L177)。"糊"的判断是**未精修 base 输出**,低估了 InstanceDiffusion。**修法**:开默认 cascade 重做质量判定。

### 🟠 高 — full-scene A/B 是三变量混淆
`peek`→`peek_full` 同时改了:①加大锚框 ②全局 caption(`a small cell phone, a small car` → `person, cell phone, umbrella, bench, bird`)③逐实例 caption。**"框是主因"未被分离证明**。**修法**:控制变量——只换框/只换 caption 各跑一次。

### 🟠 高 — "small-only = 噪声、ΔAP≈0" 是猜测
从未微调过;de-risk 只证明**视觉糊**,未证明**训练无用**。copy-paste 文献中粗糙贴图也能提升 recall(objectness)。**修法**:把 small-only 作为一条真实 arm 跑进消融,别预设结论。

### ⚪ 已降级 — 靶子排序在 500 图上脆弱(非前置问题)
TIDE dAP:Loc 6.05 vs Miss 5.91,仅差 0.14,样本=val2017 前 500 图。曾标"高",但**用户判定非主要问题**:既然策略是"按失败类型分别决定生成手段",就不依赖这个精确排序(谁先做不由 0.14 的差决定)。保留为记录,不放进前置待解决项。

### 🟡 中 — "每类误差都能用生成修"并不成立
Dupe = NMS/检测头问题,数据增强治不了;**Loc/Bkg 也只部分可由数据修**(定位差可能是回归头/特征分辨率)。菜单"对应生成任务"列暗示了过于干净的映射。**修法**:每条失败先判"是否数据可修",再谈生成。

### 🟡 中 — 分辨率链未对齐
InstanceDiffusion 出 512;COCO small 定义在原图分辨率;检测器常在更高分辨率训练。512 生成→上采样训练,小目标更糊。**修法**:明确生成/训练/评测三处分辨率,必要时切图放大(tiling)。

### 🟡 中 — HiBug2 那条是"理论可得"非"实测可得"
尚未跑 HiBug2;recon 显示它**只标中心物体 + 依赖 GPT-4o**(见 [[chen2025-hibug2-error-slice-discovery]] Recon findings)。在 COCO 密集小目标场景产出可能很弱。别与已验证的 TIDE/pycocotools 并列当等价可用。

### ⚪ 框架 — "复杂度"是多维被压成一维
至少三维:**可表达性**(接口能否描述)×**保真度**(生成器能否画出)×**可验证性**(是否需多采样+过滤)。详见 [representation-map.md](../representation-map.md) 细化表。正面收获:这张表本质=**每种失败的桥有多重**,量化了 alignment 主张——但也诚实暴露:**"桥轻"只对"框可表达"的失败成立**。

## 4c. 假诊断生成探针(2026-07-01,测生成器天花板)

**目的**:不等 HiBug2、不碰真实泄漏,先用**人造的"完整诊断结果"**(Tier-1,带丰富属性)跑 InstanceDiffusion,看生成器到底能做到什么程度。产物在 `loop_mvp/fake_diag/`(fake_diagnosis.json → bridge_fake.py → gen_inputs → out_base)。3 个整场景(街景/客厅/公园)×2 seed,**base SD1.5、cascade 0**(refiner 半缓存 + 代理限速 40kB/s,ETA 9h,已弃用 0.35,改 mirror 后台补;见 [gen-toolkit] 与记忆 hf-download-recipe)。

**能做到(强项):**
- **全局构图 + 场景连贯**:三景都可信,设定/光照对(街=黄昏暗光、客厅、公园秋景)。
- **大/中框**:位置贴合好,类别 + 属性都吃(red car→红车、gray couch→灰沙发、wooden bench→木凳、坐/站姿、**遮挡的 cat(~60px)可辨识地画在沙发上**)。
- **full-scene 修法被证实**:小目标框旁边**放大锚框**后,上次那种"整图糊成色块"消失了,场景成立。

**做不到 / 有代价(天花板,已放大逐框核实 2026-07-01):**
> ⚠️ **更正前一版结论**:前面写"<25px 一律画不出、手机丢失"是**错的**(被 512 缩略图误导)。放大逐框看(`_phone_crop_base.png` / `_far_person_crop.png` / `_bird1_crop.png`)真实情况:
- **手机(框 21×49px)= 画出来了**,是清晰黑手机——但**被框强制填满→竖着立起来**(像立起的 iPad),因为框是竖长条、InstanceDiffusion 把物体撑满框。
- **远处人(框 22×56px)= 也画出来了**,可辨识。
- **真正失败的只有鸟**(框 15×15 / 20×18,**两维都 <20px、面积 ~225–360px²**):没入树冠、无鸟。
- **天花板不是"宽度<某阈值",而是"面积/最短边太小"**:窄而高(手机/远人,面积~1000px²、长边≥45px)能画;两维都极小(鸟)才废。

**真正的失败模式 = 框硬填 → 姿态/尺度失真**(非"画不出"):
- **框=GT 仍成立**(像素确实填满框,标签几何正确);但物体**不自然**(竖手机)→ 检测器可能学歪先验。
- **关键**:竖手机部分是**我手搓的 26×46 竖框**造成的;真实 missed-GT 的手机框带**真实长宽比**(躺平=宽框),真流程会**少**这种失真。
- **框贴合仍是松的**:物体大致填满框区但非像素级紧致 → 有**标签松弛**。

**对计划的硬含义**:面积极小(两维<~20px)的目标 InstanceDiffusion@512 画不出 → 那一小撮会得到"GT 标了但像素是背景"的噪声;更普遍的是**框硬填导致的姿态失真**(用真实 GT 框可缓解)。因此小目标合成仍需在下列 fork 里选(这条 fork 是本探针的主要产出):
1. **高分辨率 / tiling**:在放大 crop 里画小目标再缩回(对齐 §4 🟡 分辨率链)。
2. **改打"小而不微"档(~32–64px)**:该档渲染没问题。
3. **最微档改用 copy-paste**:真实小目标 patch 贴进生成场景,绕开扩散画不出的问题。

**refiner 对照(2026-07-01,已验证)**:refiner 经 hf-mirror 补齐后,对客厅景跑了 `cascade 0.35`(`out_refined/900002`,`*_xl_s0.35_n20.png`)。结论——
- **画质明显提升**(材质/光照/清晰度)→ 印证旧 peek 用 `cascade 0` **低估了** InstanceDiffusion,判质必须开 refiner。
- **~60px 的猫:大赢**,精修后清晰无歧义、遮挡属性保留 → **"小而不微"32–64px 档,base+refiner 真的好用**(强化 fork 选项 2)。
- **机理**:img2img 只精修既有像素,**无中生有不了 base 没画上的目标**——所以**面积极小的鸟(base 就没画)refiner 救不回**;而 base 已画上的**手机/远人 refiner 能精修**,但**姿态失真(竖手机)refiner 不纠**(那是布局硬填、非纹理问题)。
- **修正边界**:refiner 帮"base 已放上"的目标提质,不帮"两维都极小、base 没放上"的目标(鸟)→ fork 选项 1(tiling)/3(copy-paste)对最微档仍不可省。

## 5. 下一步(对应修法)

1. **先堵泄漏**:✅ 方案已定(见 §4 🔴 修正设计)——生成源改 train2017、评测留 val2017(train∩val=∅)、加 synth↔val 近重过滤。实现待跑。
2. 开 cascade 默认值重做质量判定;full-scene 做控制变量 A/B。
3. 把 small-only / full-scene /(可选)inpaint 作为消融三 arm,**用 ΔAP_s 说话**,不预设。
4. 靶子:在堵漏 + 全量复跑前,**不急于从小目标改打 Loc**。
5. **定小目标合成路线**(见 §4c fork):高分辨率/tiling vs 改打 32–64px 档 vs 最微档 copy-paste——这决定整条 loop 对 <25px 目标到底可不可行。
