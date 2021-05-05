# encoding=utf-8
import re
import redis
import jieba
import jieba.posseg as pseg
import time  # 引入time模块
import wordcloud
# 导入imageio库中的imread函数，并用这个函数读取本地图片，作为词云形状图片
import imageio

# import datetime
# import threading
# import telegram
# from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
# from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler
# from config import TOKEN
# import sqlite3
# import time
# import os
# import importlib
# import requests
#
# bot = telegram.Bot(token=TOKEN)

pool = redis.ConnectionPool(host='127.0.0.1', port=6379, encoding='utf8', decode_responses=True)

r = redis.StrictRedis(connection_pool=pool)

key_list = r.keys()
group_list = []
for i in key_list:
    if "chat_content" in i:
        group_list.append(i[:i.find("_")])
print(group_list)

# mk = imageio.imread("/root/Jupyter/circle.png")
# w = wordcloud.WordCloud(mask=mk)
# 构建并配置词云对象w，注意要加scale参数，提高清晰度
w = wordcloud.WordCloud(width=800,
                        height=800,
                        background_color='white',
                        font_path='/root/Jupyter/hanyiqihei.ttf',
                        # mask=mk,
                        scale=5)

for group in group_list:
    start_time = float(time.time())
    # 生成词云图片
    jieba.enable_paddle()  # 启动paddle模式。 0.40版之后开始支持，早期版本不支持
    words = pseg.cut(r.get("{}_chat_content".format(group)), use_paddle=True)  # paddle模式
    word_list = []
    for word, flag in words:
        # print(word + "\t" + flag)
        if flag in ["n", "nr", "nz", "PER", "f", "ns", "LOC", "s", "nt", "ORG", "nw"]:
            # 判断该词是否有效，不为空格
            if re.match(r"^\s+?$", word) is None:
                word_list.append(word)
    # print(word_list)

    # 分析高频词
    word_amount = {}
    print(word_amount)
    for word in word_list:
        # 判断该词是否之前已经出现
        if word_amount.get(word) is not None:
            word_amount[word] = word_amount.get(word) + 1
        else:
            word_amount[word] = 1
    print(word_amount)
    word_amount = sorted(word_amount.items(), key=lambda kv: (kv[1]), reverse=True)
    print("排序后的热词：" + str(word_amount))
    hot_word_string = ""
    for i in range(min(5, len(word_amount))):
        hot_word_string += str(word_amount[i][0]) + "\t热度: " + str(word_amount[i][1]) + "\n"
    print(hot_word_string)
    # 获取消息总数
    total_message_amount = r.get("{}_total_message_amount".format(group))

    # 获取发言用户数
    user_amount = len(r.hkeys("{}_user_message_amount".format(group)))
    # 获取所有用户发言数字典
    user_message_amount = r.hgetall("-1001403536948_user_message_amount")
    user_message_amount = sorted(user_message_amount.items(), key=lambda kv: (kv[1]), reverse=True)
    print("排序后的用户：" + str(user_message_amount))
    top_5_user = ""
    for i in range(min(5, len(user_message_amount))):
        top_5_user += str(user_message_amount[i][0]) + "\t发言数: " + str(user_message_amount[i][1]) + "\n"
    print(top_5_user)
    string = " ".join(word_list)
    # 将string变量传入w的generate()方法，给词云输入文字
    w.generate(string)
    # 将词云图片导出到当前文件夹
    w.to_file('{}_chat_word_cloud.png'.format(group))

    stop_time = float(time.time())
    print("当前群组处理耗时：" + str(stop_time - start_time))
