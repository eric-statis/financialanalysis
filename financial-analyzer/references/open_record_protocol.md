# Open Record Protocol

## 目标

用稳定外壳承载每次运行的核心产物，同时明确区分：

- 模板脚本生成的结构化初稿
- Codex 复核后的正式分析与知识沉淀

## 章节记录

`chapter_records.jsonl` 每行一条记录，固定核心字段如下：

- `chapter_no`
- `chapter_title`
- `status`
- `summary`

扩展载荷如下：

- `attributes`
- `numeric_data`
- `findings`
- `anomalies`
- `evidence`
- `extensions`

记录范围仅限“已确认附注主章节”，正文不进入 `chapter_records.jsonl`。
`attributes` 至少补充：

- `note_no`
- `note_scope`
- `locator_evidence`

读取旧记录时，只依赖固定核心字段；扩展字段缺失不能导致失败。

## 模板脚本 scaffold

模板脚本允许输出以下 scaffold：

- `analysis_report_scaffold.md`
- `focus_list_scaffold.json`
- `final_data_scaffold.json`
- `soul_export_payload_scaffold.json`

这些 scaffold 只代表“脚本初稿”，必须经过 Codex 复核后才能升级为正式交付。

## 最终数据

正式 `final_data.json` 固定核心字段如下：

- `entity_profile`
- `key_conclusions`
- `topic_results`

各主题节点允许通过 `attributes` 和 `extensions` 自由增长。

## Soul 导出契约

正式 `soul_export_payload.json` 是面向 Soul Excel 导出层的稳定接口，固定核心字段如下：

- `contract_version`
- `template_version`
- `generated_at`
- `entity_profile`
- `source_artifacts`
- `module_manifest`
- `overview`
- `kpi_dashboard`
- `financial_summary`
- `debt_profile`
- `liquidity_and_covenants`
- `optional_modules`
- `evidence_index`

要求：

- 固定骨架模块必须始终存在，即使字段值为空。
- 所有可追溯字段只能通过 `evidence_refs` 关联 `evidence_index`。
- 内部知识写入日志、adoption log、运行态审计信息不得进入该契约。

## 运行清单

`run_manifest.json` 需要显式记录模板脚本结果：

- `status`
- `failure_reason`
- `notes_locator`
- `notes_catalog_summary`
- `script_output_mode`
- `codex_review_required`

成功态默认要求：

- `script_output_mode=scaffold_only`
- `codex_review_required=true`

## 正式知识写入

正式知识写入不再通过 `pending_updates.json` 主导，而是通过：

- `runtime/knowledge/knowledge_base.json`
- `runtime/knowledge/adoption_logs/`

章节级复核、写入前后的结构化 delta，以及回滚约束的正式口径见 [knowledge_adoption_delta_contract.md](/Users/yetim/project/financialanalysis/knowledge_adoption_delta_contract.md)。

每次章节级知识写入至少需要：

- 写入来源 case / chapter
- before/after hash
- 结构化 delta
- 时间戳

缺少 adoption log 的知识写入视为非法实现。
