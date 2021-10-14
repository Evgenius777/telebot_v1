from collections import UserList
from telegram import Bot, update
from telegram import Update
from telegram.utils.helpers import effective_message_type
from  telegram.utils.request import Request
from datetime import datetime
from  telegram.ext import CallbackContext, updater
from  telegram.ext import (Filters, Updater, MessageHandler, CommandHandler)

TOKEN = '2031737196:AAHOl2_R1H9gkyymCKtmPHlaiYSD7ywH2DU'
#PROXY_URL = 'https://telegg.ru/orig/bot'
BASE_URL = 'https://api.telegram.org/bot'
ADMIN_ID = [2031737196, 1871830224]
#испльзую эту функцию как декоратор для отлова ошибки  @log_error
def log_error(f):
    
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)

        except Exception as e:
            error_message = f'[ADMIN] Произошла ошибка: {e}'
            print(error_message)

            update = args[0]
            if update and hasattr(update, 'message'):
                update.message.bot.send_message(
                    chat_id = ADMIN_ID,
                    text = error_message,
                )
                #chat_id = update.message.chat_id
                #if chat_id in ADMIN_ID:
                #    update.message.reply_text(
                #       text = error_message,
                #    )
            raise e
    return inner

def admin_access(f):

    def inner(*args, **kwargs):
        update = args[0]
        if update and hasattr(update, 'message'):
            chat_id = update.message.chat_id
            if chat_id in ADMIN_ID:
                print('Доступ разрешен!!!')
                return f(*args, **kwargs)
            else:
                print('Доступ не разрешен!')
        else:
            print('Нет аргумента update')
    return inner

@log_error
@admin_access
def start(update: Update, context: CallbackContext):

    effective_name = update.effective_name()
    reply_text = 'Привет, format(effective_name)\n Для продолжения нажми далее'
    update.message.reply_text(
        text = reply_text,
        )


@log_error
@admin_access
def do_echo(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text
   
    reply_text = "Ваш ID = {}\n\n{}".format(chat_id, text)
    update.message.reply_text(
        text=reply_text,
    )
@admin_access    
@log_error
def secret_cmd(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    if chat_id not in ADMIN_ID:
        return
    update.message.reply_text(
        text = 'секрет!'
    )

@log_error
def main():
    
    req = Request(
        connect_timeout=0.5,
        read_timeout=1.0,
    )
    bot = Bot(
        token = TOKEN,
        request = req,
        base_url=BASE_URL,  
    )
    print(bot.get_me())  
    updater = Updater(
        bot=bot,
        use_context=True,
    )
    start_message = CommandHandler('start', start)
    updater.dispatcher.add_handler(start_message)

    message_handler = MessageHandler(Filters.text, do_echo)
    updater.dispatcher.add_handler(message_handler)

    command1 = CommandHandler('secret', secret_cmd)
    updater.dispatcher.add_handler(command1)

    updater.start_polling()
    updater.idle()

if __name__=='__main__':
    main()
