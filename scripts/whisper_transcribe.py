 """
 罗永浩发布会 ASR 转录脚本
 用法: python whisper_transcribe.py <视频文件路径>
 输出: 同目录下生成同名 .srt 字幕文件

 依赖: pip install openai-whisper
 GPU: RTX 4060 8GB 可跑 large-v3，一场 2h 发布会约 10-15 分钟
 """
 import sys
 import os
 import whisper

 MODEL = "large-v3"  # 中文效果最好的开源模型

 def main():
     if len(sys.argv) < 2:
         print("用法: python whisper_transcribe.py <视频文件>")
         print("示例: python whisper_transcribe.py \"E:\\锤子发布会_T1.mp4\"")
         sys.exit(1)
     
     video_path = sys.argv[1]
     if not os.path.exists(video_path):
         print(f"文件不存在: {video_path}")
         sys.exit(1)
     
     base = os.path.splitext(video_path)[0]
     srt_path = base + ".srt"
     
     print(f"加载模型 {MODEL}...")
     model = whisper.load_model(MODEL)
     
     print(f"开始转录: {video_path}")
     result = model.transcribe(
         video_path,
         language="zh",
         task="transcribe",
         verbose=True,
     )
     
     # 输出 SRT 字幕
     with open(srt_path, "w", encoding="utf-8") as f:
         for i, segment in enumerate(result["segments"], 1):
             start = segment["start"]
             end = segment["end"]
             text = segment["text"].strip()
             
             def fmt(seconds):
                 h = int(seconds // 3600)
                 m = int((seconds % 3600) // 60)
                 s = int(seconds % 60)
                 ms = int((seconds % 1) * 1000)
                 return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
             
             f.write(f"{i}\n")
             f.write(f"{fmt(start)} --> {fmt(end)}\n")
             f.write(f"{text}\n\n")
     
     print(f"完成! 字幕已保存: {srt_path}")

 if __name__ == "__main__":
     main()
