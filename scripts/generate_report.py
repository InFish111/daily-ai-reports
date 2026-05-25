#!/usr/bin/env python3
"""
Daily AI Report Generator - Tech Style with Color Categories and Animations
"""

import os
import json
import requests
from datetime import datetime, timedelta
from jinja2 import Template
import shutil
import xml.etree.ElementTree as ET

def fetch_aihot_news():
    """Fetch news from AI HOT API"""
    api_url = os.environ.get('AIHOT_API_URL', 'https://aihot.virxact.com/api/public/daily')
    
    try:
        print(f"Fetching from AI Hot API: {api_url}")
        response = requests.get(api_url, timeout=30)
        response.raise_for_status()
        data = response.json()
        news_items = data.get('news', [])
        print(f"✅ Got {len(news_items)} news items from AI Hot")
        return news_items
    except Exception as e:
        print(f"⚠️ Error fetching from AIHOT API: {e}")
        return []

def get_category_style(category):
    """Get gradient and glow colors for category"""
    styles = {
        '产品发布': {
            'gradient': 'linear-gradient(135deg, #00f5ff 0%, #0080ff 100%)',
            'glow': 'rgba(0, 245, 255, 0.3)',
            'border': '#00f5ff',
            'icon': '🚀'
        },
        '产品更新': {
            'gradient': 'linear-gradient(135deg, #a855f7 0%, #6366f1 100%)',
            'glow': 'rgba(168, 85, 247, 0.3)',
            'border': '#a855f7',
            'icon': '⚡'
        },
        '行业动态': {
            'gradient': 'linear-gradient(135deg, #f59e0b 0%, #ef4444 100%)',
            'glow': 'rgba(245, 158, 11, 0.3)',
            'border': '#f59e0b',
            'icon': '🔥'
        },
        '行业洞察': {
            'gradient': 'linear-gradient(135deg, #10b981 0%, #06b6d4 100%)',
            'glow': 'rgba(16, 185, 129, 0.3)',
            'border': '#10b981',
            'icon': '💡'
        },
        '职场趋势': {
            'gradient': 'linear-gradient(135deg, #ec4899 0%, #8b5cf6 100%)',
            'glow': 'rgba(236, 72, 153, 0.3)',
            'border': '#ec4899',
            'icon': '📈'
        },
        '并购动态': {
            'gradient': 'linear-gradient(135deg, #22d3ee 0%, #3b82f6 100%)',
            'glow': 'rgba(34, 211, 238, 0.3)',
            'border': '#22d3ee',
            'icon': '🤝'
        },
        '论文研究': {
            'gradient': 'linear-gradient(135deg, #84cc16 0%, #14b8a6 100%)',
            'glow': 'rgba(132, 204, 22, 0.3)',
            'border': '#84cc16',
            'icon': '🔬'
        },
        '工具推荐': {
            'gradient': 'linear-gradient(135deg, #f97316 0%, #eab308 100%)',
            'glow': 'rgba(249, 115, 22, 0.3)',
            'border': '#f97316',
            'icon': '🛠️'
        },
        '投融资': {
            'gradient': 'linear-gradient(135deg, #8b5cf6 0%, #d946ef 100%)',
            'glow': 'rgba(139, 92, 246, 0.3)',
            'border': '#8b5cf6',
            'icon': '💰'
        },
        '国际动态': {
            'gradient': 'linear-gradient(135deg, #06b6d4 0%, #3b82f6 100%)',
            'glow': 'rgba(6, 182, 212, 0.3)',
            'border': '#06b6d4',
            'icon': '🌍'
        },
    }
    return styles.get(category, {
        'gradient': 'linear-gradient(135deg, #64748b 0%, #94a3b8 100%)',
        'glow': 'rgba(100, 116, 139, 0.3)',
        'border': '#64748b',
        'icon': '📰'
    })

def get_weekday_cn(date_str):
    """Get Chinese weekday name"""
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
        return weekdays[date.weekday()]
    except:
        return ""

