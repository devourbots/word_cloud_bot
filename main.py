from telegram.ext import Updater
from config import TOKEN
from func import start_handler, chat_content_handler, check_schedule
import schedule
from task import do_task
import threading

schedule.every().day.at('23:30').do(do_task).tag('task')
# schedule.every(1).minutes.do(do_task).tag('task')

threading.Thread(target=check_schedule).start()

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(start_handler)
dispatcher.add_handler(chat_content_handler)

updater.start_polling()
updater.idle()
