# HEARTBEAT.md - 定时任务配置

## 每日 AI 科技日报（GitHub Actions）

### 任务 1: AI HOT 科技日报
- **来源**: AI Hot API (https://aihot.virxact.com/api/public/daily)
- **内容**: AI 领域每日热点新闻、技术动态、产品发布
- **时间**: 每天 08:30 (北京时间)
- **运行平台**: GitHub Actions
- **推送目标**: GitHub Pages (https://infish111.github.io/daily-ai-reports/)

### 配置说明

#### 1. GitHub Secrets 配置
需要在仓库设置中配置以下 Secrets:
- `AIHOT_API_URL`: `https://aihot.virxact.com/api/public/daily`

配置路径: https://github.com/InFish111/daily-ai-reports/settings/secrets/actions

#### 2. 手动触发
- 访问: https://github.com/InFish111/daily-ai-reports/actions
- 选择 "Daily AI Report" 工作流
- 点击 "Run workflow"

#### 3. 查看部署状态
- GitHub Pages 地址: https://infish111.github.io/daily-ai-reports/
- 构建状态: https://github.com/InFish111/daily-ai-reports/deployments

---

## 计划但未配置的任务

### 任务 2: 一级市场投融资日报  
- **主源**: 36氪搜索"融资"
- **时间**: 每天 08:30 (北京时间)
- **状态**: 待配置

### 任务 3: Twitter 热点追踪
- **来源**: Twitter/X News 板块
- **时间**: 每天 09:00 (北京时间)
- **状态**: 待配置

---

*最后更新: 2026-05-25*
