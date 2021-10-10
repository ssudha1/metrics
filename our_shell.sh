#!/bin/sh
mkdir /data/local/memory_dump
#echo "PKG NAME IN OUR_SHELL"
#echo $pkg
#pid=$(ps -A | grep "$pkg" | awk '{print $2}')
#echo "PID"
#echo $pid
mv /data/local/memfetch /data/local/memory_dump/memfetch
cd /data/local/memory_dump
chmod 777 memfetch
./memfetch $1
exit
