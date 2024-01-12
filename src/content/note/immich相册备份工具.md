---
pubDatetime: 2024-01-12 11:19:57
title: immich相册备份工具
slug: immich相册备份工具
tags:
  - "工具"
---

# immich相册备份工具

## 1. 安装
    
参考 [immich-docker 安装教程](https://immich.app/docs/install/docker-compose)
升级
```
docker compose pull && docker compose up -d
```

## 2. 备份

整个文件夹备份我用的是 Resilio Sync  
数据库备份及恢复参照[backup-and-restore](https://immich.app/docs/administration/backup-and-restore)  
windows 要执行这些指令需要做这些预备工作  
1. 下载 [GnuWin download | SourceForge.net](https://sourceforge.net/projects/gnuwin32/)
2. 加入path环境变量 
3. gun 目录下 增加 gunzip.bat
   ```shell
    @echo off
    gzip -d %1
    ```
备份指令需要到git cmd 窗口执行否则解压缩会有问题

## 3. 外网访问
    mxz


