#!/usr/bin/env python3
"""
Daily AI Report Generator
Generates HTML daily report from AI HOT API data
"""

import os
import json
import requests
from datetime import datetime, timedelta
from jinja2 import Template
import shutil

def fetch_aihot_news():
    """Fetch news from AI HOT API"""
    api_url = os.environ.get('AIHOT_API_URL', 'https://aihot.virxact.com/api/public/daily')
    
    try:
        response = requests.get(api_url, timeout=30)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        print(f"Error fetching from AIHOT API: {e}")
        return get_mock_data()

def get_mock_data():
    """Fallback mock data if API fails"""
    return {
        "date": datetime.now().strftime("%Y-%m-%d"),
        "news": [
            {
                "category": "产品发布",
                "title": "请配置 AIHOT_API_URL 环境变量以获取实时数据",
                "content": "当前显示的是示例数据。请在 GitHub Secrets 中设置 AIHOT_API_URL。",
                "source": "System"
            }
        ]
    }

def get_category_color(category):
    """Map category to accent color"""
    colors = {
        '产品发布': 'cyan',
        '产品更新': 'purple', 
        '行业动态': 'purple',
        '行业洞察': 'orange',
        '职场趋势': 'cyan',
        '并购动态': 'green',
        '论文研究': 'green',
        '工具推荐': 'orange'
    }
    return colors.get(category, 'cyan')

def get_weekday_cn(date_str):
    """Get Chinese weekday name"""
    weekdays = ['星期一', '星期二', '星期三', '星期四', '星期五', '星期六', '星期日']
    date = datetime.strptime(date_str, "%Y-%m-%d")
    return weekdays[date.weekday()]

def generate_html(data, date_str):
    """Generate HTML from data using template"""
    
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
            font-size: 1.6rem;
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

        .news-list {
            list-style: none;
        }

        .news-list li {
            padding: 16px 0;
            border-bottom: 1px solid var(--border);
        }

        .news-list li:last-child {
            border-bottom: none;
            padding-bottom: 0;
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

        @media (max-width: 900px) {
            .masthead { font-size: 3rem; }
            .card-featured, .card-side, .card-half { grid-column: span 12; }
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
                <span>自动生成</span>
            </div>
        </header>

        <div class="news-grid">
            {% for item in news_items %}
            <article class="card card-{{ item.span }} card-{{ item.color }}">
                <span class="category-tag">{{ item.category }}</span>
                <h2>{{ item.title }}</h2>
                <p>{{ item.content }}</p>
                {% if item.source %}
                <p style="margin-top: 12px; font-size: 0.85rem; color: var(--text-muted);">来源: {{ item.source }}</p>
                {% endif %}
            </article>
            {% endfor %}
        </div>

        <footer>
            <div class="footer-brand">AI 科技日报</div>
            <p>数据来源于 AI HOT API | 仅供信息分享，不构成投资建议</p>
            <p style="margin-top: 8px;">Generated on {{ date_str }} {{ time_str }}</p>
        </footer>
    </div>
</body>
</html>''')
    
    # Process news items
    news_items = []
    for i, item in enumerate(data.get('news', [])):
        # Determine card span based on importance/index
        if i == 0:
            span = 'featured'
        elif i == 1:
            span = 'side'
        elif i < 6:
            span = 'half'
        else:
            span = 'half'
            
        news_items.append({
            'title': item.get('title', ''),
            'content': item.get('content', ''),
            'category': item.get('category', '动态'),
            'source': item.get('source', ''),
            'color': get_category_color(item.get('category', '')),
            'span': span
        })
    
    now = datetime.now()
    html = template.render(
        date_str=date_str,
        weekday=get_weekday_cn(date_str),
        time_str=now.strftime("%H:%M"),
        news_items=news_items
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
        }
    </style>
</head>
<body>
    <h1>📰 AI 科技日报存档</h1>
    <ul class="report-list">
        {% for date in dates %}
        <li>
            <a href="{{ date.file }}">AI 科技日报 - {{ date.display }}</a>
            <div class="date">{{ date.display }}</div>
        </li>
        {% endfor %}
    </ul>
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
    
    print(f"Generating report for {date_str}...")
    
    # Fetch data
    data = fetch_aihot_news()
    
    # Generate HTML
    html = generate_html(data, date_str)
    
    # Save to file
    output_file = f'dist/{date_str}.html'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"Generated: {output_file}")
    
    # Copy existing reports if they exist
    if os.path.exists('html-files'):
        for f in os.listdir('html-files'):
            if f.endswith('.html') and f != 'index.html':
                src = os.path.join('html-files', f)
                dst = os.path.join('dist', f)
                if not os.path.exists(dst):
                    shutil.copy2(src, dst)
                    print(f"Copied existing: {f}")
    
    # Generate index
    dates = []
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
    
    print(f"Generated index with {len(dates)} reports")
    print("Done!")

if __name__ == '__main__':
    main()
