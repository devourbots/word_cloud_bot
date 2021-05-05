from telegram.ext import Updater
from config import TOKEN
from func import start_handler, chat_content_handler

updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(start_handler)
dispatcher.add_handler(chat_content_handler)

updater.start_polling()
updater.idle()
