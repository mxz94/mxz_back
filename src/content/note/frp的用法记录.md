---
pubDatetime: 2024-11-06 11:40:55
title: frp的用法记录
slug: frp的用法记录
tags:
- "工具"
---

1. 下载最新版本  
``` cmd  
wget https://github.com/fatedier/frp/releases/download/v0.61.0/frp_0.61.0_linux_arm64.tar.gz  
  
tar -zxvf frp_0.61.0_linux_arm64.tar.gz  
  
  
```  
2. 修改服务端配置  
  
``` shell  
  
bindPort = 7000 #{必选} 客户端与该端口建立连接  
log.to = "./www/server/frp_0.60.0_linux_amd64/frps.log" #{可选} 日志配置， 通过打印的方式输出日志  
log.level="info"  
log.maxDays=3  
vhostHTTPPort = 7070 #{可选} http代理需要，当访问该端口时跳到对应本地frpc代理  
vhostHTTPSPort = 7443 #{可选} https代理需要，当访问该端口时跳到对应本地frpc代理  
transport.tcpMux = true #tcp流多路复用（优化传输，客户端与服务端同时配置才有效）  
   
#身份验证  
   
auth.method = "token" #{可选}身份验证方式  
auth.token = "a1bcdefgGHSDSAFDXFW324324321313U90809" #token设置密码，用于通过身份验证创建连接  
   
#frp服务仪表板配置  
   
webServer.port = 7077 #{自行修改端口}  
webServer.addr = "0.0.0.0" #公网ip或者0.0.0.0或者域名  
webServer.user = "admin" #登录用户名{自行修改}  
webServer.password = "qq741852" #登录密码{自行修改}  
  
# 使用的域名(将一级域名替换yourdomain.com，就是你购买的域名)  
subDomainHost = "malanxi.top"  
  
  
```  
3. 设置开机启动  
```  
vim /etc/systemd/system/frps.service  
  
[Unit]  
Description=FRP Server  
   
[Service]  
Type=simple  
ExecStart=/www/server/frp_0.60.0_linux_amd64/frps -c /www/server/frp_0.60.0_linux_amd64/frps.toml  
   
[Install]  
WantedBy=multi-user.target  
  
  
  
# 启动frp  
systemctl start frps  
# 停止frp  
systemctl stop frps  
# 重启frp  
systemctl restart frps  
# 查看frp状态  
systemctl status frps  
  
systemctl enable frps  
```  
  
