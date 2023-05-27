from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CallbackContext, ConversationHandler
from stickers import *
from constants import *
from file_work import init




def start(update: Update, context: CallbackContext):
    init(update, context)
    mark_up = [[GO]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=mark_up,
        resize_keyboard=True,
        one_time_keyboard=True,
        input_field_placeholder=f'Нажми на кнопку "{GO}", чтобы продолжить'
    )
    name = update.effective_user.first_name
    update.message.reply_sticker(START_STICKER)
    context.bot.send_message(update.effective_chat.id,f"Приветствую тебя в списке задач, {name}!")
    context.bot.send_message(update.effective_chat.id,f"В этом боте ты можешь\n-создать задачу\n-изменить задачу\n-посмотреть имеющиеся\n-удалить задачу\n-отметить задачу выполненной ",
                              reply_markup=keyboard)
    return MENU


def main_menu(update: Update, context: CallbackContext):
    menu = [[READ], [CREATE, DONE], [UPDATE, DELETE]]
    keyboard = ReplyKeyboardMarkup(
        keyboard=menu,
        resize_keyboard=True,
        one_time_keyboard=True
    )
    name = update.effective_user.full_name
    context.bot.reply_sticker(MAIN_MENU_STICKER)
    context.bot.reply_text(
        f'Выберите, что хотите сделать, мастер {name}?', reply_markup=keyboard)
    return MENU_ITEMS   