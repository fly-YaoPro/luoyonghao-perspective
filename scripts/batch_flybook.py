import os

SRC = r"C:\Users\GYao\Desktop\罗永浩音频\转文字"
DST = r"E:\CodeX AI\luo-yonghao-perspective\references\sources\transcripts"

MAP = {
    "P3_坚果U1（2015.8.25）": "2015_坚果U1",
    "P4_锤子T2（2015.12.29）": "2015_T2",
    "P5_锤子M1｜M1L（2016.10.18）": "2016_M1M1L",
    "P6_坚果Pro（2017.5.9）": "2017_坚果Pro",
    "P7_坚果Pro2（2017.11.7）": "2017_坚果Pro2",
    "P8_坚果3（2018.4.9）": "2018_坚果3",
    "P9_坚果Pro2S（2018.8.20）": "2018_坚果Pro2S",
    "P10_坚果R1｜TNT工作站（2018.5.15）": "2018_坚果R1_TNT工作站",
    "P11_锤子科技和Ta的朋友们（2018.11.6）": "2018_锤子科技和Ta的朋友们",
    "P12_坚果Pro 3（2019.10.31）": "2019_坚果Pro3",
    "P13_坚果R2｜TNT2.0（2020.10.20）": "2020_坚果R2_TNT2.0",
}

HEADER = "# 锤子发布会 {title} · 字幕\n\n> 源：飞书妙记 AI 转录，未人工校对。\n> 仅供表达风格/话题分析；原话/数字/人名/产品名不得当作准确引用。\n\n"

count = 0
for fn in os.listdir(SRC):
    if not fn.endswith(".txt"):
        continue
    key = next((k for k in MAP if k in fn), None)
    if not key:
        print(f"SKIP: {fn}")
        continue
    slug = MAP[key]
    title = key.split("_", 1)[1].replace("｜", "/")
    out = os.path.join(DST, f"锤子发布会_{slug}_字幕.md")
    
    with open(os.path.join(SRC, fn), encoding="utf-8") as f:
        body = f.read().strip()
    
    lines = body.split("\n")
    chars = sum(len(l) for l in lines)
    
    with open(out, "w", encoding="utf-8") as f:
        f.write(HEADER.format(title=title))
        f.write(body)
        f.write("\n")
    
    count += 1
    print(f"OK: 锤子发布会_{slug}_字幕.md | {len(lines)}行 | {chars}字")

print(f"\nDone: {count} files")