4. nginx 域名配置  
```nginx  
  
server {  
    listen 80;  
    server_name immich.malanxi.top qb.malanxi.top;  
    listen 443 ssl http2 ;  
    sendfile on;  
    # include /www/server/panel/vhost/nginx/common.conf;  
    # allow large file uploads  
    client_max_body_size 50000M;  
    include /www/server/panel/vhost/nginx/cert/common.conf;  
    # Set headers  
    proxy_set_header Host              $http_host;  
    proxy_set_header X-Real-IP         $remote_addr;  
    proxy_set_header X-Forwarded-For   $proxy_add_x_forwarded_for;  
    proxy_set_header X-Forwarded-Proto $scheme;  
  
    # enable websockets: http://nginx.org/en/docs/http/websocket.html  
    proxy_http_version 1.1;  
    proxy_set_header   Upgrade    $http_upgrade;  
    proxy_set_header   Connection "upgrade";  
    proxy_redirect     off;  
  
    # set timeout  
    proxy_read_timeout 600s;  
    proxy_send_timeout 600s;  
    send_timeout       600s;  
      
    # gzip on;  
    # gzip_types text/plain text/css application/json application/javascript text/xml application/xml application/xml+rss text/javascript;  
    # gzip_vary on;  
    # gzip_min_length 1000;  # 只压缩大于 1000 字节的内容  
    # gzip_comp_level 5;  # 压缩级别，0-9，推荐 4-6  
  
      location /api/assets/ {  
        proxy_cache cache_one;  # 启用缓存  
        proxy_cache_key "$scheme$host$request_uri";  # 定义缓存的key  
        proxy_cache_valid 200 10m;  # 200 响应缓存 10 分钟  
        proxy_cache_valid 404 1m;    # 404 响应缓存 1 分钟  
        proxy_cache_valid any 1d;    # 其他响应缓存 1 天  
        proxy_cache_bypass $http_cache_control;  # 根据 Cache-Control 请求头绕过缓存  
  
        # 添加 X-Cache-Status 响应头  
        add_header X-Cache-Status $upstream_cache_status always;  
  
        # 代理设置  
        proxy_pass http://127.0.0.1:7070;  # 代理到后端服务  
        proxy_set_header Host $host;         # 设置请求头  
        proxy_set_header X-Real-IP $remote_addr;  # 真实 IP  
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;  # 转发 IP  
        proxy_set_header X-Forwarded-Proto $scheme;  # 请求协议  
  
        # 超时设置  
        proxy_connect_timeout 60;  
        proxy_read_timeout 60;  
        proxy_send_timeout 60;  
  
        # 缓冲设置  
        proxy_buffer_size 32k;  
        proxy_buffers 4 64k;  
        proxy_busy_buffers_size 128k;  
        proxy_temp_file_write_size 128k;  
  
        # 当发生错误时，继续请求下一个上游服务器  
        proxy_next_upstream error timeout invalid_header http_500 http_503 http_404;  
    }  
  
    location / {  
        proxy_pass http://127.0.0.1:7070;  
    }  
      
      
}  
server {  
    listen 80;  
    server_name frp.malanxi.top;  
    listen 443 ssl http2 ;  
    default_type application/octet-stream;  
    sendfile on;  
    keepalive_timeout 65;  
    index index.php index.html index.htm default.php default.htm default.html;  
    root /www/wwwroot;  
    include /www/server/panel/vhost/nginx/cert/common.conf;  
      
    location / {  
        proxy_pass http://127.0.0.1:7077;  
        proxy_set_header    Host            $host:80;  
        proxy_set_header    X-Real-IP       $remote_addr;  
        proxy_set_header    X-Forwarded-For $proxy_add_x_forwarded_for;  
        proxy_hide_header   X-Powered-By;  
    }  
}  
  
```  
  
5. 配置客户端  frpc.toml  
```  
serverAddr = "服务器ip" #[必选]服务器ip地址/域名  
serverPort = 7000 # [必选] 要连接的 frps 端口  
auth.token = "ab22cdefgGHSDSAFDXFW324324321313U90809" #与服务端校验的令牌（需一致）  
transport.tcpMux = false #tcp流多路复用（优化传输，客户端与服务端同时配置才有效）  
   
[[proxies]]  
name = "web" # 代理名称(随便填)  
type = "http" # 代理类型  
localIP = "127.0.0.1" # 代理地址, 要转发到哪个地址  
localPort = 2283 # 代理端口, 要转发到哪个端口  
#remotePort = 2283 # 远程端口(和远程 frps 哪个端口绑定在一起, 访问对应端口将使用该代理)  
subdomain="immich"  
transport.useCompression = true  
  
  
[[proxies]]  
name = "qb" # 代理名称(随便填)  
type = "http" # 代理类型  
localIP = "127.0.0.1" # 代理地址, 要转发到哪个地址  
localPort = 8081 # 代理端口, 要转发到哪个端口  
subdomain="qb"  
transport.useCompression = true  
```  
7.  利用 nssm.exe  设置 frpc 开机启动  
```  
文件夹下创建start.bat    
  
frpc.exe -c frpc.toml  
  
nssm.exe install frpc  
  
Application Path：D:\frpc\start.bat    
Startup directory：D:\frpc  
Arguments：  
  
或者   
  
Application Path：D:\frpc\frpc.exe  
Startup directory：D:\frpc  
Arguments： -c D:\frpc\frpc.toml  
```