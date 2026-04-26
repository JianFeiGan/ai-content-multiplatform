# 贡献指南 (Contributing Guide)

感谢你对 `ai-content-multiplatform` 的兴趣！我们欢迎各种形式的贡献，特别是添加新的平台适配器。

## 🚀 快速开始

1. **Fork** 本仓库。
2. 创建你的特性分支：`git checkout -b feature/my-new-feature`。
3. 提交你的改动：`git commit -m 'feat: Add some feature'`。
4. 推送到分支：`git push origin feature/my-new-feature`。
5. 提交 **Pull Request**。

## 🛠 开发环境设置

```bash
# 安装 uv 包管理器 (如果尚未安装)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 克隆并进入项目
git clone git@github.com:your-username/ai-content-multiplatform.git
cd ai-content-multiplatform

# 安装开发依赖
uv sync --group dev
```

## 📝 如何添加新平台适配器？

这是最常见的贡献方式。

### 1. 定义规则

在 `src/ai_content_multiplatform/config/rules.yaml` 中添加新平台的规则：

```yaml
new_platform:
  name: 新平台
  title_max_len: 30
  content_max_len: 1000
  tag_limit: 5
  forbidden_words: ["敏感词"]
  style_prompt: "幽默风趣，适合年轻人..."
```

### 2. 添加测试

在 `tests/` 目录下添加对应测试用例，确保规则生效。

### 3. 提交 PR

请确保所有测试通过：`uv run pytest`。

## 📜 代码规范

- 使用 `ruff` 进行代码检查和格式化。
- 所有的函数必须有类型注解 (Type Hints)。
- Commit message 请遵循 [Conventional Commits](https://www.conventionalcommits.org/) 规范。

## ✨ 致谢

感谢每一位提交 Issue、PR 和建议的开发者！
