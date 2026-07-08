import whisper, sys, os

def fmt(seconds):
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    ms = int((seconds % 1) * 1000)
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"

video = sys.argv[1]
base = os.path.splitext(video)[0]
srt = base + ".srt"

print("Loading large-v3...")
model = whisper.load_model("large-v3")

print(f"Transcribing: {os.path.basename(video)}")
result = model.transcribe(video, language="zh", task="transcribe", verbose=True)

with open(srt, "w", encoding="utf-8") as f:
    for i, seg in enumerate(result["segments"], 1):
        f.write(f"{i}\n")
        f.write(f"{fmt(seg['start'])} --> {fmt(seg['end'])}\n")
        f.write(f"{seg['text'].strip()}\n\n")

print(f"Done: {srt}")
