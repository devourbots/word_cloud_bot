group_name = '-1001403536948_chat_content'

print(group_name[:group_name.find("_")])

word_amount = {}

word_amount['y1111'] = 1
word_amount['y2222'] = 2
word_amount['y3333'] = 4
word_amount['y4444'] = 3

print(word_amount.get("123"))
print(word_amount.get("y4444"))

print(word_amount)
word_amount = sorted(word_amount.items(), key=lambda word: (word[1]))
print(word_amount)

print("--------------")
import re

str = '''
   23
'''

rst = re.match(r"^\s+?$", str)

print(rst)

import time

print(time.strftime("%Y年%m月%d日", time.localtime()))
print(time.strftime("%H:%M", time.localtime()))
