from telegram.ext import Updater
from config import TOKEN
from func import start_handler, chat_content_handler, check_schedule, rank_handler
import schedule
from task import schedule_task, flush_redis, do_task
import threading

schedule.every().day.at('11:00').do(schedule_task)
schedule.every().day.at('18:00').do(schedule_task)
schedule.every().day.at('23:30').do(schedule_task)
schedule.every().day.at('23:59').do(flush_redis)

# 测试代码，每分钟推送数据，非测试目的不要取消注释下一行
# schedule.every(1).minutes.do(schedule_task)

# 开启分析线程，当队列中由任务时，会取出任务分析生成数据
threading.Thread(target=do_task).start()

threading.Thread(target=check_schedule).start()

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(start_handler)
dispatcher.add_handler(rank_handler)
dispatcher.add_handler(chat_content_handler)

updater.start_polling()
updater.idle()
