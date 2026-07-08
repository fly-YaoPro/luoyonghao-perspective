# 需求：清洗罗永浩锤子发布会 B站 AI 字幕（交付给 Codex/DeepSeek 执行）

> 本文件自包含。执行者无需其它上下文。目标：把从 B站下载的**多场锤子发布会 AI 自动字幕**清洗成干净、可分析的 Markdown 文本，供上游做"表达风格分析"。

## 0. 一句话目标
把杂乱的 AI 字幕（含时间戳、滚动重复、碎句）清洗成**一场发布会一个 .md 文件**的干净连续文本，**只做机械清洗，绝不改写内容**。

## 1. 输入
- 位置：`E:\Claude-DB\luo-yonghao-perspective\references\sources\_raw_subtitles\`（原始字幕放这里；若无此目录请创建）
- 特点：B站字幕（多为自动/ASR），**可能有错别字、谐音错、滚动重复、无标点或标点乱**。
- **两种常见格式，先判断再处理**：
  - **格式 A（优先，最常见）**：某导出工具生成的 `.md`，带 YAML frontmatter，正文含**两段**：`## 字幕时间线`（每行 `- [MM:SS](链接) 文本`）+ `## 字幕全文`（无时间戳连读正文）。**这两段是同一内容的重复。** → 见 §3-A。
  - **格式 B**：原始 `.srt` / `.vtt` / 纯 `.txt`。→ 见 §3-B。
- ✅ **已有一个清洗好的参照样例**：`references/sources/transcripts/锤子发布会_2013_SmartisanOS操作系统_B站字幕清洗.md`，请照它的样子产出（命名与头部格式都照它）。

## 2. 输出
- 位置：`E:\Claude-DB\luo-yonghao-perspective\references\sources\transcripts\`
- 命名：`锤子发布会_<年份>_<产品或场次>_字幕清洗.md`（年份/产品从原文件名或视频标题推断；推断不出就用原视频标题，宁可保留也不要猜错）。
- **原则上每场发布会一个文件。但若输入本身是"合集"视频**（标题含"合集/精选"，一个视频里多场发布会且**无明确场次边界**）→ **保持为一个文件**，命名带"合集"，**不要凭猜测强行切分**（切错比不切更糟）。
- 编码：UTF-8。

### 每个输出文件必须以这个头部开始（原样保留，一字不改）：
```
# <发布会名称> · AI字幕清洗版
> ⚠️ 来源：B站 AI 自动字幕，**低可信度、未人工校对**。
> ⚠️ 仅供表达风格/节奏/话题分析使用；**其中任何"原话/金句/数字/人名/产品名"都不得当作准确引用**，须另行核对权威文本。
> 原始文件：<原字幕文件名>
```

## 3-A. 格式 A 清洗规则（带【字幕时间线】+【字幕全文】的导出 md）
**核心决策：只保留 `## 字幕全文` 段，丢弃 `## 字幕时间线` 段。** 理由：两段内容重复；时间戳对"风格分析"是噪声；源视频 URL 会保留在头部，将来仍可回溯核对。
1. 从 frontmatter 取 `title` 和 `resource`(视频URL)，写进输出头部（见 §2 头部模板 + §5 脚本）。
2. 用正则抽出 `## 字幕全文` 到文件末（或下一个 `##`）之间的正文。
3. 该正文按字幕句**已自然分行**：去空行、去行尾空格、去相邻完全重复行，**保持一句一行**。
4. **不加标点、不改写**（全文无标点是原样，保守起见宁可保留连读，不要瞎断句/加句号）。
5. 直接用 §5 的 `clean_bili_export.py` 即可，**零大模型 token**。

## 3-B. 格式 B 清洗规则（原始 srt/vtt/txt，机械，按顺序执行）
1. **去格式噪声**：删除 SRT 序号行、`-->` 时间戳行、`WEBVTT`/`Kind`/`Language` 头、HTML/字幕标签（如 `<i>`、`{\an8}`）、空行。
2. **去滚动重复**：AI 字幕常见"每行在上一行基础上多几个字"的滚动式重复。规则：若某行是前一行的**前缀延展**（前一行内容是它的开头子串），只保留**更长的那一行**，丢弃被包含的短行。连续增长的一组只留最终最长版本。
3. **并句成段**：把碎片行按标点合并成完整句子/自然段。没有标点时，按语气与停顿**保守地**断句（宁可长句，不要瞎加句号）。每段之间空一行。
4. **规范空白**：合并多余空格；每行行尾去空格；不留连续空行（最多一个）。

## 4. 内容红线（最重要，务必遵守）
- **禁止改写、润色、意译、扩写、总结**。你的产物必须是"同样的话，只是格式干净了"。
- **禁止编造或补全**任何原文没有的内容。
- **错别字处理 = 极保守**：只在**上下文100%确定**且是明显谐音错的情况下改（如"工将精神"→"工匠精神"这类无歧义的）；**只要有一点不确定就原样保留**。**绝不为了通顺去猜改产品名、人名、数字。** 拿不准一律不动。
- 删除内容仅限"格式噪声 + 滚动重复"，**不得删除任何实际话语内容**。

