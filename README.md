## 配置要求

内存：1G以上


## 安装方法

### 使用 Docker 安装
Docker官方安装地址：[点击访问](https://docs.docker.com/engine/install/)

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

## 使用方法

使用 `/start` 指令测试机器人与 Redis 数据库的连通情况

将机器人拉入群组，设置为管理员（不需要其他权限），设置完毕

### 将机器人设置为仅自己群组可用

如果您不想让别人使用你的机器人，那么可以将 func.py 文件中的
```angular2html
    # if chat_id not in ["1231242141"]:
    #     return
```
该段注释取消，并将自己的群组ID加入到列表中。

例如我两个的群组ID分别为：-127892174935、-471892571924

那么修改后为：
```angular2html
    if chat_id not in ["-127892174935", "-471892571924"]:
        return
```

