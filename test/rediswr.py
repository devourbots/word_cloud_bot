import redis
# encoding=utf-8
import jieba
import wordcloud
import jieba.posseg as pseg
# 导入imageio库中的imread函数，并用这个函数读取本地图片，作为词云形状图片
import imageio
import time  # 引入time模块

pool = redis.ConnectionPool(host='127.0.0.1', port=6379, encoding='utf8', decode_responses=True, db=0)
start_time = float(time.time())
r = redis.StrictRedis(connection_pool=pool)
with open("/root/Jupyter/143751443703354.txt", "r") as file:
    i = 0
    for line in file.readlines():
        i += 1
        r.append("maozedong", line)
        if i == 10:
            break
#     content = file.read()
# print(content)
print(r.get("maozedong"))

mk = imageio.imread("/root/Jupyter/circle.png")
w = wordcloud.WordCloud(mask=mk)

# 构建并配置词云对象w，注意要加scale参数，提高清晰度
w = wordcloud.WordCloud(width=800,
                        height=800,
                        background_color='white',
                        font_path='/root/Jupyter/hanyiqihei.ttf',
                        mask=mk,
                        scale=5)

# 对来自外部文件的文本进行中文分词，得到string

jieba.enable_paddle()  # 启动paddle模式。 0.40版之后开始支持，早期版本不支持
words = pseg.cut(r.get("maozedong"), use_paddle=True)  # paddle模式
word_list = []
for word, flag in words:
    # print(word + "\t" + flag)
    if flag in ["n", "nr", "nz", "PER", "f", "ns", "LOC", "s", "nt", "ORG", "nw"]:
        word_list.append(word)

string = " ".join(word_list)


# 将string变量传入w的generate()方法，给词云输入文字
w.generate(string)

# 将词云图片导出到当前文件夹
w.to_file('maozedong-3.png')


stop_time = float(time.time())
print(stop_time - start_time)