def generate_html(news_items, date_str):
    """Generate tech-style HTML with color categories and animations"""
    
    # Create inline styles for each card
    cards_html = ""
    for i, item in enumerate(news_items[:12]):
        style = get_category_style(item.get('category', '动态'))
        featured_class = "featured" if i == 0 else ""
        
        cards_html += f'''
        <article class="card {featured_class}" style="--card-border: {style['border']}; --card-glow: {style['glow']};">
            <span class="category-badge" style="background: {style['gradient']}; box-shadow: 0 4px 15px {style['glow']};">
                {style['icon']} {item.get('category', '动态')}
            </span>
            <h2>{item.get('title', '')}</h2>
            <p>{item.get('content', '')[:250]}{'...' if len(item.get('content', '')) > 250 else ''}</p>
            <div class="source-tag" style="--source-color: {style['border']}">{item.get('source', '')}</div>
        </article>
        '''
    
    sources = set(item.get('source', 'Unknown') for item in news_items)
    now = datetime.now()
    
    html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 科技日报 - {date_str}</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Noto+Sans+SC:wght@300;400;500;700;900&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-primary: #050508;
            --bg-card: rgba(20, 20, 30, 0.6);
            --text-primary: #ffffff;
            --text-secondary: #a0a0b0;
            --text-muted: #606070;
        }}

        * {{ margin: 0; padding: 0; box-sizing: border-box; }}

        body {{
            font-family: 'Inter', 'Noto Sans SC', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            min-height: 100vh;
            overflow-x: hidden;
        }}

        /* Animated background grid */
        .bg-grid {{
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background-image: 
                linear-gradient(rgba(0, 245, 255, 0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(0, 245, 255, 0.03) 1px, transparent 1px);
            background-size: 50px 50px;
            animation: gridMove 20s linear infinite;
            pointer-events: none;
            z-index: 0;
        }}

        @keyframes gridMove {{
            0% {{ transform: translate(0, 0); }}
            100% {{ transform: translate(50px, 50px); }}
        }}

        /* Floating particles */
        .particles {{
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            overflow: hidden;
            pointer-events: none;
            z-index: 1;
        }}

        .particle {{
            position: absolute;
            width: 4px; height: 4px;
            background: rgba(0, 245, 255, 0.5);
            border-radius: 50%;
            animation: float 15s infinite;
            box-shadow: 0 0 10px rgba(0, 245, 255, 0.5);
        }}

        @keyframes float {{
            0%, 100% {{ transform: translateY(100vh) rotate(0deg); opacity: 0; }}
            10% {{ opacity: 1; }}
            90% {{ opacity: 1; }}
            100% {{ transform: translateY(-100vh) rotate(720deg); opacity: 0; }}
        }}

        .container {{
            position: relative;
            z-index: 10;
            max-width: 1400px;
            margin: 0 auto;
            padding: 40px 24px;
        }}

        /* Header with glowing effect */
        header {{
            text-align: center;
            padding: 60px 0 40px;
            position: relative;
        }}

        .logo {{
            display: inline-flex;
            align-items: center;
            gap: 16px;
            margin-bottom: 24px;
        }}

        .logo-icon {{
            width: 60px; height: 60px;
            background: linear-gradient(135deg, #00f5ff 0%, #0080ff 100%);
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 28px;
            animation: pulse 2s ease-in-out infinite;
            box-shadow: 0 0 30px rgba(0, 245, 255, 0.4);
        }}

        @keyframes pulse {{
            0%, 100% {{ transform: scale(1); box-shadow: 0 0 30px rgba(0, 245, 255, 0.4); }}
            50% {{ transform: scale(1.05); box-shadow: 0 0 50px rgba(0, 245, 255, 0.6); }}
        }}

        .masthead {{
            font-size: 3.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #ffffff 0%, #00f5ff 50%, #0080ff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            letter-spacing: -0.02em;
        }}

        .tagline {{
            font-size: 1rem;
            color: var(--text-secondary);
            letter-spacing: 0.4em;
            text-transform: uppercase;
            margin-top: 8px;
        }}

        /* Date badge */
        .date-badge {{
            display: inline-flex;
            align-items: center;
            gap: 12px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 12px 24px;
            border-radius: 50px;
            margin-top: 24px;
            backdrop-filter: blur(10px);
        }}

        .date-badge span {{
            color: var(--text-secondary);
            font-size: 0.9rem;
        }}

        .date-badge .divider {{
            width: 4px; height: 4px;
            background: var(--text-muted);
            border-radius: 50%;
        }}

        /* Stats bar */
        .stats-bar {{
            display: flex;
            justify-content: center;
            gap: 48px;
            margin: 40px 0;
            flex-wrap: wrap;
        }}

        .stat {{
            text-align: center;
            padding: 20px 32px;
            background: var(--bg-card);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 16px;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
        }}

        .stat:hover {{
            transform: translateY(-5px);
            border-color: rgba(0, 245, 255, 0.3);
            box-shadow: 0 10px 40px rgba(0, 245, 255, 0.1);
        }}

        .stat-value {{
            font-size: 2.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #00f5ff 0%, #0080ff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }}

        .stat-label {{
            font-size: 0.85rem;
            color: var(--text-secondary);
            margin-top: 4px;
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }}

        /* News grid */
        .news-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(380px, 1fr));
            gap: 24px;
            margin-top: 40px;
        }}

        @media (max-width: 768px) {{
            .news-grid {{ grid-template-columns: 1fr; }}
        }}

        /* News cards with category colors */
        .card {{
            background: var(--bg-card);
            border: 1px solid rgba(255, 255, 255, 0.08);
            border-radius: 20px;
            padding: 28px;
            position: relative;
            overflow: hidden;
            backdrop-filter: blur(10px);
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        .card::before {{
            content: '';
            position: absolute;
            top: 0; left: 0; right: 0;
            height: 3px;
            background: var(--card-border);
            opacity: 0.8;
        }}

        .card:hover {{
            transform: translateY(-8px) scale(1.02);
            border-color: var(--card-border);
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4), 0 0 40px var(--card-glow);
        }}

        .category-badge {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            padding: 6px 14px;
            border-radius: 20px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 16px;
            color: white;
        }}

        .card h2 {{
            font-size: 1.25rem;
            font-weight: 700;
            line-height: 1.4;
            margin-bottom: 12px;
            color: var(--text-primary);
        }}

        .card p {{
            color: var(--text-secondary);
            font-size: 0.95rem;
            line-height: 1.7;
        }}

        .source-tag {{
            display: inline-flex;
            align-items: center;
            gap: 6px;
            margin-top: 16px;
            padding: 6px 12px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 8px;
            font-size: 0.8rem;
            color: var(--text-muted);
        }}

        .source-tag::before {{
            content: '';
            width: 6px; height: 6px;
            background: var(--source-color);
            border-radius: 50%;
            animation: blink 2s ease-in-out infinite;
        }}

        @keyframes blink {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.3; }}
        }}

        /* Featured card */
        .card.featured {{ grid-column: span 2; }}
        @media (max-width: 768px) {{
            .card.featured {{ grid-column: span 1; }}
        }}
        .card.featured h2 {{ font-size: 1.5rem; }}

        /* Footer */
        footer {{
            margin-top: 80px;
            padding: 40px;
            text-align: center;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
        }}

        .footer-logo {{
            font-size: 1.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #ffffff 0%, #00f5ff 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 16px;
        }}

        .data-sources {{
            display: flex;
            justify-content: center;
            gap: 16px;
            flex-wrap: wrap;
            margin: 24px 0;
        }}

        .source-pill {{
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 8px 16px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 50px;
            font-size: 0.85rem;
            color: var(--text-secondary);
            transition: all 0.3s ease;
        }}

        .source-pill:hover {{
            background: rgba(0, 245, 255, 0.1);
            border-color: rgba(0, 245, 255, 0.3);
            transform: translateY(-2px);
        }}

        .source-pill::before {{
            content: '';
            width: 8px; height: 8px;
            background: #00f5ff;
            border-radius: 50%;
            animation: pulse-dot 2s ease-in-out infinite;
        }}

        @keyframes pulse-dot {{
            0%, 100% {{ transform: scale(1); opacity: 1; }}
            50% {{ transform: scale(1.2); opacity: 0.7; }}
        }}

        .copyright {{
            color: var(--text-muted);
            font-size: 0.85rem;
            margin-top: 24px;
        }}

        /* Scroll reveal animation */
        .card {{
            opacity: 0;
            transform: translateY(30px);
            animation: reveal 0.6s ease forwards;
        }}

        { ''.join([f'.card:nth-child({i+1}) {{ animation-delay: {i * 0.1}s; }}' for i in range(12)]) }

        @keyframes reveal {{
            to {{ opacity: 1; transform: translateY(0); }}
        }}
    </style>
