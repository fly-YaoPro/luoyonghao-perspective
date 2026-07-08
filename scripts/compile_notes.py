import urllib.request, urllib.parse, re, os

DST = r"E:\CodeX AI\luo-yonghao-perspective\references\sources\articles"
os.makedirs(DST, exist_ok=True)
HEADERS = {"User-Agent": "Mozilla/5.0"}

def search(q):
    u = "https://www.sogou.com/web?query=" + urllib.parse.quote(q)
    r = urllib.request.Request(u, headers=HEADERS)
    return urllib.request.urlopen(r, timeout=15).read().decode("utf-8", errors="ignore")

def snippets(html):
    ts = re.findall(r"<h3[^>]*>(.*?)</h3>", html, re.DOTALL)
    ps = re.findall(r"<p[^>]*>(.*?)</p>", html, re.DOTALL)
    ps = [p for p in ps if len(p) > 60]
    out = []
    for i, t in enumerate(ts[:10]):
        ct = re.sub(r"<[^>]*>", "", t).strip()
        s = re.sub(r"<[^>]*>", "", ps[i]).strip() if i < len(ps) else ""
        if len(ct) > 5:
            out.append(ct + "\n  " + s[:300])
    return out

# Collect all topics
topics = [
    ("西门子冰箱维权", "罗永浩 西门子冰箱门 维权 2011 事件 全过程 回顾"),
    ("锤子创业决策", "罗永浩 锤子科技 创业 融资 失败 关键决策 反思"),
    ("深度报道", "罗永浩 深度报道 36氪 极客公园 晚点 人物特稿"),
    ("微博发言精选", "罗永浩 微博 经典 发言 语录"),
    ("直播口播合集", "罗永浩 直播带货 金句 经典 口播"),
]

note = "# 罗永浩 P1 素材 · 网络搜索采集\n\n"
note += "> 自动采集时间: 2026-07-08\n"
note += "> 来源: Sogou 搜索结果摘要 + 部分直接下载\n"
note += "> 注意: 这些是搜索结果片段，非完整文章。完整文章需人工访问原始链接获取。\n\n"

for label, query in topics:
    note += "## " + label + "\n\n"
    try:
        h = search(query)
        for s in snippets(h):
            note += "- " + s.replace("\n", "\n  ") + "\n\n"
    except Exception as e:
        note += "(搜索失败: " + str(e)[:80] + ")\n\n"

# Also add the profile article content if available
pf = os.path.join(DST, "profile_so_html5_qq_com.txt")
if os.path.exists(pf):
    with open(pf, encoding="utf-8") as f:
        content = f.read()
    if len(content) > 200:
        note += "## 已成功下载的文章片段\n\n"
        note += content[:3000] + "\n\n"

with open(os.path.join(DST, "_research_notes.md"), "w", encoding="utf-8") as f:
    f.write(note)

print("Research notes saved: " + str(len(note)) + " chars")