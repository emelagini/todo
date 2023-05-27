from telegram import Update
from telegram.ext import CallbackContext
import os
import csv

def init(update: Update, context:CallbackContext):
    username = update.effective_user.username
    file = f'database/{username}.scv'
    context.user_data["file"] = file
    if not os.path.exists("database"):
        os.mkdir("database")
    if not os.path.exists(file):
        open(file,"w")





def read_csv(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        todos =  list(csv.reader(file, delimiter='|'))
        return todos

    


def write_csv(filename,line_to_write):
    with open(filename, 'a', encoding='utf-8') as file:
        worker = csv.writer(file, delimiter='|',lineterminator='\n')  # \n - это перенос
        worker.writerow(line_to_write)





def read_todos(update: Update, context:CallbackContext):
    file = context.user_data["file"]
    todos = read_csv(file)
    message = ""
    for number, todo in enumerate(todos):
        text, date, time = todo
        update.message.reply_text(f"""Todo №{number}
                                        {text}
                                        Дедлайн:{date} {time}
                                        \n\n
                                        """)