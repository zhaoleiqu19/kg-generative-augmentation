# 录入流程(一批)(RUNBOOK 中文版)

1. 用户点名目标(综述 / 子主题 / "填 stage1-诊断")。
2. agent 加载 WebSearch/WebFetch,搜索,返回**候选清单(标题 + url)——暂不写任何东西**。
3. 用户挑选哪些候选写成完整笔记。
4. agent 对每个被选项 WebFetch;**仅依据抓到的正文**起草 `90-papers/authorYEAR-name.md`。
5. agent 更新概念节点、MAP.md(新 wikilink),把任何缺口追加到 GAPS.md。
6. agent 汇报:found N、fetched M、couldn't verify K。
7. 跑 `python3 docs/kg/tools/validate_kg.py` → 必须 exit 0。提交。

**护栏:** 没有抓到的 http url 就不写笔记;凭记忆起草的打标签 `unverified`;概念节点绝不链接 unverified 论文;每个数字都带出处。
