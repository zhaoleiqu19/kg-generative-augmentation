# 决策:本地生成工具链(gen-toolkit)

> 为对齐表"生成端"提供本地可跑的引擎。实测于 2026-06。代码仓库与权重在 git 仓库外(体积大),本文件是它们在工作区的索引。下载/环境的踩坑细节见会话记忆 `hf-download-recipe` / `gen-model-toolkit`。

## 已就位的模型

| 模型 | 控制接口 | 权重路径 | conda env | 状态 |
|---|---|---|---|---|
| **Flux.2-klein-4B** | 纯 T2I(不吃空间条件) | `/data1/qushiduo/models/flux2/FLUX.2-klein-4B` | `flux2`(py3.11/torch2.6) | 仅作前景素材/copy-paste |
| **SDXL-Inpaint** | 区域 inpaint | `/data1/qushiduo/models/sdxl-inpaint` | `flux2`(diffusers 原生) | ✅ 验证可用(~4.6s/张) |
| **GeoDiffusion** (COCO-Stuff 512) | 框/layout→检测图 | `/data1/qushiduo/models/geodiffusion-coco-stuff-512x512` | `geodiff` | ✅ 验证可用(多框含遮挡落位准) |
| **InstanceDiffusion** | 逐实例 框/点/掩码 | 未下 | 未建 | ⏸ 已选,押后 |

- GeoDiffusion 代码:`/home/qushiduo/gen_tools/GeoDiffusion`(推理入口 `run_layout_to_image.py` / `utils.generation_utils`)。

## 关键实测结论

- **GeoDiffusion**:给"类别+归一化框"(类别须属 COCO-Stuff 词表;电动车→最近类 `motorcycle`),内部编码成带位置 token 的固定模板 prompt;**输入框≈输出 GT 框**,能渲染真实遮挡+正确深度序。**画质受 SD1.x 天花板**:in-distribution 街景/车辆好,**近景大人脸弱**(电梯人物场景会吃亏)。无自由文本真实感杠杆。
- **SDXL-Inpaint**:把目标柔边画进背景指定 mask 区域,优于 copy-paste 硬接缝;**物体会略溢出 mask 框**,框非紧致 GT。
- **画质 vs 框正确性是核心权衡**:GeoDiffusion 强框弱画质;SDXL/Flux 强画质弱框。候选改进路线:**两阶段 = GeoDiffusion 定布局 → SDXL img2img 精修**(保框 + 提画质),待试。

## `geodiff` env 关键 pin(踩过坑)

py3.9 + torch==2.0.1(PyPI cu117 轮子,靠 PTX JIT 在 4090/sm_89 上跑)+ numpy==1.26.4 + diffusers==0.16.0(GeoDiffusion 硬断言)+ transformers==4.25.1 + huggingface_hub==0.16.4(diffusers0.16 需 `cached_download`)+ accelerate==0.16.0 + ftfy + bbox_visualizer + opencv-python。

## 验证产物

`/data1/qushiduo/models/_verify/`(SDXL inpaint 测试图、GeoDiffusion 5 布局批量、in-distribution 画质对比)。

## 待办

- InstanceDiffusion 建环境 + 入库。
- 两阶段(GeoDiffusion→SDXL 精修)试做。
