import urllib.request, urllib.parse, re, os

DST = r"E:\CodeX AI\luo-yonghao-perspective\references\sources\articles"
os.makedirs(DST, exist_ok=True)

def search_bing(q):
    url = "https://www.bing.com/search?q=" + urllib.parse.quote(q)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    resp = urllib.request.urlopen(req, timeout=15)
    return resp.read().decode("utf-8", errors="ignore")

def extract(h):
    # Bing search result links
    links = re.findall(r'<a[^>]*href="(https?://[^"]+)"[^>]*>(.*?)</a>', h, re.DOTALL)
    results = []
    for url, title in links:
        ct = re.sub(r'<[^>]*>', '', title).strip()
        if len(ct) > 10 and url.startswith('http') and 'bing.com' not in url and 'microsoft.com' not in url:
            results.append((url, ct))
    return results[:8]

def fetch_text(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        resp = urllib.request.urlopen(req, timeout=10)
        html = resp.read().decode("utf-8", errors="ignore")
        # Extract text from body
        text = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL)
        text = re.sub(r'<style[^>]*>.*?</style>', '', text, flags=re.DOTALL)
        text = re.sub(r'<[^>]+>', ' ', text)
        text = re.sub(r'\s+', ' ', text).strip()
        return text[:5000]
    except:
        return ""

# === Search 1: ??????? ===
print("=== ??????? ===")
h = search_bing("??? ????? ?? 2011 ?? ???")
for url, title in extract(h):
    print(f"  {title[:80]}")
    print(f"    {url}")

print()
print("=== ???????? ===")
h2 = search_bing("??? ???? ???? ?? ?? ????")
for url, title in extract(h2):
    print(f"  {title[:80]}")
    print(f"    {url}")

print()
print("=== ???? ===")
h3 = search_bing("??? 36? OR ???? OR ?? ???? ??")
for url, title in extract(h3):
    print(f"  {title[:80]}")
    print(f"    {url}")
