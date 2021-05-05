### 使用方法

```angular2html
cd /root

docker pull redis


echo '#! /bin/sh \
cd /root/word_cloud_bot && python3 main.py >> output 2>&1 &
tail -f /dev/null' > /root/entrypoint.sh

wget -O /root/Dockerfile https://github.com/devourbots/word_cloud_bot/raw/master/Dockerfile

vi /root/Dockerfile

在第六行修改你的机器人TOKEN

docker build . -t world_cloud_bot:latest

docker run -d -p 6379:6379 redis:latest

docker run -d --net=host world_cloud_bot:latest
```