# 宽调研:诊断方向(survey-diagnosis)

> 状态:**待搜索后填**。按 RUNBOOK——先给候选清单(标题+url)→ 作者挑 → 抓 `/abs/` 正文 → 写进 `../90-papers/` → 本表只引用。

## 范围

检测的失败诊断 / 错误切片发现 / 失败归因 / 漏检机理 / 失败预测。检测优先,分类作旁证。

## 每篇要打的标签

- **表示标签**:框 / 区域 / 属性文本 / 实例掩码(= 它输出什么形式的失败描述)
- **任务**:检测 / 分类 / 分割
- **是否为检测设计**:purpose-built / 多任务含检测 / 仅分类可迁移
- **可重复测量**:重训后能否再跑同一诊断闭环
- **验证度**:有代码 / 被引 / 已复现?(新 ≠ 已验证)

## 已在库的相关原子(引用,不复制)

- [[zhang2026-gh-esd-instance-slice-discovery]] — 实例级(检测/分割),表示≈框/实例
- [[chen2025-hibug2-error-slice-discovery]] — 多任务含检测,表示≈属性文本
- [[eyuboglu2022-domino-slice-discovery]] — 分类,表示≈属性文本
- [[chegini2023-clip-diffusion-failure-mitigation]] — 分类,诊断→生成桥

## 候选(待作者确认后入库)

> 上一轮搜索已得若干候选(TIDE / Hoiem / 漏检机理 / 安全攸关漏检预测 / Manifold-Compactness / CB-SLICE),见会话记录。**尚未写入**。开始本方向时在此粘贴候选清单。
