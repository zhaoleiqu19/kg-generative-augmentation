# kg-generative-augmentation(中文版)

> 本目录是仓库的**中文汉化版**,供展示工作流程之用。**英文原文是唯一权威来源**(校验器依赖英文 frontmatter);中文为另存,可能略滞后。原文见各文件在 `docs/` 下的对应英文版。

一棵用于研究**诊断驱动的生成式数据增强(diagnosis-driven generative data augmentation)** 的知识树:不要盲目增强——先找出数据/模型在哪里失败,再精确合成那些失败样本,然后验证差距是否被填上。

知识树本身只是副产品;**真正的交付物是 [`docs/kg/GAPS.md`](../kg/GAPS.md)(中文版见 [研究缺口-GAPS.md](研究缺口-GAPS.md))**——一份研究缺口短名单,要求每个缺口 (a) 在已调研文献里尚未被解决,且 (b) 能在一个具体的**锚点任务**上演示:电梯 CCTV 检测电动自行车 / 电动车。

---

## 中文版导航

| 文件 | 内容 | 英文原文 |
|---|---|---|
| [操作规则-CLAUDE.md](操作规则-CLAUDE.md) | 在本仓库工作的硬性规则(录入流程、反幻觉、校验门) | `CLAUDE.md` |
| [知识树-MAP.md](知识树-MAP.md) | 整棵树的嵌套索引 + 最薄弱环节判断 | `docs/kg/MAP.md` |
| [研究缺口-GAPS.md](研究缺口-GAPS.md) | **交付物**:候选研究缺口 G1–G4 | `docs/kg/GAPS.md` |
| [术语表-glossary.md](术语表-glossary.md) | 全树共用术语 | `docs/kg/00-foundations/glossary.md` |
| [RUNBOOK-录入流程.md](RUNBOOK-录入流程.md) | 每批文献的录入七步法 | `docs/kg/RUNBOOK.md` |
| **landscape/**(全景层) | | `docs/kg/10-landscape/` |
| ├ [生成式增强全景.md](landscape/生成式增强全景.md) | 宽扫描全景图 | `generative-augmentation-landscape.md` |
| ├ [合成数据有用吗.md](landscape/合成数据有用吗.md) | 有用 vs 有害的证据账本 | `does-synthetic-data-help.md` |
| └ [相关系统-全闭环邻居.md](landscape/相关系统-全闭环邻居.md) | 离全闭环最近的现有系统 | `related-systems-whole-loop.md` |
| **loop/**(四阶段主干) | | `docs/kg/20-loop/` |
| ├ [阶段1-诊断.md](loop/阶段1-诊断.md) | 错误切片发现 / 失败归因 | `stage1-state-of-the-art.md` |
| ├ [阶段2-spec.md](loop/阶段2-spec.md) | 诊断→生成规格的桥 | `stage2-state-of-the-art.md` |
| ├ [阶段3-合成.md](loop/阶段3-合成.md) | 生成工具箱 | `stage3-state-of-the-art.md` |
| └ [阶段4-闭环.md](loop/阶段4-闭环.md) | 过滤+重训+迭代安全 | `stage4-state-of-the-art.md` |
| [锚点任务-电梯电动车.md](锚点任务-电梯电动车.md) | 电梯电动车检测试验台(占位) | `docs/kg/30-anchor-task/task-sota.md` |
| [流水线-spec与plan.md](流水线-spec与plan.md) | 流水线设计规格 + 9 任务实施计划 | `docs/superpowers/specs|plans/...` |
| [论文索引.md](论文索引.md) | **29 篇**精读笔记一句话索引表 | `docs/kg/90-papers/*` |

---

## 目录结构(英文仓库)

- `docs/kg/` — Obsidian 兼容的 Markdown 笔记网
  - `MAP.md` — 整棵树的嵌套 `[[wikilinks]]` 索引
  - `GAPS.md` — 候选研究缺口的滚动列表
  - `RUNBOOK.md` — 每批文献的录入流程
  - `00-foundations/` `10-landscape/` `20-loop/` `30-anchor-task/` — 概念节点
  - `90-papers/` — 每篇论文一个原子笔记
  - `tools/validate_kg.py` — 校验器 / 测试门
- `docs/superpowers/specs/` — 设计文档
- `docs/superpowers/plans/` — 实施计划
- `pipeline/` — 流水线代码(骨架 T1–T2 + 临时决策 T3–T4,在 `feat/pipeline-skeleton` 分支)

## 校验

校验器强制检查 frontmatter 完整性、链接完整性,以及反幻觉护栏(概念节点不得引用 `unverified` 论文):

```bash
python3 docs/kg/tools/validate_kg.py
cd docs/kg/tools && python3 -m pytest test_validate_kg.py -q
```
