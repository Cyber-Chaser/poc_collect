#!/bin/bash
i=1
while :
do
   tmp=`ps -ef|grep ping|grep -v grep|awk '{print $3}'`
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
