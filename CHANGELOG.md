# Changelog

所有重要更改将记录在此文件中。

格式基于 [Keep a Changelog](https://keepachangelog.com/)，版本遵循 [语义化版本](https://semver.org/)。

---

## [0.1.0] - 2026-04-26

### 🎉 正式发布

首次公开发布。

### ✨ 新增功能

- **7 平台内容适配**：支持微信公众号、知乎、CSDN、抖音、小红书、掘金、头条号的内容自动适配
- **AI 驱动的自适应转换**：基于 OpenAI API（GPT-4o-mini），根据各平台规则智能调整标题、正文风格、标签
- **CLI 命令行工具**：
  - `adapt` — 从 Markdown 文件或文本适配内容到多平台
  - `preview` — 预览指定平台的适配效果
  - `publish` — 发布内容到指定平台（支持草稿模式）
  - `config` — 查看当前配置
  - `init` — 初始化默认配置文件
- **平台规则配置系统**：YAML 格式的规则文件，定义各平台的标题长度、内容限制、封面尺寸、风格提示词、禁用词
- **发布历史记录**：基于 SQLite 的发布记录存储
- **批量处理**：一键将内容适配到所有支持的平台
- **Dry Run 模式**：仅显示适配计划，不实际调用 LLM

### 🏗️ 架构特性

- 异步并发处理（asyncio）
- Pydantic 数据模型验证
- 类型注解全覆盖
- 文档字符串全覆盖
- Rich 终端美化输出
- 灵活的配置系统（环境变量 + YAML + 默认值）

### ✅ 测试与质量

- 完整的测试覆盖（>80%）
- Ruff 代码规范检查
- MyPy 类型检查
- pytest-cov 覆盖率报告

### 📦 技术栈

| 组件 | 技术 |
|------|------|
| CLI 框架 | Typer |
| 数据验证 | Pydantic v2 |
| LLM 集成 | OpenAI SDK |
| HTTP 客户端 | httpx |
| 终端输出 | Rich |
| 配置管理 | pydantic-settings |
| 文档解析 | Markdown, BeautifulSoup4 |
| 规则配置 | PyYAML |
