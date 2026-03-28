# Contributing

感谢你参与这个仓库的开发。这里的协作方式尽量保持开源项目常见做法：先读文档，再动手；先小改动，再扩展；先保留边界，再谈重构。

## 开始前

1. 先读 [README.md](README.md) 和 [docs/README.md](docs/README.md)。
2. 再读 [docs/quickstart.md](docs/quickstart.md) 与 [docs/architecture.md](docs/architecture.md)。
3. 需要改数据契约时，再看 [docs/contracts.md](docs/contracts.md)。

## 提交原则

- 一次只做一类改动。
- 文档、样例和实现尽量分开提交。
- 路径、字段名和产物名不要随手改。
- 如果改动会影响运行结果，先补说明，再补实现。

## 推荐工作流

1. 建一个分支或本地工作区。
2. 做最小范围修改。
3. 先验证文档链接和示例路径。
4. 再检查脚本和产物是否一致。

## 文档风格

- 标题清晰。
- 先结论后展开。
- 尽量用真实路径和真实产物名。
- 不把草稿写成最终结论。

## 代码风格

- Python 代码保持小函数、直接逻辑。
- 中文路径、日志和 Markdown/JSON 读写统一使用 UTF-8。
- 不要把运行态数据写回 skill 目录。

## 提交信息

建议使用简短祈使句，并带上前缀，例如 `docs:`、`fix:`、`feat:`。