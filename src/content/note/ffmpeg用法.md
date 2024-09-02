---
pubDatetime: 2024-05-31 11:02:16
title: ffmpeg用法
slug: ffmpeg用法
tags:
- "工具"
---

```shell  
# 1. 无损剪切视频片段 -to 指定结束时间点  -t 指定剪切时长  
ffmpeg  -i input.mp4 -ss 01:10 -to 02:10 -codec copy output.mp4  
# 视频拆分  -t 前1分钟 0：00 - 1：00  剩下的 从01：00 到结尾 part。mp4  
ffmpeg -i input.mp4 -t 01:00 part1.mp4 -ss 01:00 part2.mp4  
  
# 2. 合并两个视频  
ffmpeg -i video1.mp4 -i video2.mp4 -filter_complex "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1" -vsync vfr output.mp4  
  
# 2. 视频变速  两倍速 但是帧率不变 要想不丢失帧率 增加 原来30帧变成60帧   -r 60    
ffmpeg -i input.mp4 -vf "setpts=0.5*PTS" output.mp4  
# 变慢  
ffmpeg -i input.mp4 -vf "setpts=2*PTS,minterpolate='mi_mode=mci:mc_mode=aobmc:vsbmc=1:fps=60'" output.mp4  
  
# 3. 视频剪切  
ffmpeg -i 22.mp4 -vf "scale=iw/2:ih/2" 33.mp4  
  
# 4. 视频叠加 将视频放在左上角  
ffmpeg -i video.mp4  -i overlay.mp4 -filter_complex [0][1]overlay=x=0:y=0 output.mp4  
  
# 5. 视频添加音频 淡出效果  
ffmpeg -i video.mp4 -i audio.mp3 -af "afade=out:st=10:d=2" -map 0:v -map 1:a -c:v copy -shortest output.mp4  
  
# 6. 图片转视频  
  
ffmpeg -loop 1 -t 3 -framerate 60 -i image1.jpg -loop 1 -t 3 -framerate 60 -i image2.jpg -loop 1 -t 3 -framerate 60 -i image3.jpg -filter_complex "[0][1]xfade=transition=circleopen:duration=1:offset=2[f0]; [f0][2]xfade=transition=circleopen:duration=1:offset=4" -c:v libx264 -pix_fmt yuv420p output.mp4  
  
# 7. 增加水印并且限定时间  
  
ffmpeg -i input.mp4 -vf "drawtext=text='日照香炉生紫烟':fontfile=font.ttf:fontcolor=white@0.9:fontsize=48:x=(W-tw)/2:y=(H-th)/2:enable='between(t,0,2)',drawtext=text='日照香炉生紫烟':fontfile=font.ttf:fontcolor=white@0.9:fontsize=48:x=30:y=30:enable='gt(t,2)'" output.mp4  
  
  
  
查看视频编码信息  
  
ffprobe -show_streams -select_streams v -print_format json  
```