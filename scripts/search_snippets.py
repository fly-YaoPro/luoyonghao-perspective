import urllib.request, urllib.parse, re, os

DST = r"E:\CodeX AI\luo-yonghao-perspective\references\sources\articles"
os.makedirs(DST, exist_ok=True)
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def search_sogou(q):
    u = "https://www.sogou.com/web?query=" + urllib.parse.quote(q)
    r = urllib.request.Request(u, headers=HEADERS)
    h = urllib.request.urlopen(r, timeout=15).read().decode("utf-8", errors="ignore")
    return h

def extract_snippets(html):
    # Extract title + snippet pairs from Sogou results
    titles = re.findall(r'<h3[^>]*>(.*?)</h3>', html, re.DOTALL)
    snippets = re.findall(r'<p[^>]*class="[^"]*str[^"]*"[^>]*>(.*?)</p>', html, re.DOTALL)
    # Also try other snippet patterns
    if not snippets:
        snippets = re.findall(r'<div[^>]*class="[^"]*space[^"]*"[^>]*>(.*?)</div>', html, re.DOTALL)
    # Fallback: any p tag with substantial content
    if not snippets:
        all_ps = re.findall(r'<p[^>]*>(.*?)</p>', html, re.DOTALL)
        snippets = [p for p in all_ps if len(p) > 50]
    
    results = []
    for i, t in enumerate(titles[:15]):
        ct = re.sub(r'<[^>]*>', '', t).strip()
        snip = re.sub(r'<[^>]*>', '', snippets[i]).strip() if i < len(snippets) else ""
        if len(ct) > 5:
            results.append((ct, snip[:300]))
    return results

# ===== Siemens =====
print("=== SIEMENS ===")
h = search_sogou("罗永浩 西门子冰箱门 维权 2011 事件回顾")
for title, snippet in extract_snippets(h)[:8]:
    print(title[:100])
    print("  " + snippet[:200])
    print()

# ===== 创业决策 =====
print("=== DECISIONS ===")
h2 = search_sogou("罗永浩 锤子科技 创业历程 融资 失败 关键决策 复盘")
for title, snippet in extract_snippets(h2)[:6]:
    print(title[:100])
    print("  " + snippet[:200])
    print()

# ===== 深度报道 =====
print("=== PROFILES ===")
h3 = search_sogou("罗永浩 深度报道 36氪 极客公园 晚点 人物 创业故事")
for title, snippet in extract_snippets(h3)[:6]:
    print(title[:100])
    print("  " + snippet[:200])
    print()

# ===== 微博发言精选 =====
print("=== WEIBO ===")
h4 = search_sogou("罗永浩 微博 经典 发言 语录 合集")
for title, snippet in extract_snippets(h4)[:5]:
    print(title[:100])
    print("  " + snippet[:200])
    print()

# ===== 直播口播 =====
print("=== LIVE ===")
h5 = search_sogou("罗永浩 直播带货 经典 口播 金句 合集")
for title, snippet in extract_snippets(h5)[:5]:
    print(title[:100])
    print("  " + snippet[:200])
    print()