# W6 Regression Report

- 生成时间：2026-03-16T21:50:19+08:00
- 结果 JSON：`/Users/yetim/project/financialanalysis/financial-analyzer/test_runs/w6_regression_results.json`
- 汇总：3/3 通过

## 验证范围

- 固定 3 个案例重跑 `financial_analyzer.py`。
- 仅检查 `run_manifest.json`、`analysis_report.md`、`soul_export_payload.json`、`financial_output.xlsx` 的生成结果和结构约束。
- 不把历史 `test_runs` 目录作为通过依据。

## 案例结果

### 恒隆地产 (`henglong`) - PASS

- run dir: `/Users/yetim/project/financialanalysis/financial-analyzer/test_runs/w6_henglong`
- markdown: `/Users/yetim/project/financialanalysis/output/恒隆地产/恒隆地产2024年報/恒隆地产2024年報.md`
- notes_workfile: `/Users/yetim/project/financialanalysis/financial-analyzer/testdata/henglong_notes_workfile.json`
- returncode: `0`

- `run_manifest`: PASS
- `analysis_report`: PASS
- `soul_export_payload`: PASS
- `financial_output`: PASS

```text
[INFO] 输入文件: /Users/yetim/project/financialanalysis/output/恒隆地产/恒隆地产2024年報/恒隆地产2024年報.md
[INFO] 运行目录: /Users/yetim/project/financialanalysis/financial-analyzer/test_runs/w6_henglong
[OK] 章节记录: 4
[OK] 动态重点: 6
[OK] 待固化更新: 9
✅ 成功: 产物已生成 -> /Users/yetim/project/financialanalysis/financial-analyzer/test_runs/w6_henglong
```

### 碧桂园 (`country_garden`) - PASS

- run dir: `/Users/yetim/project/financialanalysis/financial-analyzer/test_runs/w6_country_garden`
- markdown: `/Users/yetim/project/financialanalysis/cases/碧桂园2024年年报分析.md`
- notes_workfile: `/Users/yetim/project/financialanalysis/financial-analyzer/testdata/country_garden_notes_workfile.json`
- returncode: `0`

- `run_manifest`: PASS
- `analysis_report`: PASS
- `soul_export_payload`: PASS
- `financial_output`: PASS

```text
[INFO] 输入文件: /Users/yetim/project/financialanalysis/cases/碧桂园2024年年报分析.md
[INFO] 运行目录: /Users/yetim/project/financialanalysis/financial-analyzer/test_runs/w6_country_garden
[OK] 章节记录: 31
[OK] 动态重点: 6
[OK] 待固化更新: 12
✅ 成功: 产物已生成 -> /Users/yetim/project/financialanalysis/financial-analyzer/test_runs/w6_country_garden
```

### 杭海新城控股 (`hanghai`) - PASS

- run dir: `/Users/yetim/project/financialanalysis/financial-analyzer/test_runs/w6_hanghai`
- markdown: `/Users/yetim/project/financialanalysis/cases/杭海新城控股2024年年报分析.md`
- notes_workfile: `/Users/yetim/project/financialanalysis/financial-analyzer/testdata/hanghai_notes_workfile.json`
- returncode: `0`

- `run_manifest`: PASS
- `analysis_report`: PASS
- `soul_export_payload`: PASS
- `financial_output`: PASS

```text
[INFO] 输入文件: /Users/yetim/project/financialanalysis/cases/杭海新城控股2024年年报分析.md
[INFO] 运行目录: /Users/yetim/project/financialanalysis/financial-analyzer/test_runs/w6_hanghai
[OK] 章节记录: 7
[OK] 动态重点: 6
[OK] 待固化更新: 12
✅ 成功: 产物已生成 -> /Users/yetim/project/financialanalysis/financial-analyzer/test_runs/w6_hanghai
```

## 已知缺口

### 历史 run_manifest 仍保留 Windows 绝对路径

- 分类：`observed_repo_state`
- 说明：历史 test_runs 样本不能直接作为当前 W6 基线，因为 artifacts 仍指向旧环境路径。
- 证据：
  - `{"case_id": "henglong_notes_only", "path": "C:\\Users\\Administrator\\Desktop\\项目\\信用工作流\\年报训练\\financial-analyzer\\test_runs\\henglong_notes_only\\run_manifest.json"}`
  - `{"case_id": "henglong_v3", "path": "C:\\Users\\Administrator\\Desktop\\项目\\信用工作流\\年报训练\\financial-analyzer\\test_runs\\henglong_v3\\run_manifest.json"}`

### henglong_v3 缺少正式 status 字段

- 分类：`observed_repo_state`
- 说明：该目录可作为历史排障样本，但不能继续充当成功态回归基线。
- 证据：
  - `{"case_id": "henglong_v3", "manifest_path": "/Users/yetim/project/financialanalysis/financial-analyzer/test_runs/henglong_v3/run_manifest.json"}`

### 历史目录同时存在旧内部 workbook 与新 Soul workbook

- 分类：`observed_repo_state`
- 说明：W6 v1 只认当前脚本重跑后的 financial_output.xlsx，不直接以历史目录判定通过。
- 证据：
  - `{"path": "/Users/yetim/project/financialanalysis/financial-analyzer/test_runs/henglong_soul_contract/financial_output.xlsx", "sheetnames": ["summary", "focus", "chapters", "topic_results", "pending_updates"]}`
  - `{"path": "/Users/yetim/project/financialanalysis/financial-analyzer/test_runs/henglong_soul_v1_1_alpha/soul_output.xlsx", "sheetnames": ["00_overview", "01_kpi_dashboard", "02_financial_summary", "03_debt_profile", "04_liquidity_and_covenants", "05_bond_detail", "08_topic_investment_property", "99_evidence_index"]}`

### 失败路径样本已存在，但未纳入本轮 happy-path 基线

- 分类：`known_scope_boundary`
- 说明：missing_notes_workfile 可作为 W6.1 的失败态回归输入，本轮最小回归仅覆盖 3 个成功案例。
- 证据：
  - `{"path": "/Users/yetim/project/financialanalysis/financial-analyzer/test_runs/missing_notes_workfile/run_manifest.json", "failure_reason": "notes_workfile_missing"}`

### 当前最小回归不覆盖 workbook 视觉预览质量

- 分类：`known_scope_boundary`
- 说明：本轮只验证文件生成和结构约束，不判断预览 PDF/PNG、版式和视觉一致性。

### 当前最小回归不覆盖 JSON/单元格内容级 golden diff

- 分类：`known_scope_boundary`
- 说明：W6 v1 定义为 smoke regression，不冻结 payload 内容或 Excel 单元格值。
