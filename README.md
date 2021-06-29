## 当前版本

v2.4

## 更新维护日志

[更新维护日志](https://github.com/devourbots/word_cloud_bot/wiki/%E6%9B%B4%E6%96%B0%E7%BB%B4%E6%8A%A4%E6%97%A5%E5%BF%97)

## 有问题请加群组反馈
Telegram 交流反馈群组 [点击加入](https://t.me/devourbots)

## 演示

![xq9iR.png](https://s3.jpg.cm/2021/05/05/xq9iR.png)

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

# 使用命令查看所有时区
timedatectl list-timezones

找到您所在的时区，例如：
上海 Asia/Shanghai
纽约 America/New_York

# 编辑Dockerfile
vi /root/Dockerfile

# 在第7行修改服务器所属时区，原文件为：
RUN ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime
修改为纽约当地时，修改后：
RUN ln -s /usr/share/zoneinfo/America/New_York /etc/localtime

# 在第10行修改你的机器人TOKEN
修改后：
RUN sed -i '1c TOKEN = "1749418611:AAGcpouQ4EWSDITLQXFozHjMgT_-MsVSmDM"' /root/word_cloud_bot/config.py


# 根据 Dockerfile 创建镜像
docker build . -t world_cloud_bot:latest

# 运行 Redis 镜像，此步在前
docker run -d -p 6379:6379 redis:latest

# 注意！！！
请关闭服务器 6379 端口的外网访问权限！！！如果您的主机提供商提供了安全组策略（阿里云、腾讯云、AWS等等），可以在控制台关闭6379端口。
如果您的主机商不支持自定义安全组，请根据您的发行版系统自行搜索防火墙关闭端口的方式，检测方式在下方。
不要抱有侥幸心理！不要抱有侥幸心理！不要抱有侥幸心理！

# 运行 机器人，此步在后
docker run -d --net=host world_cloud_bot:latest
```

[端口检测工具](http://tool.chinaz.com/port/), 请确保 6379 是关闭状态

![xlu8H.png](https://s3.jpg.cm/2021/05/06/xlu8H.png)

## 使用方法

使用 `/start` 指令测试机器人与 Redis 数据库的连通情况

使用 `/rank` 指令主动触发词云任务，在 config.py 里可以设置每个群组每小时主动触发次数的限制

将机器人拉入群组，设置为管理员（受机器人API所限，只有授予管理员权限后，机器人才能接收到所有用户的普通聊天文本，此机器人不需要其他权限，您可以将所有权限关闭）

所有聊天内容每天定时清理，仅用于本地分词，无其他任何用途

![xqyvt.png](https://s3.jpg.cm/2021/05/05/xqyvt.png)

### 将机器人设置为仅自己群组可用

如何编辑 Docker 容器中的文件请自行 Google

如果您不想让别人使用你的机器人，那么可以将 `config.py` 文件中的 `EXCLUSIVE_MODE = 0`改为 `EXCLUSIVE_MODE = 1`

![DGbSy.png](https://s3.jpg.cm/2021/05/09/DGbSy.png)

编辑 `/root/word_cloud_bot/func.py`，在 94 行左右，将自己的 群组ID 加入到列表中。
这里的`EXCLUSIVE_MODE = 1`不要改动，注意区分！


例如我两个的群组ID分别为：-127892174935、-471892571924

那么修改后为：
```angular2html
if EXCLUSIVE_MODE == 1 and chat_id not in ["-127892174935", "-471892571924"]:
    print(chat_id + " 为未认证群组，取消入库")
    return
```

![DGHR5.png](https://s3.jpg.cm/2021/05/09/DGHR5.png)

### 设置 /rank 指令对普通用户开放

编辑 `/root/word_cloud_bot/config.py`， 将 `RANK_COMMAND_MODE = 1` 改为 `RANK_COMMAND_MODE = 0`

![DGJuC.png](https://s3.jpg.cm/2021/05/09/DGJuC.png)


### 信息推送密度

![xW3jh.png](https://s3.jpg.cm/2021/05/05/xW3jh.png)

默认分别会在当地时间 11:00、18:00、23:30 推送三次数据统计报告，并会在 23:59 清空当日统计数据，
如需更密集的数据推送，可以编辑 /root/word_cloud_bot/main.py ，按照示例格式自行增加，相关的 docker 技术操作不再赘述

