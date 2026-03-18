---
name: financial-analyzer
description: 企业年报附注优先财务分析 skill。用于让 Codex 先定位并抽取附注，再逐章复核、逐章学习、逐章写入知识库，最后完成整案分析与 Soul 导出。
---

# Financial Analyzer

本 skill 的核心不是“脚本自己完成分析”，而是“脚本先做通用模板抽取，Codex 再按工作流逐步复核、补充、学习和落产物”。

## 工作定位

- `financial_analyzer.py` 是通用模板脚本，不是最终分析代理。
- Codex 是实际执行分析与知识学习的主体。
- 脚本输出默认视为草稿或 scaffold，不能未经复核直接当最终结论。
- 遇到特定案例时，允许在单案工作目录内修改脚本副本或辅助脚本；只有可复用改进才回写通用模板。

## 强制流程

1. 先识别报告类型、公司名、报告期、币种、审计意见。
2. 不直接进入全文分析，必须先定位财报附注。
3. 通过关键词搜索找附注候选：
   - `财务报表附注`
   - `合并财务报表项目注释`
   - `Notes to the Financial Statements`
4. 对命中点前后做抽样阅读，确认已经进入正式附注区间。
5. 在已确认的附注区间内建立主附注目录。
   - 只记录主附注，如 `1`、`10`、`17`、`18`
   - `(a)(b)` 等子附注并入父附注，不单独成章
6. 先运行模板脚本，生成章节记录与 scaffold。
7. Codex 必须复核脚本输出的附注边界、章节划分和章节摘要。
8. Codex 逐章阅读 `chapter_records`，逐章提炼：
   - 章节结论
   - 证据摘录
   - 对正式知识库的增量或修正
9. 每完成一章，就通过知识写入辅助脚本写入正式 `knowledge_base.json`，并记录 adoption log。
10. 全部章节完成后，Codex 汇总整案分析，生成正式 `analysis_report.md`、`final_data.json`、`soul_export_payload.json` 和 `financial_output.xlsx`。

## 正文边界

- 正文只用于元信息识别和附注定位。
- 正文不得直接进入 `chapter_records.jsonl`。
- 正文不得直接充当最终结论证据。
- 找不到可信附注区间时直接失败，不降级全文分析。

## 运行入口

模板脚本入口：

- `scripts/financial_analyzer.py`

批处理入口：

- `scripts/run_batch_pipeline.py`

知识写入/运维入口：

- `scripts/write_knowledge_adoption.py`
- `scripts/rollback_knowledge_adoption.py`
- `scripts/show_knowledge_adoption.py`

## 运行态 Runtime 绑定

已安装 skill 在生产态必须绑定项目内 runtime，而不是把动态状态写回 `~/.codex/skills`。

### `runtime_config` 发现顺序

1. CLI 参数 `--runtime-config`
2. 环境变量 `FINANCIAL_ANALYZER_RUNTIME_CONFIG`
3. 从当前工作目录向上逐级搜索 `runtime/runtime_config.json`

### 哪些内容必须走外部 runtime

- `runtime/runtime_config.json`
- `runtime/knowledge/knowledge_base.json`
- `runtime/knowledge/adoption_logs/`
- `runtime/state/registry/processed_reports/processed_reports.json`
- `runtime/state/batches/`
- `runtime/state/logs/`
- `runtime/state/tmp/`

### 明确禁止

以下内容不得写入 `~/.codex/skills`：

- 任意 `runtime_config`
- 任意正式 `knowledge_base` 副本
- 任意 registry / batches / logs / tmp 运行态目录
- 运行中对 `SKILL.md`、`references/*.md` 的自发改写

## 模板脚本成功态产物

模板脚本每次成功运行必须至少生成：

- `run_manifest.json`
- `chapter_records.jsonl`
- `analysis_report_scaffold.md`
- `focus_list_scaffold.json`
- `final_data_scaffold.json`
- `soul_export_payload_scaffold.json`

这些文件只代表“脚本初稿已生成”，不代表最终分析已完成。

## 最终交付产物

完成 Codex 逐章复核后，单案运行目录的正式交付产物为：

- `analysis_report.md`
- `final_data.json`
- `soul_export_payload.json`
- `financial_output.xlsx`

## 运行后最小验收清单

模板脚本成功态至少满足以下条件：

1. `run_manifest.json` 中 `status=success`。
2. `run_manifest.json` 中 `script_output_mode=scaffold_only`。
3. `run_manifest.json` 中 `codex_review_required=true`。
4. `chapter_records.jsonl` 每条记录都包含：`chapter_no`、`chapter_title`、`status`、`summary`。
5. scaffold 文件均存在且非空。

Codex 完整复核态至少满足以下条件：

1. 正式 `analysis_report.md` 已生成。
2. 正式 `final_data.json` 已生成。
3. 正式 `soul_export_payload.json` 已生成。
4. 若发生知识写入，则 `runtime/knowledge/adoption_logs/` 中存在对应日志。

## 进化原则

- 不再把 `pending_updates.json` 作为知识学习主路径。
- 通用模板脚本只负责提高起点，不负责覆盖所有案例。
- 知识学习由 Codex 按章完成，脚本只提供结构化地基和持久化工具。
- 每次章节级正式写入都应遵循 `knowledge_adoption_delta_contract.md` 的 delta 口径，并保留 adoption log / rollback 线索。
- 某个 case 的临时修补，默认先留在该 case 工作目录；只有复用价值明确时才提升为通用能力。
