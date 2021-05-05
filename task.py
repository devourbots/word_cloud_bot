import re
import jieba
import jieba.posseg as pseg
import wordcloud
import imageio
import telegram
import time
import os
import connector
from config import TOKEN

bot = telegram.Bot(token=TOKEN)

r = connector.get_connection()

key_list = r.keys()
group_list = []
for i in key_list:
    if "chat_content" in i:
        group_list.append(i[:i.find("_")])
# print(group_list)

mk = imageio.imread("/root/word_cloud_bot/circle.png")
# 构建并配置词云对象w，注意要加scale参数，提高清晰度
w = wordcloud.WordCloud(width=800,
                        height=800,
                        background_color='white',
                        font_path='/root/word_cloud_bot/font.ttf',
                        mask=mk,
                        scale=5)

for group in group_list:
    try:
        print("当前处理的群组：" + str(group))
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
        # print(word_amount)
        for word in word_list:
            # 判断该词是否之前已经出现
            if word_amount.get(word) is not None:
                word_amount[word] = word_amount.get(word) + 1
            else:
                word_amount[word] = 1
        # print(word_amount)
        word_amount = sorted(word_amount.items(), key=lambda kv: (kv[1]), reverse=True)
        # print("排序后的热词：" + str(word_amount))
        hot_word_string = ""
        for i in range(min(5, len(word_amount))):
            hot_word_string += "\t\t\t\t\t\t\t\t" + "`" + str(word_amount[i][0]) + "`" + ": " + str(
                word_amount[i][1]) + "\n"
        # print(hot_word_string)
        # 获取消息总数
        total_message_amount = r.get("{}_total_message_amount".format(group))

        # print("总发言数: " + total_message_amount)

        # 获取发言用户数
        user_amount = len(r.hkeys("{}_user_message_amount".format(group)))
        # 获取所有用户发言数字典
        user_message_amount = r.hgetall("-1001403536948_user_message_amount")
        user_message_amount = sorted(user_message_amount.items(), key=lambda kv: (kv[1]), reverse=True)
        # print("排序后的用户：" + str(user_message_amount))
        top_5_user = ""
        for i in range(min(5, len(user_message_amount))):
            top_5_user += "\t\t\t\t\t\t\t\t" + "🎖`" + str(user_message_amount[i][0]) + "`" + " 贡献: " + str(
                user_message_amount[i][1]) + "\n"
        # print(top_5_user)
        string = " ".join(word_list)
        # 将string变量传入w的generate()方法，给词云输入文字
        w.generate(string)
        # 将词云图片导出到当前文件夹
        w.to_file('{}_chat_word_cloud.png'.format(group))
        bot.send_message(
            chat_id=group,
            text="🎤 今日话题榜 🎤\n"
                 "📅 {}\n"
                 "⏱ 截至今天{}\n"
                 "🗣️ 本群{}位朋友共产生{}条发言\n"
                 "🤹‍ 大家今天讨论最多的是：\n\n"
                 "{}\n"
                 "看下有没有你感兴趣的话题? 👏".format(
                time.strftime("%Y年%m月%d日", time.localtime()),
                time.strftime("%H:%M", time.localtime()),
                user_amount,
                total_message_amount,
                hot_word_string),
            parse_mode="Markdown"
        )

        bot.send_message(
            chat_id=group,
            text="🏵 今日活跃用户排行榜 🏵\n"
                 "📅 {}\n"
                 "⏱ 截至今天{}\n\n"
                 "{}\n"
                 "感谢这些朋友今天的分享! 👏 \n"
                 "遇到问题,向他们请教说不定有惊喜😃".format(
                time.strftime("%Y年%m月%d日", time.localtime()),
                time.strftime("%H:%M", time.localtime()),
                top_5_user),
            parse_mode="Markdown"
        )

        bot.send_photo(
            chat_id=group,
            photo=open("{}_chat_word_cloud.png".format(group), "rb")
        )

        os.remove("{}_chat_word_cloud.png".format(group))

        stop_time = float(time.time())
        print("当前群组处理耗时：" + str(stop_time - start_time))
    except Exception as e:
        print(e)
        continue
r.flushall()
print("已清空数据库")
