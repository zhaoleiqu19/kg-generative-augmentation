# 50 — Alignment(诊断↔生成对齐:新方向工作区)

> 本目录是**新研究方向的家**,与 Phase 0–4 的旧知识树隔离,但**共享同一个论文原子池** `../90-papers/`。

## 这个区是什么

新方向的核心主张:流水线 = **诊断** + **生成** + 中间的**轻量桥**;只要诊断输出的表示和生成消费的控制接口**对齐**,桥就轻。详见 [对齐主张](alignment-thesis.md)。

## 原子 vs 视图(本区的第一原则)

- **原子(atoms)= `../90-papers/` 里的论文笔记**:客观事实,**唯一权威副本**。本区**只用 wikilink 引用,绝不复制**。新读的论文仍然写进 `../90-papers/`(走 RUNBOOK),本区只引用。
- **视图(views)= 本区的文件**:主张、对齐表、宽调研、新 GAPS、工具链决策——这些是*新方向的组织与观点*,全新撰写。

## 与旧树的关系

- 旧 `MAP.md` / `GAPS.md` / `00–30` 概念节点:**保留为 Phase 0–4 历史记录,不动**。
- 本区的 GAPS([对齐缺口](alignment-gaps.md))在新框架下 refine 旧 G1–G4,而非覆盖旧文件。

## 文件

| 文件 | 内容 | 状态 |
|---|---|---|
| [alignment-thesis.md](alignment-thesis.md) | 主张 + 几条轴 + 纳入标准 + 原子/视图原则 | 草稿(思路已敲定) |
| [representation-map.md](representation-map.md) | 诊断输出 × 生成输入 对齐表 | 起步(含已有原子) |
| [survey-diagnosis.md](survey-diagnosis.md) | 诊断方向宽调研(按表示标签组织) | 待搜索后填 |
| [survey-generation.md](survey-generation.md) | 生成方向宽调研(按表示标签组织) | 待搜索后填 |
| [alignment-gaps.md](alignment-gaps.md) | 新框架下的缺口 | 待两方向调研后写 |
| [decisions/gen-toolkit.md](decisions/gen-toolkit.md) | 本地生成工具链(模型/env/路径/下载配方) | 实测可用 |
