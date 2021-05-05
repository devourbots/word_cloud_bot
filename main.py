from telegram.ext import Updater
from config import TOKEN
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler
import sqlite3
from func import start, reserve, run, kill, status, update, get


updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher


start_handler = CommandHandler('start', start)
reserve_handler = CommandHandler('reserve', reserve)
run_handler = CommandHandler('run', run)
kill_handler = CommandHandler('kill', kill)
update_handler = CommandHandler('update', update)
status_handler = CommandHandler('status', status)
get_handler = CommandHandler('get', get)


dispatcher.add_handler(start_handler)
dispatcher.add_handler(reserve_handler)
dispatcher.add_handler(run_handler)
dispatcher.add_handler(kill_handler)
dispatcher.add_handler(update_handler)
dispatcher.add_handler(status_handler)
dispatcher.add_handler(get_handler)

updater.start_polling()
updater.idle()
