import datetime
import threading
import connector

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
    r = connector.get_connection()
    text = update.message.text
    chat_type = update.effective_chat.type
    user_id = update.effective_user.id
    chat_id = update.effective_message.chat_id
    print("\n---------------------------")
    print("内容: " + text)
    print("群组类型: " + str(chat_type))
    print("用户ID: " + str(user_id))
    print("chat_id: " + str(chat_id))
    if "/" in text:
        print("这是一条指令信息，跳过")
    else:
        if text[-1] not in ["，", "。", "！", "：", "？", "!", "?", ",", ":", "."]:
            r.append("{}_chat_content".format(chat_id), text + "。")
        else:
            r.append("{}_chat_content".format(chat_id), text)
        r.incrby("{}_total_message_amount".format(chat_id))
        r.hincrby("{}_user_message_amount".format(chat_id), user_id)
    print("---------------------------")


start_handler = CommandHandler('start', start)
chat_content_handler = MessageHandler(Filters.text, chat_content_exec)
