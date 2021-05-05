from telegram.ext import Updater
from config import TOKEN
from func import start_handler, chat_content_handler, check_schedule
import schedule
import task
import threading

# schedule.every().day.at('16:20').do(task).tag('task')
schedule.every(1).minutes.do(task).tag('task')

threading.Thread(target=check_schedule).start()

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(start_handler)
dispatcher.add_handler(chat_content_handler)

updater.start_polling()
updater.idle()
