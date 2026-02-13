#!/usr/bin/env python3
"""
AI博客每日摘要系统 - 测试版（无AI总结）
自动抓取AI大牛博客并发送邮件
"""

import feedparser
import requests
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
import os
import json
import time
from bs4 import BeautifulSoup

# 配置信息
BLOGS = {
    "Andrej Karpathy": "https://karpathy.github.io/feed.xml",
    "OpenAI Blog": "https://openai.com/blog/rss.xml",
    "Anthropic": "https://www.anthropic.com/news/rss.xml",
    "Distill.pub": "https://distill.pub/rss.xml",
    "Google AI Blog": "https://ai.googleblog.com/feeds/posts/default",
    "DeepMind Blog": "https://deepmind.google/blog/rss.xml",
}

def fetch_blog_posts(hours=24):
    """抓取最近24小时的博客文章"""
    posts = []
    cutoff_time = datetime.now() - timedelta(hours=hours)
    
    for blog_name, feed_url in BLOGS.items():
        try:
            print(f"正在抓取: {blog_name}...")
            feed = feedparser.parse(feed_url)
            
            for entry in feed.entries[:5]:  # 只看最新的5篇
                # 解析发布时间
                pub_date = None
                if hasattr(entry, 'published_parsed') and entry.published_parsed:
                    pub_date = datetime(*entry.published_parsed[:6])
                elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                    pub_date = datetime(*entry.updated_parsed[:6])
                
                # 如果是最近24小时的文章
                if pub_date and pub_date > cutoff_time:
                    content = ""
                    if hasattr(entry, 'summary'):
                        content = entry.summary
                    elif hasattr(entry, 'description'):
                        content = entry.description
                    
                    # 清理HTML标签
                    soup = BeautifulSoup(content, 'html.parser')
                    clean_content = soup.get_text()
                    
                    posts.append({
                        'blog': blog_name,
                        'title': entry.title if hasattr(entry, 'title') else 'Untitled',
                        'link': entry.link if hasattr(entry, 'link') else '',
                        'content': clean_content[:500],  # 限制长度
                        'date': pub_date.strftime('%Y-%m-%d %H:%M') if pub_date else 'Unknown',
                        'summary': clean_content[:200] + '...' if len(clean_content) > 200 else clean_content
                    })
                    print(f"  发现新文章: {entry.title}")
        
        except Exception as e:
            print(f"  抓取 {blog_name} 失败: {str(e)}")
            continue
    
    return posts

def create_email_html(posts):
    """创建HTML格式的邮件内容"""
    if not posts:
        return "<h2>今日无新文章</h2><p>今天没有抓取到新的博客文章。</p>"
    
    html = f"""
    <html>
    <head>
        <meta charset="UTF-8">
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                       color: white; padding: 20px; text-align: center; }}
            .post {{ background: #f9f9f9; margin: 20px 0; padding: 20px; 
                     border-left: 4px solid #667eea; border-radius: 5px; }}
            .post-title {{ color: #667eea; font-size: 18px; font-weight: bold; margin-bottom: 10px; }}
            .post-meta {{ color: #666; font-size: 14px; margin-bottom: 10px; }}
            .post-summary {{ margin-top: 10px; line-height: 1.8; }}
            .post-link {{ display: inline-block; margin-top: 10px; color: #667eea; 
                         text-decoration: none; font-weight: bold; }}
            .footer {{ text-align: center; color: #999; margin-top: 30px; padding: 20px; 
                      border-top: 1px solid #ddd; }}
            .note {{ background: #fff3cd; padding: 10px; margin: 20px 0; 
                    border-left: 4px solid #ffc107; border-radius: 5px; }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>AI博客每日摘要</h1>
            <p>{datetime.now().strftime('%Y年%m月%d日')}</p>
        </div>
        
        <div style="max-width: 800px; margin: 0 auto; padding: 20px;">
            <div class="note">
                <strong>测试模式：</strong> 当前使用测试版本，暂未启用AI总结功能。
                显示文章原始摘要。充值Anthropic API后可启用AI智能总结。
            </div>
            
            <p>今日共收集到 <strong>{len(posts)}</strong> 篇AI领域新文章：</p>
    """
    
    for post in posts:
        # 确保所有文本都是UTF-8编码
        title = post['title'].encode('utf-8', errors='ignore').decode('utf-8')
        blog = post['blog'].encode('utf-8', errors='ignore').decode('utf-8')
        summary = post['summary'].encode('utf-8', errors='ignore').decode('utf-8')
        
        html += f"""
            <div class="post">
                <div class="post-title">{title}</div>
                <div class="post-meta">来源: {blog} | 发布时间: {post['date']}</div>
                <div class="post-summary">
                    {summary}
                </div>
                <a href="{post['link']}" class="post-link">阅读原文 →</a>
            </div>
        """
    
    html += """
        <div class="footer">
            <p>此邮件由AI博客摘要系统自动生成（测试版）</p>
            <p>如需启用AI智能总结，请充值Anthropic API</p>
        </div>
        </div>
    </body>
    </html>
    """
    
    return html

def send_email(recipient, subject, html_content):
    """发送邮件"""
    sender_email = os.environ.get('SENDER_EMAIL')
    sender_password = os.environ.get('SENDER_PASSWORD')
    smtp_server = os.environ.get('SMTP_SERVER', 'smtp.gmail.com')
    smtp_port = int(os.environ.get('SMTP_PORT', '587'))
    
    if not all([sender_email, sender_password]):
        print("错误: 未设置邮件发送配置")
        return False
    
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = recipient
        
        html_part = MIMEText(html_content, 'html', 'utf-8')
        msg.attach(html_part)
        
        print(f"正在发送邮件到 {recipient}...")
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        
        print("邮件发送成功!")
        return True
        
    except Exception as e:
        print(f"邮件发送失败: {str(e)}")
        return False

def main():
    """主函数"""
    print("="*60)
    print("AI博客每日摘要系统启动（测试版 - 无AI总结）")
    print(f"运行时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    
    # 1. 抓取博客
    print("\n[1/3] 抓取博客文章...")
    posts = fetch_blog_posts(hours=24)
    print(f"共抓取到 {len(posts)} 篇新文章")
    
    if not posts:
        print("\n今日无新文章，退出")
        return
    
    # 2. 生成邮件（跳过AI总结）
    print("\n[2/3] 生成邮件内容（使用原始摘要）...")
    html_content = create_email_html(posts)
    
    # 3. 发送邮件
    print("\n[3/3] 发送邮件...")
    recipient = "liuxialu615@gmail.com"
    subject = f"AI博客每日摘要（测试版）- {datetime.now().strftime('%Y年%m月%d日')} ({len(posts)}篇新文章)"
    
    success = send_email(recipient, subject, html_content)
    
    if success:
        print("\n" + "="*60)
        print("任务完成!")
        print("="*60)
    else:
        print("\n" + "="*60)
        print("任务失败")
        print("="*60)

if __name__ == "__main__":
    main()
