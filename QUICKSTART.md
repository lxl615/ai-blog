# 🚀 5分钟快速配置指南

## 第1步: 获取Anthropic API密钥 (1分钟)

1. 访问 https://console.anthropic.com/
2. 注册/登录账号
3. 进入 API Keys 页面
4. 点击 "Create Key" 创建新密钥
5. 复制密钥（格式：sk-ant-...）

**💡 提示**: 新用户通常有$5免费额度，足够运行数月

## 第2步: 配置邮箱授权码 (2分钟)

### 使用QQ邮箱（推荐国内用户）:

1. 登录 https://mail.qq.com/
2. 点击"设置" -> "账户"
3. 找到"POP3/IMAP/SMTP/Exchange/CardDAV/CalDAV服务"
4. 开启"IMAP/SMTP服务"
5. 生成授权码（会收到短信验证）
6. 保存授权码（16位字符）

**你需要的配置:**
- SENDER_EMAIL: your_email@qq.com
- SENDER_PASSWORD: 刚才生成的16位授权码
- SMTP_SERVER: smtp.qq.com
- SMTP_PORT: 587

### 使用Gmail（推荐国外用户）:

1. 访问 https://myaccount.google.com/security
2. 开启"两步验证"
3. 访问 https://myaccount.google.com/apppasswords
4. 选择"邮件"和"其他设备"
5. 生成应用专用密码
6. 保存密码（16位字符）

**你需要的配置:**
- SENDER_EMAIL: your_email@gmail.com
- SENDER_PASSWORD: 应用专用密码
- SMTP_SERVER: smtp.gmail.com
- SMTP_PORT: 587

## 第3步: 配置GitHub Secrets (2分钟)

1. Fork本项目到你的GitHub账号
2. 进入你fork的仓库
3. 点击 Settings -> Secrets and variables -> Actions
4. 点击 "New repository secret" 添加以下5个secrets:

```
ANTHROPIC_API_KEY = sk-ant-xxxxx（第1步获取的）
SENDER_EMAIL = your_email@qq.com（你的邮箱）
SENDER_PASSWORD = xxxxxxxxxxxxxxxx（第2步获取的授权码）
SMTP_SERVER = smtp.qq.com（QQ邮箱）或 smtp.gmail.com（Gmail）
SMTP_PORT = 587
```

## 第4步: 启用GitHub Actions (<1分钟)

1. 进入仓库的 Actions 标签
2. 点击 "I understand my workflows, go ahead and enable them"
3. 找到 "AI博客每日摘要" workflow
4. 点击 "Enable workflow"
5. 点击 "Run workflow" 测试运行

## 第5步: 检查邮箱！

几分钟后，检查 448795033@qq.com 是否收到测试邮件。

---

## ✅ 配置检查清单

- [ ] Anthropic API密钥已配置
- [ ] 邮箱授权码已生成
- [ ] 5个GitHub Secrets已添加
- [ ] GitHub Actions已启用
- [ ] 测试运行成功
- [ ] 收到测试邮件

## 🎯 运行时间

系统将在每天**北京时间早上8点**自动运行并发送邮件。

## 💰 费用说明

- GitHub Actions: 免费
- Anthropic API: 每月 < $0.5（每天5篇摘要）

## 🆘 遇到问题？

查看详细的 [README.md](README.md) 中的故障排查部分，或提交Issue。

---

**配置完成！享受每日AI资讯吧！** 🎉
