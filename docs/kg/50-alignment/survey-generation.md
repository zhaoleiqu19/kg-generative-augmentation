# 宽调研:生成方向(survey-generation)

> 状态:**待搜索后填**。流程同 [survey-diagnosis.md](survey-diagnosis.md)(RUNBOOK,候选→挑→入 `../90-papers/`→本表引用)。

## 范围

可控生成用于检测数据:layout/box 条件、区域 inpaint、实例条件、个性化;遮挡处理、框正确性、in-distribution。检测优先。

## 每篇要打的标签

- **控制接口**:框/layout / 区域inpaint / 属性文本 / 实例掩码(= 它消费什么条件)
- **框正确性**:输入框 ≈ 输出 GT?还是需反检测?
- **遮挡能力**:能否渲染真实遮挡 + 正确深度序
- **画质 / 基座**:SD1.x / SDXL / Flux / 其他(影响真实感天花板)
- **闭环友好**:能否被诊断信号驱动、批量按 spec 生成
- **验证度**:代码 / 被引 / 已复现?

## 已在库的相关原子(引用)

- [[chen2023-geodiffusion-geometric-control]] · [[zhu2024-odgen-detection-generation]] · [[zhu2025-recon-region-controllable]] · [[tang2024-aerogen-remote-sensing-generation]] — 框/layout
- [[petersen2025-scene-aware-location]] · [[girella2024-diag-indistribution-defect]] — 区域/inpaint/放置
- [[zhao2023-xpaste-copy-paste]] · [[ge2023-text2image-for-detection]] — copy-paste
- [[ruiz2022-dreambooth-subject-driven]] — 个性化

## 本地已可跑(详见 decisions/gen-toolkit)

GeoDiffusion(框/layout)、SDXL-Inpaint(区域)、Flux klein(纯 T2I)。InstanceDiffusion(实例)已选未建。

## 候选(待作者确认后入库)

> 开始本方向时在此粘贴搜索候选清单。
