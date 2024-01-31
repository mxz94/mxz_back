---
pubDatetime: 2024-01-31 10:00:14
title: 利用WSA保存到Google相册
slug: 利用WSA保存到Google相册
tags:
  - "工具"
---

# 一. 利用WSA保存到google相册
1. [点击下载指定WSA](https://github.com/MustardChef/WSABuilds/releases), 这里我们直接下载X64系统的WSAonMagisk Run.bat 安装
2. 配置WSA, 高级设置，实验功能，设置共享文件夹, 开发人员模式开启， 下载[ADB工具](https://developer.android.com/tools/releases/platform-tools?hl=zh-cn) 到目录下, 执行指令 ```adb connect 127.0.0.1:58526 && adb shell "settings put global http_proxy `ip route list match 0 table all scope global | cut -F3`:7890"```, 取消代理指令 `adb shell settings put global http_proxy :0`
3. Magisk 的设置中打开 Zygyisk, 下载Lsposed模块本地安装LSPosed-v1.9.2-7024-zygisk-release.zip 进 Magisk, 打开mt文件管理器， 将 复制所有文件并覆盖从 /data/adb/modules_update/（您安装的模块）到 /data/adb/modules/（您安装的模块）, 删除 /data/adb/modules/（您安装的模块）/update  和 /data/adb/modules_update， 重启wsa maigsk， 安装lsposed.apk
4. 登录google playe 商店下载google 相册
5. 安装pixelify_gphotos_v4.1.apk,  lsposed 模块中开启, 指定针对应用
6. pixelify_gphotos 内设定设备类型 选择 [ Device to spoof ] 将机型改为 [ PixelXL ] ，选择下方的 [ Force Stop Google Photo ]

[附件地址](https://www.lanzv.com/ifwxc1mt4mdc)


# 二. 利用WSA抓包安卓软件

1. 安装WSA工具箱 将 charles 的 Help -> SSL Proxying -> Save Charles Root Certificat 证书
2. WSA工具箱 Android设置，选择安全->更多安全设置->加密与凭据->安装证书菜单，选择并安装Download目录的charles证书
3. 下载 Magisk 的MagiskTrustUserCerts模块压缩包，安装
4. 打开 charles，选择菜单Proxy -> SSL Proxying Settings...，勾选 Enable SSL Proxying，并添加新的 location，Host填*，Port填443
5. adb connect 127.0.0.1:58526 , adb shell settings put global http_proxy 192.168.x.x:8888
6. 删除代理的话 adb shell settings delete global http_proxy
   adb shell settings delete global global_http_proxy_host
   adb shell settings delete global global_http_proxy_port

