#!/usr/bin/env python3
"""
Daily AI Report Generator
Generates HTML daily report from multiple data sources

Data Sources:
- AI Hot API (primary)
- 36氪 (RSS/网页抓取)
- Twitter/X (API - optional)
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

def fetch_36kr_news():
    """Fetch news from 36氪 RSS"""
    try:
        print("Fetching from 36kr...")
        # 36氪 RSS feeds
        feeds = [
            "https://rsshub.app/36kr/information/web_news",  # 资讯
            "https://rsshub.app/36kr/search/article/融资",  # 融资相关
        ]
        
        all_items = []
        for feed_url in feeds:
            try:
                response = requests.get(feed_url, timeout=15)
                if response.status_code == 200:
                    # Parse RSS XML
                    root = ET.fromstring(response.content)
                    items = root.findall('.//item')
                    for item in items[:5]:  # 取前5条
                        title = item.find('title')
                        description = item.find('description')
                        if title is not None:
                            all_items.append({
                                'category': '投融资',
                                'title': title.text,
                                'content': description.text[:200] + '...' if description and len(description.text) > 200 else (description.text if description else ''),
                                'source': '36氪'
                            })
            except Exception as e:
                print(f"  ⚠️ Feed failed: {e}")
                continue
        
        print(f"✅ Got {len(all_items)} items from 36kr")
        return all_items
    except Exception as e:
        print(f"⚠️ Error fetching from 36kr: {e}")
        return []

def fetch_techcrunch_news():
    """Fetch tech news from TechCrunch RSS"""
    try:
        print("Fetching from TechCrunch...")
        feed_url = "https://techcrunch.com/feed/"
        response = requests.get(feed_url, timeout=15)
        
        if response.status_code == 200:
            root = ET.fromstring(response.content)
            items = root.findall('.//item')
            
            news_items = []
            for item in items[:3]:  # 取前3条
                title = item.find('title')
                description = item.find('description')
                if title is not None:
                    news_items.append({
                        'category': '国际动态',
                        'title': title.text,
                        'content': '国际科技新闻',
                        'source': 'TechCrunch'
                    })
            
            print(f"✅ Got {len(news_items)} items from TechCrunch")
            return news_items
    except Exception as e:
        print(f"⚠️ Error fetching from TechCrunch: {e}")
        return []

def get_mock_data():
    """Fallback mock data if APIs fail"""
    return [
        {
            "category": "系统通知",
            "title": "正在从多个数据源获取新闻",
            "content": "日报系统正在从 AI Hot API、36氪、TechCrunch 等多个数据源聚合科技新闻。",
            "source": "System"
        },
        {
            "category": "配置状态", 
            "title": "GitHub Actions 自动部署",
            "content": "日报系统已通过 GitHub Actions 自动部署，每天 08:30 自动生成并推送到 GitHub Pages。支持飞书通知。",
            "source": "GitHub Actions"
        }
    ]

def get_category_color(category):
    """Map category to accent color"""
    category = str(category).strip()
    colors = {
        '产品发布': 'cyan',
        '产品更新': 'purple', 
        '行业动态': 'purple',
        '行业洞察': 'orange',
        '职场趋势': 'cyan',
        '并购动态': 'green',
        '论文研究': 'green',
        '工具推荐': 'orange',
        '投融资': 'purple',
        '投资': 'purple',
        '融资': 'purple',
        '国际动态': 'green',
        '系统通知': 'cyan',
        '配置状态': 'cyan',
    }
    return colors.get(category, 'cyan')

def get_weekday_cn(date_str):
    """Get Chinese weekday name"""
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
        weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
        return weekdays[date.weekday()]
    except:
        return ""

def aggregate_news():
    """Aggregate news from all sources"""
    all_news = []
    
    # Source 1: AI Hot API (primary)
    ai_hot_news = fetch_aihot_news()
    all_news.extend(ai_hot_news)
    
    # Source 2: 36氪
    kr_news = fetch_36kr_news()
    all_news.extend(kr_news)
    
    # Source 3: TechCrunch
    tc_news = fetch_techcrunch_news()
    all_news.extend(tc_news)
    
    # If no news fetched, use mock data
    if not all_news:
        print("⚠️ No news fetched from any source, using mock data")
        all_news = get_mock_data()
    
    print(f"\n📊 Total news items: {len(all_news)}")
    return all_news

def generate_html(news_items, date_str):
    """Generate HTML from news items"""
    
    # HTML Template
    template = Template('''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 科技日报 - {{ date_str }}</title>
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700;900&family=Noto+Sans+SC:wght@300;400;500;700&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg-primary: #0a0a0f;
            --bg-secondary: #12121a;
            --bg-card: #1a1a25;
            --accent-cyan: #00d4ff;
            --accent-purple: #a855f7;
            --accent-orange: #f97316;
            --accent-green: #22c55e;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --text-muted: #64748b;
            --border: #27273a;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Noto Sans SC', sans-serif;
            background: var(--bg-primary);
            color: var(--text-primary);
            line-height: 1.6;
            min-height: 100vh;
            background-image: 
                radial-gradient(ellipse 80% 50% at 20% 40%, rgba(168, 85, 247, 0.08) 0%, transparent 50%),
                radial-gradient(ellipse 60% 40% at 80% 60%, rgba(0, 212, 255, 0.06) 0%, transparent 50%);
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 40px 24px;
        }

        header {
            text-align: center;
            padding: 60px 0 50px;
            border-bottom: 1px solid var(--border);
            margin-bottom: 50px;
            position: relative;
        }

        .masthead {
            font-family: 'Noto Serif SC', serif;
            font-size: 4.5rem;
            font-weight: 900;
            letter-spacing: -0.02em;
            background: linear-gradient(135deg, var(--text-primary) 0%, var(--accent-cyan) 50%, var(--accent-purple) 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 16px;
            text-transform: uppercase;
        }

        .tagline {
            font-size: 1rem;
            color: var(--text-muted);
            letter-spacing: 0.3em;
            text-transform: uppercase;
            margin-bottom: 24px;
        }

        .date-line {
            display: flex;
            justify-content: center;
            align-items: center;
            gap: 20px;
            font-size: 0.9rem;
            color: var(--text-secondary);
        }

        .date-line::before,
        .date-line::after {
            content: '';
            width: 60px;
            height: 1px;
            background: linear-gradient(90deg, transparent, var(--border), transparent);
        }

        .stats-bar {
            display: flex;
            justify-content: center;
            gap: 30px;
            margin-top: 20px;
            padding-top: 20px;
            border-top: 1px solid var(--border);
        }

        .stat {
            text-align: center;
        }

        .stat-value {
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--accent-cyan);
        }

        .stat-label {
            font-size: 0.75rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.1em;
        }

        .news-grid {
            display: grid;
            grid-template-columns: repeat(12, 1fr);
            gap: 24px;
        }

        .card {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 28px;
            position: relative;
            overflow: hidden;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }

        .card:hover {
            transform: translateY(-4px);
            box-shadow: 0 20px 40px rgba(0,0,0,0.3);
        }

        .card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 3px;
            background: var(--accent-color, var(--accent-cyan));
        }

        .card-featured { grid-column: span 8; }
        .card-side { grid-column: span 4; }
        .card-half { grid-column: span 6; }
        .card-full { grid-column: span 12; }

        .card-cyan { --accent-color: var(--accent-cyan); }
        .card-purple { --accent-color: var(--accent-purple); }
        .card-orange { --accent-color: var(--accent-orange); }
        .card-green { --accent-color: var(--accent-green); }

        .category-tag {
            display: inline-block;
            font-size: 0.7rem;
            font-weight: 700;
            letter-spacing: 0.15em;
            text-transform: uppercase;
            color: var(--accent-color, var(--accent-cyan));
            margin-bottom: 12px;
            padding: 4px 10px;
            border: 1px solid var(--accent-color, var(--accent-cyan));
            border-radius: 4px;
            opacity: 0.8;
        }

        .card h2 {
            font-family: 'Noto Serif SC', serif;
            font-size: 1.5rem;
            font-weight: 700;
            line-height: 1.3;
            margin-bottom: 16px;
            color: var(--text-primary);
        }

        .card h3 {
            font-size: 1.15rem;
            font-weight: 600;
            margin-bottom: 10px;
            color: var(--text-primary);
        }

        .card p {
            color: var(--text-secondary);
            font-size: 0.95rem;
            line-height: 1.7;
        }

        .source-tag {
            display: inline-block;
            font-size: 0.75rem;
            color: var(--text-muted);
            margin-top: 12px;
            padding: 2px 8px;
            background: var(--bg-secondary);
            border-radius: 4px;
        }

        footer {
            margin-top: 60px;
            padding: 40px 0;
            border-top: 1px solid var(--border);
            text-align: center;
            color: var(--text-muted);
            font-size: 0.85rem;
        }

        .footer-brand {
            font-family: 'Noto Serif SC', serif;
            font-size: 1.5rem;
            font-weight: 700;
            color: var(--text-secondary);
            margin-bottom: 12px;
        }

        .data-sources {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin-top: 16px;
            flex-wrap: wrap;
        }

        .data-source {
            display: flex;
            align-items: center;
            gap: 6px;
            font-size: 0.8rem;
            color: var(--text-muted);
        }

        .data-source::before {
            content: '';
            width: 6px;
            height: 6px;
            background: var(--accent-green);
            border-radius: 50%;
        }

        @media (max-width: 900px) {
            .masthead { font-size: 3rem; }
            .card-featured, .card-side, .card-half { grid-column: span 12; }
            .stats-bar { flex-direction: column; gap: 15px; }
        }

        @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .card {
            animation: fadeInUp 0.6s ease forwards;
            opacity: 0;
        }

        .card:nth-child(1) { animation-delay: 0.1s; }
        .card:nth-child(2) { animation-delay: 0.2s; }
        .card:nth-child(3) { animation-delay: 0.3s; }
        .card:nth-child(4) { animation-delay: 0.4s; }
        .card:nth-child(5) { animation-delay: 0.5s; }
        .card:nth-child(6) { animation-delay: 0.6s; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1 class="masthead">AI 科技日报</h1>
            <p class="tagline">Artificial Intelligence Daily</p>
            <div class="date-line">
                <span>{{ date_str }}</span>
                <span>{{ weekday }}</span>
                <span>多源聚合</span>
            </div>
            <div class="stats-bar">
                <div class="stat">
                    <div class="stat-value">{{ news_count }}</div>
                    <div class="stat-label">新闻条数</div>
                </div>
                <div class="stat">
                    <div class="stat-value">{{ source_count }}</div>
                    <div class="stat-label">数据源</div>
                </div>
                <div class="stat">
                    <div class="stat-value">08:30</div>
                    <div class="stat-label">每日推送</div>
                </div>
            </div>
        </header>

        <div class="news-grid">
            {% for item in news_items %}
            <article class="card card-{{ item.span }} card-{{ item.color }}">
                <span class="category-tag">{{ item.category }}</span>
                <h2>{{ item.title }}</h2>
                <p>{{ item.content }}</p>
                {% if item.source %}
                <span class="source-tag">{{ item.source }}</span>
                {% endif %}
            </article>
            {% endfor %}
        </div>

        <footer>
            <div class="footer-brand">AI 科技日报</div>
            <p>数据来源于多个科技媒体 | 仅供信息分享，不构成投资建议</p>
            <div class="data-sources">
                <span class="data-source">AI Hot API</span>
                <span class="data-source">36氪</span>
                <span class="data-source">TechCrunch</span>
            </div>
            <p style="margin-top: 16px;">Generated on {{ date_str }} {{ time_str }} | 自动推送</p>
        </footer>
    </div>
</body>
</html>''')
    
    # Process news items - assign card spans
    processed_items = []
    for i, item in enumerate(news_items[:12]):  # 最多显示12条
        # Determine card span based on position
        if i == 0:
            span = 'featured'
        elif i == 1:
            span = 'side'
        elif i < 6:
            span = 'half'
        else:
            span = 'half'
            
        processed_items.append({
            'title': item.get('title', ''),
            'content': item.get('content', '')[:300] + '...' if len(item.get('content', '')) > 300 else item.get('content', ''),
            'category': item.get('category', '动态'),
            'source': item.get('source', ''),
            'color': get_category_color(item.get('category', '')),
            'span': span
        })
    
    # Count unique sources
    sources = set(item.get('source', 'Unknown') for item in news_items)
    
    now = datetime.now()
    html = template.render(
        date_str=date_str,
        weekday=get_weekday_cn(date_str),
        time_str=now.strftime("%H:%M"),
        news_items=processed_items,
        news_count=len(news_items),
        source_count=len(sources)
    )
    
    return html

def generate_index(dates):
    """Generate index page with all reports"""
    template = Template('''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI 科技日报 - Archive</title>
    <style>
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            max-width: 800px;
            margin: 50px auto;
            padding: 20px;
            background: #0a0a0f;
            color: #f8fafc;
        }
        h1 {
            color: #00d4ff;
            border-bottom: 2px solid #00d4ff;
            padding-bottom: 10px;
        }
        .report-list {
            list-style: none;
            padding: 0;
        }
        .report-list li {
            margin: 10px 0;
            padding: 15px;
            background: #1a1a25;
            border-radius: 8px;
            border: 1px solid #27273a;
            transition: transform 0.2s;
        }
        .report-list li:hover {
            transform: translateX(5px);
            border-color: #00d4ff;
        }
        .report-list a {
            color: #00d4ff;
            text-decoration: none;
            font-size: 1.1em;
        }
        .report-list a:hover {
            text-decoration: underline;
        }
        .date {
            color: #64748b;
            font-size: 0.9em;
            margin-top: 5px;
        }
        .subtitle {
            color: #94a3b8;
            margin-bottom: 30px;
        }
        .info {
            background: #1a1a25;
            padding: 15px;
            border-radius: 8px;
            border-left: 3px solid #00d4ff;
            margin-bottom: 30px;
        }
        .info p {
            margin: 5px 0;
            color: #94a3b8;
        }
        .sources {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            margin-top: 10px;
        }
        .source-tag {
            background: #27273a;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 0.8rem;
            color: #94a3b8;
        }
    </style>
</head>
<body>
    <h1>📰 AI 科技日报存档</h1>
    <p class="subtitle">每日AI科技新闻自动汇总 - 多源聚合</p>
    
    <div class="info">
        <p>⏰ 每天 08:30 自动生成</p>
        <p>📊 数据源:</p>
        <div class="sources">
            <span class="source-tag">AI Hot API</span>
            <span class="source-tag">36氪</span>
            <span class="source-tag">TechCrunch</span>
        </div>
        <p style="margin-top: 10px;">🔔 支持飞书推送通知</p>
    </div>
    
    <ul class="report-list">
        {% for date in dates %}
        <li>
            <a href="{{ date.file }}">AI 科技日报 - {{ date.display }}</a>
            <div class="date">{{ date.display }}</div>
        </li>
        {% endfor %}
    </ul>
    
    <footer style="margin-top: 60px; padding-top: 20px; border-top: 1px solid #27273a; text-align: center; color: #64748b; font-size: 0.85rem;">
        <p>GitHub: InFish111/daily-ai-reports</p>
    </footer>
</body>
</html>''')
    
    return template.render(dates=dates)

def main():
    """Main entry point"""
    # Create dist directory
    os.makedirs('dist', exist_ok=True)
    
    # Get today's date
    today = datetime.now()
    date_str = today.strftime("%Y-%m-%d")
    
    print(f"🚀 Generating report for {date_str}...")
    print("=" * 50)
    
    # Aggregate news from all sources
    news_items = aggregate_news()
    
    print("=" * 50)
    
    # Generate HTML
    html = generate_html(news_items, date_str)
    
    # Save to file
    output_file = f'dist/{date_str}.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ Generated: {output_file}")
    
    # Generate index with all available reports
    dates = []
    
    # Check for existing reports in dist
    if os.path.exists('dist'):
        for f in sorted(os.listdir('dist'), reverse=True):
            if f.endswith('.html') and f != 'index.html':
                date_str_file = f.replace('.html', '')
                try:
                    d = datetime.strptime(date_str_file, "%Y-%m-%d")
                    dates.append({
                        'file': f,
                        'display': d.strftime("%Y年%m月%d日")
                    })
                except:
                    pass
    
    index_html = generate_index(dates)
    with open('dist/index.html', 'w', encoding='utf-8') as f:
        f.write(index_html)
    
    print(f"✅ Generated index with {len(dates)} reports")
    print("🎉 Done!")

if __name__ == '__main__':
    main()
