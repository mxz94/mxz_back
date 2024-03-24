---
pubDatetime: 2024-03-15 17:19:02
title: nginx
slug: nginx
tags:

- "计算机"

---

正向代理:  国内访问国外就需要代理服务器 隐藏客户端真实ip
反向代理： 一个接待对应多个服务器  隐藏服务端真实ip  负载均衡

nginx

https://www.nginx.cn/doc/


## 配置文件解读

## 日志调试

    debug_conection  指定ip   

    仅记录某个ip报错

    log_format logstash_json '{}'  json格式


location指令
=  用于特定匹配
~  正则区分大小写
~* 正则不区分大小写
^~

proxy_pass 反向代理

## 负载均衡：
upstream myserver {
<!-- 权重 -->
ip_hash;
server  ip:8081 weight=10;
server  ip2:8081 backup;
}
ip_hash  根据请求ip hash 访问固定一个客户端
least_conn 最少链接数
fair;  按招后台响应时间分配
backup 预留备份服务器
max_fails  请求失败次数
fail_timeout  请求失败达到次数后， 暂停服务时间
location / {
proxy_pass  http://myserver
proxy_set_header host $host;
proxy_set_header X-Fowarded-For $remote_addr;
}


$args：这个变量等于请求行中的参数，同$query_string。
$is_args: 如果已经设置$args，则该变量的值为"?"，否则为""。
$content_length： 请求头中的Content-length字段。
$content_type： 请求头中的Content-Type字段。
$document_uri： 与$uri相同。
$document_root： 当前请求在root指令中指定的值。
$host： 请求主机头字段，否则为服务器名称。 服务端地址
$http_user_agent： 客户端agent信息。
$http_cookie： 客户端cookie信息。
$limit_rate： 这个变量可以限制连接速率。
$request_method： 客户端请求的动作，通常为GET或POST。
$remote_addr： 客户端的IP地址。
$remote_port： 客户端的端口。
$remote_user： 已经经过Auth Basic Module验证的用户名。
$request_body_file`: 客户端请求主体的临时文件名。
$request_uri: 请求的URI，带参数
$request_filename： 当前请求的文件路径，由root或alias指令与URI请求生成。
$scheme： 所用的协议，比如http或者是https，比如rewrite ^(.+)$ $scheme://example.com$1 redirect;。
$server_protocol： 请求使用的协议，通常是HTTP/1.0或HTTP/1.1。
$server_addr： 服务器地址，在完成一次系统调用后可以确定这个值。
$server_name： 服务器名称。
$server_port： 请求到达服务器的端口号。
$request_uri： 包含请求参数的原始URI，不包含主机名，如：/foo/bar.php?arg=baz，它无法修改。
$uri： 不带请求参数的当前URI，$uri不包含主机名，如/foo/bar.html可能和最初的值有不同，比如经过重定向之类的。它可以通过内部重定向，或者使用index指令进行修改。不包括协议和主机名，例如/foo/bar.html。
$arg_mxz  取query值

限流
令牌桶 允许突发流量

limit_req_zone  限制单位时间内的请求数， 漏桶算法  不允许突发流量

http {
limit_req_zone 192.168.1.1 zone=myLimit:10m rate=5r/s;
}

server {
location / {
limit_req zone=myLimit;
rewrite / http://www.baidu.com permanent;
}
}
限制 1s 内访问 5 次
突发流量限制访问频率    limit_req zone=myLimit burst=20 nodelay; 特事特办

控制冰法连接数

limit_conn_zone $binary_remote_addr zone=perip:10m;
limit_conn_zone $server_name zone=perserver:10m;

server {
...
limit_conn perip 10;
limit_conn perserver 100;
}
limit_conn perip 10 作用的key 是 $binary_remote_addr，表示限制单个IP同时最多能持有10个连接。

limit_conn perserver 100 作用的key是 $server_name，表示虚拟主机(server) 同时能处理并发连接的总数。
##定义白名单ip列表变量
geo $limit {
default 1;
10.0.0.0/8 0;
192.168.0.0/10 0;
81.56.0.35 0;
}

map $limit $limit_key {
0 "";
1 $binary_remote_addr;
}
# 正常限流设置
limit_req_zone $limit_key zone=myRateLimit:10m rate=10r/s;


server {
...
limit_conn perip 10;
limit_conn perserver 100;
}

limit_req_conn  限制同一时间连接数，即并发限制。


location /hello/ {

    proxy_pass http://server1
}

proxy_pass http://server1    会访问到 http://server1/hello/
proxy_pass http://server2/   会访问到  http://server2

return 状态码

rewrite

为什么要用单线程？

采用单线程来异步非阻塞处理请求（管理员可以配置Nginx主进程的工作进程的数量），不会为每个请求分配cpu和内存资源，节省了大量资源，同时也减少了大量的CPU的上下文切换，所以才使得Nginx支持更高的并发。

简单过程：

主程序 Master process 启动后，通过一个 for 循环来 接收 和 处理外部信号 ；

主进程通过 fork() 函数产生 worker 子进程 ，每个子进程执行一个 for循环来实现Nginx服务器对事件的接收和处理 。

详细过程：

1、Nginx 在启动后，会有一个 master 进程和多个相互独立的 worker 进程。
2、master 接收来自外界的信号，先建立好需要 listen 的 socket（listenfd） 之后，然后再 fork 出多个 worker 进程，然后向各worker进程发送信号，每个进程都有可能来处理这个连接。
3、所有 worker 进程的 listenfd 会在新连接到来时变得可读 ，为保证只有一个进程处理该连接，所有 worker 进程在注册 listenfd 读事件前抢占 accept_mutex ，抢到互斥锁的那个进程注册 listenfd 读事件 ，在读事件里调用 accept 接受该连接。
4、当一个 worker 进程在 accept 这个连接之后，就开始读取请求、解析请求、处理请求，产生数据后，再返回给客户端 ，最后才断开连接。

Nginx 不这样，每进来一个 request ，会有一个 worker 进程去处理。但不是全程的处理，处理到什么程度呢？处理到可能发生阻塞的地方，比如向上游（后端）服务器转发 request ，并等待请求返回。那么，这个处理的 worker 不会这么傻等着，他会在发送完请求后，注册一个事件：如果 upstream 返回了，告诉我一声，我再接着干。于是他就休息去了。此时，如果再有 request 进来，他就可以很快再按这种方式处理。而一旦上游服务器返回了，就会触发这个事件，worker 才会来接手，这个 request 才会接着往下走。

这就是为什么说，Nginx 基于事件模型。

由于 web server 的工作性质决定了每个 request 的大部份生命都是在网络传输中，实际上花费在 server 机器上的时间片不多。这是几个进程就解决高并发的秘密所在。即：

webserver 刚好属于网络 IO 密集型应用，不算是计算密集型。

异步，非阻塞，使用 epoll ，和大量细节处的优化。也正是 Nginx 之所以然的技术基石。

Nginx: 采用单线程来异步非阻塞处理请求（管理员可以配置 Nginx 主进程的工作进程的数量）(epoll)，不会为每个请求分配 cpu 和内存资源，节省了大量资源，同时也减少了大量的 CPU 的上下文切换。所以才使得 Nginx 支持更高的并发。

##### nginx 安装

```bash
  wget http://nginx.org/download/nginx-1.16.0.tar.gz
  tar -xvf nginx-1.16.0.tar.gz
  whereis vim  #找出vim位置
  sudo cp -r contrib/vim/* /etc/vim   # vim高亮配置
```

查看nginx文件
![](https://raw.githubusercontent.com/mxz1994/note/master/20190828205606.png)

安装

```bash
sudo apt-get  install  build-essential   # 安装gcc编译工具
sudo apt-get install libpcre3 libpcre3-dev
sudo apt-get install openssl libssl-dev
sudo apt-get install zlib1g-dev
./configure --prefix=/home/mxz/nginx
make
sudo make install 
```

##### nginx命令行

```conf
nginx -s stop ：快速关闭Nginx，可能不保存相关信息，并迅速终止web服务。
nginx -s quit ：平稳关闭Nginx，保存相关信息，有安排的结束web服务。
nginx -s reload ：因改变了Nginx相关配置，需要重新加载配置而重载。
nginx -s reopen ：重新打开日志文件。
nginx -c filename ：为 Nginx 指定一个配置文件，来代替缺省的。
nginx -t ：不运行，而仅仅测试配置文件。nginx 将检查配置文件的语法的正确性，并尝试打开配置文件中所引用到的文件。
nginx -v：显示 nginx 的版本。
nginx -V：显示 nginx 的版本，编译器版本和配置参数。
```

::: alert-danger
执行 nginx -s reload 可能会报
\[error\] invalid PID number "" in "/home/mxz/nginx/logs/nginx.pid"

sudo ./nginx -c ~/nginx/conf/nginx.conf 解决
:::

```
ps -ef | grep nginx  查看运行
```

#### nginx 1

##### location

| 模式        | 含义       | 例子  |
| --------- | -------- | --- |
| =/uri     | 精确匹配     |     |
| ^~/uri    | 前缀匹配     |     |
| ~pattern  | 开头区分大小写  |     |
| ~*pattern | 开头不区分大小写 |     |
| /uri      |          |     |
| /         | default  |     |

常用

```conf
 location	=	/	{
     proxy_pass	http://tomcat:8080/index
     }
#	第二个必选规则是处理静态文件请求，这是	nginx	作为	http	服务器的强项 #	有两种配置模式，目录匹配或后缀匹配，任选其一或搭配使用 
location	^~	/static/	{	
    root	/webroot/static/; 
    } 
    
location	~*	\.(gif|jpg|jpeg|png|css|js|ico)$	{		
    root	/webroot/res/;
    }
#	第三个规则就是通用规则，用来转发动态请求到后端应用服务器 #	非静态文件请求就默认是动态请求，自己根据实际把握 #	毕竟目前的一些框架的流行，带.php、.jsp后缀的情况很少了 
location	/	{	
    proxy_pass	http://tomcat:8080/ 
    }
```

##### 缓存配置

#### nginx 2

##### nginx 升级

当升级nginx 时 只需将编译后的 sbin 文件copy过来
kill -USR2 nginx进程号 平滑的过度
旧版本Nginx主进程接收到-USR2信号，将重命名它的.pid文件为.oldbin，然后执行新版本的Nginx可执行程序，依次启动新版本的主进程和工作进程
并且老的master 进程不会关掉,方便我们回退
kill -QUIT 旧版本的Nginx主进程号

###### 日志切割

备份 access.log
nginx -s reopen 会重新生成日志
可以制作定时任务 按天日志分割

```
crontab -l
``````bash
#!/bin/bash
LOGS_PATH=/home/mxz/nginx/logs/history
CUR_LOGS_PATH=/home/mxz/nginx/logs
YESTERDAY=${date -d "yesterday" +%Y-%m-%d}
mv ${CUR_LOGS_PATH}/access.log ${LOGS_PATH}/access_${YESTERDAY}.log
#向Nginx 主进程发送URSR1信号. USR1 信号是重新打开日志文件
kill -USR1 $(cat /home/mxz/nginx/logs/nginx.pid)
```

##### nginx.conf

nginx压缩配置 对cpu损耗 传输效率提高
![](https://raw.githubusercontent.com/mxz1994/note/master/20190828205632.png)

代理服务
启动 nginx服务1 设定

```conf
    server {
        listen 127.0.0.1:8080;
        server_name mxz.com;

        access_log logs/mxz.access.log main;

        location / {
            alias dlib/;
            autoindex on; #访问/url 显示目录文件
            set $limit_rate 1k; #限制某些大文件的访问速度
        }
    }
```

反向代理服务器

```conf
   # cache 设置
    proxy_cache_path /tmp/nginxcache levels=1:2 keys_zone=my_cache:10m max_size=10g
                inactive=60m use_temp_path=off;

    upstream local {
        server 127.0.0.1:8080;
    }
    
    server {
        listen 80;
        server_name mxz.com;

        access_log logs/mxz.access.log main;

        location / {
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;

            proxy_cache_key $host$uri$is_args$args;
            proxy_cache_valid 200 304 302 1d;
            proxy_pass http://local;
        }
    }
```

##### 分析Access.log

1.安装 sudo apt install goaccess

```
goaccess mxz.access.log -o ../html/report.html --real-time-html --time-format='%H:%M:%S' --date-format='%d/%b/%Y' --log-format=COMBINED

```

##### 使用免费SSL证书实现一个HTTPS站点

```
添加模块动态升级
./configure --prefix=/usr/local/nginx --with-http_ssl_module

sudo apt-get install python-certbot-nginx

sudo certbot --nginx --nginx-server-root=/home/mxz/nginx/conf/ -d mxz.com
```

##### 使用openResty

```
wget https://openresty.org/download/openresty-1.15.8.1.tar.gz
./configure --prefix=/home/mxz/openresty
make
suido make install      #编译安装
```

配置nginx.conf 使用lua脚本
![](https://raw.githubusercontent.com/mxz1994/note/master/20190828205650.png)

```conf
#运行用户
#user somebody;

#启动进程,通常设置成和cpu的数量相等
worker_processes  1;

#全局错误日志
error_log  D:/Tools/nginx-1.10.1/logs/error.log;
error_log  D:/Tools/nginx-1.10.1/logs/notice.log  notice;
error_log  D:/Tools/nginx-1.10.1/logs/info.log  info;

#PID文件，记录当前启动的nginx的进程ID
pid        D:/Tools/nginx-1.10.1/logs/nginx.pid;

#工作模式及连接数上限
events {
   worker_connections 1024;    #单个后台worker process进程的最大并发链接数
}

#设定http服务器，利用它的反向代理功能提供负载均衡支持
http {
   #设定mime类型(邮件支持类型),类型由mime.types文件定义
   include       D:/Tools/nginx-1.10.1/conf/mime.types;
   default_type  application/octet-stream;
   
   #设定日志
   log_format  main  '[$remote_addr] - [$remote_user] [$time_local] "$request" '
                     '$status $body_bytes_sent "$http_referer" '
                     '"$http_user_agent" "$http_x_forwarded_for"';
                     
   access_log    D:/Tools/nginx-1.10.1/logs/access.log main;
   rewrite_log     on;
   
   #sendfile 指令指定 nginx 是否调用 sendfile 函数（zero copy 方式）来输出文件，对于普通应用，
   #必须设为 on,如果用来进行下载等应用磁盘IO重负载应用，可设置为 off，以平衡磁盘与网络I/O处理速度，降低系统的uptime.
   sendfile        on;
   #tcp_nopush     on;

   #连接超时时间
   keepalive_timeout  120;
   tcp_nodelay        on;
   
   #gzip压缩开关
   #gzip  on;

   #设定实际的服务器列表 
   upstream zp_server1{
       server 127.0.0.1:8089;
   }

   #HTTP服务器
   server {
       #监听80端口，80端口是知名端口号，用于HTTP协议
       listen       80;
       
       #定义使用www.xx.com访问
       server_name  www.javastack.cn;
       
       #首页
       index index.html
       
       #指向webapp的目录
       root D:_WorkspaceProjectgithubzpSpringNotesspring-securityspring-shirosrcmainwebapp;
       
       #编码格式
       charset utf-8;
       
       #代理配置参数
       proxy_connect_timeout 180;
       proxy_send_timeout 180;
       proxy_read_timeout 180;
       proxy_set_header Host $host;
       proxy_set_header X-Forwarder-For $remote_addr;

       #反向代理的路径（和upstream绑定），location 后面设置映射的路径
       location / {
           proxy_pass http://zp_server1;
       } 

       #静态文件，nginx自己处理
       location ~ ^/(images|javascript|js|css|flash|media|static)/ {
           root D:_WorkspaceProjectgithubzpSpringNotesspring-securityspring-shirosrcmainwebappiews;
           #过期30天，静态文件不怎么更新，过期可以设大一点，如果频繁更新，则可以设置得小一点。
           expires 30d;
       }
   
       #设定查看Nginx状态的地址
       location /NginxStatus {
           stub_status           on;
           access_log            on;
           auth_basic            "NginxStatus";
           auth_basic_user_file  conf/htpasswd;
       }
   
       #禁止访问 .htxxx 文件
       location ~ /.ht {
           deny all;
       }
       
       #错误处理页面（可选择性配置）
       #error_page   404              /404.html;
       #error_page   500 502 503 504  /50x.html;
       #location = /50x.html {
       #    root   html;
       #}
   }
}

```

##### 负载均衡配置

```conf
   #设定负载均衡的服务器列表
   upstream load_balance_server {
       #weigth参数表示权值，权值越高被分配到的几率越大
       server 192.168.1.11:80   weight=5;
       server 192.168.1.12:80   weight=1;
       server 192.168.1.13:80   weight=6;
   }
```

##### 网站有多个webapp的配置

```conf
http {
   #此处省略一些基本配置
   
   upstream product_server{
       server www.mxz.com:8081;
   }
   
   upstream admin_server{
       server www.mxz.com:8082;
   }
   
   upstream finance_server{
       server www.mxz.com:8083;
   }

   server {
       #此处省略一些基本配置
       #默认指向product的server
       location / {
           proxy_pass http://product_server;
       }

       location /product/{
           proxy_pass http://product_server;
       }

       location /admin/ {
           proxy_pass http://admin_server;
       }
       
       location /finance/ {
           proxy_pass http://finance_server;
       }
   }
}
```

##### 获取uri参数

```conf
content_by_lua_block{
                local arg = ngx.req.get_uri_args()
                for k,v in pairs(arg) do
                    ngx.say("[GET] key:", k, "v:", v)
                end

                ngx.req.read_body() -- 解析body参数之前一定要先读取body
                local arg = ngx.req.get_post_args()
                for k,v in pairs(arg) do
                    ngx.say("[POST] key:", k, "v:", v)
                end
            }
```

> curl '127.0.0.1:6699/a?a=1&b=2%26' -d 'c=3&d=4%26'

##### 传递请求uri参数

##### nginx 设置错误级别

```
error_log		logs/error.log	error;				#	日志级别 
ngx.log(ngx.ERR,	"num:",	num)
```

网络日志输出 [lua-resty-logger-socket](https://github.com/cloudflare/lua-resty-logger-socket)
lua-resty-logger-socket 的目标是替代 Nginx 标准的 ngx\_http\_log_module 以非阻塞 IO 方式 推送 access log 到远程服务器上。对远程服务器的要求是支持 syslog-ng 的日志服务。

###### nginx 黑名单

```
#使用access阶段完成准入阶段处理
            access_by_lua_block {
                ngx.log(ngx.ERR, "common", ngx.var.remote_addr)
                local black_ips = {["127.0.0.1"]=true}

                local ip = ngx.var.remote_addr
                if true == black_ips[ip] then
                    ngx.exit(ngx.HTTP_FORBIDDEN)
                end
                ngx.var.limit_rate	=	1000
            }
```

##### 防止sql注入

