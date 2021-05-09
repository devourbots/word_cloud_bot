#/bin/bash
#environment variable
source /etc/profile
#memory
while :
do
        bu=`free | awk 'NR==2{print $6}'`
        ca=`free | awk 'NR==2{print $7}'`
        us=`free | awk 'NR==2{print $3}'`
        to=`free | awk 'NR==2{print $2}'`
        mem=`expr "scale=2;($us-$bu-$ca)/$to" |bc -l | cut -d. -f2`
        if(($mem >= 90))
        then
        echo "restart"
        killall -9 python3
        cd /root/word_cloud_bot && python3 main.py >> output 2>&1 &
fi
        sleep 10
done