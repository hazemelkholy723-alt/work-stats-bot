import os
from telegram.ext import Updater, CommandHandler

TOKEN = "8558249602:AAG8Snts-MGowIJPFRiok9W3XD7DPujlWMQ"

def get_id(update, context):
    update.message.reply_text(f"الأيدي بتاع المجموعة دي هو: {update.effective_chat.id}")

def main():
    updater = Updater(TOKEN, use_context=True)
    updater.dispatcher.add_handler(CommandHandler("get_id", get_id))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
