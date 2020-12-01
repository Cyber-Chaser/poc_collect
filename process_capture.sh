#!/bin/bash
# 参考来源：https://www.cnblogs.com/xiaozi/p/9561543.html
# 用于捕捉存活时间很短的异常进程，打印相关信息
i=1
while :
do
   tmp=`ps -ef|grep ping|grep -v grep|awk '{print $3}'` # $2是进程pid，$3是父进程pid
   #echo $tmp
   if test -z "$tmp"
   then
       ((i=i+1)) 
   else
       for pid in $tmp; do
          echo "PID: "${pid}
          result=`lsof -p $pid`
          echo "Process: "${result}
          #kill -9 $pid
       done
       break
   fi 
done
echo "Total number of times: "${i}
