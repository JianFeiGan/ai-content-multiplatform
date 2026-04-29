# 一篇内容发7个平台？我用 Python + GPT 搞定了

> 你是不是也这样：写完一篇文章，微信要改格式、知乎要改风格、小红书要加 Emoji、CSDN 要调代码块……同一篇内容手动适配 7 个平台，3 小时起步。

## 😫 痛点

作为技术内容创作者，我一直在多平台同步发布内容。但每个平台的规则完全不同：

- **微信公众号**：标题 64 字以内，不支持标签，要悬念感
- **小红书**：标题 20 字以内，内容 1000 字封顶，必须加 Emoji 和 #标签
- **抖音**：内容 300 字以内，要口语化，适合 30 秒口播
- **知乎**：要专业深度，逻辑严密
- **CSDN**：要技术导向，带代码示例
- **掘金**：要实战踩坑记录
- **头条号**：要通俗冲击，大众科普

手动适配一遍，至少 3 个小时。而且每个平台的禁用词还不一样，小红书不能提"微信"，微信公众号里不能写"朋友圈"……

## ✨ 解决方案

于是我用 Python + OpenAI GPT 做了一个开源工具：**ai-content-multiplatform**

核心思路很简单：**写一篇 Markdown，AI 自动适配 7 个平台的风格和规则。**

```bash
# 安装
pip install ai-content-multiplatform

# 一条命令适配所有平台
ai-content-multiplatform adapt file article.md -p all
```

## 🎯 效果对比

以同一篇文章为例，看看 AI 是怎么根据不同平台"变身"的：

| 平台 | 适配后标题 | 风格变化 |
|------|-----------|---------|
| 微信公众号 | 🔥 程序员注意！这个AI工具正在... | 悬念感标题 + 短段落 |
| 知乎 | 大语言模型在多平台内容适配中的实践 | 专业深度 + 数据引用 |
| CSDN | Python实现AI内容多平台适配工具 | 技术导向 + 代码示例 |
| 抖音 | 你知道吗？3小时变3秒的秘密 | 口语化 + 30秒口播 |
| 小红书 | AI写作神器🔥一篇文变7篇！ | Emoji + 短句 + #标签 |
| 掘金 | 深入理解LLM内容适配引擎设计 | 技术深度 + 实战 |
| 头条号 | AI工具正在改变内容创作方式 | 通俗冲击 + 大众科普 |

**不是简单的截断和加标签，而是 GPT 根据每个平台的 style_prompt 重新改写。**

## 🏗️ 技术实现

### 整体架构

```
Markdown 输入 → ContentParser 解析 → ContentInput
                                      ↓
                            ContentAdapter.adapt()
                            (OpenAI API + 平台规则校验)
                                      ↓
                               AdaptedContent
                                      ↓
                          Formatter.save() → 7 份输出文件
```

### 核心设计

**1. Pydantic 模型驱动**

每个平台都有严格的 `PlatformRule` 模型，定义标题长度、内容上限、标签数量、封面尺寸、风格提示词和禁用词：

```python
class PlatformRule(BaseModel):
    name: str
    title_max_len: int
    content_max_len: int
    tag_limit: int
    cover_size: tuple[int, int]
    style_prompt: str
    forbidden_words: list[str]
```

**2. YAML 规则配置**

7 个平台的规则都在 `rules.yaml` 中配置，修改规则不需要改代码：

```yaml
platforms:
  xiaohongshu:
    name: "小红书"
    title_max_len: 20
    content_max_len: 1000
    tag_limit: 10
    style_prompt: |
      轻松活泼的社交媒体风格...
    forbidden_words: ["微信", "淘宝", "京东"]
```

**3. LLM 智能适配**

核心是利用 GPT 的 `style_prompt` 做风格迁移：

```python
async def adapt_with_llm(self, content: ContentInput, rule: PlatformRule) -> AdaptedContent:
    prompt = f"""
    将以下内容适配到{rule.name}平台。
    风格要求：{rule.style_prompt}
    标题上限：{rule.title_max_len}字
    内容上限：{rule.content_max_len}字
    禁用词：{rule.forbidden_words}
    
    原始内容：{content.content}
    """
    response = await self.llm_client.chat(prompt)
    return AdaptedContent(platform=rule.id, ...)
```

**4. 异步并发**

7 个平台的适配是并行的，速度很快：

```python
tasks = [adapter.adapt(content, rule) for rule in platform_rules.values()]
results = await asyncio.gather(*tasks)
```

## 📦 安装和使用

```bash
# 安装
uv tool install ai-content-multiplatform

# 配置 API Key
export OPENAI_API_KEY="sk-xxx"

# 适配到所有平台
ai-content-multiplatform adapt file article.md -p all

# 只适配特定平台
ai-content-multiplatform adapt file article.md -p weixin,xiaohongshu

# 预览效果（不保存）
ai-content-multiplatform preview content article.md weixin

# Dry Run 模式
ai-content-multiplatform adapt file article.md -p all --dry-run
```

## 💡 踩坑记录

1. **aiohttp ClientTimeout 陷阱**：aiohttp 3.10+ 内部使用 `asyncio.timeout()`，和 `loop.run_until_complete()` 不兼容，要用 `asyncio.wait_for()` 替代

2. **禁用词不是简单的字符串替换**：要考虑"微信公众号"包含"微信"这种情况，需要正则匹配

3. **不同平台的标签格式完全不同**：小红书用 `#标签`，知乎用逗号分隔，CSDN 用空格分隔

4. **LLM 输出不稳定**：用 `temperature=0.7` 平衡创造性和稳定性，`title_candidates=3` 提供备选标题

## 🔮 后续计划

- [ ] 更多平台支持（B站、YouTube、Medium）
- [ ] 图片自动适配（封面裁剪、水印）
- [ ] 定时发布功能
- [ ] Web UI 管理界面
- [ ] 本地模型支持（Ollama）

## 🔗 链接

- GitHub: https://github.com/JianFeiGan/ai-content-multiplatform
- PyPI: https://pypi.org/project/ai-content-multiplatform/

如果觉得有用，欢迎 Star ⭐ 支持一下！

---

*本文由作者原创，首发于掘金，转载请注明出处。*
