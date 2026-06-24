# CLAUDE.md(中文版)

> 在本仓库工作的操作规则。公开概览见 `README.md`。**英文 `CLAUDE.md` 为权威版本**,本文为汉化。

## 这个仓库是什么

一棵用于研究**诊断驱动的生成式数据增强**的**知识树**(用于视觉模型)。树(`docs/kg/`)是副产品;真正的交付物是 **`docs/kg/GAPS.md`**——一份 2–3 个研究缺口的短名单,要求 (a) 在已调研文献中尚未解决,且 (b) 能在**锚点任务**上演示:电梯 CCTV 检测电动车 / 电动自行车。

工作由一份实施计划驱动:`docs/superpowers/plans/2026-06-23-generative-augmentation-knowledge-tree.md`(Phase 0–5)。Phase 0(宽扫描)已完成;Phase 1 = stage1-诊断深读是下一步。

## 录入流程(RUNBOOK)

所有文献每次一批录入,遵循 `docs/kg/RUNBOOK.md`:

1. 用户点名目标 → 2. agent 搜索,返回**候选清单(标题 + url),不写任何东西** → 3. 用户挑选 → 4. agent 抓取每个被选项,**仅依据抓到的正文**起草 `90-papers/authorYEAR-name.md` → 5. 接进概念节点 + `MAP.md`,把缺口追加到 `GAPS.md` → 6. 汇报 found N / fetched M / unverified K → 7. 校验通过后提交。

## 硬性规则(不可商量)

- **每批都过校验门:** `python3 docs/kg/tools/validate_kg.py` 必须 exit 0 才能提交。**用 `python3`**——这里默认 `python` 是 2.7.5。
- **反幻觉:** 没有真实抓到的 `http(s)` url 就不写论文笔记。源若抓不到,**不要**凭记忆写——换一个能抓的等价源,或标为 unverified。凭记忆起草的笔记打标签 `unverified`。
- **概念节点**(`00/10/20/30`)**绝不**可 `[[link]]` 一个带 `unverified` 标签的论文。校验器强制此点。
- **论文笔记 frontmatter 键(严格):** `title, authors, year, url, loop-stage, tags`。`loop-stage` ∈ `foundations | landscape | stage1 | stage2 | stage3 | stage4 | anchor`。
- **每个数字都带出处**(引用论文 + 位置:abstract / Table N)。不要编数字;abstract 没有就写"待从正文提取"。
- 文件名:`90-papers/authorYEAR-name.md`,kebab-case。

## 网络检索约定(踩坑学到的)

- **arXiv:** 抓 `/abs/` 页,**不要** `/pdf/`——PDF 抓回来是二进制乱码或超出抓取大小上限。`/abs/` 给干净的标题 + 作者 + 摘要。
- **MDPI(`www.mdpi.com`):对 WebFetch 返回 HTTP 403。** 不要重试它——换 arXiv / 其它能抓的同主题源。

## 仓库约定

- **仅本地、绝不提交/推送:** `generate.py`、`batch_generate.py`、`gen_prom/`、`setup_env/`(Flux 生成脚本)。仓库是公开的;保持它们 untracked。
- `handoff.md` 是易变的会话状态——untracked,绝不提交。
- 工作在 `master` 上进行;每批直接提交。提交信息前缀:`kg(phaseN): ...` 或 `kg(stageN): ...`。
- 仅在用户要求时提交/推送。

## 各文件位置

- `docs/kg/MAP.md` — 树索引(嵌套 `[[wikilinks]]`);记录疑似最薄弱的环节。每批更新。
- `docs/kg/GAPS.md` — 交付物;滚动的候选缺口列表。
- `docs/kg/00-foundations/` `10-landscape/` `20-loop/` `30-anchor-task/` — 概念节点。
- `docs/kg/90-papers/` — 每篇论文一个原子笔记。
- `docs/kg/_templates/` — `paper-note.md`、`concept-node.md`。
- `docs/kg/tools/validate_kg.py` + `test_validate_kg.py` — 校验门(用 `python3 -m pytest` 跑测试)。
