import urllib.request, re

url = "https://mp.weixin.qq.com/s/YqPKQNHol2GBHe1CA4ftWw"
r = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
h = urllib.request.urlopen(r, timeout=10).read().decode("utf-8", errors="ignore")

# Try both patterns
m = re.search(r'id="js_content"[^>]*>(.*?)</div>\s*<script', h, re.DOTALL)
if not m:
    m = re.search(r'class="rich_media_content[^"]*"[^>]*>(.*?)</div>', h, re.DOTALL)

if m:
    text = m.group(1)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"&[a-z]+;", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    dst = r"E:\CodeX AI\luo-yonghao-perspective\references\sources\articles\wechat_laoluo_3.txt"
    with open(dst, "w", encoding="utf-8") as f:
        f.write("SOURCE: " + url + "\n\n")
        f.write(text)
    print("Saved: " + str(len(text)) + " chars")
    print(text[:300])
else:
    print("Not found - pages that work: tried js_content and rich_media_content")