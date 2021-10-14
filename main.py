import datetime
import logging
import queue
from functools import update_wrapper
from logging import Logger, getLogger

from telegram import CallbackQuery, InlineKeyboardMarkup, Update, replymarkup
from telegram.ext import (CommandHandler, Filters, MessageHandler, Updater,
                          updater)
from telegram.ext.callbackcontext import CallbackContext
from telegram.ext.callbackqueryhandler import CallbackQueryHandler
from telegram.inline.inlinekeyboardbutton import InlineKeyboardButton
from telegram.utils.request import Request

from auth_data import token
from echo_v.utils import logger_factory

"""
logger = getLogger(__name__)
logger_requests = logger_factory(logger=logger)
"""

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', #level,
)
logger = logging.getLogger(__name__)


def message_handler(update: Update, context: CallbackContext):
    update.message.reply_text(
        text="Привет тебе мой юный падаван, если ты хочешь окунуться в мир непознанного, жмякай кнопку далее"
    )


def help_command(update: Update, context: CallbackContext):
    update.message.reply_text("Для запуска с самого начала нажми /start")

def start(update: Update, context: CallbackContext):
    #answer_help = help_command()

    keyboard = [
        InlineKeyboardButton("Сколько стоит", callback_data='1'),
        InlineKeyboardButton("Помощь", callback_data='Для запуска с самого начала нажми /start'),
    ],
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('После нажатия кнопки "сколько стоит"\n введите текст для поиска: ', reply_markup=reply_markup)

def button(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()
    query.edit_message_text(text=f"Выбран параметр: {query.data}")





def main():
    logger.info("запускаем бота...")
    print('start')

    reg = Request(
        connect_timeout=0.5,
        read_timeout=1.0,
    )
    updater=Updater(
        token,
        use_context=True
    )




    updater.dispatcher.add_handler(CommandHandler('start', start))

    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    updater.dispatcher.add_handler(CommandHandler('help', help_command))

    handler = MessageHandler(Filters._Command, message_handler)
    updater.dispatcher.add_handler(handler)

    updater.start_polling()
    updater.idle()

if __name__=='__main__':
    main()
