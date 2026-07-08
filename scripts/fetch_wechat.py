import urllib.request, re

url = "https://mp.weixin.qq.com/s/YB8pcjxl0R3V9ABHnLZMMg"
r = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"})
h = urllib.request.urlopen(r, timeout=10).read().decode("utf-8", errors="ignore")

# Extract content from rich_media_content
m = re.search(r'<div[^>]*class="rich_media_content[^"]*"[^>]*>(.*?)</div>\s*<script', h, re.DOTALL)
if m:
    text = m.group(1)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"&[a-z]+;", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    
    dst = r"E:\CodeX AI\luo-yonghao-perspective\references\sources\articles\wechat_laoluo_quotes.txt"
    with open(dst, "w", encoding="utf-8") as f:
        f.write("SOURCE: " + url + "\n\n")
        f.write(text)
    print("Saved: " + str(len(text)) + " chars")
    print(text[:500])
else:
    print("Pattern not found")
    # Try alternative
    m2 = re.search(r'id="js_content"[^>]*>(.*?)</div>', h, re.DOTALL)
    if m2:
        t2 = re.sub(r"<[^>]+>", " ", m2.group(1)).strip()
        print("Alt found: " + str(len(t2)) + " chars")
        print(t2[:500])
    else:
        print("HTML snippet:", h[2000:3000])