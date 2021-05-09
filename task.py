import re
import queue
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

task_queue = queue.Queue()


def schedule_task():
    try:
        r = connector.get_connection()
        key_list = r.keys()
        group_list = []
        for i in key_list:
            if "chat_content" in i:
                group_list.append(i[:i.find("_")])
        # print(group_list)
        print("运行定时任务，让任务队列中添加任务，任务数量：{}".format(len(group_list)))
        for group in group_list:
            try:
                # 网任务队列中添加任务
                task_queue.put(group)
                # threading.Thread(target=generate, args=(group,)).start()
                # time.sleep(0.5)
            except Exception as e:
                print("群组：{} | 词云数据分析生成失败，请查看报错信息".format(group))
                print(e)
                continue
    except Exception as e:
        print("数据库连接失败，请查看报错信息")
        print(e)


def do_task():
    while True:
        group = task_queue.get()
        try:
            print("---------------------------")
            print("群组: {} | 分析处理中... | 剩余任务数量 {}".format(group, task_queue.qsize()))
            start_time = float(time.time())
            generate(group)
            stop_time = float(time.time())
            print("当前群组处理耗时：" + str(stop_time - start_time))
            print("---------------------------")
        except Exception as e:
            print("群组: {} | 处理失败，可能是机器人已经被移出群组，请检查报错！".format(group))
            print(e)
        time.sleep(1)


def add_task(group):
    task_queue.put(group)


# 核心函数，分词统计
def generate(group):
    mk = imageio.imread("/root/word_cloud_bot/circle.png")
    # 构建并配置词云对象w，注意要加scale参数，提高清晰度
    w = wordcloud.WordCloud(width=800,
                            height=800,
                            background_color='white',
                            font_path='/root/word_cloud_bot/font.ttf',
                            mask=mk,
                            scale=5)
    r = connector.get_connection()
    print("当前处理的群组：" + str(group))
    # 生成词云图片
    jieba.enable_paddle()  # 启动paddle模式。 0.40版之后开始支持，早期版本不支持
    chat_content = r.get("{}_chat_content".format(group))

    if chat_content is None:
        print("数据库中不存在此群组数据")
        try:
            time.sleep(1)
            bot.send_message(
                chat_id=group,
                text="数据库中不存在群组数据，请检查是否授予机器人管理员权限，并通过聊天添加数据量，嗨起来吧~\n"
            )
        except Exception as e:
            print("群组: {} | 机器人发送信息失败".format(group))
        return
    word_list = []
    words = pseg.cut(chat_content, use_paddle=True)  # paddle模式
    for word, flag in words:
        # print(word + "\t" + flag)
        if flag in ["n", "nr", "nz", "PER", "f", "ns", "LOC", "s", "nt", "ORG", "nw"]:
            # 判断该词是否有效，不为空格
            if re.match(r"^\s+?$", word) is None:
                word_list.append(word)
        # print(word_list)

    # 获取消息总数
    total_message_amount = r.get("{}_total_message_amount".format(group))

    # print("总发言数: " + total_message_amount)

    # 获取发言用户数
    user_amount = len(r.hkeys("{}_user_message_amount".format(group)))
    # 获取所有用户发言数字典
    user_message_amount = r.hgetall("{}_user_message_amount".format(group))
    user_message_amount = sorted(user_message_amount.items(), key=lambda kv: (int(kv[1])), reverse=True)

    if len(word_list) > 0:
        # 分析高频词
        word_amount = {}
        # print(word_amount)
        for word in word_list:
            if re.search(
                    r"[。|，|、|？|！|,|.|!|?|\\|/|+|\-|`|~|·|@|#|￥|$|%|^|&|*|(|)|;|；|‘|’|“|”|'|_|=|\"]",
                    word) is not None:
                continue
            # 判断该词是否之前已经出现
            if word_amount.get(word) is not None:
                word_amount[word] = word_amount.get(word) + 1
            else:
                word_amount[word] = 1
        # print(word_amount)
        word_amount = sorted(word_amount.items(), key=lambda kv: (int(kv[1])), reverse=True)
        if len(word_amount) > 0:
            # print("排序后的热词：" + str(word_amount))
            hot_word_string = ""
            # 默认展示前5位，少于5个则全部展示
            for i in range(min(5, len(word_amount))):
                hot_word_string += "\t\t\t\t\t\t\t\t" + "`" + str(word_amount[i][0]) + "`" + ": " + str(
                    word_amount[i][1]) + "\n"
            # print(hot_word_string)
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
    else:
        bot.send_message(
            chat_id=group,
            text="当前聊天数据量过小，嗨起来吧~"
        )

    if len(user_message_amount) > 0:
        # print("排序后的用户：" + str(user_message_amount))
        top_5_user = ""
        # 默认展示前5位，少于5个则全部展示
        for i in range(min(5, len(user_message_amount))):
            top_5_user += "\t\t\t\t\t\t\t\t" + "🎖`" + str(user_message_amount[i][0]) + "`" + " 贡献: " + str(
                user_message_amount[i][1]) + "\n"
        # print(top_5_user)
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
    else:
        bot.send_message(
            chat_id=group,
            text="当前聊天数据量过小，嗨起来吧~"
        )

    try:
        string = " ".join(word_list)
        # 将string变量传入w的generate()方法，给词云输入文字
        w.generate(string)
        # 将词云图片导出到当前文件夹
        w.to_file('{}_chat_word_cloud.png'.format(group))
        bot.send_photo(
            chat_id=group,
            photo=open("{}_chat_word_cloud.png".format(group), "rb")
        )
        os.remove("{}_chat_word_cloud.png".format(group))
    except Exception as e:
        print(e)
        print("词云图片生成失败")
        # bot.send_message(
        #     chat_id=group,
        #     text="当前聊天数据量过小，嗨起来吧~"
        # )


def flush_redis():
    r = connector.get_connection()
    r.flushall()
    print("已清空数据库")
