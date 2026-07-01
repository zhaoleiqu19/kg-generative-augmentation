# 决策:本地生成工具链(gen-toolkit)

> 为对齐表"生成端"提供本地可跑的引擎。实测于 2026-06。代码仓库与权重在 git 仓库外(体积大),本文件是它们在工作区的索引。下载/环境的踩坑细节见会话记忆 `hf-download-recipe` / `gen-model-toolkit`。

## 已就位的模型

| 模型 | 控制接口 | 权重路径 | conda env | 状态 |
|---|---|---|---|---|
| **Flux.2-klein-4B** | 纯 T2I(不吃空间条件) | `/data1/qushiduo/models/flux2/FLUX.2-klein-4B` | `flux2`(py3.11/torch2.6) | 仅作前景素材/copy-paste |
| **SDXL-Inpaint** | 区域 inpaint | `/data1/qushiduo/models/sdxl-inpaint` | `flux2`(diffusers 原生) | ✅ 验证可用(~4.6s/张) |
| **GeoDiffusion** (COCO-Stuff 512) | 框/layout→检测图 | `/data1/qushiduo/models/geodiffusion-coco-stuff-512x512` | `geodiff` | ✅ 验证可用(多框含遮挡落位准) |
| **InstanceDiffusion** | 逐实例 框/点/掩码 + 自由文本 | `gen_tools/InstanceDiffusion/pretrained/instancediffusion_sd15.pth`(13.6G)+ SD1.5 base | `instdiff`(py3.8/torch2.0.1+cu118) | ✅ 验证可用(官方 demo + **电梯锚点 demo** 均跑通,2026-06-26) |
| **MIGC** | 逐实例 框 + 短语(SD1.4) | adapter `/data1/qushiduo/models/MIGC/MIGC_SD14.ckpt`(219M)+ SD1.4 base `/data1/qushiduo/models/stable-diffusion-v1-4/` | `migc`(py3.9/torch2.0.1+cu118) | ✅ 验证可用(官方 demo + 电梯布局均出图,2026-06-29);**快**(~几秒/张, ~6GB) |
| **3DIS** | 布局→**深度图**(两阶段) | `/data1/qushiduo/models/3DIS/{unet_0901,layout_adapter}.ckpt` + 深度底模 `/data1/qushiduo/models/ldm3d-4c/` | `threedis`(py3.10/torch2.4.1+cu121) | ⚠️ 仅 **layout→depth 段**可跑(已出深度图);**FLUX 渲染段被 gated 权重卡住**(缺 `FLUX.1-Depth-dev` + `sam2_hiera_large.pt`,需 HF token)。搁置 |

- GeoDiffusion 代码:`/home/qushiduo/gen_tools/GeoDiffusion`(推理入口 `run_layout_to_image.py` / `utils.generation_utils`)。
- MIGC / 3DIS 代码:`/home/qushiduo/gen_tools/MIGC`、`/home/qushiduo/gen_tools/3DIS`。详细的"如何直接驱动"见本地未入库交接 `gen_models_handoff.md`。

## 关键实测结论

- **GeoDiffusion**:给"类别+归一化框"(类别须属 COCO-Stuff 词表;电动车→最近类 `motorcycle`),内部编码成带位置 token 的固定模板 prompt;**输入框≈输出 GT 框**,能渲染真实遮挡+正确深度序。**画质受 SD1.x 天花板**:in-distribution 街景/车辆好,**近景大人脸弱**(电梯人物场景会吃亏)。无自由文本真实感杠杆。
- **SDXL-Inpaint**:把目标柔边画进背景指定 mask 区域,优于 copy-paste 硬接缝;**物体会略溢出 mask 框**,框非紧致 GT。
- **InstanceDiffusion**:吃 全局 caption + **逐实例 `{bbox, caption}`(可选 mask)**;电梯锚点 demo(`demos/demo_elevator_ebike.json`:左电瓶车 + 中站立人 + 右**被遮挡**电瓶车)按 spec 落位渲染成功,含遮挡轴,画质受 SD1.5 限但室内 CCTV 场景可信。**待复核:输入 bbox 与渲染目标的贴合度**(决定能否直接当紧致 GT 出 COCO-json)。
- **画质 vs 框正确性是核心权衡**:GeoDiffusion 强框弱画质;SDXL/Flux 强画质弱框。候选改进路线:**两阶段 = GeoDiffusion 定布局 → SDXL img2img 精修**(保框 + 提画质),待试。

## 输入制式差异(跨模型复用布局时必看)

诊断产出 `genspec`(COCO 风格:像素 `xywh` + 逐实例 caption)。三个"框+文字"生成器的入口并不一致:

| 模型 | 坐标制式 | 布局载体 |
|---|---|---|
| InstanceDiffusion | 像素 `xywh` + 顶层全局 caption + `width/height` | **JSON 文件**(`--input_json`)|
| MIGC / 3DIS | 归一化 `xyxy`(0~1) | **写死在 .py 脚本**(无 JSON 入口)|

