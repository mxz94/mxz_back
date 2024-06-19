---
pubDatetime: 2024-03-15 17:19:02
title: nginx
slug: nginx
tags:

- "计算机"

---

正向代理:国内访问国外就需要代理服务器 隐藏客户端真实ip  
反向代理：一个接待对应多个服务器  隐藏服务端真实ip  负载均衡 nginx  

https://www.nginx.cn/doc/
## 配置文件解读

location

| 模式        | 含义       | 例子  |
| --------- | -------- | --- |
| =/uri     | 精确匹配     |     |
| ^~/uri    | 前缀匹配     |     |
| ~pattern  | 开头区分大小写  |     |
| ~*pattern | 开头不区分大小写 |     |
| /uri      |          |     |
| /         | default  |     |


```nginx configuration
# 负载均衡
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

# 代理
location / {
    proxy_pass  http://myserver
    proxy_set_header host $host;
    proxy_set_header X-Fowarded-For $remote_addr;
}

location /hello/ {
    proxy_pass http://server1;
}

proxy_pass http://server1    会访问到 http://server1/hello/
proxy_pass http://server2/   会访问到  http://server2

# 限流
# 令牌桶 允许突发流量

limit_req_zone  限制单位时间内的请求数， 漏桶算法  不允许突发流量

http {
    limit_req_zone 192.168.1.1 zone=myLimit:10m rate=5r/s;
}

# 限制 1s 内访问 5 次
# 突发流量限制访问频率    limit_req zone=myLimit burst=20 nodelay; 特事特办
server {
    listen       80;
    server_name  server.com;
    location / {
        limit_req zone=myLimit;
        rewrite / http://www.baidu.com permanent;
    }
}


# 控制冰法连接数
limit_conn_zone $binary_remote_addr zone=perip:10m;
limit_conn_zone $server_name zone=perserver:10m;

server {
...
limit_conn perip 10;
limit_conn perserver 100;
}
limit_conn perip 10 作用的key 是 $binary_remote_addr，表示限制单个IP同时最多能持有10个连接。

limit_conn perserver 100 作用的key是 $server_name，表示虚拟主机(server) 同时能处理并发连接的总数

# 正常限流设置
limit_req_zone $limit_key zone=myRateLimit:10m rate=10r/s;

server {
...
limit_conn perip 10;
limit_conn perserver 100;
}
limit_req_conn  限制同一时间连接数，即并发限制

```
**为什么要用单线程？**

采用单线程来异步非阻塞处理请求（管理员可以配置Nginx主进程的工作进程的数量），不会为每个请求分配cpu和内存资源，节省了大量资源，同时也减少了大量的CPU的上下文切换，所以才使得Nginx支持更高的并发。

**简单过程**：
主程序 Master process 启动后，通过一个 for 循环来 接收 和 处理外部信号; 主进程通过 fork() 函数产生 worker 子进程 ，每个子进程执行一个for循环来实现Nginx服务器对事件的接收和处理 。
Master  接收   Worker  处理
**详细过程**：
1. Nginx 在启动后，会有一个 master进程和多个相互独立的 worker 进程。
2. master 接收来自外界的信号，先建立好需要 listen 的 socket（listenfd） 之后，然后再 fork 出多个 worker 进程，然后向各worker进程发送信号，每个进程都有可能来处理这个连接。
3. 所有 worker 进程的 listenfd 会在新连接到来时变得可读 ，为保证只有一个进程处理该连接，所有 worker 进程在注册 listenfd 读事件前抢占 accept_mutex ，抢到互斥锁的那个进程注册 listenfd 读事件 ，在读事件里调用 accept 接受该连接。
4. 当一个 worker 进程在 accept 这个连接之后，就开始读取请求、解析请求、处理请求，产生数据后，再返回给客户端 ，最后才断开连接。

**为什么说，Nginx 基于事件模型:**  
每进来一个 request ，会有一个 worker 进程去处理。但**不是全程的处理**，处理到什么程度呢？**处理到可能发生阻塞的地方**，比如向上游（后端）服务器转发 request ，并等待请求返回。那么，这个处理的 worker 不会这么傻等着，**他会在发送完请求后，注册一个事件：如果 upstream 返回了，告诉我一声，我再接着干**。于是他就休息去了。此时，如果再有 request 进来，他就可以很快再按这种方式处理。而一旦上游服务器返回了，就会触发这个事件，worker 才会来接手，这个 request 才会接着往下走。 使用进程的好处：各个进程之间相互独立，不需要加锁
由于 web server 的工作性质决定了每个 request 的大部份生命都是在网络传输中，实际上花费在 server 机器上的时间片不多。这是几个进程就解决高并发的秘密所在。即： webserver 刚好属于网络 IO 密集型应用，不算是计算密集型。 

异步，非阻塞，使用 epoll ，和大量细节处的优化。也正是 Nginx 之所以然的技术基石。


## nginx命令行

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

```
ps -ef | grep nginx  查看运行
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

## 参数变量

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