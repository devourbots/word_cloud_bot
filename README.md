## 使用方法

### 使用 Docker 安装
官方安装地址：[点击访问](https://docs.docker.com/engine/install/)

```angular2html
cd /root

# 拉取Redis镜像
docker pull redis

# 创建 entrypoint.sh 入口文件
echo '#! /bin/sh \
cd /root/word_cloud_bot && python3 main.py >> output 2>&1 &
tail -f /dev/null' > /root/entrypoint.sh

# 创建 Dockerfile
wget -O /root/Dockerfile https://github.com/devourbots/word_cloud_bot/raw/master/Dockerfile

# 修改机器人TOKEN
vi /root/Dockerfile

在第六行修改你的机器人TOKEN

# 根据 Dockerfile 创建镜像
docker build . -t world_cloud_bot:latest

# 运行 Redis 镜像，此步在前
docker run -d -p 6379:6379 redis:latest

# 运行 机器人，此步在后
docker run -d --net=host world_cloud_bot:latest
```