## 5. 建议实现方式（省 token：能用脚本就别用大模型）
这些清洗**几乎全是确定性操作**，用下面的脚本跑即可，**不消耗大模型 token**。只有 §4 的"保守改错"在脚本处理完后，如确有必要再用轻量模型极小范围过一遍。

### 5-A. 格式 A 用这个脚本（提取「字幕全文」段）——已在样例上验证可用
```python
# clean_bili_export.py  —— 用法: python clean_bili_export.py <输入.md> <输出.md>
import sys, re
inp, outp = sys.argv[1], sys.argv[2]
raw = open(inp, encoding='utf-8', errors='ignore').read()
title = re.search(r'title:\s*"([^"]+)"', raw); title = title.group(1).strip() if title else "锤子发布会字幕"
url = re.search(r'resource:\s*"([^"]+)"', raw); url = url.group(1).strip() if url else ""
m = re.search(r'##\s*字幕全文\s*\n(.*?)(?:\n##\s|\Z)', raw, re.S)
if not m: print("!! 未找到【字幕全文】段"); sys.exit(2)
lines=[]
for ln in m.group(1).split('\n'):
    s=ln.strip()
    if not s: continue
    s=re.sub(r'^\-\s*\[[0-9:]+\]\([^)]*\)\s*','',s)   # 残留时间戳条目
    s=re.sub(r'\[[0-9:]+\]\([^)]*\)','',s).strip()
    if s: lines.append(s)
final=[]
for s in lines:
    if final and final[-1]==s: continue
    final.append(s)
is_ji = ('合集' in title) or ('精选' in title)
header=(f"# {title} · 字幕清洗版{'（合集）' if is_ji else ''}\n"
        f"> ⚠️ 来源：B站字幕（疑似自动/ASR），**低可信度、未人工校对**。\n"
        f"> ⚠️ 仅供表达风格/节奏/话题分析；\"原话/金句/数字/人名/产品名\"不得当准确引用，须另核对权威文本。\n"
        + (f"> ⚠️ 本文件为**多场发布会合集**，场次边界不明确，未强行切分。\n" if is_ji else "")
        + f"> 源视频：{url}\n\n")
open(outp,'w',encoding='utf-8').write(header + "\n".join(final) + "\n")
print("OK ->", outp, "| 行:", len(final), "| 汉字:", len(re.findall(r'[一-鿿]', "\n".join(final))))
```

### 5-B. 格式 B（原始 srt/vtt/txt）用这个脚本
```python
# clean_subtitles.py  —— 用法: python clean_subtitles.py <输入文件> <输出文件> "<发布会名称>"
import sys, re

inp, outp, title = sys.argv[1], sys.argv[2], sys.argv[3]
raw = open(inp, encoding='utf-8', errors='ignore').read()

lines = []
for ln in raw.split('\n'):
    s = ln.strip()
    if not s: continue
    if s.isdigit(): continue                      # SRT 序号
    if '-->' in s: continue                       # 时间戳
    if re.match(r'^(WEBVTT|Kind:|Language:)', s): continue
    s = re.sub(r'<[^>]+>', '', s)                 # 标签
    s = re.sub(r'\{\\[^}]*\}', '', s)             # ass 样式
    s = s.strip()
    if s: lines.append(s)

# 去滚动重复：若上一行是当前行的前缀，则用当前行替换上一行
dedup = []
for s in lines:
    if dedup and s.startswith(dedup[-1]):
        dedup[-1] = s
    elif dedup and dedup[-1].startswith(s):
        continue                                  # 当前行被上一行包含，丢弃
    else:
        dedup.append(s)

# 完全相邻重复也去掉
final = []
for s in dedup:
    if final and final[-1] == s: continue
    final.append(s)

body = '\n'.join(final)
# 轻度并句：按中文句末标点分段（保守，不新增标点）
body = re.sub(r'([。！？…])\s*', r'\1\n\n', body)

header = (f"# {title} · AI字幕清洗版\n"
          f"> ⚠️ 来源：B站 AI 自动字幕，**低可信度、未人工校对**。\n"
          f"> ⚠️ 仅供表达风格/节奏/话题分析使用；其中任何\"原话/金句/数字/人名/产品名\"都不得当作准确引用，须另行核对权威文本。\n"
          f"> 原始文件：{inp.split('/')[-1]}\n\n")

open(outp, 'w', encoding='utf-8').write(header + body + '\n')
print("done:", outp, "| 汉字:", len(re.findall(r'[一-鿿]', body)))
```

## 6. 交付校验（执行完请回报）
- 列出生成的所有 `.md` 文件名 + 每个的汉字数。
- 抽查任意一场，头 20 行是否干净连续、无时间戳、无滚动重复。
- 确认头部警告块已就位。

## 7. 交付后
把清洗好的 `.md` 放进 `transcripts/` 即可，上游会自行接手分析。**不需要**你做风格分析、总结或提炼——你的任务只到"干净文本"为止。
