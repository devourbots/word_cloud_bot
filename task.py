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
from config import TOKEN, FRONT, CHANNEL

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
        print("运行定时任务，向任务队列中添加任务，任务数量：{}".format(len(group_list)))
        for group in group_list:
            try:
                # 向任务队列中添加任务
                task_queue.put(group)
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
            ctext = f'#WORDCLOUD \n' \
                    f'群组 ID：`{group}`\n' \
                    f'执行操作：`生成词云`\n' \
                    f'结果：`成功`\n' \
                    f'处理耗时：`{str(stop_time - start_time)[:5]}`'
        except Exception as e:
            print("群组: {} | 处理失败，可能是机器人已经被移出群组，请检查报错！".format(group))
            print(e)
            ctext = f'#WORDCLOUD #SCHEDULE \n' \
                    f'群组 ID：`{group}`\n' \
                    f'执行操作：`生成词云`\n' \
                    f'结果：`失败`\n'
        if not CHANNEL == 0:
            bot.send_message(chat_id=CHANNEL, text=ctext, parse_mode="Markdown")
        time.sleep(1)


def add_task(group):
    task_queue.put(group)


# 核心函数，分词统计
def generate(group):
    mk = imageio.imread("circle.png")
    # 构建并配置词云对象w，注意要加scale参数，提高清晰度
    w = wordcloud.WordCloud(width=800,
                            height=800,
                            background_color='white',
                            font_path=FRONT,
                            mask=mk,
                            scale=5)
    r = connector.get_connection()
    print("当前处理的群组：" + str(group))
    # 生成词云图片
    jieba.enable_paddle()  # 启动paddle模式。 0.40版之后开始支持，早期版本不支持
    chat_content = r.get("{}_chat_content".format(group))

    if chat_content is None:
        print("数据库中不存在此群组 {} 数据".format(group))
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

    # 截至时间
    date = time.strftime("%Y年%m月%d日", time.localtime()) + ' ⏱ ' + time.strftime("%H:%M", time.localtime())
    text = f'📅 截至 {date}\n'
    # 分析高频词
    if len(word_list) > 0:
        word_amount = {}
        # print(word_amount)
        for word in word_list:
            if re.search(
                    r"[。|，|、|？|！|,|.|!|?|\\|/|+|\-|`|~|·|@|#|￥|$|%|^|&|*|(|)|;|；|‘|’|“|”|'|_|=|•|·|…|\"]",
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
                hot_word_string += "\t\t\t\t\t\t\t\t" + "👥 `" + str(word_amount[i][0]) + "`" + "：" + str(
                    word_amount[i][1]) + "\n"
            # print(hot_word_string)
            text += f"🗣️ 本群 {user_amount} 位成员共产生 {total_message_amount} 条发言\n" \
                    f"🤹‍ 大家今天讨论最多的是：\n\n{hot_word_string}\n"
        else:
            text += '无法分析出当前群组的热词列表，可能是数据量过小，嗨起来吧~\n'
    else:
        text += '无法分析出当前群组的热词列表，可能是数据量过小，嗨起来吧~\n'

    # 分析活跃用户
    if len(user_message_amount) > 0:
        # print("排序后的用户：" + str(user_message_amount))
        top_5_user = ""
        # 默认展示前5位，少于5个则全部展示
        for i in range(min(5, len(user_message_amount))):
            dis_name = str(user_message_amount[i][0])
            top_5_user += "\t\t\t\t\t\t\t\t" + "🎖 `" + dis_name[:min(10, len(dis_name))] + "`" + " 贡献：" + str(
                user_message_amount[i][1]) + "\n"
        # print(top_5_user)
        text += f"🏵 今日活跃用户排行榜：\n\n{top_5_user}"
    else:
        text = '无法分析出当前群组的活跃用户列表，可能是数据量过小，嗨起来吧~'

    # 开始创建词云
    img_path = 'images/default.png'
    try:
        string = " ".join(word_list)
        # 将string变量传入w的generate()方法，给词云输入文字
        w.generate(string)
        # 将词云图片导出到 images 文件夹
        w.to_file('images/{}_chat_word_cloud.png'.format(group))
        img_path = 'images/{}_chat_word_cloud.png'.format(group)
    except Exception as e:
        print(e)
        print("词云图片生成失败")

    # 发送结果
    try:
        bot.send_photo(
            chat_id=group,
            photo=open(img_path, "rb"),
            caption=text,
            parse_mode='Markdown',
            disable_notification=True
        )
    except Exception as e:
        print(e)
        r.delete('{}_chat_content'.format(group))
        print("发送结果失败")

    # 删除图片
    try:
        os.remove("images/{}_chat_word_cloud.png".format(group))
    except Exception as e:
        print(e)
        print("删除图片失败")


def flush_redis():
    r = connector.get_connection()
    r.flushall()
    print("已清空数据库")
