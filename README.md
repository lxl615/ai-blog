# 🤖 AI博客每日摘要系统

每天自动抓取AI大牛的博客，使用Claude AI总结关键内容，并发送到你的邮箱。

## ✨ 功能特点

- 📚 自动抓取知名AI研究者和机构的博客（Andrej Karpathy、Yann LeCun、OpenAI等）
- 🧠 使用Claude AI智能总结，每篇100-200字中文摘要
- 📧 每天早上8点自动发送精美HTML格式邮件
- ⚙️ 完全自动化，无需人工干预
- 🆓 使用GitHub Actions免费运行

## 📋 订阅的博客源

当前配置包括以下博客：

- **Andrej Karpathy** - 前Tesla AI总监，著名AI研究者
- **Yann LeCun** - Meta首席AI科学家，深度学习之父
- **OpenAI Blog** - OpenAI官方博客
- **Anthropic** - Anthropic公司博客
- **Google AI Blog** - Google AI研究博客
- **DeepMind Blog** - DeepMind官方博客
- **Distill.pub** - 机器学习可视化讲解

## 🚀 快速开始

### 方案A: 使用GitHub Actions（推荐，完全免费）

#### 1. Fork本项目到你的GitHub账号

点击右上角的"Fork"按钮

#### 2. 配置Secrets

在你的GitHub仓库中，进入 `Settings` -> `Secrets and variables` -> `Actions`，添加以下secrets：

| Secret名称 | 说明 | 获取方式 |
|-----------|------|---------|
| `ANTHROPIC_API_KEY` | Anthropic API密钥 | [获取链接](https://console.anthropic.com/) |
| `SENDER_EMAIL` | 发件邮箱 | 你的邮箱地址 |
| `SENDER_PASSWORD` | 邮箱密码/授权码 | 见下方说明 |
| `SMTP_SERVER` | SMTP服务器 | 见下方说明 |
| `SMTP_PORT` | SMTP端口 | 通常是587 |

#### 3. 邮箱配置说明

**使用Gmail:**
- `SENDER_EMAIL`: your_email@gmail.com
- `SENDER_PASSWORD`: [生成应用专用密码](https://myaccount.google.com/apppasswords)
- `SMTP_SERVER`: smtp.gmail.com
- `SMTP_PORT`: 587

**使用QQ邮箱:**
- `SENDER_EMAIL`: your_email@qq.com
- `SENDER_PASSWORD`: 在QQ邮箱设置中生成授权码
- `SMTP_SERVER`: smtp.qq.com
- `SMTP_PORT`: 587

**使用163邮箱:**
- `SENDER_EMAIL`: your_email@163.com
- `SENDER_PASSWORD`: 在163邮箱设置中生成授权码
- `SMTP_SERVER`: smtp.163.com
- `SMTP_PORT`: 587

#### 4. 启用GitHub Actions

1. 进入仓库的 `Actions` 标签
2. 点击 "I understand my workflows, go ahead and enable them"
3. 点击 "AI博客每日摘要" workflow
4. 点击 "Enable workflow"

#### 5. 测试运行

点击 "Run workflow" -> "Run workflow" 手动触发一次测试

### 方案B: 本地运行或服务器部署

#### 1. 克隆项目

```bash
git clone https://github.com/yourusername/ai-blog-digest.git
cd ai-blog-digest
```

#### 2. 安装依赖

```bash
pip install -r requirements.txt
```

#### 3. 配置环境变量

复制 `.env.example` 为 `.env`，并填入你的配置：

```bash
cp .env.example .env
# 编辑 .env 文件，填入你的API密钥和邮箱配置
```

#### 4. 运行

```bash
python main.py
```

#### 5. 设置定时任务（可选）

**Linux/Mac (使用crontab):**

```bash
crontab -e
```

添加以下行（每天早上8点运行）：

```cron
0 8 * * * cd /path/to/ai-blog-digest && /usr/bin/python3 main.py
```

**Windows (使用任务计划程序):**

1. 打开"任务计划程序"
2. 创建基本任务
3. 设置触发器为每天8:00
4. 操作选择"启动程序"，选择Python和main.py

## 📧 收到的邮件示例

邮件包含：
- 📅 日期和文章数量
- 📝 每篇文章的标题、来源、发布时间
- 💡 100-200字的中文AI摘要
- 🔗 原文链接

## ⚙️ 自定义配置

### 修改博客源

编辑 `main.py` 中的 `BLOGS` 字典，添加或删除博客RSS源：

```python
BLOGS = {
    "博客名称": "RSS订阅地址",
    # 添加更多...
}
```

### 修改推送时间

编辑 `.github/workflows/daily-digest.yml` 中的cron表达式：

```yaml
schedule:
  - cron: '0 0 * * *'  # UTC时间0点 = 北京时间8点
```

### 修改摘要长度

编辑 `main.py` 中 `summarize_with_claude()` 函数的prompt：

```python
prompt = f"""请用中文总结以下AI博客文章，要求：
1. 修改这里的字数要求
2. 突出核心观点和关键技术
...
```

### 修改收件人

编辑 `main.py` 中的 `recipient` 变量：

```python
recipient = "your_new_email@example.com"
```

## 💰 成本估算

- **GitHub Actions**: 完全免费（公开仓库）
- **Anthropic API**: 
  - Claude Sonnet: 约$3/百万tokens输入，$15/百万tokens输出
  - 每天5篇文章总结约消耗1000 tokens
  - **估算月成本**: < $0.5

## 🔧 故障排查

### 问题1: 邮件发送失败

**解决方案:**
- 确认邮箱密码是"应用专用密码"或"授权码"，不是邮箱登录密码
- 检查SMTP服务器和端口配置是否正确
- 确认邮箱已开启SMTP服务

### 问题2: 抓取不到文章

**解决方案:**
- 某些博客可能暂时没有更新
- RSS源可能已失效，需要更新
- 检查网络连接

### 问题3: AI总结失败

**解决方案:**
- 确认ANTHROPIC_API_KEY是否正确
- 检查API额度是否充足
- 查看GitHub Actions日志获取详细错误信息

## 📝 日志查看

### GitHub Actions日志:

1. 进入仓库的 `Actions` 标签
2. 点击对应的workflow运行记录
3. 查看详细日志

### 本地运行日志:

直接查看终端输出

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 🙏 致谢

感谢以下项目和服务：
- [Anthropic Claude API](https://www.anthropic.com/)
- [GitHub Actions](https://github.com/features/actions)
- 所有提供RSS订阅的博客作者

---

**如有问题，请提交Issue或联系维护者**

祝你阅读愉快！📚
