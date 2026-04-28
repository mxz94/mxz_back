#!/bin/bash
#!/bin/sh
echo "======================= start deploy ===================================="

echo "获取pid"
PID=$(cat /www/wwwroot/storeroom-lan/record.pid)
echo $PID;
if [ ! -n "$PID" ]
then
    echo "no server pid alive":
else
    kill -9 $PID
   echo "kill server"
   sleep 2s
fi
echo "==================================stop ok!!!!!!!!!"
BUILD_ID=dontKillMe
source /etc/profile
nohup java -Xmx256M -Xms128M -jar /www/wwwroot/storeroom-lan/storeroom-lan-admin.jar  >/www/wwwroot/storeroom-lan/service-launcher.log 2>&1 &
echo $! >  /www/wwwroot/storeroom-lan/record.pid
echo "正在启动中"  
echo "启动环境：test" 
PID=$(cat /www/wwwroot/storeroom-lan/record.pid)
echo "新的进程pid =$PID"
if [ ! -n "$PID" ]
        then
        echo "no new pid"
        exit 1
fi
sleep 1s
CHECK_URL='http://127.0.0.1:8018/ok.html'
echo "wait check server start flag..................  http://127.0.0.1:8018/ok.html"

for((i=1;i<=10;i++));
do
        RESULT=$(curl -s $CHECK_URL)
        echo "server check $i times, result:"$RESULT
        if [ "$RESULT" == "success" ] ; then
                echo 'check server success, 完成.';
                #        cp /usr/local/products/lksq/lksq-server/server-1.0.0-SNAPSHOT.jar  /usr/local/products/lksq/lksq-server/bck/server-1.0.0-SNAPSHOTbck.jar
                #	 echo "jar包复制完成"
        	exit 0
    	fi
 	sleep 5s
done

exit 1