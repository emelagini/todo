from config import TOKEN
from telegram.ext import (
    Updater,
    Filters,
    MessageHandler,
    CommandHandler,
    ConversationHandler
)
from start_menu import start, main_menu
from interrupt import *
from constants import *


updater = Updater(TOKEN) # Обновляет чат в поисках новых сообщений
dispatcher = updater.dispatcher # распределительный центр

conv_handler = ConversationHandler( #обработчик диалога
    entry_points=[CommandHandler('start', start)], # точка входа в разговор
    states={ # этапы разговора
            MENU:[MessageHandler(Filters.text & ~Filters.command, main_menu)],
            MENU_ITEMS:[
                MessageHandler(Filters.text & ~Filters.command, wrong_message)
            ]
        },
    fallbacks=[CommandHandler('end', end)] # точка выхода из разговора
)


dispatcher.add_handler(conv_handler)

print('Сервер запущен!')
updater.start_polling()
updater.idle()  # ctrl + C
