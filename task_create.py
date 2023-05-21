from stickers import *
from telegram.ext import (
    Filters,
    MessageHandler,
    CommandHandler,
    ConversationHandler, 
    CallbackContext,
    CallbackQueryHandler
)
from telegram import Update, InlineKeyboardMarkup,InlineKeyboardButton
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from constants import *
from interrupt import *
from datetime import date

class MyStyleCalendar(DetailedTelegramCalendar):
 # previous and next buttons style. they are emoji now!
    prev_button = "⬅️"
    next_button = "➡️"
    # you do not want empty cells when month and year are being selected
    empty_month_button = ""
    empty_year_button = ""
    middle_button_year = ""



def add_task(update: Update, context: CallbackContext):
    name = update.effective_user.first_name
    update.message.reply_sticker(ADD_STICKER)
    update.message.reply_text(f"Просьба ввести текст дела, мастер {name} или /no чтобы прекратить операцию добавления")
    return TASK

def handle_task_text(update: Update, context: CallbackContext):
    message = update.message.text # взяли сообщение, где пользователь пишет текст дела
    context.user_data["todo_text"] = message # сохранили это в рюкзак
   # update.message.reply_text(message)
    calendar, step = MyStyleCalendar(locale="ru",min_date=date.today()).build()
    context.bot.send_message(update.effective_chat.id,
                     f"Выберите {RU_LSTEP[step]}",
                     reply_markup=calendar)
    return DATE


def  handle_date (update: Update, context: CallbackContext):
    result, key, step =MyStyleCalendar(locale="ru",min_date=date.today()).process(update.callback_query.data)
    if not result and key:
            context.bot.send_message(update.effective_chat.id,
                                      f"Выберите {RU_LSTEP[step]}", reply_markup=key)
    elif result:
            delete_message(update,context,end= 3)
            year, month, day = str(result).split("-")
            true_date = day + "." + month + "." + year
            context.bot.send_message(update.effective_chat.id,
                                       f"Вы выбрали {true_date}",)
            return HOUR
                                                            

def  handle_hour (update: Update, context: CallbackContext):
     keyboard = []
     step = {0:0,1:6,2:12, 3:18}
     for line in range(4):
          keyboard.append([])
          for column in range(6): 
               hour = column +step[line]
               if hour < 10:
                    hour = "0" +str(hour)
               keyboard[line].append(InlineKeyboardButton(text=f"{hour}:00",callback_data=f"{hour}:00"))
     markup = InlineKeyboardMarkup(keyboard)
     complex.context.bot.send_message(update.effective_chat.id,
                                       f"Выберите час окончание задачи", reply_markup = markup)






add_handler = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex(f"^{CREATE}$"), add_task)],
    states={
        TASK: [MessageHandler(Filters.text & ~Filters.command, handle_task_text)],
        DATE:[CallbackQueryHandler(handle_date,DetailedTelegramCalendar.func())],
        HOUR: [CallbackQueryHandler(handle_hour,)]
    },
    fallbacks=[CommandHandler("no", endpoint)],
)
