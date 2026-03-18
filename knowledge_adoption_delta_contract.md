# Knowledge Adoption Delta Contract

## 1. 文档定位

这份文档定义每次章节级知识写入正式 `knowledge_base.json` 时，Codex 必须构造的结构化 delta。

它解决的是“如何把复核结果稳定、可回滚、可审计地写入正式知识库”，不是知识内容本身。

## 2. 设计目标

1. 单次写入必须可审计。
2. 单次写入必须可回滚。
3. 单次写入必须能被 `show_knowledge_adoption.py` 摘要。
4. 单次写入不能依赖隐式聊天上下文。
5. 单次写入不能绕过章节复核。

## 3. 推荐契约

```json
{
  "delta_version": "knowledge_adoption_delta_v1",
  "source": {
    "case_name": "恒隆地产",
    "chapter_no": "10",
    "chapter_title": "借款和融资成本",
    "run_dir": "/abs/path/to/run_dir",
    "chapter_record_path": "/abs/path/to/run_dir/chapter_records.jsonl",
    "scaffold_artifacts": {
      "analysis_report_scaffold": "/abs/path/to/run_dir/analysis_report_scaffold.md",
      "final_data_scaffold": "/abs/path/to/run_dir/final_data_scaffold.json",
      "soul_export_payload_scaffold": "/abs/path/to/run_dir/soul_export_payload_scaffold.json"
    }
  },
  "review": {
    "review_state": "reviewed",
    "reviewer": "Codex",
    "reviewed_at": "2026-03-18T12:00:00+08:00",
    "summary": "将章节结论正式采纳为知识条目",
    "risk_level": "low",
    "confidence": "high"
  },
  "operations": [
    {
      "op": "upsert_by_key",
      "path": "knowledge.indicators.solvency.long_term",
      "match_key": "title",
      "match_value": "长期借款结构",
      "value": {
        "title": "长期借款结构",
        "description": "新增章节复核结论"
      }
    }
  ],
  "evidence_refs": [
    {
      "type": "chapter_record",
      "path": "/abs/path/to/run_dir/chapter_records.jsonl",
      "chapter_no": "10"
    }
  ],
  "before_hash": "md5:....",
  "after_hash": "md5:....",
  "knowledge_base_version_before": "v1.0.0",
  "knowledge_base_version_after": "v1.0.1",
  "rollback": {
    "enabled": true,
    "backup_path": "/abs/path/to/adoption_logs/20260318_case_chapter_10.before.json",
    "rollback_log_path": "/abs/path/to/adoption_logs/20260318_case_chapter_10.rollback.json"
  }
}
```

## 4. 字段要求

### 4.1 `source`

- `case_name` 必填。
- `chapter_no` 必填。
- `chapter_title` 必填。
- `run_dir` 必填。
- `chapter_record_path` 必填。
- `scaffold_artifacts` 至少应包含 `analysis_report_scaffold`、`final_data_scaffold`、`soul_export_payload_scaffold`。

### 4.2 `review`

- `review_state` 建议取值：
  - `proposed`
  - `reviewed`
  - `adopted`
  - `rejected`
- `reviewer` 建议固定记录 `Codex` 或具体线程标识。
- `reviewed_at` 必须是 ISO 时间。
- `summary` 要能解释为什么接受或拒绝。
- `risk_level` 至少区分 `low`、`medium`、`high`。

### 4.3 `operations`

允许的操作类型只保留三类：

- `set`
- `append`
- `upsert_by_key`

要求：

- 每个 operation 必须显式写出 `path`。
- `upsert_by_key` 必须写出 `match_key` 和 `match_value`。
- `value` 必须是能被 `write_knowledge_adoption.py` 稳定应用的对象。

### 4.4 `evidence_refs`

至少要能回指到：

- `chapter_records.jsonl`
- 复核用 scaffold 文件
- 必要时的正文/附注定位证据

### 4.5 回滚

- 每次写入必须先保留 `before` 快照。
- 每次写入必须生成 `adoption log`。
- 任何回滚都必须保留自己的 rollback log。

## 5. 验证规则

1. `operations` 不能为空。
2. `source.case_name`、`source.chapter_no`、`source.chapter_title` 不能为空。
3. `review.review_state` 不能为空。
4. `before_hash` 与 `after_hash` 不能相同，除非本次写入是纯审计事件。
5. 没有 `adoption log` 的写入视为非法实现。
6. 不能把内部治理元数据写回 `knowledge_base` 中的正式业务字段。

## 6. 与现有脚本的关系

- `financial-analyzer/scripts/write_knowledge_adoption.py` 应接受符合本契约的 delta。
- `financial-analyzer/scripts/rollback_knowledge_adoption.py` 应能根据 log 与 backup 还原。
- `financial-analyzer/scripts/show_knowledge_adoption.py` 应能汇总 source / review / hash / result。

## 7. 建议的新线程 Prompt

```text
先阅读 AGENTS.md、automation_blueprint.md、production_execution_runbook.md、codex_review_and_finalization_runbook.md、knowledge_adoption_delta_contract.md，以及 financial-analyzer/scripts/write_knowledge_adoption.py。当前聚焦 R2：Knowledge Adoption Delta Contract 的落地实现。请把这份 delta 契约落实到脚本和文档中，使章节级知识写入具备明确的 source、review、operations、evidence_refs、hash、rollback 字段，并能被 rollback / summary 工具识别。不要把知识写入重新做成 pending_updates 或 review bundle 旧路径。
```
