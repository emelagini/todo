from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import CallbackContext, ConversationHandler
from stickers import *



def end(update: Update, context: CallbackContext):
    update.message.reply_photo(
        "https://myslide.ru/documents_7/c2d573d9e648a68842706b978ad351da/img17.jpg", 
        reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def wrong_message(update: Update, context: CallbackContext):
    update.message.reply_sticker(WRONG_COMMAND_STICKER)
    update.message.reply_text('Упс! Такой команды не существует')