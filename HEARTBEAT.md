# HEARTBEAT.md - 定时任务配置

## 每日 AI 科技日报推送（方案1）

### 任务: 飞书定时推送日报链接
- **时间**: 每天 08:35（北京时间）
- **延迟原因**: GitHub Actions 每天 08:30 生成日报，留出5分钟生成时间
- **推送方式**: 当前飞书对话
- **内容**: 检查 GitHub Pages 最新日报并发送链接

### 📋 任务详情

**执行内容**:
1. 检查 https://infish111.github.io/daily-ai-reports/ 是否有今日日报
2. 如果已生成，发送飞书消息：
   ```
   📰 AI 科技日报已生成
   📅 YYYY-MM-DD
   📊 AI Hot + 36氪 + TechCrunch
   🔗 [点击查看](https://infish111.github.io/daily-ai-reports/YYYY-MM-DD.html)
   ```
3. 如果未生成，发送提醒：
   ```
   ⏳ 日报生成中，请稍后查看
   🔗 [存档页面](https://infish111.github.io/daily-ai-reports/)
   ```

### 🌐 数据源

| 数据源 | 类型 | 内容 |
|--------|------|------|
| **AI Hot API** | API | AI 热点新闻、技术动态 |
| **36氪** | RSS | 投融资、创业资讯 |
| **TechCrunch** | RSS | 国际科技新闻 |

### 📊 访问地址

- **今日日报**: https://infish111.github.io/daily-ai-reports/2026-05-25.html
- **存档首页**: https://infish111.github.io/daily-ai-reports/

### ⚙️ 配置说明

#### GitHub Secrets 配置 ✅
配置路径: https://github.com/InFish111/daily-ai-reports/settings/secrets/actions

已配置:
- `AIHOT_API_URL`: `https://aihot.virxact.com/api/public/daily`
- `GITHUB_TOKEN`: 自动提供

#### 手动触发测试
- 访问: https://github.com/InFish111/daily-ai-reports/actions
- 选择 "Daily AI Report" 工作流
- 点击 "Run workflow"

---

## 📅 更新日志

### 2026-05-25
- ✅ 初始配置完成
- ✅ 多数据源聚合（AI Hot + 36氪 + TechCrunch）
- ✅ GitHub Actions 自动部署
- ✅ 飞书定时推送配置（方案1）

---

*配置完成: 每天 08:35 自动推送日报链接到当前对话*
