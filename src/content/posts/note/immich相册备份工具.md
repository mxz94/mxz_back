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

Win + X  + A

back  
```
docker exec -t immich_postgres pg_dumpall --clean --if-exists --username=postgres > "\path\to\backup\dump.sql"
```

restore  
```
docker compose down -v  # CAUTION! Deletes all Immich data to start from scratch.
docker compose pull     # Update to latest version of Immich (if desired)
docker compose create   # Create Docker containers for Immich apps without running them.
docker start immich_postgres    # Start Postgres server
sleep 10    # Wait for Postgres server to start up
gc "C:\path\to\backup\dump.sql" | docker exec -i immich_postgres psql --username=postgres    # Restore Backup
docker compose up -d    # Start remainder of Immich apps
```

## 3. 外网访问
    mxz