- 换算:`x1=x/W, y1=y/H, x2=(x+w)/W, y2=(y+h)/H`(`xywh_to_norm` 现成函数见 `MIGC/elevator_migc.py`、`3DIS/scripts/elevator_3dis_l2d.py`)。
- **桥接成本**:InstanceDiffusion 的入口 ≈ 诊断输出语言(零转换),是 alignment 论点的活证据;MIGC/3DIS 需一次性坐标换算 + 批量脚本。**注**:`genspec` 缺 InstanceDiffusion 需要的顶层全局 caption 与 `width/height`(后者可从 `gt_subset.json` 取),跑 loop 时需补一个 adapter。
- **3DIS 的 `git status` 不可信**:因 blob:none + 手工逐文件抓,会把存在的文件假报为 `deleted`;判断文件是否存在用 `ls`/`find`,别信 `git status`。

## 显存参考(VRAM,2026-07-01)

**卡 = 10× RTX 4090 D,单卡 24 GB(sm_89)。24 GB 是一切选型的天花板。**

**已用模型(实测/记录):**

| 模型 | 底座 | 推理显存 | 出处 |
|---|---|---|---|
| MIGC | SD1.4 | **~6 GB** | 记录 |
| InstanceDiffusion(base) | SD1.5 | **~13.6 GB 实测**(nvidia-smi;因 ckpt 是 **fp32**,fp16 载入约 ~7 GB);**开 refiner 后 ~16 GB+** | 实测 + 记忆 |
| SDXL-Inpaint | SDXL | ~10–12 GB(未单测,SDXL 档) | 推断 |
| GeoDiffusion | SD1.x | ~6–8 GB(未单测) | 推断 |
| Flux.2-klein-4B | 4B DiT | 可跑进 24 GB | 已用 |

> InstanceDiffusion 的 13.6 GB 偏高是 **fp32 权重**所致,非架构重;SD1.x 档 fp16 其实很轻(~6–7 GB)。

**按底座推断(fp16、512–1024px、batch 1、无 offload):**

| 底座 | 推理显存 | 对应框控模型 | 24 GB 卡 |
|---|---|---|---|
| SD1.x(0.86B) | ~6–10 GB | GLIGEN、BoxDiff、**MIGC / MIGC++(均 SD1.4)** | ✅ 轻松(但画质=InstDiff 同档,救不了天花板) |
| SDXL(2.6B) | ~10–14 GB | MIGC++ 若换 SDXL 底座(需自备,官方未提供) | ✅ 宽裕 |
| SD3-medium(2B) | ~12–18 GB | **CreatiLayout(SD3 变体)** | ✅ 装得下 |
| FLUX.1-dev(12B) | **~24–32 GB** | **EliGen、CreatiLayout-FLUX、3DIS-FLUX、Laytrol** | ⚠️ 到顶/超顶 → **需 fp8/nf4 量化或 CPU-offload**(量化后 ~15–20 GB) |

> 选型结论:**画质升级(FLUX)恰好卡在 24 GB 上沿**,4090 上要量化才进得去(同 3DIS-FLUX 的坑);**CreatiLayout-SD3(~12–18 GB)是最稳的画质提升**;GLIGEN/BoxDiff/MIGC 系都是 SD1.x,救不了小目标/画质天花板。实际显存还随分辨率/attention 实现(xformers/flash)/offload 变化,精确值须实跑。

**MIGC++ 现状订正(2026-07-01,查盘):** 本地只有 `MIGC_SD14.ckpt`(MIGC,SD1.4);**MIGC++ 只有代码、权重 `MIGC++_SD14.ckpt` 未下载**(脚本 assert 提示下载),且 **MIGC++ 也是 SD1.4 底座 → 非画质升级**。survey.md 里"MIGC++ 权重含 SD1.5/SD2/SDXL"的说法**待核实/疑似有误**(官方 repo 只发 SD1.4 版)。

## `geodiff` env 关键 pin(踩过坑)

py3.9 + torch==2.0.1(PyPI cu117 轮子,靠 PTX JIT 在 4090/sm_89 上跑)+ numpy==1.26.4 + diffusers==0.16.0(GeoDiffusion 硬断言)+ transformers==4.25.1 + huggingface_hub==0.16.4(diffusers0.16 需 `cached_download`)+ accelerate==0.16.0 + ftfy + bbox_visualizer + opencv-python。

## 验证产物

`/data1/qushiduo/models/_verify/`(SDXL inpaint 测试图、GeoDiffusion 5 布局批量、in-distribution 画质对比)。

## 待办

- 两阶段(GeoDiffusion→SDXL 精修)试做。
- **跑 loop**:`genspec`(像素 xywh + 逐实例 caption)→ InstanceDiffusion 批量出图(框当 GT)→ 冻 backbone 只调头微调 → 真实留出集量 ΔAP_small;MIGC 作"换生成器"对照臂。先验证输入 bbox 与渲染目标的贴合度(决定标签噪声)。
