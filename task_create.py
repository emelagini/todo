from stickers import *
from telegram.ext import (
    Filters,
    MessageHandler,
    CommandHandler,
    ConversationHandler, 
    CallbackContext,
    CallbackQueryHandler
)
from telegram import Update
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from constants import *
from datetime import date



RU_LSTEP = {'y': 'год', 'm': 'месяц', 'd': 'день'}


def add_task(update: Update, context: CallbackContext):
    name = update.effective_user.first_name
    update.message.reply_sticker(ADD_STICKER)
    update.message.reply_text(f"Просьба ввести текст дела, мастер {name} или /no чтобы прекратить операцию добавления")
    return TASK

def handle_task_text(update: Update, context: CallbackContext):
    message = update.message.text # взяли сообщение, где пользователь пишет текст дела
    context.user_data["todo_text"] = message # сохранили это в рюкзак
   # update.message.reply_text(message)
    calendar, step = DetailedTelegramCalendar(locale="ru",min_date=date.today()).build()
    context.bot.send_message(update.effective_chat.id,
                     f"Выберите {RU_LSTEP[step]}",
                     reply_markup=calendar)
    return DATE


def  handle_date (update: Update, context: CallbackContext):
    result, key, step = DetailedTelegramCalendar(locale="ru",min_date=date.today()).process(update.callback_query.data)
    if not result and key:
            context.bot.send_message(update.effective_chat.id,
                                      f"Выберите {RU_LSTEP[step]}", reply_markup=key)
    elif result:
            context.bot.send_message(update.effective_chat.id,
                                       f"Вы выбрали {result}",)
                                                            








def endpoint(update: Update, context: CallbackContext):
    update.message.reply_sticker(ENDPOINT_STICKER)
    update.message.reply_text('Операция прервана')
    return ConversationHandler.END # завершает диалог о добавлении дела
add_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex(f"^{CREATE}$"), add_task)],
    states={
        TASK: [MessageHandler(Filters.text & ~Filters.command, handle_task_text)],
        DATE:[CallbackQueryHandler(handle_date,DetailedTelegramCalendar.func())]
    },
    fallbacks=[CommandHandler("no", endpoint)],
)
