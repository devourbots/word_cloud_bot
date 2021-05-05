# encoding=utf-8
import jieba
import jieba.posseg as pseg
import time  # 引入time模块

import redis

import connector
test_word = '''
📜 ZUOLUOTV 例行群规广播 📜
📅 2021年5月5日
⏱ 截至今天08:00 本群共有11374位群友
————————————
⚖️ 自由并不意味着没有规则，群内稳定和持续的交流氛围，依靠的是大家对规则的尊重。
————————————
📖 ZUOLUOTV群管理规范 📖 
🈯 本群提倡一切事务合法合规操作
🔞 不允许传播违法、黑灰产相关内容

1.必Ban:传播黑灰产，贩卖手机卡、银行卡、个人信息。
2.必Ban:传播色情、暴力、低俗内容。
3.必Ban:群发广告，ID或头像中带广告。
4.别聊政治敏感话题，不鼓励聊翻墙、机场等话题，原因请看WHY。
5.别搞人身攻击，别搞地域黑，别发布仇恨言论，别骚扰异性。
6.别做伸手党，先看资料索引，学会谷歌搜索、善看群聊记录。
7.不要用语音，不要连续刷屏，恶意刷屏将被Ban。
8.鼓励原创分享，分享外链尽量是科技、数码、摄影、旅行主题。
9.违反群规者，飞机场见✈，异议可私信管理员，精力时间有限，私聊不解答公开问题。

'''

start_time = float(time.time())
# words = pseg.cut("我爱北京天安门")  # jieba默认模式
jieba.enable_paddle()  # 启动paddle模式。 0.40版之后开始支持，早期版本不支持
words = pseg.cut(test_word, use_paddle=True)  # paddle模式
word_list = []
for word, flag in words:
    # print(word + "\t" + flag)
    if flag in ["n", "nr", "nz", "PER", "f", "ns", "LOC", "s", "nt", "ORG", "nw"]:
        word_list.append(word)
        r = connector.get_connection()
        r.set('foo', 'Bar')
        print(r.get('foo'))
print(word_list)
stop_time = float(time.time())
print(stop_time - start_time)

