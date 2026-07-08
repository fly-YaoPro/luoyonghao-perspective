import urllib.request, urllib.parse, re

def search(q):
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(q)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    resp = urllib.request.urlopen(req, timeout=15)
    return resp.read().decode("utf-8", errors="ignore")

def extract(h, label):
    print("=== " + label + " ===")
    # Find links
    pat = r'<a[^>]*class="result__a"[^>]*href="([^"]*)"[^>]*>(.*?)</a>'
    links = re.findall(pat, h, re.DOTALL)
    # Find snippets
    pat2 = r'<a[^>]*class="result__snippet"[^>]*>(.*?)</a>'
    snippets = re.findall(pat2, h, re.DOTALL)
    print("Results: " + str(len(links)))
    for i, (url, title) in enumerate(links[:5]):
        ct = re.sub(r"<[^>]*>", "", title).strip()
        snip = re.sub(r"<[^>]*>", "", snippets[i]).strip() if i < len(snippets) else ""
        print(str(i+1) + ". " + ct)
        print("   " + snip[:200])
        print()

# Run searches
extract(search("??? ?????? ?? 2011 ???"), "???????")
extract(search("??? ???? ?????? ?? ???"), "??????")
extract(search("??? 36? ???? ?? ???? ??"), "????")
extract(search("??? ?? ???? ?? ??"), "??????")
extract(search("??? ???? ???? ?? ??"), "????")
