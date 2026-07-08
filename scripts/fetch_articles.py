import urllib.request, urllib.parse, re, os, time

DST = r"E:\CodeX AI\luo-yonghao-perspective\references\sources\articles"
os.makedirs(DST, exist_ok=True)
HEADERS = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}

def search_sogou(q):
    u = "https://www.sogou.com/web?query=" + urllib.parse.quote(q)
    r = urllib.request.Request(u, headers=HEADERS)
    h = urllib.request.urlopen(r, timeout=15).read().decode("utf-8", errors="ignore")
    return h

def extract_links(html):
    urls = re.findall(r"href='([^']+)'", html)
    urls += re.findall(r'href="([^"]+)"', html)
    valid = []
    for u in urls:
        if not u.startswith("http"):
            continue
        if "sogou.com" in u or "go2map" in u:
            continue
        if len(u) < 30:
            continue
        valid.append(u)
    return list(dict.fromkeys(valid))[:10]

def clean_text(html):
    text = re.sub(r"<script[^>]*>.*?</script>", " ", html, flags=re.DOTALL)
    text = re.sub(r"<style[^>]*>.*?</style>", " ", text, flags=re.DOTALL)
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def fetch(url, slug):
    try:
        r = urllib.request.Request(url, headers=HEADERS)
        h = urllib.request.urlopen(r, timeout=10).read().decode("utf-8", errors="ignore")
        text = clean_text(h)
        fname = os.path.join(DST, slug + ".txt")
        with open(fname, "w", encoding="utf-8") as f:
            f.write("SOURCE: " + url + "\n\n")
            f.write(text[:10000])
        print("OK: " + slug + " (" + str(len(text)) + " chars)")
        return True
    except Exception as e:
        print("FAIL: " + slug + " - " + str(e)[:80])
        return False

# Siemens
print("=== Siemens ===")
h = search_sogou("罗永浩 西门子冰箱门 维权 2011")
for u in extract_links(h)[:4]:
    dom = re.match(r"https?://([^/]+)", u).group(1).replace(".", "_")
    fetch(u, "siemens_" + dom)
    time.sleep(0.3)

# 创业决策
print("\n=== Decisions ===")
h2 = search_sogou("罗永浩 锤子科技 创业 融资 资金链断裂 失败")
for u in extract_links(h2)[:4]:
    dom = re.match(r"https?://([^/]+)", u).group(1).replace(".", "_")
    fetch(u, "decision_" + dom)
    time.sleep(0.3)

# 深度报道
print("\n=== Profile ===")
h3 = search_sogou("罗永浩 36氪 极客公园 晚点 深度报道")
for u in extract_links(h3)[:4]:
    dom = re.match(r"https?://([^/]+)", u).group(1).replace(".", "_")
    fetch(u, "profile_" + dom)
    time.sleep(0.3)

print("\n=== Done ===")