</head>
<body>
    <div class="bg-grid"></div>
    <div class="particles">
        <div class="particle" style="left: 10%; animation-delay: 0s;"></div>
        <div class="particle" style="left: 20%; animation-delay: 2s;"></div>
        <div class="particle" style="left: 30%; animation-delay: 4s;"></div>
        <div class="particle" style="left: 40%; animation-delay: 1s;"></div>
        <div class="particle" style="left: 50%; animation-delay: 3s;"></div>
        <div class="particle" style="left: 60%; animation-delay: 5s;"></div>
        <div class="particle" style="left: 70%; animation-delay: 2.5s;"></div>
        <div class="particle" style="left: 80%; animation-delay: 4.5s;"></div>
        <div class="particle" style="left: 90%; animation-delay: 1.5s;"></div>
    </div>

    <div class="container">
        <header>
            <div class="logo">
                <div class="logo-icon">📰</div>
                <div>
                    <h1 class="masthead">AI 科技日报</h1>
                    <p class="tagline">Technology Intelligence Daily</p>
                </div>
            </div>
            <div class="date-badge">
                <span>{date_str}</span>
                <span class="divider"></span>
                <span>{get_weekday_cn(date_str)}</span>
                <span class="divider"></span>
                <span>多源聚合</span>
            </div>
        </header>

        <div class="stats-bar">
            <div class="stat">
                <div class="stat-value">{len(news_items)}</div>
                <div class="stat-label">新闻条数</div>
            </div>
            <div class="stat">
                <div class="stat-value">{len(sources)}</div>
                <div class="stat-label">数据源</div>
            </div>
            <div class="stat">
                <div class="stat-value">08:30</div>
                <div class="stat-label">每日推送</div>
            </div>
        </div>

        <div class="news-grid">
            {cards_html}
        </div>

        <footer>
            <div class="footer-logo">AI 科技日报</div>
            <p style="color: var(--text-secondary);">聚合全球科技资讯，洞察AI前沿动态</p>
            <div class="data-sources">
                <span class="source-pill">AI Hot API</span>
                <span class="source-pill">36氪</span>
                <span class="source-pill">TechCrunch</span>
            </div>
            <p class="copyright">Generated on {date_str} {now.strftime("%H:%M")} | GitHub Actions 自动部署</p>
        </footer>
    </div>
