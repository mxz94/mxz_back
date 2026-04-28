import os

# ============== 配置 ==============
# podcast_files 文件夹路径（相对于此脚本）
PODCAST_DIR = r"E:\CloudMusic\mp3"  # 修改为您的实际路径
# 生成的HTML文件路径
OUTPUT_HTML = r"E:\podcast_hub.html"  # 修改为输出路径
# 服务器URL前缀
BASE_URL = "https://malanxi.top/podcast_files/"
# ==================================

def scan_podcasts(podcast_dir):
    """扫描 podcast_files 目录，返回所有子文件夹名称"""
    podcasts = []
    try:
        for item in os.listdir(podcast_dir):
            item_path = os.path.join(podcast_dir, item)
            # 只添加文件夹
            if os.path.isdir(item_path):
                podcasts.append(item)
        
        # 自然排序
        podcasts.sort()
        return podcasts
    except Exception as e:
        print(f"❌ 扫描目录失败: {e}")
        return []

def generate_html(podcasts, base_url, output_path):
    """生成播客目录HTML文件"""
    
    # 生成播客数组的JavaScript代码
    podcasts_js = ',\n        '.join([f"'{p}'" for p in podcasts])
    
    html_content = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>怀旧播客馆 | 经典有声读物</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Noto+Serif+SC:wght@400;600;700&family=Courier+Prime&display=swap" rel="stylesheet">
    <style>
        :root {{
            --primary-bg: #e8dcc4;
            --card-bg: #f5ead6;
            --text-main: #3d2817;
            --text-muted: #8b6f47;
            --accent-color: #a0522d;
            --accent-warm: #cd853f;
            --shadow-vintage: 0 4px 8px rgba(61, 40, 23, 0.2);
            --border-vintage: #8b6f47;
            --radius-vintage: 4px;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{ 
            font-family: 'Noto Serif SC', Georgia, serif;
            background: #e8dcc4;
            background-image: 
                repeating-linear-gradient(0deg, transparent, transparent 2px, rgba(139, 111, 71, 0.03) 2px, rgba(139, 111, 71, 0.03) 4px),
                repeating-linear-gradient(90deg, transparent, transparent 2px, rgba(139, 111, 71, 0.03) 2px, rgba(139, 111, 71, 0.03) 4px);
            color: var(--text-main);
            margin: 0;
            padding: 20px;
            line-height: 1.8;
            position: relative;
            min-height: 100vh;
        }}
        
        body::before {{
            content: '';
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background-image: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="100" height="100"><filter id="noise"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="4" /></filter><rect width="100" height="100" filter="url(%23noise)" opacity="0.05"/></svg>');
            pointer-events: none;
            z-index: 1;
        }}
        
        .main-container {{
            position: relative;
            z-index: 2;
            max-width: 1200px; 
            margin: 0 auto;
        }}

        .header-hero {{
            background: linear-gradient(to bottom, #d4b896 0%, #c9a978 100%);
            border: 3px solid var(--border-vintage);
            border-radius: var(--radius-vintage);
            padding: 50px 40px;
            text-align: center;
            box-shadow: 
                var(--shadow-vintage),
                inset 0 1px 0 rgba(255, 255, 255, 0.3),
                inset 0 -1px 0 rgba(0, 0, 0, 0.2);
            margin-bottom: 40px;
            position: relative;
            overflow: hidden;
        }}
        
        .header-hero::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: repeating-linear-gradient(45deg, transparent, transparent 10px, rgba(139, 111, 71, 0.02) 10px, rgba(139, 111, 71, 0.02) 20px);
            pointer-events: none;
        }}
        
        .site-title {{
            position: relative;
            z-index: 2;
            font-size: 3em;
            font-weight: 700;
            color: var(--text-main);
            margin-bottom: 15px;
            letter-spacing: 3px;
            text-shadow: 2px 2px 4px rgba(255, 255, 255, 0.5);
        }}

        .site-subtitle {{
            position: relative;
            z-index: 2;
            font-size: 1.2em;
            color: var(--text-muted);
            font-family: 'Courier Prime', monospace;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
        }}

        .site-subtitle i {{
            color: var(--accent-color);
        }}

        .podcasts-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 30px;
            margin-bottom: 50px;
        }}

        .podcast-card {{
            background: var(--card-bg);
            border: 2px solid var(--border-vintage);
            border-radius: var(--radius-vintage);
            padding: 0;
            box-shadow: var(--shadow-vintage);
            transition: all 0.3s ease;
            position: relative;
            overflow: hidden;
            text-decoration: none;
            color: inherit;
            display: block;
        }}

        .podcast-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: repeating-linear-gradient(90deg, transparent, transparent 1px, rgba(139, 111, 71, 0.02) 1px, rgba(139, 111, 71, 0.02) 2px);
            pointer-events: none;
            z-index: 1;
        }}

        .podcast-card:hover {{
            transform: translateY(-5px) scale(1.02);
            box-shadow: 0 8px 16px rgba(61, 40, 23, 0.3);
            border-color: var(--accent-color);
        }}

        .podcast-cover {{
            width: 100%;
            height: 200px;
            background-size: cover;
            background-position: center;
            border-bottom: 2px solid var(--border-vintage);
            position: relative;
            filter: sepia(0.2) contrast(1.1);
        }}

        .podcast-cover::after {{
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            right: 0;
            height: 50%;
            background: linear-gradient(to top, rgba(61, 40, 23, 0.4), transparent);
        }}

        .podcast-info {{
            padding: 25px;
            position: relative;
            z-index: 2;
            text-align: center;
        }}

        .podcast-title {{
            font-size: 1.4em;
            font-weight: 700;
            color: var(--text-main);
            margin-bottom: 20px;
            letter-spacing: 1px;
            min-height: 2.8em;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .podcast-links {{
            display: flex;
            gap: 10px;
            justify-content: center;
        }}

        .podcast-btn {{
            display: inline-flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
            background: linear-gradient(to bottom, #8b6f47 0%, #6b5637 50%, #5a4527 100%);
            color: #f5ead6;
            padding: 12px 20px;
            border: 2px solid #3d2817;
            border-radius: var(--radius-vintage);
            font-weight: 600;
            text-decoration: none;
            transition: all 0.2s ease;
            box-shadow: 0 3px 0 #3d2817, 0 4px 6px rgba(0, 0, 0, 0.3);
            font-size: 0.95em;
            flex: 1;
            max-width: 140px;
        }}

        .podcast-btn:hover {{
            filter: brightness(1.1);
            transform: translateY(-2px);
            box-shadow: 0 5px 0 #3d2817, 0 6px 8px rgba(0, 0, 0, 0.3);
        }}

        .podcast-btn:active {{
            transform: translateY(1px);
            box-shadow: 0 1px 0 #3d2817, 0 2px 4px rgba(0, 0, 0, 0.3);
        }}

        .podcast-btn.rss {{
            background: linear-gradient(to bottom, #cd853f 0%, #a0522d 50%, #8b4513 100%);
        }}

        .footer {{
            text-align: center;
            padding: 30px 20px;
            border-top: 2px solid var(--border-vintage);
            margin-top: 50px;
            color: var(--text-muted);
            font-size: 0.9em;
            position: relative;
            z-index: 2;
        }}

        .footer a {{
            color: var(--accent-color);
            text-decoration: none;
            font-weight: 600;
        }}

        .footer a:hover {{
            text-decoration: underline;
        }}

        @media (max-width: 768px) {{
            body {{
                padding: 15px;
            }}
            
            .site-title {{
                font-size: 2em;
                letter-spacing: 1px;
            }}

            .site-subtitle {{
                font-size: 1em;
            }}

            .header-hero {{
                padding: 30px 20px;
            }}

            .podcasts-grid {{
                grid-template-columns: 1fr;
                gap: 20px;
            }}

            .podcast-btn {{
                font-size: 0.9em;
                padding: 10px 15px;
            }}
        }}
    </style>
</head>
<body>

<div class="main-container">
    <div class="header-hero">
        <h1 class="site-title">怀旧播客馆</h1>
        <div class="site-subtitle">
            <i class="fas fa-microphone-alt"></i>
            <span>重温经典 · 历史文化 · 有声读物</span>
        </div>
    </div>

    <div class="podcasts-grid" id="podcasts-container">
        <!-- 播客卡片将通过 JavaScript 动态生成 -->
    </div>

    <div class="footer">
        <p>
            <i class="fas fa-broadcast-tower"></i> 自托管播客系统 | 
            <a href="https://malanxi.top/" target="_blank">访问主站</a>
        </p>
        <p style="margin-top: 10px; font-size: 0.85em;">
            © 2024 怀旧播客馆 · 所有音频版权归原作者所有
        </p>
        <p style="margin-top: 5px; font-size: 0.8em; color: var(--text-muted);">
            <i class="fas fa-sync-alt"></i> 自动生成于 Python 脚本 · 共 {len(podcasts)} 个播客
        </p>
    </div>
</div>

<script>
    // ============== 自动生成配置 ==============
    const BASE_URL = '{base_url}';

    // 播客列表（由 Python 脚本自动扫描生成）
    const podcasts = [
        {podcasts_js}
    ];
    // =========================================

    function renderPodcasts() {{
        const container = document.getElementById('podcasts-container');
        
        podcasts.forEach(podcastName => {{
            const podcastUrl = BASE_URL + encodeURIComponent(podcastName) + '/';
            const coverUrl = podcastUrl + 'cover.jpg';
            const rssUrl = podcastUrl + 'podcast.xml';
            
            const cardHTML = `
                <div class="podcast-card">
                    <div class="podcast-cover" style="background-image: url('${{coverUrl}}');"></div>
                    <div class="podcast-info">
                        <h2 class="podcast-title">${{podcastName}}</h2>
                        <div class="podcast-links">
                            <a href="${{podcastUrl}}" class="podcast-btn" target="_blank">
                                <i class="fas fa-play-circle"></i>
                                播放器
                            </a>
                            <a href="${{rssUrl}}" class="podcast-btn rss" target="_blank">
                                <i class="fas fa-rss"></i>
                                RSS
                            </a>
                        </div>
                    </div>
                </div>
            `;
            
            container.innerHTML += cardHTML;
        }});
    }}

    document.addEventListener('DOMContentLoaded', renderPodcasts);

    document.addEventListener('DOMContentLoaded', () => {{
        setTimeout(() => {{
            document.querySelectorAll('.podcast-card').forEach(card => {{
                card.addEventListener('mouseenter', function() {{
                    this.style.transform = 'translateY(-5px) scale(1.02)';
                }});
                
                card.addEventListener('mouseleave', function() {{
                    this.style.transform = 'translateY(0) scale(1)';
                }});
            }});
        }}, 100);
    }});
</script>

</body>
</html>
'''
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✅ 播客目录HTML已生成: {output_path}")
        print(f"📁 共发现 {len(podcasts)} 个播客")
        for i, p in enumerate(podcasts, 1):
            print(f"   {i}. {p}")
    except Exception as e:
        print(f"❌ 生成HTML失败: {e}")


if __name__ == '__main__':
    print("🔍 正在扫描播客目录...")
    print(f"📂 目标目录: {PODCAST_DIR}")
    
    podcasts = scan_podcasts(PODCAST_DIR)
    
    if podcasts:
        generate_html(podcasts, BASE_URL, OUTPUT_HTML)
        print(f"\n🎉 完成！")
    else:
        print("⚠️ 未找到任何播客文件夹")
