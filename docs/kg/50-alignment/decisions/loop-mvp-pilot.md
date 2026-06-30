# loop_mvp 试点:执行记录 + 红队复盘

> 状态:**进行中(2026-06-30)**。这是诊断→生成→重训"最小闭环"的第一个端到端试点;代码/产物在仓库外 `/data1/qushiduo/loop_mvp/`(不入 git)。本文件记录**已做了什么 + 思考里的漏洞**,供下一步修正。对接 [diagnosis-bridge.md](diagnosis-bridge.md)(桥设计)与 [representation-map.md](../representation-map.md)(失败类型×生成复杂度)。

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

### 🔴 致命 — val2017 泄漏
诊断与 `genspec` 全部来自 **val2017**;若用 val 布局生成训练图、再在 val 上量 ΔAP_s,则**训练见过评测场景的近复制 = 泄漏**,ΔAP_s 虚高。**修法**:诊断可留 val,但生成布局改用**训练集/不重叠池**,评测用干净 held-out。

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

## 5. 下一步(对应修法)

1. **先堵泄漏**:换生成布局来源(训练池),定干净评测集——这是任何 ΔAP 数字可信的前提。
2. 开 cascade 默认值重做质量判定;full-scene 做控制变量 A/B。
3. 把 small-only / full-scene /(可选)inpaint 作为消融三 arm,**用 ΔAP_s 说话**,不预设。
4. 靶子:在堵漏 + 全量复跑前,**不急于从小目标改打 Loc**。
