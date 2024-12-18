---
pubDatetime: 2024-03-15 17:19:53
title: linux
slug: linux
tags:

- "计算机"

---

linux


# linux

### 查看当前服务

systemctl status httpd

查看全局日志
journalctl -f -l -u httpd -u mariadb --since -300

### 批量杀死进程

```
ps aux | grep nginx | cut -c 9-15| xargs kill -9

kubectl get pods -l com.qinsilk.app=ths |grep ths-| cut -c 1-20|xargs kubectl delete pods
```

1.  ps aux 查看所有进程的命令
2.  grep "common" 在前序命令查找到的进程中过滤出存在关键字 common 的进程
3.  cut -c 9-15 在前序命令过滤出的进程中截取输出行的第 9 到 15 个字符，正好是进程 PID
4.  xargs 将前序命令得到的结果作为 kill -9 的参数

### 开机启动

修改~/.bashrc

### 任务后台运行

```
./nginx_reload.sh &
```

& 将命令 放入到作业队列中 `jobs -l` 查看

### 定时任务

### 循环任务

小技巧

```
#!/bin/bash
step=3
for((i=0;;i=(i+step)));do
    $(nginx -s reload)
    sleep $step
done
exit 0
```

### 定时监控

```
watch -d -n 1 '命令'
```

### 查找命令

#### locate

#### find

> find /home/ -name "*.txt"

#### grep

> grep -l 列出查找文件名 -on 显示搜索的关键字和行号
> grep -r 查找内容 路径
> grep -r admin /etc/
> grep 要搜索字符串 要搜索文件 --color
> sed -i "s/txt1/txt2/g" $(grep -rl txt1 ./*)

### 替换命令

### sed

> sed "s/my/Hao Chen's/g" pets.txt > hao_pets.txt 修改后新文件
> sed -i "s/my/Hao Chen's/g" pets.txt 修改旧文件
> sed 's/^/#/g' pets.txt 每一行最前面加点东西
> sed 's/$/ --- /g' pets.txt 在每一行最后面加点东西 /^#/ 以#开头 /}$
>
> KaTeX parse error: Expected group after '^' at position 33: …t 在每一行最后面加点东西 /^̲#/ 以#开头 /}
>
> / 以} 结尾
> <abc 以abc 为首的词
>
> # 注意其中的/fish/a，这意思是匹配到/fish/后就追加一行

$ sed "/fish/a This is my monkey, my monkey's name is wukong" my.conf

> 删除匹配行
> $ sed '/fish/d' my.txt

### cat

> cat > /test.txt <<EOF
> neirong
> EOF

### 解压缩指令 tar

#### 打包

> tar -czvf test.tar /etc/host* 将etc下以host开头的文件打包为test.tar
> tar -zxvf test.tar -c /usr 指定解压目录

### 配置文件

> vim ~/.profile
> source ~/.profile

### 管道符 |

### 拷贝传输文件

scp -r 目标 位置

### 显示磁盘大小

df -lh

### vim操作

vim /要查找的单词 n 向下继续查找
:%s/word1/word2/g 将Word1 替换为word2

### 快捷键

ctrl+u 删除一整行
ctrl+w 向前删除一个单词
alt+b alt+f 左右以单词为单位移动
ctrl+a ctrl+e 移至行首或行尾
ctrl+k 删除到行尾

### 别名alias s='' unalias

```
vi /etc/bashrc   source /etc/bashrc
alias svim='sudo vim'
alias c7='chmod 777'
alias cx='chmod +x'
alias ..="cd .."
alias ...="cd ..; cd .."
```

pstree -p

### 对比命令diff

通过使用 <(some command) 可以将输出视为文件。例如，对比本地文件 /etc/hosts 和一个远程文件

```
diff /etc/hosts <(ssh somehost cat /etc/hosts)
```

### tee

输出到文件

> ls -al | tee file.txt

查看连接你服务器 top10 用户端的 IP 地址：

```
netstat -nat | awk '{print $5}' | awk -F ':' '{print $1}' | sort | uniq -c | sort -rn | head -n 10
cat .bash_history | sort | uniq -c | sort -rn | head -n 10 

```

### awk

```
awk  动作名 文件名
top -h >> log

awk '{print $1, $4}'  log 截取第几列 $0 是整行
echo "1,2,3" | awk -F ',' '{print}'
NF 例数  NR 行数  $(NF-1) 倒数第一例
$ awk '$1=="Mem:" && $2=0' log  过滤数据
$ awk -F ':' '{if ($1 > "m") print $1; else print "---"}' demo.txt
```

### vim

```
vim -On file1 file2 ... 垂直分屏  o 水平分
ctrl hjkl 上下切换
```

### set

```
set -e   脚本中执行失败就会退出
```

### 快捷键

ctrl+w 删除最后一个单词
ctrl+u 删除整行

### 建立软链接

每个文件都有inode号码 stat 查看inode
硬链接 ，多个文件对应一个inode A 和B 都变
软链接 读取A导向B A为B的软链接
ln -s B.txt A.txt 创建软链接
ln 创建硬链接

tail -f 文件 动态监控文件
tail-10 查询文件后10行
more 显示百分比
less 分页查看

nohup
把它和 & 结合使用可以创建后台进程
nohup command &

### ssh

ssh -p 22 root@193.112.244.115 远程登录

### asciinema

终端录屏

> pip install asciinema
> apt-get install asciinema
> asciinema auth
> 使用asciinema rec进行录屏：
> ctrl+d退出录屏，回车则上传录制内容到网站，ctrl+c可以保存到本地
> https://asciinema.org/

删除镜像
docker rm -f `docker ps -a| grep ${projectName}|awk '{print $1}'`

docker rm -f `docker ps -a| grep Exited|awk '{print $1}'`

cd /var/jenkins_home/workspace/lzc/target/

docker images|grep none|awk '{print $3}'|xargs docker rmi

# 查看日志

cat filename | grep -C 5 '关键字' 　　(显示日志里匹配字串那行以及前后5行)
cat -n demo.txt|grep aa 查看第几行
more +1234 从第几行开始看

EOF 是 end of file 的缩写
<<EOF 开始

EOF 结束

< 输入重定向 <<追加

> 输出重定向

# 文件查找

which : 查看执行文件的位置。

whereis : 查看可执行文件位置和相关文件。

locate : 配合数据库缓存，快速查看文件的位置。

grep : 过滤匹配，他是一个文件搜索工具。

find : 可以根据条件查看文件。

nohup java -jar  aa.jar server.port

netstat -anp | grep duankou

ll /proc/{pid}/exe