</body>
</html>'''
    
    return html

def main():
    """Main entry point"""
    os.makedirs('dist', exist_ok=True)
    
    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")
    
    print(f"🚀 Generating tech-style report for {date_str}...")
    
    # For now, use sample data to demonstrate the new design
    sample_news = [
        {
            "category": "产品发布",
            "title": "OpenAI 发布 GPT-5 预览版，性能提升 40%",
            "content": "OpenAI 今日发布了 GPT-5 的预览版本，新模型在推理能力、代码生成和多模态理解方面都有显著提升。据官方数据，GPT-5 在各项基准测试中平均性能提升 40%。",
            "source": "AI Hot API"
        },
        {
            "category": "行业动态",
            "title": "Anthropic 融资 20 亿美元，估值突破 200 亿",
            "content": "Anthropic 宣布完成新一轮 20 亿美元融资，由 Spark Capital 领投。公司估值从 180 亿美元跃升至 220 亿美元。",
            "source": "36氪"
        },
        {
            "category": "论文研究",
            "title": "Google DeepMind 提出新的 Transformer 架构",
            "content": "Google DeepMind 研究团队发布了一篇新论文，提出了一种改进的 Transformer 架构，在保持性能的同时将计算复杂度降低了 50%。",
            "source": "TechCrunch"
        },
        {
            "category": "工具推荐",
            "title": "Claude Code 新增多文件编辑功能",
            "content": "Anthropic 更新了 Claude Code 工具，新增多文件同时编辑、智能代码重构和自动测试生成功能。",
            "source": "AI Hot API"
        },
        {
            "category": "国际动态",
            "title": "欧盟通过 AI 法案最终版本",
            "content": "欧盟议会正式通过了 AI 法案的最终版本，该法案将对高风险 AI 应用实施严格监管，预计 2025 年初生效。",
            "source": "TechCrunch"
        },
        {
            "category": "投融资",
            "title": "AI 芯片初创公司 Cerebras 获 5 亿美元融资",
            "content": "专注于 AI 加速芯片的初创公司 Cerebras 宣布获得 5 亿美元 D 轮融资，公司估值达到 40 亿美元。",
            "source": "36氪"
        }
    ]
    
    # Generate HTML with tech style
    html = generate_html(sample_news, date_str)
    
    # Save to file
    output_file = f'dist/{date_str}.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ Generated tech-style report: {output_file}")
    print("🎉 Done!")

if __name__ == '__main__':
    main()