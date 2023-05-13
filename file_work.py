from telegram import Update
from telegram.ext import CallbackContext
import os

def init(update: Update, context: CallbackContext):
    username = update.effective_user.username
    file = f'database/{username}.scv'
    if not os.path.exists("database"):
        os.mkdir("database")
    if not os.path.exists(file):
        open(file,"w")