# HEARTBEAT.md - 定时任务配置

## 每日 AI 科技日报（GitHub Actions）✅ 已启用

### 任务: AI 科技日报 - 多源聚合
- **触发时间**: 每天 08:30 (北京时间)
- **运行平台**: GitHub Actions
- **推送目标**: GitHub Pages + 飞书通知

### 📊 数据源

| 数据源 | 类型 | 内容 |
|--------|------|------|
| **AI Hot API** | API | AI 领域每日热点新闻、技术动态、产品发布 |
| **36氪** | RSS | 投融资、创业、行业动态 |
| **TechCrunch** | RSS | 国际科技新闻、硅谷动态 |

### 🌐 访问地址

- **存档首页**: https://infish111.github.io/daily-ai-reports/
- **今日日报**: https://infish111.github.io/daily-ai-reports/2026-05-25.html

### ⚙️ 配置说明

#### 1. GitHub Secrets 配置 ✅

配置路径: https://github.com/InFish111/daily-ai-reports/settings/secrets/actions

已配置:
- `AIHOT_API_URL`: `https://aihot.virxact.com/api/public/daily`
- `GITHUB_TOKEN`: 自动提供（用于部署）

待配置（可选）:
- `FEISHU_WEBHOOK`: 飞书机器人 webhook 地址（用于推送通知）

#### 2. 飞书机器人配置步骤

1. 在飞书群聊中点击 **设置** → **群机器人** → **添加机器人**
2. 选择 **自定义机器人**
3. 设置机器人名称（如 "AI日报"）和头像
4. 复制生成的 **Webhook 地址**
5. 在 GitHub Secrets 中添加 `FEISHU_WEBHOOK`

#### 3. 手动触发

- 访问: https://github.com/InFish111/daily-ai-reports/actions
- 选择 "Daily AI Report" 工作流
- 点击 "Run workflow"

#### 4. 查看运行状态

- GitHub Actions 日志: https://github.com/InFish111/daily-ai-reports/actions
- GitHub Pages 部署: https://github.com/InFish111/daily-ai-reports/deployments

---

## 📋 功能特性

### 已实现 ✅
- [x] 多数据源聚合（AI Hot + 36氪 + TechCrunch）
- [x] 自动定时生成（每天 08:30）
- [x] GitHub Pages 自动部署
- [x] 响应式 HTML 页面
- [x] 新闻分类和颜色标签
- [x] 数据来源标注

### 计划中 📝
- [ ] Twitter/X 热点追踪
- [ ] 飞书推送通知（待配置 webhook）
- [ ] 邮件订阅
- [ ] 周报/月报汇总

---

## 📅 更新日志

### 2026-05-25
- ✅ 初始配置完成
- ✅ 支持 AI Hot API 数据源
- ✅ GitHub Actions 自动部署
- ✅ 添加 36氪、TechCrunch 数据源
- ✅ 准备飞书推送功能

---

*最后更新: 2026-05-25*
