import datetime
import threading

import telegram
from telegram import InlineKeyboardMarkup, InlineKeyboardButton, ForceReply
from telegram.ext import CommandHandler, MessageHandler, Filters, ConversationHandler, CallbackQueryHandler
from config import TOKEN
import sqlite3
import time
import os
import importlib
import requests

bot = telegram.Bot(token=TOKEN)


def start(update, context):
    print('进入start函数')
    update.message.reply_text(
        '您好！',
    )


def chat_content_exec(update, context):
    chat_id = update.effective_message.chat_id
    print(chat_id)


start_handler = CommandHandler('start', start)
chat_content_handler = MessageHandler(Filters.text, chat_content_exec),
